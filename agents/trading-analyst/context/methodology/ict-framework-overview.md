# ICT Framework Overview

## What This Framework Is

ICT — Inner Circle Trader — is a price-action methodology that reframes the
chart through the lens of liquidity, market structure, and institutional
positioning. The premise: retail-style indicator soup (RSI cross, MACD
divergence, moving average bounce) describes what already happened. ICT
describes what is about to happen — where smart-money order flow is
parked, where stops are concentrated, and where price will likely run to
take liquidity before delivering the actual move.

The vocabulary is specific: order blocks, fair value gaps, liquidity
grabs, breaker blocks, market structure shifts, premium and discount
arrays. Each term names a structural feature of the chart, not a derived
indicator. When the agent calls a trade, it names the ICT feature first
and the entry second.

ICT applies most cleanly on liquid, well-traded instruments — index
futures (ES, NQ), major forex pairs (EUR/USD, GBP/USD), major equities
(SPY, QQQ, NVDA), and high-volume crypto (BTC, ETH). It degrades on thin
or news-driven names where price action is structurally less informative.

## Why It Matters For This Agent

Trading Analyst's Setup-Rigor-Pole gates every entry on whether the setup
is **named**. ICT supplies the naming vocabulary. An entry that cannot be
described as "we're long the 4H bullish order block at 5142 after the 1H
fair value gap mitigated, target the unfilled liquidity above 5189" is
not a setup — it is a hunch.

The Posture-Current-Pole calibrates ICT setups to current regime: order
blocks work cleanest in trending posture; fair value gaps deliver
predictably in ranging-to-expansion transitions; liquidity grabs are
strongest at session boundaries. The pole catches the operator who tries
to run a 2021-bull-market order-block setup in a 2026 chop regime.

The Risk-1%-Pole pairs with ICT structure naturally: the stop sits on
the far side of the named structural feature (below the order block,
above the breaker), and size flows from that distance.

## Core Concepts

### 1. Liquidity

The fuel of all price movement. Stops sit above swing highs and below
swing lows. Pending orders cluster at obvious levels — round numbers,
prior session high/low, daily/weekly high/low. Smart money runs price
to take this liquidity before delivering the real move. When the agent
calls a setup, it identifies where the liquidity sits and which direction
price needs to run to take it.

Two flavors: **buy-side liquidity** (stops above highs, breakout orders
above resistance) and **sell-side liquidity** (stops below lows,
breakout orders below support). The agent reads which side gets taken
first; that is usually the wrong-way move that precedes the right-way
move.

### 2. Order Block

The last opposite-color candle before a strong directional move. A
**bullish order block** is the last down candle before a sustained rally;
a **bearish order block** is the last up candle before a sustained drop.
Order blocks mark institutional accumulation/distribution zones. Price
frequently returns to the order block to mitigate (re-test) before
continuing in the original direction.

Setup form: price moves away from the order block, then returns; entry
is at the order block boundary; stop is the far side of the order block;
target is the next liquidity pool in the direction of the original move.

### 3. Fair Value Gap (FVG)

A three-candle pattern where candle 2 leaves a wick-gap between candle 1
and candle 3. The gap represents inefficient price delivery — institutions
moved price faster than the order book could fully transact. Price tends
to return to fill this gap before continuing.

Setup form: identify FVG on higher timeframe; wait for price to return
into the FVG on lower timeframe; enter on the mitigation; stop beyond
the FVG; target the next liquidity pool.

### 4. Market Structure Shift (MSS) / Change of Character (CHoCH)

A market structure shift is the moment a trend's higher-high-higher-low
pattern (uptrend) or lower-high-lower-low pattern (downtrend) breaks. A
break of the most recent counter-trend swing point marks the shift. CHoCH
specifically marks the first sign of trend exhaustion.

The agent uses MSS to confirm that posture has rotated before calling
counter-trend setups. Without MSS confirmation, a counter-trend setup is
fighting structure — which the Risk-1%-Pole catches.

### 5. Premium and Discount Arrays

The chart range is divided into **premium** (upper half) and **discount**
(lower half) relative to a recent dealing range. ICT methodology favors
**buying in discount** and **selling in premium**. An entry in premium
on a long thesis is structurally weak; an entry in discount on a long
thesis is structurally aligned.

The agent reads where price currently sits in the range and flags
premium/discount mismatch on the proposed direction.

### 6. Liquidity Grab / Stop Hunt

