# ROOK — Vault Operating Rules

> Read this before doing anything in the vault. These rules **override** any imported skill defaults.
>
> ROOK is simultaneously (a) an Obsidian vault, (b) a Claude Code workspace, and (c) a 20-agent Agentic OS. All three readings must hold simultaneously — don't optimize one at the expense of the others.

---

## The pattern: Compounding-Append + Contradiction-Surfacer

**Git-shape, not Karpathy-shape.** History is permanent.

- **Every change is versioned.** `## Version history` preserves the journey — the iteration that got to current state IS the credibility.
- **`## For future Claude (TL;DR)`** at the top of every memory file is the pinned HEAD — read first to decide relevance in 10 seconds.
- **Contradictions surface as questions, never silent overwrites.** When new info conflicts with existing memory, write `## ⚠️ CONTRADICTION YYYY-MM-DD` at top with both versions; let the operator lock the resolution before any rewrite.
- **Indexes** (`MASTER_INDEX.md`, per-agent `INDEX.md`) point at HEAD AND link to history.

**Why not Karpathy LLM Wiki:** rewrite-on-update destroys the audit trail that compounds across sessions. The compounding history is the moat — what's referenced, defended, and taught.

---

## Section 0 — AI-first rules (apply universally)

The vault is designed for future-Claude to read and reason over. Every note follows:

1. **Self-contained context** — each note explains itself; don't rely on backlinks alone
2. **`## For future Claude (TL;DR)`** — 2-3 sentence summary block at top
3. **Rich frontmatter** — every memory file uses the canonical template. Required: `name`, `description`, `type`, `date`, `confidence`, `ai-first: true`
4. **Recency markers per claim** — "as of YYYY-MM-DD" for any time-sensitive fact
5. **Sources preserved verbatim** — quotes, URLs, `originSessionId` when known
6. **Wikilinks mandatory** — `[[file]]` for cross-refs Obsidian indexes
7. **Confidence level explicit** — `stated | high | medium | speculation`
8. **Hierarchical Supervisor pattern** — Chief of Staff distills subagent returns to ≤2K tokens before surfacing (verdict + action + reasoning + source pointer; never raw paste). See [`agents/chief-of-staff/SKILL.md`](agents/chief-of-staff/SKILL.md) § Distilled Return rule.
11. **Visible-output gate** — agents NEVER narrate their own reasoning in visible output. All process-thinking goes in <thinking> blocks. First line is verdict/dispatch/question/artifact — banned: "Now I have a clear picture", "Let me check", "Actually,", "My next move is", "I am realizing/wondering/structuring". See agents/chief-of-staff/SKILL.md § VISIBLE OUTPUT GATE.
12. **Context-load gate (universal — every agent, every invocation)** — BEFORE answering anything substantive in its domain, an agent MUST load its own context surfaces. The router does NOT pre-fetch everything; load-on-demand is the rule. Failure mode: agent goes straight to trial-and-error because it didn't read the docs already in the vault (Shopify token saga 2026-05-20, 1 hour wasted). Discipline:
    - **Step 1 of every domain-bound response:** read the agent's own `memory/MEMORY.md` (per-agent catalog) and the root `MASTER_INDEX.md` (cross-agent catalog).
    - **Step 2:** query the shared shelf via graphify, then read the specific files the question maps to. Three shelves to know:
        - **Connector question** → `.claude/connectors/<service>/README.md` + `api-reference.md` (MCP-backed OR clean-REST + shared creds)
        - **Shared reference (the canonical cross-cutting shelf)** → `.claude/reference/`:
            - `.claude/reference/<service>/` — API + library docs (TradingView, Tradovate, Schwab, etc.)
            - `.claude/reference/contract-templates/<category>/` — NDA, contracts, SOW, SaaS, partnerships
            - `.claude/reference/sops/` — operator SOPs (operator vault only)
        - **Agent-internal** → `agents/<agent>/memory/` — compounding learnings, decisions, feedback (versioned-append, per-agent). Captures land in root `inbox/` and the router moves them to ONE home (shared shelf OR agent memory) — never duplicated.
    - **Step 3 (only after 1 + 2):** answer / execute / dispatch.
    - **Banned:** answering from training-data recall when vault context exists. If the vault has it, the vault wins.
    - **Banned:** the router or chief-of-staff trying to pre-fetch all context for a downstream agent. The downstream agent loads what it needs; the router only routes.
    - **`.claude/reference/` is SHARED** — any agent can read any subfolder there. Don't hide cross-cutting material (API docs, contract templates, SOPs, methodology playbooks shared across agents) inside one agent's `memory/`. If two or more agents could need it, it goes on the shared shelf.
    - **What stays agent-scoped:** ONLY the agent's voice/personality bench, its own SKILL.md modes, the agent-specific methodology (not the shared playbooks), and the agent's compounding `memory/` (versioned-append history). Everything else cross-cutting → shared shelf.
    - **Pattern source:** `CLAUDE CODE/MEMORY/feedback_load_shopify_context_at_session_start.md` (locked 2026-05-20).

