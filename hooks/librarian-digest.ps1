# librarian-digest.ps1
# Event: PostToolUse (cadence-based)
# Increments a counter in $env:LOCALAPPDATA\PrimoLabs\librarian-counter.txt
# every N tool calls (default 50). When threshold hits, appends a digest
# scan stub to agents/librarian/memory/librarian_digest.md with three
# sections:
#   - Findings:    what shifted in the vault since last digest
#   - Hooks-created (passive, auto-live): non-mutating reminders the agent
#                  can ship without confirm
#   - Hooks-proposed (mutating/blocking, awaiting user Y/N): blocking hooks
#                  that need explicit approval
#
# This is a SCAN STUB -- it doesn't run the librarian agent inline (too slow).
# It writes a "[ ] digest due" line that the librarian agent acts on next time
# it's dispatched. The hook's job is to NOTICE and RECORD the cadence.

$ErrorActionPreference = 'SilentlyContinue'

$Cadence = if ($env:PRIMOLABS_LIBRARIAN_CADENCE) { [int]$env:PRIMOLABS_LIBRARIAN_CADENCE } else { 50 }

function Resolve-VaultRoot {
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) { return $env:PRIMOLABS_VAULT_ROOT }
    if ($PSScriptRoot) {
        $parent = Split-Path $PSScriptRoot -Parent
        if ($parent -and (Test-Path $parent)) { return $parent }
    }
    return $null
}

try {
    $raw = [Console]::In.ReadToEnd()
    # PostToolUse -- stdin is the tool result envelope. We don't need to parse it.

    $vaultRoot = Resolve-VaultRoot
    if (-not $vaultRoot) { exit 0 }

    $stateDir = Join-Path $env:LOCALAPPDATA 'PrimoLabs'
    if (-not (Test-Path $stateDir)) {
        New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
    }

    $counterFile = Join-Path $stateDir 'librarian-counter.txt'
    $count = 0
    if (Test-Path $counterFile) {
        try { $count = [int](Get-Content -Path $counterFile -Raw -ErrorAction Stop).Trim() } catch { $count = 0 }
    }
    $count++

    if ($count -lt $Cadence) {
        Set-Content -Path $counterFile -Value $count -Encoding ASCII -ErrorAction SilentlyContinue
        exit 0
    }

    # Threshold reached -- reset counter, append digest entry
    Set-Content -Path $counterFile -Value 0 -Encoding ASCII -ErrorAction SilentlyContinue

    $digestPath = Join-Path $vaultRoot 'agents\librarian\memory\librarian_digest.md'
    $digestDir = Split-Path $digestPath -Parent
    if (-not (Test-Path $digestDir)) {
        New-Item -ItemType Directory -Path $digestDir -Force | Out-Null
    }

    $stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm')

    # If file doesn't exist, write the HEAD block first
    if (-not (Test-Path $digestPath)) {
        $head = @"
# Librarian Digest

> ## For future Claude (TL;DR)
> Cadence-driven scan log. The librarian-digest.ps1 hook appends a new entry
> every $Cadence tool calls. Each entry is a STUB -- the librarian agent
> processes the stub into Findings / Hooks-created / Hooks-proposed when
> next dispatched. Entries with `[ ] pending` haven't been processed yet.

---

"@
        Set-Content -Path $digestPath -Value $head -Encoding UTF8
    }

    # Recent vault activity for the stub's "scope" hint
    $recentFiles = @()
    try {
        $scanRoots = @(
            (Join-Path $vaultRoot 'agents'),
            (Join-Path $vaultRoot 'departments'),
            (Join-Path $vaultRoot 'skills')
        )
        $cutoff = (Get-Date).AddHours(-2)
        foreach ($r in $scanRoots) {
            if (-not (Test-Path $r)) { continue }
            $files = Get-ChildItem -Path $r -Recurse -File -Force -ErrorAction SilentlyContinue |
                Where-Object { $_.LastWriteTime -ge $cutoff -and $_.Extension -in @('.md','.json','.ps1','.sh') } |
                Select-Object -First 10
            $recentFiles += $files
        }
    } catch { }

    $scopeList = ""
    if ($recentFiles.Count -gt 0) {
        $relList = $recentFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 8 | ForEach-Object {
            "  - " + $_.FullName.Substring($vaultRoot.Length).TrimStart('\','/')
        }
        $scopeList = ($relList -join "`n")
    } else {
        $scopeList = "  - (no recent file changes detected)"
    }

    $entry = @"

## $stamp -- Cadence digest [ ] pending

**Scope hint** (files modified in last 2h):
$scopeList

**Findings:** (librarian agent to fill on next dispatch)
- [ ] TBD -- librarian scans vault state vs Graphify index and notes drift.

**Hooks-created** (passive, auto-live -- librarian may add without confirm):
- [ ] TBD -- non-mutating reminders, additionalContext-only hooks.

**Hooks-proposed** (mutating/blocking, awaiting user Y/N):
- [ ] TBD -- PreToolUse deny gates, PostToolUse mutators, anything that
      blocks or rewrites -- never auto-applied.

---
"@

    Add-Content -Path $digestPath -Value $entry -Encoding UTF8 -ErrorAction SilentlyContinue
    exit 0

} catch {
    exit 0
}
