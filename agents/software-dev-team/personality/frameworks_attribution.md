---
date: 2026-05-14
type: frameworks-attribution
agent: Software Dev Team
status: academic-reference-only (NEVER invoked in agent output)
---

# Software Dev Team -- Frameworks Attribution (academic credit)

This file credits the originators of each methodology in [`frameworks_index.md`](frameworks_index.md).
**The agent does not invoke these names in output.** Methodologies are called by methodology name.

This file exists for:
1. Academic integrity -- the methodologies are not original to this agent.
2. Cohort lesson reference -- students learn the source material to understand the methodology.
3. Customer extension -- when building variant agents, the originator's corpus is the place to study.

## Bench composition

**Active bench:** Ship-Velocity / Production-Readiness / Debuggability

## Methodology originators

### Ship-Velocity-Pole methodologies

John Carmack -- iteration speed, inline checks, 90% social decision, gradient descent learning.

### Production-Readiness-Pole methodologies

DHH (David Heinemeier Hansson) -- convention over configuration, monolith first, programmer happiness, omakase stack.

### Debuggability-Pole methodologies

Linus Torvalds -- good taste, kernel coding style, bisect-to-root-cause, merge decision.

### gstack BAKE-IN modes

gstack v1+ skills (lock-architecture, pre-land-review, root-cause-debug, qa-loop, qa-report, health-score, perf-regression, security-audit) -- Brian Cui / gstack project. repo-ops absorbs former github-expert capability per librarian decision 2026-05-14.

### Cross-pole synthesis

Ship-then-polish synthesizes Carmack iteration speed + Linus taste. Data-structures-first -- Linus's 'bad programmers worry about code' aphorism.

## Customer extension

If a customer wants to build a variant Software Dev Team with different bench figures:

1. Choose 3 figures whose methodologies map to the active pole composition (or alternative pole compositions from the Bench Library in `_bench.md`).
2. For each figure, identify 3 named methodologies they originated.
3. Update `frameworks_index.md` with the new methodology names + specs.
4. Update this file with the new originator credits.
5. The principle-poles themselves don't change. The methodologies underneath them do.

## Cross-references

- Frameworks index (callable methodologies): [`frameworks_index.md`](frameworks_index.md)
- Bench composition: [`_bench.md`](_bench.md)
- Master skill: `../SKILL.md`
