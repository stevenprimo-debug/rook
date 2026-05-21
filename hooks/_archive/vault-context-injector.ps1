# vault-context-injector.ps1
# UserPromptSubmit hook -- DETERMINISTIC vault search on every topic-substantive
# prompt. Greps DEPARTMENTS + Clippings + CLAUDE CODE/MEMORY for keyword matches
# from the user's prompt and injects findings as a system reminder BEFORE the
# agent responds.
#
# Built 2026-05-13 per Pass-8 lock in
# CLAUDE CODE/MEMORY/project_primolabs_run_the_protocol_locked.md
#
# Why it exists: the operator's mental model was that the agent auto-searches vault
# on every prompt. It did NOT until this hook. Now it does -- guaranteed at
# the harness layer, not depending on agent judgment.
#
# Companion to: existing dispatch-guard.ps1, session-prelude.ps1
# Coexists with: obsidian-capture skill (manual capture INTO vault -- different concern)

$ErrorActionPreference = 'SilentlyContinue'

# ---- CONFIG ---------------------------------------------------------------
$VaultRoot   = if ($env:ROOK_VAULT_ROOT) { $env:ROOK_VAULT_ROOT } else { Split-Path (Split-Path $PSScriptRoot -Parent) -Parent }
$SearchPaths = @(
    'DEPARTMENTS',
    'Clippings',
    'CLAUDE CODE\MEMORY'
)
$MaxKeywords     = 5    # top distinctive keywords to grep
$MaxFilesPerKw   = 4    # max files surfaced per keyword
$MaxMatchesTotal = 12   # hard cap across all keywords
$MinPromptWords  = 5    # skip prompts shorter than this
$SnippetChars    = 100  # chars of matched-line context to show
$HardTimeoutSec  = 5    # bail if total grep time exceeds this

# Common English stopwords + the operator-conversation filler. Pruned aggressively
# so we keep proper nouns + topic words.
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
    'fucking','fuck','shit','okay','ok','yeah','yes','no','sure','sort','kind'
)

# Opt-out phrases -- if user writes any of these, skip vault search this turn
$OptOutPatterns = @(
    'skip vault',
    'no search',
    'ignore vault',
    'no context',
    'fresh start',
    'no rag'
)

# out/ trigger phrases -- when ANY of these appear, inject an
# explicit reminder that the deliverable goes to $VAULT_ROOT\out\,
# NOT a dept folder.
$FromClaudeTriggers = @(
    'send this to obsidian',
    'send me this',
    'send it to obsidian',
    'send to obsidian',
    'save this for me',
    'save this to obsidian',
    'i need this on my phone',
    'drop this in my notes',
    'put this in obsidian',
    'give me this in obsidian',
    'send me the outline',
    'send me this outline',
    'send me this rundown',
    'send me the agenda',
    'send me the plan',
    'send me the brief',
    'send me a brief',
    'save this as a note',
    'add this to obsidian',
    'into obsidian',
    'in my notes app',
    'for my notes'
)

