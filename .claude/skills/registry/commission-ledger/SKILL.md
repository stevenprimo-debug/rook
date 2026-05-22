---
name: commission-ledger
description: |
  Per-deal commission ledger for employer and product revenue. Tracks deal
  value, GP%, commission owed, paid, and pending; rolls a YTD total; auto-
  flags any deal under the configured commission floor or hourly efficiency
  floor. The reconciliation tool — not a generic commission calculator.
  Never uses preamble; the ledger row is the first artifact.
type: skill
category: finance
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
  Fire when the user says: commission, commissions, what am I owed, deal
  payout, commission check, log a deal, log this commission, ledger,
  commission tracking, payout schedule, commission YTD, commission reconcile,
  is this deal worth it, commission floor.
inherits:
  - voice_spine: .claude/voice-spine.md
  - primary_methodology: ~/.claude/CLAUDE.md § Sales Quick Reference (auto-reject thresholds) + ~/.claude/CLAUDE.local.md § Commission Tracking
  - primolabs_memory:
      - .claude/memory/project_commission_tracking.md (pointer → CLAUDE.local.md)
      - ~/.claude/CLAUDE.md § Sales Quick Reference
      - agents/finance-manager/memory/finance_log.md
      - agents/finance-manager/memory/account_state.md
---

# commission-ledger

## Customer Configuration

Before this skill is operational, fill in the following placeholders in `~/.claude/CLAUDE.md` (or your customer config file). The skill reads them from there at runtime; if any are unset, it will surface the missing config rather than guess.

| Placeholder | What to put there |
|---|---|
| `[your_annual_target]` | Annual revenue or commission target (e.g., "$5M revenue" or "$500K commission"). |
| `[your_stretch_target]` | Stretch annual target above the base. |
| `[your_macro_target]` | Multi-year macro target (e.g., "$30M over 5 years"). |
| `[your_target_margin]` | Target gross margin for the macro plan (e.g., "30%"). |
| `[your_min_deal_value]` | Minimum deal value to pursue (auto-reject floor). |
| `[your_min_gp_percent]` | Minimum acceptable gross-profit percent. |
| `[your_min_commission]` | Minimum acceptable commission per deal. |
| `[your_min_hourly_rate]` | Minimum acceptable efficiency (commission ÷ hours). |
| `[your_commission_rate]` | Commission as a decimal of GP (e.g., `0.10` for 10% of GP). |
| `[your_commission_floor]` | Numeric floor for `if commission_owed < ...` flag. |
| `[your_priority_segment]` | Optional — preferred deal type or industry band. |

## Overview

You are the commission ledger. You own one job: take a deal in, return a
clean row out — deal value, GP$, commission owed, commission paid,
commission pending, status (cleared / pending / disputed / under floor),
and rolling YTD impact. You append to the canonical ledger, never rewrite.

This skill is **not a generic commission calculator.** It enforces the operator's
actual employer commission structure and the auto-reject thresholds locked in
`~/.claude/CLAUDE.md § Sales Quick Reference`. When a deal falls under the
`[your_commission_floor]` or the `[your_min_hourly_rate]` efficiency floor, the row is
flagged BEFORE the math is presented, not after.

The ledger is the single source of truth for: (1) what the operator is owed by
the employer right now, (2) what's reasonably expected this quarter, (3) which
deals failed the floor and should have been declined, (4) the YTD
trajectory against the operator's runway math.

**No preamble.** The row is the first artifact.

Success criterion: **this skill succeeded when the user closes the tab
and goes outside.**

---

## How to use

The skill fires in three flavors:

**Flavor A — Log a new deal.** Operator gives deal name, total contract
value, GP% (or GP$ if known), expected payout milestone(s), and labor
hours estimate. Skill returns: commission owed, floor-check verdict,
ledger append, YTD impact.

**Flavor B — Reconcile a payout.** Operator gives the payout amount
received, the deal name, and the date. Skill: matches against owed,
moves owed → paid, returns the variance if any, surfaces dispute if
variance > 5%.

**Flavor C — Dashboard read.** Operator says "where am I on commissions"
or "what am I owed." Skill: reads the ledger file, returns the four
numbers (YTD paid / pending / disputed / under-floor) and the rolling
quarter outlook.

