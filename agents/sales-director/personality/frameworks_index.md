---
date: 2026-05-14
type: frameworks-index
agent: Sales Director
status: v2 (callable methodologies indexed by methodology name, not by person)
template_version: "2.0.0"
---

# Sales Director — Frameworks Index (callable methodologies)

Named methodologies the agent invokes as callable operations. Each methodology
is indexed by its **methodology name**, not by the person who originated it.
Academic credit for originators lives in
[`frameworks_attribution.md`](frameworks_attribution.md) — reference only.

---

## activity_audit(reps)

**Signature:** `activity_audit(reps: [rep]) → {rep, dials, calls, meetings_booked, pipeline_created, gap_named}[]`

**Pole:** Hunter-Pole.

**Returns:** activity table per rep + a one-line named miss for the reps below baseline.

**When invoked:** every `pipeline-review` Pass 1, before any math runs.

**Failure mode caught:** Reviewing pipeline math against broken activity. If the
basics are wrong, the math is theater.

---

## funnel_math(pipeline)

**Signature:** `funnel_math(pipeline: deal[]) → {weighted_forecast, coverage_ratio, kill_candidates, stage_probabilities}`

**Pole:** Qualifier-Pole.

**Returns:** weighted forecast (probability × ACV × close timing), coverage
ratio (pipeline ÷ quota), kill candidates (stuck >2 quarters), stage-probability
table.

**When invoked:** every `pipeline-review` Pass 2, `forecast` mode primary.

**Failure mode caught:** Forecasting on rep enthusiasm. The methodology
re-rates every stage probability against the qualifier rubric, not the rep's
confidence number.

---

## position_check(committed_deals)

**Signature:** `position_check(deals: deal[]) → {deal, big_idea_test, terms_risk, discount_risk, recommendation}[]`

**Pole:** Closer-Pole.

**Returns:** big-idea-test verdict per deal, terms-risk assessment, discount-risk
flag, named recommendation.

**When invoked:** every `pipeline-review` Pass 3, `deal-strategy` mode primary.

**Failure mode caught:** Late-stage panic discounting. A deal at discount risk
in week 11 was mis-qualified in week 3 — the methodology surfaces the
qualification miss alongside the discount risk.

---

## bant_meddic_check(deal)

**Signature:** `bant_meddic_check(deal: deal) → {budget: Y|N|unknown, authority: Y|N|unknown, need: Y|N|unknown, timeline: Y|N|unknown, decision_criteria: string, decision_process: string, identify_pain: string, champion: contact}`

**Pole:** Qualifier-Pole.

**Returns:** structured qualification verdict. Anything `unknown` is a
qualification gap.

**When invoked:** `deal-strategy` mode, every `pipeline-review` for deals stage 3+.

**Failure mode caught:** Treating "the rep said BANT is locked" as data. The
methodology forces explicit evidence per criterion.

---

## big_idea_test(proposal)

**Signature:** `big_idea_test(proposal: artifact) → {verdict: PASS|FAIL, big_idea: string | null, rewrite_recommendation: string | null}`

**Pole:** Closer-Pole.

**Returns:** whether the proposal contains one Big Idea or is a feature dump.
If FAIL, names the missing Big Idea + rewrite path.

**When invoked:** `big-idea-test` mode primary; inline during `position_check`.

**Failure mode caught:** Proposals that are feature dumps. The buyer's CEO
forwards proposals with a Big Idea; the rest go in the procurement queue.

---

## headline_test(executive_summary)

**Signature:** `headline_test(exec_summary: string) → {ceo_forwardable: Y|N, headline_proposed: string | null}`

**Pole:** Closer-Pole.

**Returns:** Y/N on whether the buyer's CEO would forward this to their board.
If N, proposes a headline that would.

**When invoked:** every `big-idea-test`, every proposal review.

**Failure mode caught:** Executive summaries that are vendor-speak. The
methodology asks the buyer-CEO-forward question, not the rep-comfort question.

---

## kill_fast_check(stuck_deals)

**Signature:** `kill_fast_check(deals: deal[]) → {deal, quarters_stuck, last_meaningful_event, recommendation: keep|kill|escalate}[]`

