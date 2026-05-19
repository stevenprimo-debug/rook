#!/usr/bin/env bash
# posture-staleness-gate.sh
# Event: PreToolUse
# Blocks tool calls when the latest agents/trading-analyst/memory/posture*.md
# HEAD-block `last_verified` is older than N days. No-op outside trading work.

set -u
STALE_DAYS="${PRIMOLABS_POSTURE_STALE_DAYS:-7}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RAW=$(cat 2>/dev/null || true)
[[ -z "$RAW" ]] && exit 0

if ! command -v jq >/dev/null 2>&1; then exit 0; fi

CWD=$(echo "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
TOOL_INPUT=$(echo "$RAW" | jq -c '.tool_input // {}' 2>/dev/null)

IN_TRADING=0
[[ "$CWD" == *"agents/trading-analyst"* ]] && IN_TRADING=1

if [[ "$IN_TRADING" -eq 0 ]]; then
    if ! echo "$TOOL_INPUT" | grep -qiE '\b(entry|stop loss|target price|take profit|trade plan|trade setup|risk-sized|long this|short this|buy this|sell this|position size)\b'; then
        exit 0
    fi
fi

VAULT_ROOT=""
if [[ -n "${PRIMOLABS_VAULT_ROOT:-}" && -d "$PRIMOLABS_VAULT_ROOT" ]]; then
    VAULT_ROOT="$PRIMOLABS_VAULT_ROOT"
elif [[ -d "$SCRIPT_DIR/.." ]]; then
    VAULT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
fi
[[ -z "$VAULT_ROOT" ]] && exit 0

MEM_DIR="$VAULT_ROOT/agents/trading-analyst/memory"
[[ ! -d "$MEM_DIR" ]] && exit 0

LATEST=$(ls -1t "$MEM_DIR"/posture*.md 2>/dev/null | head -1)
if [[ -z "$LATEST" ]]; then
    MSG="===== POSTURE GATE: MISSING =====

No posture file at $MEM_DIR/posture*.md

Per Posture-Current-Pole, every trade verdict requires a posture read.
Run mode=posture_read FIRST, then re-issue the verdict.
===== END POSTURE GATE ====="
    jq -n --arg m "$MSG" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$m}}'
    exit 0
fi

# Parse last_verified from HEAD
LAST_VERIFIED=$(head -n 30 "$LATEST" | grep -iE 'last[_-]verified\s*[:=]\s*[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)

if [[ -z "$LAST_VERIFIED" ]]; then
    # Fall back to mtime (BSD/GNU date compatible)
    if date -r "$LATEST" "+%Y-%m-%d" >/dev/null 2>&1; then
        LAST_VERIFIED=$(date -r "$LATEST" "+%Y-%m-%d")
    else
        LAST_VERIFIED=$(stat -c "%y" "$LATEST" 2>/dev/null | cut -d' ' -f1)
    fi
fi
[[ -z "$LAST_VERIFIED" ]] && exit 0

# Compute age
NOW_EPOCH=$(date +%s)
if date -j -f "%Y-%m-%d" "$LAST_VERIFIED" "+%s" >/dev/null 2>&1; then
    VERIFIED_EPOCH=$(date -j -f "%Y-%m-%d" "$LAST_VERIFIED" "+%s")
else
    VERIFIED_EPOCH=$(date -d "$LAST_VERIFIED" "+%s" 2>/dev/null)
fi
[[ -z "$VERIFIED_EPOCH" ]] && exit 0

AGE_DAYS=$(( (NOW_EPOCH - VERIFIED_EPOCH) / 86400 ))

if [[ "$AGE_DAYS" -gt "$STALE_DAYS" ]]; then
    REL="${LATEST#$VAULT_ROOT/}"
    MSG="===== POSTURE GATE: STALE-REFUSE =====

Posture file: $REL
Last verified: $LAST_VERIFIED ($AGE_DAYS days ago)
Threshold: $STALE_DAYS days

No trade verdict ships against a stale posture. Run mode=posture_read
FIRST, update last_verified, then re-issue.
===== END POSTURE GATE ====="
    jq -n --arg m "$MSG" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$m}}'
    exit 0
fi

exit 0
