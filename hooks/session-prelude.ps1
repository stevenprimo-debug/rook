# session-prelude.ps1
# Event: SessionStart (and optionally UserPromptSubmit for time-sensitive injection)
# Injects critical context Claude must see before composing a response:
#   1. Current local time (light — no hard-stop in ship vault)
#   2. Dept master-skill load gate (cwd-aware)
#   3. Recently modified files in active project dirs (last 24h)
#   4. Protocol checks
#
# Vault root resolution order:
#   1. $env:PRIMOLABS_VAULT_ROOT  <- set by INSTALL
#   2. $PSScriptRoot parent dir   <- hooks/ lives at vault root
#   3. data.cwd from stdin        <- session is inside the vault

$ErrorActionPreference = 'SilentlyContinue'

# === CONFIGURATION (override via env vars) ====================================
# Hard-stop logic removed from ship vault. May return as opt-in cohort feature later.

function Resolve-VaultRoot {
    param($cwd)
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) {
        return $env:PRIMOLABS_VAULT_ROOT
    }
    if ($PSScriptRoot) {
        $parent = Split-Path $PSScriptRoot -Parent
        if ($parent -and (Test-Path $parent)) { return $parent }
    }
    if ($cwd -and (Test-Path $cwd)) {
        # Walk up looking for an 'agents' or 'departments' folder
        $cur = $cwd
        for ($i = 0; $i -lt 6; $i++) {
            if ((Test-Path (Join-Path $cur 'agents')) -or (Test-Path (Join-Path $cur 'departments'))) {
                return $cur
            }
            $cur = Split-Path $cur -Parent
            if (-not $cur) { break }
        }
    }
    return $null
}

