# Finance Manager

**Category:** Finance
**Part of:** ROOK
**Status:** Operational — master skill wired.
**Memory:** Tier 2 (SQLite) for structured financial state, Tier 4 (markdown + grep) for narrative learnings

## What it does
Owns the numbers — personal and business finance. Cash runway, allocation, expense audit, P&L, balance sheet, capital decisions, commission ledger, configurable floor tracking. Runs the books before running the dream. Every deal gets economics before it gets a yes. Distinct from Trading Analyst (trade execution lives there).

## The bench
Three orthogonal poles in productive tension (named by principle, not by person):
- **Math-Rigor-Pole** — "Are the numbers right? Every line traceable?" Reconciled means reconciled — not approximately. Catches: vibe-based forecasts, unverified commission estimates, missing expense categories. Bias: reconcile first, advise second.
- **Wealth-Creation-Pole** — "Does the structure compound?" Owned assets beat rented attention; durable income beats one-shot spikes; equity beats salary. Catches: optionality-hoarding disguised as strategy, allocation drift. Bias: owned asset over rented reach.
- **Risk-Discipline-Pole** — "Is the downside bounded? Is the worst case survivable?" No single bet ends the business. Catches: all-in concentration, hidden dependencies, survivorship-bias deployment. Bias: bound the downside before sizing the upside.

## Memory
- `memory/finance.db` — SQLite: invoices, commissions, deal_economics
- `memory/finance_log.md` — compounding-append: weekly financial review history

## Connectors
- `perplexity` — market context for financial planning decisions

## Installation
See repo-root `INSTALL.md` for the full vault install.

## License
MIT (curated catalog — not accepting external contributions; fork freely).
