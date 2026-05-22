# `.claude/reference/` — shared reference shelf

Vault-level reference docs that ANY agent can load on demand. Distinct from `.claude/connectors/` (which has credentials + operational `client.py`). Reference is just docs: API contracts, library introductions, doc clippings, vendor SDKs, methodology snapshots, brand assets.

## Why vault-level (not per-agent)

Load-on-demand context only works when there's one canonical static shelf every agent can read. Putting API docs under `agents/<one-agent>/context/` creates a cross-agent-read awkwardness — when finance-manager needs the Tradovate API doc that trading-analyst owns, it has to know to look in another agent's folder. That breaks the pattern.

Shared reference = one source of truth. Librarian organizes; every agent reads.

## What's here (16 shelves)

Organized by **category of reference**, not by consuming agent. Every category is readable by every agent.

### Anthropic platform (the runtime ROOK lives in)

| Shelf | Scope | Primary consumers |
|---|---|---|
| `anthropic/` | Canonical Anthropic docs — API reference, Claude Code (settings, hooks, slash-commands, output-styles, skills, subagents, mcp, plan-mode, headless), Agent SDK (overview, setting-sources), capability guides (prompt-engineering, tool-use, prompt-caching, vision, skills, extended-thinking, system-prompts, citations), glossary, clippings of Anthropic posts. Includes `managed-agents/` subfolder (overview, get-started, pricing-analysis, pros-cons-self-host, scaling). | every agent — substrate docs |
| `anthropic-cookbook/` | 13 distilled cookbook patterns across agent-patterns, RAG, multimodal, prompt-engineering, evaluations, tools, skills-dev, integrations + the ROOK gap analysis | chief-of-staff, librarian, deep-researcher, software-dev-team, r-and-d-lead |

### Trading + finance vendor APIs

| Shelf | Scope | Primary consumers |
|---|---|---|
| `tradingview/` | TradingView Advanced Charts library — full official doc set (13 files: intro, getting-started, connecting-data, widget-constructor, widget-methods, ui-elements, api-reference, datafeed-api, module-datafeed, trading-platform-methods, best-practices, build-ai-library-assistant) | trading-analyst, r-and-d-lead, designer, software-dev-team |
| `tradovate/` | Tradovate futures broker — REST + WebSocket API | trading-analyst, finance-manager |
| `charles-schwab-api-docs/` | Charles Schwab Trader API — equities/options (Thinkorswim is the UI on top) | trading-analyst, finance-manager |

### Commerce + CRM vendor APIs

| Shelf | Scope | Primary consumers |
|---|---|---|
| `shopify/` | 21 files — webhooks, agentic-commerce, admin integration, apps in orders + fulfillment, secure-tokens, storefront-mcp, app package for React Router, Shopify CLI, Flow automation, mobile support, network security, QuickBooks-for-Shopify | shopify-agent, sales-director |
| `hubspot/` | API reference (date-based versioning 2026-03) + Web/Mobile SDKs (Node/Python/PHP/Ruby/HubSpot.js/React UI Extensions) | marketing-director, sales-director, inbox-manager |

### Creative + design

| Shelf | Scope | Primary consumers |
|---|---|---|
| `creative-design/` | Design references — Mobbin MCP (AI-agent design pattern library), best AI agents for graphic designers, Introducing Claude Design by Anthropic Labs | designer, creative-director, copywriter |
| `higgsfield-video-and-image-gen/` | Higgsfield AI infrastructure (video + image gen) + Higgsfield.AI MCP / CLI / APP | designer, creative-director, social-media-manager |

### Marketing

| Shelf | Scope | Primary consumers |
|---|---|---|
| `marketing/` | Ad-platform references — Claude Ads paid-advertising audit pattern | marketing-director, seo-specialist |
| `ai-agent-custom-skills/` | 3 community catalogs — VoltAgent awesome-agent-skills (~200 skills), Marketing Skills for AI Agents, 10 Best Claude Skill Repos for Marketing 2026 | marketing-director, content-strategist, seo-specialist, r-and-d-lead |

### Contract + business templates

| Shelf | Scope | Primary consumers |
|---|---|---|
| `contract-templates/` | NDAs, software dev agreements, SaaS licenses, MSAs, SOW templates, YC-form SaaS subscription. See `contract-templates/README.md` for full inventory + sanitization rules. | sales-director, account-manager, finance-manager, shopify-agent |

### Knowledge methodology

