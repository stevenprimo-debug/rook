# graphify-weekly-rebuild.ps1 -- weekly graphify rebuild (Windows Task Scheduler)
# ---------------------------------------------------------------------------
# Registered by INSTALL.ps1 as a weekly scheduled task.
# Runs `python -m graphify update <vault-root>` on agents/ and .claude/reference/.
# `update` is AST-only re-extraction — no LLM tokens, no API key needed for code changes.
# For full semantic re-extract (LLM-required), operator runs `graphify extract` manually.
#
# Skips silently if:
#   - graphify Python module isn't installed
#   - vault root can't be resolved
#   - Anthropic API key not set AND no graph.json exists yet (nothing to update)
#
# Logs to <vault-root>/agents/librarian/memory/graphify-rebuild.log

$ErrorActionPreference = 'SilentlyContinue'

function Resolve-VaultRoot {
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) {
        return $env:PRIMOLABS_VAULT_ROOT
    }
    if ($PSScriptRoot) {
        $parent = Split-Path $PSScriptRoot -Parent
        if ($parent -and (Test-Path $parent)) { return $parent }
    }
    return $null
}

$VaultRoot = Resolve-VaultRoot
if (-not $VaultRoot) { exit 0 }

$LogFile = Join-Path $VaultRoot 'agents\librarian\memory\graphify-rebuild.log'
$LogDir = Split-Path $LogFile -Parent
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$Now = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

# Check for LLM key (used by full extract, not update — but flag for visibility)
$HasKey = ($env:ANTHROPIC_API_KEY -or $env:GEMINI_API_KEY -or $env:GOOGLE_API_KEY -or $env:OPENAI_API_KEY)

# Confirm python + graphify are present
$pythonOk = $false
try { python -c "import graphify" 2>$null; if ($LASTEXITCODE -eq 0) { $pythonOk = $true } } catch { }
if (-not $pythonOk) {
    "$Now SKIP graphify_module_not_installed" | Out-File -FilePath $LogFile -Append -Encoding utf8
    exit 0
}

$Success = $true
foreach ($target in @('agents', '.claude\reference')) {
    $targetPath = Join-Path $VaultRoot $target
    if (-not (Test-Path $targetPath)) { continue }
    try {
        $output = python -m graphify update $targetPath 2>&1
        if ($LASTEXITCODE -eq 0) {
            "$Now OK update $target" | Out-File -FilePath $LogFile -Append -Encoding utf8
        } else {
            $Success = $false
            "$Now FAIL update $target exit=$LASTEXITCODE" | Out-File -FilePath $LogFile -Append -Encoding utf8
        }
    } catch {
        $Success = $false
        "$Now ERROR update $target msg=$($_.Exception.Message)" | Out-File -FilePath $LogFile -Append -Encoding utf8
    }
}

$keyStatus = if ($HasKey) { 'true' } else { 'false' }
"$Now DONE key_present=$keyStatus success=$Success" | Out-File -FilePath $LogFile -Append -Encoding utf8
exit 0
