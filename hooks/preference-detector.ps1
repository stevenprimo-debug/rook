# preference-detector.ps1
# Event: UserPromptSubmit
# Detects spoken preferences in the user prompt -- patterns like
# "always do X", "every time", "from now on", "never do Y", "remind me to",
# "before responding", "after every Write/Edit" -- and surfaces a system
# reminder that points Claude at the `auto-hook-from-preference` skill.
#
# This hook does NOT generate the hook itself; the skill does. The hook's
# job is to make sure the skill fires on the right prompts so preferences
# don't silently die in chat.

$ErrorActionPreference = 'SilentlyContinue'

# Preference patterns -- ordered loosely by strength
$PreferencePatterns = @(
    '(?i)\bfrom now on\b',
    '(?i)\balways (do|use|include|run|check|verify|read|load|invoke|remember|remind)\b',
    '(?i)\bevery time\b',
    '(?i)\bnever (do|use|skip|ignore|forget|bypass)\b',
    '(?i)\bremind me to\b',
    '(?i)\bwhenever (i|you) \w+',
    '(?i)\bbefore (responding|replying|answering|tool)',
    '(?i)\bafter (every|each) (write|edit|tool|response|command)\b',
    '(?i)\bmake (this|that) a (rule|hook|automatic)\b',
    '(?i)\b/auto[-_]?hook\b',
    '(?i)\bauto[- ]?hook this\b',
    '(?i)\bstop (asking|reminding|saying|doing|requesting)\b',
    '(?i)\bmake sure to always\b'
)

# Anti-patterns -- phrases that LOOK like preferences but are descriptive
# ("I always forget to...", "you always do that")
$AntiPatterns = @(
    '(?i)\bi always (forget|miss|skip|mess up)\b',
    '(?i)\byou always (do|forget|miss)\b',
    '(?i)\bthat''?s always how\b'
)

try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
    $prompt = $data.prompt
    if (-not $prompt) { exit 0 }

    # Anti-pattern check -- skip if descriptive
    foreach ($p in $AntiPatterns) {
        if ($prompt -match $p) { exit 0 }
    }

    $hits = @()
    foreach ($p in $PreferencePatterns) {
        if ($prompt -match $p) { $hits += $Matches[0] }
    }

    if ($hits.Count -eq 0) { exit 0 }

    # De-dupe
    $unique = $hits | Select-Object -Unique
    $hitList = ($unique | ForEach-Object { "  - `"$_`"" }) -join "`n"

    $reminder = @"
===== PREFERENCE DETECTED =====

The prompt contains preference language:
$hitList

This is a candidate for harness-level enforcement via the
'auto-hook-from-preference' skill (skills/registry/auto-hook-from-preference).

BEFORE answering anything else, decide:
  1. Is this a recurring preference the user wants enforced? -> INVOKE
     auto-hook-from-preference skill with the verbatim quote. The skill
     classifies it (UserPromptSubmit / PreToolUse / PostToolUse / SessionStart /
     Stop / scheduled-task / memory-only), drafts a hook script + settings.json
     edit + memory entry, then asks ONE confirm.
  2. Is this a one-off behavioral note for this thread? -> Acknowledge in chat,
     proceed with the actual task. No hook needed.

If unsure, ASK the user: "Want me to convert that to a hook so the harness
enforces it automatically?" -- then proceed if yes.

Memory rules are advisory; hooks are enforced. The drift gap this closes:
saying it once should be enough.

===== END PREFERENCE DETECTED =====
"@

    $output = @{
        hookSpecificOutput = @{
            hookEventName     = 'UserPromptSubmit'
            additionalContext = $reminder
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 0

} catch {
    exit 0
}
