#!/usr/bin/env bash
# routing-enforcer.sh
# Event: UserPromptSubmit
# Reads routing-rules.json (sibling to this script), matches the user prompt
# against each agent's keyword set, and injects each matching entry's
# enforce_message into the context.
#
# Manifest resolution:
#   1. $PRIMOLABS_HOOKS_DIR/routing-rules.json
#   2. <script dir>/routing-rules.json
#   3. $PRIMOLABS_VAULT_ROOT/hooks/routing-rules.json
#
# Requires: jq (https://stedolan.github.io/jq/)
# Falls back to silent-pass if jq is missing — never blocks a prompt.

set -u

MAX_DEPTS=3
MIN_WORDS=3

# Silent fail wrapper
fail_silent() { exit 0; }
trap fail_silent ERR

# Locate jq
if ! command -v jq >/dev/null 2>&1; then
    exit 0
fi

# Resolve script dir
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Resolve manifest
MANIFEST=""
for cand in \
    "${PRIMOLABS_HOOKS_DIR:-}/routing-rules.json" \
    "$SCRIPT_DIR/routing-rules.json" \
    "${PRIMOLABS_VAULT_ROOT:-}/hooks/routing-rules.json"
do
    if [[ -n "$cand" && -f "$cand" ]]; then
        MANIFEST="$cand"
        break
    fi
done
[[ -z "$MANIFEST" ]] && exit 0

# Read prompt from stdin
RAW=$(cat)
[[ -z "$RAW" ]] && exit 0

PROMPT=$(echo "$RAW" | jq -r '.prompt // empty' 2>/dev/null)
[[ -z "$PROMPT" ]] && exit 0

WORD_COUNT=$(echo "$PROMPT" | wc -w | tr -d ' ')
[[ "$WORD_COUNT" -lt "$MIN_WORDS" ]] && exit 0

# Pick agents or departments key
ENTRY_KEY=$(jq -r 'if .agents then "agents" elif .departments then "departments" else empty end' "$MANIFEST")
[[ -z "$ENTRY_KEY" ]] && exit 0

# Iterate keys, accumulate match counts
declare -A MATCHES
PROMPT_LC=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

while IFS= read -r DEPT_KEY; do
    [[ -z "$DEPT_KEY" ]] && continue
    COUNT=0

    # Primary keywords
    while IFS= read -r KW; do
        [[ -z "$KW" ]] && continue
        KW_LC=$(echo "$KW" | tr '[:upper:]' '[:lower:]')
        if [[ "$PROMPT_LC" == *"$KW_LC"* ]]; then
            COUNT=$((COUNT + 2))
        fi
    done < <(jq -r ".${ENTRY_KEY}[\"$DEPT_KEY\"].primary_keywords[]? // empty" "$MANIFEST" 2>/dev/null)

    # Secondary keywords (half weight = 1)
    while IFS= read -r KW; do
        [[ -z "$KW" ]] && continue
        KW_LC=$(echo "$KW" | tr '[:upper:]' '[:lower:]')
        if [[ "$PROMPT_LC" == *"$KW_LC"* ]]; then
            COUNT=$((COUNT + 1))
        fi
    done < <(jq -r ".${ENTRY_KEY}[\"$DEPT_KEY\"].secondary_keywords[]? // empty" "$MANIFEST" 2>/dev/null)

    # Excludes (demote)
    while IFS= read -r EX; do
        [[ -z "$EX" ]] && continue
        EX_LC=$(echo "$EX" | tr '[:upper:]' '[:lower:]')
        if [[ "$PROMPT_LC" == *"$EX_LC"* ]]; then
            COUNT=$((COUNT - 4))
            [[ "$COUNT" -lt 0 ]] && COUNT=0
        fi
    done < <(jq -r ".${ENTRY_KEY}[\"$DEPT_KEY\"].excludes | if . then keys[] else empty end" "$MANIFEST" 2>/dev/null)

    if [[ "$COUNT" -gt 0 ]]; then
        MATCHES["$DEPT_KEY"]=$COUNT
    fi
done < <(jq -r ".${ENTRY_KEY} | keys[]" "$MANIFEST" 2>/dev/null)

[[ ${#MATCHES[@]} -eq 0 ]] && exit 0

# Sort by score desc, take top N
SORTED=$(
    for k in "${!MATCHES[@]}"; do
        echo "${MATCHES[$k]} $k"
    done | sort -rn | head -n "$MAX_DEPTS" | awk '{print $2}'
)

# Build reminder body
SECTIONS=""
while IFS= read -r DEPT_KEY; do
    [[ -z "$DEPT_KEY" ]] && continue
    ROLE=$(jq -r ".${ENTRY_KEY}[\"$DEPT_KEY\"].role // empty" "$MANIFEST")
    MSG=$(jq -r ".${ENTRY_KEY}[\"$DEPT_KEY\"].enforce_message // empty" "$MANIFEST")
    [[ -z "$MSG" ]] && continue

    SECTION="*** $DEPT_KEY KEYWORDS DETECTED (role: $ROLE) ***
$MSG"

    # Upstream chain?
    UPSTREAM=$(jq -r ".dispatch_chains[\"$DEPT_KEY\"].upstream | if . then join(\" -> \") else empty end" "$MANIFEST" 2>/dev/null)
    CHAIN_REASON=$(jq -r ".dispatch_chains[\"$DEPT_KEY\"].reason // empty" "$MANIFEST" 2>/dev/null)
    if [[ -n "$UPSTREAM" ]]; then
        SECTION="$SECTION

UPSTREAM DISPATCH CHAIN: $UPSTREAM -> $DEPT_KEY
Reason: $CHAIN_REASON"
    fi

    if [[ -z "$SECTIONS" ]]; then
        SECTIONS="$SECTION"
    else
        SECTIONS="$SECTIONS

----

$SECTION"
    fi
done <<< "$SORTED"

[[ -z "$SECTIONS" ]] && exit 0

MANIFEST_REL=$(basename "$MANIFEST")
REMINDER="===== ROUTING ENFORCER (auto-injected) =====

Manifest: $MANIFEST_REL (single source of truth — edit there, not here)

$SECTIONS

----

GLOBAL RULES (every fire):
  - Output format: your FIRST response line MUST be one of:
      [DEPLOY] <one-sentence classification>
      [ASSIGN] <one-sentence classification>
      [PARK]   <one-sentence classification>
    If you ask any question or take any action before stating the route,
    you have failed the protocol. Per feedback_ceo_dispatch_route_before_asking.md.
  - Main-thread anti-thesis: dispatch a subagent for analysis/verdict work.
  - Reversibility gate: irreversible actions require explicit user confirm.
  - False positive: if the work is ABOUT the dept (not IN the dept), proceed.

===== END ROUTING ENFORCER ====="

# Emit JSON
jq -n --arg ctx "$REMINDER" '{
    hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext: $ctx
    }
}'

exit 0
