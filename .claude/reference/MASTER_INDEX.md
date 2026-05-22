---
name: reference-master-index
generated: 2026-05-22
auto-generated-by: librarian weekly sweep (this snapshot: hand-written)
total-shelves: 16
total-files: ~100 (excludes graphify-out cache)
---

# `.claude/reference/` — Master Index

Comprehensive per-shelf file navigation. Sister doc to [README.md](README.md) (architecture + categories). This file is the look-it-up index; the README is the read-it-once explainer.

**Status:** initial hand-written snapshot 2026-05-22. Librarian's weekly sweep will auto-regenerate going forward.

---

## anthropic/ — Anthropic platform docs (29 files)

### Top-level
- [anthropic/glossary.md](anthropic/glossary.md) — Claude glossary (Obsidian clipping)
- [anthropic/anthropic-agents-for-financial-services.md](anthropic/anthropic-agents-for-financial-services.md) — Anthropic-published financial-services example

### api/
- [anthropic/api/overview.md](anthropic/api/overview.md) — API overview (Obsidian clipping)

### claude-code/
- [anthropic/claude-code/overview.md](anthropic/claude-code/overview.md)
- [anthropic/claude-code/settings.md](anthropic/claude-code/settings.md)
- [anthropic/claude-code/hooks.md](anthropic/claude-code/hooks.md)
- [anthropic/claude-code/slash-commands.md](anthropic/claude-code/slash-commands.md)
- [anthropic/claude-code/output-styles.md](anthropic/claude-code/output-styles.md)
- [anthropic/claude-code/skills.md](anthropic/claude-code/skills.md) — load-bearing: ROOK agent = skill substrate
- [anthropic/claude-code/subagents.md](anthropic/claude-code/subagents.md) — chief-of-staff dispatch substrate
- [anthropic/claude-code/mcp.md](anthropic/claude-code/mcp.md)
- [anthropic/claude-code/headless.md](anthropic/claude-code/headless.md)
- [anthropic/claude-code/plan-mode.md](anthropic/claude-code/plan-mode.md)

### agent-sdk/
- [anthropic/agent-sdk/overview.md](anthropic/agent-sdk/overview.md)
- [anthropic/agent-sdk/setting-sources.md](anthropic/agent-sdk/setting-sources.md)

### guides/
- [anthropic/guides/prompt-engineering.md](anthropic/guides/prompt-engineering.md)
- [anthropic/guides/tool-use.md](anthropic/guides/tool-use.md)
- [anthropic/guides/prompt-caching.md](anthropic/guides/prompt-caching.md)
- [anthropic/guides/vision.md](anthropic/guides/vision.md)
- [anthropic/guides/skills.md](anthropic/guides/skills.md) — canonical Anthropic Agent Skills spec
- [anthropic/guides/extended-thinking.md](anthropic/guides/extended-thinking.md)
- [anthropic/guides/system-prompts.md](anthropic/guides/system-prompts.md)
- [anthropic/guides/citations.md](anthropic/guides/citations.md)
- [anthropic/guides/common-use-cases.md](anthropic/guides/common-use-cases.md)

### clippings/ (Obsidian-curated)
- [anthropic/clippings/Claude Code.md](anthropic/clippings/Claude Code.md)
- [anthropic/clippings/Anthropic What are skills.md](anthropic/clippings/Anthropic What are skills.md)
- [anthropic/clippings/Anthropic Courses.md](anthropic/clippings/Anthropic Courses.md)
- [anthropic/clippings/Claude for Creative Work.md](anthropic/clippings/Claude for Creative Work.md)
- [anthropic/clippings/Debugging.md](anthropic/clippings/Debugging.md)
- [anthropic/clippings/reduce-hallucinations.md](anthropic/clippings/reduce-hallucinations.md)
- [anthropic/clippings/increase-output-consistency.md](anthropic/clippings/increase-output-consistency.md)
- [anthropic/clippings/prompting-best-practices.md](anthropic/clippings/prompting-best-practices.md) — 57 KB load-bearing canonical guide
- [anthropic/clippings/managed-agents-overview.md](anthropic/clippings/managed-agents-overview.md) — relocated to managed-agents/overview.md (2026-05-22)

### managed-agents/ (subfolder, 6 files)
- [anthropic/managed-agents/README.md](anthropic/managed-agents/README.md)
- [anthropic/managed-agents/overview.md](anthropic/managed-agents/overview.md)
- [anthropic/managed-agents/get-started.md](anthropic/managed-agents/get-started.md)
- [anthropic/managed-agents/pricing-analysis.md](anthropic/managed-agents/pricing-analysis.md)
- [anthropic/managed-agents/pros-cons-self-host.md](anthropic/managed-agents/pros-cons-self-host.md)
- [anthropic/managed-agents/scaling-decoupling-brain-from-hands.md](anthropic/managed-agents/scaling-decoupling-brain-from-hands.md)

