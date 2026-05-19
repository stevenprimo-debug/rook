# Perplexity connector

**Status:** v1 — `client.py` shipped; tested against Search API.

## Consumers
- `deep-researcher` (primary — second-opinion synthesis, source-cited search)
- `seo-specialist` (AEO Mode — Perplexity is itself an answer engine; testing surface)
- `chief-of-staff` (optional — quick fact-check on routing decisions)
- `marketing-director` (competitive scans)

## Why this matters
Perplexity returns **source-cited synthesized answers**. Where WebSearch
returns links and WebFetch returns one page, Perplexity returns "the answer
with citations." For deep-researcher, that means ping-pong synthesis: Claude
proposes, Perplexity counter-synthesizes, Claude reconciles. Different models,
different training cuts — disagreement surfaces what's actually contested.

## Credentials
- Env var: `PERPLEXITY_API_KEY`
- Storage convention: `~/.claude/credentials/perplexity.json` (gitignored) OR
  PowerShell profile env var
- Setup: console.perplexity.ai -> API Keys -> create key (one-time view, save
  immediately)

## Endpoints
- Base URL: `https://api.perplexity.ai`
- Auth: `Authorization: Bearer <PERPLEXITY_API_KEY>`
- Content-Type: `application/json`

| Endpoint | Method | Purpose |
|---|---|---|
| `/search` | POST | Search with synthesized summary + citations |
| `/agent` | POST | Agent API — multi-turn synthesis |
| `/embeddings` | POST | Embed text for vector search |

## Reversibility class
- ALL endpoints are **Y (read-only)**. Perplexity makes no external state
  change on the operator's behalf. Cost is the only side effect (per-query
  pricing), so consumers should respect a sane `max_results` and avoid
  paginated loops without explicit operator confirm.

## Rate limits + cost
- Pricing tier set at console; default is per-query metered
- No hard rate limit documented; respect 429 backoff exponentially

## Invocation pattern

```python
from claude_connectors.perplexity import PerplexityClient

ppx = PerplexityClient.from_env()

# Single search
result = ppx.search(
    query="What's the current state of multi-agent coordinator caps in the Anthropic API?",
    max_results=5,
    max_tokens_per_page=512,
)

# result.summary -> str (Perplexity's synthesized answer)
# result.citations -> list[dict] with url + title + snippet
# result.raw -> dict (full response)

# Ping-pong pattern (deep-researcher's bread and butter)
claude_thesis = "<your synthesis>"
ppx_counter = ppx.search(query=f"Counter-evidence or disagreement with: {claude_thesis}")
# Claude reads ppx_counter.summary + citations, decides whether to revise thesis
```

## Operator setup checklist
- [x] Perplexity API key created (2026-05-19)
- [ ] Key stored at `~/.claude/credentials/perplexity.json` OR env var
- [ ] Env var `PERPLEXITY_API_KEY` set in PowerShell profile
- [ ] Tested `ppx.search()` returns expected data
- [ ] Add deep-researcher's voice corpus reference (which queries land vs which return generic)

## Notes
- The Anthropic-hosted MCP marketplace does NOT currently expose Perplexity
  as a vendored MCP — this is direct API integration via `_lib/perplexity/client.py`.
- For the AMA (Anthropic Managed Agents) deployment path, this connector ships
  as part of the operator's vault setup; the Perplexity key is operator-owned
  and never traverses ROOK infrastructure.
