---
name: tool-use
source: https://platform.claude.com/docs/en/build-with-claude/tool-use/overview
fetched: 2026-05-22
category: guides
rook-relevance: high
---

# Tool Use

## What it is

Claude calls functions you define (client tools) or that Anthropic provides (server tools). Highest-leverage primitive for agent capability — outsized capability gains on SWE-bench, LAB-Bench FigQA.

## Key concepts + config

### Client tools vs server tools
- **Client tools** (your code executes): user-defined tools + Anthropic-schema tools like `bash`, `text_editor`. Claude returns `stop_reason: "tool_use"` with `tool_use` blocks; you execute and POST back `tool_result`.
- **Server tools** (Anthropic executes): `web_search`, `code_execution`, `web_fetch`, `tool_search`. Results come back directly.

### Simplest example (server tool)
```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[{"type": "web_search_20260209", "name": "web_search"}],
    messages=[{"role": "user", "content": "What's the latest on the Mars rover?"}],
)
```

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-7",
    "max_tokens": 1024,
    "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    "messages": [{"role": "user", "content": "Latest on Mars rover?"}]
  }'
```

### Strict tool use
Add `strict: true` to tool definitions to guarantee tool calls match your schema exactly. See `/agents-and-tools/tool-use/strict-tool-use`.

### Tool-use loop (client tools — pseudo-code)
```python
# Claude returns stop_reason="tool_use"
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = your_executor(tool_use)
    response = client.messages.create(
        ...,
        messages=[
            *prior_messages,
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
            ]},
        ],
    )
```

### Missing parameters
- Opus more likely to ask for missing required params
- Sonnet may infer reasonable defaults — not guaranteed safe
- Use Opus when stakes are high for parameter completeness

### MCP connector
For connecting to MCP servers via API instead of Claude Code, see `/agents-and-tools/mcp-connector`. For building your own MCP client, see modelcontextprotocol.io.

### Pricing
Tool use system prompt adds tokens **per request**:
| Model | `auto`/`none` | `any`/`tool` |
|---|---|---|
| Opus 4.5–4.7, Sonnet 4.5–4.6, Haiku 4.5 | 346 | 313 |
| Haiku 3.5 (legacy) | 264 | 340 |

Plus: tools array (names + descriptions + schemas), `tool_use` blocks, `tool_result` blocks. Server tools add usage-based pricing (e.g., web search per query).

### `tool_choice` options
- `auto` (default) — model decides
- `none` — no tools
- `any` — must use a tool
- `tool` — must use specific named tool
(Tool-choice constraint: `any`/`tool` with extended thinking — see [[extended-thinking]])

## ROOK applicability

The Agent tool (subagent dispatch) is the single most-used tool for ROOK's chief-of-staff. `strict: true` on user-defined tools is how ROOK should guarantee dispatched briefs match the expected JSON shape (no parsing failures downstream). Opus's "more likely to ask for missing params" behavior is why chief-of-staff should default to Opus when the spitball is ambiguous, fall back to Sonnet when scope is locked. Tool use system-prompt token cost (~346 tokens) is non-trivial — informs whether to bundle many tools into one agent or split across subagents.

## Cross-references
- [[../claude-code/mcp]] — MCP transport for tools
- [[extended-thinking]] — `tool_choice` constraints with thinking
- [[prompt-caching]] — caching tool definitions
- [[../agent-sdk/overview]] — built-in tools list
