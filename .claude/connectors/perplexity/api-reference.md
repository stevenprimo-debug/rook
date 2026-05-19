# Perplexity API — agent-facing reference

Source: docs.perplexity.ai (verify against live docs on connector first-use; this snapshot may go stale).

## Authentication

All endpoints use bearer token auth:
```
Authorization: Bearer pplx-...
Content-Type: application/json
```

Token is created at console.perplexity.ai/account/setup. Single-view at creation — store immediately.

## /search

Synthesized search with source citations. Primary endpoint for deep-researcher's ping-pong pattern.

**Request:**
```json
{
  "query": "string",
  "max_results": 3,
  "max_tokens_per_page": 256
}
```

**Response (representative; field names may evolve):**
```json
{
  "answer": "Synthesized response with inline citation markers",
  "citations": [
    {"url": "https://...", "title": "...", "snippet": "..."}
  ],
  "usage": {"prompt_tokens": N, "completion_tokens": N}
}
```

## /agent

Multi-turn agent API. Useful when the synthesis needs the prior turn for context.

**Request:**
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "system", "content": "You are a research synthesizer."},
    {"role": "user", "content": "First question."},
    {"role": "assistant", "content": "Previous answer."},
    {"role": "user", "content": "Follow-up that depends on the previous answer."}
  ],
  "max_tokens": 1024
}
```

## /embeddings

Vector embeddings for retrieval / similarity. Use when building a corpus an agent will repeatedly query.

**Request:**
```json
{
  "model": "embed-v1",
  "input": ["text 1", "text 2"]
}
```

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 200 | OK | proceed |
| 400 | Bad request — usually malformed body | inspect detail, fix payload |
| 401 | Auth failed — key revoked or wrong | rotate at console |
| 429 | Rate limit | exponential backoff, max 3 retries |
| 500-599 | Perplexity-side | exponential backoff |

## Ping-pong pattern (deep-researcher's canonical use)

```python
# Step 1: Claude produces a thesis
claude_thesis = compose_thesis(question)

# Step 2: Perplexity counter-synthesizes
ppx_response = ppx.search(
    query=f"Counter-evidence or disagreement with: {claude_thesis}",
    max_results=5,
)

# Step 3: Claude reads citations, decides whether to revise
if disagreement_found(ppx_response):
    revised = revise_thesis(claude_thesis, ppx_response.citations)
else:
    revised = claude_thesis

# Step 4 (optional): Multi-turn refinement via /agent
final = ppx.agent(messages=[
    {"role": "user", "content": revised},
    {"role": "assistant", "content": "(Claude's revised thesis)"},
    {"role": "user", "content": "What's the strongest steelman against this?"}
])
```

This is the pattern deep-researcher's bench (Source-Credibility-Pole + Synthesis-Pole) optimizes for. Each ping-pong cycle should produce either consensus (both models converge) or a labeled gap (the disagreement IS the finding).
