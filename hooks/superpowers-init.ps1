# superpowers-init.ps1
# Event: SessionStart
# Confirms `using-superpowers` skill is invocable, logs the Skill-tool
# requirement so Claude reads it BEFORE answering anything (including
# clarifying questions). Falls back gracefully if the skill is missing.
#
# Resolution: looks for skills/registry/using-superpowers/SKILL.md under
# the vault root (env var, sibling-to-hooks, or stdin cwd walk-up).

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
            if ((Test-Path (Join-Path $cur 'skills')) -and (Test-Path (Join-Path $cur 'agents'))) {
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
    try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { $data = $null }

    $cwd = ""
    if ($data -and $data.cwd) { $cwd = $data.cwd }

    $vaultRoot = Resolve-VaultRoot -cwd $cwd

    $skillPath = $null
    if ($vaultRoot) {
        $candidates = @(
            (Join-Path $vaultRoot 'skills\registry\using-superpowers\SKILL.md'),
            (Join-Path $vaultRoot 'skills\using-superpowers\SKILL.md')
        )
        foreach ($c in $candidates) {
            if (Test-Path $c) { $skillPath = $c; break }
        }
    }

    $lines = @()
    $lines += ""
    $lines += "===== SUPERPOWERS INIT ====="

    if ($skillPath) {
        $rel = if ($vaultRoot) { $skillPath.Substring($vaultRoot.Length).TrimStart('\','/') } else { $skillPath }
        $lines += "Skill registry detected. The `using-superpowers` skill is invocable."
        $lines += "  Location: $rel"
        $lines += ""
        $lines += "MANDATORY before ANY response (including clarifying questions):"
        $lines += "  1. If you think there is even a 1% chance a skill applies to this task, INVOKE IT."
        $lines += "  2. Use the Skill tool -- never read SKILL.md files via the Read tool."
        $lines += "  3. Skill bodies are loaded into your context when invoked -- follow them directly."
        $lines += ""
        $lines += "Skills override default system prompt behavior. User instructions in CLAUDE.md"
        $lines += "take precedence over skills. Skills take precedence over default behavior."
    } else {
        $lines += "Skill registry NOT detected at expected paths."
        $lines += "Falling back to plain assistant mode -- skills will not auto-load."
        if ($vaultRoot) {
            $lines += "Expected: $vaultRoot\skills\registry\using-superpowers\SKILL.md"
        } else {
            $lines += "Set PRIMOLABS_VAULT_ROOT env var to enable skill loading."
        }
    }

    $lines += "===== END SUPERPOWERS INIT ====="
    $lines += ""

    Write-Output ($lines -join "`n")
    exit 0

} catch {
    exit 0
}
