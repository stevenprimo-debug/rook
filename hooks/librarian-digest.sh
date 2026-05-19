#!/usr/bin/env bash
# librarian-digest.sh
# Event: PostToolUse — cadence-based
# Increments a counter; on threshold appends a digest stub to
# agents/librarian/memory/librarian_digest.md.

set -u
CADENCE="${PRIMOLABS_LIBRARIAN_CADENCE:-50}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Drain stdin (PostToolUse payload not needed here)
cat >/dev/null 2>&1 || true

VAULT_ROOT=""
if [[ -n "${PRIMOLABS_VAULT_ROOT:-}" && -d "$PRIMOLABS_VAULT_ROOT" ]]; then
    VAULT_ROOT="$PRIMOLABS_VAULT_ROOT"
elif [[ -d "$SCRIPT_DIR/.." ]]; then
    VAULT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
fi
[[ -z "$VAULT_ROOT" ]] && exit 0

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/primolabs"
mkdir -p "$STATE_DIR" 2>/dev/null
COUNTER_FILE="$STATE_DIR/librarian-counter.txt"

COUNT=0
if [[ -f "$COUNTER_FILE" ]]; then
    COUNT=$(cat "$COUNTER_FILE" 2>/dev/null | tr -d ' \n\r' || echo 0)
fi
COUNT=$((COUNT + 1))

if [[ "$COUNT" -lt "$CADENCE" ]]; then
    echo "$COUNT" > "$COUNTER_FILE"
    exit 0
fi

echo "0" > "$COUNTER_FILE"

DIGEST="$VAULT_ROOT/agents/librarian/memory/librarian_digest.md"
mkdir -p "$( dirname "$DIGEST" )" 2>/dev/null

if [[ ! -f "$DIGEST" ]]; then
    cat > "$DIGEST" <<EOF
# Librarian Digest

> ## For future Claude (TL;DR)
> Cadence-driven scan log. The librarian-digest.sh hook appends a new entry
> every $CADENCE tool calls. Each entry is a STUB — the librarian agent
> processes the stub into Findings / Hooks-created / Hooks-proposed when
> next dispatched.

---

EOF
fi

STAMP=$(date "+%Y-%m-%d %H:%M")

# Recent files for scope hint
SCOPE=""
RECENT=$(find "$VAULT_ROOT/agents" "$VAULT_ROOT/departments" "$VAULT_ROOT/skills" \
    -type f \( -name "*.md" -o -name "*.json" -o -name "*.ps1" -o -name "*.sh" \) \
    -mmin -120 2>/dev/null | head -8)
if [[ -n "$RECENT" ]]; then
    while IFS= read -r f; do
        SCOPE="${SCOPE}  - ${f#$VAULT_ROOT/}
"
    done <<< "$RECENT"
else
    SCOPE="  - (no recent file changes detected)
"
fi

cat >> "$DIGEST" <<EOF

## $STAMP — Cadence digest [ ] pending

**Scope hint** (files modified in last 2h):
$SCOPE
**Findings:** (librarian agent to fill on next dispatch)
- [ ] TBD — librarian scans vault state vs Graphify index and notes drift.

**Hooks-created** (passive, auto-live):
- [ ] TBD — non-mutating reminders.

**Hooks-proposed** (mutating/blocking, awaiting user Y/N):
- [ ] TBD — PreToolUse deny gates, PostToolUse mutators.

---
EOF

exit 0
