# Google Analytics (GA4) connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct + Google MCP.

## Consumers
- `seo-specialist`
- `marketing-director`

## Integration kind
API-direct + Google MCP

## Credentials
OAuth2. Env vars GA4_SERVICE_ACCOUNT_JSON, GA4_PROPERTY_ID.

## Reversibility class
All endpoints are Y (read-only on already-collected events).

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/google-analytics.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
