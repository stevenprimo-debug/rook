# Meta Graph API (Instagram + Facebook) connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct.

## Consumers
- `social-media-manager`

## Integration kind
API-direct

## Credentials
OAuth2 with Page-scoped tokens. Env vars META_APP_ID, META_APP_SECRET, META_PAGE_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID.

## Reversibility class
Posts, comments, replies, DMs are N. Insights and read-only profile data are Y. IG and FB share one connector via Meta's unified API.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/meta-graph.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