16. **Rule #16 — Cross-model verification on reversibility=N decisions**: Before executing any irreversible action (client email, prod push, public post, money, force-push), the executing agent MUST surface the decision via `second-opinion-verify` — a vendor-neutral skill that runs an adversarial review through Perplexity (primary), Claude Opus subagent (fallback), or flags the decision for manual review (final fallback). Returns AGREE / DISAGREE-WITH-REASON / NEEDS-MORE-CONTEXT. Synthesis required: "Sonnet says X. Second opinion says Y. My call is Z because [specific reason]." Skill: `.claude/skills/second-opinion-verify/SKILL.md`. Locked 2026-05-21, renamed from `codex-cross-verify` 2026-05-22 (Codex CLI not bundled; Perplexity is customer's available adversarial model).

17. **Rule #17 — Output format: HTML default for human-eyes artifacts.** ROOK outputs default to HTML for any artifact a human will see outside the vault (customer deliverables, `_from_rook/` reading inbox, anything that becomes a PDF, dashboard artifacts, briefs, plans, proposals, reports). Markdown stays for internal-only: memory files, SKILL.md, CLAUDE.md, README.md, routing manifests, system files. **Email exception:** customer-facing emails are plain text — "Hello [First Name]," opener, clear concise bullet points, customizable voice via inbox-manager templates. Brand injection applies to all HTML outputs — colors, fonts, logo pulled from `.claude/memory/rook_brand.md` (or operator-config when in operator-mode). Templates live at `.claude/templates/html/`. The brand-loader at `.claude/templates/html/brand-loader.py` emits a JSON dict consumed by every Jinja2 template. The operator-personal `.eml + X-Unsent: 1 + Cheers,` pattern is a LOCAL override in operator vault config, not part of the ROOK shipped product. Locked 2026-05-21.

13. **Rule #13 — Model-tier routing**: chief-of-staff, librarian, inbox-manager, and 9 other Opus-tier agents run on Opus model. Per-agent assignment locked in `hooks/routing-rules.json` (model field per agent slug). Reason: Sonnet rationalizes past routing-enforcer text; Opus follows it. Locked 2026-05-21. Full roster: account-manager, chief-of-staff, content-strategist, creative-director, deep-researcher, designer, engineering-lead, finance-manager, inbox-manager, librarian, software-dev-team (all child skills), trading-analyst = Opus. All others = Sonnet.

14. **Rule #14 — AskUserQuestion-only gate (with free-text exception)**: Every discrete choice (2+ mutually exclusive options) uses the AskUserQuestion tool with the GStack decision-brief format. Free-text inputs (names, URLs, dollar amounts, single-string values) MAY use a one-line prose question with no preamble — e.g., "Client name?" — when forcing them through AskUserQuestion's Other field adds a round-trip without value. Discrete choices stay AskUserQuestion. The bar for prose: ONE line, no preamble, no warmth, single input. Decision-brief format required on AskUserQuestion calls: header chip ≤12 chars, question ending in `?`, 2-4 options each ≥40 chars, one option flagged "(Recommended)", effort-bearing options dual-scaled "(human: ~N days / CC: ~N min)". Violation = re-do. Bundle up to 4 questions per AskUserQuestion call where possible to avoid round-trip waste. Source: GStack decision-brief format borrow + Music City Cuts round-trip-multiplication finding, locked 2026-05-21, amended 2026-05-22.

15. **Rule #15 — Distillation applies to main-thread → operator boundary**: Main thread response ≤2K visible tokens. Long artifacts (briefs, plans, full subagent returns) are saved to `_FROM_CLAUDE/` (operator vault reading inbox) or `agents/<slug>/memory/` (ship vault compounding layer) with a pointer in chat — never pasted inline. Decisions are surfaced via AskUserQuestion, not prose. Self-check before emitting any response ≥2K visible tokens: is this the distilled verdict + action + reasoning + pointer? If not, distill first. Source: morning verbose-return failure mode, locked 2026-05-21.

