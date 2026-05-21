# Tradovate API — agent-facing reference

**Status:** stub — verify against https://api.tradovate.com/ docs on first connector use.
**Base URLs:**
- Demo REST: `https://demo.tradovateapi.com/v1`
- Live REST: `https://live.tradovateapi.com/v1`
- Demo WS: `wss://demo.tradovateapi.com/v1/websocket`
- Live WS: `wss://live.tradovateapi.com/v1/websocket`
- Market-data WS: `wss://md.tradovateapi.com/v1/websocket`

## Authentication

POST `/auth/accesstokenrequest`:
```json
{
  "name": "<TRADOVATE_USERNAME>",
  "password": "<TRADOVATE_PASSWORD>",
  "appId": "<TRADOVATE_APP_ID>",
  "appVersion": "<TRADOVATE_APP_VERSION>",
  "cid": <TRADOVATE_CID>,
  "sec": "<TRADOVATE_SEC>"
}
```

Response: `{ "accessToken": "...", "expirationTime": "...", "userId": ..., ... }`
Bearer token in subsequent requests: `Authorization: Bearer <accessToken>`

Token expires in ~80 minutes. Refresh proactively via `/auth/renewaccesstoken`.

## Endpoints

| Endpoint | Method | Purpose | Reversibility |
|---|---|---|---|
| `/auth/accesstokenrequest` | POST | Acquire bearer token | Y |
| `/auth/renewaccesstoken` | GET | Refresh token before expiry | Y |
| `/account/list` | GET | List accounts owned by operator | Y |
| `/account/find` | GET | Find one account by ID | Y |
| `/position/list` | GET | All open positions | Y |
| `/order/list` | GET | Order history | Y |
| `/order/placeorder` | POST | **Place new order** | **N** |
| `/order/modifyorder` | POST | **Modify working order** | **N** |
| `/order/cancelorder` | POST | **Cancel working order** | **N** (fills may have occurred) |
| `/order/liquidateposition` | POST | **Market-close a position** | **N** |
| `/fillFee/list` | GET | Commission + fee history | Y |
| `/cashBalance/list` | GET | Cash balance per account | Y |
| `/marginSnapshot/list` | GET | Margin requirements | Y |
| `/contract/find` | GET | Resolve instrument by symbol | Y |
| `/exchange/list` | GET | List exchanges | Y |
| `/product/list` | GET | List products (ES, NQ, CL, GC, etc.) | Y |

## Order placement payload (N — operator confirm required)

```json
{
  "accountSpec": "<account-name>",
  "accountId": <id>,
  "action": "Buy" | "Sell",
  "symbol": "ESM6",
  "orderQty": 1,
  "orderType": "Market" | "Limit" | "Stop" | "StopLimit",
  "price": <limit-price-if-limit>,
  "stopPrice": <stop-price-if-stop>,
  "timeInForce": "Day" | "GTC" | "IOC" | "FOK",
  "isAutomated": false
}
```

`isAutomated: true` flags the order as algo-originated for regulatory reporting. ROOK trading-analyst should set this true when placing orders from a webhook-routed strategy.

## WebSocket subscription pattern

After auth, open WS connection. Send authorization frame first:
```
authorize\n0\n\n{"accessToken":"<token>"}
```

Then subscribe to user data:
```
user/syncrequest\n1\n\n{"users":[<userId>]}
```

User data includes positions, orders, fills, cash balances — real-time updates.

Market data WS is separate (`md.tradovateapi.com`) — subscribe to `md/subscribequote` for quotes, `md/subscribeDOM` for depth-of-market.

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 200 | OK | proceed |
| 400 | Bad order params (qty, price tick, contract expired) | surface to operator |
| 401 | Token expired or invalid | refresh via `/auth/renewaccesstoken` |
| 403 | Account permission denied | operator action needed |
| 429 | Rate limit | exponential backoff |
| 500-599 | Tradovate server | exponential backoff, surface after 3 retries |

## Reversibility per endpoint

All `/order/*` write endpoints + `/order/liquidateposition` are N. Fills happen in milliseconds, no "undo." Operator-confirm gate is mandatory.

All `/account/list`, `/position/list`, `/order/list`, `/fillFee/list`, `/cashBalance/list`, `/marginSnapshot/list` are Y — agents read autonomously.

## Notes for first-use

1. Verify live docs at https://api.tradovate.com/
2. Confirm demo credentials work with a smoke `/auth/accesstokenrequest`
3. Implement `client.py` modeled on `.claude/connectors/perplexity/client.py`
4. Add the operator-confirm gate decorator around every N-class call
5. Wire token refresh background task (60-min default refresh cadence)
6. For WebSocket: use `websockets` Python lib, heartbeat every 30s to keep connection alive
7. Risk-rule precheck: BEFORE calling `/order/placeorder`, validate against `agents/trading-analyst/memory/risk_rules.md` (max contracts, daily loss limit not exceeded)
