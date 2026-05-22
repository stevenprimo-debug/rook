# preamble-resolver.ps1 -- ROOK Tiered Preamble Resolver (Windows)
# ---------------------------------------------------------------------------
# Fires on SessionStart (after session-prelude.ps1).
# Loads tiered preamble content from .claude/preamble/T1.md through T4.md
# and injects into the session system-reminder.
#
# Tier selection: reads $env:ROOK_PREAMBLE_TIER (default 2 if unset).
# Agents declare their tier in their SKILL.md frontmatter (preamble-tier: 1|2|3|4).
# If unset, T1+T2 fires (safe default for all agents).
#
# Output: writes preamble block to stdout so Claude Code picks it up as
# a system-reminder injection (same pattern as session-prelude.ps1).

$ErrorActionPreference = 'SilentlyContinue'

$VaultRoot = $env:PRIMOLABS_VAULT_ROOT
if (-not $VaultRoot) {
    # Fall back to relative detection from this script's location
    $VaultRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
}

$PreambleDir = Join-Path $VaultRoot '.claude\preamble'

# Determine tier from env (default 2)
$Tier = [int]($env:ROOK_PREAMBLE_TIER)
if ($Tier -lt 1 -or $Tier -gt 4) { $Tier = 2 }

# Load tiers 1..N cumulatively (T4 includes T1+T2+T3+T4)
$blocks = @()
for ($t = 1; $t -le $Tier; $t++) {
    $p = Join-Path $PreambleDir "T$t.md"
    if (Test-Path $p) {
        $blocks += (Get-Content -Raw -Path $p -Encoding UTF8)
    }
}

if ($blocks.Count -eq 0) {
    exit 0
}

$separator = "`n`n---`n`n"
$preamble = "===== ROOK PREAMBLE (Tier $Tier) =====`n`n" + ($blocks -join $separator) + "`n`n===== END ROOK PREAMBLE ====="

Write-Output $preamble
exit 0
