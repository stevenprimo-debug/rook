---
name: tool-evaluation
source: https://github.com/anthropics/claude-cookbooks/blob/main/tool_evaluation/tool_evaluation.ipynb
fetched: 2026-05-22
category: Evaluations
rook-relevance: medium
rook-status: absorb-recommended
---

# Tool Evaluation

## What it is

Parallel evaluation harness for testing tools across independent agent instances. Tasks load from XML files, each runs through an agent loop with a defined tool set, harness captures accuracy + duration + tool-call count per task, aggregates into a report with agent-provided feedback on tool quality.

Architecture separates: task parsing, agent execution with tool instrumentation, metric collection, result aggregation.

## Key code/config

Task XML:
```xml
<task>
  <prompt>calculation request</prompt>
  <response>expected answer</response>
</task>
```

Scoring: binary exactness `int(response == task["response"])` + tool call count + per-task duration via `time.time()` wraps.

Sample run: **87.5% accuracy (7/8 tasks), 22.73s avg per task, 7.75 tool calls avg, 8.6-38.4s task duration range.**

## ROOK applicability

Direct fit for ROOK's agents that wield Anthropic Skills tools (markitdown, html2pdf, graphify, obsidian-cli) — i.e., every agent inherits the Universal Stack. A tool-eval harness would catch silent breakage when an upstream skill version changes the markitdown output shape and an agent's downstream parse fails.

Complements the broader eval shelf (see `building-evals.md`). Where building-evals tests "does the agent route correctly," tool-evaluation tests "does the tool itself behave as the agent expects."

## Recommended action

**absorb-recommended** — fold into the `.claude/evals/` scaffold. Add a `tool-evals/` subdirectory with XML tasks for the Universal Stack skills. Effort: ~1 day after evals scaffold lands. Combined with building-evals work above, this is a 4-day v3.1 sprint item.
