# routing-enforcer.ps1
# Event: UserPromptSubmit
# Reads hooks/routing-rules.json (sibling to this script), matches the user
# prompt against each dept/agent's keyword set, and injects each matching
# entry's enforce_message into the context. Caps at MaxDeptsToFire so
# the injection doesn't become wall-of-text.
#
# Manifest resolution order (first match wins):
#   1. $env:PRIMOLABS_HOOKS_DIR/routing-rules.json     <- set by INSTALL
#   2. $PSScriptRoot/routing-rules.json                <- sibling to script
#   3. $env:PRIMOLABS_VAULT_ROOT/hooks/routing-rules.json
#
# This script is PORTABLE -- it does NOT hardcode user paths. The INSTALL
# script writes $env:PRIMOLABS_HOOKS_DIR into the settings.json env block.

$ErrorActionPreference = 'SilentlyContinue'

$MaxDeptsToFire = 3
$MinPromptWords = 3

function Resolve-ManifestPath {
    $candidates = @()
    if ($env:PRIMOLABS_HOOKS_DIR) {
        $candidates += (Join-Path $env:PRIMOLABS_HOOKS_DIR 'routing-rules.json')
    }
    if ($PSScriptRoot) {
        $candidates += (Join-Path $PSScriptRoot 'routing-rules.json')
    }
    if ($env:PRIMOLABS_VAULT_ROOT) {
        $candidates += (Join-Path $env:PRIMOLABS_VAULT_ROOT 'hooks\routing-rules.json')
    }
    foreach ($c in $candidates) {
        if ($c -and (Test-Path $c)) { return $c }
    }
    return $null
}

try {
    # ---- READ PROMPT --------------------------------------------------------
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    try {
        $data = $raw | ConvertFrom-Json -ErrorAction Stop
    } catch {
        exit 0
    }
    $prompt = $data.prompt
    if (-not $prompt) { exit 0 }

    $words = $prompt -split '\s+' | Where-Object { $_ }
    if ($words.Count -lt $MinPromptWords) { exit 0 }

    # ---- LOAD MANIFEST ------------------------------------------------------
    $ManifestPath = Resolve-ManifestPath
    if (-not $ManifestPath) { exit 0 }

    try {
        $manifest = Get-Content -Raw -Encoding UTF8 -Path $ManifestPath -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
    } catch {
        exit 0
    }

    # v3 manifest is agent-keyed under "agents"; v2 was "departments".
    # Support both -- try agents first, fall back to departments.
    $entries = $manifest.agents
    if (-not $entries) { $entries = $manifest.departments }
    if (-not $entries) { exit 0 }

    $chains = $manifest.dispatch_chains

    # ---- MATCH KEYWORDS -----------------------------------------------------
    $deptMatches = @{}

    foreach ($prop in $entries.PSObject.Properties) {
        $key = $prop.Name
        $entry = $prop.Value
        $count = 0.0

        if ($entry.primary_keywords) {
            foreach ($kw in $entry.primary_keywords) {
                if (-not $kw) { continue }
                $escaped = [regex]::Escape($kw)
                if ($kw -match '^[A-Za-z0-9]+$') {
                    $pattern = "(?i)\b$escaped\b"
                } else {
                    $pattern = "(?i)$escaped"
                }
                if ($prompt -match $pattern) { $count += 1 }
            }
        }

        if ($entry.secondary_keywords) {
            foreach ($kw in $entry.secondary_keywords) {
                if (-not $kw) { continue }
                $escaped = [regex]::Escape($kw)
                if ($kw -match '^[A-Za-z0-9]+$') {
                    $pattern = "(?i)\b$escaped\b"
                } else {
                    $pattern = "(?i)$escaped"
                }
                if ($prompt -match $pattern) { $count += 0.5 }
            }
        }

        if ($entry.ticker_patterns) {
            if ($entry.ticker_patterns.explicit_ticker) {
                if ($prompt -match $entry.ticker_patterns.explicit_ticker) { $count += 1 }
            }
            if ($entry.ticker_patterns.known_tickers) {
                foreach ($t in $entry.ticker_patterns.known_tickers) {
                    if ($prompt -cmatch "\b$([regex]::Escape($t))\b") { $count += 1 }
                }
            }
        }

        if ($count -gt 0) {
            $deptMatches[$key] = $count
        }
    }

    if ($deptMatches.Count -eq 0) { exit 0 }

    # ---- EXCLUDE DEMOTION ---------------------------------------------------
    foreach ($prop in $entries.PSObject.Properties) {
        $key = $prop.Name
        $entry = $prop.Value
        if (-not $deptMatches.ContainsKey($key)) { continue }
        if (-not $entry.excludes) { continue }
        foreach ($exProp in $entry.excludes.PSObject.Properties) {
            $exPhrase = $exProp.Name
            $escaped = [regex]::Escape($exPhrase)
            if ($prompt -match "(?i)$escaped") {
                $deptMatches[$key] = [Math]::Max(0, $deptMatches[$key] - 2)
            }
        }
    }

    $final = $deptMatches.GetEnumerator() |
        Where-Object { $_.Value -gt 0 } |
        Sort-Object -Property Value -Descending |
        Select-Object -First $MaxDeptsToFire

    if (-not $final -or $final.Count -eq 0) { exit 0 }

    # ---- BUILD REMINDER -----------------------------------------------------
    $sections = @()
    foreach ($e in $final) {
        $key = $e.Key
        $entry = $entries.$key
        $role = $entry.role
        $msg = $entry.enforce_message
        if (-not $msg) { continue }
        $msg = $msg -replace '\\n', "`n"

        $section = "*** $key KEYWORDS DETECTED (role: $role) ***`n$msg"

        if ($chains -and $chains.$key) {
            $chain = $chains.$key
            $upstream = $chain.upstream -join ' -> '
            $reason = $chain.reason
            $section += "`n`nUPSTREAM DISPATCH CHAIN: $upstream -> $key`nReason: $reason"
        }

        $sections += $section
    }

    if ($sections.Count -eq 0) { exit 0 }

    $body = $sections -join "`n`n----`n`n"
    $manifestRel = Split-Path $ManifestPath -Leaf

    $reminder = @"
===== ROUTING ENFORCER (auto-injected) =====

Manifest: $manifestRel (single source of truth -- edit there, not here)

$body

----

GLOBAL RULES (every fire):
  - Main-thread anti-thesis: when an analysis/verdict dept fires, do NOT
    thesis from main thread. Dispatch a subagent. Main thread synthesizes
    the return into a one-line answer.
  - Reversibility gate: irreversible actions (client email, prod change,
    public post, money) require explicit user confirm before DEPLOY.
  - False positive handling: if the work is hook/infrastructure/discussion
    ABOUT the dept (not work IN the dept), mark false positive and proceed.

===== END ROUTING ENFORCER =====
"@

    $output = @{
        hookSpecificOutput = @{
            hookEventName     = 'UserPromptSubmit'
            additionalContext = $reminder
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 0

} catch {
    exit 0
}
