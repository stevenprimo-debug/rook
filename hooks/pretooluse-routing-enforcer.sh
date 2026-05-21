#!/usr/bin/env bash
# pretooluse-routing-enforcer.sh
# Event: PreToolUse
# Blocks main-thread Edit/Write calls targeting agents/<slug>/** paths.
# Subagent sessions (detected via parent_session_id or ROOK_SUBAGENT=1) are ALLOWED.
#
# Requires: jq
# Falls back to silent-pass if jq is missing — never blocks a prompt.
#
# Override: set ROOK_SUBAGENT=1 in the env to pass unconditionally (subagent signal).

set -u

fail_silent() { exit 0; }
trap fail_silent ERR

# jq required
if ! command -v jq >/dev/null 2>&1; then
    exit 0
fi

RAW=$(cat)
[[ -z "$RAW" ]] && exit 0

# Only intercept Edit and Write tools
TOOL_NAME=$(echo "$RAW" | jq -r '.tool_name // empty' 2>/dev/null)
[[ -z "$TOOL_NAME" ]] && exit 0
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

# Extract target file path from tool_input
TARGET_PATH=$(echo "$RAW" | jq -r '(.tool_input.file_path // .tool_input.path) // empty' 2>/dev/null)
[[ -z "$TARGET_PATH" ]] && exit 0

# Normalize path separators
NORMALIZED=$(echo "$TARGET_PATH" | tr '\\' '/')

# Check if path matches agents/<slug>/** pattern
if ! echo "$NORMALIZED" | grep -qE 'agents/[^/]+/'; then
    exit 0
fi

# WHITELIST: session_handoffs/ is a system-managed handoff sink
# (context-watch-gate writes here). Allowed even from main thread.
if echo "$NORMALIZED" | grep -qE 'agents/[^/]+/memory/session_handoffs/'; then
    exit 0
fi

# Extract agent slug
AGENT_SLUG=$(echo "$NORMALIZED" | grep -oE 'agents/([^/]+)/' | head -1 | sed 's|agents/||;s|/||')
[[ -z "$AGENT_SLUG" ]] && AGENT_SLUG="<agent>"

# Detect subagent origin
IS_SUBAGENT=0

# Check env var override
if [[ "${ROOK_SUBAGENT:-}" == "1" ]]; then
    IS_SUBAGENT=1
fi

# Check parent_session_id in hook context
if [[ "$IS_SUBAGENT" -eq 0 ]]; then
    PARENT_SESSION=$(echo "$RAW" | jq -r '(.parent_session_id // .session_context.parent_session_id) // empty' 2>/dev/null)
    if [[ -n "$PARENT_SESSION" ]]; then
        IS_SUBAGENT=1
    fi
fi

if [[ "$IS_SUBAGENT" -eq 1 ]]; then
    exit 0
fi

# BLOCK: main-thread write to agent path
BLOCK_MSG="[PRETOOLUSE BLOCK] This file is owned by \`$AGENT_SLUG\`. Main thread cannot Edit/Write it directly.

Dispatch via the Agent tool: spawn a general-purpose subagent with the prompt
\"you are $AGENT_SLUG, do <task>\". The subagent inherits write access to its own files.

To override (legitimate main-thread infra write only):
  Set environment variable ROOK_SUBAGENT=1, or confirm parent_session_id is
  present in the hook context.

Blocked path: $TARGET_PATH"

jq -n --arg reason "$BLOCK_MSG" '{
    hookSpecificOutput: {
        hookEventName: "PreToolUse",
        decision: "block",
        reason: $reason
    }
}'

exit 2  # exit 2 = block in Claude Code PreToolUse hooks
