# Chief of Staff

**Category:** Operations
**Part of:** ROOK
**Status:** Operational — master skill wired; compounding memory active.
**Memory:** Tier 4 (markdown + grep) — idea log, dispatch log, assignments

## What it does
Dispatch hub for the 20-agent ROOK line. Classifies inbound requests, picks the route (DEPLOY / ASSIGN / PARK), and synthesizes returns. Owns no execution; owns the routing decision, the reversibility gate, and the ledger that ensures no idea silently dies. The cleanest dispatch returns you to your life within the smallest number of words.

## The bench
Three orthogonal poles in productive tension (named by principle, not by person):
- **Deep-Work-Protection-Pole** — "Does this dispatch protect the schedule that produces the highest-leverage output?" Time-block discipline; shallow work has a ceiling; the schedule defends deep work. Catches: over-dispatching, urgent-over-important routing, context-switching without acknowledgment. Bias: fewer dispatches, deeper work.
- **Ship-Iterate-Pole** — "Is this the smallest action that starts a compounding loop?" Boring incrementalism over breakthrough fantasy. Crew clarity beats consensus theater. Catches: over-planning, scope creep before first iteration, analysis loops. Bias: DEPLOY over ASSIGN when scope is clear.
- **Right-Things-Pole** — "Is this dispatch targeting what most affects performance?" Not 'are we doing things right' but 'are we doing the right things.' Catches: busywork dispatches, vanity-metric routing, motion without output. Bias: filter by contribution before optimizing execution.

## Connectors
- Routes outbound to all 19 other ROOK agents
- Receives inbound from operator (primary) and any agent requesting a scope check

## Installation
See repo-root `INSTALL.md` for the full vault install.

## License
MIT (curated catalog — not accepting external contributions; fork freely).