# ---- READ PROMPT ----------------------------------------------------------
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

    # ---- out/ TRIGGER DETECTION ----------------------------------
    # If user is asking us to "send" / "save" a doc for Obsidian consumption,
    # inject a hard reminder about the folder convention. Fires BEFORE
    # vault-context grep so the reminder always lands even on short prompts.
    $promptLower = $prompt.ToLower()
    $fromClaudeFired = $false
    foreach ($trig in $FromClaudeTriggers) {
        if ($promptLower -match [regex]::Escape($trig)) {
            $fromClaudeFired = $true
            break
        }
    }
    if ($fromClaudeFired) {
        $today = (Get-Date).ToString('yyyy-MM-dd')
        $fromClaudeReminder = @"
===== out/ TRIGGER DETECTED =====

the operator asked you to send/save a doc for Obsidian consumption.

MANDATORY PATH: $env:VAULT_ROOT\out\${today}-<slug>.md

DO NOT save to:
  - DEPARTMENTS/<any-dept>/assignments/
  - DEPARTMENTS/<any-dept>/memory/
  - CLAUDE CODE/MEMORY/
  - any other location

Dept folders are for WORK ARTIFACTS. `out/` is the operator's READING
INBOX -- agendas, briefs, summaries, outlines, plans, rundowns, prep
docs, pre-meeting notes. Anything he'll open on his phone via Obsidian
Sync to read.

After saving, tell the operator the file is at the `out/` path so he
can find it.

Memory ref: CLAUDE CODE/MEMORY/feedback_from_claude_folder_convention.md

===== END out/ TRIGGER =====
"@
        Write-Output $fromClaudeReminder
    }

    # ---- KEYWORD EXTRACTION -----------------------------------------------
    # Tokenize: alphanumeric word boundaries, drop punctuation
    $tokens = [regex]::Matches($prompt, '\b[A-Za-z][A-Za-z0-9_-]{2,}\b') |
              ForEach-Object { $_.Value }

    # Drop stopwords (case-insensitive), keep originals to preserve casing for proper nouns
    $stopHash = @{}
    foreach ($s in $Stopwords) { $stopHash[$s.ToLower()] = $true }

    $candidates = $tokens | Where-Object { -not $stopHash[$_.ToLower()] }

    if ($candidates.Count -eq 0) { exit 0 }

    # Score single words: proper nouns (capitalized mid-prompt) and longer words rank higher
    $scored = @{}
    for ($i = 0; $i -lt $candidates.Count; $i++) {
        $word = $candidates[$i]
        $key = $word.ToLower()
        $score = $word.Length
        # Boost capitalized proper-noun-likes (not first word, capitalized)
        if ($i -gt 0 -and $word -cmatch '^[A-Z]') { $score += 4 }
        # Boost longer words
        if ($word.Length -ge 6) { $score += 2 }
        # Aggregate (prefer first-seen casing)
        if (-not $scored.ContainsKey($key)) {
            $scored[$key] = @{ Word = $word; Score = $score; IsBigram = $false }
        } else {
            $scored[$key].Score += $score
        }
    }

    # ALSO extract bigrams (consecutive 2-word phrases from candidates).
    # Bigrams are far more topical than single words and surface skill/folder
    # names like "obsidian capture", "rook dashboard", "brief generator".
    # Scored HIGHER than single words because of topical density.
    for ($i = 0; $i -lt $candidates.Count - 1; $i++) {
        $bigram = "$($candidates[$i]) $($candidates[$i+1])"
        $bigramKey = $bigram.ToLower()
        $bigramScore = $candidates[$i].Length + $candidates[$i+1].Length + 8  # base boost
        # Extra boost if either word is capitalized
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

    # ---- GREP VAULT -------------------------------------------------------
    $startTime = Get-Date
    $allMatches = @()

    foreach ($kw in $topKeywords) {
        if (((Get-Date) - $startTime).TotalSeconds -gt $HardTimeoutSec) { break }

        foreach ($subPath in $SearchPaths) {
            $fullPath = Join-Path $VaultRoot $subPath
            if (-not (Test-Path $fullPath)) { continue }

            try {
                $hits = Select-String -Path "$fullPath\*.md" -Pattern $kw `
                                      -SimpleMatch -List -ErrorAction SilentlyContinue |
                        Select-Object -First $MaxFilesPerKw

                # Recurse into subdirs (DEPARTMENTS/**)
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
                    $relPath = $h.Path.Replace($VaultRoot + '\', '').Replace('\', '/')
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

    # ---- INJECT REMINDER --------------------------------------------------
    $matchLines = $deduped | ForEach-Object {
        "  [$($_.Keyword)] $($_.Path):$($_.Line)  $($_.Snippet)"
    }
    $matchBlock = $matchLines -join "`n"

    $kwList = $topKeywords -join ', '

    $reminder = @"
===== VAULT CONTEXT (auto-injected, deterministic) =====

Keywords searched: $kwList
Matches found in DEPARTMENTS + Clippings + CLAUDE CODE/MEMORY:

$matchBlock

USE THIS CONTEXT FIRST. Read the most-relevant matched files BEFORE
responding to the operator's prompt. Do NOT ask the operator to provide context that
is already in the vault. If matches are stale or off-topic, say so and
proceed -- but always check first.

This auto-injection is the realization of Pass-8 architectural lock
(2026-05-13) -- see CLAUDE CODE/MEMORY/project_primolabs_run_the_protocol_locked.md.

===== END VAULT CONTEXT =====
"@

    Write-Output $reminder
    exit 0

} catch {
    # Never break the user's prompt because of a hook bug
    exit 0
}
