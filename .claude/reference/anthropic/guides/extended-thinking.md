---
name: extended-thinking
source: https://platform.claude.com/docs/en/build-with-claude/extended-thinking
fetched: 2026-05-22
category: guides
rook-relevance: high
---

# Extended Thinking

## What it is

Enhanced reasoning with transparent step-by-step thought. Responses include `thinking` content blocks followed by `text` blocks.

## Key concepts + config

### Model support
| Model | Config |
|---|---|
| Opus 4.7 | `thinking: {type: "adaptive"}` + effort param. Manual mode returns 400 |
| Opus 4.6 | `adaptive` recommended; manual still works but deprecated |
| Sonnet 4.6 | `adaptive` recommended; manual + interleaved thinking deprecated |
| Mythos Preview | Adaptive by default; `display` defaults to `"omitted"` |
| Other Claude 4 | `thinking: {type: "enabled", budget_tokens: N}` |

### Basic config
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Your query"}],
)
```
`budget_tokens` < `max_tokens` (except with interleaved thinking).

### Display modes
- `display: "summarized"` (default on Claude 4) — returns summarized text, charged for full thinking. First few lines more verbose (useful for prompt eng)
- `display: "omitted"` (default on Opus 4.7, Mythos) — empty `thinking` field + encrypted `signature`. **Faster TTFT when streaming**. Still charged full.

```python
thinking={"type": "enabled", "budget_tokens": 10000, "display": "omitted"}
```

### Streaming
```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[...],
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```
With `display: "omitted"` no `thinking_delta` events — only `signature_delta`.

### Tool use with thinking
**Critical: always pass thinking blocks back unchanged in subsequent turns.**

```python
# First request: thinking + tool_use
response = client.messages.create(thinking={...}, tools=[weather_tool], messages=[...])
thinking_block = next(b for b in response.content if b.type == "thinking")
tool_use_block = next(b for b in response.content if b.type == "tool_use")

# Second request: MUST include thinking block in assistant turn
client.messages.create(
    thinking={...},
    tools=[weather_tool],
    messages=[
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": [thinking_block, tool_use_block]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_use_block.id, "content": "88°F"}
        ]},
    ],
)
```

### Tool choice limits with thinking
- Only `tool_choice: {"type": "auto"}` (default) or `{"type": "none"}`
- Cannot force `"any"` or specific tool

### Toggling thinking mid-turn
- **Cannot** toggle during tool-use loops
- Whole assistant turn must be single thinking mode
- If toggled: API silently disables thinking (silent degradation)
- **Plan thinking strategy at turn start**

### Interleaved thinking
Think between tool calls and after results.

Supported:
- Mythos Preview: automatic
- Opus 4.7 / 4.6 / Sonnet 4.6: automatic via adaptive
- Sonnet 4.6 manual: `interleaved-thinking-2025-05-14` beta header
- Other Claude 4: beta header

With interleaved thinking, `budget_tokens` CAN exceed `max_tokens`.

### Prompt caching interaction
- System prompt with cache markers → preserved when thinking params change
- Message-level cache → invalidated when budget changes
- Use same thinking params across turns for cache hits
- Opus 4.5+ / Sonnet 4.6+: thinking blocks kept by default; earlier models / Haiku: removed from context (but must preserve in tool-use turns)
- Cached thinking blocks count as input tokens when read

### Response format
```json
{"content": [
  {"type": "thinking", "thinking": "Let me analyze...", "signature": "WaUjzkypQ..."},
  {"type": "text", "text": "Based on my analysis..."}
]}
```

### Billing
- Charged for **full thinking tokens** regardless of `display`
- `budget_tokens` limits full thinking, not summary
- Cannot use `max_tokens: 0` with extended thinking (cache pre-warming incompatible)
- Output limits: Opus 4.7/4.6/Sonnet 4.6 = 64–128k; Mythos = 128k

### Best practices
1. Larger budget → quality on complex problems; Claude may not use all
2. `display: "omitted"` for latency-sensitive streaming
3. Preserve thinking blocks in multi-turn + tool use
4. Plan thinking mode at turn start
5. 1-hour cache for extended thinking tasks (often >5min)

## ROOK applicability

Extended thinking is the right call for office-hours, autoplan, plan-eng-review-equivalent ROOK agents — anywhere the answer benefits from explicit reasoning. `display: "omitted"` is the right default for ROOK agents that stream — operator wants the verdict fast, not the deliberation. **The tool-use thinking-block-preservation rule is a footgun**: ROOK's chief-of-staff must propagate `thinking` blocks when chaining tool calls — if not, silent degradation. Bake this into the dispatch loop.

## Cross-references
- [[tool-use]] — `tool_choice` constraints
- [[prompt-caching]] — cache interaction with thinking
- [[system-prompts]] — system prompt + thinking budget tradeoffs
- [[../claude-code/skills]] — `ultrathink` keyword in skill content for one-off deep reasoning
