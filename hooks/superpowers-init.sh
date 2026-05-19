#!/usr/bin/env bash
# superpowers-init.sh
# Event: SessionStart
# Confirms `using-superpowers` skill is invocable. Falls back gracefully if missing.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RAW=$(cat 2>/dev/null || true)

CWD=""
if [[ -n "$RAW" ]] && command -v jq >/dev/null 2>&1; then
    CWD=$(echo "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
fi

VAULT_ROOT=""
if [[ -n "${PRIMOLABS_VAULT_ROOT:-}" && -d "$PRIMOLABS_VAULT_ROOT" ]]; then
    VAULT_ROOT="$PRIMOLABS_VAULT_ROOT"
elif [[ -d "$SCRIPT_DIR/.." ]]; then
    VAULT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
elif [[ -n "$CWD" ]]; then
    cur="$CWD"
    for _ in 1 2 3 4 5 6; do
        if [[ -d "$cur/skills" && -d "$cur/agents" ]]; then
            VAULT_ROOT="$cur"
            break
        fi
        cur="$( dirname "$cur" )"
        [[ "$cur" == "/" ]] && break
    done
fi

SKILL_PATH=""
if [[ -n "$VAULT_ROOT" ]]; then
    for cand in \
        "$VAULT_ROOT/skills/registry/using-superpowers/SKILL.md" \
        "$VAULT_ROOT/skills/using-superpowers/SKILL.md"
    do
        if [[ -f "$cand" ]]; then
            SKILL_PATH="$cand"
            break
        fi
    done
fi

echo ""
echo "===== SUPERPOWERS INIT ====="

if [[ -n "$SKILL_PATH" ]]; then
    REL="${SKILL_PATH#$VAULT_ROOT/}"
    echo "Skill registry detected. The 'using-superpowers' skill is invocable."
    echo "  Location: $REL"
    echo ""
    echo "MANDATORY before ANY response (including clarifying questions):"
    echo "  1. If a skill might apply, INVOKE IT (Skill tool)."
    echo "  2. Never Read SKILL.md files — use the Skill tool."
    echo "  3. Skill bodies load into your context — follow them directly."
else
    echo "Skill registry NOT detected. Falling back to plain assistant mode."
    if [[ -n "$VAULT_ROOT" ]]; then
        echo "Expected: $VAULT_ROOT/skills/registry/using-superpowers/SKILL.md"
    else
        echo "Set PRIMOLABS_VAULT_ROOT env var to enable skill loading."
    fi
fi

echo "===== END SUPERPOWERS INIT ====="
echo ""
exit 0
