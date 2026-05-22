# dispatch-budget-watchdog.ps1
# Event: PreToolUse (matcher: Task|Agent)
# Enforces per-agent dispatch budgets: max recursion depth, token ceiling, and
# wall-clock cap. Reads the target agent's SKILL.md frontmatter `budget:` block.
# Maintains lineage state at ~/.claude/.rook-dispatch-lineage (JSON).
#
# Blocks the dispatch when:
#   - current_depth + 1 > max_dispatch_depth
#   - lineage tokens_used > token_budget
#   - lineage wall_clock > time_budget_minutes
#
# Warns (advisory message, does NOT block) when:
#   - tokens_used > 0.8 * token_budget
#
# Fail-open: any internal error -> exit 0 silently. Never breaks a tool call.
# Lineage state is cleared by SessionStart (separate hook clears the file).

$ErrorActionPreference = 'SilentlyContinue'

function FailOpen { exit 0 }

try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { FailOpen }

    try { $data = $raw | ConvertFrom-Json -ErrorAction Stop } catch { FailOpen }

    # SessionStart path: clear lineage state and exit
    $hookEvt = $null
    if ($data.hook_event_name) { $hookEvt = "$($data.hook_event_name)" }
    if ($hookEvt -eq 'SessionStart') {
        $stateDir = Join-Path $env:USERPROFILE ".claude"
        $statePath = Join-Path $stateDir ".rook-dispatch-lineage"
        if (Test-Path $statePath) { Remove-Item -Force -Path $statePath -ErrorAction SilentlyContinue }
        exit 0
    }

    # Only fire on Task / Agent tool calls
    $toolName = $null
    if ($data.tool_name) { $toolName = "$($data.tool_name)" }
    if (-not $toolName) { FailOpen }
    if ($toolName -notmatch '^(Task|Agent)$') { FailOpen }

    # Resolve target agent slug from tool_input
    $targetAgent = $null
    if ($data.tool_input) {
        if ($data.tool_input.subagent_type) { $targetAgent = "$($data.tool_input.subagent_type)" }
        elseif ($data.tool_input.agent)     { $targetAgent = "$($data.tool_input.agent)" }
        elseif ($data.tool_input.name)      { $targetAgent = "$($data.tool_input.name)" }
    }
    if (-not $targetAgent) { FailOpen }

    # Resolve vault root
    $vaultRoot = $null
    if ($env:PRIMOLABS_VAULT_ROOT -and (Test-Path $env:PRIMOLABS_VAULT_ROOT)) {
        $vaultRoot = $env:PRIMOLABS_VAULT_ROOT
    } elseif ($PSScriptRoot) {
        $parent = Split-Path $PSScriptRoot -Parent
        if ($parent -and (Test-Path $parent)) { $vaultRoot = $parent }
    }
    if (-not $vaultRoot) { FailOpen }

    $skillPath = Join-Path $vaultRoot "agents/$targetAgent/SKILL.md"
    if (-not (Test-Path $skillPath)) { FailOpen }

    # Parse frontmatter
    $skillRaw = Get-Content -Path $skillPath -Raw -Encoding UTF8
    if (-not $skillRaw) { FailOpen }
    $skillRaw = $skillRaw.TrimStart([char]0xFEFF)
    if (-not $skillRaw.StartsWith("---")) { FailOpen }
    $afterOpen = $skillRaw.Substring(3)
    $closeIdx = $afterOpen.IndexOf("`n---")
    if ($closeIdx -lt 0) { FailOpen }
    $fmText = $afterOpen.Substring(0, $closeIdx)

    # Crude YAML extract for the budget: block (avoid full YAML dep)
    # Look for lines like:
    #   budget:
    #     time_budget_minutes: 15
    #     token_budget: 100000
    #     max_dispatch_depth: 3
    $timeBudget   = $null
    $tokenBudget  = $null
    $depthBudget  = $null
    $inBudget = $false
    foreach ($line in ($fmText -split "`r?`n")) {
        if ($line -match '^\s*budget\s*:\s*$') { $inBudget = $true; continue }
        if ($inBudget) {
            if ($line -match '^\s{2,}time_budget_minutes\s*:\s*(\d+)') { $timeBudget = [int]$Matches[1]; continue }
            if ($line -match '^\s{2,}token_budget\s*:\s*(\d+)')        { $tokenBudget = [int]$Matches[1]; continue }
            if ($line -match '^\s{2,}max_dispatch_depth\s*:\s*(\d+)')  { $depthBudget = [int]$Matches[1]; continue }
            # If we see a non-indented key, we left the budget block
            if ($line -match '^\S' -and $line.Trim().Length -gt 0) { $inBudget = $false }
        }
    }

    # If no budget block at all, fail-open (don't block agents without budgets)
    if (-not $timeBudget -and -not $tokenBudget -and -not ($depthBudget -ne $null)) {
        FailOpen
    }

    # Lineage state file
    $stateDir = Join-Path $env:USERPROFILE ".claude"
    if (-not (Test-Path $stateDir)) { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null }
    $statePath = Join-Path $stateDir ".rook-dispatch-lineage"

    $state = $null
    if (Test-Path $statePath) {
        try {
            $state = Get-Content -Raw -Path $statePath -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop
        } catch { $state = $null }
    }
    if (-not $state) {
        $state = [PSCustomObject]@{
            depth        = 0
            tokens_used  = 0
            started_at   = (Get-Date).ToString("o")
            last_agent   = ""
        }
    }

    $currentDepth = 0
    if ($state.depth) { $currentDepth = [int]$state.depth }
    $tokensUsed = 0
    if ($state.tokens_used) { $tokensUsed = [int]$state.tokens_used }

    # Roll up tokens_used from the input event if present (Claude Code provides usage on tool boundaries)
    if ($data.usage -and $data.usage.total_tokens) {
        try { $tokensUsed = [int]$data.usage.total_tokens } catch {}
    }

    # Compute wall-clock since lineage start
    $wallMin = 0.0
    try {
        $startedAt = [datetime]::Parse($state.started_at)
        $wallMin = ((Get-Date) - $startedAt).TotalMinutes
    } catch { $wallMin = 0.0 }

    # ---- DEPTH GATE ----
    if ($depthBudget -ne $null -and ($currentDepth + 1) -gt $depthBudget) {
        $msg = @"
===== DISPATCH-BUDGET-WATCHDOG: DEPTH LIMIT =====
dispatch depth limit reached for $targetAgent
current_depth=$currentDepth, would_become=$($currentDepth + 1), max_dispatch_depth=$depthBudget

Per the target agent's SKILL.md budget block, this dispatch would exceed the
recursion ceiling. Block in place -- synthesize from already-collected returns
or return to the operator with a status update. Do NOT spawn another sub-agent.

Lineage state: $statePath
===== END WATCHDOG =====
"@
        $output = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'deny'
                permissionDecisionReason = $msg
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $output
        exit 0
    }

    # ---- TOKEN GATE ----
    if ($tokenBudget -and $tokensUsed -gt $tokenBudget) {
        $msg = @"
===== DISPATCH-BUDGET-WATCHDOG: TOKEN LIMIT =====
token budget exceeded for $targetAgent
tokens_used=$tokensUsed, token_budget=$tokenBudget

Lineage has burned past its token ceiling. Block in place. Synthesize from
collected returns or escalate to the operator. Do NOT spawn another dispatch.

Lineage state: $statePath
===== END WATCHDOG =====
"@
        $output = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'deny'
                permissionDecisionReason = $msg
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $output
        exit 0
    }

    # ---- TIME GATE ----
    if ($timeBudget -and $wallMin -gt [double]$timeBudget) {
        $msg = @"
===== DISPATCH-BUDGET-WATCHDOG: TIME LIMIT =====
wall-clock budget exceeded for $targetAgent
elapsed_minutes=$([math]::Round($wallMin,1)), time_budget_minutes=$timeBudget

Lineage has run past its time ceiling. Block in place. Return current state
to the operator. Do NOT spawn another dispatch.

Lineage state: $statePath
===== END WATCHDOG =====
"@
        $output = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'deny'
                permissionDecisionReason = $msg
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $output
        exit 0
    }

    # ---- WARNING THRESHOLD (advisory only) ----
    if ($tokenBudget -and $tokensUsed -gt ($tokenBudget * 0.8)) {
        $pct = [math]::Round(($tokensUsed / [double]$tokenBudget) * 100, 1)
        $warn = "[dispatch-budget-watchdog] WARN: $targetAgent lineage at $pct% of token budget ($tokensUsed / $tokenBudget). Consider closing out."
        # Advisory: emit to stderr so it surfaces in transcript without blocking
        [Console]::Error.WriteLine($warn)
    }

    # Pass: increment depth and persist
    $state.depth        = $currentDepth + 1
    $state.tokens_used  = $tokensUsed
    $state.last_agent   = $targetAgent
    try {
        $json = $state | ConvertTo-Json -Depth 5 -Compress
        [System.IO.File]::WriteAllText($statePath, $json, [System.Text.UTF8Encoding]::new($false))
    } catch { }

    exit 0

} catch {
    exit 0
}
