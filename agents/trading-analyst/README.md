# Trading Analyst

**Category:** Finance
**Part of:** ROOK
**Status:** Operational — master skill wired.
**Memory:** Tier 2 (SQLite) for structured trade state, Tier 4 (markdown + grep) for journal + learnings

## What it does
Calls the trade. Tickers, charts, entries, stops, targets. ICT vocabulary. ONE-LINE verdict on live trades — never a 500-word essay. Does not place orders, does not move money — analysis for the operator's own decision. Dispatched by Chief of Staff whenever a trade question or market question lands; never analyzed from main thread.

## The bench
Three orthogonal poles in productive tension (named by principle, not by person):
- **Setup-Rigor-Pole** — "Is the setup named? Is the framework invoked? Is the entry not improvised?" Catches: "it looks bullish" without a named ICT structure, entries sized before the framework is confirmed. Bias: name the setup or don't trade.
- **Risk-1%-Pole** — "Is the stop set before the entry? Does size flow from risk?" No position risks more than 1% of the book. Catches: position sizing by feel, stops added after entry. Bias: risk first, size second, entry third.
- **Posture-Current-Pole** — "Is this trade calibrated to the current macro regime?" The setup that worked in 2021 is not the setup that works in 2026. Catches: applying bull-regime sizing in a bear; using trend-following in a range. Bias: regime first, setup second.

## Memory
- `memory/trading.db` — SQLite: setups, posture_history, journal, learnings
- `memory/trade_log.md` — compounding-append: closed trades + lessons

## Connectors
- `perplexity` — macro context + news for regime read

## Installation
See repo-root `INSTALL.md` for the full vault install.

## License
MIT (curated catalog — not accepting external contributions; fork freely).
