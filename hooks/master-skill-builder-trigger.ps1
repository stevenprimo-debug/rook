# master-skill-builder-trigger.ps1
# Events: Stop | PreCompact | SessionEnd
# ---------------------------------------------------------------------------
# Cheap hook (<2s wall time). Decides whether to fire the master-skill-builder
# distillation pipeline based on the trigger event + a fast heuristic check.
# If the heuristic passes, injects a system reminder telling Claude to invoke
# `master-skill-builder` against the current session. The actual distillation
# runs as part of the next Claude turn — this hook does NOT block.
#
# Trigger discrimination: passed via $env:ROOK_SKB_TRIGGER env var, set by the
# INSTALL.ps1 hook spec (one registered instance per event). Falls back to
# inferring from hook-event JSON shape if env var is missing.
#
# Skip-gate heuristics live inside the master-skill-builder SKILL.md (Step 1) —
# this hook does the cheap upstream filter (token-volume, event sanity) and
# delegates the expensive filter (file-edit count, idempotency) to the skill.
# ---------------------------------------------------------------------------

$ErrorActionPreference = 'SilentlyContinue'

function Resolve-VaultRoot {
    param($cwd)
    if ($env:ROOK_VAULT_ROOT -and (Test-Path $env:ROOK_VAULT_ROOT)) {
        return $env:ROOK_VAULT_ROOT
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

function Append-Log {
    param($vaultRoot, $trigger, $sessionId, $action, $reason)
    $logPath = Join-Path $vaultRoot '.claude\skills\_invocation.log'
    $logDir = Split-Path $logPath -Parent
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
    $iso = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
    $line = "$iso | $trigger | $sessionId | $action | $reason"
    Add-Content -Path $logPath -Value $line -Encoding UTF8
}

try {
    $raw = [Console]::In.ReadToEnd()
    $data = $null
    if ($raw) { try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { } }

    # Determine trigger (trim whitespace — cmd `set X=Y && ...` can leak trailing space)
    $trigger = $env:ROOK_SKB_TRIGGER
    if ($trigger) { $trigger = $trigger.Trim() }
    if (-not $trigger) {
        # Infer from event shape
        if ($data -and $data.PSObject.Properties.Name -contains 'event') {
            $trigger = $data.event
        } else {
            $trigger = 'unknown'
        }
    }

    $cwd = ""
    if ($data -and $data.cwd) { $cwd = $data.cwd }
    $vaultRoot = Resolve-VaultRoot -cwd $cwd
    if (-not $vaultRoot) { exit 0 }

    $sessionId = if ($data -and $data.session_id) { $data.session_id } else { 'unknown' }

    # ---- Upstream skip gate (cheap, runs in hook) -------------------------
    # The hook itself does NOT run the distillation. It just decides whether
    # to inject the system reminder that asks Claude to do so.

    # Stop hook: only fire if the turn produced ≥5 tool calls AND ≥3 file edits.
    # Counts come from data.tool_calls / data.file_edits (Claude Code provides
    # these on the Stop event payload). If not present, default to no-fire.
    if ($trigger -eq 'Stop') {
        $toolCalls = 0
        $fileEdits = 0
        if ($data.tool_calls_count) { $toolCalls = [int]$data.tool_calls_count }
        if ($data.file_edits_count) { $fileEdits = [int]$data.file_edits_count }
        # Fallback: count from tool_calls array if present
        if ($toolCalls -eq 0 -and $data.tool_calls) { $toolCalls = @($data.tool_calls).Count }
        if ($fileEdits -eq 0 -and $data.file_edits) { $fileEdits = @($data.file_edits).Count }

        if ($toolCalls -lt 5 -or $fileEdits -lt 3) {
            Append-Log $vaultRoot 'Stop' $sessionId 'no-op' "upstream-gate: tool_calls=$toolCalls file_edits=$fileEdits"
            exit 0
        }
    }

    # PreCompact: always fire (compaction is lossy by definition — capture is cheap insurance)
    # SessionEnd: fire only if session token count ≥100K AND no skill staged this session
    if ($trigger -eq 'SessionEnd') {
        $tokenCount = 0
        if ($data.session_tokens) { $tokenCount = [int]$data.session_tokens }
        if ($tokenCount -lt 100000) {
            Append-Log $vaultRoot 'SessionEnd' $sessionId 'no-op' "upstream-gate: session_tokens=$tokenCount lt 100K"
            exit 0
        }
        # Check if we already staged a skill this session
        $stagingDir = Join-Path $vaultRoot '.claude\skills\_staging'
        if (Test-Path $stagingDir) {
            $existing = Get-ChildItem -Path $stagingDir -Directory -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -notmatch '^_' } |
                Where-Object {
                    $skillFile = Join-Path $_.FullName 'SKILL.md'
                    if (Test-Path $skillFile) {
                        (Get-Content $skillFile -Raw -ErrorAction SilentlyContinue) -match [regex]::Escape("source_session_id: $sessionId") `
                            -or (Get-Content $skillFile -Raw -ErrorAction SilentlyContinue) -match [regex]::Escape("source_session: $sessionId")
                    } else { $false }
                }
            if ($existing -and @($existing).Count -gt 0) {
                Append-Log $vaultRoot 'SessionEnd' $sessionId 'no-op' "upstream-gate: skill already staged this session"
                exit 0
            }
        }
    }

    # ---- Build the system reminder (delegated to next Claude turn) --------
    # Note the trigger so master-skill-builder can pick the right mode (auto-stop |
    # auto-precompact | auto-sessionend) and apply trigger-specific skip thresholds.

    $modeMap = @{
        'Stop'        = 'auto-stop'
        'PreCompact'  = 'auto-precompact'
        'SessionEnd'  = 'auto-sessionend'
    }
    $mode = $modeMap[$trigger]
    if (-not $mode) { $mode = 'manual' }

    $reminder = @"
===== MASTER SKILL BUILDER — $trigger HOOK FIRED =====

Lifecycle event: $trigger
Session: $sessionId
Mode hint: $mode

Invoke the `master-skill-builder` skill against the current session.
Path: .claude/skills/registry/master-skill-builder/SKILL.md

Apply the full pipeline:
  1. Skip-gate check (Step 1 of the skill) — most events should no-op here
  2. If passing, distill via auto-skill-builder + route via rook-skill-creator
  3. Stage to .claude/skills/_staging/<YYYY-MM-DD>-<slug>/SKILL.md (NOT live registry)
  4. Append to .claude/skills/_staging/_pending_promotion.md
  5. Log to .claude/skills/_invocation.log

DO NOT skip the skip gate. DO NOT write to live registry. Pollution > missed capture is the design.

If the skill no-ops, write one log line and return silently. Do not narrate the no-op to the operator.

If the skill stages successfully, return one line to the operator:
  "Skill staged: <slug> — librarian will surface Monday."

===== END MASTER SKILL BUILDER HOOK =====
"@

    Write-Output $reminder
    Append-Log $vaultRoot $trigger $sessionId 'hook-fired' "system-reminder injected, mode=$mode"
    exit 0

} catch {
    # Hook MUST NOT block the session. Silent fail.
    try {
        $vaultRoot = Resolve-VaultRoot -cwd $null
        if ($vaultRoot) {
            Append-Log $vaultRoot 'error' 'unknown' 'error' $_.Exception.Message
        }
    } catch { }
    exit 0
}
