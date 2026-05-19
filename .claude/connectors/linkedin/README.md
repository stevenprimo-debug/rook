# LinkedIn connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (LinkedIn API v2).

## Consumers
- `social-media-manager`
- `sales-director`

## Integration kind
API-direct (LinkedIn API v2)

## Credentials
OAuth2. Env vars LI_CLIENT_ID, LI_CLIENT_SECRET, LI_ACCESS_TOKEN.

## Reversibility class
Posts, comments, connection invites are N. Profile reads are Y but limited by LinkedIn's API scope (most data requires partner approval).

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/linkedin.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
