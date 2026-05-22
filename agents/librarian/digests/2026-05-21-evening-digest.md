---
digest: 2026-05-21-evening
scope: ROOK vault only (C:\Users\User\Desktop\PrimoLabs_PoweredByClaude)
out_of_scope: operator vault (C:\Users\User\Desktop\PRIMOLABS\) — not touched
mode: digest-write
cadence: on-demand
scanned:
  - agents/*/SKILL.md, CLAUDE.md, README.md, personality/, memory/, graphify-out/, skills/
  - agents/_methodology-gap-index.md
  - agents/_ROSTER.md, .claude/agents/*.md
  - projects/, _from_rook/, _archive/, hooks/
deferred:
  - .claude/skills/registry/** (vendored skills, large; not memory-bearing)
  - scripts/, CORE/ (code, not docs)
---

# Librarian Evening Digest — 2026-05-21

## Executive Summary

- **Orphans:** 8 files (1 rename-duplicate registration, 4 zero-byte personality stubs, 2 thin bench stubs, 1 truncated return)
- **Broken edges:** 2 patterns (40 phantom methodology files referenced by gap-index but never created; 20 graphify-out stubs reporting "graphify not installed")
- **Contradictions:** 3 subgraphs (skeleton-frontmatter vs filled-body across 21 CLAUDE.md; "PRIMOLABS vault rules" vs ROOK product framing in 17 files; roster naming "Inbox Custodian" vs registration `inbox-manager.md`)
- **Low-read:** 0 candidates (vault is young — oldest file 2026-05-15, none meet the 90-day staleness floor from `prune-policy.md`)
- **Biggest red flag:** `agents/_methodology-gap-index.md` claims 40 substantive methodology files exist at `agents/<agent>/context/methodology/` — none of those folders or files exist anywhere in the repo. The index is hallucinated artifact documentation.

---

## 1. Orphan nodes (8)

Files in agents/ that no other ROOK file references, or that exist only as placeholder stubs.

| Path | Size | Issue | Recommended action |
|---|---|---|---|
| `.claude/agents/inbox-custodian.md` | 3425B | Duplicate registration — identical size + timestamp to `inbox-manager.md`; roster #4 uses `inbox-manager.md` | ARCHIVE FLAG → `_archive/2026-05/orphan-registrations/` |
| `agents/account-manager/personality/frameworks_index.md` | 0B | Zero-byte stub — empty file in load-bearing personality folder | FILL or ARCHIVE FLAG |
| `agents/account-manager/personality/frameworks_attribution.md` | 0B | Zero-byte stub | FILL or ARCHIVE FLAG |
| `agents/inbox-manager/personality/frameworks_index.md` | 0B | Zero-byte stub | FILL or ARCHIVE FLAG |
| `agents/inbox-manager/personality/frameworks_attribution.md` | 0B | Zero-byte stub | FILL or ARCHIVE FLAG |
| `agents/account-manager/personality/_bench.md` | 217B | Stub bench — placeholder-grade vs. 3-8KB peer benches | FILL (not archive — load-bearing) |
| `agents/inbox-manager/personality/_bench.md` | 144B | Stub bench — thinnest in roster | FILL (not archive — load-bearing) |
| `agents/designer/memory/returns/2026-05-21-music-city-cuts-identity.md` | 759B | Wave-2 return truncated — opens with "Upstream Chain Confirmation" header then stops; no actual identity system content | FILL or ARCHIVE FLAG (Wave 2 abandoned mid-write) |

**Why this matters:** Zero-byte files in load-bearing folders (`personality/`) tell the agent "no bench, no frameworks" rather than "this is missing" — the agent runs without its philosophy bench attached. Worse than absent.

---

## 2. Broken edges (2 patterns)

Documentation references that resolve to nothing.

| Source | Bad target | Issue | Recommended action |
|---|---|---|---|
| `agents/_methodology-gap-index.md` (lines 26-113) | `agents/<agent>/context/methodology/*.md` × 40 | Index claims 40 methodology files generated. Zero `context/` folders exist anywhere in `agents/`. Zero methodology/ folders. Files do not exist. | HARD GATE — operator decides: are the methodology files actually missing (build them) or is the gap-index aspirational/wrong (archive the index)? |
| 20× `agents/*/graphify-out/REPORT.md` | graphify capability | All 20 REPORTs say "graphify not installed or returned error" with the same `error: unknown command` body | SOFT GATE — fix graphify install, OR flag the auto-stub pattern for redesign |

**Wikilinks:** Zero `[[wikilink]]` references found outside librarian's own docs (`SKILL.md` describing what they mean, `prune-policy.md` describing inbound-link checking). The ROOK vault uses relative markdown paths, not wikilinks. No broken wikilinks to surface.

**External pointers (out of scope):** `agents/_methodology-gap-index.md` cites files like `project_canonical_stack.md`, `wealth_creator_mode.md`, `methodology_rfp_response_pipeline.md` — these belong to the operator vault, not ROOK. They're correctly external; flagging only so the customer-facing index doesn't ship with operator-vault-private references.

**Why this matters:** The methodology-gap-index sits at `agents/_methodology-gap-index.md` — a top-level index file, the kind a customer would read first. It promises 40 substantive methodology files that don't exist. That's the single biggest credibility risk in the vault right now.

---

## 3. Contradiction subgraphs (3)

| Subgraph | Detail | Recommended action |
|---|---|---|
| **Skeleton-frontmatter vs filled-body** | All 21 `agents/*/CLAUDE.md` files carry `status: skeleton` in frontmatter. Body content has diverged: 4 are filled (librarian, account-manager, inbox-manager, engineering-lead); 17 still have `[One-line role description.]` placeholders. Frontmatter `status:` no longer reflects body reality on 4 files. | SOFT GATE — flip `status: skeleton` → `status: complete` on the 4 filled CLAUDE.md files. |
| **"PRIMOLABS vault rules" vs ROOK product framing** | 18 of 21 CLAUDE.md files say `inherited from PRIMOLABS vault rules` in the Memory section. ROOK's top-level `CLAUDE.md` explicitly flags this as anti-pattern (real-company-names contamination). The 4 filled files say `ROOK vault rules`. | SOFT GATE — replace "PRIMOLABS" → "ROOK" in remaining 17 CLAUDE.md files + `agents/_template/CLAUDE.md`. |
| **Roster naming vs registration filename** | `.claude/agents/_ROSTER.md` line 10 names the agent "Inbox Custodian" but points to `inbox-manager.md`. The folder is `agents/inbox-manager/`. The orphan registration `.claude/agents/inbox-custodian.md` shows the old name was Inbox Custodian, renamed to Inbox Manager. Roster wasn't fully updated. | SOFT GATE — flip roster row 10 "Inbox Custodian" → "Inbox Manager" to match folder + registration. |

**Why this matters:** Each contradiction is small, but together they tell a customer reading the roster + a CLAUDE.md + the gap-index that the product is mid-migration. Customer-extensible product surfaces (`CLAUDE.md`, `_ROSTER.md`, top-level indices) carry brand bleed and skeleton flags. Project-level `CLAUDE.md` calls this out as anti-pattern; remaining 17 files violate it.

---

## 4. Low-read candidates (0)

Vault is too young to meet staleness threshold. Oldest tracked file: `agents/content-strategist/personality/frameworks_attribution.md` (2026-05-15, 6 days ago). `prune-policy.md` default `stale_after_days: 90`. No file qualifies.

**Why this matters:** Skip this section until ~2026-08-15. Re-run the staleness pass once any file crosses 90 days idle.

---

## 5. Prune candidates (archive flag only — no moves executed)

Items from §1 and §2 with recommended archive destinations. **Nothing has been moved.** Archive only with explicit operator approval.

| Path | Proposed destination | Soft/Hard gate |
|---|---|---|
| `.claude/agents/inbox-custodian.md` | `_archive/2026-05/orphan-registrations/inbox-custodian.md` | SOFT (clear duplicate, low risk) |
| 4× zero-byte personality files (acct-mgr + inbox-mgr) | `_archive/2026-05/zero-byte-personality/` IF the decision is "don't fill" — otherwise FILL not archive | SOFT (zero-content; harmless to archive) |
| `agents/designer/memory/returns/2026-05-21-music-city-cuts-identity.md` | `_archive/2026-05/truncated-returns/` OR finish the return | HARD (touches Wave 2 of active Music City Cuts dispatch — see `chief-of-staff/memory/idea_log.md` row 2 + `dispatch_log.md` row 2-3) |
| 20× `agents/*/graphify-out/REPORT.md` | Keep in place but fix graphify, OR add the path pattern to `.gitignore` | HARD (capability decision — does graphify ship with ROOK or not?) |
| `agents/_methodology-gap-index.md` | Keep + build the 40 missing files, OR archive the index | HARD (40 phantom files = product credibility risk; operator owns the call) |

---

## Approval gate

### Hard-gate items (require explicit operator approval before any action)

1. **Methodology gap-index reckoning** — 40 phantom files referenced. Build them, or archive the index? This is the single biggest item in tonight's digest.
2. **Designer Wave-2 return** — truncated. Finish it (Music City Cuts is still active per chief-of-staff dispatch log), or archive and re-dispatch designer?
3. **Graphify capability decision** — 20 auto-stub REPORTs report graphify not installed. Ship with broken capability + stubs, fix the install, or remove the pattern entirely?

### Soft-gate items (librarian would draft + run unless rejected in next digest)

1. Flip `status: skeleton` → `status: complete` in 4 filled CLAUDE.md files (librarian, account-manager, inbox-manager, engineering-lead).
2. Replace "PRIMOLABS vault rules" → "ROOK vault rules" in remaining 17 CLAUDE.md files + `_template/CLAUDE.md`.
3. Fix `_ROSTER.md` line 10 "Inbox Custodian" → "Inbox Manager".
4. Archive `.claude/agents/inbox-custodian.md` to `_archive/2026-05/orphan-registrations/`.
5. Fill or archive the 4 zero-byte personality files (account-manager + inbox-manager × frameworks_index + frameworks_attribution).
6. Fill or archive the 2 stub bench files (account-manager 217B, inbox-manager 144B).

### Not touched

- Operator vault `C:\Users\User\Desktop\PRIMOLABS\` — out of scope this run.
- `_archive/` contents — already archived, audit excludes.
- `.claude/skills/registry/**` — vendored skill packs, not memory-bearing.
- `scripts/`, `CORE/`, `hooks/` — code surfaces, not the librarian's beat.

---

## Compounding-append note

This digest is the HEAD for 2026-05-21. Future digests should append, never rewrite. If a hard-gate item resolves before next sweep, the resolution row appends as `RESOLVED <date>` and the old finding stays as audit trail.
