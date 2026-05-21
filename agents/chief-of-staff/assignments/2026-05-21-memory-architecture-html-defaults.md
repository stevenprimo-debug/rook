---
date: 2026-05-21
type: assignment
priority: P0 — ship-blocker for v1.0
target_agent: software-dev-team
model: sonnet
estimated_wallclock: ~8 hours AI-paced (single focused session)
issued_by: chief-of-staff (Sonnet, main thread)
operator_approval: 2026-05-21 — locked across 8+ AskUserQuestion exchanges
---

# Memory Architecture + HTML Defaults — Comprehensive Assignment

## Why this exists

ROOK ships v1.0 with these architectural choices locked today:
- All 20 agents communicate via shared shelf (graphify) — already working
- Per-agent memory upgrades: graphify subgraph for all 20, SQLite for 6 structured-state agents, Chroma+local-embedder for 2 cross-cutting synthesizers
- Customer-facing artifacts default to HTML (brand-injected); internal-only stays markdown; email is plain-text with generic ROOK default
- Website-ready: every agent's memory + connectors exposed in machine-readable form via `_roster.json`
- inbox-manager renamed to inbox-manager throughout
- Yesterday's README rewrite chaos cleaned up — 8 inaccurate READMEs reconciled to SKILL/bench, 1 missing README created

## Hard constraints (DO NOT VIOLATE)

