# vault-context-injector.ps1
# UserPromptSubmit hook -- DETERMINISTIC vault search on every topic-substantive
# prompt. Greps the agent roster + projects + archive for keyword matches from
# the operator's prompt and injects findings as a system reminder BEFORE the
# agent responds.
#
# Why it exists: the agent's mental model assumes auto-search of vault state
# on every prompt. Without this hook, it doesn't -- it only loads what its
# Step 1 SKILL.md tells it to. This hook guarantees vault context surfaces at
# the harness layer, not depending on agent judgment.
#
# Companion to: session-prelude.ps1 (loads agent identity), routing-enforcer.ps1
# (fires the matched agent's enforce_message).

$ErrorActionPreference = 'SilentlyContinue'

# ---- CONFIGURATION (override via env vars) ----------------------------------
$MaxKeywords     = 5    # top distinctive keywords to grep
$MaxFilesPerKw   = 4    # max files surfaced per keyword
$MaxMatchesTotal = 12   # hard cap across all keywords
$MinPromptWords  = 5    # skip prompts shorter than this
$SnippetChars    = 100  # chars of matched-line context to show
$HardTimeoutSec  = 5    # bail if total grep time exceeds this

# Vault root resolution order (same pattern as session-prelude.ps1):
#   1. $env:PRIMOLABS_VAULT_ROOT
#   2. $PSScriptRoot parent dir (hooks/ lives at vault root)
#   3. data.cwd from stdin (session is inside the vault)
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
        $cur = $cwd
        for ($i = 0; $i -lt 6; $i++) {
            if ((Test-Path (Join-Path $cur 'agents')) -and (Test-Path (Join-Path $cur 'hooks'))) {
                return $cur
            }
            $cur = Split-Path $cur -Parent
            if (-not $cur) { break }
        }
    }
    return $null
}

# Search paths inside the vault root. Order matters -- earlier paths surface
# first when matches tie on recency.
$SearchPaths = @(
    'agents',
    'projects',
    '_archive'
)

# Common English stopwords + conversational filler. Pruned aggressively
# so proper nouns + topic words survive.
$Stopwords = @(
    'a','an','the','is','are','was','were','be','been','being','am',
    'do','does','did','have','has','had','will','would','can','could',
    'should','may','might','must','shall','this','that','these','those',
    'with','from','into','onto','about','what','who','when','where','why',
    'how','and','or','but','if','then','else','you','your','yours','we',
    'our','ours','my','mine','me','i','it','its','them','they','their',
    'just','like','want','need','get','got','go','going','make','made',
    'know','think','really','also','some','any','all','one','two','three',
    'thing','things','stuff','here','there','today','tomorrow','yesterday',
    'now','next','last','for','to','of','in','on','at','as','by','up',
    'down','out','off','over','under','again','more','most','other','than',
    'so','no','not','very','too','only','own','same','such','well','also',
    'maybe','probably','definitely','really','actually','basically','literally',
    'okay','ok','yeah','yes','no','sure','sort','kind'
)

# Opt-out phrases -- if operator writes any of these, skip vault search this turn
$OptOutPatterns = @(
    'skip vault',
    'no search',
    'ignore vault',
    'no context',
    'fresh start',
    'no rag'
)