---

## anthropic-cookbook/ — Distilled cookbook patterns (14 files)

- [anthropic-cookbook/ROOK-gap-analysis.md](anthropic-cookbook/ROOK-gap-analysis.md) — load-bearing — 5 absorb-recommended, 3 inherit-via-skill, 3 already-implemented, 2 skip
- [anthropic-cookbook/agent-patterns/](anthropic-cookbook/agent-patterns/) — orchestrator-workers + sub-agent patterns
- [anthropic-cookbook/rag/](anthropic-cookbook/rag/) — RAG fundamentals, knowledge-graph construction
- [anthropic-cookbook/extended-thinking/](anthropic-cookbook/extended-thinking/) — thinking + tool use
- [anthropic-cookbook/multimodal/](anthropic-cookbook/multimodal/) — vision, charts/graphs/powerpoints
- [anthropic-cookbook/prompt-engineering/](anthropic-cookbook/prompt-engineering/) — prompt-caching, metaprompt
- [anthropic-cookbook/evaluations/](anthropic-cookbook/evaluations/) — building-evals, tool-evaluation
- [anthropic-cookbook/skills-dev/](anthropic-cookbook/skills-dev/) — custom skill development
- [anthropic-cookbook/tools/](anthropic-cookbook/tools/) — parallel-tools, tool-use-with-pydantic
- [anthropic-cookbook/integrations/](anthropic-cookbook/integrations/) — multi-document agents

---

## tradingview/ — TradingView Advanced Charts (13 files)

Full official doc set: intro, getting-started, connecting-data, widget-constructor, widget-methods, ui-elements, api-reference, datafeed-api, module-datafeed, trading-platform-methods, best-practices, build-ai-library-assistant.

---

## tradovate/ — Tradovate futures broker (2 files)
- REST + WebSocket API reference

## charles-schwab-api-docs/ — Charles Schwab Trader API (3 files)
- [charles-schwab-api-docs/README.md](charles-schwab-api-docs/README.md)
- [charles-schwab-api-docs/api-reference.md](charles-schwab-api-docs/api-reference.md)
- [charles-schwab-api-docs/developer-portal-overview.md](charles-schwab-api-docs/developer-portal-overview.md)

---

## shopify/ — Shopify platform (22 files)

Webhooks (about, subscriptions, GraphQL admin subscribe), agentic-commerce, apps-in-orders-and-fulfillment, build-a-storefront-ai-agent, customize-shopify-inbox, generate-secure-tokens, admin integration, localize-your-app, mobile-support, secure-network-service-ports, set-up-iframe-protection, Shopify APIs/libraries/tools, React Router app package, Shopify CLI, Shopify Flow, storefront-mcp, shorten-urls-with-care, quickbooks-for-shopify (relocated from `quickbooks/` 2026-05-22).

---

## hubspot/ — HubSpot CRM platform (2 files)
- [hubspot/api-reference-2026-03.md](hubspot/api-reference-2026-03.md) — date-based versioning, 7 namespaces, auth methods
- [hubspot/web-mobile-sdks.md](hubspot/web-mobile-sdks.md) — Node/Python/PHP/Ruby/HubSpot.js/React UI Extensions SDK matrix

---

## creative-design/ — Design references (3 files)
- [creative-design/mobbin-mcp.md](creative-design/mobbin-mcp.md) — Mobbin MCP design reference for AI agents
- [creative-design/best-ai-agents-for-graphic-designers.md](creative-design/best-ai-agents-for-graphic-designers.md)
- [creative-design/introducing-claude-design-by-anthropic-labs.md](creative-design/introducing-claude-design-by-anthropic-labs.md)

---

## higgsfield-video-and-image-gen/ — Higgsfield AI (2 files)
- [higgsfield-video-and-image-gen/higgsfield-ai-infrastructure.md](higgsfield-video-and-image-gen/higgsfield-ai-infrastructure.md)
- [higgsfield-video-and-image-gen/higgsfield-ai-image-mcp-cli-app.md](higgsfield-video-and-image-gen/higgsfield-ai-image-mcp-cli-app.md)

---

## marketing/ — Ad-platform + marketing references (1 file)
- [marketing/claude-ads-paid-advertising-audit.md](marketing/claude-ads-paid-advertising-audit.md) — 250-check rubric pattern

---

