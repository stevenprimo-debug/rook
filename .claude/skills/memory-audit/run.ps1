# memory-audit/run.ps1
# Active audit of the operator memory system. Writes phone-readable report to out/.
# v1.1 - 2026-05-14 (ASCII-safe, no em-dashes or backticks in strings)

$ErrorActionPreference = 'Stop'
$root = "C:\Users\User\Desktop\PRIMOLABS"
$today = Get-Date -Format 'yyyy-MM-dd'
$now = Get-Date -Format 'yyyy-MM-dd HH:mm'
$reportPath = Join-Path $root "out\$today-memory-audit.md"

$outDir = Split-Path $reportPath -Parent
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

$issuesCritical = New-Object System.Collections.Generic.List[string]
$issuesWarning  = New-Object System.Collections.Generic.List[string]

# CHECK 1 - Index file size vs 24KB load limit
$indexFiles = @(
  "CLAUDE CODE\MEMORY\MEMORY.md",
  "CLAUDE CODE\MEMORY\MEMORY_PROJECTS.md",
  "CLAUDE CODE\MEMORY\MEMORY_DEPTS.md"
)
$check1Lines = New-Object System.Collections.Generic.List[string]
foreach ($rel in $indexFiles) {
  $full = Join-Path $root $rel
  if (Test-Path $full) {
    $size = (Get-Item $full).Length
    $kb = [math]::Round($size / 1024, 1)
    $lineCount = (Get-Content $full | Measure-Object -Line).Lines
    if ($size -gt 24576) {
      $status = "RED OVER LIMIT"
      $issuesCritical.Add(("Index {0} is {1} KB (>24KB load limit)" -f $rel, $kb))
    } elseif ($size -gt 20480) {
      $status = "YELLOW WARNING"
      $issuesWarning.Add(("Index {0} is {1} KB (approaching 24KB)" -f $rel, $kb))
    } else {
      $status = "GREEN OK"
    }
    $check1Lines.Add(("- {0} | {1} | {2} KB / {3} lines" -f $status, $rel, $kb, $lineCount))
  } else {
    $check1Lines.Add(("- MISSING | {0}" -f $rel))
    $issuesWarning.Add(("Index file {0} does not exist" -f $rel))
  }
}

