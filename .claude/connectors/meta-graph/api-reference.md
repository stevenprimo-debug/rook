# Meta Graph API (Instagram + Facebook) API — agent-facing reference

**Status:** stub — fill in on first connector use against the live docs.

## Authentication
OAuth2 with Page-scoped tokens. Env vars META_APP_ID, META_APP_SECRET, META_PAGE_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID.

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

Posts, comments, replies, DMs are N. Insights and read-only profile data are Y. IG and FB share one connector via Meta's unified API.

## Notes for first-use

When the consuming agent invokes this connector for the first time:
1. Verify the live API docs against this stub
2. Update endpoint table with the calls you actually need
3. Add error patterns specific to this service
4. If implementing `client.py`, copy `.claude/connectors/perplexity/client.py` as the pattern
