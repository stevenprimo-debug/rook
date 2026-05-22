---
name: setting-sources
source: https://code.claude.com/docs/en/agent-sdk/setting-sources (404 at fetch time — documented inline from agent-sdk/overview)
fetched: 2026-05-22
category: agent-sdk
rook-relevance: medium
---

# Setting Sources

## What it is

The dedicated `/en/agent-sdk/setting-sources` URL returned 404 at fetch time. The behavior is documented in the [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) under "Claude Code features":

> By default the SDK loads these from `.claude/` in your working directory and `~/.claude/`. To restrict which sources load, set `setting_sources` (Python) or `settingSources` (TypeScript) in your options.

Plus the parallel `claude --bare -p` mode which skips all filesystem discovery.

## Key concepts + config

### Default behavior (no `setting_sources` set)
Agent SDK auto-discovers and loads from:
- `.claude/` in working directory (skills, commands, agents, hooks, MCP)
- `~/.claude/` (user-level skills, commands, agents, hooks, MCP)
- `CLAUDE.md` / `.claude/CLAUDE.md` (memory)
- Plugins via `plugins` option

### Restricting sources
```python
from claude_agent_sdk import ClaudeAgentOptions

# Hypothetical — refer to live SDK docs for exact value list
options = ClaudeAgentOptions(
    setting_sources=[],  # disable all filesystem auto-discovery
    # or
    setting_sources=["project"],  # only .claude/ from cwd
)
```

```typescript
const options = {
  settingSources: [],
  // or settingSources: ["project"]
};
```

### Parallel: CLI `--bare` mode
The CLI equivalent is `claude --bare -p`, which:
- Skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, CLAUDE.md
- Only flags you pass explicitly take effect
- Required context flags: `--append-system-prompt`, `--settings <file>`, `--mcp-config <file>`, `--agents <json>`, `--plugin-dir`, `--plugin-url`
- Skips OAuth + keychain reads — auth must be `ANTHROPIC_API_KEY` or `apiKeyHelper`

### Use cases for restricting
- CI/CD where teammate's `~/.claude` hooks shouldn't fire
- Production agents where any local config drift is a regression risk
- Self-contained agent distributions (like ROOK) where the binary ships with bundled config

## ROOK applicability

This matters when ROOK ships as an Agent SDK binary instead of expecting users to run `claude` interactively. Setting `setting_sources=[]` and passing config explicitly via SDK options gives ROOK deterministic behavior — no surprise hooks from a teammate's `~/.claude/`. This is the SDK analog of `claude --bare`, and the recommended pattern for ROOK CI workers (sanitization auditor, second-opinion-verify, librarian sweep).

## Cross-references
- [[overview]] — parent doc with `setting_sources` mentioned
- [[../claude-code/headless]] — CLI `--bare` mode (parallel)
- [[../claude-code/settings]] — what's normally loaded from `.claude/`
