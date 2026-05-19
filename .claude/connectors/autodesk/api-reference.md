# Autodesk (Fusion / AutoCAD) API — agent-facing reference

**Status:** stub — fill in on first connector use against the live docs.

## Authentication
OAuth2 3-legged or 2-legged depending on use. Env vars AUTODESK_CLIENT_ID, AUTODESK_CLIENT_SECRET.

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

Reading files, extracting BOM data, querying model state are Y. Writing changes back to a hosted model is N.

## Notes for first-use

When the consuming agent invokes this connector for the first time:
1. Verify the live API docs against this stub
2. Update endpoint table with the calls you actually need
3. Add error patterns specific to this service
4. If implementing `client.py`, copy `.claude/connectors/perplexity/client.py` as the pattern
