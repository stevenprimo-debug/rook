# precompact-handoff.ps1
# Event: PreCompact
# Fires when Claude Code is about to compact the context window.
# Injects an instruction telling the agent to write a structured session
# summary to a markdown file BEFORE compaction destroys the context.
#
# Architectural choice (vs Mem0): file-based handoff lives in the operator's
# vault. Compounding-append, no cloud dependency, owner: librarian.
#
# Vault root resolution mirrors session-prelude.ps1 / vault-context-injector.ps1.

$ErrorActionPreference = 'SilentlyContinue'

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

try {
    $raw = [Console]::In.ReadToEnd()
    $data = $null
    if ($raw) { try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { } }

    $cwd = ""
    if ($data -and $data.cwd) { $cwd = $data.cwd }
    $vaultRoot = Resolve-VaultRoot -cwd $cwd
    if (-not $vaultRoot) { exit 0 }

    # Build the target handoff path: agents/chief-of-staff/memory/session_handoffs/YYYY-MM-DD-HHMM-precompact.md
    $timestamp = (Get-Date).ToString('yyyy-MM-dd-HHmm')
    $handoffDir = Join-Path $vaultRoot 'agents\chief-of-staff\memory\session_handoffs'
    if (-not (Test-Path $handoffDir)) {
        New-Item -ItemType Directory -Path $handoffDir -Force | Out-Null
    }
    $handoffPath = Join-Path $handoffDir "$timestamp-precompact.md"
    $handoffRelative = "agents/chief-of-staff/memory/session_handoffs/$timestamp-precompact.md"

    $reminder = @"
===== PRECOMPACT HOOK — WRITE HANDOFF BEFORE CONTEXT DROPS =====

Claude Code is about to compact the context window. Anything not written
to a file is going to be lost or summarized away.

MANDATORY (before responding to anything else): write a structured session
handoff to:

    $handoffRelative

Use this shape (compounding-append friendly):

```
---
date: $timestamp
type: handoff
trigger: precompact
---

## Goals locked this session
[1-3 bullets — what was the mission]

## Decisions made
[Each decision with the why, not just the what]

## Files modified
[Path + one-line change description per file]

## Current state
[Where things stand right now — what's done, what's in flight]

## Next steps
[Top 3 actions for the next session to pick up cold]

## Open contradictions / things to surface
[Anything the librarian should flag next sweep, OR nothing.]
```

After writing, continue with whatever the operator asked. The handoff is
the safety net — the librarian's weekly sweep will index it, and the next
session's `session-prelude` will surface it as recent activity.

NEVER skip this. Compaction without a handoff = institutional knowledge
silently lost. This is the exact failure mode the file-based memory
pattern was built to prevent.

===== END PRECOMPACT HOOK =====
"@

    Write-Output $reminder
    exit 0

} catch {
    exit 0
}