---

## Section 0.1 — Memory Architecture (ship-safe)

### The 4-tier model

| Tier | Backend | When to use | Cost | Offline |
|---|---|---|---|---|
| **1 — Vector + Graph** | ChromaDB (local) + graphify | Cross-cutting synthesizers whose job is concept retrieval across 1K+ docs | $0 — local CPU | Yes |
| **2 — SQLite** | stdlib sqlite3, WAL mode | Structured state that needs SQL (deals, orders, threads, setups) — grows past what grep handles reliably | $0 — stdlib | Yes |
| **3 — PDF/vectorless** | markitdown → markdown | Drawing packs, vendor specs, PDFs the agent reads but doesn't store structured state from | $0 — markitdown | Yes |
| **4 — Markdown + grep** | Files + ripgrep/glob | All other agents — knowledge is narrative, sparse, or slow-moving. Compounding-append + graphify query on the shared shelf covers 80% of retrieval needs | $0 — stdlib | Yes |

### Per-agent tier assignments

| Agent | Tier | Backend | Notes |
|---|---|---|---|
| librarian | 1 | ChromaDB + graphify | Indexes full vault weekly |
| deep-researcher | 1 | ChromaDB + graphify | Indexes research corpus + shared shelf |
| account-manager | 2 | SQLite (`accounts.db`) | Accounts, deals, renewals, at_risk_signals |
| finance-manager | 2 | SQLite (`finance.db`) | Invoices, commissions, deal_economics |
| sales-director | 2 | SQLite (`pipeline.db`) | Prospects, deals, stage_transitions, outreach_log |
| shopify-agent | 2 | SQLite (`shopify.db`) | Orders, line_items, customers, merchants, fulfillment |
| trading-analyst | 2 | SQLite (`trading.db`) | Setups, posture_history, journal, learnings |
| inbox-manager | 2 | SQLite (`messages.db`) | Threads, messages, drafts, escalations, triage_status |
| engineering-lead | 3 | markitdown + PDF | Drawing packs, vendor specs — read-only |
| chief-of-staff | 4 | Markdown + grep | Idea log, dispatch log, assignment briefs |
| content-strategist | 4 | Markdown + grep | Editorial strategy, brief archive |
| copywriter | 4 | Markdown + grep | Copy patterns, voice notes |
| creative-director | 4 | Markdown + grep | Brand decisions, direction history |
| designer | 4 | Markdown + grep | Design decisions, UI patterns |
| marketing-director | 4 | Markdown + grep | Campaign history, channel strategy |
| product-manager | 4 | Markdown + grep | Product specs, roadmap decisions |
| r-and-d-lead | 4 | Markdown + grep | Experiment logs, prototype notes |
| seo-specialist | 4 | Markdown + grep | Keyword maps, AEO baselines |
| social-media-manager | 4 | Markdown + grep | Post archive, engagement patterns |
| software-dev-team | 4 | Markdown + grep | Architecture decisions, implementation notes |

### Cross-agent communication patterns

- **Shared shelf** (`.claude/reference/`) — primary read path for any cross-cutting knowledge. Any agent reads any subfolder. Written by librarian's weekly sweep.
- **graphify query** — every agent's Step 1 queries the shared shelf graph (`python -m graphify query "..." --budget 1500`) before answering substantive questions. Faster than walking folders; returns only matching files.
- **Per-agent subgraph** — each agent's `graphify-out/` is an index over its own `memory/`. Regenerated weekly by `scripts/regenerate-agent-subgraphs.py`.
- **Chief-of-staff dispatch** — cross-agent work flows via chief-of-staff assignment briefs (`agents/chief-of-staff/assignments/`). Agents do not read each other's memory directly.
- **Inbox routing** — captures land in `inbox/` and are routed by the router to ONE home: shared shelf or agent memory. Never duplicated.

### Cost picture

- **$0/month** — no cloud services, no API subscriptions, no hosted databases.
- **ZERO API keys** required for base operation. Optional: operator may provide Shopify, Gmail, or other connector credentials in operator-mode config.
- **Works offline** — ChromaDB is local (PersistentClient, no server). sentence-transformers runs on CPU. sqlite3 is stdlib. graphify is local Python.
- **One-time model download** — librarian + deep-researcher download `all-MiniLM-L6-v2` (~200MB) on first `embed.py index` run. Cached to `~/.cache/huggingface/`. All subsequent runs are offline.

