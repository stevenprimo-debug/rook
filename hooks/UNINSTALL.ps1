# UNINSTALL.ps1 -- Removes PrimoLabs Stack hooks from ~/.claude/settings.json
# Leaves non-PrimoLabs hooks untouched. Backs up settings.json first.

[CmdletBinding()]
param(
    [string]$ClaudeHome = "$env:USERPROFILE\.claude"
)

$ErrorActionPreference = 'Stop'

function Write-Step($m) { Write-Host "[UNINSTALL] $m" -ForegroundColor Cyan }
function Write-OK($m)   { Write-Host "  OK    $m" -ForegroundColor Green }
function Write-Warn($m) { Write-Host "  WARN  $m" -ForegroundColor Yellow }

$SettingsPath = Join-Path $ClaudeHome 'settings.json'
if (-not (Test-Path $SettingsPath)) {
    Write-Warn "No settings.json at $SettingsPath -- nothing to uninstall."
    exit 0
}

$ourHooks = @(
    'routing-enforcer.ps1',
    'session-prelude.ps1',
    'superpowers-init.ps1',
    'posture-staleness-gate.ps1',
    'librarian-digest.ps1',
    'preference-detector.ps1',
    'context-watch-gate.ps1'
)

$settings = Get-Content -Raw -Path $SettingsPath -Encoding UTF8 | ConvertFrom-Json

# Backup
$backup = "$SettingsPath.primolabs-uninstall-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item -Path $SettingsPath -Destination $backup -Force
Write-OK "Backup: $backup"

function Is-OurHook($cmd) {
    foreach ($n in $ourHooks) {
        if ($cmd -like "*$n*") { return $true }
    }
    return $false
}

if ($settings.hooks) {
    foreach ($eventProp in @($settings.hooks.PSObject.Properties)) {
        $event = $eventProp.Name
        $groups = @($settings.hooks.$event)
        $cleaned = @()
        foreach ($g in $groups) {
            if (-not $g.hooks) { $cleaned += $g; continue }
            $kept = @()
            foreach ($h in $g.hooks) {
                if (-not (Is-OurHook $h.command)) { $kept += $h }
            }
            if ($kept.Count -gt 0) {
                $cleaned += [PSCustomObject]@{ matcher = $g.matcher; hooks = $kept }
            }
        }
        $settings.hooks.$event = $cleaned
    }
}

# Strip env vars too
if ($settings.env) {
    $envVars = @('PRIMOLABS_VAULT_ROOT','PRIMOLABS_HOOKS_DIR','PRIMOLABS_POSTURE_STALE_DAYS')
    foreach ($v in $envVars) {
        if ($settings.env.PSObject.Properties.Name -contains $v) {
            $settings.env.PSObject.Properties.Remove($v)
        }
    }
}

$json = $settings | ConvertTo-Json -Depth 10
Set-Content -Path $SettingsPath -Value $json -Encoding UTF8

# Remove Task Scheduler safety net (shutdown-resilience for librarian)
$TaskName = 'PrimoLabsLibrarianDailySweep'
try {
    Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
    Write-OK "Task Scheduler entry removed: $TaskName"
} catch {
    # task may not exist; silent pass
}

Write-Step "Uninstall complete"
Write-OK "PrimoLabs hooks and env vars removed from $SettingsPath"
Write-OK "Task Scheduler safety net removed"
Write-OK "Other hooks/env preserved"
Write-Host ""
Write-Host "To re-install: pwsh ./hooks/INSTALL.ps1"
exit 0
