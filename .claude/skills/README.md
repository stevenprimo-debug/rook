# this system — Skills Library

> Every this agent ships with this curated library of operator-grade skills. Agents invoke them automatically; you can also call them directly as slash commands in Claude Code.

Skills are progressive-disclosure tools — small SKILL.md files with metadata that load only when their triggers fire. They turn recurring patterns into reusable capabilities so you (and the agents) never re-solve the same problem.

---

## Universal Stack (every agent inherits these 4)

Every agent shipped with this system declares these four skills in its frontmatter. They form the input-synthesis-output loop the agents rely on.

| Skill | Path | What it does | When an agent uses it |
|---|---|---|---|
| `markitdown` | (Universal Stack) | Convert any file (PDF / DOCX / XLSX / PPT / audio / video / YouTube / EPub / images-OCR / ZIP) into markdown the agent can reason over | INPUT — any time the user drops a file |
| `graphify` | (Universal Stack) | Turn markdown into a knowledge graph for synthesis across docs | SYNTHESIS — when an agent needs to connect concepts across many sources |
| `obsidian-cli` | (Universal Stack) | Programmatic read/write to the user's Obsidian vault | VAULT I/O — when work needs to land in the user's second brain, not just the chat |
| `html2pdf` | `core/html-to-pdf/` | Convert standalone HTML to seamless single-page PDFs (no page breaks, no pagination artifacts) | OUTPUT — when a polished, shareable PDF is the final artifact |

---

## Document Format Library

Reading, editing, and producing standard business document formats.

| Skill | Path | What it unlocks |
|---|---|---|
| `pdf` | `core/skills/pdf/` | Read, extract, merge, split, watermark, OCR, and fill PDFs |
| `pptx` | `core/skills/pptx/` | Create and edit PowerPoint decks with proper layouts, themes, and chart embedding |
| `xlsx` | `core/skills/xlsx/` | Open, clean, and produce spreadsheets — formulas, formatting, charts, multi-sheet workbooks |
| `docx` | `core/skills/docx/` | Generate and edit Word documents — headings, tables, page numbers, letterheads, tracked changes |

---

## Design Library

Production-grade visual work. Agents that produce visible surfaces load these.

| Skill | Path | What it unlocks |
|---|---|---|
| `frontend-design` | `core/skills/frontend-design/` | Distinctive, production-grade frontend interfaces. Anti-slop taste enforcement — avoids the generic AI aesthetic |
| `design-for-ai` | `registry/design-for-ai/` | Color, type, composition, and hierarchy critic. Has CHECKER + APPLIER modes for review-then-fix loops |
| `gsap-skills` | `registry/gsap-skills/` | The official GreenSock animation pack — 8 sub-skills covering core, plugins, ScrollTrigger, React, frameworks, performance, timeline, and utils |

---

## CAD / Engineering

For agents that read technical drawings or operate CAD tooling.

| Skill | Path | What it unlocks |
|---|---|---|
| `drawing-reader` | `registry/drawing-reader/` | Extract equipment lists and model numbers from CAD PDFs via PyPDF2 text extraction — avoids the vision-model hallucination problem on technical drawings |
| `freecad-mcp` | `registry/freecad-mcp/` | FreeCAD MCP wrapper — drive FreeCAD operations programmatically for parametric modeling and BOM generation |

---

## Dev Practices Library (operator-grade engineering)

The full obra/superpowers pack — engineering discipline as skills. Agents on the build side load these.

| Skill | Path | What it unlocks |
|---|---|---|
| `subagent-driven-development` | `registry/subagent-driven-development/` | Decompose work into focused subagent tasks instead of bloating the main thread |
| `systematic-debugging` | `registry/systematic-debugging/` | Root-cause investigation — no patches, no symptom-chasing |
| `using-git-worktrees` | `registry/using-git-worktrees/` | Parallel branches without thrashing — multiple workstreams, one repo |
| `verification-before-completion` | `registry/verification-before-completion/` | Prove it works before marking done — diff behavior, run tests, demonstrate correctness |
| `writing-skills` | `registry/writing-skills/` | Pattern for writing SKILL.md files that actually trigger and execute reliably |
| `writing-plans` | `registry/writing-plans/` | Pattern for writing implementation plans that survive review |

---

## UX / UI

| Skill | Path | What it unlocks |
|---|---|---|
| `ui-ux-pro-max-skill` | `registry/ui-ux-pro-max-skill/` | Python CLI search across 67 styles / 161 palettes / 57 font pairings / 99 UX rules / 25 chart types. Discovery + UX audit |

---

## Meta-Capability (the skills that build skills)

These are the skills that extend this system itself.

| Skill | Path | What it unlocks |
|---|---|---|
| `skill-creator` | `core/skills/skill-creator/` | The canonical Anthropic skill-creator. Scaffolds a new SKILL.md with proper frontmatter, triggers, and structure |
| `cookbook-lookup` | `core/skills/cookbook-lookup/` | Reference library for the Anthropic Claude Cookbooks — surface Anthropic's recommended pattern before building from scratch |
| `prompt-builder` | `core/skills/prompt-builder/` | Structure long unstructured prompts retroactively. Auto-invoked silently per Workflow Rule #9 |
| `auto-skill-builder` | `registry/auto-skill-builder/` | Capture a recurring pattern into a permanent SKILL.md — for when "we keep doing this" surfaces |
| `brainstorming` | `registry/brainstorming/` | Structured ideation pattern — diverge, then converge |
| `auto-hook-from-preference` | `registry/auto-hook-from-preference/` | Convert spoken preferences ("always do X", "from now on", "never") into harness-enforced hooks. Memory rules are advisory; hooks are mandatory |
| `audit-memory-skills` | `registry/audit-memory-skills/` | Recursive integrity audit on the compounding loop — verifies MEMORY.md indexes are current, daily skills are backed up, handoff files are functional |

---

## How agents use these

Each agent's frontmatter declares which skills it can invoke. When the agent fires for a task, the declared skills are available as callable tools — the agent shells out to them the same way you'd call a function. Skills load progressively: metadata is always in context, the SKILL.md body loads when the skill triggers, and bundled resources (scripts, references, assets) load only on demand. This keeps the agent's context window clean while giving it deep capability.

---

## How customers use these directly

Most skills are invocable as slash commands in Claude Code. Type `/` and the registered skills surface as autocomplete options. Common invocations:

- `/audit-memory-skills` — run the memory audit
- `/auto-skill-builder` — capture a new skill from a pattern
- `/prompt-builder` — structure a long prompt
- `/brainstorming` — kick off structured ideation

See each skill's SKILL.md for full invocation pattern and trigger phrases.

---

## Skills NOT shipped (intentional cuts)

- **Vertical-vendor-specific skills** (a sales/CAD/engineering-scope stack built for one user vertical-integration day job) -- single-vendor. Not generalizable.
- **Client-specific formatting enforcers** — formatting skills wired to one customer's asset registry. Single-tenant.
- **`cowork-image-ingest` / `inbox-routing` / `cowork-video-ingest`** — internal vault-routing plumbing. Deferred — will ship in a future "Inbox Pack" release.
- **`obsidian-capture`** — capture-pipeline still being generalized; ships in a future release.
- **`primo-session-rules`** — operator-personal session enforcement. Not shipped.
- **`prometheus-sow`** — SOW generator wired to one specific quoting platform. Not shipped.
- **`nesting-engine`** — single-application CAD nesting routine. Not shipped.
- **`copywriter` / `social-media`** — currently scoped to one specific brand voice. Will ship as templates in a future release.

The cuts above stay in the source repo for the author's personal use but are not part of the customer-shipped Stack.
