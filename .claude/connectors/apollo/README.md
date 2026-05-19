# Apollo.io connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct.

## Consumers
- `sales-director`

## Integration kind
API-direct

## Credentials
API key. Env var APOLLO_API_KEY.

## Reversibility class
List enrichment, person search are Y (Apollo's own data). Pushing to operator's CRM is N — use the hubspot connector for that.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/apollo.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
