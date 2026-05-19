# Google Drive / SharePoint connector

**Status:** v1 stub — README + api-reference scaffolded; Anthropic MCP (already wired).

## Consumers
- `account-manager`
- `librarian`
- `inbox-custodian`

## Integration kind
Anthropic MCP (already wired)

## Credentials
Wired via Anthropic MCP setup.

## Reversibility class
File create / overwrite / delete are N. Reads (search, list, read_file_content) are Y.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/drive-sharepoint.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