### Upgrade path (operator/cohort versions)

| From | To | When | How |
|---|---|---|---|
| Tier 4 (markdown) | Tier 2 (SQLite) | Agent accumulates structured state that grep struggles with (>500 records) | Write `schema.sql` + `db.py`, update SKILL.md Step 1 |
| Tier 1 local Chroma | Tier 1 hosted Chroma | Multi-user cohort, shared retrieval across operator instances | Swap `chromadb.PersistentClient` for `chromadb.HttpClient`, set `CHROMA_HOST` env var |
| Local embedder | OpenAI `text-embedding-3-small` | Operator wants higher-quality embeddings and accepts API cost | Swap `SentenceTransformerEmbeddingFunction` for `OpenAIEmbeddingFunction` in `embed.py` — gated by `OPENAI_API_KEY` env var |

Tier downgrades are never automatic. Tier upgrades require operator approval (reversibility gate).

---

## Section 1 — Vault structure

```
rook/
├── _CLAUDE.md                ← THIS FILE (vault operating rules)
├── CLAUDE.md                 ← top-level routing contract
├── MASTER_INDEX.md           ← cross-agent wikilink hub (auto-generated)
├── agents/                   ← the 20 specialist agents
│   └── <agent>/
│       ├── SKILL.md          ← agent body
│       ├── CLAUDE.md         ← agent routing scope
│       ├── README.md         ← human-facing description
│       ├── personality/      ← _bench.md + frameworks index
│       └── memory/           ← agent learned state (versioned-append; per-agent)
├── .claude/
│   ├── reference/            ← SHARED shelf (API docs, templates, SOPs, methodology — readable by ALL agents)
│   ├── reference/graphify-out/  ← graphify index over the shelf (librarian regenerates weekly)
│   └── connectors/           ← MCP-backed + clean-REST service clients with shared creds
├── projects/                 ← customer's job-shaped work
├── hooks/                    ← runtime enforcement (.ps1 + .sh + routing-rules.json)
├── scripts/                  ← maintenance scripts (regenerate-routing-rules.py, etc.)
├── inbox/                    ← capture landing zone (router moves files out to shelf OR agent memory)
└── _archive/                 ← librarian-quarantined content (append-only, never deleted)
```

**Per-agent context-loading pattern:** every agent's Step 1 reads its OWN `memory/MEMORY.md` (catalog) + relevant `memory/` files on session start. Domain-bound questions then **query the shared shelf via graphify** (`python -m graphify query "..." --budget 1500`) — the graph indexes `.claude/reference/` so the agent pulls only matching files instead of walking folders. Cross-agent reads happen via explicit handoff to librarian, NOT by reading another agent's memory directly.

---

## Section 2 — Files you MUST NOT rewrite (immutable / append-only)

| Class | Path | Behavior |
|---|---|---|
| Routed captures | `inbox/` (pre-route) and dated routed files under `.claude/reference/<topic>/` or `agents/<agent>/memory/captures/` | IMMUTABLE — operator voice preserved verbatim. Cross-ref via NEW files; never edit the source. |
| Idea log | `agents/chief-of-staff/memory/idea_log.md` | APPEND-ONLY ledger. New entries at the bottom; never rewrite existing. |
| Dispatch log | `agents/chief-of-staff/memory/dispatch_log.md` | APPEND-ONLY table. Add rows; never edit existing rows. |
| Session handoffs | `_archive/HANDOFFS/session-*.md` | APPEND-ONLY. Auto-generated. |
| `MASTER_INDEX.md` | repo root | AUTO-GENERATED by librarian's weekly sweep. Never hand-edit. |
| Per-agent context INDEX | `agents/*/memory/MEMORY.md` | AUTO-GENERATED. Never hand-edit. |
| Routing-rules.json keyword arrays | `hooks/routing-rules.json` (primary/secondary) | AUTO-MIRRORED from each agent's SKILL.md `## Routing Keywords` block. Edit SKILL.md and run `python scripts/regenerate-routing-rules.py`. |
| `_template_memory.md` | every `memory/` folder | TEMPLATE. Update canonical at agent root; mirror to dept folders if needed. |

---

## Section 3 — Files you MAY versioned-append (the compounding layer)

These ARE candidates for rewrite — but **versioned-append, not rewrite-in-place**.

