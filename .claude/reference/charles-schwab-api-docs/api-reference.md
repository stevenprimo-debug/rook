# Charles Schwab Trader API — agent-facing reference

**Status:** stub — verify against https://developer.schwab.com/products/trader-api--individual on first connector use.
**Base URL:** `https://api.schwabapi.com`

## Authentication

OAuth 2.0 authorization code flow:

1. Operator visits authorization URL: `https://api.schwabapi.com/v1/oauth/authorize?client_id=<APP_KEY>&redirect_uri=<CALLBACK>&response_type=code`
2. Schwab redirects to callback with `?code=<auth_code>` (URL-encoded)
3. POST `/v1/oauth/token` with `grant_type=authorization_code`, `code=<auth_code>`, `redirect_uri=<CALLBACK>`, basic auth header `Authorization: Basic base64(APP_KEY:APP_SECRET)` → receive access token (30 min) + refresh token (7 days)
4. For subsequent requests: `Authorization: Bearer <access_token>`
5. Before access token expires: POST `/v1/oauth/token` with `grant_type=refresh_token`, `refresh_token=<rt>` → new access token
6. Before refresh token expires (7 days): operator must redo the full browser flow

## Endpoints

### Account & trading

| Endpoint | Method | Purpose | Reversibility |
|---|---|---|---|
| `/trader/v1/accounts/accountNumbers` | GET | List operator's account numbers (hashed) | Y |
| `/trader/v1/accounts` | GET | List accounts with positions | Y |
| `/trader/v1/accounts/{accountHash}` | GET | Read one account detail | Y |
| `/trader/v1/accounts/{accountHash}/orders` | GET | List orders for account | Y |
| `/trader/v1/accounts/{accountHash}/orders` | POST | **Place new order** | **N** |
| `/trader/v1/accounts/{accountHash}/orders/{orderId}` | PUT | **Replace order** | **N** |
| `/trader/v1/accounts/{accountHash}/orders/{orderId}` | DELETE | **Cancel order** | **N** |
| `/trader/v1/accounts/{accountHash}/transactions` | GET | Transaction history | Y |
| `/trader/v1/orders` | GET | List orders across all accounts | Y |
| `/trader/v1/userPreference` | GET | Read user preferences (default account, etc.) | Y |

### Market data

| Endpoint | Method | Purpose | Reversibility |
|---|---|---|---|
| `/marketdata/v1/{symbol}/quotes` | GET | Quote for one symbol | Y |
| `/marketdata/v1/quotes` | GET | Batch quotes (comma-separated symbols) | Y |
| `/marketdata/v1/chains` | GET | Options chain | Y |
| `/marketdata/v1/expirationchain` | GET | Options expiration dates | Y |
| `/marketdata/v1/pricehistory` | GET | Historical OHLC bars | Y |
| `/marketdata/v1/movers/{index}` | GET | Top movers ($SPX, $DJI, etc.) | Y |
| `/marketdata/v1/markets` | GET | Market hours | Y |
| `/marketdata/v1/instruments` | GET | Instrument lookup by symbol/CUSIP | Y |

## Order payload (N — operator confirm required)

```json
{
  "orderType": "MARKET" | "LIMIT" | "STOP" | "STOP_LIMIT",
  "session": "NORMAL" | "AM" | "PM" | "SEAMLESS",
  "duration": "DAY" | "GOOD_TILL_CANCEL" | "FILL_OR_KILL",
  "orderStrategyType": "SINGLE" | "OCO" | "TRIGGER",
  "price": "150.00",
  "orderLegCollection": [{
    "instruction": "BUY" | "SELL" | "BUY_TO_OPEN" | "SELL_TO_CLOSE",
    "quantity": 100,
    "instrument": {
      "symbol": "AAPL",
      "assetType": "EQUITY" | "OPTION" | "ETF"
    }
  }]
}
```

Options legs use `assetType: "OPTION"` and the OSI-format symbol (e.g., `AAPL  260620C00150000`).

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 200 | OK | proceed |
| 201 | Order accepted (placement success) | proceed; poll order status for fill |
| 400 | Bad order (price tick, insufficient buying power, market closed) | surface to operator |
| 401 | Access token expired | refresh via `/v1/oauth/token` |
| 403 | Account permission denied (e.g., options level too low) | operator action needed |
| 404 | Resource not found | confirm account hash / order ID |
| 429 | Rate limit (120 req/min default) | exponential backoff 1s, 2s, 4s |
| 500-599 | Schwab server | exponential backoff, surface after 3 retries |

## Reversibility per endpoint

All `POST /orders`, `PUT /orders/{id}`, `DELETE /orders/{id}` are N. Cancel is N because by the time cancel is sent, fills may have occurred. Operator-confirm gate mandatory.

All `GET` endpoints are Y — agents read autonomously.

## Notes for first-use

1. Verify live docs at https://developer.schwab.com/products/trader-api--individual
2. Complete OAuth dance manually first time; capture refresh token
3. Implement `client.py` with bearer-token rotation built-in (refresh 5 min before expiry)
4. Add the operator-confirm gate decorator around every N-class call
5. For options: respect the operator's approved options level (level 2 vs 3 vs 4) — refuse to place orders that exceed it
6. Pre-market / after-hours: only enable `session: "AM"` / `"PM"` / `"SEAMLESS"` after explicit operator opt-in
7. Wire weekly refresh-token-renewal reminder into chief-of-staff Monday cadence
