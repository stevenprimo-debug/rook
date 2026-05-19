# test/run-all.ps1 -- Dry-run each hook with a realistic payload and
# assert it does not throw / does not hang / produces sane output.
#
# Exit 0 if all hooks pass; non-zero if any fail.

$ErrorActionPreference = 'Continue'
$HooksDir = Split-Path $PSScriptRoot -Parent
$VaultRoot = Split-Path $HooksDir -Parent

$env:PRIMOLABS_VAULT_ROOT = $VaultRoot
$env:PRIMOLABS_HOOKS_DIR  = $HooksDir

$failures = @()

function Invoke-Hook {
    param(
        [string]$Name,
        [string]$Script,
        [string]$StdinJson,
        [int]$TimeoutSec = 10
    )
    Write-Host "  [test] $Name" -NoNewline

    $scriptPath = Join-Path $HooksDir $Script
    if (-not (Test-Path $scriptPath)) {
        Write-Host " SKIP (missing)" -ForegroundColor Yellow
        return
    }

    try {
        $job = Start-Job -ScriptBlock {
            param($sp, $stdin)
            $stdin | & powershell -NoProfile -NonInteractive -File $sp 2>&1
        } -ArgumentList $scriptPath, $StdinJson

        $done = Wait-Job -Job $job -Timeout $TimeoutSec
        if (-not $done) {
            Stop-Job -Job $job -Force
            Remove-Job -Job $job -Force
            Write-Host " FAIL (timeout >${TimeoutSec}s)" -ForegroundColor Red
            $script:failures += $Name
            return
        }
        $out = Receive-Job -Job $job
        Remove-Job -Job $job -Force

        # Sanity: hooks should never throw a PowerShell error. They may produce no output.
        if ($out -match 'ParserError|RuntimeException|TerminatingError|CommandNotFoundException') {
            Write-Host " FAIL (error in stdout)" -ForegroundColor Red
            Write-Host "    $out"
            $script:failures += $Name
            return
        }

        Write-Host " OK" -ForegroundColor Green
    } catch {
        Write-Host " FAIL ($($_.Exception.Message))" -ForegroundColor Red
        $script:failures += $Name
    }
}

Write-Host "Running hook dry-run tests..."
Write-Host ""

# 1. routing-enforcer -- feed a prompt that should fire the trading-analyst keywords
$payload1 = @{
    prompt = "what's the SOXL trade setup looking like for tomorrow"
    cwd    = $VaultRoot
} | ConvertTo-Json -Compress
Invoke-Hook 'routing-enforcer.ps1' 'routing-enforcer.ps1' $payload1

# 2. session-prelude -- fire with cwd inside an agent dir
$agentCwd = Join-Path $VaultRoot 'agents\trading-analyst'
$payload2 = @{
    cwd             = $agentCwd
    hook_event_name = 'SessionStart'
} | ConvertTo-Json -Compress
Invoke-Hook 'session-prelude.ps1' 'session-prelude.ps1' $payload2

# 3. superpowers-init
$payload3 = @{ cwd = $VaultRoot } | ConvertTo-Json -Compress
Invoke-Hook 'superpowers-init.ps1' 'superpowers-init.ps1' $payload3

# 4. posture-staleness-gate -- feed a trade-keyword tool call from trading-analyst cwd
$payload4 = @{
    cwd        = $agentCwd
    tool_name  = 'Write'
    tool_input = @{
        file_path = 'memory\trade_plan.md'
        content   = 'long this setup at 21.50 stop 20.80 target 24'
    }
} | ConvertTo-Json -Compress -Depth 5
Invoke-Hook 'posture-staleness-gate.ps1' 'posture-staleness-gate.ps1' $payload4

# 5. librarian-digest -- just fire, counter logic should increment
Invoke-Hook 'librarian-digest.ps1' 'librarian-digest.ps1' '{}'

# 6. preference-detector -- feed a preference statement
$payload6 = @{
    prompt = "from now on always check the time before responding"
} | ConvertTo-Json -Compress
Invoke-Hook 'preference-detector.ps1' 'preference-detector.ps1' $payload6

Write-Host ""
if ($failures.Count -eq 0) {
    Write-Host "ALL HOOKS PASSED" -ForegroundColor Green
    exit 0
} else {
    Write-Host "FAILED: $($failures -join ', ')" -ForegroundColor Red
    exit 1
}
