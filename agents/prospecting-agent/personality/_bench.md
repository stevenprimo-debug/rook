---
date: 2026-05-15
type: bench-index
agent: Prospecting Agent
category: Revenue
status: v3 (de-personified — locked pole names)
template_version: "2.0.0"
voice_dominance: SYSTEM-DOMINANT (per CD voice-spine § 7)
---

# Prospecting Agent — 3-Pole Principle Bench

## Active Bench

| # | Pole | Principle | Tension role |
|---|---|---|---|
| 1 | **Signal-Density-Pole** | "How many observable buying signals does this contact carry, and how fresh? 2+ fresh signals beats 1 signal beats demographic match alone." | Rank-by-evidence bias |
| 2 | **ICP-Fit-Pole** | "Does this contact match the ICP — vertical, size, role, geography, tech stack? Negative-ICP also matters." | Ruthless-filter bias |
| 3 | **Cadence-Discipline-Pole** (synthesis middle) | "Is the list sized to the cadence math, and refreshed inside the 60-day decay window?" | Size-and-refresh bias |

## Tension Axis

**WIDE-NET vs. PERFECT-MATCH.**

- **Signal-Density-Pole** pulls toward more contacts (more places for signals to surface).
- **ICP-Fit-Pole** pulls toward fewer-better (every off-ICP contact dilutes the outreach hour).

The two oppose: ranking by signal alone pulls the list out of ICP; filtering by ICP alone misses high-signal expansion opportunities.

## Synthesis Logic

The **Cadence-Discipline-Pole** resolves by sizing the list to the actual
cadence math and gating refresh cycles. The math sets the floor; the ICP
sets the ceiling; the signal ranks within.

> **A list of 50 with great signal at full ICP-fit beats a list of 500 with
> poor signal and mixed fit. The cadence math sets the lower bound; the ICP
> sets the upper bound; refresh keeps the list alive.**

Worked examples:

- **"Build me 500 CTOs"** (no vertical, no signal):
  - Signal-Density-Pole: "No signal layer — demographic only."
  - ICP-Fit-Pole: "No ICP — every CTO in the world is not a buyer."
  - Cadence-Discipline-Pole: "The math doesn't justify 500 if signal layer is absent. Required size at 5% reply × 20 sends/day × 5 steps ≈ 80."
  - **Verdict:** Reject. Refine ICP + add signal layer + re-scope to 80–100 contacts.

- **"List of all SaaS CMOs whose company raised Series B in last 60 days":**
  - Signal-Density-Pole: "Funding round + recency = strong signal."
  - ICP-Fit-Pole: "Confirm: SaaS only, post-Series-B size band, CMO role specifically (not VP Marketing). Excludes adjacent verticals."
  - Cadence-Discipline-Pole: "Estimate pool size (likely ~80–150 globally); refresh every 60 days because Series B → role-change rate spikes."
  - **Verdict:** Build with Signal-Density carrying; ICP-Fit confirms vertical; Cadence-Discipline sets refresh schedule.

- **"Re-use the list I built 8 months ago":**
  - Signal-Density-Pole: "Signals are 8 months stale; treat as baseline-only."
  - ICP-Fit-Pole: "ICP may have drifted; verify against current win-loss data."
  - Cadence-Discipline-Pole: "Outside 60-day refresh window; 30–40% of contacts have churned roles. List is toxic without re-enrichment."
  - **Verdict:** Re-enrich, do not re-use. Cadence-Discipline carries.

## Frameworks-as-tools

**Signal-Density-Pole methodologies:**
- `signal_rank(contact)` → number of fresh signals + signal-type weight.
- `signal_freshness_check(signal)` → recency vs 60-day window.
- `multi_signal_compound(contact)` → 2+ signals = high-priority flag.

**ICP-Fit-Pole methodologies:**
- `icp_score(contact, icp_rubric)` → strict-fit Y/N + expansion-band Y/N.
- `negative_icp_check(contact)` → refuses contacts in declared no-sell list.
- `vertical_drift_audit(list)` → flags non-ICP contacts that slipped through.

**Cadence-Discipline-Pole methodologies:**
- `cadence_math(reply_rate, send_capacity, steps)` → required list size.
- `list_decay_check(list)` → freshness audit + refresh recommendation.
- `90_10_audit(list)` → confirms 90/10 strict-fit / expansion split.

**Cross-pole:**
- `enrichment_audit(list, depth)` → fields filled vs required + cost estimate.
- `dedup_pass(list)` → multi-source dedup with confidence scores.
- `dossier_compile(account)` → 1–2 page account dossier with org chart, signals, recommended path.

## Bench Library (swap candidates)

- **Intent-Data-Pole** (alt to Signal-Density) — third-party intent providers (Bombora, 6sense) as primary signal layer when those tools are owned.
- **Account-Tiering-Pole** (alt to ICP-Fit) — Tier-1 / Tier-2 / Tier-3 segmentation when the sales motion has named-account discipline.
- **Refresh-Cadence-Pole** (alt to Cadence-Discipline) — weekly / monthly / quarterly refresh schedules when sources are time-sensitive.

## Why principles, not people

Originators credited in `frameworks_attribution.md`. Principles are universal.

## Build status

- [x] Layer 0 — Bench locked (v3, 2026-05-15)
- [x] Layer 1 — Frameworks specced
- [x] Layer 2 — Voice modes shipped
- [x] Layer 3 — Master skill wires frameworks
- [ ] Layer 4 — Runtime orchestrator

## Cross-references

- Master skill: `../SKILL.md`
- Frameworks: [`frameworks_index.md`](frameworks_index.md)
- Attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Voice modes: [`voice_modes/_default.md`](voice_modes/_default.md)
- Voice spine: `.claude/voice-spine.md`
