# Figma connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct + community MCP available.

## Consumers
- `designer`
- `creative-director`

## Integration kind
API-direct + community MCP available

## Credentials
Personal access token. Env var FIGMA_PAT.

## Reversibility class
Reads (file structure, components, variants) are Y. Comments and webhook setup are N.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/figma.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