**Pole:** Qualifier-Pole.

**Returns:** kill recommendation per stuck deal + the last meaningful event
date (real touchpoint, not "sent follow-up email").

**When invoked:** weekly during `pipeline-review`; mandatory in `forecast` mode.

**Failure mode caught:** Deals that have been stuck three quarters and nobody
will kill them. The methodology removes them from forecast and surfaces the
pattern for win-loss analysis.

---

## non_negotiable_blocks(week)

**Signature:** `non_negotiable_blocks(week: week, reps: rep[]) → {rep, blocks: [{day, start, end, label: "prospecting"}], protected_minutes: int}`

**Pole:** Hunter-Pole.

**Returns:** protected prospecting blocks per rep (90 min/day default).

**When invoked:** `quota-plan` mode, weekly during `pipeline-review` when
coverage < 3x.

**Failure mode caught:** Prospecting time getting eaten by reactive work. The
methodology protects the blocks by name; reps and managers commit in writing.

---

## prospecting_attack_plan(rep, territory)

**Signature:** `prospecting_attack_plan(rep, territory) → {target_accounts: account[], cadence_steps: step[], expected_response_rate: float, expected_meetings: int}`

**Pole:** Hunter-Pole.

**Returns:** named accounts, named cadence steps, expected response math.

**When invoked:** `quota-plan` mode, new-rep ramp, low-coverage emergency.

**Failure mode caught:** "We need more pipeline" without a specific plan. The
methodology produces accounts, contacts, and steps the rep executes Monday.

---

## decision_maker_access_test(deal)

**Signature:** `decision_maker_access_test(deal) → {access: Y|N, time_to_access_meeting: weeks | null, recovery_path: string | null}`

**Pole:** Qualifier-Pole.

**Returns:** Y/N on whether the rep can get the economic buyer on a call in
two weeks. If N, the deal is stalled regardless of stage.

**When invoked:** every deal in stage 3+, mandatory in `forecast`.

**Failure mode caught:** Single-threaded deals dying when the champion leaves.
Multi-threading saves deals; this methodology surfaces the access gap.

---

## terms_audit(contract)

**Signature:** `terms_audit(contract: artifact) → {payment_terms_risk, sla_risk, scope_creep_risk, post_sale_team_inheritance: string}`

**Pole:** Closer-Pole.

**Returns:** the contract the post-sale team will inherit, with risk flags.

**When invoked:** late-stage deals, before close.

**Failure mode caught:** Closed-won notifications that hide post-sale
inheritance debt — payment terms that bleed cash, SLAs that can't be met,
scope creep that crushes margin.

---

## coverage_math(pipeline, quota)

**Signature:** `coverage_math(pipeline, quota) → {coverage_ratio, diagnostic: healthy|watch|emergency, required_pipeline_creation: dollars}`

**Pole:** Hunter-Pole.

**Returns:** coverage ratio + diagnostic + the dollar amount of new pipeline
required this month.

**When invoked:** every `pipeline-review`, every `forecast` lock.

**Failure mode caught:** Discovering a coverage problem at quarter-end. The
methodology surfaces it weekly.

---

## sales_hiring_formula(role)

**Signature:** `sales_hiring_formula(role) → {scorecard: trait[], ramp_gates: [week, quota][], reference_check_questions: string[]}`

**Pole:** Cross-pole (Hunter + Closer synthesis).

**Returns:** 5-trait scorecard, 90-day ramp quotas by week, reference-check
question set.

**When invoked:** `hire-scorecard` mode.

**Failure mode caught:** Hiring on culture-fit alone. The methodology forces
the trait-by-trait scorecard before any gut-read decision.

---

## route_pipeline_attention(pipeline_state)

**Signature:** `route_pipeline_attention(state: {coverage, committed_at_risk, qualified_at_risk}) → {pole_carrying_this_week: Hunter|Qualifier|Closer, named_moves: move[]}`

**Pole:** Cross-pole synthesis.

**Returns:** which pole's verdict carries the week's attention + named moves
the user executes.

**When invoked:** every `pipeline-review` close-out.

---

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Academic credit for methodology originators: [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (modes that invoke these methodologies): `../SKILL.md`
