# The Context Loop

> The substrate that makes ROOK an Agentic OS instead of a bag of agents.

ROOK is an Agentic OS — the coordination layer above your agents. An Agentic OS manages five things: orchestration (who handles what), memory (what gets remembered), **context** (what each agent knows), specialization (how agents compose), and feedback (how the system gets better). The Context Loop is how ROOK delivers the third pillar — and the fifth, because the loop is self-reinforcing.

The 20 agents are the surface; the Context Loop is the substrate. Every capture you make — a phone screenshot, a voice memo, a web clipping, a PDF — flows through five stages and ends up indexed in a shared knowledge graph, queryable by any agent, persistent until the librarian quarantines it.

## The five stages

```
1. CAPTURE   ─→   2. INGEST   ─→   3. ROUTE   ─→   4. QUERY   ─→   5. PRUNE
   (any input)     (→ markdown)    (→ shelf OR    (graph query     (weekly
                                    agent memory)  on agent fire)   librarian)
```

### 1. Capture — any input, any device

What you can drop in:

- Phone screenshot (Obsidian Sync auto-syncs to vault)
- Voice memo (Whisper → markdown)
- Web clipping (Obsidian Web Clipper extension)
- PDF / DOCX / XLSX / audio / video (file drop in vault inbox)
- YouTube URL (transcribed via yt-dlp → Whisper)

Captures land in `inbox/` at the vault root. No tagging required. No "which folder?" decision required at capture time.

### 2. Ingest — every format becomes clean markdown

`markitdown` (universal-stack capability, baked into every agent) converts every input to clean markdown. PDF tables, scanned images, audio transcripts, video transcripts, image-with-OCR — all normalized to one shape before routing happens.

This is the layer that means **the capture format never determines what comes next.** A screenshot and a voice memo and a PDF all arrive at stage 3 looking identical.

### 3. Route — two destinations, decided by content

`inbox-routing` reads each ingested markdown file's content + frontmatter + filename and classifies it into ONE of two destinations:

**Destination A — Shared shelf (`.claude/reference/<topic>/`):**
Cross-cutting reference material that ANY agent might need. API docs, contract templates, library references, methodology playbooks, industry intel. Filed by topic (`shopify/`, `tradingview/`, `templates/`, `methodology/`, etc.), not by consuming agent. One file lives in one place; the graph (see Stage 4) makes it findable from any angle.

**Destination B — Agent memory (`agents/<agent>/memory/`):**
Agent-specific learnings, decisions the agent owns, compounding feedback from session-by-session work. The agent's own brain, distinct from the shared institutional library. Compounding-append pattern — versioned, never silently rewritten.

**Fan-out is NOT the default.** Each file has one home. The graph handles "which agent should care about this" via semantic query, not via folder duplication. If the customer wants explicit cross-agent visibility, they can add a frontmatter pointer — but the graph alone usually does the work.

### 4. Query — agents read context on demand via the graph

When you invoke any agent, Step 1 of its master skill loads the agent's identity (personality, memory) — that's cheap. For anything in its domain, it then **queries the graph** built by graphify on the shared shelf:

```bash
graphify query "shopify webhook implementation"
# → returns the 5 most relevant files across the shelf
```

The agent walks into the session knowing how to find what it needs — and pulls only the files that match its current question. No 50-file folder walks. No stale context dumped into every prompt. Just-in-time loading via graph traversal.

**This is the compounding step.** Every file you add to the shelf becomes a node in the graph. Every agent that reads it leaves a faint usage trace. Six months in, the graph encodes thousands of cross-references — Shopify webhook docs link to operator-confirm gates link to Tradovate order endpoints link to your customer-trust pattern memory. The agent isn't smarter; the graph is denser.

