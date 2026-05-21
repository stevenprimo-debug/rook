#!/usr/bin/env bash
# session-prelude.sh
# Event: SessionStart (and optionally UserPromptSubmit)
# Surfaces: dept/agent context, hard-stop time check, recent files, protocol checks.
#
# Vault root resolution: $PRIMOLABS_VAULT_ROOT -> <script dir>/.. -> data.cwd

set -u

# HARDSTOP env vars removed from ship vault (was operator-personal default).
# May return as opt-in cohort feature configured during onboarding.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Read stdin (may be empty for SessionStart)
RAW=$(cat 2>/dev/null || true)

# Resolve cwd from input (jq optional)
CWD=""
EVENT="SessionStart"
if [[ -n "$RAW" ]] && command -v jq >/dev/null 2>&1; then
    CWD=$(echo "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
    EVENT=$(echo "$RAW" | jq -r '.hook_event_name // "SessionStart"' 2>/dev/null)
fi

# Resolve vault root
VAULT_ROOT=""
if [[ -n "${PRIMOLABS_VAULT_ROOT:-}" && -d "$PRIMOLABS_VAULT_ROOT" ]]; then
    VAULT_ROOT="$PRIMOLABS_VAULT_ROOT"
elif [[ -d "$SCRIPT_DIR/.." ]]; then
    VAULT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
elif [[ -n "$CWD" ]]; then
    cur="$CWD"
    for _ in 1 2 3 4 5 6; do
        if [[ -d "$cur/agents" || -d "$cur/departments" ]]; then
            VAULT_ROOT="$cur"
            break
        fi
        cur="$( dirname "$cur" )"
        [[ "$cur" == "/" ]] && break
    done
fi

BODY=""
append() { BODY="${BODY}${1}
"; }

append ""
append "===== SESSION PRELUDE (auto-injected) ====="

# Dept/agent gate
if [[ -n "$CWD" && -n "$VAULT_ROOT" ]]; then
    REL="${CWD#$VAULT_ROOT}"
    REL="${REL#/}"
    AGENT=""
    DEPT=""
    if [[ "$REL" =~ ^agents/([^/]+) ]]; then
        AGENT="${BASH_REMATCH[1]}"
    elif [[ "$REL" =~ ^(departments|DEPARTMENTS)/([^/]+) ]]; then
        DEPT="${BASH_REMATCH[2]}"
    fi
    if [[ -n "$AGENT" ]]; then
        SKILL_PATH="$VAULT_ROOT/agents/$AGENT/SKILL.md"
        append ""
        append "*** AGENT WORK DETECTED: $AGENT ***"
        if [[ -f "$SKILL_PATH" ]]; then
            append "MANDATORY: Load this agent's SKILL.md before any work."
            append "  Path: agents/$AGENT/SKILL.md"
        else
            append "WARNING: No SKILL.md at $SKILL_PATH"
        fi
    elif [[ -n "$DEPT" ]]; then
        append ""
        append "*** DEPT WORK DETECTED: $DEPT ***"
        LOWER=$(echo "$DEPT" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
        for cand in \
            "$VAULT_ROOT/departments/$DEPT/skills/${LOWER}-master/SKILL.md" \
            "$VAULT_ROOT/departments/$DEPT/skills/${LOWER}/SKILL.md"
        do
            if [[ -f "$cand" ]]; then
                append "MANDATORY: Read the dept master skill BEFORE any Edit/Write."
                append "  Path: ${cand#$VAULT_ROOT/}"
                break
            fi
        done
    fi
fi

# Time (light, no hard stop — removed from ship vault, may return as opt-in cohort feature)
append ""
append "TIME: $(date '+%a %Y-%m-%d %I:%M %p')"

# Recent files
if [[ -n "$VAULT_ROOT" && -d "$VAULT_ROOT" ]]; then
    append ""
    append "RECENTLY MODIFIED FILES (last 24h):"
    FILES=$(find "$VAULT_ROOT/agents" "$VAULT_ROOT/departments" "$VAULT_ROOT/projects" "$VAULT_ROOT/skills" \
            -type f \( -name "*.md" -o -name "*.html" -o -name "*.json" -o -name "*.py" -o -name "*.ts" -o -name "*.ps1" -o -name "*.sh" \) \
            -mtime -1 2>/dev/null \
            | grep -v "\.git/" | grep -v "node_modules/" | grep -v "__pycache__/" \
            | head -15)
    if [[ -z "$FILES" ]]; then
        append "  (no modifications in last 24h)"
    else
        while IFS= read -r f; do
            REL="${f#$VAULT_ROOT/}"
            append "  $REL"
        done <<< "$FILES"
    fi
fi

# Protocol
append ""
append "PROTOCOL CHECKS BEFORE RESPONDING:"
append "  1. ADHD One-Thread — name pivots explicitly."
append "  2. Anchor on the active product, not the freshest file."
append "  3. Verify project status BEFORE speaking — read the recent files above."
append "  4. Investigate before apologizing."
append "  5. Match execution mode — ship 80% over wait at 100% when live with a client."

append ""
append "===== END PRELUDE ====="
append ""

if [[ "$EVENT" == "UserPromptSubmit" ]] && command -v jq >/dev/null 2>&1; then
    jq -n --arg ctx "$BODY" '{hookSpecificOutput:{hookEventName:"UserPromptSubmit",additionalContext:$ctx}}'
else
    printf "%s" "$BODY"
fi

exit 0
