# Adobe Acrobat / PDF Services API API — agent-facing reference

**Status:** stub — fill in on first connector use against the live docs.

## Authentication
OAuth2 client credentials. Env vars ADOBE_CLIENT_ID, ADOBE_CLIENT_SECRET.

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

PDF generation and form-fill are Y (output is local). Submission to e-sign workflows is N — use the adobe-sign connector for that.

## Notes for first-use

When the consuming agent invokes this connector for the first time:
1. Verify the live API docs against this stub
2. Update endpoint table with the calls you actually need
3. Add error patterns specific to this service
4. If implementing `client.py`, copy `.claude/connectors/perplexity/client.py` as the pattern
