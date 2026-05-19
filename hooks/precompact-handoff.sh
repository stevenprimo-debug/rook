#!/usr/bin/env bash
# precompact-handoff.sh -- bash port of precompact-handoff.ps1
# Event: PreCompact. Injects a "write the handoff before context drops" reminder.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RAW=$(cat 2>/dev/null || true)

if command -v jq >/dev/null 2>&1; then
    CWD=$(echo "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
else
    CWD=$(echo "$RAW" | grep -o '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"cwd"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
fi

resolve_vault_root() {
    if [ -n "${PRIMOLABS_VAULT_ROOT:-}" ] && [ -d "$PRIMOLABS_VAULT_ROOT" ]; then
        echo "$PRIMOLABS_VAULT_ROOT"; return
    fi
    local parent="$(dirname "$SCRIPT_DIR")"
    if [ -d "$parent" ]; then echo "$parent"; return; fi
    local cur="$CWD"
    for _ in 1 2 3 4 5 6; do
        if [ -d "$cur/agents" ] && [ -d "$cur/hooks" ]; then echo "$cur"; return; fi
        cur="$(dirname "$cur")"
        [ "$cur" = "/" ] && break
    done
    echo ""
}
VAULT_ROOT=$(resolve_vault_root)
[ -z "$VAULT_ROOT" ] && exit 0

TIMESTAMP=$(date +"%Y-%m-%d-%H%M")
HANDOFF_DIR="$VAULT_ROOT/agents/chief-of-staff/memory/session_handoffs"
mkdir -p "$HANDOFF_DIR"
HANDOFF_REL="agents/chief-of-staff/memory/session_handoffs/${TIMESTAMP}-precompact.md"

cat <<EOF
===== PRECOMPACT HOOK -- WRITE HANDOFF BEFORE CONTEXT DROPS =====

Claude Code is about to compact the context window. Anything not written
to a file is going to be lost or summarized away.

MANDATORY (before responding to anything else): write a structured session
handoff to:

    $HANDOFF_REL

Use this shape (compounding-append friendly):

\`\`\`
---
date: $TIMESTAMP
type: handoff
trigger: precompact
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

After writing, continue with whatever the operator asked. The handoff is
the safety net.

===== END PRECOMPACT HOOK =====
EOF

exit 0
