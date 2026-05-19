# Vault Provenance — What You Just Installed

> A receipt. Everything that ships with ROOK, what it does, where it lives.

ROOK is not a chatbot wrapper. It is an **Agentic OS** — the coordination layer that sits above your agents and manages how they work together: what each one knows, who handles what, what gets remembered, and what happens when something fails. Without a coordination layer, you have agents. With one, you have a system.

This file enumerates what's in the box so you understand what your subscription is paying for.

## The 5 components of an Agentic OS — and where each lives in ROOK

| Component | What it does | Where it lives |
|---|---|---|
| **Orchestration** | Routes every session to the right agent; enforces upstream dispatch chains | `agents/chief-of-staff/` + `hooks/routing-enforcer.{ps1,sh}` + `hooks/routing-rules.json` |
| **Memory** | Per-agent memory tier (synth / structured / document / default) declared in SKILL.md frontmatter; librarian audits + prunes weekly | `agents/<agent>/memory/` + `agents/librarian/` + `hooks/librarian-weekly-sweep.{ps1,sh}` |
| **Context** | Recursive capture → ingest → route → read → prune loop; each agent loads its scoped context on session start | `context-loop.md` + `agents/<agent>/context/` + `.claude/skills/registry/inbox-routing/` |
| **Specialization** | 20 agents with structured interfaces, principle-bench debate before verdict, customer-extensible voice library | `agents/<each>/SKILL.md` + `agents/_template/SKILL.md` + `.claude/skills/registry/` |
| **Feedback** | Compounding-append memory (never silent overwrite); contradiction surfacing; weekly Monday digest from the librarian | `agents/*/memory/*.md` (HEAD blocks) + `agents/librarian/SKILL.md` weekly-sweep mode |

ROOK has all five. Most agent products ship one and call it done.

---

## The four pillars

```
.claude/        ← Project config (Anthropic-canonical)
agents/         ← 20 hardened agents, each with master skill + bench + voice library
projects/       ← Job-shaped work space (you bring the projects)
hooks/          ← Runtime enforcement that fires on every prompt
```

Plus `_archive/` (append-only history, never deleted) and `CLAUDE.md` (top-level routing contract).

---

## The 20 agents

Each agent ships with:

