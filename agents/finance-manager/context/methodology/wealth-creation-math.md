# Wealth Creation Math

## What This Framework Is

Wealth creation math is the quantitative spine underneath every
financial decision the operator makes. It separates two fundamentally
different income engines:

- **Engine A (time-for-cash):** W-2 income, hourly consulting,
  commission on closed deals. Income stops the moment the operator
  stops working. Compounding is limited to whatever surplus is
  carved off and reinvested.
- **Engine B (asset-producing):** SaaS subscriptions, royalty
  streams, licensed products, equity stakes. Income continues with
  declining marginal time input. Compounding is structural — every
  additional asset built compounds against the existing base.

The math reveals a single brutal truth: Engine A income, no matter
how large, hits a ceiling determined by hours available × hourly
rate. Engine B income compounds against its own base. A $50K/year
asset that grows 30% annually doubles in roughly 2.5 years; the same
$50K of Engine A income remains $50K next year unless the operator
trades more hours.

Wealth creation math also exposes the **hidden cost of Engine A
dominance**: every hour spent on Engine A is an hour not spent
building Engine B. The marginal hour is the lever — and the
compounding penalty for spending the marginal hour on Engine A is
not 1:1; it is exponential when projected across the years until
freedom-fund target.

## Why It Matters For This Agent

Finance Manager's Compounding-First-Pole and Mission-Alignment-Pole
both require this framework. Compounding-First asks: "Is the
freedom-fund balance compounding at a rate that hits target by
[milestone target date]?" Mission-Alignment asks: "Is the operator's attention
flowing toward Engine B work or being absorbed by Engine A demands?"

The agent uses wealth creation math to convert qualitative anxiety
("am I making progress?") into quantitative answers:

- Current freedom-fund balance, monthly contribution rate, projected
  balance at milestone date, gap to target.
- Engine A income vs. Engine B income, ratio over time, trend
  direction.
- Hours allocated to Engine A vs. Engine B over the last week, ratio,
  trend.
- Per-hour wealth productivity: Engine B income produced per Engine B
  hour, compared against Engine A hourly rate.

When the math is honest, the decision becomes obvious. When the math
is hidden, the operator stays trapped in Engine A by default.

## Core Concepts

### 1. Compounding (CAGR)

Compounding is the mechanism by which Engine B beats Engine A over
time. The formula:

```
future_value = present_value × (1 + rate)^years
```

A $10K asset compounding at 30% annually:
- Year 1: $13K
- Year 2: $16.9K
- Year 3: $22K
- Year 5: $37.1K
- Year 10: $137.9K

