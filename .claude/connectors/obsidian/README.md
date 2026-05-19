# Obsidian (via obsidian-cli) connector

**Status:** v1 stub — README + api-reference scaffolded; wrapper around existing skill.

## Consumers
- `librarian`
- `chief-of-staff`
- `all agents (vault I/O)`

## Integration kind
wrapper around existing skill

## Credentials
No external auth — local vault path via VAULT_ROOT env var. Wraps the obsidian-cli skill already shipped.

## Reversibility class
Vault reads are Y. Vault writes are reversible at the filesystem level but should still be logged to librarian's append log.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/obsidian.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
