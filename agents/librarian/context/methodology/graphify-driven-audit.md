# Graphify-Driven Audit

## What This Framework Is

Graphify-driven audit is the practice of converting an unstructured
corpus (memory files, project documents, vendored references, codebase
artifacts) into a knowledge graph, then using the graph to surface
findings that flat-file reading misses: orphan nodes (memory entries
nothing references), broken wikilinks, duplicate or near-duplicate
entries, stale references to deprecated systems, and gaps where the
graph expects coverage that doesn't exist.

The framework operates on the assumption that **vault structure is a
graph, not a list** — every memory file, every reference clipping,
every dept's CLAUDE.md is a node, and every wikilink, file reference,
and conceptual relationship is an edge. Flat file reading misses
edge-quality problems; graph traversal surfaces them.

The audit produces three categories of findings:

1. **Structural** — orphan nodes, broken edges, missing index
   entries, duplicate-or-near-duplicate content, files that grew
   past size cap.

2. **Drift** — last-verified timestamps that are stale, HEAD
   pointers that haven't been updated, references to deprecated
   tooling or processes.

3. **Coverage** — domains the graph expects (per the org chart)
   that have no memory accumulation; agents that should reference
   each other but don't; concepts named in one file that lack
   definition anywhere in the graph.

The audit is a recurring discipline, not a one-shot. Each audit
produces a remediation list; remediation appended to memory per
the compounding-append pattern; the next audit verifies
remediation landed and finds new findings.

## Why It Matters For This Agent

Librarian's Pruning-Pole asks: "Is the vault accumulating signal
or accumulating noise?" Graphify-driven audit is the diagnostic
that answers the question with structured evidence rather than
intuition.

The pole catches three specific failure modes:

1. **Orphan accumulation** — memory entries written once, never
   referenced again, but never pruned. The graph identifies them
   as zero-edge nodes.

2. **Reference rot** — wikilinks and file references that point at
   moved, renamed, or deleted targets. The graph identifies broken
   edges.

3. **Coverage gaps** — domains that should have memory (per the
   org chart) but don't. The graph identifies expected nodes that
   are missing.

For the operator's vault (hundreds of memory files across departments,
agents, and projects), manual audit is intractable. Graphify
converts the audit into a structured operation: ingest the corpus,
traverse the graph, generate findings, propose remediations.

## Core Concepts

### 1. The Vault-as-Graph Model

Every artifact in the vault is a node:
- Memory files (with timestamp metadata, content body, links to
  other nodes).
- Department CLAUDE.md files (with routing rules, scope, member
  references).
- Agent SKILL.md files (with bench, frameworks, voice modes,
  cross-agent routing).
- Reference clippings (with source URL, vendoring date,
  domain tags).
- Project files (with status, dependencies, owner).

