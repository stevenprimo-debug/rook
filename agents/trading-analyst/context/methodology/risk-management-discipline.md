# Risk Management Discipline

## What This Framework Is

Risk management discipline is the operating system every trader runs
underneath whatever methodology generates the setups. ICT names the
trade; risk management determines whether the trade survives long enough
to matter. The framework reduces to three measurable rules: a fixed
maximum loss per trade (the 1% rule), a fixed maximum loss per day (the
3% rule), and a stop-before-entry sequencing rule that prevents the
single most common failure mode in retail trading — placing the stop
after the position has already moved.

The discipline is not about generating wins. It is about surviving the
losses. A trader who survives drawdowns long enough to compound a 55%
win rate at 2:1 reward-to-risk wins. A trader who blows up at the third
losing streak does not, regardless of methodology fluency.

The math: position size is not chosen — it is derived. Risk per trade
is a constant (1% of book, ceiling). Stop distance is determined by the
named setup's structural boundary. Size flows out of these two inputs:

```
position_size = (book_equity × risk_per_trade%) / (entry_price - stop_price)
```

Everything else — what feels reasonable, what other traders are doing,
how confident the trader feels — is noise that the equation refuses to
let in.

## Why It Matters For This Agent

Trading Analyst's Risk-1%-Pole is the discipline pole. Where Setup-Rigor
gates on whether the setup is named, Risk-1% gates on whether the
position survives. The pole catches three specific failure modes:

1. **Unsized entries** — the operator names a setup but never specifies
   risk, then asks "how much should I buy?" Risk-1% inverts the question:
   risk first, size second.

2. **Moved stops** — the position moves against the operator, who then
   widens the stop "to give it room." The pole refuses: stops widen only
   by plan, never under stress.

3. **Position stacking past the daily limit** — three losing trades in a
   row push the book past 3% daily drawdown; the operator wants one more
   to "make it back." The pole refuses: 3% triggers stop-trading-for-the-day.

The Posture-Current-Pole adjusts the 1% number based on regime: in high-
vol regimes, risk-per-trade may step down to 0.5%; in tight, quiet
regimes, 1% is the ceiling that should rarely be hit. The discipline
adapts; the ceiling does not.

## Core Concepts

### 1. The 1% Rule (Per-Trade Risk Ceiling)

No single position risks more than 1% of book equity. On a $50K book,
maximum loss per trade is $500. The 1% is not a target — it is a
ceiling. Lower-conviction setups risk 0.5%. Higher-conviction setups
do not exceed 1%; the temptation to "go bigger on the certain one" is
exactly the temptation that produces account-ending losses, because the
"certain one" is the one the trader stopped scrutinizing.

Why 1%: at a 50% win rate and 2:1 reward-to-risk, the trader gains 0.5%
per trade on average. At 1% risk, this compounds. At 5% risk, a six-trade
losing streak (probability roughly 1 in 64) drops the book by 30% — and
the math of recovery from 30% drawdown is a 43% gain, which most traders
do not reliably produce. The 1% rule sets the floor so that losing
streaks are survivable.

### 2. The 3% Daily Drawdown Limit

Cumulative loss across all trades in a single day cannot exceed 3% of
book equity. If three trades each risk 1% and all three lose, the day
ends — regardless of how appealing the next setup looks. The 3% rule
exists because losing days produce **tilt** — emotional state where
judgment degrades, where the trader chases revenge entries, where the
setup quality required to stop the bleed is exactly the setup quality
the tilted trader cannot recognize.

The agent surfaces daily P&L on every entry audit. If the day has
already taken two 1% losses and the operator proposes a third trade,
the agent's audit will note: "current daily drawdown: -2.0%; one more
loss hits the 3% limit; setup conviction must be elevated."

### 3. Stop-Before-Entry Sequencing

The stop is set before the position is taken — not after. This is the
single most violated rule in retail trading and the single most powerful
discipline once enforced. The mechanism is procedural:

1. Identify the named setup.
2. Identify the structural stop (far side of order block, beyond fair
   value gap, below swing low).
3. Calculate position size from (book × 1%) / (entry - stop).
4. Submit the entry order AND the stop order together.

Without stop-before-entry, the position has no defined risk and the
trader cannot lose discipline because they had no discipline to lose.
A position without a stop is not a trade — it is an investment, with
infinite downside.

### 4. Size-Flows-From-Risk

Position size is an output, not an input. The math:

```
risk_dollars = book_equity × risk_per_trade%
stop_distance = entry_price - stop_price  (for longs)
position_size = risk_dollars / stop_distance
```

Concrete example, $50K book, 1% risk, long entry $5142, stop $5128:
- risk_dollars = $50,000 × 0.01 = $500
- stop_distance = $5142 - $5128 = $14
- position_size = $500 / $14 = 35.7 contracts → 35 contracts

The trader does not get to ask "is 35 the right size?" The math
determined 35 is the right size given the constraint that no trade
exceeds 1% loss.

### 5. Reward-to-Risk Minimum (R:R)