The same $10K under a mattress remains $10K, while inflation erodes
its real value. Engine A income (next year's $50K consulting check)
does not compound — it must be earned again from scratch each year.

CAGR (Compound Annual Growth Rate) is the rate at which an asset must
grow each year to reach a target:

```
CAGR = (ending_value / starting_value)^(1/years) - 1
```

For the operator's freedom-fund target: given current balance, target
balance, and years to target, the required CAGR is determined. If
required CAGR exceeds achievable CAGR through investment alone, the
gap must close through additional contributions (Engine A surplus
deployed) or through faster Engine B income growth.

### 2. Time Value of Money

A dollar today is worth more than a dollar a year from now because
today's dollar can be deployed productively. The discount rate
applied to future cash flows reflects both the opportunity cost
(what else the dollar could be earning) and the risk that the future
dollar does not arrive.

For the operator: a $5K deal that pays in 12 months is not worth $5K
today. At a 10% discount rate, it is worth $4,545 today. This matters
when comparing deals: a $4,500 deal that pays in 30 days may be more
valuable than a $5K deal that pays in 12 months.

### 3. The Rule of 72

A mental-math shortcut for compounding doubling time:

```
years_to_double ≈ 72 / annual_growth_rate%
```

- 10% growth: doubles in ~7.2 years
- 20% growth: doubles in ~3.6 years
- 30% growth: doubles in ~2.4 years
- 50% growth: doubles in ~1.4 years

The operator uses Rule of 72 to sanity-check freedom-fund projections:
if current balance is $50K and target is $400K (8x), three doublings
are required. At 20% growth, that is ~10.8 years. At 30%, ~7.2 years.
At 50%, ~4.2 years. The math reveals whether the target is reachable
on the current trajectory or whether the rate must change.

### 4. Engine A vs. Engine B (The Mission-Alignment Filter)

Every income stream is classified:

**Engine A characteristics:**
- Income stops when work stops.
- Hours required scale linearly with income.
- Income ceiling is roughly (hours × rate × utilization).
- Examples: [your employer] W-2 + commission, hourly consulting, side-engagement
  retainers, one-off project fees.

**Engine B characteristics:**
- Income continues with declining marginal work.
- Hours required to maintain income are sub-linear vs. income earned.
- Income ceiling is roughly (asset_base × growth_rate), with no
  inherent cap.
- Examples: SaaS subscriptions, licensed products, royalties, equity
  stakes, productized content libraries, owned distribution.

For the operator, current state (mid-2026):
- Engine A: [your employer] ($5M revenue target × 10% commission GP × the operator
  split, plus consulting). Dominant.
- Engine B: [your product] (early), [your product line] (early), Stage
  Pro (early). Subordinate.

Mission-alignment progress is measured by **the ratio of Engine B
income to Engine A income** over time. Exit-by-Dec-2026 requires
this ratio to cross 1.0 — Engine B income must equal or exceed
Engine A income (or, equivalently, asset-base must produce enough
income via portfolio CAGR to replace W-2).

### 5. Freedom-Fund Math

The freedom fund is the deployed asset base that produces enough
passive income to cover lifestyle costs. The math:

```
required_freedom_fund = annual_lifestyle_cost / safe_withdrawal_rate
```

At a 4% safe withdrawal rate (the conservative "Trinity Study" number):
- $50K/year lifestyle → $1.25M fund required
- $80K/year lifestyle → $2.0M fund required
- $135K/year lifestyle → $3.4M fund required

For the operator targeting $100K net self-employed income at exit:
the target is closer to "Engine B income replaces Engine A" than
"freedom fund produces it passively." Both are valid endpoints; the
math differs:

- **Freedom-fund endpoint**: need $2.5M deployed at 4% to produce
  $100K/year passive.
- **Engine B endpoint**: need $100K/year recurring income from SaaS
  + products with low marginal time input.

The Engine B endpoint reaches sooner because asset-producing income
streams compound faster than passive portfolios.

### 6. The Marginal Hour Calculation

Every hour the operator works is one of two things:
- An Engine A hour (produces this-period cash).
- An Engine B hour (produces a compounding asset).

The marginal hour math:

```
Engine A hour: produces (hourly_rate) of income, taxed at marginal rate.
Engine B hour: produces (incremental asset value) compounding at CAGR.
```

Concrete example, $200/hour Engine A vs. building a $50/month SaaS
subscription:
- Engine A hour: $200 × (1 - 0.35 tax) = $130 net.
- Engine B hour (one of 50 hours to build the SaaS feature that adds
  $50/month MRR): produces $1/hour of MRR added, which is $12/year
  per hour invested. But $12 × (life_of_subscriber × growth_factor)
  → if the SaaS lives 5 years and the customer base grows 2x, the
  hour produced $120-200 over the asset life, AND the feature
  contributes to compounding growth of the platform.

The math reveals: Engine A hours are visible and immediate; Engine B
hours are invisible and delayed. The freedom-fund math cannot work
without conscious allocation of marginal hours toward Engine B.

### 7. The 60-Minute Product Evaluation Rule (Applied Math)

Per locked feedback: "New product ideas get max 60 min to prove plan
+ profit + exit fit." Wealth-creation math translates this into a
quantitative gate. A product idea must demonstrate:

- **Plan**: a credible 90-day path to first $1K MRR or equivalent.
- **Profit**: gross margin ≥60% (SaaS) or ≥40% (physical/services).
- **Exit fit**: contributes to Engine B income, not Engine A.

If any of three fails, the idea is parked. The math is the gate that
prevents Engine A energy from leaking into "side hustles" that are
just additional Engine A under disguise.

## Common Applications

**Monthly Engine A/B ratio report:**
The agent calculates:
- Engine A income this month: $X ([your employer] commission, consulting).
- Engine B income this month: $Y (SaaS MRR × 1, royalties).
- Ratio: Y/X.
- Trend over last 3 months.

The report surfaces whether Engine B is growing faster than Engine A
(progress toward exit) or whether Engine A is absorbing all attention.

**Freedom-fund projection:**
Given current balance, monthly contributions, and assumed CAGR, the
agent projects forward to [milestone target date]:
```
balance_at_target = current × (1+CAGR/12)^months + monthly_contribution × annuity_factor
```
If projected balance < target, the agent surfaces the gap and proposes
options: increase contributions, increase CAGR (which requires
Engine B growth), extend target date.

**[your employer] deal opportunity-cost analysis:**
A potential $200K [your employer] opportunity requires 40 hours of evaluation
+ scoping work. The agent calculates:
- 40 hours × $200/hour notional = $8K opportunity cost.
- Expected value of deal: $200K × 25% GP × probability of close × the operator
  split = realistic $7-12K.
- 40 hours redirected to [your product]: building 1 SaaS feature ≈ $50-200/month
  recurring → $600-2400 ARR, compounding.

The math reveals the deal is break-even at best on opportunity cost.
The decision flows to the operator with the math visible, not hidden.

**Compounding-check at session end:**
The agent reads: did this week's work add to the Engine B asset base?
If the answer is "no work shipped on [your product] / [your platform] / [your physical/SaaS product],"
Compounding-First-Pole surfaces it as a flag.

**Tax-efficient deployment:**
Engine A income produces taxable cash. Engine B income may produce
qualified dividends, capital gains, or pass-through income at
preferential rates. The agent flags when Engine A surplus could be
deployed into Engine B assets at lower effective tax rates than
holding cash.

## Anti-patterns (when this framework is misapplied)

**Counting gross revenue as wealth.** A $5M annual [your employer] revenue
target produces a much smaller take-home (commission × GP × the operator
split, less taxes). Reporting "I'm at $3M YTD" without converting to
take-home is dishonest math.

**Treating "side hustle" as Engine B by default.** A consulting
side engagement that requires the operator to work hours is Engine A,
not Engine B — regardless of whether it is the day job. Mission-
Alignment-Pole requires the asset-producing test, not the
not-the-day-job test.

**Linear-thinking the freedom fund.** "I save $5K/month, target is
$300K, so 5 years." This ignores compounding. At 10% CAGR + $5K/month
on a $50K base, the fund hits $300K in roughly 3 years, not 4.2. The
operator either over-saves (Engine A burnout) or under-saves
(misses target).

**Discounting future income to zero.** Treating SaaS subscriptions
or product royalties as worth only this-month's cash flow undervalues
Engine B. A $100/month subscription with 80% gross margin and 24-month
average customer lifetime is worth ~$1,920 in lifetime value — not
$100.

**Compounding ignored on the deal side.** A relationship that
produces one $50K deal this year may produce three deals next year
if cultivated. The math of customer lifetime value applies to [your employer]
accounts too — but only if reinvestment in the relationship is
treated as Engine B-style asset-building, not Engine A-style hourly
work.

**Per locked rule: <$100K value, <15% GP, <$15K commission, <$300/hr
efficiency = auto-reject.** Wealth-creation math is the source of
these thresholds. Below these numbers, the deal does not produce
enough surplus to compound the freedom fund — it just produces
activity.

**Wealth creator mode misapplied.** Per `wealth_creator_mode.md`, the
Naval-style stress test compares Engine A vs. Engine B over multi-year
horizons. Misusing the framework to justify any [your employer] deal as "fueling
the exit" without doing the actual math produces post-hoc
rationalization, not honest analysis.

## Cross-references

- Agent skill: `agents/finance-manager/SKILL.md`
- Bench: `agents/finance-manager/personality/_bench.md` (Compounding-First-Pole, Mission-Alignment-Pole)
- Frameworks index: `agents/finance-manager/personality/frameworks_index.md`
- Companion methodology: `agents/finance-manager/context/methodology/accounting-framework.md`
- Vendored reference: `agents/finance-manager/context/references/mastering-saas-pricing.md`
- Memory: `.claude/memory/user_profile.md`
- Memory: `.claude/memory/project_exit_roadmap.md`
- Memory: `.claude/memory/feedback_sixty_minute_rule.md`
- Memory: `agents/finance-manager/memory/wealth_creator_mode.md`