| Shelf | Scope | Primary consumers |
|---|---|---|
| `para-basb/` | Tiago Forte PARA + BASB knowledge-organization framework — 5 reference articles + index | chief-of-staff, librarian, content-strategist |
| `methodology/` | Cross-cutting methodology promotion target — populated by librarian's `shelf-promote` mode when 2+ agents independently develop the same pattern. Reserved space. See `methodology/README.md` for promotion criteria. | librarian, chief-of-staff |

### AI agent catalogs (external)

| Shelf | Scope | Primary consumers |
|---|---|---|
| `21st-dev-ai-agents/` | 21st-dev's AI agent catalog + AI agent registry | r-and-d-lead, product-manager |

### JavaScript libraries

| Shelf | Scope | Primary consumers |
|---|---|---|
| `chartjs/` | Chart.js library reference — chart types, install, basic usage, ROOK applicability (pairs with html2pdf for client-deliverable charting) | software-dev-team, trading-analyst, finance-manager, marketing-director, seo-specialist |

### Auto-generated (not source-controlled)

| Shelf | Scope |
|---|---|
| `graphify-out/` | Operator-local graphify cache — entire shared shelf indexed as a knowledge graph. Gitignored. Rebuilt by librarian's weekly sweep against the customer's local vault. |

## Pattern (per `_CLAUDE.md` § 0 rule #12)

When any agent is about to use one of these services:

1. **graphify-query first** — `python -m graphify query "<your question>" --budget 1500` returns the top relevant 5-10 files across the shelf
2. **Read the canonical README** in the matched shelf (`<shelf>/README.md`) for scope, integration touchpoints, consumers
3. **Read the specific topic file** the question maps to (`<shelf>/<topic>.md`)
4. **Verify against live docs** at the URL in the file's frontmatter — these snapshots may go stale
5. **For services with credentials**, fall back to `.claude/connectors/<service>/` for the operational client (this shelf is doc-only)

## Distinction from `.claude/connectors/`

| Surface | What it contains | Has credentials? | Has `client.py`? |
|---|---|---|---|
| `.claude/connectors/<service>/` | MCP-backed OR clean-REST services with shared creds (Gmail, Cal.com, Stripe, HubSpot, Perplexity) | Yes (centralized) | Often yes |
| `.claude/reference/<shelf>/` | API references + library docs + clippings + methodology — without credentials, without shared client | No — operator-credential, per-agent auth flow when needed | No — agents write per-use client code |

Egress for `reference/` services is still allowlisted at the runtime layer — see `.claude/connectors/_egress-allowlist.md` § "Agent-implemented API surfaces".

## Adding a new shelf

1. `mkdir .claude/reference/<shelf-name>/` (kebab-case, lowercase, descriptive)
2. Write `README.md` — scope, integration touchpoints, primary consumers, status, cross-references
3. Add per-topic files as the canonical content (e.g., `api-reference.md`, `getting-started.md`, or named clippings)
4. If the shelf references a service with API calls — add the egress row to `.claude/connectors/_egress-allowlist.md`
5. The librarian sweeps the shelf into MASTER_INDEX.md on next weekly run

## Naming conventions

- **kebab-case, lowercase** for shelf folders (`creative-design/`, not `Creative-Design/` or `creative_design/`)
- **Descriptive over compact** when the shelf could be confused (`charles-schwab-api-docs/` over `schwab/`; `contract-templates/` over `templates/`)
- **Family-name only for Anthropic models** in shelf content (Opus / Sonnet / Haiku — never release versions like 4.6 or 4.7 in normative ROOK content; reference clippings can preserve original version strings since they're dated snapshots)

## Librarian responsibility

The librarian agent owns shelf organization:
- Dedup-checking when new references arrive (same content at different paths → flag for canonicalization)
- Stale-flagging snapshots (timestamp older than 6 months → review against live docs)
- Surfacing cross-shelf patterns (e.g., "Tradovate and Schwab both use OAuth with weekly refresh ceremonies — codify the pattern")
- Promoting agent-specific patterns to `methodology/` when 2+ agents independently develop the same concept
- Regenerating `MASTER_INDEX.md` (this folder's per-shelf navigation index) on weekly sweep

## See also

- [MASTER_INDEX.md](MASTER_INDEX.md) — comprehensive per-shelf file listing (this folder)
- `_CLAUDE.md` § 0 rule #12 — context-load gate
- `.claude/connectors/README.md` — operational client/credential layer (sister surface)
- `agents/librarian/SKILL.md` — librarian sweep + shelf-promote mode

---

<sub>Powered by [Claude](https://www.anthropic.com/claude) · Built by [PrimoLabs](https://primolabs.ai)</sub>
