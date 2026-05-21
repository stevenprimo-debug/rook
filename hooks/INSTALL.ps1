# INSTALL.ps1 -- PrimoLabs Stack hook installer (Windows)
# ---------------------------------------------------------------------------
# One command. Wires all 6 hooks into ~/.claude/settings.json, sets up env
# vars pointing back at the vault, runs a dry-run on each hook, reports.
#
# Usage:
#   cd PrimoLabs_PoweredByClaude
#   pwsh ./hooks/INSTALL.ps1
#
# Idempotent: running twice doesn't double-wire. Existing non-PrimoLabs hooks
# are preserved. Existing PrimoLabs hooks are updated in place.
#
# Exit codes: 0 = success, 1 = soft failure (some hooks missing/failed), 2 = hard failure (no settings.json access)

[CmdletBinding()]
param(
    [string]$ClaudeHome = "$env:USERPROFILE\.claude",
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Step($msg) { Write-Host "[INSTALL] $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "  OK    $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  WARN  $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "  FAIL  $msg" -ForegroundColor Red }

# ---- RESOLVE PATHS ----------------------------------------------------------
$HooksDir = $PSScriptRoot
$VaultRoot = Split-Path $HooksDir -Parent

Write-Step "Resolving paths"
Write-OK "Hooks dir:  $HooksDir"
Write-OK "Vault root: $VaultRoot"

if (-not (Test-Path $ClaudeHome)) {
    Write-Step "Creating $ClaudeHome"
    New-Item -ItemType Directory -Path $ClaudeHome -Force | Out-Null
}

$SettingsPath = Join-Path $ClaudeHome 'settings.json'

# ---- VERIFY HOOK FILES EXIST ------------------------------------------------
Write-Step "Verifying hook scripts exist"
$RequiredHooks = @(
    'routing-enforcer.ps1',
    'session-prelude.ps1',
    'vault-context-injector.ps1',
    'session-end-detect.ps1',
    'precompact-handoff.ps1',
    'superpowers-init.ps1',
    'posture-staleness-gate.ps1',
    'librarian-digest.ps1',
    'preference-detector.ps1',
    'pretooluse-routing-enforcer.ps1',
    'preamble-resolver.ps1',
    'context-watch-gate.ps1'
)
$missing = @()
foreach ($h in $RequiredHooks) {
    $p = Join-Path $HooksDir $h
    if (Test-Path $p) {
        Write-OK $h
    } else {
        Write-Err "$h NOT FOUND at $p"
        $missing += $h
    }
}
if ($missing.Count -gt 0) {
    Write-Err "Missing $($missing.Count) hook scripts. Aborting."
    exit 1
}

# ---- VERIFY routing-rules.json (used by routing-enforcer) -------------------
$ManifestPath = Join-Path $HooksDir 'routing-rules.json'
if (Test-Path $ManifestPath) {
    Write-OK "routing-rules.json present ($((Get-Item $ManifestPath).Length) bytes)"
} else {
    Write-Warn "routing-rules.json NOT present -- routing-enforcer will silent-pass until manifest exists."
}

# ---- BUILD HOOK COMMANDS ----------------------------------------------------
function Build-HookCmd {
    param([string]$scriptName)
    $abs = Join-Path $HooksDir $scriptName
    return "powershell -NoProfile -NonInteractive -File `"$abs`""
}

# Spawn-detach wrapper: returns immediately, launches the target script as a
# hidden background process that survives the SessionEnd hook return.
# Used for librarian-digest so the 5-10 min sweep runs without blocking
# the customer's session exit.
function Build-BackgroundHookCmd {
    param([string]$scriptName)
    $abs = Join-Path $HooksDir $scriptName
    # PowerShell-escaped inner command: launches $abs hidden, returns immediately
    $inner = "Start-Process powershell -ArgumentList '-NoProfile','-WindowStyle','Hidden','-File','$abs' -WindowStyle Hidden | Out-Null"
    return "powershell -NoProfile -NonInteractive -Command `"$inner`""
}

$cmdRouting              = Build-HookCmd 'routing-enforcer.ps1'
$cmdPreToolUseRouting    = Build-HookCmd 'pretooluse-routing-enforcer.ps1'
$cmdPrelude              = Build-HookCmd 'session-prelude.ps1'
$cmdPreamble             = Build-HookCmd 'preamble-resolver.ps1'
$cmdVaultCtx             = Build-HookCmd 'vault-context-injector.ps1'
$cmdSessionEnd           = Build-HookCmd 'session-end-detect.ps1'
$cmdPreCompact           = Build-HookCmd 'precompact-handoff.ps1'
$cmdSuperpowers          = Build-HookCmd 'superpowers-init.ps1'
$cmdPosture              = Build-HookCmd 'posture-staleness-gate.ps1'
$cmdLibrarianBackground  = Build-BackgroundHookCmd 'librarian-digest.ps1'
$cmdPreference           = Build-HookCmd 'preference-detector.ps1'
$cmdSessionMode          = Build-HookCmd 'session-mode-injector.ps1'
$cmdContextWatch         = Build-HookCmd 'context-watch-gate.ps1'

# ---- LOAD OR CREATE settings.json ------------------------------------------
Write-Step "Reading $SettingsPath"
$settings = $null
if (Test-Path $SettingsPath) {
    try {
        $settings = Get-Content -Raw -Path $SettingsPath -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop
        Write-OK "Existing settings.json loaded"
    } catch {
        Write-Err "settings.json exists but is invalid JSON: $($_.Exception.Message)"
        Write-Err "Refusing to overwrite. Fix the file or remove it and re-run."
        exit 2
    }
} else {
    Write-Warn "No settings.json -- creating fresh"
    $settings = [PSCustomObject]@{}
}

# Helper: ensure property exists as PSObject
function Ensure-Property {
    param($obj, $name, $defaultValue)
    if (-not ($obj.PSObject.Properties.Name -contains $name)) {
        $obj | Add-Member -MemberType NoteProperty -Name $name -Value $defaultValue
    }
}

Ensure-Property $settings 'env'   ([PSCustomObject]@{})
Ensure-Property $settings 'hooks' ([PSCustomObject]@{})

# ---- SET ENV VARS -----------------------------------------------------------
Write-Step "Wiring env vars"
$envBlock = $settings.env

$envDefaults = @{
    PRIMOLABS_VAULT_ROOT          = $VaultRoot
    PRIMOLABS_HOOKS_DIR           = $HooksDir
    PRIMOLABS_POSTURE_STALE_DAYS  = '7'
}

foreach ($k in $envDefaults.Keys) {
    $existing = $envBlock.$k
    if ($k -in @('PRIMOLABS_VAULT_ROOT','PRIMOLABS_HOOKS_DIR')) {
        # Always overwrite path-pointers -- they must match this install
        if ($envBlock.PSObject.Properties.Name -contains $k) {
            $envBlock.$k = $envDefaults[$k]
        } else {
            $envBlock | Add-Member -MemberType NoteProperty -Name $k -Value $envDefaults[$k]
        }
        Write-OK "$k = $($envDefaults[$k])"
    } else {
        # Preserve user-customized values; only set if missing
        if ($envBlock.PSObject.Properties.Name -notcontains $k) {
            $envBlock | Add-Member -MemberType NoteProperty -Name $k -Value $envDefaults[$k]
            Write-OK "$k = $($envDefaults[$k]) (default)"
        } else {
            Write-OK "$k = $existing (preserved)"
        }
    }
}

# ---- WIRE HOOKS -------------------------------------------------------------
Write-Step "Wiring hooks into settings.json"

$hooksBlock = $settings.hooks

# Spec for each event: list of (hook-script-name, command-string, timeout)
$hookSpec = [ordered]@{
    'SessionStart' = @(
        @{ name = 'superpowers-init.ps1';         cmd = $cmdSuperpowers; timeout = 8;  matcher = '' },
        @{ name = 'session-prelude.ps1';          cmd = $cmdPrelude;     timeout = 12; matcher = '' },
        @{ name = 'preamble-resolver.ps1';        cmd = $cmdPreamble;    timeout = 5;  matcher = '' },
        @{ name = 'session-mode-injector.ps1';    cmd = $cmdSessionMode; timeout = 5;  matcher = '' }
    )
    'UserPromptSubmit' = @(
        @{ name = 'routing-enforcer.ps1';        cmd = $cmdRouting;      timeout = 10; matcher = '' },
        @{ name = 'preference-detector.ps1';     cmd = $cmdPreference;   timeout = 8;  matcher = '' },
        @{ name = 'context-watch-gate.ps1';      cmd = $cmdContextWatch; timeout = 8;  matcher = '' },
        @{ name = 'vault-context-injector.ps1';  cmd = $cmdVaultCtx;     timeout = 8;  matcher = '' },
        @{ name = 'session-end-detect.ps1';      cmd = $cmdSessionEnd;   timeout = 5;  matcher = '' }
    )
    'PreCompact' = @(
        @{ name = 'precompact-handoff.ps1';      cmd = $cmdPreCompact;  timeout = 5;  matcher = '' }
    )
    'PreToolUse' = @(
        @{ name = 'posture-staleness-gate.ps1';         cmd = $cmdPosture;          timeout = 6;  matcher = '' },
        @{ name = 'pretooluse-routing-enforcer.ps1';    cmd = $cmdPreToolUseRouting; timeout = 5;  matcher = '' }
    )
    'SessionEnd' = @(
        # Spawn-detached: hook returns in <1s; librarian-digest.ps1 keeps running
        # in background for 5-10 min. Survives session exit but NOT computer shutdown.
        # Computer-shutdown resilience requires the Task Scheduler safety net (see below).
        @{ name = 'librarian-digest.ps1';      cmd = $cmdLibrarianBackground; timeout = 5;  matcher = '' }
    )
}

# Idempotency: remove any existing entries whose command points to one of OUR hooks,
# then re-add. This way running INSTALL twice doesn't double-wire, and we always
# carry the latest command string (in case the install path changed).
$ourHookNames = $RequiredHooks  # filename matching

function Is-OurHook {
    param([string]$commandStr)
    foreach ($n in $ourHookNames) {
        if ($commandStr -like "*$n*") { return $true }
    }
    return $false
}

foreach ($event in $hookSpec.Keys) {
    # Ensure event array exists
    if (-not ($hooksBlock.PSObject.Properties.Name -contains $event)) {
        $hooksBlock | Add-Member -MemberType NoteProperty -Name $event -Value @()
    }

    $eventArray = @($hooksBlock.$event)

    # Strip out matcher groups that consist ENTIRELY of our hooks (we'll re-add)
    # AND strip out any of our hooks living inside mixed-matcher groups.
    $cleaned = @()
    foreach ($grp in $eventArray) {
        if (-not $grp.hooks) { $cleaned += $grp; continue }
        $kept = @()
        foreach ($h in $grp.hooks) {
            if ($h.command -and (Is-OurHook $h.command)) {
                # drop -- we'll re-add
            } else {
                $kept += $h
            }
        }
        if ($kept.Count -gt 0) {
            # rebuild group with surviving hooks
            $newGrp = [PSCustomObject]@{
                matcher = $grp.matcher
                hooks   = $kept
            }
            $cleaned += $newGrp
        }
        # if kept is empty AND the group was all-PrimoLabs, drop the whole group
    }

    # Build our matcher group, append
    $primoHooks = @()
    foreach ($spec in $hookSpec[$event]) {
        $primoHooks += [PSCustomObject]@{
            type    = 'command'
            command = $spec.cmd
            timeout = $spec.timeout
        }
        Write-OK "$event :: $($spec.name)"
    }
    $primoGroup = [PSCustomObject]@{
        matcher = ''
        hooks   = $primoHooks
    }

    $cleaned += $primoGroup
    $hooksBlock.$event = $cleaned
}

# ---- TASK SCHEDULER: shutdown-resilience safety net -------------------------
# Registers a Windows Task Scheduler entry that runs librarian-digest at user
# login (delayed 5 min). If the SessionEnd spawn-detached run got killed by a
# laptop-close / shutdown / crash, this catches it on next boot.
# The task checks for a recent digest before running; if librarian wrote a
# digest in the last 24h, it exits early.
Write-Step "Registering Task Scheduler safety net for librarian"
$TaskName = 'PrimoLabsLibrarianDailySweep'
$LibrarianAbs = Join-Path $HooksDir 'librarian-digest.ps1'

try {
    # Unregister any prior version (idempotent re-install)
    Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue

    # Action: run librarian-digest.ps1 hidden, with PRIMOLABS_LIBRARIAN_BACKUP=1
    # (the script checks this env var + last-digest timestamp to decide whether to run)
    $action = New-ScheduledTaskAction `
        -Execute 'powershell.exe' `
        -Argument "-NoProfile -WindowStyle Hidden -File `"$LibrarianAbs`""

    # Trigger: at user logon, delayed 5 min (let login complete first)
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $trigger.Delay = 'PT5M'

    # Settings: catch-up if missed (computer was off), allow run on battery, stop after 15 min
    $settingsTask = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

    # Register under current user, no elevation needed
    $principal = New-ScheduledTaskPrincipal `
        -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType Interactive `
        -RunLevel Limited

    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description 'PrimoLabs ROOK: catches missed librarian-digest runs after laptop close / shutdown. Runs at user login + 5 min, skips if digest was written in last 24h.' `
        -Action $action `
        -Trigger $trigger `
        -Settings $settingsTask `
        -Principal $principal `
        -Force | Out-Null

    Write-OK "Task Scheduler entry registered: $TaskName (runs at login + 5 min delay)"
} catch {
    Write-Warn "Could not register Task Scheduler entry: $($_.Exception.Message)"
    Write-Warn "Shutdown-resilience disabled. SessionEnd hook still works while computer is on."
}

# ---- WRITE -----------------------------------------------------------------
Write-Step "Writing settings.json"
if ($DryRun) {
    Write-Warn "DryRun: not writing. Would write:"
    $settings | ConvertTo-Json -Depth 10
} else {
    # Backup existing file
    if (Test-Path $SettingsPath) {
        $backup = "$SettingsPath.primolabs-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item -Path $SettingsPath -Destination $backup -Force
        Write-OK "Backup: $backup"
    }

    $json = $settings | ConvertTo-Json -Depth 10
    # ConvertTo-Json renders & etc.; settings.json is happy with literal Unicode.
    # Use WriteAllText with no-BOM UTF-8 encoding so python json.load() doesn't choke on BOM.
    [System.IO.File]::WriteAllText($SettingsPath, $json, [System.Text.UTF8Encoding]::new($false))
    Write-OK "Wrote $SettingsPath"
}

# ---- DRY-RUN TEST EACH HOOK ------------------------------------------------
Write-Step "Dry-run testing hooks"

$TestDir = Join-Path $HooksDir 'test'
if (-not (Test-Path $TestDir)) {
    Write-Warn "test/ folder not found -- skipping dry-run"
} else {
    # Set env vars in this process so the hooks see the right paths
    $env:PRIMOLABS_VAULT_ROOT = $VaultRoot
    $env:PRIMOLABS_HOOKS_DIR  = $HooksDir

    $TestScript = Join-Path $TestDir 'run-all.ps1'
    if (Test-Path $TestScript) {
        try {
            & powershell -NoProfile -NonInteractive -File $TestScript
            $rc = $LASTEXITCODE
            if ($rc -eq 0) {
                Write-OK "All hooks passed dry-run"
            } else {
                Write-Warn "Dry-run exited $rc -- some hooks may have soft-failed"
            }
        } catch {
            Write-Warn "Dry-run threw: $($_.Exception.Message)"
        }
    } else {
        Write-Warn "test/run-all.ps1 missing -- skipping"
    }
}

# ---- FINAL SUMMARY ----------------------------------------------------------
Write-Step "Install complete"
Write-Host ""
Write-Host "  Settings:   $SettingsPath"
Write-Host "  Vault:      $VaultRoot"
Write-Host "  Hooks dir:  $HooksDir"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Start a new Claude Code session (existing sessions need a restart to pick up settings.json changes)."
Write-Host "  2. The first user prompt will trigger SessionStart + UserPromptSubmit hooks. Look for"
Write-Host "     '===== SESSION PRELUDE =====' and '===== SUPERPOWERS INIT =====' in the system reminder."
Write-Host "  3. To disable a specific hook, edit $SettingsPath and remove its entry."
Write-Host "  4. To uninstall, run: pwsh ./hooks/UNINSTALL.ps1"
Write-Host ""

exit 0
