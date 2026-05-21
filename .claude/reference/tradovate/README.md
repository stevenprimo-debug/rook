# Tradovate connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (REST + WebSocket).
**Use case:** Futures trading. Tradovate is a futures-only broker (CME, CBOT, NYMEX, COMEX). For equities/options use `schwab` connector.

## Consumers
- `trading-analyst` (live + paper futures execution, position queries, P&L reads)
- `finance-manager` (account balance, margin status, daily P&L for the wealth-creator-mode evaluator)

## Integration kind
API-direct (Tradovate REST API + WebSocket for market data). Two environments:
- **Demo / paper**: `demo.tradovateapi.com` — paper account, free
- **Live**: `live.tradovateapi.com` — funded futures account required

## Credentials
- `TRADOVATE_USERNAME` — operator's Tradovate login
- `TRADOVATE_PASSWORD` — operator's Tradovate password
- `TRADOVATE_APP_ID` — application identifier (operator-named, e.g., "rook-trading-analyst")
- `TRADOVATE_APP_VERSION` — semver, e.g., "1.0.0"
- `TRADOVATE_CID` — client ID (issued by Tradovate when API access is granted)
- `TRADOVATE_SEC` — client secret
- `TRADOVATE_ENV` — `demo` or `live` (default: `demo`)
- Stored at `~/.claude/credentials/tradovate.json`

Auth flow: POST to `/auth/accesstokenrequest` with the above credentials → receive bearer token + ~80-minute expiry. Token MUST be refreshed before expiry (background refresh task).

## Reversibility class
- **Y (reversible)**: account list, position list, order list, market data (REST + WS), instrument search, fills history
- **N (irreversible)**: place order, modify order, cancel order (technically irreversible — fills happen in milliseconds), liquidate position

The default operating mode for ROOK trading-analyst is **paper / demo**. Live trading requires explicit operator opt-in per account, and EVERY order placement requires operator-confirm gate — even on demo, because the muscle memory transfers.

## Operator setup checklist
- [ ] Tradovate demo account created at https://www.tradovate.com/
- [ ] API access requested — Tradovate issues CID/SEC after review (typically 1-3 business days)
- [ ] All env vars set OR `~/.claude/credentials/tradovate.json` populated
- [ ] `TRADOVATE_ENV=demo` confirmed for first run
- [ ] Smoke test: `POST /auth/accesstokenrequest` → expect 200 with `accessToken` and `userId`
- [ ] List positions on empty demo account: `GET /position/list` → expect `[]`
- [ ] Operator-confirm gate verified BEFORE any `/order/placeorder` call
- [ ] Token refresh background task wired (auto-refresh 5 min before expiry)
- [ ] Risk limits configured in `agents/trading-analyst/memory/risk_rules.md` (max contracts per order, daily loss limit)

## Live-trading gate (separate from operator-confirm)

Before flipping `TRADOVATE_ENV=live`, the operator must:
1. Verify at least 30 days of demo trading following the same strategy
2. Confirm the strategy's max drawdown observed in demo is within risk tolerance
3. Update `agents/trading-analyst/memory/risk_rules.md` with live-account-specific limits
4. Add a `live_trading_enabled: true` flag to operator's Tradovate config

ROOK trading-analyst defaults to refusing live execution until this flag is set.

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
- TradingView webhook → Tradovate order is the canonical N-gated pipeline; see `.claude/connectors/tradingview/README.md` for the alert-staging pattern.
