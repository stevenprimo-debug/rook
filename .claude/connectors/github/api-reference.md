# GitHub API — agent-facing reference

**Status:** stub — fill in on first connector use against the live docs.

## Authentication
Personal access token or GitHub App. Env vars GITHUB_TOKEN (PAT) or app-credentials JSON.

## Endpoints

| Endpoint | Method | Purpose | Reversibility |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 200 | OK | proceed |
| 401 | Auth failed | rotate / re-auth |
| 429 | Rate limit | exponential backoff |
| 500-599 | Vendor-side | exponential backoff |

## Reversibility per endpoint

Reads (repo / issue / PR / commit) are Y. Writes (commits, PRs, merges, releases, issue creation) are N. The github-ops child skill enforces this gate.

## Notes for first-use

When the consuming agent invokes this connector for the first time:
1. Verify the live API docs against this stub
2. Update endpoint table with the calls you actually need
3. Add error patterns specific to this service
4. If implementing `client.py`, copy `.claude/connectors/perplexity/client.py` as the pattern
