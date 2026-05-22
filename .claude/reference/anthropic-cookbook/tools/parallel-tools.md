---
name: parallel-tools
source: https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/parallel_tools.ipynb
fetched: 2026-05-22
category: Tools & Tool Use
rook-relevance: medium
rook-status: inherit-via-skill
---

# Parallel Tool Calls via Batch Meta-Pattern

## What it is

Claude 3.7+ underuses native parallel tool calling. The workaround is a meta-tool called `batch_tool` that wraps an array of tool invocations. When the model sees `batch_tool` available, it preferentially invokes it to declare multiple concurrent operations in a single turn — eliminating sequential round-trips. The client unpacks the array and dispatches all sub-calls in parallel.

This is purely a prompt-and-schema trick. No SDK change required. The win is converting N sequential turns into 1 turn — latency drops roughly N-fold for independent calls.

## Key code/config

Tool schema:

```python
"invocations": {
  "type": "array",
  "items": {
    "properties": {
      "name": {"type": "string"},
      "arguments": {"type": "string"}
    }
  }
}
```

Dispatch logic:

```python
if tool_name == "batch_tool":
    for invocation in tool_input["invocations"]:
        results.append(process_tool_call(
            invocation["name"],
            json.loads(invocation["arguments"])
        ))
```

## Measured improvements / costs

**No quantified metrics in the notebook.** Benefit is conceptual: simultaneous vs. sequential execution. Real-world wins depend entirely on how independent the wrapped calls are.

## ROOK applicability

ROOK's chief-of-staff already dispatches subagents — and Claude Code's tool runtime supports natural parallel `function_calls` blocks (chief-of-staff orchestration pattern already uses this). The `batch_tool` meta-pattern is an API-level workaround for environments without parallel calling, not a Claude Code pattern. Inside Claude Code, parallel calls already work via parallel tool_use blocks. The cookbook pattern would only matter if ROOK ships an Anthropic-API-direct path (none currently planned).

## Recommended action

**inherit-via-skill** — document the batch-tool pattern in `.claude/reference/` for operators who later build API-direct flows, but no agent absorbs it now. ROOK's parallel dispatch happens via Claude Code's native parallel tool_use blocks, not API meta-tools.