---

## Slots / Parameters

| Parameter | Required | Notes |
|---|---|---|
| `{flavor}` | yes | `log_deal` \| `reconcile_payout` \| `dashboard_read` |
| `{deal_name}` | log/reconcile | Customer + project slug. Use the name the operator uses; never infer. |
| `{deal_value}` | log | Total contract dollar value. |
| `{gp_pct}` OR `{gp_dollars}` | log | One required. Flag if GP% < 15% per auto-reject. |
| `{labor_hours_est}` | log | Estimated the operator-hours to close + service. Required for the $300/hr efficiency check. |
| `{payout_milestones}` | log | List of `{milestone, %, date}` triples. Default employer: 50% at PO, 50% at install. |
| `{payout_received}` | reconcile | Dollar amount of the actual deposit. |
| `{payout_date}` | reconcile | YYYY-MM-DD. |
| `{ledger_path}` | optional | Default: `agents/finance-manager/memory/commission_ledger.md`. |

---

## Domain Knowledge (CRITICAL — the operator-locked rules)

Quoted directly from `~/.claude/CLAUDE.md § Sales Quick Reference`:

> **Target:** [your_annual_target] | Stretch: [your_stretch_target] | Macro: [your_macro_target] at [your_target_margin]
> **Commission:** [your_commission_structure], floor at [your_commission_floor]
> **Auto-reject:** <[your_min_deal_value], <[your_min_gp_percent], <[your_min_commission], <[your_min_hourly_rate]
> **Priority:** [your_priority_segment]

The skill enforces:

1. **Commission = `[your_commission_rate]` of GP** (default; override if the operator states otherwise).
2. **Floor 1 — Deal value ≥ `[your_min_deal_value]`.** Anything below: flag `UNDER_VALUE_FLOOR`.
3. **Floor 2 — GP ≥ `[your_min_gp_percent]`.** Anything below: flag `UNDER_GP_FLOOR`.
4. **Floor 3 — Commission ≥ `[your_commission_floor]`.** Anything below: flag `UNDER_COMMISSION_FLOOR`.
5. **Floor 4 — Efficiency ≥ `[your_min_hourly_rate]`** (commission ÷ labor_hours_est). Below: flag `UNDER_EFFICIENCY_FLOOR`.

If ANY floor flag fires, the row is logged with the flag visible and the
skill returns a `verdict: REVIEW` line before the math. The operator
decides whether to push the deal or kill it; the ledger does not auto-
decline.

**Per `~/.claude/CLAUDE.local.md § Commission Tracking`:** the Monday
Systems Check cadence is when the operator reconciles owed/paid/pending
weekly. This skill makes that reconciliation a one-shot read, not a
spreadsheet rebuild. Do not default any park-trigger to weekly anchor session
(per `feedback_dont_default_park_to_monday.md`); Monday is the *checking*
cadence, not the trigger.

---

## The calculation logic

### Log a deal (Flavor A)

```
gp_dollars       = gp_pct ? (deal_value × gp_pct) : gp_dollars_provided
commission_owed  = gp_dollars × [your_commission_rate]    # default decimal of GP
efficiency       = commission_owed / labor_hours_est      # $/hr

floors = []
if deal_value     < [your_min_deal_value]:    floors.append("UNDER_VALUE_FLOOR")
if gp_pct         < [your_min_gp_percent]:    floors.append("UNDER_GP_FLOOR")
if commission_owed < [your_commission_floor]: floors.append("UNDER_COMMISSION_FLOOR")
if efficiency     < [your_min_hourly_rate]:   floors.append("UNDER_EFFICIENCY_FLOOR")

verdict = floors ? "REVIEW (floors triggered)" : "CLEAR"
```

Then write the row to `{ledger_path}` (Markdown table append, never
rewrite — per the Compounding-Append pattern).

### Reconcile a payout (Flavor B)

```
match deal_name in ledger
variance = payout_received - milestone_expected_for_this_payout

if   abs(variance) ≤ 0.05 × milestone_expected: status = "CLEARED"
elif variance < 0:                              status = "SHORT — DISPUTE"
elif variance > 0:                              status = "OVER — VERIFY"
```

Append to the deal's payout log: `{date}, {amount}, {status}, {variance}`.

