#!/usr/bin/env bash
# graphify-weekly-rebuild.sh -- weekly graphify rebuild (cron / launchd)
# ---------------------------------------------------------------------------
# POSIX equivalent of graphify-weekly-rebuild.ps1.
# Runs `python -m graphify update <vault-root>` on agents/ and .claude/reference/.
# AST-only re-extraction (no LLM tokens, no API key needed).
# For full semantic re-extract, operator runs `graphify extract` manually.

set -u

resolve_vault_root() {
    if [ -n "${PRIMOLABS_VAULT_ROOT:-}" ] && [ -d "$PRIMOLABS_VAULT_ROOT" ]; then
        echo "$PRIMOLABS_VAULT_ROOT"
        return
    fi
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local parent
    parent="$(dirname "$script_dir")"
    [ -d "$parent" ] && echo "$parent"
}

VAULT_ROOT="$(resolve_vault_root)"
[ -z "$VAULT_ROOT" ] && exit 0

LOG_FILE="$VAULT_ROOT/agents/librarian/memory/graphify-rebuild.log"
mkdir -p "$(dirname "$LOG_FILE")"

NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

HAS_KEY=false
if [ -n "${ANTHROPIC_API_KEY:-}" ] || [ -n "${GEMINI_API_KEY:-}" ] || [ -n "${GOOGLE_API_KEY:-}" ] || [ -n "${OPENAI_API_KEY:-}" ]; then
    HAS_KEY=true
fi

PYTHON=""
command -v python3 >/dev/null 2>&1 && PYTHON=$(command -v python3)
[ -z "$PYTHON" ] && command -v python >/dev/null 2>&1 && PYTHON=$(command -v python)
if [ -z "$PYTHON" ]; then
    echo "$NOW SKIP no_python_on_PATH" >> "$LOG_FILE"
    exit 0
fi

if ! "$PYTHON" -c "import graphify" >/dev/null 2>&1; then
    echo "$NOW SKIP graphify_module_not_installed" >> "$LOG_FILE"
    exit 0
fi

SUCCESS=true
for target in "$VAULT_ROOT/agents" "$VAULT_ROOT/.claude/reference"; do
    [ -d "$target" ] || continue
    if "$PYTHON" -m graphify update "$target" >/dev/null 2>&1; then
        echo "$NOW OK update $target" >> "$LOG_FILE"
    else
        SUCCESS=false
        echo "$NOW FAIL update $target" >> "$LOG_FILE"
    fi
done

echo "$NOW DONE key_present=$HAS_KEY success=$SUCCESS" >> "$LOG_FILE"
exit 0
