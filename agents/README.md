# your product / Agents

The 20 shippable agents that make up the/ROOK product line.

## Categories (matching yourcompany.com/agents)

- **Operations** — Chief of Staff
- **Revenue** — Sales Outreach, Prospecting Agent, Sales Director, Shopify Agent
- **Marketing** — Marketing Director, Content Strategist, Social Media Manager, SEO Specialist, AEO Specialist
- **Creative** — Creative Director, Designer, Copywriter
- **Research** — Deep Researcher
- **Build** — Product Manager, Software Dev Team
- **Lab** — R&D Lead
- **Finance** — Finance Manager, Trading Analyst
- **Platform** — GitHub Expert (internal/operational — not on website)

## Custom Roles
Custom Roles is a **website CTA** (contact form), not an agent folder.

## Architecture

Each agent follows the same shape:
- `CLAUDE.md` — routing + scope
- `SKILL.md` — master skill with modes (operational)
- `personality/` — 3-tastemaker bench (polar + polar + middle); each figure has `_profile.md`, `frameworks.md`, `quotes.md`, `speak_as.md`
- `context/` — bundled curated knowledge (RAG corpus later)
- `memory/` — compounding institutional knowledge per agent
- `README.md` — public-facing description

## Voice umbrella
All 20 agents inherit the ROOK voice spine:
`.claude/voice-spine.md`

## Philosophy bench (system-level, inherited via Chief of Staff)
- **Naval Ravikant** — leverage, specific knowledge, long-term games
- **James Clear** — atomic habits, identity-based change, systems > goals
- **Cal Newport** — deep work, slow productivity, "do less, deeper"

## Build status
- [x] Skeleton — folders + stubs for all 20 agents (2026-05-12)
- [ ] Designer — first complete agent (reference build, in progress)
- [ ] Remaining 19 — populated per-agent over time

## Relationship to agents/
`agents/` is the operator's internal workspace and stays unchanged.
`Agents/` is the shippable product. Master-skill PATTERNS may be borrowed from `agents/`; raw content (your employer client data, personal context) does NOT cross over.

## License
MIT — curated catalog. Fork freely; external contributions not accepted (per the no-contribution lock, 2026-05-12).
