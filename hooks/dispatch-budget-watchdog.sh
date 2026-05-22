#!/usr/bin/env bash
# dispatch-budget-watchdog.sh
# Event: PreToolUse (matcher: Task|Agent)
# Enforces per-agent dispatch budgets: max recursion depth, token ceiling,
# wall-clock cap. Reads target agent's SKILL.md frontmatter `budget:` block.
# Lineage state at $HOME/.claude/.rook-dispatch-lineage (JSON).
#
# Blocks on depth+1>max_dispatch_depth, tokens>token_budget, wall>time_budget_minutes.
# Warns advisory at 0.8 * token_budget.
# Fail-open on any internal error.

set -u

# Fail-open helper
fail_open() { exit 0; }

RAW=$(cat 2>/dev/null || true)
[[ -z "$RAW" ]] && fail_open

command -v jq >/dev/null 2>&1 || fail_open

# SessionStart path: clear lineage state and exit
HOOK_EVT=$(echo "$RAW" | jq -r '.hook_event_name // empty' 2>/dev/null)
if [[ "$HOOK_EVT" == "SessionStart" ]]; then
    STATE_PATH_CLEAR="${HOME:-$USERPROFILE}/.claude/.rook-dispatch-lineage"
    rm -f "$STATE_PATH_CLEAR" 2>/dev/null || true
    exit 0
fi

TOOL_NAME=$(echo "$RAW" | jq -r '.tool_name // empty' 2>/dev/null)
[[ -z "$TOOL_NAME" ]] && fail_open
case "$TOOL_NAME" in
    Task|Agent) ;;
    *) fail_open ;;
esac

# Target agent slug
TARGET=$(echo "$RAW" | jq -r '.tool_input.subagent_type // .tool_input.agent // .tool_input.name // empty' 2>/dev/null)
[[ -z "$TARGET" ]] && fail_open

# Vault root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_ROOT=""
if [[ -n "${PRIMOLABS_VAULT_ROOT:-}" && -d "$PRIMOLABS_VAULT_ROOT" ]]; then
    VAULT_ROOT="$PRIMOLABS_VAULT_ROOT"
elif [[ -d "$SCRIPT_DIR/.." ]]; then
    VAULT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
fi
[[ -z "$VAULT_ROOT" ]] && fail_open

SKILL_PATH="$VAULT_ROOT/agents/$TARGET/SKILL.md"
[[ ! -f "$SKILL_PATH" ]] && fail_open

