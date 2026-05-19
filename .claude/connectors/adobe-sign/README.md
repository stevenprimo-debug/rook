# Adobe Sign connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct.

## Consumers
- `sales-director`
- `account-manager`

## Integration kind
API-direct

## Credentials
OAuth2. Env vars ADOBE_SIGN_CLIENT_ID, ADOBE_SIGN_CLIENT_SECRET, ADOBE_SIGN_REFRESH_TOKEN.

## Reversibility class
Sending agreements for signature is N. Reading agreement status is Y.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/adobe-sign.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
