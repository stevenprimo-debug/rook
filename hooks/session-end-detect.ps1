# session-end-detect.ps1
# Event: UserPromptSubmit
# Detects natural-language session-end signals in the operator's prompt
# ("signing off", "wrap up", "calling it", etc.) and injects a "write final
# handoff" reminder.
#
# Companion to precompact-handoff.ps1. PreCompact catches involuntary
# context drops; this catches the operator's voluntary "I'm done for now."

$ErrorActionPreference = 'SilentlyContinue'

# Natural-language signals. Lowercase-match against the prompt.
$SessionEndSignals = @(
    'signing off',
    'sign off',
    'wrap up',
    'wrapping up',
    "let's wrap",
    'wrap it up',
    'calling it',
    "i'm done",
    'done for now',
    'done for the day',
    'done for tonight',
    'going to bed',
    'heading out',
    'heading home',
    'shutting down',
    'end of session',
    'end the session',
    'session end',
    'closing out',
    'closing this out',
    'time to stop',
    "that's it for today",
    "that's it for tonight",
    'see you tomorrow',
    'catch you tomorrow',
    'catch you next time'
)

function Resolve-VaultRoot {
    param($cwd)
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) {
        return $env:PRIMOLABS_VAULT_ROOT
    }
    if ($PSScriptRoot) {
        $parent = Split-Path $PSScriptRoot -Parent
        if ($parent -and (Test-Path $parent)) { return $parent }
    }
    if ($cwd -and (Test-Path $cwd)) {
        $cur = $cwd
        for ($i = 0; $i -lt 6; $i++) {
            if ((Test-Path (Join-Path $cur 'agents')) -and (Test-Path (Join-Path $cur 'hooks'))) {
                return $cur
            }
            $cur = Split-Path $cur -Parent
            if (-not $cur) { break }
        }
    }
    return $null
}

try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }
    $data = $raw | ConvertFrom-Json -ErrorAction Stop
    $prompt = $data.prompt
    if (-not $prompt) { exit 0 }

    $promptLower = $prompt.ToLower()
    $signalMatched = $null
    foreach ($sig in $SessionEndSignals) {
        if ($promptLower -match [regex]::Escape($sig)) {
            $signalMatched = $sig
            break
        }
    }
    if (-not $signalMatched) { exit 0 }

    $cwd = ""
    if ($data.cwd) { $cwd = $data.cwd }
    $vaultRoot = Resolve-VaultRoot -cwd $cwd
    if (-not $vaultRoot) { exit 0 }

    $timestamp = (Get-Date).ToString('yyyy-MM-dd-HHmm')
    $handoffDir = Join-Path $vaultRoot 'agents\chief-of-staff\memory\session_handoffs'
    if (-not (Test-Path $handoffDir)) {
        New-Item -ItemType Directory -Path $handoffDir -Force | Out-Null
    }
    $handoffRelative = "agents/chief-of-staff/memory/session_handoffs/$timestamp-sessionend.md"

    $reminder = @"
===== SESSION-END SIGNAL DETECTED =====

The operator's prompt contains a session-end signal: "$signalMatched"

MANDATORY (before saying goodbye): write a final session handoff to:

    $handoffRelative

Use this shape:

```
---
date: $timestamp
type: handoff
trigger: session-end
signal_phrase: "$signalMatched"
---

## What we shipped this session
[Bullet list of completed work — files changed, decisions locked, problems solved]

## What's parked / still open
[Anything intentionally not finished — with the reason and the trigger to pick it back up]

## Locked decisions worth remembering
[Decisions that should survive into future sessions — with the *why*]

## Next session pickup
[The first 3 things the next session should do, cold-start]

## Anything to flag for the librarian
[Contradictions, drift candidates, audit items — OR nothing.]
```

THEN respond to the operator's actual sign-off message. The handoff is
the institutional-memory closure — without it, this session's compounding
value is lost the moment the window closes.

After writing the handoff, end with a one-line confirmation to the operator:
"Handoff written: <relative path>. Catch you next time."

===== END SESSION-END SIGNAL =====
"@

    Write-Output $reminder
    exit 0

} catch {
    exit 0
}
