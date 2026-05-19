---
date: 2026-05-14
type: frameworks-index
agent: Marketing Director
status: v2
template_version: "2.0.0"
---

# Marketing Director — Frameworks Index

Methodologies indexed by name. Originators in `frameworks_attribution.md`.

---

## voice_corpus_check(artifact)

**Signature:** `voice_corpus_check(artifact, brand_corpus) → {brand_match: 0-100, deviation_flags: [string]}`

**Pole:** Voice-Pole.

**Returns:** how closely the artifact matches the brand's existing voice corpus.

**Failure mode caught:** Brand drift, generic-SaaS phrasing, AI-slop cadences slipping into brand-critical artifacts.

---

## wedge_audit(position)

**Signature:** `wedge_audit(position) → {is_copyable: bool, table_stakes: bool, defensibility_score: 0-10, structural_advantage: string | null}`

**Pole:** Wedge-Pole.

**Returns:** whether the position is genuinely defensible or commodity-claim dressed up.

**Failure mode caught:** "Easiest / fastest / most affordable" framings treated as positions; features framed as wedges.

---

## amplification_math(spend, horizon)

**Signature:** `amplification_math(spend: dollars, horizon_years: int) → {one_year_lift: dollars, three_year_compounding_value: dollars, owned_audience_growth: int}`

**Pole:** Amplification-Pole.

**Returns:** projected lift over multi-year horizon, factoring channel decay.

**Failure mode caught:** Launch-lift-only optimization; campaigns that look good in Q1 and dead in Q5.

---

## generic_saas_audit(copy)

**Signature:** `generic_saas_audit(copy) → {generic_phrases_found: [string], rewrite_suggestions: [string]}`

**Pole:** Voice-Pole.

**Returns:** flags generic SaaS phrases ("we help X do Y," "the leading platform," "transform your business").

---

## ai_slop_detect(copy)

**Signature:** `ai_slop_detect(copy) → {slop_score: 0-10, patterns_found: [string], rewrite: string}`

**Pole:** Voice-Pole.

**Returns:** identifies GPT-default cadences ("In today's competitive landscape," "Whether you're..., or...", em-dash-overuse, three-noun-lists).

**Failure mode caught:** AI-slop drift into brand-critical content.

---

## borrowed_cool_check(positioning)

**Signature:** `borrowed_cool_check(positioning, reference_brand) → {borrowed: bool, fade_horizon: years}`

**Pole:** Voice-Pole.

**Returns:** flags positioning that imitates another brand without organic ownership.

**Failure mode caught:** "We're like Stripe for X" / "Uber for Y" cliché.

---

## table_stakes_check(claim)

**Signature:** `table_stakes_check(claim, competitor_set) → {is_table_stakes: bool, competitors_claiming: int}`

**Pole:** Wedge-Pole.

**Returns:** whether every competitor in the set claims the same thing.

**Failure mode caught:** Treating commodity claims as differentiation.

---

## defensibility_score(position)

**Signature:** `defensibility_score(position) → {score: 0-10, defensibility_source: structural | brand | network | content | none, copy_horizon_years: int}`

**Pole:** Wedge-Pole.

**Returns:** how hard the position is to copy and how long the moat lasts.

---

## owned_audience_growth_check(channel_plan)

**Signature:** `owned_audience_growth_check(plan) → {owned_growth_per_dollar: ratio, paid_to_owned_conversion: float}`

**Pole:** Amplification-Pole.

**Returns:** whether the channel plan grows owned list/community per dollar spent.

**Failure mode caught:** Paid-acquisition strategies that don't build durable audience.

---

## compounding_content_score(content)

**Signature:** `compounding_content_score(content) → {compounding: bool, decay_curve: string, ranking_horizon_months: int}`

**Pole:** Amplification-Pole.

**Returns:** whether content compounds (SEO/AEO, evergreen) or decays (news, trend-jack).

---

## channel_decay_audit(channels)

**Signature:** `channel_decay_audit(channels) → [{channel, decay_rate_yoy, alternative_compounding_channel}]`

**Pole:** Amplification-Pole.

**Returns:** decay assessment per channel + compounding alternatives.

---

## campaign_brief_synthesize(inputs)

**Signature:** `campaign_brief_synthesize(cd_brief, position, audience, channels) → {brief_markdown: string, downstream_dispatches: [agent_brief]}`

**Pole:** Cross-pole synthesis.

**Returns:** the final brief + downstream agent dispatch list.

---

## channel_mix_analyze(channels)

**Signature:** `channel_mix_analyze(channels) → {recommendation: [{channel, allocation_pct, rationale}]}`

**Pole:** Cross-pole.

**Returns:** channel mix with allocation + reasoning.

---

## audience_persona_build(segment)

**Signature:** `audience_persona_build(segment) → {persona: {jtbd, trigger_events, status_quo, narrowest_wedge, future_fit}}`

**Pole:** Cross-pole.

**Returns:** JTBD-based persona (not demographic).

---

## gtm_phase_plan(launch)

**Signature:** `gtm_phase_plan(launch) → {pre_launch: phase, launch: phase, post_launch: phase, risk_register: [risk]}`

**Pole:** Cross-pole.

**Returns:** phased GTM plan with risk register.

---

## Cross-references

- Bench: [`_bench.md`](_bench.md)
- Attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill: `../SKILL.md`
