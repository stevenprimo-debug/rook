#!/usr/bin/env bash
# context-watch-gate.sh -- bash port of context-watch-gate.ps1
# Event: UserPromptSubmit
# Proactive context-usage monitor. Closes the gap that PreCompact (harness-fired
# near 100%) is too late to save in-flight work.
#
# Reads the session transcript JSONL provided in the stdin payload, walks the
# usage blocks to compute the CURRENT resident context (latest usage block,
# matches what Claude Code's UI shows), and emits:
#   - silent pass below ROOK_CONTEXT_WARN_PCT (default 70)
#   - visible chat warning between warn and hardstop
#   - system-reminder HARD STOP at ROOK_CONTEXT_HARDSTOP_PCT (default 85)
#
# Token-counting algorithm:
#   For each usage block: effective = input + cache_creation + cache_read.
#   Track LATEST (file-order) such block. The harness auto-compacts on overflow,
#   so the peak watermark earlier in the session is NOT current resident size.
#   Also track session peak for the warning body.
#
# Model-window detection:
#   The JSONL "model" field is bare "claude-opus-4-7" for both 200K and 1M
#   variants -- Anthropic does not include the [1m] suffix. So if any usage
#   block sum > 200K, the session must be on the 1M variant. The explicit
#   [1m]/-1m/_1m regex is kept as a secondary signal.
#
# Config env vars:
#   ROOK_CONTEXT_WARN_PCT       default 70
#   ROOK_CONTEXT_HARDSTOP_PCT   default 85
#   ROOK_CONTEXT_WATCH_DISABLED set to "1" to silence entirely
#   CLAUDE_MAX_CONTEXT_TOKENS   default 200000 (explicit override)
#
# Any failure -> exit 0 silently. Never break user prompt submission.

set -u

# Escape hatch
if [ "${ROOK_CONTEXT_WATCH_DISABLED:-}" = "1" ]; then
    exit 0
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Thresholds
WARN_PCT="${ROOK_CONTEXT_WARN_PCT:-70}"
STOP_PCT="${ROOK_CONTEXT_HARDSTOP_PCT:-85}"
case "$WARN_PCT" in ''|*[!0-9]*) WARN_PCT=70 ;; esac
case "$STOP_PCT" in ''|*[!0-9]*) STOP_PCT=85 ;; esac
if [ "$STOP_PCT" -le "$WARN_PCT" ]; then
    STOP_PCT=$((WARN_PCT + 10))
    [ "$STOP_PCT" -gt 99 ] && STOP_PCT=99
fi

MAX_CONTEXT="${CLAUDE_MAX_CONTEXT_TOKENS:-200000}"
ENV_OVERRIDE=0
if [ -n "${CLAUDE_MAX_CONTEXT_TOKENS:-}" ]; then
    case "$CLAUDE_MAX_CONTEXT_TOKENS" in ''|*[!0-9]*) ;; *) ENV_OVERRIDE=1 ;; esac
fi
case "$MAX_CONTEXT" in ''|*[!0-9]*) MAX_CONTEXT=200000 ;; esac

RAW=$(cat 2>/dev/null || true)
[ -z "$RAW" ] && exit 0

HAVE_JQ=0
command -v jq >/dev/null 2>&1 && HAVE_JQ=1

