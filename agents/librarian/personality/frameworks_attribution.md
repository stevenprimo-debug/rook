---
name: Librarian — Frameworks Attribution (academic credit, never invoked)
description: Academic credit for the figures who originated each methodology the librarian invokes. THIS FILE IS REFERENCE ONLY. The agent never names these figures in output. The frameworks themselves are listed in `frameworks_index.md` by methodology name; this file records their intellectual provenance for honest accounting.
type: frameworks-attribution
agent: librarian
version: "2.0.0"
---

## For future Claude (TL;DR — pinned HEAD as of 2026-05-14)

**Rule:** This is the ONLY file in the librarian agent folder where living people are named. The agent never names these figures in any output — chat, digest, audit log, hook registry, anywhere. When the librarian invokes a framework, it invokes it BY METHODOLOGY NAME from `frameworks_index.md`. The attribution exists for honest accounting and for the rare user-initiated "show me the lineage" curtain-pull, never for unsolicited surfacing.

**Status:** active.

**Why this rule exists:** Per voice-spine § 3.7 — *the work loses its concept the moment you point at it.* Naming the originators makes the agent sound like a literature review instead of a custodian. Worse, it dates the product and personalizes it to its author's tastemakers rather than to the principles themselves.

**Apply when:** considering naming a figure in any output. The answer is no, except when the user explicitly says "show the lineage" / "who came up with this" / "what's the origin of this framework."

---

## Vigilance-Pole framework origins

### Graph-based knowledge representation

Lineage traces through several decades of work in information science and knowledge graphs.

- **Tim Berners-Lee** — semantic web vision, linked data principles. The graph-of-claims framing.
- **Larry Page + Sergey Brin** — PageRank as a graph-traversal authority signal; the precursor to thinking of read-frequency as a graph signal.
- **Andrej Karpathy** — "LLM Wiki" proposal for autonomous knowledge bases; the librarian adopts ~25% of his pattern (contradiction-surfacing, future-Claude HEAD blocks, confidence levels) and rejects the rest (rewrite-on-update, scheduled rewrite agents, external research commands).

### Last-verified gates + stale-after triggers

- **Frederick Brooks** — *The Mythical Man-Month*, the observation that software (and by extension, documentation) decays without active maintenance.
- **Donella Meadows** — systems thinking on stocks-and-flows; staleness as a flow problem, not a stock problem.

### HEAD block / future-Claude TL;DR pattern

- **Linux kernel maintainers** — the discipline of writing for the person who will read the patch in five years.
- **Andrej Karpathy** — the explicit "future-Claude" framing from the LLM Wiki proposal.

### Routing-enforcer false-positive logging

- **[Product Owner] (vault author)** — the original feedback rule `feedback_routing_enforcer_false_positives.md`. the operator's own pattern.

### Index split discipline

- **Donald Knuth** — the discipline of cross-referenced index design from *The Art of Computer Programming*.
- **Library of Congress classification system** — split-by-topic when a category outgrows its slot.

---

## Pruning-Pole framework origins

### Archive vs. delete

- **Vannevar Bush** — *As We May Think* (1945); the Memex vision; the impulse to preserve trails of association.
- **Library of Congress + National Archives** — institutional archival practice; the legal and operational discipline that "removed from active circulation" ≠ "destroyed."
- **Git as a system** — versioned-everything; the idea that destructive operations should be opt-in, not default.

### Read-frequency analysis

- **PageRank**, again — citation frequency as a relevance signal.
- **John Sweller** — cognitive load theory; the case for an active corpus small enough to be cognitively loadable.

### Duplicate-concept detection

- **Christopher Alexander** — *A Pattern Language*; the discipline of naming a concept once, canonically, and pointing back to it.
- **Ward Cunningham** — wiki design; the "refactor to canonical" pattern from c2.com.

### Completed-project sprawl

- **Tiago Forte** — PARA system; the "archive" tier as the home for completed projects + their methodology promotion.

---

## Continuity-Pole framework origins

