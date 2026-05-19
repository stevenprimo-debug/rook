# Twitter / X connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (v2 API).

## Consumers
- `social-media-manager`

## Integration kind
API-direct (v2 API)

## Credentials
Bearer token + OAuth1 for write endpoints. Env vars X_BEARER_TOKEN, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.

## Reversibility class
Tweets, replies, DMs, follows are N. Read endpoints (search, user lookup, mentions) are Y. Heavy rate-limits on v2 free tier.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/twitter-x.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