if [ "$HAVE_JQ" = "1" ]; then
    CWD=$(printf '%s' "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
    TRANSCRIPT=$(printf '%s' "$RAW" | jq -r '.transcript_path // empty' 2>/dev/null)
else
    CWD=$(printf '%s' "$RAW" | grep -o '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"cwd"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
    TRANSCRIPT=$(printf '%s' "$RAW" | grep -o '"transcript_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"transcript_path"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
fi

[ -z "$TRANSCRIPT" ] && exit 0
[ ! -f "$TRANSCRIPT" ] && exit 0

resolve_vault_root() {
    if [ -n "${PRIMOLABS_VAULT_ROOT:-}" ] && [ -d "$PRIMOLABS_VAULT_ROOT" ]; then
        echo "$PRIMOLABS_VAULT_ROOT"; return
    fi
    local parent="$(dirname "$SCRIPT_DIR")"
    if [ -d "$parent" ]; then echo "$parent"; return; fi
    local cur="$CWD"
    for _ in 1 2 3 4 5 6; do
        [ -z "$cur" ] && break
        if [ -d "$cur/agents" ] && [ -d "$cur/hooks" ]; then echo "$cur"; return; fi
        cur="$(dirname "$cur")"
        [ "$cur" = "/" ] && break
    done
    echo ""
}

LATEST_EFFECTIVE=0
PEAK_EFFECTIVE=0
USAGE_EXCEEDS_200K=0
MODEL_1M=0
MODEL_200K=0
TOTAL_CHARS=0

if [ "$HAVE_JQ" = "1" ]; then
    # Per-line: emit the input+cache_creation+cache_read sum for usage lines.
    SUMS=$(jq -rc '
        ((.message.usage // .usage) // null)
        | if . == null then empty
          else ((.input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0))
          end
    ' "$TRANSCRIPT" 2>/dev/null)
    if [ -n "$SUMS" ]; then
        # awk computes: latest non-zero, peak, and 1M evidence flag.
        read LATEST_EFFECTIVE PEAK_EFFECTIVE USAGE_EXCEEDS_200K <<EOF
$(printf '%s\n' "$SUMS" | awk 'BEGIN{latest=0; peak=0; exc=0} {v=$1+0; if(v>0){latest=v; if(v>peak)peak=v; if(v>200000)exc=1}} END{print latest" "peak" "exc}')
EOF
    fi

    # Model hint scan -- secondary signal only (today's JSONL strips the [1m] suffix).
    MODELS=$(jq -rc '((.message.model // .model) // "") | ascii_downcase' "$TRANSCRIPT" 2>/dev/null)
    if printf '%s\n' "$MODELS" | grep -E -q '\[1m\]|-1m([^a-z0-9]|$)|_1m([^a-z0-9]|$)'; then MODEL_1M=1; fi
    if printf '%s\n' "$MODELS" | grep -q '200k'; then MODEL_200K=1; fi

    # Char fallback only if no usage found
    if [ "${LATEST_EFFECTIVE:-0}" -eq 0 ]; then
        TOTAL_CHARS=$(jq -rc '
            (.message.content // .content // "") as $c
            | if ($c | type) == "string" then ($c | length)
              elif ($c | type) == "array" then ($c | map((.text // "") | tostring | length) | add // 0)
              else 0 end
        ' "$TRANSCRIPT" 2>/dev/null | awk 'BEGIN{s=0} {s+=$1+0} END{print s+0}')
    fi
else
    # No jq: grep usage numbers per line.
    while IFS= read -r line; do
        INP=$(printf '%s' "$line" | grep -o '"input_tokens"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | grep -o '[0-9]*$')
        CC=$(printf '%s' "$line" | grep -o '"cache_creation_input_tokens"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | grep -o '[0-9]*$')
        CR=$(printf '%s' "$line" | grep -o '"cache_read_input_tokens"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | grep -o '[0-9]*$')
        [ -z "$INP" ] && INP=0
        [ -z "$CC" ] && CC=0
        [ -z "$CR" ] && CR=0
        if printf '%s' "$line" | grep -q '"input_tokens"'; then
            EFF=$((INP + CC + CR))
            if [ "$EFF" -gt 0 ]; then
                LATEST_EFFECTIVE=$EFF
                [ "$EFF" -gt "$PEAK_EFFECTIVE" ] && PEAK_EFFECTIVE=$EFF
                [ "$EFF" -gt 200000 ] && USAGE_EXCEEDS_200K=1
            fi
        fi
        TOTAL_CHARS=$((TOTAL_CHARS + ${#line}))
        if printf '%s' "$line" | grep -E -iq '"model"[^,}]*\[1m\]|"model"[^,}]*-1m|"model"[^,}]*_1m'; then MODEL_1M=1; fi
        if printf '%s' "$line" | grep -E -iq '"model"[^,}]*200k'; then MODEL_200K=1; fi
    done < "$TRANSCRIPT"
fi

# Default any unset numerics to 0 (jq path may leave them blank)
: "${LATEST_EFFECTIVE:=0}"
: "${PEAK_EFFECTIVE:=0}"
: "${USAGE_EXCEEDS_200K:=0}"

EFFECTIVE=$LATEST_EFFECTIVE
if [ "$EFFECTIVE" -eq 0 ]; then
    if [ "$TOTAL_CHARS" -gt 0 ]; then
        EFFECTIVE=$((TOTAL_CHARS * 10 / 35))  # /3.5
    else
        exit 0
    fi
fi

# Apply model hints if user did not override via env. Evidence (any usage > 200K)
# is the strongest 1M signal because today's JSONL model field is bare for both.
if [ "$ENV_OVERRIDE" = "0" ]; then
    if [ "$USAGE_EXCEEDS_200K" = "1" ] || [ "$MODEL_1M" = "1" ]; then
        MAX_CONTEXT=1000000
    elif [ "$MODEL_200K" = "1" ]; then
        MAX_CONTEXT=200000
    fi
fi

[ "$MAX_CONTEXT" -le 0 ] && exit 0

PCT=$(( (EFFECTIVE * 100) / MAX_CONTEXT ))

if [ "$PCT" -lt "$WARN_PCT" ]; then
    exit 0
fi

if [ "$PCT" -lt "$STOP_PCT" ]; then
    echo "[context-watch] Session context at ${PCT}% of ${MAX_CONTEXT} tokens (~${EFFECTIVE} current). Peak this session: ~${PEAK_EFFECTIVE}. Hard stop fires at ${STOP_PCT}% and will force a handoff write. Consider wrapping the current sub-task at a natural break and writing a handoff now."
    exit 0
fi

VAULT_ROOT=$(resolve_vault_root)
TIMESTAMP=$(date +"%Y-%m-%d-%H%M")
HANDOFF_REL="agents/chief-of-staff/memory/session_handoffs/${TIMESTAMP}-watchgate.md"
if [ -n "$VAULT_ROOT" ]; then
    mkdir -p "$VAULT_ROOT/agents/chief-of-staff/memory/session_handoffs" 2>/dev/null || true
fi

cat <<EOF
===== CONTEXT WATCH -- HARD STOP =====

Session context is at ${PCT}% of the ${MAX_CONTEXT}-token window
(~${EFFECTIVE} tokens resident; peak this session ~${PEAK_EFFECTIVE}).
The harness PreCompact event fires near 100% -- too late to safely write
a handoff. This gate fires at ${STOP_PCT}% so the operator does not lose work.

MANDATORY (before responding to the user's prompt above): write a
structured session handoff to:

    $HANDOFF_REL

Use this shape (compounding-append friendly):

\`\`\`
---
date: $TIMESTAMP
type: handoff
trigger: context-watch-gate
context_pct: $PCT
---

## Goals locked this session
[1-3 bullets -- what was the mission]

## Decisions made
[Each decision with the why, not just the what]

## Files modified
[Path + one-line change description per file]

## Current state
[Where things stand right now -- what's done, what's in flight]

## Next steps
[Top 3 actions for the next session to pick up cold]

## Open contradictions / things to surface
[Anything the librarian should flag next sweep, OR nothing.]
\`\`\`

After writing the handoff, answer the user's prompt as normal. The handoff
is the safety net -- the librarian sweep will index it, and the next
session's session-prelude will surface it as recent activity.

To silence this gate (not recommended) set ROOK_CONTEXT_WATCH_DISABLED=1.
To adjust thresholds: ROOK_CONTEXT_WARN_PCT / ROOK_CONTEXT_HARDSTOP_PCT.

===== END CONTEXT WATCH =====
EOF

exit 0