Every relationship is an edge:
- Wikilinks (`[[NMA_PROJECT_FACTS]]`) — explicit references.
- File references (relative path links) — explicit references.
- Concept references (a name in one file that's defined in another)
  — implicit, requires concept-resolution.
- Routing edges (dept A delegates to dept B per CLAUDE.md routing
  table) — structural.

The graph is the source-of-truth view; the file system is the
storage view. The audit operates on the graph.

### 2. Orphan Detection

Orphan nodes are memory entries (or reference clippings) with
zero or near-zero incoming edges. They were written, but nothing
references them.

Orphans are not automatically bad. Some categories of memory
(personal-reflection notes, one-time decision logs) legitimately
have no incoming references. But persistent orphans across multiple
audits are signal: the entry didn't compound, suggesting it was
either premature, off-topic, or duplicates content elsewhere.

The audit produces an orphan list with remediation options:
- **Link** — find natural references in other files and add
  edges.
- **Promote** — move the orphan into a more discoverable location
  (e.g., into the index).
- **Archive** — move to archive folder if the entry served its
  one-time purpose.
- **Merge** — if the orphan duplicates content elsewhere,
  consolidate.

### 3. Broken-Edge Detection

Broken edges are wikilinks or file references that point at
targets that don't exist (file deleted, renamed, moved). The
graph traversal flags every broken edge.

Remediation options:
- **Repoint** — the target was renamed; update the reference.
- **Restore** — the target was deleted but is still relevant;
  restore from archive or rewrite.
- **Remove** — the target is permanently gone; remove the
  reference and append a note explaining the removal.

### 4. Duplicate/Near-Duplicate Detection

Two memory entries cover the same content with slightly different
wording. The graph traversal identifies high-similarity nodes
(via content embedding or shingle hashing).

Duplicates are usually accidental: two sessions captured the same
lesson without checking for prior entries. Remediation:
consolidate into one canonical entry, archive the duplicates with
references back to the canonical entry.

### 5. Stale Timestamp Detection

Per the compounding-append pattern, each memory entry carries a
last-verified timestamp. The audit identifies entries with
timestamps older than a configurable threshold (e.g., 90 days for
operational rules, 180 days for project facts).

Stale-timestamp entries get surfaced for re-verification:
- Re-read the entry; is it still accurate?
- If yes, refresh the timestamp.
- If no, append a new entry with current state; mark the old
  entry superseded.

### 6. Coverage-Gap Detection

The org chart specifies which departments and agents exist. The
audit checks that each has the expected memory structure:
- `CLAUDE.md` (scope and routing).
- `memory/` folder with at least an index file.
- `personality/` folder (for agents) with bench, voice modes,
  frameworks index.
- `context/` folder (for agents) with references and methodology.

Missing artifacts get flagged as coverage gaps. Remediation:
populate the missing artifact, or document why the absence is
intentional (e.g., new department, awaiting initial work).

### 7. The Audit Cycle

The recurring audit cycle:

1. **Ingest** — graphify the current vault state into the graph.
2. **Traverse** — run structural, drift, and coverage queries.
3. **Generate findings** — orphans, broken edges, duplicates,
   stale timestamps, coverage gaps.
4. **Propose remediations** — for each finding, propose specific
   action.
5. **Operator review** — the operator reviews findings and approves
   remediations.
6. **Apply** — agent applies approved remediations, appending
   changes to memory.
7. **Re-audit** — next cycle confirms remediation landed.

Cycle cadence: quarterly for full audit, monthly for stale-timestamp
and broken-edge scans, ad-hoc when significant structural changes
occur.

## Common Applications

**Quarterly full vault audit:**
The agent runs `/graphify` against the full vault, generates the
graph, runs all audit queries. Output: structured findings list
with severity tiers. the operator reviews; approves bulk remediations
(repoint broken links, consolidate clear duplicates) and reviews
individual findings (which orphans to archive vs. promote).

**Memory wall diagnostic:**
A specific session hit a memory wall (agent couldn't find a
relevant memory entry that should exist). Librarian runs a
targeted audit: did the relevant entry exist? Was it indexed?
Was the routing logic finding it? Output: specific diagnostic with
remediation (e.g., the entry existed but wasn't in the index;
add to index).

**Post-restructure audit:**
After a vault restructure (e.g., the 2026-04-24 v2 dept
restructure), Librarian runs a comprehensive audit to catch
broken edges produced by the restructure. Output: all references
that pointed at moved files. Bulk repoint applied.

**Dept-scoped audit:**
A single department's memory folder is audited for orphans, stale
timestamps, missing references. Output: dept-specific
remediations. Useful when a dept's memory has grown organically
and needs cleanup before promotion of any entries to root.

**Cross-agent memory share audit:**
Audit identifies memory entries that are referenced by multiple
agents — these are candidates for promotion to higher-level
memory (root or dept root). Entries referenced by zero or one
agent stay scoped where they live.

**Concept-coverage audit:**
A new concept (e.g., "agentic commerce") starts appearing in
multiple files without a canonical definition node. Audit flags
the gap; remediation: create a canonical definition entry that
the other entries reference.

## Anti-patterns (when this framework is misapplied)

**Audit-without-remediation.** Running audits, generating findings,
and never applying remediations. The audit produces no value
unless the findings get acted on.

**Bulk-archive without review.** Treating orphan detection as
permission to delete entries. Orphans get reviewed; remediation
options include archive, but also link, promote, and merge.
Bulk-delete loses signal.

**Per locked feedback: "Compounding-Append + Contradiction-Surfacer."**
Audit remediations follow the same pattern: append to memory,
surface contradictions, never silent overwrite.

**Per locked feedback: "Memory Architecture Failure Modes."**
The audit operationalizes the diagnostic checklist for the four
named failure modes: HEAD blocks, last-verified timestamps,
index-load-limits, routing false-positives.

**Treating the graph as authoritative.** The graph is a view of
the vault state at audit time. The file system is the storage;
the operator-locked decisions are the source of truth. If the
graph disagrees with the operator, the graph is wrong (or the
audit found a real issue worth surfacing).

**Per locked feedback: "Grep Existing Skills BEFORE Writing About
Them."** The audit operationalizes this: before recommending the
creation of a new skill or memory file, the graph check confirms
the artifact doesn't already exist under a different name.

**Audit-by-intuition.** Skipping graphify and "spot-checking" the
vault by reading files. Manual audit misses edge-quality problems
that graph traversal catches. The framework requires graph
traversal as the audit substrate.

**Per locked feedback: "Self-Improvement Loop."** Audit findings
that surface recurring mistakes become memory entries themselves:
the audit produces lessons, and those lessons compound into
future audits.

## Cross-references

- Agent skill: `agents/librarian/SKILL.md`
- Bench: `agents/librarian/personality/_bench.md` (Pruning-Pole, Contradiction-Surface-Pole)
- Frameworks index: `agents/librarian/personality/frameworks_index.md`
- Companion methodology: `agents/librarian/context/methodology/compounding-append-pattern.md`
- Vendored reference: `agents/librarian/context/references/anthropic-ama-architecture.md`
- Skill: `~/.claude/skills/graphify/SKILL.md`
- Memory: `.claude/memory/MEMORY.md`
- Memory: `.claude/memory/feedback_memory_architecture_failure_modes.md`
- Memory: `.claude/memory/feedback_grep_existing_skills_before_writing_about_them.md`
- Memory: `.claude/memory/feedback_filter_personal_vs_agent_team_patterns.md`
