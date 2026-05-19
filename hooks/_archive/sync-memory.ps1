# sync-memory.ps1
# Fires after Write or Edit tool use.
# If the file written is a memory file (~/.claude/projects/*/memory/*.md),
# mirrors it to $VAULT_ROOT\CLAUDE CODE\MEMORY\ so it gets Drive-synced and GitHub-backed.

$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { exit 0 }

$filePath = $data.tool_input.file_path
if (-not $filePath) { exit 0 }

$memoryDest = "$env:VAULT_ROOT\CLAUDE CODE\MEMORY"

# Match any file inside a .claude/projects/*/memory/ directory
if ($filePath -match "\.claude\\projects\\[^\\]+\\memory\\(.+)$") {
    $relativePath = $Matches[1]
    $destPath = Join-Path $memoryDest $relativePath

    # Create subdirs if needed
    $destDir = Split-Path $destPath -Parent
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    if (Test-Path $filePath) {
        Copy-Item $filePath $destPath -Force
    }
}
