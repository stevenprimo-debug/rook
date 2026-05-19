#!/usr/bin/env bash
# preference-detector.sh
# Event: UserPromptSubmit
# Detects spoken preferences and surfaces an auto-hook-from-preference invocation hint.

set -u

if ! command -v jq >/dev/null 2>&1; then exit 0; fi

RAW=$(cat 2>/dev/null || true)
[[ -z "$RAW" ]] && exit 0

PROMPT=$(echo "$RAW" | jq -r '.prompt // empty' 2>/dev/null)
[[ -z "$PROMPT" ]] && exit 0

# Anti-patterns first (descriptive, not directive)
if echo "$PROMPT" | grep -qiE '\bi always (forget|miss|skip|mess up)\b'; then exit 0; fi
if echo "$PROMPT" | grep -qiE '\byou always (do|forget|miss)\b'; then exit 0; fi
if echo "$PROMPT" | grep -qiE "\bthat'?s always how\b"; then exit 0; fi

PATTERNS=(
    '\bfrom now on\b'
    '\balways (do|use|include|run|check|verify|read|load|invoke|remember|remind)\b'
    '\bevery time\b'
    '\bnever (do|use|skip|ignore|forget|bypass)\b'
    '\bremind me to\b'
    '\bwhenever (i|you) [a-z]+'
    '\bbefore (responding|replying|answering|tool)'
    '\bafter (every|each) (write|edit|tool|response|command)\b'
    '\bmake (this|that) a (rule|hook|automatic)\b'
    '\b/auto[-_]?hook\b'
    '\bauto[- ]?hook this\b'
    '\bstop (asking|reminding|saying|doing|requesting)\b'
    '\bmake sure to always\b'
)

HITS=""
for p in "${PATTERNS[@]}"; do
    MATCH=$(echo "$PROMPT" | grep -oiE "$p" | head -1)
    if [[ -n "$MATCH" ]]; then
        HITS="${HITS}  - \"$MATCH\"
"
    fi
done

[[ -z "$HITS" ]] && exit 0

REMINDER="===== PREFERENCE DETECTED =====

The prompt contains preference language:
$HITS
This is a candidate for harness-level enforcement via the
auto-hook-from-preference skill (skills/registry/auto-hook-from-preference).

BEFORE answering anything else, decide:
  1. Is this a recurring preference to enforce? → INVOKE
     auto-hook-from-preference skill with the verbatim quote.
  2. Is this a one-off note for this thread? → Acknowledge, proceed.

If unsure, ASK: 'Want me to convert that to a hook?' — then proceed if yes.

===== END PREFERENCE DETECTED ====="

jq -n --arg ctx "$REMINDER" '{hookSpecificOutput:{hookEventName:"UserPromptSubmit",additionalContext:$ctx}}'
exit 0
