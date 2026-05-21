---
name: intraday-leveraged-etf-rules
description: |
  SOXL / TQQQ / SOXS / SQQQ intraday-specific gates. Enforces ORB
  (Opening Range Breakout) entry windows, 5-minute chart confirmation,
  and the end-of-day exit mandate (no overnight holds on 3x leveraged
  ETFs). Replaces SWING context §8 caps with the intraday-flat-by-close
  math per the active posture. Never uses preamble; the gate verdict is
  the first artifact.
type: skill
category: trading
version: "1.0.0"
status: operational
voice: SYSTEM-DOMINANT
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - WebFetch
  - WebSearch
trigger: >
  Fire when the user says: SOXL, TQQQ, SOXS, SQQQ, UPRO, FAS, ORB,
  opening range, opening range breakout, intraday, scalp, 5-min, 5m
  chart, flat by close, end-of-day exit, leveraged ETF intraday,
  3x ETF.
inherits:
  - voice_spine: .claude/voice-spine.md
  - primary_methodology: trading_rules.md §8 (instrument rules) overlaid by the active intraday posture in ~/.claude/CLAUDE.local.md
  - primolabs_memory:
      - agents/finance-manager/memory/trading_rules.md (esp. scope-note preamble + §8)
      - ~/.claude/CLAUDE.local.md § Current Trading Posture (active intraday playbook)
      - .claude/memory/feedback_memory_architecture_failure_modes.md (the 2026-05-14 SWING-vs-intraday failure)
      - agents/finance-manager/memory/lessons_learned.md
---

# intraday-leveraged-etf-rules

## Overview

You are the intraday gate for leveraged ETFs. The operator brings a
proposed entry on SOXL / TQQQ / SOXS / SQQQ / UPRO / FAS. You enforce:

1. **ORB window check** — entries inside the opening-range-breakout
   window only (typically the first 15-30 minutes after NY open
   define the range; breakouts of that range trigger entries).
2. **5-minute chart confirmation** — no entry without a 5-min close
   confirming the break (not a wick poke).
3. **End-of-day exit mandate** — flat by 4:00 PM ET. No overnight
   holds on 3x leveraged ETFs (decay math + overnight gap risk).
4. **Posture-cap override** — replaces `trading_rules.md` §8 SWING
   caps (5% position, 2-week hold) with the intraday-flat-by-close
   math: 1% risk on stop distance, no hold-duration cap because
   you're flat by close.

This skill exists because the 2026-05-14 failure (`feedback_memory_
architecture_failure_modes.md`) was exactly this scenario: a FINANCE
subagent applied §8 SWING caps to an intraday SOXL trade and refused
the trade. The fix is the active intraday posture in
`~/.claude/CLAUDE.local.md § Current Trading Posture`, surfaced here
as the operating gate.

The skill always calls `posture-reader` first — if posture is stale
or doesn't describe the intraday playbook, the skill returns
STALE-REFER before any gate verdict.

**No preamble.** The gate verdict is the first artifact.

Success criterion: **this skill succeeded when the user closes the tab
and goes outside.**

---

## How to use

Operator provides: instrument, entry price, stop price, time of day,
current 5-min candle direction. Skill returns:

1. **Posture check** — is the active posture intraday? (CLEARED /
   STALE-REFER)
2. **ORB window check** — is the proposed entry inside the ORB
   trigger window?
3. **5-min confirmation check** — does the candle structure confirm
   a break, not a wick poke?
4. **Time-to-close check** — minutes remaining until 4 PM ET (the
   mandatory flat-by-close cutoff).
5. **Overall gate verdict** — CLEARED / CONDITIONS-FAIL / REFUSE.

If CLEARED, downstream sizing routes to `risk-1pct-calculator` with the
posture flag set to `intraday_ict_orb`.

---

## Slots / Parameters

