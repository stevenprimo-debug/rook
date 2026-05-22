---
name: prompt-caching
source: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
fetched: 2026-05-22
category: guides
rook-relevance: high
---

# Prompt Caching

## What it is

Caches prompt prefixes for cost + latency reduction. Cache writes at explicit `cache_control` breakpoints; reads via 20-block backward lookback. Lifetime 5 minutes (default) or 1 hour (2x write cost).

## Key concepts + config

### Pricing multipliers
- 5m cache write = 1.25x base input
- 1h cache write = 2x base input
- Cache read = 0.1x base input

### Automatic caching (simplest)
```json
{
  "cache_control": {"type": "ephemeral"},
  "system": "...",
  "messages": [...]
}
```
Top-level `cache_control` auto-applies breakpoint to last cacheable block, moves forward as conversation grows.

### Explicit breakpoints (up to 4 per request)
```json
{
  "model": "claude-opus-4-7",
  "system": [
    {"type": "text", "text": "System instructions...", "cache_control": {"type": "ephemeral"}}
  ],
  "messages": [
    {"role": "user", "content": [
      {"type": "text", "text": "User query...", "cache_control": {"type": "ephemeral"}}
    ]}
  ]
}
```

### TTL = 1 hour
```json
{"cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

### Pre-warming
```json
{"max_tokens": 0, "system": [{"type": "text", "text": "...", "cache_control": {"type": "ephemeral"}}]}
```
Reads prompt into cache without generating output.

### Cacheable content
- Tools (entire `tools` array)
- System messages
- Text messages (user/assistant turns)
- Images, documents
- Tool use + tool results

**NOT cacheable**: thinking blocks directly, empty text blocks, sub-content blocks (citation refs).

### Usage fields in response
- `cache_creation_input_tokens` — written to cache (new entry)
- `cache_read_input_tokens` — read from cache (hit)
- `input_tokens` — after last breakpoint (not cached)

Total input = sum of all three.

### Critical placement rule
**Place `cache_control` on the last block whose prefix is identical across requests.**

❌ Putting breakpoint after a timestamp = prefix changes every request = no cache hit.

✅ Put static content first, breakpoint at end of static, varying content after.

### Cache invalidation matrix
| Change | Invalidates |
|---|---|
| Tool definitions | Tools + System + Messages |
| Web search / citations toggle | System + Messages |
| Speed setting | System + Messages |
| `tool_choice` param | Messages only |
| Images anywhere | Messages only |
| Extended thinking settings | Messages only |
| Non-tool content in thinking (Opus <4.5, Sonnet <4.6, all Haiku) | Messages |

Opus 4.5+ and Sonnet 4.6+ preserve thinking blocks by default.

### Minimum thresholds
- Opus 4.7/4.6/4.5, Haiku 4.5, Mythos: **4,096 tokens**
- Sonnet 4.6/4.5, Opus 4.1, Haiku 3.5: 1,024–2,048 tokens

Shorter prompts not cached, no error. Check `cache_creation_input_tokens` to verify.

### Workspace isolation (Feb 5 2026+)
- Claude API, Bedrock, Vertex AI: per-workspace within org
- Bedrock/Vertex legacy: org-level
- Never cross-org

### Best practices
1. Start with automatic caching for multi-turn
2. Use explicit breakpoints when sections change at different frequencies
3. Cache early reusable content (system, tools, context)
4. Place breakpoints on static prefixes
5. Keep breakpoint within 20-block lookback of last write
6. Pre-warm latency-sensitive apps with `max_tokens: 0`
7. Use 1-hour cache for >5min request gaps

## ROOK applicability

This is how the cost story holds for the 20-agent OS. Each agent's SKILL.md becomes a stable prefix — cache it. Routing-enforcer hook output becomes a varying suffix — don't cache. For chief-of-staff dispatching the same brief shape repeatedly, put the brief template + scope rules in `system` with `cache_control`, put the actual spitball in `messages` (varying). Critical for ROOK economic viability at scale — without prompt caching, every agent invocation re-pays for the full SKILL.md body.

## Cross-references
- [[tool-use]] — caching tool definitions invalidates everything
- [[extended-thinking]] — thinking settings invalidate messages cache
- [[citations]] — cached document blocks work with citations
- [[../claude-code/skills]] — skill content lifecycle / compaction interaction
