# Adobe Acrobat / PDF Services API connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct.

## Consumers
- `sales-director`
- `account-manager`
- `designer`

## Integration kind
API-direct

## Credentials
OAuth2 client credentials. Env vars ADOBE_CLIENT_ID, ADOBE_CLIENT_SECRET.

## Reversibility class
PDF generation and form-fill are Y (output is local). Submission to e-sign workflows is N — use the adobe-sign connector for that.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/adobe-acrobat.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
