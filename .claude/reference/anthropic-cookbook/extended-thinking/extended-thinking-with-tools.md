---
name: extended-thinking-with-tools
source: https://github.com/anthropics/claude-cookbooks/blob/main/extended_thinking/extended_thinking_with_tool_use.ipynb
fetched: 2026-05-22
category: Extended Thinking
rook-relevance: medium
rook-status: inherit-via-skill
---

# Extended Thinking + Tool Use

## What it is

Enable transparent step-by-step reasoning BEFORE tool calls. Initial response can contain three block types: `thinking`, optional `text`, and `tool_use`. The model deliberates about which tools to call in the thinking block, then commits to tool invocations. After tool results return, the next response does NOT regenerate thinking — it reuses the preserved thinking context from history.

Key constraint: thinking blocks (including their cryptographic signatures) must be preserved verbatim in conversation history. The API validates signatures to ensure reasoning hasn't been tampered with.

## Key code/config

```python
thinking={
    "type": "enabled",
    "budget_tokens": 2000  # minimum 1024
}
```

Preservation pattern when sending tool results back:

```python
assistant_blocks = [
    block for block in response.content
    if block.type in ["thinking", "redacted_thinking", "tool_use"]
]
messages = [
    {"role": "user", "content": "initial query"},
    {"role": "assistant", "content": assistant_blocks},
    {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tid, "content": result}
    ]}
]
```

## Measured improvements / costs

No quantitative benchmarks. Tradeoff acknowledged: "tool use and thinking together can increase token usage and response time." Value is observability, not raw accuracy.

## ROOK applicability

ROOK's chief-of-staff dispatch + reversibility-gate (Rule #16 second-opinion-verify) already extracts decision rationale, but does so via prose synthesis, not signed thinking blocks. The cookbook's pattern is API-direct; inside Claude Code the thinking model is opaque to the agent layer. The pattern would only matter if ROOK exposes an API-direct adversarial verifier (Opus subagent with thinking enabled, returning structured rationale).

## Recommended action

**inherit-via-skill** — document the thinking+tools pattern in `.claude/reference/` for operators building API-direct second-opinion flows. No agent absorbs it in v3.1.