- A **master skill** (`SKILL.md`) — the operating brain, typically 700–1,200 lines of locked decision logic
- A **3-pole principle bench** (`personality/_bench.md`) — three orthogonal principles held in productive tension. Bench is named by principle, not by person. Originators credited in `personality/frameworks_attribution.md`.
- A **customer-extensible voice library** (`personality/voice_modes/`) — out-of-box `_default.md` voice plus scaffolding for you to author `<custom>.md` modes (your brand, your favorite operator's voice, your team register)
- A **frameworks index** (`personality/frameworks_index.md`) — named methodologies the agent invokes
- **Agent-specific skills** baked into the frontmatter (the registry skills curated for that agent's domain)
- **Memory** (`memory/`) — agent-written learned state, librarian-audited
- **Context** (`context/`) — human-curated reference material, loaded on every session start

| Category | Agents |
|---|---|
| Operations | chief-of-staff · librarian |
| Revenue | sales-director · sales-outreach · prospecting-agent · shopify-agent |
| Marketing | marketing-director · content-strategist · social-media-manager · seo-specialist |
| Creative | creative-director · designer · copywriter |
| Research | deep-researcher |
| Build | product-manager · software-dev-team · engineering-lead |
| Lab | r-and-d-lead |
| Finance | finance-manager · trading-analyst |

**chief-of-staff** is the front door — the orchestrator that classifies and routes. **librarian** is the flywheel — the memory custodian that compounds your vault and prunes it weekly. These two are the meta layer; the other 18 are domain specialists.

---

## The universal stack (baked into every agent)

Every one of the 20 agents inherits the same canonical file → knowledge → vault → output pipeline:

| Layer | Tool | What it does |
|---|---|---|
| Input | `markitdown` | Any file (PDF, DOCX, XLSX, PPT, audio, video, YouTube, image-with-OCR, EPub, ZIP) → clean markdown |
| Synthesis | `graphify` | Markdown corpus → queryable knowledge graph |
| Vault I/O | `obsidian-cli` | Programmatic read/write to your Obsidian vault |
| Output | `html2pdf` | HTML deliverable → seamless single-page PDF |
| Skill authoring | `anthropic-skills:skill-creator` | Every agent can scaffold new child skills |

No agent re-implements these. All 20 call the same canonical wrappers.

---

## The skills library

`.claude/skills/` ships with three layers:

- **`core/`** — the universal-stack skills (markitdown, graphify, obsidian-cli, html-to-pdf) plus shared utilities (audit-memory-skills, auto-skill-builder, cookbook-lookup, docx, frontend-design, pdf, pptx, prompt-builder, schedule, skill-creator, xlsx)
- **`registry/`** — domain-specific skills baked into agents (apollo-prospect-search, brainstorming, claude-design-skill, competitive-scan, deal-economics, design-for-ai, dispatching-parallel-agents, drawing-reader, freecad-mcp, frontend-design, gsap-skills, icp-fit-scorer, ict-pattern-detector, inbox-routing, nesting-engine, outreach-drafter, pine-script-template, pnl-tracker, risk-1pct-calculator, seo-audit-quick, shopify-polaris-component, source-credibility-check, subagent-driven-development, systematic-debugging, test-driven-development, topic-cluster-strategist, trading-dashboard-builder, ui-ux-pro-max-skill, unreal-baseline-skillset, using-git-worktrees, verification-before-completion, writing-skills, and ~30 more)
- **`templates/`** — contract scaffolds for the work agents actually produce (msa-template, nda-template, proposal-template, sop-template, sow-template, plus AMA multi-agent template variants for cold-outreach, deep-researcher, e-commerce-ops, lead-to-deal-pipeline, meta-ads-creative-critic, research-then-write, sales-triage, seo-keyword-research)

---

## The Context Loop

The architecture that makes ROOK compound with use. Five stages, recursive:

```
CAPTURE → INGEST → ROUTE → READ → PRUNE → (back to capture)
```

Full detail in [`context-loop.md`](context-loop.md). The librarian closes the loop; without the librarian, the loop is open and the vault drifts. With the librarian, the loop holds.

---

## The hooks layer

`hooks/` ships with the runtime enforcement that makes the system work even when you're not paying attention:

- **routing-enforcer** — reads `routing-rules.json` on every prompt and fires the right agent's brief
- **session-prelude** — auto-injects context on session start (recent files, locked decisions)
- **vault-context-injector** — keyword-matches the prompt against your vault and surfaces relevant prior notes
- **session-end-detect** — natural-language detection of session-end signals ("signing off", "wrap up", etc.); injects a "write final handoff" reminder before goodbye
- **precompact-handoff** — fires when Claude Code is about to compact the context window; injects instruction to write a structured session summary to `agents/chief-of-staff/memory/session_handoffs/` before context drops
- **librarian-weekly-sweep** — cron trigger for the librarian (Sunday night)
- **dispatch-chains** — enforces upstream dispatch for design/copy/brand work (creative-director → marketing-director → designer/copywriter)

One-time install via `hooks/INSTALL.ps1` (Windows) or `hooks/INSTALL.sh` (Mac/Linux). Idempotent — safe to re-run.

---

## The voice spine

Every agent inherits a single org-wide voice contract: anti-AI-slop, anti-warmth-default, anti-bullet-list-as-default-output, anti-named-figure-invocation. The spine guarantees ROOK doesn't sound like a chatbot regardless of which agent you're talking to.

Customer extensibility: each agent has a `personality/voice_modes/` directory that ships with `_default.md`. You add `<custom>.md` files there to make agents speak in your brand voice, your favorite operator's register, or your team's house style. The customization is what the cohort teaches.

---

## The compounding-append memory pattern

ROOK never silently overwrites memory. Every update appends a versioned entry with timestamp. The HEAD (current best) lives in a pinned `## For future Claude` block at the top of each memory file. The history below it is the audit trail.

Contradictions surface as questions for you to lock, not as silent rewrites. The librarian's contradiction map (in the weekly digest) surfaces files that disagree with each other so you can decide which version is canonical.

---

## What this means at the subscription tier

You are paying for:

1. **The 20 agents** — each with hardened master skills, principle benches, voice libraries
2. **The Context Loop** — the recursive context system that compounds with use
3. **The librarian flywheel** — the weekly sweep + Monday digest that proves the loop is working
4. **The skills library** — the curated registry baked into the right agents
5. **The hooks layer** — runtime enforcement that fires automatically
6. **The voice spine + frameworks index** — the anti-slop, anti-warmth-default voice contract
7. **The master template v2** — every agent can scaffold new child skills as you discover patterns
8. **The compounding-append memory pattern** — your knowledge compounds; nothing silent-overwrites

The 20 agents are the surface. The system underneath them is the product.

---

## Cross-references

- [`README.md`](README.md) — the public-facing intro
- [`CLAUDE.md`](CLAUDE.md) — the top-level routing contract
- [`context-loop.md`](context-loop.md) — the named architecture (the substrate)
- [`agents/librarian/prune-policy.md`](agents/librarian/prune-policy.md) — customer-tunable pruning rules
- [`.claude/agents/_ROSTER.md`](.claude/agents/_ROSTER.md) — the canonical 20-agent list
- [`agents/_template/SKILL.md`](agents/_template/SKILL.md) — the master template every agent inherits
