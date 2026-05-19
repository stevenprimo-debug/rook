#!/usr/bin/env bash
# test/run-all.sh — Dry-run each hook with a realistic payload.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOOKS_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
VAULT_ROOT="$( cd "$HOOKS_DIR/.." && pwd )"

export PRIMOLABS_VAULT_ROOT="$VAULT_ROOT"
export PRIMOLABS_HOOKS_DIR="$HOOKS_DIR"

FAILURES=()

run_hook() {
    local name="$1" script="$2" payload="$3"
    printf "  [test] %s" "$name"
    if [[ ! -f "$HOOKS_DIR/$script" ]]; then
        printf " SKIP (missing)\n"
        return
    fi

    # 10s timeout
    if command -v timeout >/dev/null 2>&1; then
        OUT=$(echo "$payload" | timeout 10s bash "$HOOKS_DIR/$script" 2>&1)
        RC=$?
    else
        OUT=$(echo "$payload" | bash "$HOOKS_DIR/$script" 2>&1)
        RC=$?
    fi

    if [[ "$RC" -ne 0 ]]; then
        printf " FAIL (exit %d)\n" "$RC"
        echo "    $OUT" | head -5
        FAILURES+=("$name")
        return
    fi

    if echo "$OUT" | grep -qiE "syntax error|command not found|unbound variable"; then
        printf " FAIL (error in stdout)\n"
        echo "    $OUT" | head -5
        FAILURES+=("$name")
        return
    fi

    printf " OK\n"
}

echo "Running hook dry-run tests..."
echo ""

# 1. routing-enforcer
run_hook "routing-enforcer.sh" "routing-enforcer.sh" \
    "{\"prompt\":\"what's the SOXL trade setup looking like for tomorrow\",\"cwd\":\"$VAULT_ROOT\"}"

# 2. session-prelude
run_hook "session-prelude.sh" "session-prelude.sh" \
    "{\"cwd\":\"$VAULT_ROOT/agents/trading-analyst\",\"hook_event_name\":\"SessionStart\"}"

# 3. superpowers-init
run_hook "superpowers-init.sh" "superpowers-init.sh" \
    "{\"cwd\":\"$VAULT_ROOT\"}"

# 4. posture-staleness-gate
run_hook "posture-staleness-gate.sh" "posture-staleness-gate.sh" \
    "{\"cwd\":\"$VAULT_ROOT/agents/trading-analyst\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"memory/trade_plan.md\",\"content\":\"long this setup at 21.50 stop 20.80 target 24\"}}"

# 5. librarian-digest
run_hook "librarian-digest.sh" "librarian-digest.sh" "{}"

# 6. preference-detector
run_hook "preference-detector.sh" "preference-detector.sh" \
    "{\"prompt\":\"from now on always check the time before responding\"}"

echo ""
if [[ ${#FAILURES[@]} -eq 0 ]]; then
    echo "ALL HOOKS PASSED"
    exit 0
else
    echo "FAILED: ${FAILURES[*]}"
    exit 1
fi
