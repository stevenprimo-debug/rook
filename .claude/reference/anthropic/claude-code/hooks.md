---
name: hooks
source: https://code.claude.com/docs/en/hooks
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Claude Code Hooks

## What it is

Programmable lifecycle hooks that execute at session events, per-turn events, and per-tool events. The mechanism ROOK uses for routing-enforcer and any deterministic behavior the model can't be trusted to follow.

## Key concepts + config

### Event types
- **Session**: `SessionStart`, `Setup`, `SessionEnd`
- **Per-turn**: `UserPromptSubmit`, `UserPromptExpansion`, `Stop`
- **Per-tool**: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`
- **Permission**: `PermissionRequest`, `PermissionDenied`
- **Reactive**: `FileChanged`, `ConfigChange`
- **Worktree**: `WorktreeCreate`, `WorktreeRemove`

### Config shape
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName|OtherTool",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "/path/to/script",
            "args": [],
            "timeout": 600,
            "statusMessage": "Checking...",
            "async": false,
            "asyncRewake": false
          }
        ]
      }
    ]
  }
}
```

**Hook types**: `command`, `http`, `mcp_tool`, `prompt`, `agent`

**Locations**: user/project/local settings, managed policy, plugin `hooks/hooks.json`, skill/agent frontmatter

### Matcher patterns
| Pattern | Eval | Example |
|---|---|---|
| `*` / `""` / omitted | match all | every event |
| Letters/digits/`_`/`\|` | exact/list | `Bash` or `Edit\|Write` |
| Other chars | regex | `^Notebook` or `mcp__.*` |

**MCP tool matching**: `"matcher": "mcp__memory__.*"` or `"matcher": "mcp__.*__write.*"`

### Command hook forms

**Exec form (with args)** — direct spawn, no shell:
```json
{"type": "command", "command": "node",
 "args": ["${CLAUDE_PLUGIN_ROOT}/script.js", "--fix"]}
```

**Shell form (no args)** — passes to `sh -c` / PowerShell, supports pipes/globs:
```json
{"type": "command",
 "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/script.js --fix"}
```

**Async**:
```json
{"async": true, "asyncRewake": true}
```

### HTTP hooks
```json
{
  "type": "http",
  "url": "http://localhost:8080/validate",
  "timeout": 30,
  "headers": {"Authorization": "Bearer $MY_TOKEN"},
  "allowedEnvVars": ["MY_TOKEN"]
}
```

### MCP tool hooks
```json
{
  "type": "mcp_tool",
  "server": "my_server",
  "tool": "security_scan",
  "input": {"file_path": "${tool_input.file_path}"}
}
```

### Exit codes
- **0** → success; stdout parsed for JSON
- **2** → blocking error; stderr shown to user
- **Other** → non-blocking error

### JSON output fields
```json
{
  "continue": true,
  "stopReason": "message",
  "suppressOutput": false,
  "systemMessage": "warning",
  "terminalSequence": "\033]777;notify;Title;Body\007",
  "hookSpecificOutput": {
    "hookEventName": "EventName",
    "additionalContext": "context for Claude"
  }
}
```

### PreToolUse decision control
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny|allow|ask|defer",
    "permissionDecisionReason": "reason"
  }
}
```

### Common input fields
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/dir",
  "permission_mode": "default|plan|auto",
  "hook_event_name": "EventName",
  "agent_id": "subagent-id",
  "agent_type": "agent-name"
}
```

### Environment variables
- `CLAUDE_PROJECT_DIR` — project root
- `CLAUDE_PLUGIN_ROOT` — plugin install dir
- `CLAUDE_PLUGIN_DATA` — plugin persistent data dir
- `CLAUDE_ENV_FILE` — (SessionStart/Setup/CwdChanged/FileChanged) append `export VAR=value`

## ROOK applicability

This is the mechanism behind `routing-enforcer.ps1` — fires on `UserPromptSubmit`, reads `routing-rules.json`, injects each matching dept's `enforce_message`. PreToolUse hooks back the "never silently drop an idea" guarantee. PostToolUse hooks can run sanitization auditors. The `if` field's permission-rule syntax is how ROOK gates destructive operations.

## Cross-references
- [[settings]] — where hooks are configured
- [[slash-commands]] — skills/agents can declare scoped hooks
- [[../agent-sdk/overview]] — programmatic hook orchestration
