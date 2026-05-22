#!/usr/bin/env bash
# preamble-resolver.sh -- ROOK Tiered Preamble Resolver (macOS / Linux)
# ---------------------------------------------------------------------------
# Fires on SessionStart (after session-prelude.sh).
# Loads tiered preamble content from .claude/preamble/T1.md through T4.md
# and injects into the session system-reminder.
#
# Tier selection: reads $ROOK_PREAMBLE_TIER (default 2 if unset).
# Output: writes preamble block to stdout for Claude Code system-reminder pickup.

set -u

VAULT_ROOT="${PRIMOLABS_VAULT_ROOT:-}"
if [ -z "$VAULT_ROOT" ]; then
    # Fallback: two levels up from this script
    VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

PREAMBLE_DIR="$VAULT_ROOT/.claude/preamble"

TIER="${ROOK_PREAMBLE_TIER:-2}"
# Clamp to 1-4
if [ "$TIER" -lt 1 ] 2>/dev/null || [ "$TIER" -gt 4 ] 2>/dev/null; then
    TIER=2
fi

BLOCKS=()
for t in $(seq 1 "$TIER"); do
    p="$PREAMBLE_DIR/T${t}.md"
    if [ -f "$p" ]; then
        BLOCKS+=("$(cat "$p")")
    fi
done

if [ "${#BLOCKS[@]}" -eq 0 ]; then
    exit 0
fi

echo "===== ROOK PREAMBLE (Tier $TIER) ====="
echo ""
FIRST=1
for block in "${BLOCKS[@]}"; do
    if [ "$FIRST" -eq 0 ]; then
        echo ""
        echo "---"
        echo ""
    fi
    echo "$block"
    FIRST=0
done
echo ""
echo "===== END ROOK PREAMBLE ====="

exit 0