A directional spike that takes out a recent swing high or low (collecting
the stops parked there), then reverses sharply. The grab is the smart-money
mechanism for accumulating opposite-direction positions at the cost of
late-trend retail orders. The agent watches the grab, waits for the
reversal confirmation, then enters in the post-grab direction.

Setup form: identify a clear liquidity pool (prior session high, daily
high, weekly high); wait for price to spike through and immediately
reverse; enter on the reversal; stop above the grab high (for shorts);
target the next opposite-side liquidity pool.

### 7. Breaker Block

When an order block fails — price violates it cleanly — that violated
order block becomes a **breaker**, now flipping its role. A failed
bullish order block becomes resistance; a failed bearish order block
becomes support. Breakers mark where structure has flipped and supply
clean entry zones for the new direction.

## Common Applications

**Pre-market setup audit (mode: setup_audit):**
"Long ES at 5142 — bullish 4H order block, 1H FVG above mitigated, daily
discount, NY session liquidity pool above 5189."
The agent verifies: named setup? Yes (order block + FVG confluence).
Premium/discount aligned? Yes (discount on long). Liquidity target? Yes
(5189 buy-side liquidity). Risk-1%-Pole sizes the position from
entry-to-stop. Verdict: go.

**Counter-trend rejection:**
"Short NVDA at 142 — looks tired."
The agent refuses. No named setup, no MSS confirmation that trend has
rotated, premium/discount unclear, no named liquidity target. Setup-Rigor
catches it before Risk-1%-Pole has to.

**Regime mismatch:**
"Order block trade on BTC at session lows, 4H trending down."
The agent flags: order blocks deliver cleanest in trending posture
matching the OB direction. A bullish OB in a 4H downtrend is fighting
posture. Posture-Current downgrades the setup to half-conviction or
refuses it.

**Liquidity-grab entry on NQ open:**
"Pre-NY-open spike above prior session high, immediate reversal, MSS on
5-minute."
The agent confirms: liquidity grab named, reversal candle confirms,
MSS on entry timeframe, target = prior session low (sell-side liquidity).
Risk = stop above grab high. Size = 1% of book / (entry - stop).
Verdict: go.

## Anti-patterns (when this framework is misapplied)

**Naming the setup after the fact.** Calling "order block!" on any
candle near a level retroactively is not setup discipline. The order
block is identified as the last opposite-color candle before the move
that already happened; the entry is when price returns to test it. If
the entry is the move itself, there is no order block — there is just
chasing.

**FVG without confluence.** Every chart has dozens of fair value gaps.
Trading every one without confluence (order block alignment, premium/
discount fit, liquidity target) produces noise trades. Setup-Rigor-Pole
requires ≥2 confluences before entry.

**Counter-trend without MSS.** Calling a reversal trade before market
structure has shifted is fighting trend on hope. The agent waits for the
break of the most recent counter-trend swing point before sizing
counter-trend setups.

**Stop-hunt-shaped entries without the hunt.** The "spike-and-reverse"
pattern is meaningful only when there is named liquidity above/below
that got taken. A spike-and-reverse in the middle of a range with no
specific stop pool above/below is not a liquidity grab — it is just
volatility.

**ICT vocabulary as decoration.** Using ICT terms to dress up a hunch
("I think it's going up because of the order block") without specifying
which order block, on which timeframe, with which mitigation level, and
with which liquidity target — is vocabulary abuse. Each term carries a
specific spatial referent on the chart. If it cannot be pointed to, it
is not named.

**Trades against current regime without explicit acknowledgment.** Per
the locked anti-pattern list: "Trades against current regime without
explicit acknowledgment." ICT setups assume the underlying regime
supports them. The agent surfaces regime when calling the trade.

**Investment advice without disclaimer.** Per the locked anti-pattern
list: "Investment advice without disclaimers — this is analysis, not
advice." Every ICT setup output ends with the analysis-only disclaimer.

## Cross-references

- Agent skill: `agents/trading-analyst/SKILL.md`
- Bench: `agents/trading-analyst/personality/_bench.md` (Setup-Rigor-Pole / Risk-1%-Pole / Posture-Current-Pole)
- Frameworks index: `agents/trading-analyst/personality/frameworks_index.md`
- Vendored reference: `agents/trading-analyst/context/references/ict-trading-ultimate-guide.md`
- Vendored reference: `agents/trading-analyst/context/references/tradingview-best-practices.md`
- Companion methodology: `agents/trading-analyst/context/methodology/risk-management-discipline.md`
- Memory: `agents/finance-manager/memory/wealth_creator_mode.md`