| Class | Path | Behavior |
|---|---|---|
| Agent memory files | `agents/*/memory/<topic>.md` | When contradicting info lands: add `## ⚠️ CONTRADICTION YYYY-MM-DD` at top, surface both versions, wait for operator lock, THEN add `## v<n> — YYYY-MM-DD` block. Original v1 stays. |
| Feedback / lessons | `agents/*/memory/feedback_*.md` | Same versioned-append rule. |
| `MEMORY.md` index | `agents/*/memory/MEMORY.md` | EXCEPTION — this is a router, not a record. Edit-in-place is fine. |

**Pattern:**
1. New info arrives that contradicts an existing memory.
2. Add `## ⚠️ CONTRADICTION YYYY-MM-DD` block at top with both versions + the source files.
3. Surface to operator: *"Contradiction found. Old: X. New: Y. Source: Z. Lock?"*
4. After operator lock, ADD a `## v<n+1> — YYYY-MM-DD` block with the new state. **Original v1 stays.**
5. Move the `## For future Claude (TL;DR)` to reflect the current state. Archive the old TL;DR under its version block.

**File-size cap (400 lines) — protocol when a versioned-append file approaches/exceeds:**
1. Create `<topic>_archive_v<n>.md` next to the original — move OLDEST version blocks into the archive file.
2. Keep the most recent 2-3 versions + current TL;DR in the live file.
3. Add `## Earlier history` link at the bottom of the live file: `Earlier history preserved at [[<topic>_archive_v1]]`.
4. The archive file is APPEND-ONLY (do NOT continue versioning into it — once archived, it's frozen).

**Do NOT delete history.** Compounding history is the moat. Archive ≠ delete.

---

## Section 4 — When the contradiction-surfacer fires

- **On significant capture** — when a new file lands in `inbox/` and the router moves it to an agent's `context/`: scan agent memory for contradictions; surface candidates.
- **On weekly sweep** — librarian's Sunday-night graphify sweep: full vault contradiction-scan + stale-flag review + broken-wikilink check + duplicate-file check.
- **On explicit invocation** — operator says "audit my vault" / "find contradictions" / "what's stale" / "is anything out of date."

Do NOT fire on every conversation tick. Audits are surfacing operations, not silent rewrites.

---

## Section 5 — Cross-agent routing on writes

The "never create in isolation" rule:

| You create/update... | Also update / cross-ref... |
|---|---|
| Agent brief in `<agent>/memory/` | Add `related:` frontmatter array; link the chief-of-staff dispatch entry if relevant. |
| New chief-of-staff dispatch | Append to `idea_log.md` AND row to `dispatch_log.md`. |
| Cross-cutting decision (spans 2+ agents) | Add line to `MASTER_INDEX.md` cross-references. |
| Brand decision | Cross-ref `creative-director` + `marketing-director` + any affected `<agent>/CLAUDE.md`. |
| Pre-launch decision (designer/copywriter/etc.) | State whether the upstream dispatch chain ran (creative-director → marketing-director → downstream). |

---

## Section 6 — Voice rules (house style)

- **Terse over polished.** Lead with the answer/action.
- **No preamble.** No "Great question!" No "Let me think..."
- **One sentence > three.**
- **Banned phrases:** delve, leverage (verb-as-filler), robust, harness, unlock, elevate (verb), transformative, synergy, ecosystem, 10x, level up, deep dive, as an AI.
- **No emojis in artifacts** unless explicitly asked.
- **Verify before claiming.** When the operator says "this is wrong," diff the data first; don't reflexively concede.

---

## Section 7 — What is NOT installed (intentional)

These were considered and rejected:

- **Karpathy LLM Wiki rewrite-on-update** — anti-thetical to compounding-as-moat. The audit trail IS the product.
- **Mem0 / LangGraph / LangChain memory frameworks** — different architectural paradigm. ROOK uses file-based Tier 4 memory + graphify weekly synthesis. Re-evaluate for v2 if scale demands per-customer conversational memory.

What IS installed:

- **graphify** — knowledge-graph generator over the vault. Each agent's `graphify-out/REPORT.md` is regenerated weekly by the librarian.
- **obsidian-cli** — programmatic vault read/write.
- **markitdown** — universal file → markdown conversion (the input layer for any artifact the operator drops in).
- **inbox-routing** — keyword-based capture routing to per-agent `context/`.
- **MCP servers** — standardized tool access across agents.

**Filter to apply BEFORE installing any future pattern:** does this preserve audit trail + compound history + handle multi-agent reads? If any of the three is no, the pattern fails the gate.

---

*Last updated 2026-05-19. Compounding-Append + Contradiction-Surfacer pattern locked.*