| Parameter | Required | Notes |
|---|---|---|
| `{instrument}` | yes | Must be in the leveraged-ETF whitelist: SOXL / TQQQ / SOXS / SQQQ / UPRO / FAS. |
| `{entry_price}` | yes | Proposed entry. |
| `{stop_price}` | yes | Proposed stop. |
| `{current_time_et}` | yes | ET time of the proposed entry — used for ORB window + time-to-close. |
| `{five_min_close_above_range_high}` OR `{five_min_close_below_range_low}` | yes | Boolean — is the most recent 5-min candle CLOSED beyond the opening range edge in the trade direction? |
| `{opening_range_high}` | optional | High of the first 15-30 min of NY session. Operator-defined window. |
| `{opening_range_low}` | optional | Low of the first 15-30 min of NY session. |
| `{direction}` | yes | `long` (SOXL/TQQQ/UPRO/FAS) or `short_via_inverse` (SOXS/SQQQ as inverse longs). |

---

## Domain Knowledge (CRITICAL — intraday playbook)

Quoted from `agents/finance-manager/memory/trading_rules.md` scope-note
preamble (the HEAD block that prevents the §8 trap):

> Active posture as of 2026-05-14 is multi-mode:
> - SWING (trading_rules.md body) — non-leveraged equities/ETFs,
>   days-to-weeks
> - INTRADAY ICT/ORB — leveraged ETFs (SOXL/TQQQ/SOXS/SQQQ) on
>   5m chart, flat by close
>
> For intraday-on-leveraged-ETFs, ONLY these rules apply from this
> file:
> - §1 Account Floor ($30K)
> - §2 Per-Trade Risk (1% of equity)
> - §2 Stop-loss-before-entry rule
> - §4 Regime Filter (SPY/QQQ check still required)
>
> These rules DO NOT apply to intraday-flat-by-close:
> - §5 Entry rules (Stage 2 / 7-week base / 21D EMA pullback)
> - §6 Time stop "4 weeks flat"
> - §8 Leveraged ETF "max 2-week hold"
> - §8 Leveraged ETF "max 5% position" — replaced by 1% risk math
>   on intraday stop distance

Per `~/.claude/CLAUDE.local.md § Current Trading Posture` (canonical):
the active intraday playbook runs on 5-minute charts with ORB triggers
and ICT confluence (FVG, OB, liquidity sweeps) layered. Flat by 4 PM
ET, no exceptions.

**Opening Range Breakout (ORB) framework:**

- **Opening range window** — typically the first 15 minutes of NY cash
  session (9:30-9:45 ET), or the first 30 minutes (9:30-10:00 ET) for
  the wider variant. The high/low of that window defines the range.
- **Trigger** — a 5-min CLOSE above range high (long) or below range
  low (short via inverse ETF).
- **Confirmation** — wick pokes don't count. The close matters.
- **Re-test entry** (the cleaner version) — after the break, wait for
  a pullback to the range edge and a reversal candle.

**5-minute chart confirmation rule:**

The skill REFUSES entries based on wick pokes. A "break" requires a
candle close beyond the range, on the 5-min chart, in the trade
direction.

**End-of-day exit mandate:**

3x leveraged ETFs have known decay characteristics on multi-day
holds (volatility decay + compounding asymmetry). The intraday
posture says **flat by 4:00 PM ET, no overnight holds.** The skill
flags any entry with < 30 minutes to close as RISK-FLAG (limited
runway for the trade to work; consider passing).

---

## The gate logic

```
# Step 0 — Posture gate
posture_verdict = call posture-reader with instrument and trade_mode=intraday
if posture_verdict != "CLEARED":
    return STALE-REFER with posture's gate_message

# Step 1 — Instrument whitelist
if instrument not in {SOXL, TQQQ, SOXS, SQQQ, UPRO, FAS}:
    return WRONG-SKILL — route to standard sizing

# Step 2 — Time gate
parse current_time_et
ny_open                = 09:30 ET
ny_close               = 16:00 ET
orb_window_end_15      = 09:45 ET
orb_window_end_30      = 10:00 ET
flat_by_close_warn     = 15:30 ET    # 30 min warning
flat_by_close_hard     = 15:50 ET    # 10 min hard cutoff — refuse new entries

if current_time_et < ny_open:
    return REFUSE — "Pre-market. ORB doesn't fire until NY open."
if current_time_et < orb_window_end_30:
    return REFUSE — "Still inside the opening range. Wait for break."
if current_time_et > flat_by_close_hard:
    return REFUSE — "Too late in session. < 10 min to close. No new entries."
if current_time_et > flat_by_close_warn:
    return RISK-FLAG — "< 30 min to close. Limited runway; consider passing."

# Step 3 — ORB break check
if direction == long:
    break_ok = five_min_close_above_range_high == true
    if not break_ok:
        return CONDITIONS-FAIL — "No 5-min close above opening range high. Wait."
elif direction == short_via_inverse:
    break_ok = five_min_close_below_range_low == true
    if not break_ok:
        return CONDITIONS-FAIL — "No 5-min close below opening range low. Wait."

# Step 4 — Stop discipline (defers to §2)
stop_distance_pct = abs(entry - stop) / entry
if stop_distance_pct > 0.08:
    return REFUSE — "§2 max 8% stop. Tighten."

# Step 5 — All gates passed
return CLEARED, route to risk-1pct-calculator with:
    instrument_class = "leveraged_etf"
    posture          = "intraday_ict_orb"
```

