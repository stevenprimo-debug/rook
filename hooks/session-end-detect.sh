#!/usr/bin/env bash
# session-end-detect.sh -- bash port of session-end-detect.ps1
# Event: UserPromptSubmit. Detects natural-language session-end signals.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Read stdin JSON
RAW=$(cat 2>/dev/null || true)
[ -z "$RAW" ] && exit 0

if command -v jq >/dev/null 2>&1; then
    PROMPT=$(echo "$RAW" | jq -r '.prompt // empty' 2>/dev/null)
    CWD=$(echo "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
else
    PROMPT=$(echo "$RAW" | grep -o '"prompt"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"prompt"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
    CWD=$(echo "$RAW" | grep -o '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"cwd"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
fi
[ -z "$PROMPT" ] && exit 0

PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

SIGNALS=(
    "signing off"
    "sign off"
    "wrap up"
    "wrapping up"
    "let's wrap"
    "wrap it up"
    "calling it"
    "i'm done"
    "done for now"
    "done for the day"
    "done for tonight"
    "going to bed"
    "heading out"
    "heading home"
    "shutting down"
    "end of session"
    "end the session"
    "session end"
    "closing out"
    "closing this out"
    "time to stop"
    "that's it for today"
    "that's it for tonight"
    "see you tomorrow"
    "catch you tomorrow"
    "catch you next time"
)

MATCHED=""
for sig in "${SIGNALS[@]}"; do
    case "$PROMPT_LOWER" in *"$sig"*) MATCHED="$sig"; break ;; esac
done
[ -z "$MATCHED" ] && exit 0

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
HANDOFF_REL="agents/chief-of-staff/memory/session_handoffs/${TIMESTAMP}-sessionend.md"

cat <<EOF
===== SESSION-END SIGNAL DETECTED =====

The operator's prompt contains a session-end signal: "$MATCHED"

MANDATORY (before saying goodbye): write a final session handoff to:

    $HANDOFF_REL

Use this shape:

\`\`\`
---
date: $TIMESTAMP
type: handoff
trigger: session-end
signal_phrase: "$MATCHED"
---

## What we shipped this session
[Bullet list of completed work]

## What's parked / still open
[Anything intentionally not finished -- with the reason and the trigger to pick it back up]

## Locked decisions worth remembering
[Decisions that should survive into future sessions -- with the *why*]

## Next session pickup
[The first 3 things the next session should do, cold-start]

## Anything to flag for the librarian
[Contradictions, drift candidates -- OR nothing.]
\`\`\`

THEN respond to the operator's actual sign-off. End with one-line confirmation:
"Handoff written: <relative path>. Catch you next time."

===== END SESSION-END SIGNAL =====
EOF

exit 0