### Compounding-append + contradiction-surfacer

- **[Product Owner] (vault author)** — locked the pattern 2026-05-09 in vault `_CLAUDE.md` after reviewing Karpathy's LLM Wiki proposal. The 25% adoption / 75% rejection is the operator's call. The compounding-append framing is downstream of git semantics and Bush's Memex.
- **Linus Torvalds** — git's commit-as-immutable model; the substrate for compounding-append.

### HEAD-rewrite for state files

- **Git refs** — HEAD as the "current best," tags + commits as the historical context. Direct lift.

### Vault-manifest stub

- **Robert C. Martin** — *Clean Architecture*; the "boundary file" pattern — a small surface other modules read to coordinate without each running its own scan.
- **[Product Owner]** — the librarian-specific framing of the manifest as a session-start substrate other agents inherit.

### Three-tier autonomy cut (passive / mutating / blocking)

- **Anthropic Computer Use safety model** — the framing of agent actions by blast radius, with explicit human-in-the-loop for the irreversible tier.
- **[Product Owner]** — locked the specific 3-tier cut for the librarian 2026-05-14 16:14, the operator verbatim: *"I can't imagine we're ever going to talk to the librarian but the librarian creating hooks also seems like the librarian should be able to create hooks based on findings."*

---

## Synthesis framework origins

### Severity classifier (HIGH / MEDIUM / LOW)

- **Standard incident-response classification** from SRE practice; lifted directly.

### Hook tier classifier

- **Anthropic SDK hook patterns** + the operator's 3-tier autonomy lock.

### Librarian digest assembly

- **Pull-request / changelog tradition** — the digest is a weekly PR against the operator's attention.

### Monday Anchor anti-pattern check

- **[Product Owner]** — `feedback_dont_default_park_to_monday.md` (2026-05-12). The rule that "Monday Anchor is a checking cadence, not a trigger" is the operator's lock.

---

## On the role of attribution in agent output

The voice-spine rule (§ 3.7) is law: the librarian never names the figures above in output. When the librarian invokes a framework, it invokes the framework's METHODOLOGY NAME from `frameworks_index.md`. This is the same discipline that makes the chess-piece origin story (per `project_rook_brand.md`) appear in `/about` pages and YC pitches but never in hero copy. The work loses its concept the moment you point at it.

The exception, locked across all agents in the line: when the user explicitly asks *"who came up with this framework?"* or *"show me the lineage,"* the agent surfaces this file's relevant entry. That is the curtain-pull mode. It is reserved for the user pulling back the curtain — never for the agent volunteering it.

---

## On adding to this file

When the librarian adopts a new framework, the originator is recorded here in the relevant pole section. The entry includes:

- The figure's name.
- The methodology / work / lineage being credited.
- Whether the adoption is direct lift, partial adoption, or downstream framing.

Versioned-append: every addition gets a dated entry at the bottom.

---

## Versioned append (history)

- **2026-05-14** — Initial v2.0 lock. Attribution recorded for 15 frameworks across Vigilance/Pruning/Continuity/synthesis. Lineage spans Berners-Lee, Page, Brin, Karpathy, Brooks, Meadows, Linux kernel maintainers, Knuth, Library of Congress, Bush, National Archives, Torvalds, Sweller, PageRank tradition, Alexander, Cunningham, Forte, Martin, Anthropic Computer Use safety model, and [Product Owner] (vault author). Source: librarian build pass per v3 generator spec.

---

## Cross-references

- Frameworks index (callable methodologies, by name): `frameworks_index.md`
- Bench: `_bench.md`
- SKILL.md: `../SKILL.md`
- Voice spine "say it once, never repeat" rule: `.claude/voice-spine.md` § 3.7
- Memory failure modes: `.claude/memory/feedback_memory_architecture_failure_modes.md`
- Karpathy LLM Wiki adoption lock: `_CLAUDE.md` at vault root (2026-05-09)
- Autonomy cut lock: `agents/chief-of-staff/memory/idea_log.md` (2026-05-14 16:14)
