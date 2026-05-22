# Charles Schwab connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (Trader API, OAuth 2.0).
**Use case:** Equities + options + ETF trading via Schwab Trader API. Thinkorswim is Schwab's trading platform — the API is the programmatic backend for it. For futures, use `tradovate` connector instead.

## Consumers
- `trading-analyst` (equity + options strategy execution, position queries, options chain reads)
- `finance-manager` (account balance + P&L for wealth-creator-mode evaluator)

## Integration kind
API-direct (Schwab Trader API). OAuth 2.0 with authorization code flow + refresh tokens. Requires Schwab Developer Portal app registration.

## Credentials
- `SCHWAB_APP_KEY` — client ID from https://developer.schwab.com/
- `SCHWAB_APP_SECRET` — client secret from developer portal
- `SCHWAB_CALLBACK_URL` — OAuth redirect URI registered with the app (e.g., `https://127.0.0.1:8182/`)
- `SCHWAB_REFRESH_TOKEN` — operator-issued refresh token (7-day lifetime, requires re-auth weekly)
- `SCHWAB_ACCESS_TOKEN` — short-lived bearer (30-min lifetime, refresh via refresh token)
- Stored at `~/.claude/credentials/schwab.json`

Token refresh: access tokens last 30 minutes; refresh tokens last 7 days. Operator must complete browser-based OAuth dance weekly to mint a new refresh token. There is no fully unattended refresh — this is a Schwab regulatory choice, not an oversight.

## Reversibility class
- **Y (reversible)**: account list, positions, orders history, market data, options chains, transactions history, movers, quote
- **N (irreversible)**: place order, replace order, cancel order, move funds

Operator-confirm gate mandatory on all N-class endpoints.

## Operator setup checklist
- [ ] Schwab brokerage account funded (live trading)
- [ ] Developer portal account at https://developer.schwab.com/
- [ ] "Individual Developer" app created (free tier covers most operator use)
- [ ] App approved by Schwab (typically 1-2 weeks for live data + trading access)
- [ ] App key + secret stored at `~/.claude/credentials/schwab.json`
- [ ] OAuth callback URL configured (HTTPS required; localhost OK for dev)
- [ ] First OAuth dance completed → refresh token captured
- [ ] Weekly refresh-token-renewal reminder added to chief-of-staff cadence
- [ ] Smoke test: `GET /accounts/accountNumbers` → expect account list
- [ ] Operator-confirm gate verified BEFORE any order placement
- [ ] Risk limits configured in `agents/trading-analyst/memory/risk_rules.md` (max share count per order, daily loss limit, no naked-options gate)

## Thinkorswim relationship

Thinkorswim is Schwab's desktop/web trading platform UI. It uses the same Schwab account backend the Trader API exposes. **You don't connect to Thinkorswim via this API** — you connect to Schwab, and Thinkorswim is one UI on top of the same brokerage account. Positions placed via this connector appear in Thinkorswim and vice versa.

If the operator uses Thinkorswim for visual chart-based discretionary trading + ROOK for systematic execution, the two coexist on the same account.

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
- Schwab acquired TD Ameritrade in 2023; the legacy TD Ameritrade API was retired 2024. Use ONLY the new Schwab Trader API — do not reference TDA docs.