try {
    $raw = [Console]::In.ReadToEnd()
    try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { $data = $null }

    $cwd = ""
    if ($data -and $data.cwd) { $cwd = $data.cwd }

    $vaultRoot = Resolve-VaultRoot -cwd $cwd

    $lines = @()
    $lines += ""
    $lines += "===== SESSION PRELUDE (auto-injected) ====="

    # --- DEPT/AGENT MASTER-SKILL LOAD GATE -----------------------------------
    if ($cwd -and $vaultRoot) {
        $relCwd = ""
        if ($cwd.StartsWith($vaultRoot)) {
            $relCwd = $cwd.Substring($vaultRoot.Length).TrimStart('\','/')
        }

        $deptMatch = $null
        $agentMatch = $null
        if ($relCwd -match '^(agents)[\\/]([^\\/]+)') {
            $agentMatch = $Matches[2]
        } elseif ($relCwd -match '^(departments|DEPARTMENTS)[\\/]([^\\/]+)') {
            $deptMatch = $Matches[2]
        }

        if ($agentMatch) {
            $agentDir = Join-Path $vaultRoot "agents\$agentMatch"
            $skillPath = Join-Path $agentDir 'SKILL.md'
            $lines += ""
            $lines += "*** AGENT WORK DETECTED: $agentMatch ***"
            if (Test-Path $skillPath) {
                $rel = $skillPath.Substring($vaultRoot.Length).TrimStart('\','/')
                $lines += "MANDATORY: Load this agent's SKILL.md before any work in this folder."
                $lines += "  Path: $rel"
            } else {
                $lines += "WARNING: No SKILL.md found at $skillPath. Surface this gap."
            }
        } elseif ($deptMatch) {
            $deptDir = Join-Path $vaultRoot "departments\$deptMatch"
            $skillsDir = Join-Path $deptDir 'skills'
            $masterSkill = $null
            if (Test-Path $skillsDir) {
                $lower = $deptMatch.ToLower() -replace ' ','-'
                $candidates = @(
                    (Join-Path $skillsDir "$lower-master\SKILL.md"),
                    (Join-Path $skillsDir "$lower\SKILL.md")
                )
                foreach ($c in $candidates) {
                    if (Test-Path $c) { $masterSkill = $c; break }
                }
                if (-not $masterSkill) {
                    $found = Get-ChildItem -Path $skillsDir -Recurse -Filter 'SKILL.md' -ErrorAction SilentlyContinue |
                        Where-Object { $_.Directory.Name -match 'master' } | Select-Object -First 1
                    if ($found) { $masterSkill = $found.FullName }
                }
            }
            $lines += ""
            $lines += "*** DEPT WORK DETECTED: $deptMatch ***"
            if ($masterSkill) {
                $rel = $masterSkill.Substring($vaultRoot.Length).TrimStart('\','/')
                $lines += "MANDATORY: Read the dept master skill BEFORE any Edit/Write in this dept."
                $lines += "  Path: $rel"
            }
            $brandPath = Join-Path $deptDir 'memory\brand_design.md'
            if (Test-Path $brandPath) {
                $rel = $brandPath.Substring($vaultRoot.Length).TrimStart('\','/')
                $lines += "MANDATORY: Also load brand rules: $rel"
            }
        }
    }

    # --- TIME (light, no hard stop) ------------------------------------------
    $lines += ""
    $lines += "TIME: $(Get-Date -Format 'ddd yyyy-MM-dd h:mm tt')"

    # --- RECENT FILES (last 24h) ---------------------------------------------
    if ($vaultRoot -and (Test-Path $vaultRoot)) {
        $lines += ""
        $lines += "RECENTLY MODIFIED FILES (last 24h, project dirs):"

        $scanRoots = @(
            (Join-Path $vaultRoot 'agents'),
            (Join-Path $vaultRoot 'departments'),
            (Join-Path $vaultRoot 'projects'),
            (Join-Path $vaultRoot 'skills')
        )

        $cutoff = (Get-Date).AddHours(-24)
        $validExt = @('.md', '.html', '.json', '.py', '.ts', '.tsx', '.jsx', '.css', '.ps1', '.sh')
        $skipPatterns = @('\.git\\', 'node_modules\\', 'worktrees\\', '__pycache__\\', '\.pytest_cache\\')

        $recent = @()
        foreach ($r in $scanRoots) {
            if (-not (Test-Path $r)) { continue }
            try {
                $files = Get-ChildItem -Path $r -Recurse -File -Force -ErrorAction SilentlyContinue |
                    Where-Object {
                        $_.LastWriteTime -ge $cutoff -and
                        $validExt -contains $_.Extension
                    } | Select-Object -First 50
                foreach ($f in $files) {
                    $skip = $false
                    foreach ($pat in $skipPatterns) {
                        if ($f.FullName -match $pat) { $skip = $true; break }
                    }
                    if (-not $skip) { $recent += $f }
                }
            } catch { }
        }

        if ($recent.Count -eq 0) {
            $lines += "  (no modifications in last 24h)"
        } else {
            $sorted = $recent | Sort-Object LastWriteTime -Descending | Select-Object -First 15
            foreach ($f in $sorted) {
                $rel = $f.FullName.Substring($vaultRoot.Length).TrimStart('\','/')
                $time = $f.LastWriteTime.ToString("MM-dd HH:mm")
                $lines += "  $time  $rel"
            }
            if ($recent.Count -gt 15) {
                $lines += "  ... ($($recent.Count - 15) more, capped at 15)"
            }
        }
    }

    # --- PROTOCOL CHECKS -----------------------------------------------------
    $lines += ""
    $lines += "PROTOCOL CHECKS BEFORE RESPONDING:"
    $lines += "  1. ADHD One-Thread -- name pivots explicitly before switching."
    $lines += "  2. Anchor on the active product when ambiguous, not the freshest file."
    $lines += "  3. Verify project status BEFORE speaking -- read the recent files above."
    $lines += "  4. Investigate before apologizing -- when told 'this is wrong', diff data first."
    $lines += "  5. Match execution mode -- ship 80% over wait at 100% when live with a client."

    $lines += ""
    $lines += "===== END PRELUDE ====="
    $lines += ""

    $output = $lines -join "`n"

    # SessionStart hooks accept plain stdout; UserPromptSubmit prefers JSON.
    $eventName = if ($data -and $data.hook_event_name) { $data.hook_event_name } else { 'SessionStart' }

    if ($eventName -eq 'UserPromptSubmit') {
        $json = @{
            hookSpecificOutput = @{
                hookEventName     = 'UserPromptSubmit'
                additionalContext = $output
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $json
    } else {
        Write-Output $output
    }
    exit 0

} catch {
    exit 0
}