# Extract budget block from frontmatter.
# Strategy: strip BOM, read up to first closing '---' after start, grep for keys.
# We strip the BOM (U+FEFF / EF BB BF) before awk so the first '---' line matches.
FM=$(sed '1s/^\xEF\xBB\xBF//' "$SKILL_PATH" 2>/dev/null | awk '
    BEGIN { count=0 }
    /^---[[:space:]]*$/ { count++; if (count==2) exit; if (count==1) next }
    count==1 { print }
' 2>/dev/null)

[[ -z "$FM" ]] && fail_open

TIME_BUDGET=$(echo "$FM" | awk '
    /^budget:[[:space:]]*$/ { inb=1; next }
    inb==1 && /^[[:space:]]{2,}time_budget_minutes:/ { sub(/^[^:]*:[[:space:]]*/, ""); print; exit }
    inb==1 && /^[^[:space:]]/ { inb=0 }
' | tr -d ' ')
TOKEN_BUDGET=$(echo "$FM" | awk '
    /^budget:[[:space:]]*$/ { inb=1; next }
    inb==1 && /^[[:space:]]{2,}token_budget:/ { sub(/^[^:]*:[[:space:]]*/, ""); print; exit }
    inb==1 && /^[^[:space:]]/ { inb=0 }
' | tr -d ' ')
DEPTH_BUDGET=$(echo "$FM" | awk '
    /^budget:[[:space:]]*$/ { inb=1; next }
    inb==1 && /^[[:space:]]{2,}max_dispatch_depth:/ { sub(/^[^:]*:[[:space:]]*/, ""); print; exit }
    inb==1 && /^[^[:space:]]/ { inb=0 }
' | tr -d ' ')

# If none parsed, fail-open
if [[ -z "$TIME_BUDGET" && -z "$TOKEN_BUDGET" && -z "$DEPTH_BUDGET" ]]; then
    fail_open
fi

# Lineage state
STATE_DIR="${HOME:-$USERPROFILE}/.claude"
mkdir -p "$STATE_DIR" 2>/dev/null || true
STATE_PATH="$STATE_DIR/.rook-dispatch-lineage"

CURRENT_DEPTH=0
TOKENS_USED=0
STARTED_AT=""
if [[ -f "$STATE_PATH" ]]; then
    CURRENT_DEPTH=$(jq -r '.depth // 0' "$STATE_PATH" 2>/dev/null || echo 0)
    TOKENS_USED=$(jq -r '.tokens_used // 0' "$STATE_PATH" 2>/dev/null || echo 0)
    STARTED_AT=$(jq -r '.started_at // empty' "$STATE_PATH" 2>/dev/null)
fi
[[ -z "$STARTED_AT" ]] && STARTED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Pull tokens from event if present
EVT_TOKENS=$(echo "$RAW" | jq -r '.usage.total_tokens // empty' 2>/dev/null)
if [[ -n "$EVT_TOKENS" && "$EVT_TOKENS" =~ ^[0-9]+$ ]]; then
    TOKENS_USED="$EVT_TOKENS"
fi

# Wall-clock minutes since lineage start
NOW_EPOCH=$(date -u +%s)
START_EPOCH=""
if date -u -d "$STARTED_AT" +%s >/dev/null 2>&1; then
    START_EPOCH=$(date -u -d "$STARTED_AT" +%s)
elif date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$STARTED_AT" +%s >/dev/null 2>&1; then
    START_EPOCH=$(date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$STARTED_AT" +%s)
fi
WALL_MIN=0
if [[ -n "$START_EPOCH" ]]; then
    WALL_MIN=$(( (NOW_EPOCH - START_EPOCH) / 60 ))
fi

emit_block() {
    local msg="$1"
    jq -n --arg m "$msg" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$m}}'
    exit 0
}

# ---- DEPTH GATE ----
if [[ -n "$DEPTH_BUDGET" ]]; then
    NEXT_DEPTH=$((CURRENT_DEPTH + 1))
    if [[ "$NEXT_DEPTH" -gt "$DEPTH_BUDGET" ]]; then
        MSG="===== DISPATCH-BUDGET-WATCHDOG: DEPTH LIMIT =====
dispatch depth limit reached for $TARGET
current_depth=$CURRENT_DEPTH, would_become=$NEXT_DEPTH, max_dispatch_depth=$DEPTH_BUDGET

Per the target agent's SKILL.md budget block, this dispatch would exceed the
recursion ceiling. Block in place -- synthesize from already-collected returns
or return to the operator. Do NOT spawn another sub-agent.

Lineage state: $STATE_PATH
===== END WATCHDOG ====="
        emit_block "$MSG"
    fi
fi

# ---- TOKEN GATE ----
if [[ -n "$TOKEN_BUDGET" && "$TOKENS_USED" -gt "$TOKEN_BUDGET" ]]; then
    MSG="===== DISPATCH-BUDGET-WATCHDOG: TOKEN LIMIT =====
token budget exceeded for $TARGET
tokens_used=$TOKENS_USED, token_budget=$TOKEN_BUDGET

Lineage has burned past its token ceiling. Block in place. Synthesize from
collected returns or escalate to the operator.

Lineage state: $STATE_PATH
===== END WATCHDOG ====="
    emit_block "$MSG"
fi

# ---- TIME GATE ----
if [[ -n "$TIME_BUDGET" && "$WALL_MIN" -gt "$TIME_BUDGET" ]]; then
    MSG="===== DISPATCH-BUDGET-WATCHDOG: TIME LIMIT =====
wall-clock budget exceeded for $TARGET
elapsed_minutes=$WALL_MIN, time_budget_minutes=$TIME_BUDGET

Lineage has run past its time ceiling. Return current state to the operator.

Lineage state: $STATE_PATH
===== END WATCHDOG ====="
    emit_block "$MSG"
fi

# ---- WARNING THRESHOLD ----
if [[ -n "$TOKEN_BUDGET" ]]; then
    THRESH=$(( TOKEN_BUDGET * 8 / 10 ))
    if [[ "$TOKENS_USED" -gt "$THRESH" ]]; then
        PCT=$(( TOKENS_USED * 100 / TOKEN_BUDGET ))
        echo "[dispatch-budget-watchdog] WARN: $TARGET lineage at ${PCT}% of token budget ($TOKENS_USED / $TOKEN_BUDGET). Consider closing out." 1>&2
    fi
fi

# Pass — increment depth and persist
NEW_DEPTH=$((CURRENT_DEPTH + 1))
jq -n \
    --argjson d "$NEW_DEPTH" \
    --argjson t "$TOKENS_USED" \
    --arg s "$STARTED_AT" \
    --arg a "$TARGET" \
    '{depth:$d, tokens_used:$t, started_at:$s, last_agent:$a}' > "$STATE_PATH" 2>/dev/null || true

exit 0
