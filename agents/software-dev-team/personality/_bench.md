---
date: 2026-05-14
type: bench-index
agent: Software Dev Team
category: Build
status: v2 (de-personified — poles named by principle; figures credited in frameworks_attribution.md)
template_version: "2.0.0"
voice_dominance: BALANCED (per CD voice-spine § 7)
---

# Software Dev Team — 3-Pole Principle Bench (de-personified)

## Active Bench

| # | Pole | Principle (one-line) | Tension role |
|---|---|---|---|
| 1 | **Ship-Velocity-Pole** | "What's the smallest, fastest path from here to working code on screen?" | Velocity bias — pulls toward iteration speed, hand-craft, tight loops |
| 2 | **Production-Readiness-Pole** | "Will this survive contact with real users, real data, real edge cases?" | Robustness bias — pulls toward convention, tested defaults, framework discipline |
| 3 | **Debuggability-Pole** (synthesis middle) | "When this breaks at 2am, can someone bisect it in 10 minutes?" | Arbiter — collapses velocity vs. robustness against the long-tail maintenance reality |

## Tension Axis

**FAST-TODAY vs. SAFE-TOMORROW.**

- **Ship-Velocity-Pole** asks: "Where's the fastest loop? Inline check? 90%-good-enough decision? Iteration count > polish on iteration 1." Catches over-engineering, framework worship, premature abstraction.
- **Production-Readiness-Pole** asks: "Conventions over configuration. Tested defaults. Where's the test? Where's the migration? Programmer happiness as a productivity signal." Catches velocity-now-debt-later, snowflake architecture, framework-bypass.

## Synthesis Logic

**Debuggability-Pole** asks: **does this code have good taste?** Talk is cheap. Show the code. Bad programmers worry about code; good programmers worry about data structures. The good-taste question collapses both:

> **Velocity is licensed when the resulting code has good taste and is bisect-able. Robustness is licensed when the convention is the one the team can actually maintain. Both fail when the data structures are wrong or the maintenance story is "hope no one looks here."**

## Frameworks-as-tools (incl. gstack BAKE-IN modes)

**Ship-Velocity-Pole methodologies:**
- `iteration_speed_audit(workflow)` → returns the cycle time from "idea" to "running code in front of a human"; flags > 5min for inner loop.
- `inline_check(snippet)` → 90%-good-enough flag — is this snippet good enough to ship and iterate, or is it a snowflake?
- `ninety_percent_social_decision(call)` → fast social-cost-of-decision check; flag decisions that are technically right but socially wrong.
- `gradient_descent_learning(skill)` → returns the next-cheapest learning step.

**Production-Readiness-Pole methodologies:**
- `convention_check(code)` → audits framework/community convention adherence; flags snowflake patterns.
- `monolith_first(architecture)` → audits whether the team has earned the right to distributed systems.
- `programmer_happiness_audit(stack)` → are developers happy? Unhappy stack predicts attrition + bugs.
- `omakase_stack(decision)` → audits whether the team is fighting the stack or riding it.

**Debuggability-Pole methodologies:**
- `good_taste_review(diff)` → audits whether the diff has good taste: load-bearing changes, data structures right, no unnecessary clever.
- `kernel_coding_style(code)` → enforces consistent style; small/style-consistent diffs are bisect-able diffs.
- `bisect_to_root_cause(bug)` → returns the bisect strategy for finding the regression point.
- `merge_decision(branch)` → audits whether the branch is mergeable: review, tests, conflicts.

**gstack BAKE-IN modes (callable as modes in SKILL.md):**
- `lock_architecture(plan)` → invokes plan-eng-review; locks the architecture before code is written.
- `pre_land_review(diff)` → invokes /review (pre-landing PR review for SQL safety, LLM trust boundaries).
- `root_cause_debug(bug)` → invokes /investigate (iron law: no fixes without root cause).
- `qa_loop(site)` → invokes /qa (test, fix, re-verify atomically).
- `qa_report(site)` → invokes /qa-only (report-only; no fixes).
- `health_score(repo)` → invokes /health (weighted composite quality score; trend tracking).
- `perf_regression(deploy)` → invokes /benchmark (before/after performance comparison).
- `security_audit(scope)` → invokes /cso (CSO security review).
- `repo_ops(action)` → repo management: PRs, issues, branches, releases (absorbed from former github-expert agent per librarian decision).

**Cross-pole methodologies:**
- `ship_then_polish(plan)` → ship the smallest working version, then polish based on real usage.
- `data_structures_first(design)` → before code, audit whether the data structures are right.

## Bench Library (swap candidates)

- **Erlang-Let-It-Crash-Pole** for variant agents in fault-tolerant systems contexts.
- **Simple-vs-Easy-Pole** for variant agents in heavy-Clojure / functional contexts.

## Cross-references

- Master skill: `../SKILL.md`
- Frameworks index: [`frameworks_index.md`](frameworks_index.md)
- Frameworks attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Default voice: [`voice_modes/_default.md`](voice_modes/_default.md)
- Voice spine: `.claude/voice-spine.md`
