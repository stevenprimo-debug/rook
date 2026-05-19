# The Context Loop

> The substrate that makes ROOK an Agentic OS instead of a bag of agents.

ROOK is an Agentic OS — the coordination layer above your agents. An Agentic OS manages five things: orchestration (who handles what), memory (what gets remembered), **context** (what each agent knows), specialization (how agents compose), and feedback (how the system gets better). The Context Loop is how ROOK delivers the third pillar — and the fifth, because the loop is self-reinforcing.

The 20 agents are the surface; the Context Loop is the substrate. Every capture you make — a phone screenshot, a voice memo, a web clipping, a PDF — flows through five stages and ends up in the right agent's working memory, where it stays compounded until it stops earning its keep.

## The five stages

```
1. CAPTURE   ─→   2. INGEST   ─→   3. ROUTE   ─→   4. READ   ─→   5. PRUNE
   (any input)     (→ markdown)    (→ agent)       (every fire)    (weekly)
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

### 3. Route — single primary agent, with explicit fan-out when needed

`inbox-routing` reads each ingested markdown file's content + frontmatter + filename and scores it against each agent's `routing_keywords` (defined in that agent's `SKILL.md` frontmatter).

**Default behavior:** the highest-scoring agent gets the file. It writes to `agents/<agent>/context/YYYY-MM/<slug>.md`. One file, one home, no duplication.

**Fan-out override:** if you spot a capture that legitimately serves multiple agents (a competitor's pricing screenshot is relevant to sales-director AND deep-researcher AND marketing-director), add this to the file's frontmatter:

```yaml
routes-to: [sales-director, deep-researcher, marketing-director]
```

The librarian's next weekly sweep notices the `routes-to:` entry and creates symlinks into each additional agent's `context/` folder. The original file stays single-sourced — only one truth, multiple read paths.

### 4. Read — every agent loads context on session start

When you invoke any agent, Step 1 of its master skill (the canonical opening of every ROOK agent's SKILL.md) reads:

```
agents/<agent>/context/    ← human-curated + auto-routed material
agents/<agent>/memory/     ← agent-written learned state
```

The agent walks into the session already knowing what's been captured for it. You don't paste, you don't reference — the context is already loaded.

**This is the compounding step.** Every session, the agent reads what's there. Every capture you make adds to what's there. Six months in, the designer agent has read every screenshot of every reference you ever liked, every brand decision you ever wrote down, every voice memo about why the last project failed. The agent isn't smarter — its context is denser.

### 5. Prune — librarian weekly sweep, auto-quarantine, on-demand restore

The vault stays fast and accurate because the librarian agent runs every week and quarantines content that no longer earns its keep.

**What the librarian does each Sunday night:**

1. Walks every agent's `context/` and `memory/`
2. Scores each file against the prune policy (see [`agents/librarian/prune-policy.md`](agents/librarian/prune-policy.md))
3. Moves stale files to `_archive/<YYYY-MM>/pruned/` with a one-line reason in `librarian-log.md`
4. Reconciles any `routes-to:` frontmatter updates from the last week (creates new symlinks, removes stale ones)
5. Writes the Monday digest

**What you see Monday morning:** a single markdown digest at the vault root. "Quarantined 47 notes last week. 12 from designer/context (>90 days unread), 18 from deep-researcher/context (superseded by newer notes), 17 from copywriter/memory (legacy patterns)." Each entry is one line with a restore command. One scan, three decisions, back to work.

**Quarantine, never delete.** Pruning moves files to `_archive/`. You can restore any file with one command at any time. The history is the audit trail; HEAD is the current best.

---

## Memory tier per agent

Most agent products ship one memory backend and call it a day. ROOK ships four, and each agent runs the backend that fits its work. The customer doesn't choose; the agent's tier is declared in its SKILL.md frontmatter and the librarian respects it during the weekly sweep.

| Tier | Backend | Who runs it | What it stores |
|---|---|---|---|
| **1 — Synthesizer** | Vector index + graph subset | chief-of-staff · librarian · deep-researcher | Semantic search across the vault + entity relationships across many files |
| **2 — Structured operator** | SQLite | sales-director · finance-manager · trading-analyst · shopify-agent | Deals, transactions, positions, products — anything tabular |
| **3 — Document reader** | Vectorless, on-demand PDF read | engineering-lead | CAD drawings, spec sheets, long technical PDFs queried per-session |
| **4 — Default** | Markdown + grep | the other 12 agents | Files ARE the index; no preprocessing |

**Why per-agent, not per-query:** the agent's data shape doesn't change every query. The shape is a property of the work, not the question. Sales pipeline data is tabular every day; brand guidelines are markdown every day. Picking the memory architecture per agent (declared once, used for every session) is simpler, cheaper, and explainable.

**How to choose a tier (the lesson, from the IG decision-guide framework):**

1. **What is the shape of this agent's data?** Text blobs → Tier 1 or 4. Numbers + structured fields → Tier 2. Reference PDFs that don't change → Tier 3.
2. **How dense are the relationships across files?** High → Tier 1 (graph). Low → Tier 4.
3. **Does the agent need exact lookups?** Yes → Tier 2 (SQL). No → Tier 1 or 4.
4. **How big does the corpus get?** Stays small (<100 files) → Tier 4 is fine. Grows past that → upgrade to Tier 1.

This is the cohort lesson on memory architecture — when to upgrade an agent from Tier 4 to Tier 1 because the corpus crossed the point markdown alone can serve.

### Tier 1 — vector index location

Each Tier 1 agent has a private vector index at:

```
agents/<agent>/memory/.vector-index/
```

Git-ignored. Rebuilt by the librarian during the Sunday sweep. Per-agent scope — no agent reads another's index directly; cross-agent context flows through explicit `routes-to:` frontmatter and `context/00-inherited.md` cross-references.

### Tier 2 — SQLite schemas

Each Tier 2 agent ships with a minimal default schema in its `memory/` folder. The customer extends with `ALTER TABLE` as their work grows. Defaults:

- **sales-director** — `memory/pipeline.db` → `deals(id, name, stage, value, gp_pct, owner, created_at, updated_at)`
- **finance-manager** — `memory/transactions.db` → `transactions(id, date, type, amount, category, notes)`
- **trading-analyst** — `memory/positions.db` → `positions(id, ticker, side, entry, stop, target, size, status, opened_at, closed_at)`
- **shopify-agent** — `memory/store.db` → `products(id, sku, title, price, margin_pct, status)` + `orders(id, product_id, qty, customer, status, ordered_at)`

Defaults exist so the agent works on day one. Customer-authored extensions are the moat the cohort teaches.

### Tier 3 — vectorless document reads

Tier 3 agents do NOT preprocess their document corpus. PDFs sit in `agents/<agent>/context/sources/` and get read on agent demand — not in background. Right for engineering-lead because spec sheets and drawings are large, infrequently queried, and don't benefit from vector embedding when only a few sections are needed per session.

### Tier 4 — markdown + grep

The default for all 12 remaining agents. Files in `agents/<agent>/context/` and `agents/<agent>/memory/` are the index. Step 1 of the master skill loads them on session start. No preprocessing, no vectors, no DB. Files ARE the corpus.

This is the right starting tier for any new agent. Upgrade to Tier 1 only when the corpus grows past the point where markdown + grep stops returning useful matches.

---

## Why this is the product

Most agent tools ship the agents. ROOK ships the loop the agents run inside.

The loop is what means your agents get smarter over time without you doing anything. The capture habit is the only input you provide. The librarian handles the cleanup. The router handles the filing. The agents handle the work.

A subscription justifies itself when something runs continuously and produces something you can see. The Monday digest is that artifact. Every week, you can scroll the digest and watch the loop working — what got captured, what got routed where, what got quarantined, what your agents read into context. The proof of the system is visible by design.

---

## What the customer authors (the moat layer)

The Context Loop ships with sensible defaults. Customers tune four levers:

1. **Routing keywords** in `routing-rules.json` and each agent's SKILL.md `routing_keywords` block — what fires what.
2. **Voice modes** in `agents/<agent>/personality/voice_modes/<custom>.md` — how each agent sounds.
3. **Prune policy** in `agents/librarian/prune-policy.md` — how aggressive the librarian is.
4. **Cross-references** in each agent's `context/00-inherited.md` — when one agent should also read another's context.

These four files are what the cohort teaches. ROOK ships the system; the cohort teaches you to make it yours.

---

## What this is NOT

- **NOT a vector database.** Context lives as markdown files in folders. Agents read files on session start. The librarian builds a graph over time (Phase 3); the substrate is filesystem-first.
- **NOT a departments-as-folders abstraction.** Each agent owns its own context. When one agent needs another's, it lists the path explicitly in `context/00-inherited.md`. Per-agent + explicit cross-references survives any refactor where agents get swapped, renamed, or replaced.
- **NOT a multi-route-by-default router.** Routing is single-primary-with-explicit-override. Duplicate-context-everywhere is worse than under-routing — the customer adds `routes-to:` when fan-out is the right call.
- **NOT a delete-and-forget system.** Pruning is quarantine. History is the audit trail. The compounding-append rule is the moat.

---

## Cross-references

- [`agents/librarian/SKILL.md`](agents/librarian/SKILL.md) — vault custodian; weekly sweep + on-demand restore
- [`agents/librarian/prune-policy.md`](agents/librarian/prune-policy.md) — customer-tunable pruning rules
- [`.claude/skills/registry/inbox-routing/SKILL.md`](.claude/skills/registry/inbox-routing/SKILL.md) — the router
- [`.claude/skills/core/markitdown/SKILL.md`](.claude/skills/core/markitdown/SKILL.md) — the ingestion layer
- [`vault-provenance.md`](vault-provenance.md) — what's in the box (the receipt)
- [`agents/_template/SKILL.md`](agents/_template/SKILL.md) — every agent inherits the Step 1 context-load pattern from here
