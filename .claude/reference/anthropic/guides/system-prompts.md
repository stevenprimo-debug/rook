---
name: system-prompts
source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/system-prompts
fetched: 2026-05-22
category: guides
rook-relevance: high
---

# System Prompts

## What it is

Top-level role/voice/behavior instructions passed via the `system` parameter (Messages API) or via `--system-prompt` / `--append-system-prompt` (Claude Code CLI). Separate from user/assistant message content.

## Key concepts + config

### Basic shape
```python
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    system="You are a senior code reviewer. Lead with the verdict. Skip preamble.",
    messages=[{"role": "user", "content": "Review this diff..."}],
)
```

### As an array (for cache_control)
```python
system=[
    {"type": "text", "text": "Long system prompt..."},
    {"type": "text", "text": "Voice rules...", "cache_control": {"type": "ephemeral"}},
]
```

### Patterns

**Role setting**: "You are a senior security engineer reviewing for OWASP Top 10..."

**Voice setting**: "Lead with verdict. No preamble. Banned words: delve, leverage, robust."

**Output format**: "Respond in this exact JSON shape: `{verdict: 'pass'|'fail', reasons: [...]}`"

**Reasoning style**: "Think step by step inside `<thinking>` tags before answering."

**Constraints**: "Never modify files outside the working directory. Never run network commands."

### Claude Code system prompt flags
```bash
# Append to default Claude Code system prompt
claude -p "..." --append-system-prompt "You are a security engineer..."
# Read from file
claude -p "..." --append-system-prompt-file ./system.md
# Fully replace (lose Claude Code's built-in SWE instructions)
claude -p "..." --system-prompt "Custom from scratch..."
```

### Output styles (Claude Code alternative)
Per [[../claude-code/output-styles]]: Output styles modify the system prompt directly and apply to every response. Use when you want a different role/tone/format every turn.

### Best practices

**Be specific about role + audience**: "You are a code reviewer **for a Python codebase** writing for **the implementing engineer**, not their manager."

**Direct constraints work better than negations**: "Use only Python 3.11+ features" > "Don't use old Python"

**Use XML tags inside system prompts** for structure:
```
<role>...</role>
<constraints>...</constraints>
<output_format>...</output_format>
```

**Lead with the most important rules** — system prompts are read top-to-bottom; later rules have less weight.

**System prompt is cached aggressively** — cheap to make it long ONCE; expensive if you change it every request (invalidates everything).

**Don't put varying content in system** — put it in `messages` so the cached prefix stays stable.

## ROOK applicability

The ROOK voice contract belongs in the system prompt (or output-style equivalent). For each of the 20 agents, SKILL.md body becomes their system prompt when run as a subagent — so SKILL.md is THE place to encode role + voice + constraints. Don't repeat the voice contract in each agent's body — put it once in CLAUDE.md (which loads for all agents) and let agent bodies add specialization. `--append-system-prompt` is the right pattern for the routing-enforcer hook injecting dept-specific guidance without replacing Claude Code's defaults.

## Cross-references
- [[prompt-engineering]] — broader best practices
- [[prompt-caching]] — system caches well; don't varying it
- [[../claude-code/output-styles]] — alternative to system param
- [[../claude-code/subagents]] — `prompt` field = subagent system prompt
