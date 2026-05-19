# ROOK

**The Agentic OS for solo operators and small teams. Built on Claude.**

ROOK is the coordination layer that sits above your agents and runs them as a system. Twenty specialists, one orchestrator, one memory custodian. Each agent ships with a master skill, a customer-extensible voice library, and the universal file → knowledge → vault → export pipeline baked in.

Without a coordination layer, you have agents. With one, you have a system.

## The 5 things an Agentic OS manages

| Component | What it answers | How ROOK delivers it |
|---|---|---|
| **Orchestration** | Who handles what? | chief-of-staff routes every session; cross-dept routing enforcer fires on every prompt |
| **Memory** | What gets remembered? | 4-tier memory model per agent (vector + graph / SQLite / vectorless PDF / markdown+grep) |
| **Context** | What does each agent know? | Per-agent `SKILL.md` + `context/YYYY-MM/` + the recursive Context Loop |
| **Specialization** | How do agents compose? | 20 agents with structured interfaces via the master template + routing manifest |
| **Feedback** | How does the system get better? | Compounding-append memory + librarian weekly sweep + contradiction surfacing |

Most agent products give you one of these. ROOK gives you all five.

## The 4 pillars

```
PrimoLabs_PoweredByClaude/
├── .claude/                <- Project config
│   ├── agents/             <- Anthropic-canonical subagent definitions
│   ├── skills/             <- Shared skill library (core + registry + templates)
│   ├── rules/              <- Path-scoped CLAUDE.md fragments
│   └── settings.json
├── CLAUDE.md               <- Top-level routing
├── agents/                 <- 20 shippable agents
├── projects/               <- Job-shaped work area
├── hooks/                  <- Routing enforcer, memory audit, session hooks
└── _archive/               <- Superseded content (append-only, never deleted)
```

Personal user state (accounts, schedule, family events) lives OUTSIDE this folder at `~/.claude/CLAUDE.md` per Anthropic canonical pattern. Personal context never ships with the agents.

## The 20 agents

**Operations:** chief-of-staff · librarian
**Revenue:** sales-director · sales-outreach · prospecting-agent · shopify-agent
**Marketing:** marketing-director · content-strategist · social-media-manager · seo-specialist
**Creative:** creative-director · designer · copywriter
**Research:** deep-researcher
**Build:** product-manager · software-dev-team · engineering-lead
**Lab:** r-and-d-lead
**Finance:** finance-manager · trading-analyst

Chief of Staff and Librarian are the power pair: orchestrator + memory custodian. Every session passes through them. The other eighteen are domain specialists.

## Universal stack (every agent inherits)

| Capability | Tool | What it does |
|---|---|---|
| Input | markitdown | PDF / DOCX / XLSX / audio / video → clean markdown |
| Synthesis | graphify | Markdown corpus → knowledge graph |
| Vault I/O | obsidian-cli | Programmatic read/write to your vault |
| Output | html2pdf | HTML → seamless single-page PDF |
| Skill authoring | skill-creator | Every agent can scaffold new child skills |

## Voice modes

Every agent ships with a default voice plus a `personality/voice_modes/` directory the customer extends. Drop a `<your-mode>.md` into the folder, set `{voice_mode}=<your-mode>` at invocation, and the agent loads that file as its voice spine for the session.

## Install

[Install instructions — see `INSTALL.md`]

## License

MIT (curated catalog — not accepting external contributions; fork freely).
