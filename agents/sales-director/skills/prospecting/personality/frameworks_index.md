---
date: 2026-05-14
type: frameworks-index
agent: Prospecting Agent
status: v2
template_version: "2.0.0"
---

# Prospecting Agent — Frameworks Index

Methodologies indexed by name. Originators in `frameworks_attribution.md`.

---

## signal_rank(contact)

**Signature:** `signal_rank(contact) → {score: 0-100, signals: [{type, source, freshness_days}], priority: high|priority|baseline}`

**Pole:** Signal-Pole.

**Returns:** scored signal verdict per contact.

**Signal hierarchy (decreasing strength):**
1. Funding round (Series A+, IPO, M&A) — +40
2. New executive start (CEO/CRO/CIO) — +30
3. Champion role change (ours follows them) — +25
4. Tech-stack signal (competitor displacement, integration) — +20
5. Content activity (CEO posted on the topic) — +10
6. Demographic match alone — baseline +5

Multi-signal compounding: 2+ fresh signals = high-priority bonus +15.

**Failure mode caught:** Ranking on title alone when better signals exist.

---

## icp_score(contact)

**Signature:** `icp_score(contact, icp_def) → {score: 0-100, attribute_match: {vertical, size, role, geo, tech_stack}}`

**Pole:** Fit-Pole.

**Returns:** ICP fit score per attribute + overall.

**Scoring:**
- Strict ICP attribute match: +20 each
- Adjacent ICP match: +10 each
- ICP miss: 0
- Negative-ICP hit (e.g., wrong vertical): −50 disqualifier

**Failure mode caught:** Lists with 90/10 expansion drift — too many outliers dilute.

---

## cadence_math(reply_rate, capacity, steps)

**Signature:** `cadence_math(reply: float, capacity: int, steps: int) → {required_list_size: int}`

**Pole:** Scale-Pole.

**Returns:** required list size for quarterly quota.

**Formula:** `required = (quota_meetings / reply_rate) / capacity_per_week_per_rep * 13_weeks * (1 / cadence_step_yield_factor)`.

**Failure mode caught:** Lists that starve the cadence or oversaturate the rep.

---

## freshness_check(signal)

**Signature:** `freshness_check(signal) → {fresh: bool, age_days: int}`

**Pole:** Signal-Pole.

**Returns:** whether the signal is within 60 days.

**Failure mode caught:** Stale-signal hopium — a funding round from 2 years ago is not a buying signal.

---

## multi_signal_compounding(contact)

**Signature:** `multi_signal_compounding(contact) → {count: int, types: [string], compounding_bonus: int}`

**Pole:** Signal-Pole.

**Returns:** count of fresh signals + bonus calculation.

**Rule:** 2+ fresh signals = +15 bonus. 3+ = +25. Compounds because multiple signals = active buying cycle.

---

## hand_craft_ceiling(list_size)

**Signature:** `hand_craft_ceiling(size) → {method: hand-craft | bulk-with-scoring, rationale: string}`

**Pole:** Scale-Pole.

**Returns:** whether the list size requires hand-craft or bulk+scoring.

**Threshold:** 50 contacts = upper limit of hand-craft. >50 requires scoring pipeline.

---

## negative_icp_filter(contact)

**Signature:** `negative_icp_filter(contact, neg_icp) → {exclude: bool, reason: string}`

**Pole:** Fit-Pole.

**Returns:** whether to exclude based on negative-ICP criteria.

**Failure mode caught:** Including prospects you'd refuse to sell to.

---

## 90_10_expansion_rule(list)

**Signature:** `90_10_expansion_rule(list, strict_icp_def) → {strict_match_pct: float, expansion_candidates: int, verdict: PASS|FAIL}`

**Pole:** Fit-Pole.

**Returns:** whether the list maintains 90% strict-ICP / 10% high-signal-expansion.

**Failure mode caught:** ICP drift — over-expanding for signal at the cost of fit discipline.

---

## list_decay_check(list_age)

**Signature:** `list_decay_check(age_days) → {decay_rate: float, recommended_action: refresh|re-enrich|discard}`

**Pole:** Cross-pole (Signal + Fit synthesis).

**Returns:** decay rate + action.

**Rule:** 5-10%/month decay from role changes; lists >6mo should re-enrich.

---

## enrichment_audit(list)

**Signature:** `enrichment_audit(list) → {duplicates: int, missing_fields: dict, stale_data_count: int}`

**Pole:** Cross-pole.

**Returns:** quality verdict on enrichment state.

---

## combined_score(signal, icp)

**Signature:** `combined_score(signal_score, icp_score) → {combined: float, priority: high|mid|low}`

**Pole:** Cross-pole synthesis.

**Returns:** ranked combined score for outreach prioritization.

**Formula:** `combined = (signal * 0.6) + (icp * 0.4)`. Signal weighted higher because ICP-only contacts without signal are baseline.

---

## Cross-references

- Bench: [`_bench.md`](_bench.md)
- Attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill: `../SKILL.md`
