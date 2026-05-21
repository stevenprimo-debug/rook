# context-watch-gate.ps1
# Event: UserPromptSubmit
# Proactive context-usage monitor. Closes the gap that PreCompact (harness-fired
# near 100%) is too late to save in-flight work.
#
# Reads the session transcript JSONL provided in the stdin payload, walks the
# usage blocks to compute the CURRENT resident context (latest usage block --
# matches what Claude Code's UI shows), and emits:
#   - silent pass below the warn threshold (default 70%)
#   - visible chat warning between warn and hardstop (default 70-84%)
#   - system-reminder HARD STOP at hardstop+ (default 85%) instructing the model
#     to write a structured handoff before responding to the user's prompt
#
# Token-counting algorithm:
#   For each JSONL line that parses as JSON and exposes message.usage:
#     effective = input_tokens + cache_creation_input_tokens + cache_read_input_tokens
#   Track LATEST (most recent) such block in file order. This matches what the
#   Claude Code UI reports because the harness auto-compacts on overflow, so
#   the peak watermark earlier in the session is NOT current resident size.
#   Also track the session peak for the warning message body.
#
#   Fallback (no usage blocks found yet): count total characters of message
#   content / 3.5 chars-per-token. Conservative-ish for English+code mix.
#
# Model-window detection:
#   The JSONL "model" field is bare "claude-opus-4-7" for BOTH the 200K and
#   1M variants -- Anthropic does not include the [1m] suffix in the stored
#   model id. So we fall back to evidence: if ANY observed usage block sum
#   exceeded 200K, the session must be on the 1M variant (impossible on 200K).
#   The explicit [1m]/-1m/_1m regex is kept as a secondary signal in case
#   Anthropic adds the suffix to the field in future versions.
#
# Configuration (env vars, all optional):
#   ROOK_CONTEXT_WARN_PCT       default 70    -- pct that triggers visible warning
#   ROOK_CONTEXT_HARDSTOP_PCT   default 85    -- pct that triggers hard-stop reminder
#   ROOK_CONTEXT_WATCH_DISABLED set to "1"    -- escape hatch, silences entirely
#   CLAUDE_MAX_CONTEXT_TOKENS   default 200000 -- model context window (explicit override)
#
# Error handling: any exception -> exit 0 silently. NEVER break prompt submission.

