#!/bin/bash
# session-mode-injector.sh
# Fires on SessionStart (POSIX equivalent of session-mode-injector.ps1).
# Surfaces the active ROOK session mode at the top of the session
# so the operator never accidentally writes to shipped paths while in operator-mode.

rook_mode="${ROOK_SESSION_MODE:-}"
if [ -z "$rook_mode" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    context_file="$script_dir/../.claude/.session_context"
    if [ -f "$context_file" ]; then
        rook_mode="$(tr -d '[:space:]' < "$context_file")"
    fi
fi
if [ -z "$rook_mode" ]; then
    rook_mode="customer"
fi

rook_mode="$(echo "$rook_mode" | tr '[:upper:]' '[:lower:]')"
if [ "$rook_mode" != "operator" ] && [ "$rook_mode" != "customer" ]; then
    echo "WARNING: ROOK_SESSION_MODE='$rook_mode' is unrecognized. Defaulting to 'customer'."
    rook_mode="customer"
fi

if [ "$rook_mode" = "operator" ]; then
    echo "===== ROOK SESSION MODE: OPERATOR ====="
    echo "Active mode: OPERATOR (your real-data working vault)"
    echo ""
    echo "Memory writes go to: agents/<agent>/memory/operator/<file>"
    echo "Context writes go to: agents/<agent>/context/operator/<file>"
    echo ""
    echo "These paths are EXCLUDED from package-for-cohort.py."
    echo "Your accumulated personal/client data NEVER ships to customers."
    echo "See .claude/session-modes.md for full convention."
    echo "===== END SESSION MODE BLOCK ====="
else
    echo "===== ROOK SESSION MODE: CUSTOMER ====="
    echo "Active mode: CUSTOMER (default — operator did not set ROOK_SESSION_MODE)"
    echo ""
    echo "Memory writes go to: agents/<agent>/memory/<file> (shipped paths)"
    echo ""
    echo "If you ARE the operator (this is your build vault, not a customer install),"
    echo "set in your shell rc: export ROOK_SESSION_MODE=operator"
    echo "===== END SESSION MODE BLOCK ====="
fi

exit 0
