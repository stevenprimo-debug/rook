# QuickBooks Online connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct.

## Consumers
- `finance-manager`

## Integration kind
API-direct

## Credentials
OAuth2 flow. Env vars QBO_CLIENT_ID, QBO_CLIENT_SECRET, QBO_REFRESH_TOKEN, QBO_REALM_ID.

## Reversibility class
All POST/PUT/DELETE (journal entries, invoices, bills) are N. Reads are Y.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/quickbooks.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
