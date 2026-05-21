# context-watch-gate-test.ps1 -- unit test for context-watch-gate
# Synthesizes fake session JSONL files at known token counts, invokes the hook,
# asserts the expected output shape (silent / warning / hard-stop).

$ErrorActionPreference = 'Continue'
$HooksDir  = Split-Path $PSScriptRoot -Parent
$VaultRoot = Split-Path $HooksDir -Parent
$Hook      = Join-Path $HooksDir 'context-watch-gate.ps1'

if (-not (Test-Path $Hook)) {
    Write-Host "[FAIL] context-watch-gate.ps1 not found at $Hook" -ForegroundColor Red
    exit 1
}

$TmpDir = Join-Path $env:TEMP "rook-ctxwatch-test-$([guid]::NewGuid().ToString('N').Substring(0,8))"
New-Item -ItemType Directory -Path $TmpDir -Force | Out-Null

function Make-Transcript {
    param([int]$InputTokens, [int]$CacheRead = 0, [int]$CacheCreate = 0, [string]$Model = 'claude-opus-4-7')
    $path = Join-Path $TmpDir "$([guid]::NewGuid().ToString('N').Substring(0,8)).jsonl"
    $line = @{
        type    = 'assistant'
        message = @{
            model   = $Model
            content = @(@{ type = 'text'; text = 'synthetic test turn' })
            usage   = @{
                input_tokens                  = $InputTokens
                cache_creation_input_tokens   = $CacheCreate
                cache_read_input_tokens       = $CacheRead
                output_tokens                 = 100
            }
        }
    } | ConvertTo-Json -Depth 10 -Compress
    Set-Content -Path $path -Value $line -Encoding UTF8
    return $path
}

function Invoke-HookWith {
    param([string]$Stdin, [int]$TimeoutSec = 10)
    $job = Start-Job -ScriptBlock {
        param($hk, $sin)
        $sin | & powershell -NoProfile -NonInteractive -File $hk 2>&1
    } -ArgumentList $Hook, $Stdin
    $done = Wait-Job -Job $job -Timeout $TimeoutSec
    if (-not $done) {
        Stop-Job -Job $job -Force; Remove-Job -Job $job -Force
        return @{ Out = '<TIMEOUT>'; Exit = -1 }
    }
    $out = Receive-Job -Job $job
    Remove-Job -Job $job -Force
    return @{ Out = ($out -join "`n"); Exit = 0 }
}

# Clear thresholds env so we test defaults
Remove-Item Env:\ROOK_CONTEXT_WARN_PCT       -ErrorAction SilentlyContinue
Remove-Item Env:\ROOK_CONTEXT_HARDSTOP_PCT   -ErrorAction SilentlyContinue
Remove-Item Env:\ROOK_CONTEXT_WATCH_DISABLED -ErrorAction SilentlyContinue
Remove-Item Env:\CLAUDE_MAX_CONTEXT_TOKENS   -ErrorAction SilentlyContinue

$failures = @()

function Assert-Test {
    param([string]$Name, [bool]$Pass, [string]$Detail = '')
    if ($Pass) {
        Write-Host "  [PASS] $Name" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $Name -- $Detail" -ForegroundColor Red
        $script:failures += $Name
    }
}

# ---------- Gate 1: empty stdin -> exit 0 silent
$r = Invoke-HookWith -Stdin ''
Assert-Test 'empty stdin silent' (($r.Out -eq '' -or $r.Out -eq $null)) "got output: $($r.Out)"

# ---------- Gate 2: 50% transcript -> silent
$t50  = Make-Transcript -InputTokens 100000
$pay = @{ cwd = $VaultRoot; transcript_path = $t50 } | ConvertTo-Json -Compress
$r = Invoke-HookWith -Stdin $pay
Assert-Test '50% silent' (($r.Out -eq '' -or $r.Out -eq $null)) "got output: $($r.Out)"

# ---------- Gate 3: 75% transcript -> visible warning, NOT hard-stop
$t75 = Make-Transcript -InputTokens 150000
$pay = @{ cwd = $VaultRoot; transcript_path = $t75 } | ConvertTo-Json -Compress
$r = Invoke-HookWith -Stdin $pay
$is75Warn = ($r.Out -match '\[context-watch\]' -and $r.Out -cnotmatch 'HARD STOP =====')
Assert-Test '75% warning printed' $is75Warn "got: $($r.Out.Substring(0, [Math]::Min(200, $r.Out.Length)))"

# ---------- Gate 4: 90% transcript -> HARD STOP system-reminder
$t90 = Make-Transcript -InputTokens 180000
$pay = @{ cwd = $VaultRoot; transcript_path = $t90 } | ConvertTo-Json -Compress
$r = Invoke-HookWith -Stdin $pay
$is90Stop = ($r.Out -match 'CONTEXT WATCH -- HARD STOP' -and $r.Out -match 'session_handoffs' -and $r.Out -match 'watchgate.md')
Assert-Test '90% hard-stop block' $is90Stop "got: $($r.Out.Substring(0, [Math]::Min(300, $r.Out.Length)))"

# ---------- Gate 5: ROOK_CONTEXT_WATCH_DISABLED=1 silences even at 90%
$env:ROOK_CONTEXT_WATCH_DISABLED = '1'
$r = Invoke-HookWith -Stdin $pay
Assert-Test 'disabled env var silences' (($r.Out -eq '' -or $r.Out -eq $null)) "got: $($r.Out)"
Remove-Item Env:\ROOK_CONTEXT_WATCH_DISABLED -ErrorAction SilentlyContinue

# Cleanup
Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue

Write-Host ''
if ($failures.Count -eq 0) {
    Write-Host 'context-watch-gate: ALL TESTS PASSED' -ForegroundColor Green
    exit 0
} else {
    Write-Host "context-watch-gate: FAILED -- $($failures -join ', ')" -ForegroundColor Red
    exit 1
}
