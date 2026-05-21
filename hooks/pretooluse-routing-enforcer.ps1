# pretooluse-routing-enforcer.ps1
# Event: PreToolUse
# Blocks main-thread Edit/Write calls targeting agents/<slug>/** paths.
# Subagent sessions (detected via parent_session_id or ROOK_SUBAGENT=1) are
# ALLOWED to write their own agent files.
#
# Hook context (from Claude Code):
#   tool_name  — name of the tool being called (Edit, Write, etc.)
#   tool_input — JSON string with tool parameters (file_path, etc.)
#   session_id — current session ID
#   parent_session_id — set when running inside a spawned subagent; empty on main thread
#
# Behavior:
#   BLOCK: main-thread Edit/Write to agents/<slug>/** → emit blocking message
#   PASS:  all other tool calls, subagent calls to any path, non-agent paths
#
# Override: if ROOK_SUBAGENT=1 env var is set, always PASS (subagent-origin signal)

$ErrorActionPreference = 'SilentlyContinue'

try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }

    try {
        $data = $raw | ConvertFrom-Json -ErrorAction Stop
    } catch {
        exit 0
    }

    # Only intercept Edit and Write tools
    $toolName = $data.tool_name
    if ($toolName -notin @('Edit', 'Write')) { exit 0 }

    # Extract the target file path
    $toolInput = $data.tool_input
    $targetPath = $null
    if ($toolInput -is [string]) {
        try { $toolInput = $toolInput | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
    }
    if ($toolInput.file_path) { $targetPath = $toolInput.file_path }
    elseif ($toolInput.path)  { $targetPath = $toolInput.path }
    if (-not $targetPath) { exit 0 }

    # Normalize path separators for matching
    $normalizedPath = $targetPath -replace '\\', '/'

    # Check if path matches agents/<slug>/** pattern
    $agentPathPattern = [regex]'^(.*/)?(agents/[^/]+/)'
    if (-not ($normalizedPath -match 'agents/[^/]+/')) { exit 0 }

    # WHITELIST: session_handoffs/ is a system-managed handoff sink (context-watch-gate writes here)
    # Allowed even from main thread — these are produced by hook-driven safety nets, not agent work.
    if ($normalizedPath -match 'agents/[^/]+/memory/session_handoffs/') { exit 0 }

    # Extract agent slug from path
    $agentSlugMatch = [regex]::Match($normalizedPath, 'agents/([^/]+)/')
    $agentSlug = if ($agentSlugMatch.Success) { $agentSlugMatch.Groups[1].Value } else { '<agent>' }

    # Detect subagent origin:
    # 1. ROOK_SUBAGENT=1 env var (explicit subagent signal from brief)
    # 2. parent_session_id field present and non-empty in hook context
    # 3. Hook context has a session_type = 'subagent' (future API field)
    $isSubagent = $false

    if ($env:ROOK_SUBAGENT -eq '1') {
        $isSubagent = $true
    }

    # Check parent_session_id from hook context data
    if (-not $isSubagent) {
        $parentSessionId = $data.parent_session_id
        if ($parentSessionId -and ($parentSessionId.ToString().Trim() -ne '')) {
            $isSubagent = $true
        }
        # Also check session_context if available
        if ($data.session_context -and $data.session_context.parent_session_id) {
            $pid2 = $data.session_context.parent_session_id.ToString().Trim()
            if ($pid2 -ne '') { $isSubagent = $true }
        }
    }

    if ($isSubagent) { exit 0 }

    # BLOCK: main-thread write to agent path
    $blockMsg = @"
[PRETOOLUSE BLOCK] This file is owned by ``$agentSlug``. Main thread cannot Edit/Write it directly.

Dispatch via the Agent tool: spawn a general-purpose subagent with the prompt
"you are $agentSlug, do <task>". The subagent inherits write access to its own files.

To override (if you are CERTAIN this is a legitimate main-thread infra write):
  Set environment variable ROOK_SUBAGENT=1 in your prompt context, or confirm
  that parent_session_id is present in the hook context.

Blocked path: $targetPath
"@

    $output = @{
        hookSpecificOutput = @{
            hookEventName  = 'PreToolUse'
            decision       = 'block'
            reason         = $blockMsg
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 2  # exit 2 = block in Claude Code PreToolUse hooks

} catch {
    exit 0
}
