# Autodesk (Fusion / AutoCAD) connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (Forge / Platform Services).

## Consumers
- `engineering-lead`

## Integration kind
API-direct (Forge / Platform Services)

## Credentials
OAuth2 3-legged or 2-legged depending on use. Env vars AUTODESK_CLIENT_ID, AUTODESK_CLIENT_SECRET.

## Reversibility class
Reading files, extracting BOM data, querying model state are Y. Writing changes back to a hosted model is N.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/autodesk.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
