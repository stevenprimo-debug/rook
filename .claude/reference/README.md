# `.claude/reference/` — shared API + library reference shelf

Vault-level reference docs that ANY agent can load on demand. Distinct from `.claude/connectors/` (which has credentials + operational `client.py`). Reference is just docs: API contracts, library introductions, getting-started guides.

## Why vault-level (not per-agent)

The whole point of load-on-demand context is one canonical static shelf that ALL agents can read. Putting API docs under `agents/<one-agent>/context/` creates a cross-agent-read awkwardness — when finance-manager needs the Tradovate API doc that trading-analyst owns, it has to know to look in another agent's folder. That breaks the pattern.

Shared reference = one source of truth. Librarian organizes; every agent reads.

## What's here

The shelf is organized by **category of reference**, not by consuming agent. Every category is readable by every agent — that's the whole point.

### API & library references

| Service | Scope | Primary consumers |
|---|---|---|
| `tradingview/` | TradingView Advanced Charts library — full official doc set (intro, getting-started, connecting-data, widget-constructor, widget-methods, ui-elements, api-reference, datafeed-api, module-datafeed, trading-platform-methods, best-practices, build-ai-library-assistant) — 13 files | trading-analyst, r-and-d-lead, designer, software-dev-team |
| `tradovate/` | Tradovate futures broker — REST + WebSocket API | trading-analyst, finance-manager |
| `schwab/` | Charles Schwab Trader API (equities/options; Thinkorswim is the UI on top) | trading-analyst, finance-manager |

### Document & contract templates

| Category | Scope | Primary consumers |
|---|---|---|
| `templates/nda/` | NDAs, confidentiality agreements | sales-director, shopify-agent, r-and-d-lead, account-manager |
| `templates/contracts/` | Software dev agreements, SaaS licenses, MSAs | sales-director, account-manager, finance-manager |
| `templates/sow/` | Statement of Work templates | sales-director, account-manager |
| `templates/saas/` | YC-form SaaS subscription agreements | sales-director, finance-manager |
| `templates/partnerships/` | Partnership agreements (placeholder) | sales-director, chief-of-staff |

See `templates/README.md` for full inventory + usage rules.

## Pattern (per `_CLAUDE.md` § 0 rule #12)

When any agent is about to use one of these services:

1. Read `<service>/README.md` for setup, reversibility classes, integration touchpoints
2. Read `<service>/api-reference.md` (if present) for endpoint shapes, auth flow, error handling
3. Verify against the live docs URL at the top of each `README.md` (these snapshots may go stale)
4. Implement client code that respects the reversibility gates documented per endpoint
5. Add the operator-confirm gate decorator around every N-class call

## Distinction from `.claude/connectors/`

| Surface | What it contains | Has credentials? | Has `client.py`? |
|---|---|---|---|
| `.claude/connectors/<service>/` | MCP-backed OR clean-REST services with shared creds (Gmail, Cal.com, Stripe, HubSpot) | Yes (centralized) | Often yes |
| `.claude/reference/<service>/` | API references + library docs for services without MCP and without shared client (TradingView, Tradovate, Schwab) | No — operator-credential, per-agent auth flow | No — agents write per-use client code |

Egress for `reference/` services is still allowlisted at the runtime layer — see `.claude/connectors/_egress-allowlist.md` § "Agent-implemented API surfaces".

## Adding a new reference

1. `mkdir .claude/reference/<service>/`
2. Write `README.md` (scope, integration touchpoints, consumers, status) and optionally `api-reference.md` (endpoint table)
3. Add the egress row to `.claude/connectors/_egress-allowlist.md` § "Agent-implemented API surfaces"
4. Librarian sweeps the shelf into the master index on next run

## Librarian responsibility

The librarian agent owns shelf organization: dedup-checking when new references arrive, flagging stale snapshots (timestamp older than 6 months → review against live docs), and surfacing cross-service patterns (e.g., "Tradovate and Schwab both use OAuth with weekly refresh ceremonies — codify the pattern").
