# librarian-weekly-sweep.ps1
# Trigger: Windows Task Scheduler, weekly (default: Sunday 11:00 PM local)
#
# Walks every agent's context/ and memory/, identifies stale files per
# agents/librarian/prune-policy.md, quarantines them to _archive/<YYYY-MM>/pruned/,
# writes librarian-log.md and a Monday digest scaffold.
#
# Complementary to librarian-digest.ps1 (PostToolUse, in-session counter). This
# is the OUT-OF-SESSION cron sweep. The librarian agent reads the scaffold and
# fills in the intelligent analysis (drift narrative, contradictions, hook
# proposals) when the user next opens it.
#
# Install: registered by hooks/INSTALL.ps1 as a scheduled task.
#
# Usage (manual run): pwsh hooks/librarian-weekly-sweep.ps1

[CmdletBinding()]
param(
    [string]$VaultRoot,
    [switch]$DryRun,
    [int]$MaxQuarantinePerSweep = 100
)

$ErrorActionPreference = 'Stop'

# Resolve vault root
if (-not $VaultRoot) {
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) {
        $VaultRoot = $env:PRIMOLABS_VAULT_ROOT
    } elseif ($PSScriptRoot) {
        $VaultRoot = Split-Path $PSScriptRoot -Parent
    } else {
        Write-Host "ERROR: Cannot resolve vault root. Set PRIMOLABS_VAULT_ROOT env var." -ForegroundColor Red
        exit 2
    }
}

if (-not (Test-Path "$VaultRoot/agents")) {
    Write-Host "ERROR: $VaultRoot does not look like a ROOK vault (no agents/ folder)." -ForegroundColor Red
    exit 2
}

# Read prune policy (parse the YAML-ish tuning knobs)
$policyFile = "$VaultRoot/agents/librarian/prune-policy.md"
if (-not (Test-Path $policyFile)) {
    Write-Host "ERROR: prune-policy.md not found at $policyFile" -ForegroundColor Red
    exit 1
}

$policy = Get-Content $policyFile -Raw
$staleDays = 90  # default
$contextHandling = 'keep_recent'
$memoryHandling = 'same'
if ($policy -match 'stale_after_days:\s*(\d+)') { $staleDays = [int]$Matches[1] }
if ($policy -match 'context_handling:\s*(\w+)') { $contextHandling = $Matches[1] }
if ($policy -match 'memory_handling:\s*(\w+)') { $memoryHandling = $Matches[1] }
if ($policy -match 'max_quarantine_per_sweep:\s*(\d+)') { $MaxQuarantinePerSweep = [int]$Matches[1] }

$today = Get-Date
$staleCutoff = $today.AddDays(-$staleDays)
$archiveMonth = $today.ToString('yyyy-MM')
$archiveRoot = "$VaultRoot/_archive/$archiveMonth/pruned"
$logFile = "$VaultRoot/agents/librarian/librarian-log.md"
$digestPath = "$VaultRoot/_FROM_CLAUDE/$(Get-Date -Format 'yyyy-MM-dd')-librarian-digest.md"

if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $archiveRoot | Out-Null
    New-Item -ItemType Directory -Force -Path (Split-Path $digestPath) | Out-Null
}

$candidates = @()
$contractFiles = @('SKILL.md', 'CLAUDE.md', 'README.md')

# Walk agents/*/context/ and agents/*/memory/
$walkRoots = Get-ChildItem "$VaultRoot/agents" -Directory | Where-Object { $_.Name -ne '_template' } | ForEach-Object {
    @("$($_.FullName)/context", "$($_.FullName)/memory")
}

