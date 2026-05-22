---
name: prompt-caching
source: https://github.com/anthropics/claude-cookbooks/blob/main/misc/prompt_caching.ipynb
fetched: 2026-05-22
category: Responses & Prompt Engineering
rook-relevance: high
rook-status: absorb-recommended
---

# Prompt Caching

## What it is

Store frequently-reused context (system prompt, tools, message history, large document blocks) at API-side cache; pay 1.25× write cost once, then 0.1× standard input cost on every hit. Cache breakpoints can be automatic (single `cache_control` param at request level) or explicit (per content block). Default TTL 5 minutes (renewed on every hit); 1-hour TTL available at 2× base cost.

Cacheable: system prompts, message history, tools, text content blocks. Minimums: 1024 tokens (Sonnet), 4096 tokens (Opus/Haiku).

## Key code/config

Automatic (recommended starting point):
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    cache_control={"type": "ephemeral"},
    messages=[...]
)
```

Explicit breakpoint:
```python
{"type": "text", "text": "long context", "cache_control": {"type": "ephemeral"}}
```

## Measured improvements / costs

Cookbook benchmark on Pride and Prejudice (~187K tokens):

| Scenario | Time | Cache state |
|---|---|---|
| No caching baseline | 4.89s | — |
| First cached call (write) | 4.28s | 187,361 written |
| Second cached call (hit) | **1.48s** | 187,361 read — **3.3× faster** |

Multi-turn (4 questions): 99% of input tokens served from cache after turn 1. Reads cost 1/10× input rate. **Break-even after 2-3 reuses; savings up to 90% on repeated workloads.**

## ROOK applicability

Massive fit. ROOK's pattern is "agent loads its own context surfaces at Step 1 of every invocation" — meaning the same context (SKILL.md, MEMORY.md, shared shelf, voice-spine) is re-loaded every turn. With caching:

- **Voice spine + frameworks** — loaded by every agent, every turn → high-volume reuse
- **SKILL.md + personality bench** — per-agent, loaded each invocation
- **Shared shelf reference** — loaded by deep-researcher / librarian / engineering-lead repeatedly

Inside Claude Code today the runtime handles caching transparently — operators rarely touch it. But for any agent invoked at API-direct level (cohort customer building their own pipeline on top of ROOK), explicit cache_control on the agent's loaded SKILL.md + memory blocks could deliver the 90% savings the cookbook quotes.

## Recommended action

**absorb-recommended** — document a caching-strategy section in `.claude/reference/prompt-caching.md` that maps to ROOK's context-load gate (Rule #12). Specifically: which surfaces are cache-worthy (SKILL.md, voice spine, shared shelf shards), recommended TTLs (5min for active sessions, 1hr for batch sweeps like librarian's weekly index). Effort: ~half day to document; cost-savings only realize when customer wires it into their API path. Cohort-facing value.
