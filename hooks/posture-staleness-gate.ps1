# posture-staleness-gate.ps1
# Event: PreToolUse (scoped to trading-analyst work)
# Reads agents/trading-analyst/memory/posture*.md HEAD freshness. If the latest
# posture note is older than $StaleDays days, surface STALE-REFUSE: blocks the
# trade verdict, requires posture re-verify.
#
# Defends against the 2026-05-14 09:35 stale-posture failure mode where a 2021
# setup was traded against 2026 macro because the agent never checked posture.
#
# This hook fires on EVERY PreToolUse but is a no-op unless cwd is inside
# agents/trading-analyst/. It also no-ops if the user prompt does not look
# like a trade-execution request (verdict/entry/stop/target keywords).

$ErrorActionPreference = 'SilentlyContinue'

$StaleDays = if ($env:PRIMOLABS_POSTURE_STALE_DAYS) { [int]$env:PRIMOLABS_POSTURE_STALE_DAYS } else { 7 }

function Resolve-VaultRoot {
    param($cwd)
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) { return $env:PRIMOLABS_VAULT_ROOT }
    if ($PSScriptRoot) {
        $parent = Split-Path $PSScriptRoot -Parent
        if ($parent -and (Test-Path $parent)) { return $parent }
    }
    if ($cwd) {
        $cur = $cwd
        for ($i = 0; $i -lt 6; $i++) {
            if ((Test-Path (Join-Path $cur 'agents')) -and (Test-Path (Join-Path $cur 'skills'))) { return $cur }
            $cur = Split-Path $cur -Parent
            if (-not $cur) { break }
        }
    }
    return $null
}

try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }

    $cwd = ""
    if ($data.cwd) { $cwd = $data.cwd }

    # Only fire when work appears to be in trading-analyst territory
    $inTrading = $false
    if ($cwd -and $cwd -match 'agents[\\/]trading-analyst') { $inTrading = $true }

    # Also fire if the recent user prompt mentions trade execution keywords
    # (this hook gets the tool args, not the prompt -- but if cwd isn't trading,
    # we look at the tool input for ticker/setup hints)
    $toolInput = ""
    if ($data.tool_input) {
        $toolInput = ($data.tool_input | ConvertTo-Json -Depth 5 -Compress 2>$null)
    }

    $tradeKeywords = '(?i)\b(entry|stop loss|target price|take profit|trade plan|trade setup|risk-sized|long this|short this|buy this|sell this|position size)\b'
    if (-not $inTrading -and ($toolInput -notmatch $tradeKeywords)) {
        exit 0
    }

    # Locate posture file
    $vaultRoot = Resolve-VaultRoot -cwd $cwd
    if (-not $vaultRoot) { exit 0 }

    $memDir = Join-Path $vaultRoot 'agents\trading-analyst\memory'
    if (-not (Test-Path $memDir)) { exit 0 }

    $postureFiles = Get-ChildItem -Path $memDir -Filter 'posture*.md' -ErrorAction SilentlyContinue
    if (-not $postureFiles -or $postureFiles.Count -eq 0) {
        $msg = @"
===== POSTURE GATE: MISSING =====

No posture file found at $memDir\posture*.md

Per the trading-analyst SKILL.md Posture-Current-Pole, every trade verdict
requires a posture read on file. Run mode=posture_read FIRST, write
memory/posture_<period>.md, then return to the trade.

REFUSING tool call until posture is on file.
===== END POSTURE GATE =====
"@
        # PreToolUse JSON: decision=block surfaces the message AND blocks the tool.
        $output = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'deny'
                permissionDecisionReason = $msg
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $output
        exit 0
    }

    # Pick newest posture file
    $latest = $postureFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1

    # Check HEAD block for last_verified: YYYY-MM-DD
    $headLines = Get-Content -Path $latest.FullName -TotalCount 30 -ErrorAction SilentlyContinue
    $lastVerified = $null
    foreach ($line in $headLines) {
        if ($line -match '(?i)last[_-]verified\s*[:=]\s*(\d{4}-\d{2}-\d{2})') {
            try { $lastVerified = [datetime]::ParseExact($Matches[1], 'yyyy-MM-dd', $null) } catch { }
            break
        }
    }

    # Fall back to file mtime if no explicit last_verified
    if (-not $lastVerified) {
        $lastVerified = $latest.LastWriteTime
    }

    $ageDays = ((Get-Date) - $lastVerified).TotalDays

    if ($ageDays -gt $StaleDays) {
        $rel = $latest.FullName.Substring($vaultRoot.Length).TrimStart('\','/')
        $msg = @"
===== POSTURE GATE: STALE-REFUSE =====

Posture file: $rel
Last verified: $($lastVerified.ToString('yyyy-MM-dd')) ($([math]::Round($ageDays,1)) days ago)
Threshold: $StaleDays days

Per trading-analyst SKILL.md anti-pattern "posture-stale-but-trading-anyway":
no trade verdict ships against a stale posture. The 2021 setup is not the
2026 setup when macro regime has moved.

Run mode=posture_read FIRST. Update memory/posture_<period>.md with current
VIX / DXY / 10Y / regime read. Set last_verified to today. Then re-issue
the verdict.

REFUSING tool call until posture is current.
===== END POSTURE GATE =====
"@
        $output = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'deny'
                permissionDecisionReason = $msg
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $output
        exit 0
    }

    # Fresh -- silent pass
    exit 0

} catch {
    exit 0
}