**What graphify gives you (the GraphRAG layer):**
- Knowledge graph with entity + relation extraction
- Community detection (cross-document patterns you didn't ask for)
- BFS / DFS traversal for query
- Multi-hop reasoning (`graphify path "AuthModule" "Database"`)
- Audit trail (EXTRACTED / INFERRED / AMBIGUOUS labels with confidence scores)
- Token-budgeted responses (`--budget 1500`)
- MCP server option for live agent access
- Incremental updates — only re-extracts changed files

### 5. Prune — librarian weekly sweep, auto-quarantine, on-demand restore

The vault stays fast and accurate because the librarian agent runs every week.

**What the librarian does each Sunday night (or whatever weekly cadence the customer configures):**

1. Runs `graphify update .` — re-indexes any new/changed files (incremental, ~5-10 min)
2. Walks the shared shelf + every agent's memory
3. Scores each file against the prune policy (see [`agents/librarian/prune-policy.md`](agents/librarian/prune-policy.md))
4. Moves stale files to `_archive/<YYYY-MM>/pruned/` with a one-line reason
5. Surfaces dedup candidates (graph's `semantically_similar_to` edges)
6. Surfaces shelf-promotion candidates (when 2+ agents have memory entries about the same concept)
7. Writes the Monday digest to `agents/librarian/digests/<YYYY-MM-DD>-digest.md`

**What you see Monday morning:** a single digest in `agents/librarian/digests/`. "Quarantined 47 notes last week. 12 from designer/memory (>90 days unread), 18 superseded by newer notes, 17 dedup candidates flagged. Two patterns ready to promote from memory to shelf (designer + creative-director both learned X)." Each entry is one line with a restore command. One scan, three decisions, back to work.

**Quarantine, never delete.** Pruning moves files to `_archive/`. You can restore any file with one command at any time. The history is the audit trail; HEAD is the current best.

---

## The two top-level inboxes

| Folder | What lands here | Direction |
|---|---|---|
| `inbox/` | Customer captures — screenshots, voice memos, clippings, PDFs | Customer → ROOK |
| `_from_rook/` | ROOK artifacts for the customer to read — briefs, plans, digests, reports | ROOK → Customer |

The `_from_rook/` convention (carried over from the operator's workflow): when any agent generates a doc the customer is meant to read later in Obsidian (a session brief, a Monday digest, a research summary, a meeting prep), it writes there with a date-prefixed slug — `_from_rook/2026-05-20-monday-digest.md`. That folder is the customer's reading queue.

---

## Memory tier per agent

Most agent products ship one memory backend and call it a day. ROOK ships four, and each agent runs the backend that fits its work. The customer doesn't choose; the agent's tier is declared in its SKILL.md frontmatter and the librarian respects it during the weekly sweep.

| Tier | Backend | Who runs it | What it stores |
|---|---|---|---|
| **1 — Synthesizer** | Vector index + graph subset | chief-of-staff · librarian · deep-researcher | Semantic search across the shelf + entity relationships across many files |
| **2 — Structured operator** | SQLite | sales-director · finance-manager · trading-analyst · shopify-agent | Deals, transactions, positions, products — anything tabular |
| **3 — Document reader** | Vectorless, on-demand PDF read | engineering-lead | CAD drawings, spec sheets, long technical PDFs queried per-session |
| **4 — Default** | Markdown + grep + graph query | the other 12 agents | Files ARE the index (in shared shelf + per-agent memory); graphify is the cross-shelf retrieval layer |

**Why per-agent, not per-query:** the agent's data shape doesn't change every query. Sales pipeline data is tabular every day; brand guidelines are markdown every day. Picking the memory architecture per agent (declared once, used for every session) is simpler, cheaper, and explainable.

**How to choose a tier (the lesson, from the IG decision-guide framework):**

1. **What is the shape of this agent's data?** Text blobs → Tier 1 or 4. Numbers + structured fields → Tier 2. Reference PDFs that don't change → Tier 3.
2. **How dense are the relationships across files?** High → Tier 1 (graph). Low → Tier 4.
3. **Does the agent need exact lookups?** Yes → Tier 2 (SQL). No → Tier 1 or 4.
4. **How big does the corpus get?** Stays small (<100 files) → Tier 4 is fine. Grows past that → graphify gives Tier-1-style query without a separate vector index.

This is the cohort lesson on memory architecture — when to upgrade an agent's data layer because the corpus crossed the point markdown alone can serve.

### Tier 1 — vector index location

Each Tier 1 agent has a private vector index at:

```
agents/<agent>/memory/.vector-index/
```

Git-ignored. Rebuilt by the librarian during the Sunday sweep. The shared graph at `.claude/reference/graphify-out/graph.json` already provides cross-shelf semantic retrieval — Tier 1 vector indexes are only needed for agent-specific fuzzy search beyond what the graph offers.

### Tier 2 — SQLite schemas

Each Tier 2 agent ships with a minimal default schema in its `memory/` folder. The customer extends with `ALTER TABLE` as their work grows. Defaults:

- **sales-director** — `memory/pipeline.db` → `deals(id, name, stage, value, gp_pct, owner, created_at, updated_at)`
- **finance-manager** — `memory/transactions.db` → `transactions(id, date, type, amount, category, notes)`
- **trading-analyst** — `memory/positions.db` → `positions(id, ticker, side, entry, stop, target, size, status, opened_at, closed_at)`
- **shopify-agent** — `memory/store.db` → `products(id, sku, title, price, margin_pct, status)` + `orders(id, product_id, qty, customer, status, ordered_at)`

Defaults exist so the agent works on day one. Customer-authored extensions are the moat the cohort teaches.

### Tier 3 — vectorless document reads

Tier 3 agents do NOT preprocess their document corpus. Reference PDFs live in `.claude/reference/<topic>/sources/` on the shared shelf and get read on agent demand — not in background. Right for engineering-lead because spec sheets and drawings are large, infrequently queried, and don't benefit from vector embedding when only a few sections are needed per session.

### Tier 4 — markdown + grep + graph query

The default for all 12 remaining agents. The shared shelf (`.claude/reference/`) + per-agent memory (`agents/<agent>/memory/`) ARE the corpus. Graphify provides cross-shelf semantic retrieval for everyone, regardless of tier. No preprocessing, no embeddings, no separate DB needed for default-tier agents.

This is the right starting tier for any new agent. Upgrade to Tier 1 (per-agent vector) only when the corpus grows past the point where shared-shelf graph query stops returning useful matches.

---

## Why this is the product

Most agent tools ship the agents. ROOK ships the loop the agents run inside.

The loop is what means your agents get smarter over time without you doing anything. The capture habit is the only input you provide. The librarian handles the cleanup. The router handles the filing. The graph handles the retrieval. The agents handle the work.

A subscription justifies itself when something runs continuously and produces something you can see. The Monday digest in `_from_rook/` is that artifact. Every week, you can scroll the digest and watch the loop working — what got captured, what got routed where, what got quarantined, what the graph grew, what your agents read into context. The proof of the system is visible by design.

---

## What the customer authors (the moat layer)

The Context Loop ships with sensible defaults. Customers tune four levers:

1. **Routing keywords** in `routing-rules.json` and each agent's SKILL.md `routing_keywords` block — what fires what.
2. **Voice modes** in `agents/<agent>/personality/voice_modes/<custom>.md` — how each agent sounds.
3. **Prune policy** in `agents/librarian/prune-policy.md` — how aggressive the librarian is.
4. **Frontmatter on shelf files** — `consumers: [agent1, agent2]`, `last_verified: YYYY-MM-DD`, `status: v1`. The graph reads this metadata; richer frontmatter = sharper queries.

These four levers are what the cohort teaches. ROOK ships the system; the cohort teaches you to make it yours.

---

## What this is NOT

- **NOT a per-agent context dump.** Agents don't read everything on session start. They query the graph for the relevant 3-5 files. Token-efficient, fast, focused.
- **NOT a departments-as-folders abstraction.** The shared shelf is organized by topic (Shopify, TradingView, templates), not by consuming agent. Any agent reads any topic via graph query.
- **NOT a multi-route-by-default router.** Each file lives in one place. The graph makes it findable from any angle — that's the whole point of GraphRAG over folder routing.
- **NOT a delete-and-forget system.** Pruning is quarantine. History is the audit trail. Compounding-append is the moat.
- **NOT hybrid vector+graph RAG.** ROOK ships pure-graph GraphRAG (graphify). Entity-driven queries, multi-hop reasoning, community detection. The vector layer is an optional upgrade per agent (Tier 1), not the default.

---

## Cross-references

- [`agents/librarian/SKILL.md`](agents/librarian/SKILL.md) — vault custodian; weekly sweep + on-demand restore + graphify rebuild cadence
- [`agents/librarian/prune-policy.md`](agents/librarian/prune-policy.md) — customer-tunable pruning rules
- [`.claude/reference/README.md`](.claude/reference/README.md) — the shared shelf inventory
- [`.claude/reference/graphify-out/graph.json`](.claude/reference/graphify-out/graph.json) — the knowledge graph (machine-queryable)
- [`.claude/reference/graphify-out/GRAPH_REPORT.md`](.claude/reference/graphify-out/GRAPH_REPORT.md) — the graph audit (god nodes, communities, surprising connections)
- [`.claude/skills/registry/inbox-routing/SKILL.md`](.claude/skills/registry/inbox-routing/SKILL.md) — the router
- [`.claude/skills/core/markitdown/SKILL.md`](.claude/skills/core/markitdown/SKILL.md) — the ingestion layer
- [`vault-provenance.md`](vault-provenance.md) — what's in the box (the receipt)
- [`agents/_template/SKILL.md`](agents/_template/SKILL.md) — every agent inherits the Step 1 context-load pattern from here
- [`_CLAUDE.md`](_CLAUDE.md) § rule #12 — the universal context-load gate (graph query before training-data recall)
