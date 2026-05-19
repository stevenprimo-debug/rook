# assignments-stale-check.ps1
# Fires on Stop. Scans DEPARTMENTS/CEO/assignments/ for stale items (>14 days untouched).
# Appends a "STALE ASSIGNMENTS" block to today's handoff log so they cannot silently rot.
# Non-destructive: never deletes or modifies assignments. Just surfaces them.

$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = $null }

$assignDir = "$env:VAULT_ROOT\DEPARTMENTS\CEO\assignments"
$handoffsDir = "$env:VAULT_ROOT\CLAUDE CODE\HANDOFFS"

if (-not (Test-Path $assignDir)) { exit 0 }
if (-not (Test-Path $handoffsDir)) { exit 0 }

$staleThreshold = (Get-Date).AddDays(-14)
$today = Get-Date -Format "yyyy-MM-dd"
$handoffFile = Join-Path $handoffsDir "session-$today.md"

# Find stale assignments
$stale = @()
try {
    $stale = Get-ChildItem -Path $assignDir -File -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -lt $staleThreshold } |
        Sort-Object LastWriteTime
} catch {
    exit 0
}

if ($stale.Count -eq 0) { exit 0 }

# Check if today's handoff already has a STALE ASSIGNMENTS block from a prior Stop in this session
# Avoid duplicate appends within the same day
$alreadyFlagged = $false
if (Test-Path $handoffFile) {
    $content = Get-Content $handoffFile -Raw -ErrorAction SilentlyContinue
    if ($content -match "## STALE ASSIGNMENTS \($today\)") {
        $alreadyFlagged = $true
    }
}
if ($alreadyFlagged) { exit 0 }

# Build the block
$block = @()
$block += ""
$block += "## STALE ASSIGNMENTS ($today)"
$block += ""
$block += "Open in DEPARTMENTS/CEO/assignments/, last touched > 14 days ago. Review or close:"
$block += ""
foreach ($s in $stale) {
    $age = [math]::Round(((Get-Date) - $s.LastWriteTime).TotalDays)
    $block += "- $($s.Name) (last touched $($s.LastWriteTime.ToString('yyyy-MM-dd')), $age days ago)"
}
$block += ""
$block += "*To close: rename to .closed.md, or move to DEPARTMENTS/CEO/assignments/_closed/, or delete if void.*"
$block += ""

# Append (create file if missing)
if (-not (Test-Path $handoffFile)) {
    Set-Content -Path $handoffFile -Value "# Session Log - $today`n" -Encoding UTF8
}
Add-Content -Path $handoffFile -Value ($block -join "`n") -Encoding UTF8

exit 0
