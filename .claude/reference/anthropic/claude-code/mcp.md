---
name: mcp
source: https://code.claude.com/docs/en/mcp
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Claude Code + MCP

## What it is

Model Context Protocol — open standard for connecting Claude Code to external tools, databases, APIs. ROOK uses MCP for graphify, second-opinion-verify (Perplexity), and any future external integrations.

## Key concepts + config

### Three transports
- **HTTP** (recommended for remote) — `claude mcp add --transport http <name> <url>`
- **SSE** (deprecated) — `claude mcp add --transport sse <name> <url>`
- **stdio** (local process) — `claude mcp add --transport stdio <name> -- <cmd> [args]`

In JSON, `streamable-http` is an alias for `http`.

### Install examples
```bash
# Remote HTTP
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With auth header
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"

# Local stdio with env
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

### Option ordering rule
All options (`--transport`, `--env`, `--scope`, `--header`) come **before** the name. `--` separates name from command.

### Three scopes
| Scope | Loads in | Shared | Stored |
|---|---|---|---|
| Local (default) | Current project | No | `~/.claude.json` |
| Project | Current project | Yes (VCS) | `.mcp.json` in root |
| User | All your projects | No | `~/.claude.json` |

**Precedence**: Local > Project > User > Plugin > claude.ai connectors. Three scopes match by name; plugins/connectors match by endpoint.

### .mcp.json shape
```json
{
  "mcpServers": {
    "shared-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {"Authorization": "Bearer ${API_KEY}"},
      "timeout": 600000,
      "alwaysLoad": false
    }
  }
}
```

### Env var expansion in .mcp.json
- `${VAR}` — value of VAR
- `${VAR:-default}` — VAR or default
- Available in: `command`, `args`, `env`, `url`, `headers`

### Management
```bash
claude mcp list
claude mcp get <name>
claude mcp remove <name>
/mcp                    # in session — status, OAuth, channels
```

### Plugin-provided MCP
Plugins bundle servers in `.mcp.json` at plugin root or inline in `plugin.json`. Use `${CLAUDE_PLUGIN_ROOT}` for paths, `${CLAUDE_PLUGIN_DATA}` for persistent state, `${CLAUDE_PROJECT_DIR}` for project root.

### OAuth
401/403 from server flags it for OAuth. Use `/mcp` to authenticate. Fixed callback: `--callback-port 8080`. Pre-configured credentials: `--client-id ... --client-secret`. Override discovery: `oauth.authServerMetadataUrl`. Restrict scopes: `oauth.scopes: "channels:read chat:write"`.

### Tool Search (default ON)
MCP tools deferred until needed — only names load upfront. Toggle via `ENABLE_TOOL_SEARCH`:
- (unset) — defer all (default; falls back on Vertex/proxies)
- `true` — defer always
- `auto` — load upfront if <10% context window
- `auto:N` — custom threshold percentage
- `false` — load all upfront

Exempt a server: `"alwaysLoad": true` in its config. Disable ToolSearch tool: `"deny": ["ToolSearch"]`.

### Output limits
Warns at 10,000 tokens. Default cap 25,000. Adjust via `MAX_MCP_OUTPUT_TOKENS`. Server-side tool annotation: `_meta["anthropic/maxResultSizeChars"]` (max 500,000).

### Use Claude Code AS an MCP server
```bash
claude mcp serve
```
Exposes Claude's tools (View, Edit, LS) to other MCP clients.

### Reference resources via @mention
`@server:protocol://resource/path` — e.g. `@github:issue://123`.

### MCP prompts as commands
`/mcp__servername__promptname [args]`

## ROOK applicability

graphify MCP is how ROOK queries the knowledge graph. Future ROOK distributions ship project-scoped `.mcp.json` so cohort users get the same connectors. `alwaysLoad: true` is for critical-path servers like graphify; everything else stays deferred. `headersHelper` is the pattern for short-lived token auth (relevant for second-opinion-verify rotating Perplexity keys without leaking them to config).

## Cross-references
- [[overview]] — MCP listed as integration point
- [[hooks]] — `mcp_tool` hook type
- [[skills]] — skills can reference MCP resources
- [[../guides/tool-use]] — tool-use API patterns