Minimum acceptable R:R is 1.5:1; preferred is 3:1+. Below 1.5:1, the
trade requires a >67% win rate just to break even, which most setups
do not produce. The math:

```
breakeven_win_rate = 1 / (1 + R:R)
```

- 1:1 R:R → 50% win rate to break even
- 1.5:1 R:R → 40% win rate to break even
- 2:1 R:R → 33% win rate to break even
- 3:1 R:R → 25% win rate to break even

Higher R:R setups produce profit at lower win rates. The agent flags
any setup with R:R below 1.5 — not because the trade cannot work, but
because the math is fighting the trader before the trade even fires.

### 6. Moved-Stop Refusal

Once the stop is set, it widens only by plan — never under stress. Two
acceptable adjustments:

- **Trail to break-even** after first target hit (locks in zero-loss).
- **Trail to lock partial profit** as price extends.

One unacceptable adjustment: **widening the stop because price is
approaching it**. This is the single trade behavior that converts 1%
losses into 5% losses. The agent's audit refuses any "move stop wider"
request.

### 7. Correlation Risk

Three open positions all long-correlated assets (SPY + QQQ + NVDA) are
not three 1% risks — they are one 3% risk on a single market direction.
The Risk-1%-Pole reads correlation across the open book and flags
concentration. Maximum effective book risk at any time should not exceed
4-5% across all open positions.

## Common Applications

**Pre-entry size calculation:**
Operator: "Long NQ here, stop below 18420."
Agent: "Book $50K, risk 1% = $500. Entry 18445, stop 18420, distance
25 pts. NQ point value $20 → $500 risk / ($20 × 25) = 1 contract.
Sized: 1 NQ. Verdict: go."

**Daily drawdown gate:**
Operator on 4th trade attempt: "Long ES here."
Agent: "Daily P&L: -2.4%. One more 1% loss hits the 3.4% ceiling above
the 3% daily limit. This setup must clear elevated bar: name the setup,
confluence ≥3, R:R ≥2.5. If not, defer to tomorrow."

**Stop-widen refusal:**
Operator: "Price is testing my stop, I'm moving it down to give it room."
Agent: "Refusing. Moved-stop discipline: stops widen only by plan, never
under stress. Current behavior is converting a 1% loss into a 2% loss.
Two options: exit now at planned stop, or accept the trade is invalidated
and step away from the screen."

**Correlation audit:**
Operator: "Adding QQQ long here."
Agent: "Current book: long SPY 1% risk, long NVDA 1% risk. Adding QQQ
long stacks 3% effective risk on single-direction equity beta. Either
size QQQ to 0.5% or close SPY first to maintain ≤2% effective risk."

**R:R audit:**
Operator: "Long here, target +5 pts, stop -8 pts."
Agent: "R:R = 5/8 = 0.6. Below 1.5 minimum. Breakeven win rate required:
62%. This setup must historically produce >62% win rate to be net-positive
or be passed. Verdict: pass unless setup history justifies."

## Anti-patterns (when this framework is misapplied)

**Sizing by conviction instead of by stop.** "I'm really confident,
let me go 2%." The 1% is a ceiling, not a slider. Doubling size on
"high conviction" doubles the loss when conviction was wrong — which
is exactly when conviction was overconfidence.

**Mental stops.** "I'll exit if it gets there." Mental stops are not
stops. They are intentions that fail under stress. The order is placed
or the stop does not exist.

**Averaging down on losing positions.** "Adding here, it has to bounce."
The agent refuses. Averaging down is moving the effective stop wider
while increasing size — the worst possible action structurally.

**Skipping the math.** "I'll figure out size after I see how it moves."
The position is sized before entry or there is no entry. Size derived
post-hoc is size that absorbed the first move against — which becomes
the loss the trader did not budget for.

**Compounding through the drawdown.** "I lost 2% today, so I need to
make it back by sizing up the next trade." Per the locked anti-pattern
list: "'Just one more trade' after daily drawdown limit hit." The day
ends at 3%. Tilt-recovery happens overnight, not in the next bar.

**Tight stops to enable large sizes.** "I'll put the stop super tight
so I can size huge." A tight stop on a setup whose structural risk is
wider is a stop placed in the wrong location — it will get taken by
normal noise. Stop location is determined by the setup, not by the size
the trader wants.

**Investment-advice framing.** Per the locked anti-pattern list and
the agent's standing disclaimer: this is analysis, not investment
advice. Every output includes the disclaimer.

## Cross-references

- Agent skill: `agents/trading-analyst/SKILL.md`
- Bench: `agents/trading-analyst/personality/_bench.md` (Risk-1%-Pole)
- Frameworks index: `agents/trading-analyst/personality/frameworks_index.md`
  (conviction_sizing, cut_when_wrong)
- Companion methodology: [[ict-framework-overview]]
- Vendored reference: `.claude/reference/7-skills-quant-trading-firms.md`
- Vendored reference: `.claude/reference/what-quant-analyst-does.md`
- Memory: `agents/finance-manager/memory/wealth_creator_mode.md`
- Global rule: `~/.claude/CLAUDE.md` (sales auto-reject thresholds — analogous discipline)
