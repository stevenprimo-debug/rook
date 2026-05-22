# ROOK / Agents

The 20 shippable agents that make up the ROOK product line.

## The 20 agents (by category)

- **Operations** — chief-of-staff · librarian · account-manager · inbox-manager
- **Revenue** — sales-director · shopify-agent
- **Marketing** — marketing-director · content-strategist · social-media-manager · seo-specialist
- **Creative** — creative-director · designer · copywriter
- **Research** — deep-researcher
- **Build** — product-manager · software-dev-team · engineering-lead
- **Lab** — r-and-d-lead
- **Finance** — finance-manager · trading-analyst

Authoritative roster: [.claude/agents/_ROSTER.md](../.claude/agents/_ROSTER.md) (and the filesystem children of this folder). If this list disagrees with `_ROSTER.md`, `_ROSTER.md` wins.

## Sub-skills (not peer agents)

`sales-director/skills/outreach/` and `sales-director/skills/prospecting/` are child skills under sales-director — not standalone agents. Outreach generates cold emails; prospecting builds account lists. Both are invoked from inside sales-director's `closing` and `discovery` modes.

## Per-agent contract (5 required items)

Each agent ships with:

1. `CLAUDE.md` — routing scope (load-on-demand context rules + cross-dept delegation)
2. `SKILL.md` — master skill body (3-pole bench, parameters, routing keywords, the prompt, worked examples)
3. `personality/_bench.md` — 3-pole principle bench (depersonified — named by principle, not by figure)
4. `personality/frameworks_index.md` — methodology references the agent invokes
5. `personality/frameworks_attribution.md` — academic credit for borrowed methodology
6. `memory/` — agent-written learned state (librarian-audited via weekly sweep)
7. `context/` — optional human-curated reference material (loaded on session start)
8. `README.md` — public-facing description

AEO was folded into seo-specialist on 2026-05-14 — one agent, two benches (SEO mode + AEO mode), parameter-switched.

## Voice umbrella

All 20 agents inherit the ROOK voice spine: [.claude/voice-spine.md](../.claude/voice-spine.md). Banned vocabulary, lead-with-the-move discipline, no-preamble rule, anti-AI-slop posture all locked there.

## Routing

The cross-agent routing manifest is at [hooks/routing-rules.json](../hooks/routing-rules.json). Each agent's `## Routing Keywords` block in their SKILL.md is the canonical source — the manifest is an auto-mirror. Edit SKILL.md, run `python scripts/regenerate-routing-rules.py`.

## Master template

Every agent inherits the **ROOK Master Skill Template v2** at [_template/SKILL.md](_template/SKILL.md). New agents scaffold from this template (or invoke the bundled `skill-creator` at `.claude/skills/core/skills/skill-creator/`). Full positioning doc at [_template/README.md](_template/README.md).

## Cross-references

- [`.claude/agents/_ROSTER.md`](../.claude/agents/_ROSTER.md) — authoritative agent slug list
- [`.claude/voice-spine.md`](../.claude/voice-spine.md) — org-wide voice contract
- [`hooks/routing-rules.json`](../hooks/routing-rules.json) — routing manifest (auto-mirrored from each agent's SKILL.md)
- [`agents/_template/SKILL.md`](_template/SKILL.md) — Master Skill Template v2 (every agent inherits)

## License

MIT — curated catalog. Fork freely; external contributions not accepted (per the no-contribution lock, 2026-05-12).

---

<sub>Powered by [Claude](https://www.anthropic.com/claude) · Built by [PrimoLabs](https://primolabs.ai)</sub>
