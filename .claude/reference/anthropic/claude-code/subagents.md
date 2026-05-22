---
name: subagents
source: https://code.claude.com/docs/en/sub-agents
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Subagents (Claude Code)

## What it is

Specialized AI assistants for task-specific workflows. Each runs in its own context window with custom system prompt, tools, and permissions. Claude delegates by matching the subagent's `description` field. THIS is the primary mechanism behind ROOK's 20-agent OS.

## Key concepts + config

### Built-in subagents
- **Explore** — Haiku, read-only tools, file/code search. Skips CLAUDE.md and git status
- **Plan** — inherits model, read-only, used during plan mode. Skips CLAUDE.md and git status
- **general-purpose** — all tools, complex multi-step tasks
- **statusline-setup**, **claude-code-guide** — helpers

### Scope precedence (highest → lowest)
1. Managed settings (org-wide)
2. `--agents` CLI flag (session-only)
3. `.claude/agents/` (project)
4. `~/.claude/agents/` (user)
5. Plugin `agents/` directory

Walks up from cwd for project agents. `--add-dir` does NOT add agent search paths. Plugin subfolders form scoped identifiers (`plugin:review:security`).

### File shape
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

### Frontmatter (required: `name`, `description`)
| Field | Notes |
|---|---|
| `name` | lowercase + hyphens; identity (not filename) |
| `description` | when Claude should delegate |
| `tools` | allowlist (inherits all if omitted) |
| `disallowedTools` | denylist (applied first) |
| `model` | `sonnet`, `opus`, `haiku`, full ID, or `inherit` (default) |
| `permissionMode` | `default|acceptEdits|auto|dontAsk|bypassPermissions|plan` |
| `maxTurns` | cap on agentic turns |
| `skills` | preload into context at startup (full content) |
| `mcpServers` | scoped MCP — list of names or inline configs |
| `hooks` | scoped lifecycle hooks |
| `memory` | `user|project|local` — persistent dir |
| `background` | always run as background task |
| `effort` | `low|medium|high|xhigh|max` |
| `isolation` | `worktree` — temporary git worktree |
| `color` | display color |
| `initialPrompt` | auto-submitted as first turn when run as main session |

### Model resolution order
1. `CLAUDE_CODE_SUBAGENT_MODEL` env var
2. Per-invocation `model` parameter
3. Frontmatter `model`
4. Main conversation model

### Tool restrictions
```yaml
tools: Read, Grep, Glob, Bash        # allowlist
disallowedTools: Write, Edit         # denylist
tools: Agent(worker, researcher)     # restrict spawnable agents
```

### Scoped MCP
```yaml
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github   # reference existing
```
Inline servers connect when subagent starts, disconnect when it finishes. Keeps tool descriptions out of main context.

### Permission mode inheritance
- Parent `bypassPermissions` / `acceptEdits` → takes precedence, can't override
- Parent auto mode → inherited; frontmatter `permissionMode` ignored

### Preload skills
```yaml
skills: [api-conventions, error-handling-patterns]
```
Full skill content injected at startup. Cannot preload skills with `disable-model-invocation: true`.

### Persistent memory
```yaml
memory: user      # ~/.claude/agent-memory/<name>/
memory: project   # .claude/agent-memory/<name>/
memory: local     # .claude/agent-memory-local/<name>/
```
When enabled: first 200 lines / 25KB of `MEMORY.md` auto-injected. Read/Write/Edit auto-enabled.

### Hooks in frontmatter
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
```
Stop hooks auto-converted to `SubagentStop` events. `SubagentStart`/`SubagentStop` events fire in main session.

### Invoke explicitly
- Natural language: "Use the test-runner subagent..."
- @-mention: `@"code-reviewer (agent)"` — guarantees
- Session-wide: `claude --agent code-reviewer` or settings `{"agent": "code-reviewer"}`

### Background vs foreground
- Foreground blocks main conversation; prompts passed through
- Background runs concurrently; **auto-denies anything that would prompt**
- Ctrl+B backgrounds running task. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` disables.

### Fork mode (experimental, v2.1.117+)
Set `CLAUDE_CODE_FORK_SUBAGENT=1`. Forks inherit full conversation history, system prompt, tools, model, message log. Replaces general-purpose dispatch. `/fork <directive>` spawns one manually.

### Spawn restriction
Subagents **cannot spawn other subagents**. Nested workflows must use Skills or chained dispatches from main.

### Disable subagents
```json
{"permissions": {"deny": ["Agent(Explore)", "Agent(my-custom-agent)"]}}
```

### Auto-compaction
Subagents support auto-compaction (~95% capacity by default). Override via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`. Logged as `compact_boundary` events in transcripts at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`.

### Best practices
- Focused single-purpose agents
- Detailed `description` (Claude uses for delegation)
- Limit tools for security
- Check project agents into VCS

## ROOK applicability

THIS is the substrate for the 20-agent OS. Every agent in `agents/<name>/SKILL.md` is structurally a subagent file. ROOK's chief-of-staff dispatches via Agent tool with `Agent(subagent_name)`. The `memory` field is what makes compounding-append work. `mcpServers` scoping is the right home for graphify (give it to librarian and deep-researcher only). `isolation: worktree` is the lever for destructive ops without polluting the main checkout.

## Cross-references
- [[skills]] — `context: fork` is the inverse pattern
- [[hooks]] — `SubagentStart`/`SubagentStop` events
- [[../agent-sdk/overview]] — programmatic AgentDefinition
- [[settings]] — `Agent(...)` permission rules
