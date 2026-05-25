#!/usr/bin/env bash
# master-skill-builder-trigger.sh
# Events: Stop | PreCompact | SessionEnd
# ---------------------------------------------------------------------------
# POSIX companion to master-skill-builder-trigger.ps1.
# Decides whether to fire the master-skill-builder distillation pipeline
# based on the trigger event + a fast heuristic check. Hook is cheap (<2s);
# actual distillation runs as part of the next Claude turn via a system
# reminder. Hook does NOT block.
# ---------------------------------------------------------------------------

set -u

# ---- Resolve vault root ---------------------------------------------------
resolve_vault_root() {
    local cwd="${1:-}"
    if [[ -n "${ROOK_VAULT_ROOT:-}" && -d "${ROOK_VAULT_ROOT}" ]]; then
        echo "${ROOK_VAULT_ROOT}"
        return 0
    fi
    local script_dir
    script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    if [[ -d "$script_dir/.." ]]; then
        local parent
        parent="$( cd "$script_dir/.." && pwd )"
        if [[ -d "$parent/agents" && -d "$parent/hooks" ]]; then
            echo "$parent"
            return 0
        fi
    fi
    if [[ -n "$cwd" && -d "$cwd" ]]; then
        local cur="$cwd"
        for _ in 1 2 3 4 5 6; do
            if [[ -d "$cur/agents" && -d "$cur/hooks" ]]; then
                echo "$cur"
                return 0
            fi
            cur="$(dirname "$cur")"
            [[ "$cur" == "/" || -z "$cur" ]] && break
        done
    fi
    return 1
}

append_log() {
    local vault="$1" trigger="$2" session="$3" action="$4" reason="$5"
    local log_path="$vault/.claude/skills/_invocation.log"
    mkdir -p "$(dirname "$log_path")"
    local iso
    iso="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    printf '%s | %s | %s | %s | %s\n' "$iso" "$trigger" "$session" "$action" "$reason" >> "$log_path"
}

# ---- Read stdin (Claude Code passes event JSON) ---------------------------
raw=""
if [[ ! -t 0 ]]; then
    raw="$(cat)"
fi

# Extract fields with jq if available, else fall back to env vars
trigger="${ROOK_SKB_TRIGGER:-unknown}"
cwd=""
session_id="unknown"
tool_calls=0
file_edits=0
session_tokens=0

if command -v jq >/dev/null 2>&1 && [[ -n "$raw" ]]; then
    cwd="$(echo "$raw" | jq -r '.cwd // ""' 2>/dev/null || echo "")"
    sid="$(echo "$raw" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")"
    [[ -n "$sid" && "$sid" != "null" ]] && session_id="$sid"
    tc="$(echo "$raw" | jq -r '.tool_calls_count // 0' 2>/dev/null || echo 0)"
    [[ "$tc" =~ ^[0-9]+$ ]] && tool_calls="$tc"
    fe="$(echo "$raw" | jq -r '.file_edits_count // 0' 2>/dev/null || echo 0)"
    [[ "$fe" =~ ^[0-9]+$ ]] && file_edits="$fe"
    st="$(echo "$raw" | jq -r '.session_tokens // 0' 2>/dev/null || echo 0)"
    [[ "$st" =~ ^[0-9]+$ ]] && session_tokens="$st"
    if [[ "$trigger" == "unknown" ]]; then
        evt="$(echo "$raw" | jq -r '.event // ""' 2>/dev/null || echo "")"
        [[ -n "$evt" ]] && trigger="$evt"
    fi
fi

vault_root="$(resolve_vault_root "$cwd")" || exit 0

# ---- Upstream skip gate ---------------------------------------------------
if [[ "$trigger" == "Stop" ]]; then
    if [[ "$tool_calls" -lt 5 || "$file_edits" -lt 3 ]]; then
        append_log "$vault_root" "Stop" "$session_id" "no-op" "upstream-gate: tool_calls=$tool_calls file_edits=$file_edits"
        exit 0
    fi
fi

if [[ "$trigger" == "SessionEnd" ]]; then
    if [[ "$session_tokens" -lt 100000 ]]; then
        append_log "$vault_root" "SessionEnd" "$session_id" "no-op" "upstream-gate: session_tokens=$session_tokens lt 100K"
        exit 0
    fi
    # Check if a skill was already staged this session
    staging_dir="$vault_root/.claude/skills/_staging"
    if [[ -d "$staging_dir" ]]; then
        if grep -rls "source_session_id: $session_id\|source_session: $session_id" "$staging_dir" 2>/dev/null | grep -q .; then
            append_log "$vault_root" "SessionEnd" "$session_id" "no-op" "upstream-gate: skill already staged this session"
            exit 0
        fi
    fi
fi

# ---- Mode hint -----------------------------------------------------------
case "$trigger" in
    Stop)        mode="auto-stop" ;;
    PreCompact)  mode="auto-precompact" ;;
    SessionEnd)  mode="auto-sessionend" ;;
    *)           mode="manual" ;;
esac

# ---- Emit system reminder -------------------------------------------------
cat <<EOF
===== MASTER SKILL BUILDER — $trigger HOOK FIRED =====

Lifecycle event: $trigger
Session: $session_id
Mode hint: $mode

Invoke the \`master-skill-builder\` skill against the current session.
Path: .claude/skills/registry/master-skill-builder/SKILL.md

Apply the full pipeline:
  1. Skip-gate check (Step 1 of the skill) — most events should no-op here
  2. If passing, distill via auto-skill-builder + route via rook-skill-creator
  3. Stage to .claude/skills/_staging/<YYYY-MM-DD>-<slug>/SKILL.md (NOT live registry)
  4. Append to .claude/skills/_staging/_pending_promotion.md
  5. Log to .claude/skills/_invocation.log

DO NOT skip the skip gate. DO NOT write to live registry. Pollution > missed capture is the design.

If the skill no-ops, write one log line and return silently. Do not narrate the no-op to the operator.

If the skill stages successfully, return one line to the operator:
  "Skill staged: <slug> — librarian will surface Monday."

===== END MASTER SKILL BUILDER HOOK =====
EOF

append_log "$vault_root" "$trigger" "$session_id" "hook-fired" "system-reminder injected, mode=$mode"
exit 0