## ai-agent-custom-skills/ — Community skill catalogs (3 files)
- [ai-agent-custom-skills/voltagent-awesome-agent-skills.md](ai-agent-custom-skills/voltagent-awesome-agent-skills.md) — 176 KB, full VoltAgent catalog
- [ai-agent-custom-skills/marketing-skills-for-ai-agents.md](ai-agent-custom-skills/marketing-skills-for-ai-agents.md)
- [ai-agent-custom-skills/10-best-claude-skill-repos-for-marketing-2026.md](ai-agent-custom-skills/10-best-claude-skill-repos-for-marketing-2026.md)

---

## contract-templates/ — Contract + document templates (9 files across 4 categories)

### nda/
- `1 Master Software Development Agreement.md`
- `Confidentiality and Non Disclosure Agreement.md`

### contracts/
- `Saas License Agreement.md`
- `Sample Software Development Agreement Indian Developer US Client.md`
- `Software Development Agreement Template.md`

### saas/
- `YC Form SaaS Agreement.md`

### sow/
- `Professional Services Statement of Work.md`
- `SEC SOW TEMPLATE.md`

See [contract-templates/README.md](contract-templates/README.md) for full inventory + sanitization rules.

---

## para-basb/ — PARA + BASB knowledge framework (6 files)
- [para-basb/_INDEX.md](para-basb/_INDEX.md)
- 5 reference articles (PARA method, organizing in PARA, hard facts of life, simple system, note-taking)

---

## methodology/ — Cross-cutting promotion target (1 file)
- [methodology/README.md](methodology/README.md) — empty shelf, populated by librarian shelf-promote mode

---

## 21st-dev-ai-agents/ — External AI agent catalogs (2 files)
- [21st-dev-ai-agents/21st-dev-catalog.md](21st-dev-ai-agents/21st-dev-catalog.md)
- [21st-dev-ai-agents/ai-agent-registry.md](21st-dev-ai-agents/ai-agent-registry.md)

---

## chartjs/ — Chart.js library reference (1 file)
- [chartjs/README.md](chartjs/README.md) — install, chart types, ROOK applicability across 5 agents

---

## graphify-out/ — Operator-local graph cache (gitignored)

71 files (~1 MB) — entire shared shelf indexed as a knowledge graph for graphify queries. Regenerated weekly by librarian sweep. Never source-controlled.

---

## Quick navigation by consuming agent

| Agent | Primary shelves |
|---|---|
| chief-of-staff | anthropic/, anthropic-cookbook/, para-basb/, methodology/ |
| librarian | anthropic/, anthropic-cookbook/, para-basb/, methodology/ |
| deep-researcher | anthropic-cookbook/ (RAG), all shelves (cross-cutting research) |
| sales-director | contract-templates/, hubspot/, shopify/ |
| account-manager | contract-templates/, hubspot/, shopify/ |
| inbox-manager | hubspot/, anthropic/guides/citations.md |
| marketing-director | marketing/, ai-agent-custom-skills/, hubspot/, creative-design/ |
| content-strategist | ai-agent-custom-skills/, para-basb/, creative-design/ |
| social-media-manager | creative-design/, higgsfield-video-and-image-gen/, marketing/ |
| seo-specialist | marketing/, ai-agent-custom-skills/, anthropic/guides/ |
| creative-director | creative-design/, higgsfield-video-and-image-gen/ |
| designer | creative-design/, higgsfield-video-and-image-gen/, anthropic/guides/vision.md, tradingview/ (chart UX) |
| copywriter | creative-design/, contract-templates/ (legal-copy reference) |
| trading-analyst | tradingview/, tradovate/, charles-schwab-api-docs/, chartjs/ |
| finance-manager | tradovate/, charles-schwab-api-docs/, contract-templates/, chartjs/ |
| shopify-agent | shopify/, contract-templates/, hubspot/ |
| software-dev-team | anthropic/, anthropic-cookbook/, chartjs/, hubspot/ |
| engineering-lead | anthropic/guides/vision.md (drawing-pack OCR), chartjs/ |
| product-manager | anthropic-cookbook/, 21st-dev-ai-agents/, ai-agent-custom-skills/ |
| r-and-d-lead | 21st-dev-ai-agents/, ai-agent-custom-skills/, higgsfield-video-and-image-gen/, anthropic-cookbook/ |

---

## Maintenance

- This file regenerated by librarian on weekly sweep
- Hand-edits between sweeps OK but will be overwritten — landlord rules
- New shelves: see [README.md § Adding a new shelf](README.md)
- Stale snapshots: librarian flags any file with `fetched` frontmatter older than 6 months
- Cross-shelf dedup: librarian runs MD5-hash sweep on new arrivals

---

<sub>Powered by [Claude](https://www.anthropic.com/claude) · Built by [PrimoLabs](https://primolabs.ai)</sub>
