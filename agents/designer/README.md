# Designer

**Category:** Creative
**Part of:** ROOK
**Status:** Operational (v2.0.0).
**Memory:** Tier 4 (markdown) — waivers log, exemplars log, joy-neutral log, locked-standard cross-references

## What it does

Reviews visual surfaces before they ship and refuses the quietly-off ones. Proposals, decks, landing pages, dashboards, brand marks, icons, signage, motion — the agent runs every surface through three passes (Restraint gates, Expression joy-check, Care audit) and returns a verdict, an appendix, and the single next move. No "let me look at this." First line is the gate table, the verdict, or the cut.

Also produces, when asked — but only after creative-director and marketing-director briefs are loaded. Cold-design dispatches on branded surfaces are refused; the chain enforces the playbook for a reason. Visual Storyteller stack (claude-design-skill, design-for-ai, frontend-design, gsap-skills, ui-ux-pro-max-skill) is inherited and auto-loaded.

## The bench

Three poles in productive tension (named by principle, not by person; originators credited in `personality/frameworks_attribution.md` and never invoked in output):

- **Restraint-Pole** — "Does every element on this surface justify itself?" Runs the 10 binary gates. Catches decorative gradients, fourth type weights that don't earn the hierarchy, color counts above three families, template chrome no one chose. Bias: less, but better — and partial passes are failures.
- **Expression-Pole** — "Has the work earned its joy?" NEUTRAL is the failure mode, not the safe middle. Catches professionally-competent-no-personality work, brand-by-template execution, beige-by-default. Bias: beauty IS function; one moment of expression earned beats none.
- **Care-Pole** (synthesis middle) — "Did the maker honor the unseen?" Audits alt text, PDF metadata, HTML title, focus states, empty states, mobile reflow, slow-network behavior. Arbitrates Restraint vs. Expression by asking whether both were the result of intentional craft or accidental defaults. Bias: simplicity is the consequence of care, never the goal.

## Connectors

- `(none required)` — outputs are HTML, PDF, image files, and verdicts written to `context/`. No external service calls in standard mode.

## Installation

See repo-root `INSTALL.md` for the full vault install. Per-agent install runs automatically when the vault is installed — no separate agent install step.

## License

MIT (curated catalog — not accepting external contributions; fork freely).
