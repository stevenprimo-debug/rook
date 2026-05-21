#!/usr/bin/env bash
# context-watch-gate-test.sh -- unit test for context-watch-gate.sh
# Synthesizes JSONL at known token counts, invokes the hook, asserts output.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOOKS_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
VAULT_ROOT="$( cd "$HOOKS_DIR/.." && pwd )"
HOOK="$HOOKS_DIR/context-watch-gate.sh"

if [ ! -f "$HOOK" ]; then
    printf '[FAIL] context-watch-gate.sh not found at %s\n' "$HOOK"
    exit 1
fi

TMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'ctxwatch')

make_transcript() {
    local inp="$1"
    local f="$TMP_DIR/$(date +%s%N 2>/dev/null || date +%s)-$RANDOM.jsonl"
    cat > "$f" <<JSON
{"type":"assistant","message":{"model":"claude-opus-4-7","content":[{"type":"text","text":"synthetic test turn"}],"usage":{"input_tokens":$inp,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":100}}}
JSON
    echo "$f"
}

invoke_hook() {
    local stdin_payload="$1"
    printf '%s' "$stdin_payload" | bash "$HOOK" 2>&1
}

unset ROOK_CONTEXT_WARN_PCT ROOK_CONTEXT_HARDSTOP_PCT ROOK_CONTEXT_WATCH_DISABLED CLAUDE_MAX_CONTEXT_TOKENS

FAILS=0
assert_test() {
    local name="$1" pass="$2" detail="${3:-}"
    if [ "$pass" = "1" ]; then
        printf '  [PASS] %s\n' "$name"
    else
        printf '  [FAIL] %s -- %s\n' "$name" "$detail"
        FAILS=$((FAILS + 1))
    fi
}

# Gate 1: empty stdin
OUT=$(invoke_hook "" || true)
if [ -z "$OUT" ]; then assert_test "empty stdin silent" 1; else assert_test "empty stdin silent" 0 "got: $OUT"; fi

# Gate 2: 50% (100k of 200k)
T50=$(make_transcript 100000)
PAY="{\"cwd\":\"$VAULT_ROOT\",\"transcript_path\":\"$T50\"}"
OUT=$(invoke_hook "$PAY" || true)
if [ -z "$OUT" ]; then assert_test "50% silent" 1; else assert_test "50% silent" 0 "got: $OUT"; fi

# Gate 3: 75%
T75=$(make_transcript 150000)
PAY="{\"cwd\":\"$VAULT_ROOT\",\"transcript_path\":\"$T75\"}"
OUT=$(invoke_hook "$PAY" || true)
if printf '%s' "$OUT" | grep -q '\[context-watch\]' && ! printf '%s' "$OUT" | grep -q 'HARD STOP'; then
    assert_test "75% warning printed" 1
else
    assert_test "75% warning printed" 0 "got: $(printf '%s' "$OUT" | head -c 200)"
fi

# Gate 4: 90%
T90=$(make_transcript 180000)
PAY="{\"cwd\":\"$VAULT_ROOT\",\"transcript_path\":\"$T90\"}"
OUT=$(invoke_hook "$PAY" || true)
if printf '%s' "$OUT" | grep -q 'CONTEXT WATCH -- HARD STOP' \
   && printf '%s' "$OUT" | grep -q 'session_handoffs' \
   && printf '%s' "$OUT" | grep -q 'watchgate.md'; then
    assert_test "90% hard-stop block" 1
else
    assert_test "90% hard-stop block" 0 "got: $(printf '%s' "$OUT" | head -c 300)"
fi

# Gate 5: disabled
export ROOK_CONTEXT_WATCH_DISABLED=1
OUT=$(invoke_hook "$PAY" || true)
if [ -z "$OUT" ]; then assert_test "disabled env silences" 1; else assert_test "disabled env silences" 0 "got: $OUT"; fi
unset ROOK_CONTEXT_WATCH_DISABLED

rm -rf "$TMP_DIR" 2>/dev/null || true

printf '\n'
if [ "$FAILS" -eq 0 ]; then
    printf 'context-watch-gate: ALL TESTS PASSED\n'
    exit 0
else
    printf 'context-watch-gate: %d FAILURE(S)\n' "$FAILS"
    exit 1
fi