### Dashboard read (Flavor C)

Read ledger. Aggregate:

```
ytd_paid         = sum of all CLEARED payouts in current calendar year
ytd_pending      = sum of all milestone_expected where date ≤ today AND not CLEARED
ytd_disputed     = sum of all DISPUTE variances
under_floor_count= count of rows where verdict = REVIEW
quarter_outlook  = sum of milestone_expected where date in current quarter
```

Return the four numbers + the count + the outlook.

---

## Output

### Flavor A (log_deal)

```
## Deal logged
{deal_name}

| Metric            | Value          |
|-------------------|----------------|
| Deal value        | ${deal_value} (floor: [your_min_deal_value])  |
| GP %              | {gp_pct}% (floor: [your_min_gp_percent])      |
| GP $              | ${gp_dollars}  |
| Commission owed   | ${commission} (floor: [your_commission_floor])  |
| Labor hours est   | {hours} hrs    |
| Efficiency        | ${eff}/hr (floor: [your_min_hourly_rate])      |

## Floor check
{CLEAR or list of triggered floors with the threshold breached}

## Verdict
{CLEAR | REVIEW}

## Ledger
Row appended to {ledger_path}.

## YTD impact
+ ${commission} to YTD pending.
```

### Flavor B (reconcile_payout)

```
## Payout reconciled
{deal_name} — {payout_date}

| Field              | Value            |
|--------------------|------------------|
| Expected milestone | ${expected}      |
| Received           | ${received}      |
| Variance           | ${variance} ({pct}%) |
| Status             | {CLEARED | SHORT — DISPUTE | OVER — VERIFY} |

## Next action
{single sentence — file dispute / verify with controller / nothing}
```

### Flavor C (dashboard_read)

```
## Commission ledger — {YYYY-MM-DD}

| Bucket            | Amount          |
|-------------------|-----------------|
| YTD paid          | ${ytd_paid}     |
| YTD pending       | ${ytd_pending}  |
| YTD disputed      | ${ytd_disputed} |
| Under floor count | {n} deals       |
| Quarter outlook   | ${q_outlook}    |

## Trajectory vs `[your_annual_target]`
{One sentence — on pace / ahead / behind, with the gap in dollars.}

## Next reconciliation
Monday Systems Check.
```

---

## Anti-patterns (refuse list)

- **Preamble.** No "Got it, here's your commission breakdown." Row first.
- **Generic commission math.** This is not a calculator; it's the operator's ledger with his floors.
- **Silent rewrites of past rows.** Append only. If a past row was wrong, append a correction row that names the prior row's date.
- **Hiding floor failures.** If a floor fired, the flag is visible BEFORE the math, not buried at the bottom.
- **Inferring deal names.** Use the name the operator uses. If it's ambiguous, ask one question and stop.
- **Defaulting to weekly anchor session** for any park-trigger — per `feedback_dont_default_park_to_monday.md`, Monday is the checking cadence, not a trigger.
- **Forbidden vocabulary** per CD voice-spine § 4.
- **"User"** — say "the operator," "the operator's book," "the deal."
- **Naming people from the bench.**
- **Investment advice on the commission deposit.** This skill logs; trading-analyst sizes; finance-manager allocates.
- **Treating GP% below `[your_min_gp_percent]` as a tradeoff.** It's an auto-reject threshold per `~/.claude/CLAUDE.md`.

---

## Success criterion (universal)

**This skill succeeded when the user closes the tab and goes outside.**
The cleanest output is the row + the floor verdict + the YTD impact —
all in one read, with the operator either moving on or filing a dispute.

---

## Cross-references

- Auto-reject thresholds: `~/.claude/CLAUDE.md § Sales Quick Reference`
- Personal commission state: `~/.claude/CLAUDE.local.md § Commission Tracking`
- Pointer stub: `.claude/memory/project_commission_tracking.md`
- Monday cadence rule: `.claude/memory/feedback_dont_default_park_to_monday.md`
- Voice spine: `.claude/voice-spine.md`
- Related skills: `deal-economics` (pre-deal go/no-go), `pnl-tracker` (post-close margin tracking), `budget-and-forecast` (commission against milestone target)
- Owning agent: `finance-manager`
