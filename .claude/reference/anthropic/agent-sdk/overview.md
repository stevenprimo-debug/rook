---
name: overview
source: https://code.claude.com/docs/en/agent-sdk/overview
fetched: 2026-05-22
category: agent-sdk
rook-relevance: high
---

# Agent SDK Overview

## What it is

Library form of Claude Code. Same tools, agent loop, context management — programmable in Python and TypeScript. Build autonomous agents that read files, run commands, search web, edit code. As of June 15 2026, Agent SDK + `claude -p` usage on subscription plans draws from a separate Agent SDK credit.

## Key concepts + config

### Install
```bash
# Python
pip install claude-agent-sdk
# TypeScript (bundles native binary)
npm install @anthropic-ai/claude-agent-sdk
```

### Authentication
```bash
export ANTHROPIC_API_KEY=your-api-key
```
Third-party providers:
- Bedrock: `CLAUDE_CODE_USE_BEDROCK=1`
- AWS Claude Platform: `CLAUDE_CODE_USE_ANTHROPIC_AWS=1` + `ANTHROPIC_AWS_WORKSPACE_ID`
- Vertex: `CLAUDE_CODE_USE_VERTEX=1`
- Azure Foundry: `CLAUDE_CODE_USE_FOUNDRY=1`

Anthropic does not allow third-party developers to offer claude.ai login or rate limits in their products. Use API key auth.

### Minimal example (Python)
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

### Minimal example (TypeScript)
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.ts",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

### Built-in tools
`Read`, `Write`, `Edit`, `Bash`, `Monitor` (watch background script), `Glob`, `Grep`, `WebSearch`, `WebFetch`, `AskUserQuestion`.

### Hooks (callbacks, not commands)
```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

options = ClaudeAgentOptions(
    permission_mode="acceptEdits",
    hooks={"PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]},
)
```
Events: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, etc.

### Subagents (AgentDefinition)
```python
from claude_agent_sdk import AgentDefinition

ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Agent"],  # Agent required
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code reviewer.",
            prompt="Analyze code quality and suggest improvements.",
            tools=["Read", "Glob", "Grep"],
        )
    },
)
```
Subagent messages include `parent_tool_use_id`.

### MCP
```python
mcp_servers={
    "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
}
```

### Sessions
```python
session_id = None
async for message in query(prompt="Read auth module", options=...):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        session_id = message.data["session_id"]

# Resume
async for message in query(prompt="Now find callers", options=ClaudeAgentOptions(resume=session_id)):
    ...
```

### Setting sources
By default loads `.claude/` from cwd and `~/.claude/`. Restrict via `setting_sources` (Python) / `settingSources` (TS). See [[setting-sources]].

### Filesystem-loaded features
- Skills: `.claude/skills/*/SKILL.md`
- Slash commands: `.claude/commands/*.md`
- Memory: `CLAUDE.md` or `.claude/CLAUDE.md`
- Plugins: programmatic via `plugins` option

### vs Client SDK
Client SDK = raw API + you implement tool loop. Agent SDK = built-in tool execution.

### vs Managed Agents
Agent SDK runs in your process, on your filesystem. Managed Agents = hosted REST API on Anthropic infra. Common path: prototype with Agent SDK → move to Managed Agents for production.

### Branding (for partners)
Allowed: "Claude Agent", "Claude", "{YourAgentName} Powered by Claude". Not permitted: "Claude Code", "Claude Code Agent", Claude Code ASCII art.

## ROOK applicability

This is how ROOK could ship as a standalone library/binary instead of requiring users to run `claude` interactively. The hooks-as-callbacks model is cleaner than shell-out hooks for the routing-enforcer pattern. `AgentDefinition` lets ROOK construct agents programmatically — useful for the chief-of-staff dispatching dynamically vs requiring static .md files. Session resume + `parent_tool_use_id` is how to track which agent owns which artifact across long-running ROOK workflows.

## Cross-references
- [[setting-sources]] — restrict filesystem loading
- [[../claude-code/subagents]] — same concept, file-based
- [[../claude-code/hooks]] — same events, shell-based
- [[../guides/tool-use]] — underlying API
