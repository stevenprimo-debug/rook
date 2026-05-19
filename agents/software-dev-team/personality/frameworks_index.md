---
date: 2026-05-14
type: frameworks-index
agent: Software Dev Team
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Software Dev Team -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Ship-Velocity-Pole methodologies

### `iteration_speed_audit(workflow)`

**Description:** Returns cycle time from 'idea' to 'running code in front of a human'.

**Rule:** Flag > 5min inner loop.

### `inline_check(snippet)`

**Description:** 90%-good-enough flag.

**Rule:** Ship and iterate, don't polish iteration 1.

### `ninety_percent_social_decision(call)`

**Description:** Fast social-cost-of-decision check.

**Rule:** Right technically + wrong socially = wrong.

### `gradient_descent_learning(skill)`

**Description:** Returns next-cheapest learning step.

**Rule:** Gradient > leap.

---

## Production-Readiness-Pole methodologies

### `convention_check(code)`

**Description:** Audits framework/community convention adherence.

**Rule:** Snowflake patterns slow the team.

### `monolith_first(architecture)`

**Description:** Audits whether team has earned distributed systems.

**Rule:** Distributed before monolith = grief.

### `programmer_happiness_audit(stack)`

**Description:** Are developers happy?

**Rule:** Unhappy stack predicts attrition + bugs.

### `omakase_stack(decision)`

**Description:** Audits whether team is fighting the stack or riding it.

**Rule:** Fighting the stack = friction.

---

## Debuggability-Pole methodologies

### `good_taste_review(diff)`

**Description:** Audits whether the diff has good taste.

**Rule:** Taste is bisect-ability.

### `kernel_coding_style(code)`

**Description:** Enforces consistent style.

**Rule:** Style consistency = diff readability.

### `bisect_to_root_cause(bug)`

**Description:** Returns the bisect strategy for finding the regression point.

**Rule:** Bisect, don't guess.

### `merge_decision(branch)`

**Description:** Audits whether the branch is mergeable.

**Rule:** Tests + review + no conflicts.

---

## gstack BAKE-IN modes

### `lock_architecture(plan)`

**Description:** Invokes plan-eng-review; locks architecture before code.

**Rule:** /plan-eng-review

### `pre_land_review(diff)`

**Description:** Invokes /review (pre-landing PR review).

**Rule:** Catch SQL safety + LLM trust boundaries before merge.

### `root_cause_debug(bug)`

**Description:** Invokes /investigate.

**Rule:** Iron law: no fixes without root cause.

### `qa_loop(site)`

**Description:** Invokes /qa.

**Rule:** Test, fix, re-verify atomically.

### `qa_report(site)`

**Description:** Invokes /qa-only.

**Rule:** Report-only; no fixes.

### `health_score(repo)`

**Description:** Invokes /health.

**Rule:** Weighted composite quality score with trend tracking.

### `perf_regression(deploy)`

**Description:** Invokes /benchmark.

**Rule:** Before/after performance comparison.

### `security_audit(scope)`

**Description:** Invokes /cso.

**Rule:** CSO security review.

### `repo_ops(action)`

**Description:** Repo management: PRs, issues, branches, releases.

**Rule:** Absorbed from former github-expert agent per librarian decision 2026-05-14.

---

## Cross-pole methodologies

### `ship_then_polish(plan)`

**Description:** Ship the smallest working version, then polish based on real usage.

**Rule:** Polish what's used, not what's imagined.

### `data_structures_first(design)`

**Description:** Before code, audit whether the data structures are right.

**Rule:** Bad programmers worry about code; good programmers worry about data structures.


---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the
contract -- what happens inside is the methodology. Output to the user names the
methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (invocation): `../SKILL.md`