# ---- READ PROMPT ------------------------------------------------------------
try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    $data = $raw | ConvertFrom-Json
    $prompt = $data.prompt
    if (-not $prompt) { exit 0 }

    # Skip on opt-out
    foreach ($pat in $OptOutPatterns) {
        if ($prompt -match [regex]::Escape($pat)) { exit 0 }
    }

    # Skip on too-short prompts
    $words = $prompt -split '\s+' | Where-Object { $_ }
    if ($words.Count -lt $MinPromptWords) { exit 0 }

    # Resolve vault root
    $cwd = ""
    if ($data.cwd) { $cwd = $data.cwd }
    $vaultRoot = Resolve-VaultRoot -cwd $cwd
    if (-not $vaultRoot) { exit 0 }

    # ---- KEYWORD EXTRACTION -------------------------------------------------
    # Tokenize: alphanumeric word boundaries, drop punctuation
    $tokens = [regex]::Matches($prompt, '\b[A-Za-z][A-Za-z0-9_-]{2,}\b') |
              ForEach-Object { $_.Value }

    # Drop stopwords (case-insensitive), keep originals to preserve casing for proper nouns
    $stopHash = @{}
    foreach ($s in $Stopwords) { $stopHash[$s.ToLower()] = $true }

    $candidates = $tokens | Where-Object { -not $stopHash[$_.ToLower()] }

    if ($candidates.Count -eq 0) { exit 0 }

    # Score single words: proper nouns + longer words rank higher
    $scored = @{}
    for ($i = 0; $i -lt $candidates.Count; $i++) {
        $word = $candidates[$i]
        $key = $word.ToLower()
        $score = $word.Length
        if ($i -gt 0 -and $word -cmatch '^[A-Z]') { $score += 4 }
        if ($word.Length -ge 6) { $score += 2 }
        if (-not $scored.ContainsKey($key)) {
            $scored[$key] = @{ Word = $word; Score = $score; IsBigram = $false }
        } else {
            $scored[$key].Score += $score
        }
    }

    # ALSO extract bigrams (consecutive 2-word phrases).
    # Bigrams are far more topical than single words and surface agent/folder
    # names like "chief of staff", "dispatch log", "weekly sweep".
    # Scored HIGHER than single words because of topical density.
    for ($i = 0; $i -lt $candidates.Count - 1; $i++) {
        $bigram = "$($candidates[$i]) $($candidates[$i+1])"
        $bigramKey = $bigram.ToLower()
        $bigramScore = $candidates[$i].Length + $candidates[$i+1].Length + 8
        if ($candidates[$i] -cmatch '^[A-Z]' -or $candidates[$i+1] -cmatch '^[A-Z]') {
            $bigramScore += 6
        }
        if (-not $scored.ContainsKey($bigramKey)) {
            $scored[$bigramKey] = @{ Word = $bigram; Score = $bigramScore; IsBigram = $true }
        }
    }

    # Top N by score (bigrams will naturally rise to the top due to scoring)
    $topKeywords = $scored.Values |
                   Sort-Object -Property Score -Descending |
                   Select-Object -First $MaxKeywords |
                   ForEach-Object { $_.Word }

    if ($topKeywords.Count -eq 0) { exit 0 }

    # ---- GREP VAULT ---------------------------------------------------------
    $startTime = Get-Date
    $allMatches = @()

    foreach ($kw in $topKeywords) {
        if (((Get-Date) - $startTime).TotalSeconds -gt $HardTimeoutSec) { break }

        foreach ($subPath in $SearchPaths) {
            $fullPath = Join-Path $vaultRoot $subPath
            if (-not (Test-Path $fullPath)) { continue }

            try {
                $hits = Select-String -Path "$fullPath\*.md" -Pattern $kw `
                                      -SimpleMatch -List -ErrorAction SilentlyContinue |
                        Select-Object -First $MaxFilesPerKw

                # Recurse into subdirs (agents/**)
                $subdirs = Get-ChildItem -Path $fullPath -Directory -Recurse -ErrorAction SilentlyContinue |
                           Select-Object -First 50  # cap directory traversal
                foreach ($d in $subdirs) {
                    if (((Get-Date) - $startTime).TotalSeconds -gt $HardTimeoutSec) { break }
                    $subHits = Select-String -Path "$($d.FullName)\*.md" -Pattern $kw `
                                             -SimpleMatch -List -ErrorAction SilentlyContinue |
                               Select-Object -First $MaxFilesPerKw
                    if ($subHits) { $hits = $hits + $subHits }
                }

                foreach ($h in $hits) {
                    $relPath = $h.Path.Replace($vaultRoot + '\', '').Replace('\', '/')
                    $snippet = $h.Line.Trim()
                    if ($snippet.Length -gt $SnippetChars) {
                        $snippet = $snippet.Substring(0, $SnippetChars) + '...'
                    }
                    $allMatches += [PSCustomObject]@{
                        Keyword = $kw
                        Path    = $relPath
                        Line    = $h.LineNumber
                        Snippet = $snippet
                        MTime   = (Get-Item $h.Path -ErrorAction SilentlyContinue).LastWriteTime
                    }
                }
            } catch { continue }
        }
    }

    if ($allMatches.Count -eq 0) { exit 0 }

    # Dedup by Path, keep most-recent file first
    $deduped = $allMatches |
               Sort-Object -Property MTime -Descending |
               Group-Object -Property Path |
               ForEach-Object { $_.Group[0] } |
               Select-Object -First $MaxMatchesTotal

    # ---- INJECT REMINDER ----------------------------------------------------
    $matchLines = $deduped | ForEach-Object {
        "  [$($_.Keyword)] $($_.Path):$($_.Line)  $($_.Snippet)"
    }
    $matchBlock = $matchLines -join "`n"
    $kwList = $topKeywords -join ', '

    $reminder = @"
===== VAULT CONTEXT (auto-injected, deterministic) =====

Keywords searched: $kwList
Matches found across the agent roster + projects + archive:

$matchBlock

USE THIS CONTEXT FIRST. Read the most-relevant matched files BEFORE
responding to the operator's prompt. Do NOT ask the operator to provide
context that is already in the vault. If matches are stale or off-topic,
say so and proceed -- but always check first.

===== END VAULT CONTEXT =====
"@

    Write-Output $reminder
    exit 0

} catch {
    # Never break the operator's prompt because of a hook bug
    exit 0
}
