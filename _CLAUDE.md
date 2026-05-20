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
8. **Session-mode awareness** — operator-mode writes go to `<dir>/operator/` subpaths; customer-mode writes go to standard paths. See [`.claude/session-modes.md`](.claude/session-modes.md). `package-for-cohort.py` excludes `operator/` paths.
9. **Hierarchical Supervisor pattern** — Chief of Staff distills subagent returns to ≤2K tokens before surfacing (verdict + action + reasoning + source pointer; never raw paste). See [`agents/chief-of-staff/SKILL.md`](agents/chief-of-staff/SKILL.md) § Distilled Return rule.
10. **Anthropic Managed Agents deployment** — when deploying via Managed Agents (vs local Claude Code), the API requires `anthropic-beta: managed-agents-2026-04-01` header and is currently research-preview. See [`.claude/anthropic-deployment-notes.md`](.claude/anthropic-deployment-notes.md) for full spec, rate limits, and roster-size guidance.
11. **Visible-output gate** — agents NEVER narrate their own reasoning in visible output. All process-thinking goes in <thinking> blocks. First line is verdict/dispatch/question/artifact — banned: "Now I have a clear picture", "Let me check", "Actually,", "My next move is", "I am realizing/wondering/structuring". See agents/chief-of-staff/SKILL.md § VISIBLE OUTPUT GATE.

---

## Section 1 — Vault structure

```
PrimoLabs_PoweredByClaude/
├── _CLAUDE.md                ← THIS FILE (vault operating rules)
├── CLAUDE.md                 ← top-level routing contract
├── MASTER_INDEX.md           ← cross-agent wikilink hub (auto-generated)
├── agents/                   ← the 20 specialist agents
│   └── <agent>/
│       ├── SKILL.md          ← agent body
│       ├── CLAUDE.md         ← agent routing scope
│       ├── README.md         ← human-facing description
│       ├── personality/      ← _bench.md + frameworks index
│       ├── memory/           ← agent learned state (versioned-append)
│       ├── context/          ← human-curated reference + auto-routed captures
│       └── graphify-out/     ← per-agent synthesis (librarian regenerates)
├── projects/                 ← customer's job-shaped work
├── hooks/                    ← runtime enforcement (.ps1 + .sh + routing-rules.json)
├── scripts/                  ← maintenance scripts (regenerate-routing-rules.py, etc.)
├── inbox/                    ← capture landing zone (router moves files out)
└── _archive/                 ← librarian-quarantined content (append-only, never deleted)
```

**Per-agent context-loading pattern:** every agent's Step 1 reads its OWN `context/` + `memory/` folders on session start. Cross-agent reads happen via explicit handoff to librarian, NOT by reading another agent's memory directly.

---

## Section 2 — Files you MUST NOT rewrite (immutable / append-only)

| Class | Path | Behavior |
|---|---|---|
| Routed captures | `agents/*/context/YYYY-MM/*.md` | IMMUTABLE — operator voice preserved verbatim. Cross-ref via NEW files; never edit the source. |
| Idea log | `agents/chief-of-staff/memory/idea_log.md` | APPEND-ONLY ledger. New entries at the bottom; never rewrite existing. |
| Dispatch log | `agents/chief-of-staff/memory/dispatch_log.md` | APPEND-ONLY table. Add rows; never edit existing rows. |
| Session handoffs | `_archive/HANDOFFS/session-*.md` | APPEND-ONLY. Auto-generated. |
| `MASTER_INDEX.md` | repo root | AUTO-GENERATED by librarian's weekly sweep. Never hand-edit. |
| Per-agent context INDEX | `agents/*/context/INDEX.md` | AUTO-GENERATED. Never hand-edit. |
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