foreach ($walkRoot in $walkRoots) {
    if (-not (Test-Path $walkRoot)) { continue }
    $isMemory = $walkRoot -like '*/memory'
    $effectiveStaleDays = $staleDays
    if ($isMemory -and $memoryHandling -eq 'aggressive') { $effectiveStaleDays = [math]::Floor($staleDays / 2) }
    $effectiveCutoff = $today.AddDays(-$effectiveStaleDays)

    Get-ChildItem $walkRoot -Recurse -File -Filter '*.md' | ForEach-Object {
        $file = $_
        if ($contractFiles -contains $file.Name) { return }

        # Skip recent files (under 14 days old)
        if (($today - $file.CreationTime).TotalDays -lt 14) { return }

        # Skip pinned files
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ($content -match 'pin:\s*true') { return }

        # context_handling: keep_recent → exempt current + last 2 months
        if (-not $isMemory -and $contextHandling -eq 'keep_recent') {
            $monthFolder = Split-Path (Split-Path $file.FullName -Parent) -Leaf
            if ($monthFolder -match '^\d{4}-\d{2}$') {
                $folderDate = [datetime]::ParseExact($monthFolder + '-01', 'yyyy-MM-dd', $null)
                if (($today - $folderDate).TotalDays -lt 90) { return }
            }
        }

        # Staleness check (read timestamp via librarian-log.md is ideal, fallback to LastWriteTime)
        $lastRead = $file.LastWriteTime
        if ($lastRead -gt $effectiveCutoff) { return }

        # Orphan check (no inbound links in vault)
        $slug = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $hasInbound = Select-String -Path "$VaultRoot/agents/*/*.md", "$VaultRoot/agents/*/*/*.md" `
            -Pattern "\[\[$slug\]\]|\($slug\.md\)|\($slug\)" `
            -Quiet -ErrorAction SilentlyContinue
        if ($hasInbound) { return }

        # Near-empty check
        $size = $file.Length
        $reason = "stale $([math]::Floor(($today - $lastRead).TotalDays))d, 0 inbound"
        if ($size -lt 200) { $reason = "near-empty ($size bytes)" }

        $candidates += [PSCustomObject]@{
            FullName = $file.FullName
            Slug     = $slug
            Reason   = $reason
            Relative = $file.FullName.Substring($VaultRoot.Length + 1).Replace('\','/')
        }
    }
}

$quarantined = 0
$flagged = 0
$logEntries = @()
$digestEntries = @()

if ($candidates.Count -gt $MaxQuarantinePerSweep) {
    # Safety brake: flag for manual review instead of auto-quarantining
    $flagged = $candidates.Count
    $digestEntries += "## FLAGGED FOR MANUAL REVIEW (over max_quarantine_per_sweep=$MaxQuarantinePerSweep)"
    $digestEntries += "$($candidates.Count) files flagged; auto-quarantine skipped this sweep. Run `pwsh hooks/librarian-weekly-sweep.ps1 -MaxQuarantinePerSweep <higher>` to override."
    $digestEntries += ''
    foreach ($c in $candidates | Select-Object -First 20) {
        $digestEntries += "- $($c.Relative) — $($c.Reason)"
    }
} else {
    foreach ($c in $candidates) {
        $targetPath = "$archiveRoot/$($c.Slug).md"
        if (-not $DryRun) {
            Move-Item -Path $c.FullName -Destination $targetPath -Force -ErrorAction SilentlyContinue
            # Write tombstone at original path
            "> archived $($today.ToString('yyyy-MM-dd')) → _archive/$archiveMonth/pruned/$($c.Slug).md`n" `
                | Set-Content -Path $c.FullName -Encoding utf8
        }
        $quarantined++
        $logEntries += "$($today.ToString('yyyy-MM-dd')) | quarantined | $($c.Relative) | reason: $($c.Reason) | restore: librarian restore $($c.Slug)"
        $digestEntries += "- $($c.Relative) — $($c.Reason). Restore: ``librarian restore $($c.Slug)``"
    }
}

# Append to librarian-log.md
if ($logEntries.Count -gt 0 -and -not $DryRun) {
    $logEntries | Add-Content -Path $logFile -Encoding utf8
}

# --- Tier 1 vector index rebuild ---
# Walk every agent's SKILL.md, find agents with `tier: 1` in the memory: block,
# rebuild their vector index at agents/<agent>/memory/.vector-index/
$tier1Rebuilt = @()
$tier1Failed = @()

Get-ChildItem "$VaultRoot/agents" -Directory | Where-Object { $_.Name -ne '_template' } | ForEach-Object {
    $agentDir = $_.FullName
    $agentName = $_.Name
    $skillPath = Join-Path $agentDir 'SKILL.md'
    if (-not (Test-Path $skillPath)) { return }

    $skillContent = Get-Content $skillPath -Raw
    # Match tier: 1 inside the memory: YAML block
    if ($skillContent -match '(?s)^memory:.*?  tier:\s*1\b') {
        $indexPath = Join-Path $agentDir 'memory\.vector-index'
        $contextDir = Join-Path $agentDir 'context'
        $memoryDir = Join-Path $agentDir 'memory'

        if (-not $DryRun) {
            try {
                # Clear existing index (rebuild from scratch each sweep)
                if (Test-Path $indexPath) { Remove-Item -Recurse -Force $indexPath -ErrorAction SilentlyContinue }
                New-Item -ItemType Directory -Force -Path $indexPath | Out-Null

                # Invoke graphify on the agent's corpus
                # graphify CLI: walks markdown corpus, builds entity+relation graph, writes JSON index
                $graphifyArgs = @($contextDir, $memoryDir, '--output', $indexPath, '--quiet')
                & graphify @graphifyArgs 2>$null

                # Write index metadata so the agent knows when it was last rebuilt
                @{
                    rebuilt_at    = $today.ToString('yyyy-MM-dd HH:mm:ss')
                    sweep_type    = 'weekly-cron'
                    agent         = $agentName
                    sources       = @($contextDir, $memoryDir)
                } | ConvertTo-Json | Set-Content -Path (Join-Path $indexPath 'index.meta.json') -Encoding utf8

                $tier1Rebuilt += $agentName
            } catch {
                $tier1Failed += "${agentName}: $($_.Exception.Message)"
            }
        } else {
            $tier1Rebuilt += "$agentName (dry-run)"
        }
    }
}

# Append vector-index summary to log
if ($tier1Rebuilt.Count -gt 0 -and -not $DryRun) {
    "$($today.ToString('yyyy-MM-dd')) | vector-index-rebuilt | tier-1 agents: $($tier1Rebuilt -join ', ')" | Add-Content -Path $logFile -Encoding utf8
}
if ($tier1Failed.Count -gt 0 -and -not $DryRun) {
    foreach ($f in $tier1Failed) {
        "$($today.ToString('yyyy-MM-dd')) | vector-index-FAILED | $f" | Add-Content -Path $logFile -Encoding utf8
    }
}

# Write Monday digest scaffold (librarian agent fills in analysis on next dispatch)
$healthNote = if ($flagged -gt 0) { '⚠️ exceeds threshold' } else { 'within threshold' }
$digestContent = @"
---
date: $($today.ToString('yyyy-MM-dd'))
sweep_type: weekly-cron
health: $healthNote
quarantined: $quarantined
flagged_for_review: $flagged
---

# Librarian Weekly Digest — $($today.ToString('yyyy-MM-dd'))

## Sweep Summary

- Walked: $(($walkRoots | Where-Object { Test-Path $_ }).Count) directories
- Quarantined: $quarantined files → ``_archive/$archiveMonth/pruned/``
- Flagged for review: $flagged files

## Quarantines This Sweep

$($digestEntries -join "`n")

## Awaiting Librarian Agent

Open the librarian to:
- Read this scaffold and fill in drift narrative
- Surface contradictions in the vault
- Propose hooks for compounding patterns
- Re-rank quarantines by load-bearing-ness

## Restore Instructions

To restore any quarantined file: ``librarian restore <slug>``
Or manually: move from ``_archive/$archiveMonth/pruned/<slug>.md`` back to its original path.

---

*Generated by ``hooks/librarian-weekly-sweep.ps1``. The librarian agent reads this on next dispatch and fills in the intelligent analysis.*
"@

if (-not $DryRun) {
    $digestContent | Set-Content -Path $digestPath -Encoding utf8
}

Write-Host "weekly sweep complete — $quarantined quarantined, $flagged flagged, digest: $digestPath"
exit 0