- **$0/month runtime cost.** Customer installs ROOK and never gets billed.
- **ZERO API keys required to function.** No OpenAI, no third-party services in the base install.
- **Works offline.** Customer can disconnect internet and ROOK still operates.
- **`pip install -r requirements.txt` is the install ceiling.** No additional manual setup.
- **Absolute paths only** — your cwd may be operator vault (`C:\Users\User\Desktop\PRIMOLABS\`); all writes target SHIP vault (`C:\Users\User\Desktop\PrimoLabs_PoweredByClaude\`). Never the operator vault mirror at `PRIMOLABS\Agents\`.

## Estimated AI-paced timeline: ~8 hours

Per `feedback_build_time_estimates_exaggerated.md` — AI-paced means subagent + parallel execution, not human-team weeks.

---

## Item 1 — Per-agent graphify subgraph (all 20)

**~45 min**

Each of the 20 agents gets its own graphify subgraph over its `memory/` folder.

- Add a Python helper at `scripts/regenerate-agent-subgraphs.py` — iterates 20 agents, runs `python -m graphify agents/<slug>/memory/ --output agents/<slug>/graphify-out/`
- Update `agents/librarian/SKILL.md` to add this regeneration to the weekly sweep
- Update each agent's SKILL.md Step 1 (context load) to query its own subgraph at session start (in addition to the existing shared shelf query)

Cost: ~30s per agent build × 20 = ~10 min runtime on weekly sweep. Disk: ~1-5MB per agent.

## Item 2 — SQLite schemas for 6 declared_tier-2 agents

**~2 hours**

Six agents with `declared_tier: 2` get real SQLite schemas. Each schema is ~30-50 lines DDL + a small Python helper.

| Agent | DB file | Tables |
|---|---|---|
| account-manager | `memory/accounts.db` | accounts, deals, renewals, at_risk_signals |
| finance-manager | `memory/finance.db` | invoices, commissions, deal_economics |
| sales-director | `memory/pipeline.db` | prospects, deals, stage_transitions, outreach_log |
| shopify-agent | `memory/shopify.db` | orders, line_items, customers, merchants, fulfillment |
| trading-analyst | `memory/trading.db` | setups, posture_history, journal, learnings |
| inbox-manager | `memory/messages.db` | messages, threads, drafts, escalations, triage_status |

For each agent:
1. Write `agents/<slug>/memory/schema.sql` with the DDL
2. Write `agents/<slug>/memory/db.py` — thin sqlite3 helper module: connect, query, write, migrate
3. Update agent's SKILL.md Step 1 to load the helper + query patterns for the agent's domain
4. Document the schema in the agent's README "Memory" section (will auto-regenerate via Item 7)

Use stdlib `sqlite3` only. No SQLAlchemy. No ORM. Keep it simple.

## Item 3 — ChromaDB + local sentence-transformers (librarian + deep-researcher)

**~1.5 hours**

Only librarian + deep-researcher get the semantic-search layer. They're the two synthesizers whose JOB is cross-cutting concept lookup.

- Add `chromadb` and `sentence-transformers` to `requirements.txt`
- Note the first-run model download size (~200MB for `all-MiniLM-L6-v2`) in README
- Build `agents/librarian/memory/chroma/` + helper at `agents/librarian/memory/embed.py`
- Build same at `agents/deep-researcher/memory/chroma/` + `embed.py`
- Embed: librarian indexes the full vault on weekly sweep; deep-researcher indexes its own research corpus + shared shelf
- Query interface in each agent's SKILL.md Step 1
- Use `sentence-transformers/all-MiniLM-L6-v2` as the default embedder — runs on CPU, free, works offline

NO OpenAI embeddings. NO API keys.

## Item 4 — README accuracy pass (8 rewrites + 1 missing)

**~45 min**

Per the librarian's audit (`_FROM_CLAUDE/2026-05-21-librarian-readme-audit.md` if it was saved; otherwise read the audit transcript):

**Fix these 8 inaccurate READMEs to match SKILL.md + `_bench.md`:**
chief-of-staff, content-strategist, copywriter, creative-director, finance-manager, librarian, social-media-manager, software-dev-team, trading-analyst

**Strict rules for rewrites:**
- SKILL/bench is canonical (don't rewrite the bench to match the README)
- NO figure names anywhere — pole names must be PRINCIPLES not people (per `_CLAUDE.md` de-personification rule)
- Voice = account-manager pattern (terse, principle-named, declarative)
- Categories must match SKILL.md `category:` field
- Status line must reflect SKILL.md `status:` field
- Connectors must match SKILL.md `connectors:` field

**Create the missing README at `agents/inbox-manager/README.md` (note: file is being renamed in Item 5, so create at the new path)**

## Item 5 — Rename `inbox-manager` → `inbox-manager`

**~30 min**

- Folder rename: `agents/inbox-manager/` → `agents/inbox-manager/`
- Find-replace `inbox-manager` → `inbox-manager` in ALL files: SKILL.md, CLAUDE.md, README.md, `_CLAUDE.md`, `MASTER_INDEX.md`, `hooks/routing-rules.json`, every other agent's SKILL.md that references it
- Update `routing-rules.json` `agents.inbox-manager` block (the slug key + all references)
- Update `routing-rules.json` `model_distribution` (which lists `inbox-manager` per Primo's locked model assignment)
- Update the dispatch_log references in chief-of-staff if any

Validate: `python -c "import json; json.load(open('hooks/routing-rules.json'))"` passes.

## Item 6 — `_roster.json` + `regenerate-roster.py`

**~30 min**

Create the auto-generated machine-readable agent roster.

**Schema (locked in main-thread brief 2026-05-21):**

```json
{
  "_meta": {
    "generated_at": "ISO-8601 timestamp",
    "generated_by": "librarian weekly sweep",
    "version": "1.0",
    "agent_count": 20
  },
  "agents": [
    {
      "slug": "shopify-agent",
      "name": "Shopify Agent",
      "category": "Revenue",
      "status": "operational",
      "model": "sonnet",
      "role_one_line": "...",
      "bench": {
        "pole_1": "...",
        "pole_2": "...",
        "pole_3_synth": "...",
        "tension_axis": "..."
      },
      "memory": {
        "primary_tier": 2,
        "backend": "SQLite",
        "schema_file": "memory/orders.db",
        "rationale_one_line": "...",
        "secondary": [{"tier": 4, "backend": "markdown+grep", "purpose": "..."}],
        "queries_shared_shelf": true
      },
      "connectors": [
        {"name": "...", "purpose": "...", "reversibility": "N", "auth_required": "...", "type": "..."}
      ],
      "dispatch": {
        "upstream_required": null,
        "downstream_pattern": "returns-to-chief-of-staff"
      }
    }
  ],
  "dispatch_chains": { "designer": ["creative-director", "marketing-director", "designer"] },
  "categories": ["Revenue", "Operations", "Marketing", "Creative", "Build", "Lab", "Research", "Finance", "Platform"],
  "model_distribution": {"opus": 12, "sonnet": 8},
  "memory_distribution": {
    "tier_1_vector_graph": ["librarian", "deep-researcher"],
    "tier_2_sqlite": ["account-manager", "finance-manager", "sales-director", "shopify-agent", "trading-analyst", "inbox-manager"],
    "tier_3_vectorless_pdf": ["engineering-lead"],
    "tier_4_markdown": ["..."]
  }
}
```

- Write `scripts/regenerate-roster.py` — reads each `agents/<slug>/SKILL.md` frontmatter and emits `_roster.json`
- Source-of-truth pattern: SKILL.md frontmatter, never duplicated
- Wire into librarian's weekly sweep (after subgraph regen)
- File location: `_roster.json` at vault root (peer to `MASTER_INDEX.md`)

## Item 7 — Structured frontmatter on all 20 SKILL.md (memory + connectors blocks)

**~30 min**

Update every agent's SKILL.md frontmatter to expose the canonical structured blocks for the roster generator.

Required new frontmatter fields per agent:

```yaml
memory:
  primary_tier: 2  # 1=vector+graph | 2=SQLite | 3=PDF | 4=markdown+grep
  backend: SQLite
  schema_file: memory/orders.db
  rationale_one_line: "Order data is structured; SQL beats grep at 10k+ orders"
  secondary:
    - tier: 4
      backend: markdown+grep
      purpose: "narrative learnings, merchant notes"
  queries_shared_shelf: true

connectors:
  - name: shopify-admin-api
    purpose: Order + product CRUD, webhook subscriptions
    reversibility: N
    auth_required: operator-provided API key
    type: REST
```

Apply to all 20 agents. Use the locked memory tier assignments (Item 2 + 3 above).

## Item 8 — Rule #17 + HTML default templates + brand-injection layer

**~1.5 hours**

**Add Rule #17 to `_CLAUDE.md` Section 0:**

> 17. **Output format — HTML default for human-eyes artifacts.** ROOK outputs default to HTML for any artifact a human will see outside the vault (customer deliverables, `_from_rook/` reading inbox, anything that becomes a PDF, dashboard artifacts, briefs, plans, proposals, reports). Markdown stays for internal-only (memory files, SKILL.md, CLAUDE.md, README.md, routing manifests, system files). **Email exception:** customer-facing emails are plain text — "Hello [First Name]" opener, clear concise bullet points, customizable voice via inbox-manager templates. Brand injection applies to all HTML outputs — colors, fonts, logo pulled from `.claude/memory/rook_brand.md` (or operator-config when in operator-mode). The operator-personal `.eml + X-Unsent: 1 + Cheers,` pattern is a LOCAL override in operator vault config, not part of the ROOK shipped product.

**Build HTML templates at `.claude/templates/html/`:**
- `brief.html.j2` — Jinja2 template for an agent brief (header with brand, body, footer)
- `plan.html.j2` — for a plan/roadmap artifact (sections, tables, timeline)
- `proposal.html.j2` — for a customer proposal (cover, body, signature blocks)
- `report.html.j2` — for a deliverable report (executive summary, body, appendix)

Each template:
- CSS variables pulled from a brand-tokens JSON file
- Logo URL pulled from brand config
- Font stack declared at top
- Responsive (mobile-readable in Obsidian's HTML preview + browser)

**Build the brand-injection layer at `.claude/templates/html/brand-loader.py`:**
- Reads `.claude/memory/rook_brand.md` (ship product default) OR operator's brand override (if `ROOK_BRAND_OVERRIDE` env var set)
- Emits a JSON dict of `{primary_color, secondary_color, accent, body_font, heading_font, logo_url, brand_name}`
- Templates consume this dict

**Build inbox-manager default email template at `agents/inbox-manager/templates/default-email.md`:**
- "Hello [First Name]," opener
- Bullet-point body slot
- No sign-off block (operator picks)
- Plain text — NOT HTML

**Update each agent's SKILL.md `write_targets:` table** to declare HTML defaults for customer-facing artifacts.

## Item 9 — `_CLAUDE.md` documentation pass

**~30 min**

Add a new section to `_CLAUDE.md` after Section 0:

**Section 0.1 — Memory Architecture (ship-safe)**

Document:
- The 4-tier memory model
- Per-agent tier assignments (the 20-agent table from Item 7)
- Cross-agent communication patterns (shared shelf + dispatch + dispatch_log)
- Cost picture ($0/month, no API keys, offline)
- Upgrade path for operator/cohort versions (optional Chroma+OpenAI)

Also add the new rules #16 (cross-model verification from prior phase) and #17 (HTML defaults from this phase) if they're not already there.

## Verification gates (run all, report results)

1. `python -c "import json; json.load(open('C:/Users/User/Desktop/PrimoLabs_PoweredByClaude/hooks/routing-rules.json')); print('OK')"` — passes
2. `python -c "import json; json.load(open('C:/Users/User/Desktop/PrimoLabs_PoweredByClaude/_roster.json')); print('OK')"` — passes, 20 agents present
3. `agents/inbox-manager/` exists; `agents/inbox-manager/` does NOT exist
4. `agents/inbox-manager/README.md` exists with substantive content
5. Grep `inbox-manager` across the entire ship vault — ZERO hits
6. All 20 agent SKILL.md files have the new `memory:` and `connectors:` frontmatter blocks
7. SQLite schemas exist + Python helpers exist for the 6 tier-2 agents
8. Chroma helpers exist for librarian + deep-researcher
9. `.claude/templates/html/` contains the 4 templates + brand-loader.py
10. `agents/inbox-manager/templates/default-email.md` exists with the "Hello [First Name]" pattern
11. `_CLAUDE.md` has rule #17 + Section 0.1
12. `scripts/regenerate-roster.py` runs successfully and emits valid `_roster.json`
13. Per-agent subgraphs generated (spot-check 3 random agents have `graphify-out/` populated)
14. `requirements.txt` includes `chromadb`, `sentence-transformers`
15. No API keys referenced anywhere in the runtime code (only optional `ROOK_BRAND_OVERRIDE` env var)

## Return contract (≤500 words)

- Items 1-9 status: DONE / PARTIAL / BLOCKED with one-line reason
- Files created or modified (paths only, no contents)
- 15 verification gate results (pass/fail per gate)
- Any new product-quality findings surfaced during the work
- Any decisions you had to make (e.g., schema choices) — list as "I decided X because Y; flag if wrong"

Do NOT paste code, full file contents, or token usage stats. Main thread distills your return for the operator.

If you need an operator decision mid-work, return ≤200 words with the specific question + 2-4 options + recommended option. Do NOT proceed past an ambiguity.