# CHECK 2 - Files without HEAD blocks
$memoryFiles = Get-ChildItem -Path $root -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object {
  $_.FullName -match '\\memory\\' -and
  $_.FullName -notmatch '\\_archive\\' -and
  $_.FullName -notmatch '\\\.claude\\' -and
  $_.FullName -notmatch '\\node_modules\\' -and
  $_.FullName -notmatch '\\graphify-out' -and
  $_.FullName -notmatch '\\Clippings\\' -and
  $_.FullName -notmatch 'CLAUDE_MEMORY\\' -and
  $_.FullName -notmatch 'CLAUDE-CODE-STARTER-KIT' -and
  $_.FullName -notmatch 'jessica-kruebbe-cowork' -and
  $_.FullName -notmatch 'primolabs-os-starter' -and
  $_.Name -ne '_template_memory.md' -and
  $_.Name -notmatch '_log\.md$' -and
  $_.Name -ne 'capture_routing_keywords.md' -and
  $_.Name -ne 'MEMORY.md' -and
  $_.Name -ne 'MEMORY_PROJECTS.md' -and
  $_.Name -ne 'MEMORY_DEPTS.md' -and
  $_.Name -notmatch '^idea_log' -and
  $_.Name -notmatch '^dispatch_log' -and
  $_.Name -notmatch '^archive_log'
}
$withHead = 0
$withoutHead = New-Object System.Collections.Generic.List[string]
foreach ($f in $memoryFiles) {
  $head = Get-Content $f.FullName -TotalCount 40 -ErrorAction SilentlyContinue
  $hasHead = $false
  foreach ($line in $head) { if ($line -match 'For future Claude') { $hasHead = $true; break } }
  if ($hasHead) { $withHead++ }
  else { $withoutHead.Add($f.FullName.Replace($root + '\','')) }
}
$totalAuditable = $memoryFiles.Count
$pct = if ($totalAuditable -gt 0) { [math]::Round(($withHead / $totalAuditable) * 100, 0) } else { 0 }
if ($pct -lt 50) { $issuesCritical.Add(("HEAD coverage is {0}% - most memory files lack pinned HEAD blocks" -f $pct)) }
elseif ($pct -lt 80) { $issuesWarning.Add(("HEAD coverage is {0}% - incomplete" -f $pct)) }

# CHECK 3 - Stale posture files
$staleFiles = New-Object System.Collections.Generic.List[string]
$verifiedFiles = 0
foreach ($f in $memoryFiles) {
  $contentLines = Get-Content $f.FullName -TotalCount 30 -ErrorAction SilentlyContinue
  $content = $contentLines -join "`n"
  if ($content -match 'last_verified:\s*(\d{4}-\d{2}-\d{2})') {
    $verifiedFiles++
    $lastVerified = [DateTime]::ParseExact($matches[1], 'yyyy-MM-dd', $null)
    $staleAfter = 30
    if ($content -match 'stale_after_days:\s*(\d+)') { $staleAfter = [int]$matches[1] }
    $ageDays = ((Get-Date) - $lastVerified).Days
    if ($ageDays -gt $staleAfter) {
      $rel = $f.FullName.Replace($root + '\','')
      $staleFiles.Add(("{0} (age: {1} days, gate: {2})" -f $rel, $ageDays, $staleAfter))
      $issuesWarning.Add(("Stale posture file: {0} ({1} days old, gate {2})" -f $rel, $ageDays, $staleAfter))
    }
  }
}

# CHECK 4 - Folder sizes
$bloat = New-Object System.Collections.Generic.List[psobject]
$topDirs = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue
foreach ($d in $topDirs) {
  try {
    $size = (Get-ChildItem -Path $d.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $size) { $size = 0 }
    $mb = [math]::Round($size / 1MB, 1)
    $bloat.Add([pscustomobject]@{ Name = $d.Name; MB = $mb })
  } catch {}
}
$bloat = $bloat | Sort-Object MB -Descending | Select-Object -First 10

$appJsonPath = Join-Path $root ".obsidian\app.json"
$ignoredPatterns = @()
if (Test-Path $appJsonPath) {
  try {
    $appJsonText = (Get-Content $appJsonPath) -join "`n"
    $appJson = $appJsonText | ConvertFrom-Json
    if ($appJson.userIgnoreFilters) { $ignoredPatterns = $appJson.userIgnoreFilters }
  } catch {}
}

function Test-FolderIgnored($folderName, $patterns) {
  foreach ($pat in $patterns) {
    $clean = $pat.TrimEnd('/').TrimEnd('\')
    $clean = $clean -replace '^\\\\', ''
    if ($folderName -eq $clean) { return $true }
    try { if ($folderName -match $clean) { return $true } } catch {}
  }
  return $false
}
foreach ($b in $bloat) {
  if ($b.MB -gt 500) {
    if (-not (Test-FolderIgnored $b.Name $ignoredPatterns)) {
      $issuesWarning.Add(("Sync-bloat: {0} is {1} MB and not in Obsidian userIgnoreFilters" -f $b.Name, $b.MB))
    }
  }
}

# CHECK 5 - Contradiction map
$concepts = @{
  'PrimoLabs palette' = @('brand_primolabs', 'brand_primolabs_palette_burnt_operator', 'brand_design')
  'PrimoLabs wedge'   = @('positioning_insight_solopreneur_boss', 'positioning_insight_team_works_for_you', 'feedback_no_boss_framing')
  'Trading posture'   = @('trading_rules', 'project_current_trading_posture')
}
$contradictions = New-Object System.Collections.Generic.List[string]
foreach ($concept in $concepts.Keys) {
  $patterns = $concepts[$concept]
  $found = New-Object System.Collections.Generic.List[string]
  foreach ($f in $memoryFiles) {
    foreach ($pattern in $patterns) {
      if ($f.Name -match $pattern) { $found.Add($f.FullName.Replace($root + '\','')); break }
    }
  }
  if ($found.Count -gt 1) {
    $hasMarker = $false
    foreach ($matchedFile in $found) {
      $head = Get-Content (Join-Path $root $matchedFile) -TotalCount 30 -ErrorAction SilentlyContinue
      foreach ($line in $head) {
        if ($line -match 'SUPERSEDED|HISTORICAL|REVERSED|CORRECTED') { $hasMarker = $true; break }
      }
      if ($hasMarker) { break }
    }
    if (-not $hasMarker) {
      $contradictions.Add(("**{0}** - {1} files, no SUPERSEDED markers: {2}" -f $concept, $found.Count, ($found -join ', ')))
      $issuesWarning.Add(("Concept '{0}' spans {1} files with no SUPERSEDED markers - potential silent conflict" -f $concept, $found.Count))
    }
  }
}

# CHECK 6 - Oversized memory files (>15KB = flag for trim/split)
$oversized = New-Object System.Collections.Generic.List[psobject]
foreach ($f in $memoryFiles) {
  $kb = [math]::Round($f.Length / 1024, 1)
  if ($kb -gt 15) {
    $oversized.Add([pscustomobject]@{ Path = $f.FullName.Replace($root + '\',''); KB = $kb })
    $issuesWarning.Add(("Oversized memory file: {0} is {1} KB (budget: 15KB)" -f $f.FullName.Replace($root + '\',''), $kb))
  }
}

# CHECK 7 - Folder file counts (>30 active files per memory folder = consolidation candidate)
$folderCounts = $memoryFiles | Group-Object { $_.Directory.FullName } | Sort-Object Count -Descending
$bloatedFolders = New-Object System.Collections.Generic.List[psobject]
foreach ($g in $folderCounts) {
  if ($g.Count -gt 30 -and $g.Name -notmatch '_archive') {
    $rel = $g.Name.Replace($root + '\','')
    $bloatedFolders.Add([pscustomobject]@{ Folder = $rel; Count = $g.Count })
    $issuesWarning.Add(("Folder {0} has {1} active files (budget: 30) - consolidation candidate" -f $rel, $g.Count))
  }
}

# Composite score
$indexScore = if ($issuesCritical | Where-Object { $_ -match 'Index' }) { 0 } elseif ($issuesWarning | Where-Object { $_ -match 'Index' }) { 1 } else { 2 }
$headScore = if ($pct -lt 50) { 0 } elseif ($pct -lt 80) { 1 } else { 2 }
$staleScore = if ($staleFiles.Count -ge 3) { 0 } elseif ($staleFiles.Count -ge 1) { 1 } else { 2 }
$bloatCount = ($issuesWarning | Where-Object { $_ -match 'Sync-bloat' }).Count
$bloatScore = if ($bloatCount -ge 2) { 0 } elseif ($bloatCount -ge 1) { 1 } else { 2 }
$contradictionScore = if ($contradictions.Count -ge 3) { 0 } elseif ($contradictions.Count -ge 1) { 1 } else { 2 }
$budgetScore = if (($oversized.Count + $bloatedFolders.Count) -ge 5) { 0 } elseif (($oversized.Count + $bloatedFolders.Count) -ge 1) { 1 } else { 2 }
$composite = $indexScore + $headScore + $staleScore + $bloatScore + $contradictionScore + $budgetScore

# Build report
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add(("# Memory Audit - {0}" -f $today))
$lines.Add("")
$lines.Add(("> Generated {0} CT by memory-audit skill (DEPARTMENTS/CEO/skills/memory-audit/run.ps1)." -f $now))
$lines.Add("> Read on phone via Obsidian. Surfaces issues only - no autonomous fixes.")
$lines.Add("")
$lines.Add(("## Composite health: **{0} / 12**" -f $composite))
$lines.Add("")
if ($composite -ge 10) { $lines.Add("GREEN: Healthy. No action needed.") }
elseif ($composite -ge 7) { $lines.Add("YELLOW: Some drift. Review warnings below.") }
else { $lines.Add("RED: Multiple issues. Review critical items first.") }
$lines.Add("")
$lines.Add("| Check | Score | Status |")
$lines.Add("|---|---|---|")
$idxStatus = if ($indexScore -eq 2) { "GREEN" } elseif ($indexScore -eq 1) { "YELLOW" } else { "RED" }
$headStatus = if ($headScore -eq 2) { "GREEN" } elseif ($headScore -eq 1) { "YELLOW" } else { "RED" }
$stStatus = if ($staleScore -eq 2) { ("GREEN 0 stale") } elseif ($staleScore -eq 1) { ("YELLOW {0} stale" -f $staleFiles.Count) } else { ("RED {0} stale" -f $staleFiles.Count) }
$blStatus = if ($bloatScore -eq 2) { "GREEN" } elseif ($bloatScore -eq 1) { "YELLOW" } else { "RED" }
$ctStatus = if ($contradictionScore -eq 2) { "GREEN 0" } elseif ($contradictionScore -eq 1) { ("YELLOW {0}" -f $contradictions.Count) } else { ("RED {0}" -f $contradictions.Count) }
$lines.Add(("| Index size | {0}/2 | {1} |" -f $indexScore, $idxStatus))
$lines.Add(("| HEAD coverage | {0}/2 | {1} ({2}%) |" -f $headScore, $headStatus, $pct))
$lines.Add(("| Stale posture | {0}/2 | {1} |" -f $staleScore, $stStatus))
$lines.Add(("| Sync bloat | {0}/2 | {1} |" -f $bloatScore, $blStatus))
$lines.Add(("| Contradictions | {0}/2 | {1} |" -f $contradictionScore, $ctStatus))
$bgStatus = if ($budgetScore -eq 2) { "GREEN" } elseif ($budgetScore -eq 1) { ("YELLOW {0} over budget" -f ($oversized.Count + $bloatedFolders.Count)) } else { ("RED {0} over budget" -f ($oversized.Count + $bloatedFolders.Count)) }
$lines.Add(("| Budgets (size/count) | {0}/2 | {1} |" -f $budgetScore, $bgStatus))
$lines.Add("")
$lines.Add("---")
$lines.Add("")

if ($issuesCritical.Count -gt 0) {
  $lines.Add("## CRITICAL")
  $lines.Add("")
  foreach ($i in $issuesCritical) { $lines.Add(("- {0}" -f $i)) }
  $lines.Add("")
}

if ($issuesWarning.Count -gt 0) {
  $lines.Add("## WARNINGS")
  $lines.Add("")
  foreach ($i in $issuesWarning) { $lines.Add(("- {0}" -f $i)) }
  $lines.Add("")
}

$lines.Add("---")
$lines.Add("")
$lines.Add("## Check details")
$lines.Add("")
$lines.Add("### 1. Index files vs 24KB load limit")
$lines.Add("")
foreach ($l in $check1Lines) { $lines.Add($l) }
$lines.Add("")

$lines.Add("### 2. HEAD block coverage")
$lines.Add("")
$lines.Add(("**{0} / {1}** auditable memory files have ## For future Claude HEAD blocks (**{2}%**)." -f $withHead, $totalAuditable, $pct))
$lines.Add("")
if ($withoutHead.Count -gt 0 -and $withoutHead.Count -le 20) {
  $lines.Add("**Missing HEAD blocks:**")
  foreach ($f in $withoutHead) { $lines.Add(("- {0}" -f $f)) }
  $lines.Add("")
} elseif ($withoutHead.Count -gt 20) {
  $lines.Add(("**{0} files missing HEAD blocks.** Top 20 by recency:" -f $withoutHead.Count))
  $topMissing = $withoutHead | ForEach-Object {
    $fp = Join-Path $root $_
    [pscustomobject]@{ Path = $_; LastWrite = (Get-Item $fp).LastWriteTime }
  } | Sort-Object LastWrite -Descending | Select-Object -First 20
  foreach ($f in $topMissing) { $lines.Add(("- {0} (last modified {1})" -f $f.Path, $f.LastWrite.ToString('yyyy-MM-dd'))) }
  $lines.Add("")
}

$lines.Add("### 3. Posture file staleness")
$lines.Add("")
$lines.Add(("**{0}** files carry last_verified frontmatter. **{1}** are past their stale-after gate." -f $verifiedFiles, $staleFiles.Count))
$lines.Add("")
if ($staleFiles.Count -gt 0) {
  $lines.Add("**Stale files:**")
  foreach ($f in $staleFiles) { $lines.Add(("- {0}" -f $f)) }
  $lines.Add("")
}
if ($verifiedFiles -eq 0) {
  $lines.Add("WARNING: No files carry last_verified frontmatter yet. Convention not adopted - agents have no way to detect stale state. Add to drift-prone files: posture, brand, positioning, project status.")
  $lines.Add("")
}

$lines.Add("### 4. Folder sizes (top 10)")
$lines.Add("")
$lines.Add("| Folder | Size (MB) | In ignoreFilters? |")
$lines.Add("|---|---|---|")
foreach ($b in $bloat) {
  $ignored = Test-FolderIgnored $b.Name $ignoredPatterns
  if ($ignored) { $marker = "IGNORED" }
  elseif ($b.MB -gt 500) { $marker = "RED NOT IGNORED" }
  else { $marker = "-" }
  $lines.Add(("| {0} | {1} | {2} |" -f $b.Name, $b.MB, $marker))
}
$lines.Add("")

$lines.Add("### 5. Contradiction map")
$lines.Add("")
if ($contradictions.Count -gt 0) {
  foreach ($c in $contradictions) { $lines.Add(("- {0}" -f $c)) }
} else {
  $lines.Add("No contradictions detected in tracked concept clusters.")
}
$lines.Add("")
$lines.Add("**Tracked clusters:** PrimoLabs palette, PrimoLabs wedge, Trading posture. v1 manual definition; v2 will use semantic clustering.")
$lines.Add("")

$lines.Add("### 6. Size budgets (15 KB per memory file)")
$lines.Add("")
if ($oversized.Count -gt 0) {
  $lines.Add(("**{0} files over 15 KB:**" -f $oversized.Count))
  foreach ($o in ($oversized | Sort-Object KB -Descending)) {
    $lines.Add(("- {0} ({1} KB)" -f $o.Path, $o.KB))
  }
} else {
  $lines.Add("All memory files within 15 KB budget.")
}
$lines.Add("")

$lines.Add("### 7. Folder file-count budgets (30 active files per memory folder)")
$lines.Add("")
if ($bloatedFolders.Count -gt 0) {
  $lines.Add(("**{0} folders over 30 active files:**" -f $bloatedFolders.Count))
  foreach ($b in $bloatedFolders) {
    $lines.Add(("- {0} ({1} files) - consolidate or archive" -f $b.Folder, $b.Count))
  }
} else {
  $lines.Add("All folders within 30-file budget.")
}
$lines.Add("")

$lines.Add("**Folder distribution (top 10):**")
$lines.Add("")
$lines.Add("| Folder | Active files |")
$lines.Add("|---|---|")
foreach ($g in ($folderCounts | Select-Object -First 10)) {
  $rel = $g.Name.Replace($root + '\','')
  $lines.Add(("| {0} | {1} |" -f $rel, $g.Count))
}
$lines.Add("")

$lines.Add("---")
$lines.Add("")
$lines.Add("*Run manually: pwsh DEPARTMENTS/CEO/skills/memory-audit/run.ps1*")

$report = $lines -join "`n"
$report | Out-File -FilePath $reportPath -Encoding utf8 -Force

Write-Host ("Memory audit complete. Composite: {0}/12 | Critical: {1} | Warnings: {2}" -f $composite, $issuesCritical.Count, $issuesWarning.Count)
Write-Host ("Report: {0}" -f $reportPath)