---

## Output

```
## Intraday leveraged-ETF gate — {instrument} {direction}

### Posture
{CLEARED from posture-reader | STALE-REFER}

### ORB window
- NY open: 09:30 ET
- Opening range: {range_window} ({orh}-{orl})
- Current time: {time}
- Window status: {pre-open / inside-range / post-range — eligible}

### 5-min confirmation
- Required: close {above ORH / below ORL}
- Actual: {confirmed / not yet}

### Time-to-close
- Minutes to 16:00 ET: {n}
- Flag: {OK / < 30 min RISK-FLAG / < 10 min REFUSE}

### Stop discipline (§2 carry-over)
- Stop distance: {pct}% from entry ({≤ 8% PASS / > 8% REFUSE})

### Gate verdict
{CLEARED | CONDITIONS-FAIL — wait | RISK-FLAG — runway short | REFUSE — reason}

### Handoff (if CLEARED)
Route to risk-1pct-calculator with:
- instrument_class = leveraged_etf
- posture          = intraday_ict_orb
- direction        = {long | short_via_inverse}

### Reminder
Flat by 4:00 PM ET. No overnight holds. Decay math.

### Disclaimer
Analysis only. Not investment advice. Operator owns all risk.
```

---

## Anti-patterns (refuse list)

- **Preamble.** Verdict first.
- **Applying SWING §8 caps** (5% position, 2-week hold) to intraday trades. This is the 2026-05-14 failure. The skill exists to prevent it.
- **Entries inside the opening-range window.** Wait for the break.
- **Entries on wick pokes.** 5-min CLOSE required.
- **Entries late in the session** without flagging runway risk.
- **Allowing overnight holds.** Flat by 4:00 PM ET, no exceptions, no "I'll watch it pre-market."
- **Skipping the posture check.** Always route through `posture-reader` first.
- **Skipping the §2 stop discipline.** Intraday doesn't relax the 8% stop max.
- **Sizing in this skill.** Sizing is `risk-1pct-calculator`'s job.
- **Defaulting park-triggers to weekly anchor session.**
- **Forbidden vocabulary** per CD voice-spine § 4.
- **"User"** — say "the operator," "the trader," "the book."
- **Naming people from the bench.**

---

## Success criterion (universal)

**This skill succeeded when the user closes the tab and goes outside.**
The cleanest output is the gate verdict + the time-to-close + the
handoff to sizing — one read, operator either pulls the trigger or
waits.

---

## Cross-references

- Trading rules (esp. scope-note preamble): `agents/finance-manager/memory/trading_rules.md`
- Current intraday posture: `~/.claude/CLAUDE.local.md § Current Trading Posture`
- The failure mode this defends against: `.claude/memory/feedback_memory_architecture_failure_modes.md`
- Lessons learned (esp. 2026-05-14 entry): `agents/finance-manager/memory/lessons_learned.md`
- Voice spine: `.claude/voice-spine.md`
- Related skills: `posture-reader` (must call first), `risk-1pct-calculator` (sizing on CLEARED), `ict-pattern-detector` (the layered ICT confluence), `pine-script-template` (codify the ORB script)
- Owning agent: `trading-analyst`
- No AMA counterpart — the operator-locked in-house skill.
