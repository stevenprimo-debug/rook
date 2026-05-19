---
date: 2026-05-14
type: frameworks-index
agent: Finance Manager
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Finance Manager -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Math-Rigor-Pole methodologies

### `profit_first_buckets(revenue)`

**Description:** Allocates revenue to fixed buckets before opex eats it.

**Rule:** Profit is a habit, not an event.

### `inverted_GAAP(business)`

**Description:** Audits whether the business is profitable in cash terms even if not in GAAP terms.

**Rule:** Cash > paper.

### `bank_balance_accounting(account)`

**Description:** Uses actual bank balance as source of truth.

**Rule:** If accounting reports diverge, accounting is wrong.

### `quarterly_distribution(profit)`

**Description:** Enforces quarterly profit distribution.

**Rule:** Distribution makes profit visible.

---

## Wealth-Creation-Pole methodologies

### `three_buckets(net_worth)`

**Description:** Allocates to security / risk-with-known-downside / unbounded-upside buckets.

**Rule:** Three buckets > one bucket.

### `all_seasons_portfolio(allocation)`

**Description:** Audits whether the portfolio survives all 4 economic regimes.

**Rule:** Regime-independence > regime-prediction.

### `dollar_cost_average_check(plan)`

**Description:** Audits DCA cadence; flags timing-the-market behavior.

**Rule:** Cadence > timing.

### `freedom_fund_target(annual_expenses)`

**Description:** Returns the freedom-fund target (typically 25x annual expenses).

**Rule:** 25x = the bar.

---

## Risk-Discipline-Pole methodologies

### `purpose_of_business_check(decision)`

**Description:** Is this decision serving the business's purpose, or capital ego?

**Rule:** Purpose first.

### `effective_capital_allocation(option_set)`

**Description:** Returns the option that creates and keeps a customer fastest.

**Rule:** Customer-velocity > capital-velocity.

### `downside_bound(move)`

**Description:** Names the worst case in dollar terms.

**Rule:** Flag moves with unbounded downside.

---

## Cross-pole methodologies

### `cash_runway_audit(state)`

**Description:** How many months of runway exist.

**Rule:** <12 months = red.

### `wealth_vs_business_capital_split(net_worth)`

**Description:** Audits whether personal wealth is dangerously concentrated in business equity.

**Rule:** Concentration risk is silent until it's loud.


---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the
contract -- what happens inside is the methodology. Output to the user names the
methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (invocation): `../SKILL.md`
