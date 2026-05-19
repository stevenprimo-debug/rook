# session-stop.ps1
# Fires when a Claude Code session ends.
# Writes a session marker to $VAULT_ROOT\CLAUDE CODE\HANDOFFS\session-YYYY-MM-DD.md

$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = $null }

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$date      = Get-Date -Format "yyyy-MM-dd"
$cwd       = if ($data.cwd)        { $data.cwd }        else { $PWD.Path }
$sessionId = if ($data.session_id) { $data.session_id } else { "unknown" }

$handoffsDir = "$env:VAULT_ROOT\CLAUDE CODE\HANDOFFS"
if (-not (Test-Path $handoffsDir)) {
    New-Item -ItemType Directory -Path $handoffsDir | Out-Null
}

$file = Join-Path $handoffsDir "session-$date.md"

# Create header if new file
if (-not (Test-Path $file)) {
    Set-Content $file "# Session Log - $date`n"
}

# Append session marker
$project = Split-Path $cwd -Leaf
Add-Content $file "- $timestamp | Project: $project | Path: $cwd | ID: $sessionId"
