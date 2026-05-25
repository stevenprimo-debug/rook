# hydrate-gate.ps1 -- WebFetch host allowlist gate (fail-closed), PowerShell wrapper.
#
# Usage:
#   powershell -NoProfile -File hooks/lib/hydrate-gate.ps1 -Url <url> [-ServiceHint <hint>]
#   Exit 0 = allowed, 1 = blocked, 2 = malformed input.
#
# Delegates to .claude/connectors/_gate.py. This wrapper only locates the
# repo root + invokes Python.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Url,
    [string]$ServiceHint = ''
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Url)) {
    Write-Error 'usage: hydrate-gate.ps1 -Url <url> [-ServiceHint <hint>]'
    exit 2
}

function Resolve-RepoRoot {
    param([string]$startDir)
    $cur = $startDir
    for ($i = 0; $i -lt 8; $i++) {
        if ((Test-Path (Join-Path $cur '.claude/connectors')) -and (Test-Path (Join-Path $cur 'agents'))) {
            return $cur
        }
        $parent = Split-Path $cur -Parent
        if (-not $parent -or $parent -eq $cur) { return $null }
        $cur = $parent
    }
    return $null
}

$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$repoRoot = Resolve-RepoRoot -startDir $scriptDir

if (-not $repoRoot) {
    Write-Output 'BLOCK reason=repo-root-not-found'
    exit 1
}

$py = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    $found = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($found) { $py = $candidate; break }
}
if (-not $py) {
    Write-Output 'BLOCK reason=python-not-on-path'
    exit 1
}

$gatePath = Join-Path $repoRoot '.claude/connectors/_gate.py'
$args = @($gatePath, $Url)
if ($ServiceHint) { $args += $ServiceHint }

& $py @args
exit $LASTEXITCODE
