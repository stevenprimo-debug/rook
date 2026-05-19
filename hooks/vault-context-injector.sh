#!/usr/bin/env bash
# vault-context-injector.sh
# UserPromptSubmit hook -- bash port of vault-context-injector.ps1
# Performs deterministic vault grep for keywords in the operator's prompt
# and injects findings as a system reminder.
#
# Vault root resolution: $PRIMOLABS_VAULT_ROOT -> <script dir>/.. -> data.cwd

set -u

MAX_KEYWORDS=5
MAX_FILES_PER_KW=4
MAX_MATCHES_TOTAL=12
MIN_PROMPT_WORDS=5
SNIPPET_CHARS=100
HARD_TIMEOUT_SEC=5

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Read stdin (JSON from Claude Code)
RAW=$(cat 2>/dev/null || true)
[ -z "$RAW" ] && exit 0

# Extract prompt + cwd from JSON (jq optional; fallback to grep)
if command -v jq >/dev/null 2>&1; then
    PROMPT=$(echo "$RAW" | jq -r '.prompt // empty' 2>/dev/null)
    CWD=$(echo "$RAW" | jq -r '.cwd // empty' 2>/dev/null)
else
    PROMPT=$(echo "$RAW" | grep -o '"prompt"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"prompt"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
    CWD=$(echo "$RAW" | grep -o '"cwd"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"cwd"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
fi
[ -z "$PROMPT" ] && exit 0

# Opt-out
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')
for pat in "skip vault" "no search" "ignore vault" "no context" "fresh start" "no rag"; do
    case "$PROMPT_LOWER" in *"$pat"*) exit 0 ;; esac
done

# Skip on too-short prompts
WORD_COUNT=$(echo "$PROMPT" | tr -s '[:space:]' '\n' | grep -c .)
[ "$WORD_COUNT" -lt "$MIN_PROMPT_WORDS" ] && exit 0

# Resolve vault root
resolve_vault_root() {
    if [ -n "${PRIMOLABS_VAULT_ROOT:-}" ] && [ -d "$PRIMOLABS_VAULT_ROOT" ]; then
        echo "$PRIMOLABS_VAULT_ROOT"; return
    fi
    local parent="$(dirname "$SCRIPT_DIR")"
    if [ -d "$parent" ]; then echo "$parent"; return; fi
    # Walk up from cwd
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

# Stopwords (compact set)
STOPWORDS=" a an the is are was were be been being am do does did have has had will would can could should may might must shall this that these those with from into onto about what who when where why how and or but if then else you your yours we our ours my mine me i it its them they their just like want need get got go going make made know think really also some any all one two three thing things stuff here there today tomorrow yesterday now next last for to of in on at as by up down out off over under again more most other than so no not very too only own same such well maybe probably definitely actually basically literally okay ok yeah yes sure sort kind "

# Tokenize: extract alphanumeric words length>=3
TOKENS=$(echo "$PROMPT" | tr -c '[:alnum:]_-' ' ' | tr -s ' ' '\n' | awk 'length($0)>=3')

# Filter out stopwords, score by length, preserve order for bigrams later
declare -A SCORED
declare -a CANDIDATES
while IFS= read -r word; do
    [ -z "$word" ] && continue
    lower=$(echo "$word" | tr '[:upper:]' '[:lower:]')
    case "$STOPWORDS" in *" $lower "*) continue ;; esac
    CANDIDATES+=("$word")
    # Score: length + 4 if capitalized, +2 if length>=6
    score=${#word}
    [[ "$word" =~ ^[A-Z] ]] && score=$((score + 4))
    [ "${#word}" -ge 6 ] && score=$((score + 2))
    existing=${SCORED["$lower"]:-0}
    SCORED["$lower"]=$((existing + score))
done <<< "$TOKENS"

[ "${#CANDIDATES[@]}" -eq 0 ] && exit 0

# Top N keywords by score
TOP_KEYWORDS=$(
    for key in "${!SCORED[@]}"; do
        echo "${SCORED[$key]} $key"
    done | sort -rn | head -n "$MAX_KEYWORDS" | awk '{$1=""; print $0}' | sed 's/^ //'
)

[ -z "$TOP_KEYWORDS" ] && exit 0

# Grep vault for each keyword
declare -a ALL_MATCHES
START_TIME=$(date +%s)
SEARCH_PATHS=("agents" "projects" "_archive")

while IFS= read -r kw; do
    [ -z "$kw" ] && continue
    NOW=$(date +%s)
    [ $((NOW - START_TIME)) -gt "$HARD_TIMEOUT_SEC" ] && break

    for sp in "${SEARCH_PATHS[@]}"; do
        full_path="$VAULT_ROOT/$sp"
        [ ! -d "$full_path" ] && continue

        # Use grep -rl for matching files, then grep -n for line numbers (capped per keyword)
        matches=$(grep -rln --include='*.md' -F -- "$kw" "$full_path" 2>/dev/null | head -n "$MAX_FILES_PER_KW")
        while IFS= read -r mpath; do
            [ -z "$mpath" ] && continue
            line_info=$(grep -n -F -- "$kw" "$mpath" 2>/dev/null | head -n 1)
            line_num=$(echo "$line_info" | cut -d: -f1)
            snippet=$(echo "$line_info" | cut -d: -f2- | sed 's/^[[:space:]]*//' | head -c "$SNIPPET_CHARS")
            rel_path="${mpath#$VAULT_ROOT/}"
            ALL_MATCHES+=("[$kw] $rel_path:$line_num  $snippet")
        done <<< "$matches"
    done
done <<< "$TOP_KEYWORDS"

[ "${#ALL_MATCHES[@]}" -eq 0 ] && exit 0

# Dedup by path, cap total
DEDUPED=$(printf '%s\n' "${ALL_MATCHES[@]}" | awk -F':' '!seen[$2]++' | head -n "$MAX_MATCHES_TOTAL")

KW_LIST=$(echo "$TOP_KEYWORDS" | paste -sd ', ' -)

cat <<EOF
===== VAULT CONTEXT (auto-injected, deterministic) =====

Keywords searched: $KW_LIST
Matches found across the agent roster + projects + archive:

$DEDUPED

USE THIS CONTEXT FIRST. Read the most-relevant matched files BEFORE
responding to the operator's prompt. Do NOT ask the operator to provide
context that is already in the vault. If matches are stale or off-topic,
say so and proceed -- but always check first.

===== END VAULT CONTEXT =====
EOF

exit 0
