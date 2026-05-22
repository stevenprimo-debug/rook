---
name: settings
source: https://code.claude.com/docs/en/settings
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Claude Code Settings

## What it is

Configuration system for Claude Code — controls permissions, hooks, model, output style, MCP servers, skills, sandboxing. Four scopes with precedence ordering.

## Key concepts + config

### Scope precedence (highest to lowest)
1. **Managed** — `managed-settings.json` (MDM/system)
2. **Command line args** — temporary session overrides
3. **Local** — `.claude/settings.local.json` (gitignored)
4. **Project** — `.claude/settings.json` (committed, team-shared)
5. **User** — `~/.claude/settings.json` (personal, all projects)

### File locations
| Feature | User | Project | Local |
|---|---|---|---|
| Settings | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| MCP | `~/.claude.json` | `.mcp.json` | `~/.claude.json` |
| Agents | `~/.claude/agents/` | `.claude/agents/` | — |

Windows: `~/.claude` → `%USERPROFILE%\.claude`

### Core settings shape
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run lint)", "Read(~/.zshrc)"],
    "deny": ["Bash(curl *)", "Read(./.env)", "Read(./.env.*)"],
    "defaultMode": "acceptEdits"
  },
  "env": {"CLAUDE_CODE_ENABLE_TELEMETRY": "1"},
  "model": "claude-sonnet-4-6",
  "outputStyle": "Explanatory"
}
```

### Key settings keys
- **Model**: `model`, `effortLevel` (`low|medium|high|xhigh`), `alwaysThinkingEnabled`, `outputStyle`
- **Permissions**: `permissions.allow|ask|deny`, `permissions.defaultMode` (`default|acceptEdits|plan|auto|dontAsk|bypassPermissions`), `permissions.additionalDirectories`
- **Sandbox**: `sandbox.enabled`, `sandbox.filesystem.allowWrite|denyWrite|denyRead`, `sandbox.network.allowedDomains|deniedDomains`
- **Env/tools**: `env`, `defaultShell` (`bash|powershell`), `apiKeyHelper`, `otelHeadersHelper`
- **UI**: `editorMode` (`normal|vim`), `tui` (`default|fullscreen`), `spinnerTipsEnabled`, `showTurnDuration`, `language`
- **Auto Mode**: `autoMode: {environment, allow, soft_deny, hard_deny}`, `disableAutoMode`
- **MCP**: `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `allowedMcpServers`, `deniedMcpServers`
- **Skills**: `skillOverrides` (`on|name-only|user-invocable-only|off`), `skillListingBudgetFraction` (default 0.01)
- **Git**: `attribution: {commit, pr}`, `includeGitInstructions`
- **Worktrees**: `worktree.baseRef` (`fresh|head`), `worktree.symlinkDirectories`, `worktree.sparsePaths`, `worktree.bgIsolation`

### Hot-reload
Most settings reload on file change. Restart required for `model`, `outputStyle`. `ConfigChange` hook fires on detected changes.

### Managed settings (enterprise)
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`
- Windows: `C:\Program Files\ClaudeCode\managed-settings.json`
- Drop-in fragments: `managed-settings.d/*.json` (merged alphabetically)

### Best practices
- Project scope = team-shared permissions/hooks
- Local scope = test before committing
- `$schema` enables IDE autocomplete
- Permission rules merge across scopes; **deny always wins**
- Arrays merge (don't replace) in sandbox/network

## ROOK applicability

Settings is where ROOK plants its hooks (routing-enforcer in `.claude/settings.json`), enables MCP servers, scopes agent permissions, and ships managed configs for cohort distribution. `skillOverrides` is the operator's primary control over the 20-agent listing budget. `permissions.deny` and `sandbox.*` are the security floor.

## Cross-references
- [[hooks]] — hook configuration shape
- [[skills]] — `skillOverrides`, `skillListingBudgetFraction`
- [[../guides/skills]] — Agent Skills spec
