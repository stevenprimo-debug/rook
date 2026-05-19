# Google Search Console connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct + Google MCP.

## Consumers
- `seo-specialist`

## Integration kind
API-direct + Google MCP

## Credentials
OAuth2 service account or user OAuth. Env vars GSC_SERVICE_ACCOUNT_JSON OR GSC_OAUTH_REFRESH_TOKEN + property URL.

## Reversibility class
All endpoints are Y (read-only on indexed data + crawl errors). Submitting sitemaps is technically a write but reversible.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/google-search-console.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
