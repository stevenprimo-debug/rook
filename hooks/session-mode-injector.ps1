# session-mode-injector.ps1
# Fires on SessionStart. Surfaces the active ROOK session mode at the top of the session
# so the operator never accidentally writes to shipped paths while in operator-mode.
#
# Reads $env:ROOK_SESSION_MODE. Falls back to .claude/.session_context if env var unset.
# Default mode: customer (fail-safe — operator must opt-in explicitly).

$rookMode = $env:ROOK_SESSION_MODE
if (-not $rookMode) {
    $contextFile = Join-Path $PSScriptRoot "..\.claude\.session_context"
    if (Test-Path $contextFile) {
        $rookMode = (Get-Content $contextFile -Raw -ErrorAction SilentlyContinue).Trim()
    }
}
if (-not $rookMode) { $rookMode = "customer" }

$rookMode = $rookMode.ToLower()
if ($rookMode -ne "operator" -and $rookMode -ne "customer") {
    Write-Output "WARNING: ROOK_SESSION_MODE='$rookMode' is unrecognized. Defaulting to 'customer'."
    $rookMode = "customer"
}

if ($rookMode -eq "operator") {
    Write-Output "===== ROOK SESSION MODE: OPERATOR ====="
    Write-Output "Active mode: OPERATOR (your real-data working vault)"
    Write-Output ""
    Write-Output "Memory writes go to: agents/<agent>/memory/operator/<file>"
    Write-Output "Context writes go to: agents/<agent>/context/operator/<file>"
    Write-Output ""
    Write-Output "These paths are EXCLUDED from package-for-cohort.py."
    Write-Output "Your accumulated personal/client data NEVER ships to customers."
    Write-Output "See .claude/session-modes.md for full convention."
    Write-Output "===== END SESSION MODE BLOCK ====="
} else {
    Write-Output "===== ROOK SESSION MODE: CUSTOMER ====="
    Write-Output "Active mode: CUSTOMER (default — operator did not set ROOK_SESSION_MODE)"
    Write-Output ""
    Write-Output "Memory writes go to: agents/<agent>/memory/<file> (shipped paths)"
    Write-Output ""
    Write-Output "If you ARE the operator (this is your build vault, not a customer install),"
    Write-Output "set in PowerShell profile: \$env:ROOK_SESSION_MODE = 'operator'"
    Write-Output "===== END SESSION MODE BLOCK ====="
}

exit 0
