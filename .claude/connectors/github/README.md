# GitHub connector

**Status:** v1 stub — README + api-reference scaffolded; Anthropic official MCP available.

## Consumers
- `software-dev-team`
- `software-dev-team/skills/github-ops`

## Integration kind
Anthropic official MCP available

## Credentials
Personal access token or GitHub App. Env vars GITHUB_TOKEN (PAT) or app-credentials JSON.

## Reversibility class
Reads (repo / issue / PR / commit) are Y. Writes (commits, PRs, merges, releases, issue creation) are N. The github-ops child skill enforces this gate.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/github.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
