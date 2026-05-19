# Register a Windows Task Scheduler job that runs the ingestion pipeline every 3 days at 5:00 PM.
# Schedule history (2026-05-04):
#   - Originally every 15 min — burned ~96 runs/day, hit rate limits, dominant API spend.
#   - Tried daily at 5pm — still too frequent given research enrichment cost per image.
#   - Locked: every 3 days at 5pm — the operator values the research enrichment (invaluable context),
#     so we batch less frequently rather than disabling research. Captures 3 days of Drive
#     uploads per run; ~10x reduction vs daily, ~96x reduction vs original.
# Run this script once from an elevated (Admin) PowerShell prompt to (re-)register.

$TaskName = "COWORK-InboxIngestion"

# Resolve the REAL python.exe (not the WindowsApps launcher stub which opens the Store)
$PythonExe = & python -c "import sys; print(sys.executable)" 2>$null
if (-not $PythonExe -or $PythonExe -like "*WindowsApps*") {
    Write-Error "Could not resolve a real python.exe (got: $PythonExe). Install Python or activate a venv before running this script."
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path  # ...\CORE\inbox_ingestion
$WorkDir = Split-Path -Parent $ScriptDir                       # ...\CORE

$Action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "-m inbox_ingestion" `
    -WorkingDirectory $WorkDir

$Trigger = New-ScheduledTaskTrigger `
    -Daily `
    -DaysInterval 3 `
    -At "12:00PM"

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

# Remove existing registration so this script is idempotent
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue | Out-Null

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "COWORK INBOX: polls Drive every 3 days at noon (laptop reliably on) and processes new images via Claude Vision + research enrichment" `
    -RunLevel Limited

Write-Host ""
Write-Host "Scheduled task '$TaskName' registered."
Write-Host "  Python:    $PythonExe"
Write-Host "  WorkDir:   $WorkDir"
Write-Host "  Schedule:  every 3 days at 12:00 PM"
Write-Host ""
Write-Host "To remove: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