$ErrorActionPreference = 'SilentlyContinue'

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
    # Escape hatch
    if ($env:ROOK_CONTEXT_WATCH_DISABLED -eq '1') { exit 0 }

    # Thresholds
    $warnPct = 70
    $stopPct = 85
    if ($env:ROOK_CONTEXT_WARN_PCT) {
        $parsed = 0
        if ([int]::TryParse($env:ROOK_CONTEXT_WARN_PCT, [ref]$parsed) -and $parsed -gt 0 -and $parsed -lt 100) {
            $warnPct = $parsed
        }
    }
    if ($env:ROOK_CONTEXT_HARDSTOP_PCT) {
        $parsed = 0
        if ([int]::TryParse($env:ROOK_CONTEXT_HARDSTOP_PCT, [ref]$parsed) -and $parsed -gt 0 -and $parsed -le 100) {
            $stopPct = $parsed
        }
    }
    if ($stopPct -le $warnPct) { $stopPct = [Math]::Min(99, $warnPct + 10) }

    # Read payload
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    $data = $null
    try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
    if (-not $data) { exit 0 }

    $cwd = ''
    if ($data.cwd) { $cwd = $data.cwd }
    $transcriptPath = $null
    if ($data.transcript_path) { $transcriptPath = $data.transcript_path }
    if (-not $transcriptPath -or -not (Test-Path -LiteralPath $transcriptPath)) { exit 0 }

    # Context window detection (env var wins; otherwise inferred below)
    $maxContext = 200000
    $envOverride = $false
    if ($env:CLAUDE_MAX_CONTEXT_TOKENS) {
        $parsed = 0
        if ([int]::TryParse($env:CLAUDE_MAX_CONTEXT_TOKENS, [ref]$parsed) -and $parsed -gt 1000) {
            $maxContext = $parsed
            $envOverride = $true
        }
    }

    # Walk the JSONL:
    #   - latestEffective: input+cache_creation+cache_read on the LAST usage block we see
    #   - peakEffective:   max of same across the whole file (for warning body)
    #   - modelHint1M / modelHint200K: regex hints on "model" field (rare, kept for future)
    #   - usageExceeds200K: evidence-based 1M signal (any usage sum > 200K proves 1M model)
    $latestEffective = 0
    $peakEffective = 0
    $totalChars = 0
    $modelHint1M = $false
    $modelHint200K = $false
    $usageExceeds200K = $false

    $reader = [System.IO.File]::OpenText($transcriptPath)
    try {
        while (-not $reader.EndOfStream) {
            $line = $reader.ReadLine()
            if (-not $line) { continue }
            $obj = $null
            try { $obj = $line | ConvertFrom-Json -ErrorAction Stop } catch { continue }
            if (-not $obj) { continue }

            # Model hint scan (kept for future-proofing; today's JSONL strips the [1m] suffix)
            $modelField = $null
            if ($obj.message -and $obj.message.model) { $modelField = $obj.message.model }
            elseif ($obj.model) { $modelField = $obj.model }
            if ($modelField) {
                $m = $modelField.ToString().ToLower()
                if ($m -match '\[1m\]' -or $m -match '-1m\b' -or $m -match '_1m\b') { $modelHint1M = $true }
                elseif ($m -match '200k') { $modelHint200K = $true }
            }

            # Usage extraction
            $usage = $null
            if ($obj.message -and $obj.message.usage) { $usage = $obj.message.usage }
            elseif ($obj.usage) { $usage = $obj.usage }
            if ($usage) {
                $inp = 0; $cc = 0; $cr = 0
                if ($usage.input_tokens) { $inp = [int]$usage.input_tokens }
                if ($usage.cache_creation_input_tokens) { $cc = [int]$usage.cache_creation_input_tokens }
                if ($usage.cache_read_input_tokens) { $cr = [int]$usage.cache_read_input_tokens }
                $eff = $inp + $cc + $cr
                if ($eff -gt 0) {
                    $latestEffective = $eff
                    if ($eff -gt $peakEffective) { $peakEffective = $eff }
                    if ($eff -gt 200000) { $usageExceeds200K = $true }
                }
            }

            # Char fallback accumulation (only used if no usage found)
            if ($obj.message -and $obj.message.content) {
                $c = $obj.message.content
                if ($c -is [string]) { $totalChars += $c.Length }
                elseif ($c -is [System.Array]) {
                    foreach ($block in $c) {
                        if ($block.text) { $totalChars += $block.text.ToString().Length }
                        elseif ($block -is [string]) { $totalChars += $block.Length }
                    }
                }
            }
        }
    } finally {
        $reader.Close()
    }

    # Resolve effective context size from LATEST observed usage (current resident).
    $effectiveTokens = $latestEffective
    if ($effectiveTokens -le 0) {
        # Fallback: chars / 3.5
        if ($totalChars -gt 0) {
            $effectiveTokens = [int]($totalChars / 3.5)
        } else {
            exit 0
        }
    }

    # Apply model hints only if user did not explicitly override via env.
    # Evidence (any usage > 200K) is the strongest 1M signal because the JSONL
    # model field today is bare "claude-opus-4-7" for both variants.
    if (-not $envOverride) {
        if ($usageExceeds200K -or $modelHint1M) {
            $maxContext = 1000000
        } elseif ($modelHint200K) {
            $maxContext = 200000
        }
    }

    if ($maxContext -le 0) { exit 0 }
    $pct = [int][Math]::Round(($effectiveTokens / [double]$maxContext) * 100, 0)

    if ($pct -lt $warnPct) {
        # Silent pass
        exit 0
    }

    if ($pct -lt $stopPct) {
        # Visible warning in chat (not a system-reminder)
        $msg = "[context-watch] Session context at $pct% of $maxContext tokens (~$effectiveTokens current). Peak this session: ~$peakEffective. Hard stop fires at $stopPct% and will force a handoff write. Consider wrapping the current sub-task at a natural break and writing a handoff now."
        Write-Output $msg
        exit 0
    }

    # Hard stop: emit system-reminder instructing model to write handoff
    $vaultRoot = Resolve-VaultRoot -cwd $cwd
    $timestamp = (Get-Date).ToString('yyyy-MM-dd-HHmm')
    $handoffRelative = "agents/chief-of-staff/memory/session_handoffs/$timestamp-watchgate.md"
    if ($vaultRoot) {
        $handoffDir = Join-Path $vaultRoot 'agents\chief-of-staff\memory\session_handoffs'
        if (-not (Test-Path $handoffDir)) {
            New-Item -ItemType Directory -Path $handoffDir -Force | Out-Null
        }
    }

    $reminder = @"
===== CONTEXT WATCH -- HARD STOP =====

Session context is at $pct% of the $maxContext-token window
(~$effectiveTokens tokens resident; peak this session ~$peakEffective).
The harness PreCompact event fires near 100% -- too late to safely write
a handoff. This gate fires at $stopPct% so the operator does not lose work.

MANDATORY (before responding to the user's prompt above): write a
structured session handoff to:

    $handoffRelative

Use this shape (compounding-append friendly):

```
---
date: $timestamp
type: handoff
trigger: context-watch-gate
context_pct: $pct
---

## Goals locked this session
[1-3 bullets -- what was the mission]

## Decisions made
[Each decision with the why, not just the what]

## Files modified
[Path + one-line change description per file]

## Current state
[Where things stand right now -- what's done, what's in flight]

## Next steps
[Top 3 actions for the next session to pick up cold]

## Open contradictions / things to surface
[Anything the librarian should flag next sweep, OR nothing.]
```

After writing the handoff, answer the user's prompt as normal. The handoff
is the safety net -- the librarian sweep will index it, and the next
session's session-prelude will surface it as recent activity.

To silence this gate (not recommended) set ROOK_CONTEXT_WATCH_DISABLED=1.
To adjust thresholds: ROOK_CONTEXT_WARN_PCT / ROOK_CONTEXT_HARDSTOP_PCT.

===== END CONTEXT WATCH =====
"@

    Write-Output $reminder
    exit 0

} catch {
    exit 0
}
