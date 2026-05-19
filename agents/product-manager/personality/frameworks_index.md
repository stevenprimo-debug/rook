---
date: 2026-05-14
type: frameworks-index
agent: Product Manager
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Product Manager -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Jobs-to-be-Done-Pole methodologies

### `problem_over_feature(spec)`

**Description:** Flags features without a named customer problem.

**Rule:** No problem = no product.

### `discovery_vs_delivery(team_state)`

**Description:** Returns team's current discovery health; flags discovery debt.

**Rule:** Discovery debt = wrong-feature risk.

### `risk_framework(initiative)`

**Description:** Maps risk across value, usability, feasibility, business viability.

**Rule:** All four matter; usually one dominates.

---

## Scope-Restraint-Pole methodologies

### `opportunity_solution_tree(outcome)`

**Description:** Maps outcome -> opportunities -> solutions -> experiments; flags missing branches.

**Rule:** Tree before sprint.

### `continuous_interviewing(week)`

**Description:** Audits whether team hits 1 customer interview/week minimum.

**Rule:** Cadence prevents discovery debt.

### `assumption_test_design(solution)`

**Description:** Returns the cheapest experiment that tests the riskiest assumption.

**Rule:** Test the assumption, not the feature.

---

## Shippability-Pole methodologies

### `purpose_people_process(team)`

**Description:** Audits three preconditions for team health.

**Rule:** All three or none of three.

### `feedback_specificity(critique)`

**Description:** Vague feedback is useless; returns rewrites.

**Rule:** Name the behavior, not the trait.

### `one_on_one_quality_check(cadence)`

**Description:** Audits PM-to-engineer feedback loop quality.

**Rule:** 1-on-1 is the leverage point.

---

## Cross-pole methodologies

### `team_topology_check(scope)`

**Description:** Does the team have the shape to ship this scope?

**Rule:** Shape matches scope, or scope matches shape.

### `outcome_vs_output(roadmap)`

**Description:** Audits whether the roadmap measures outcomes or output.

**Rule:** Output is the trap.


---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the
contract -- what happens inside is the methodology. Output to the user names the
methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (invocation): `../SKILL.md`
