---
name: Librarian — Frameworks Index (methodologies only)
description: Every callable methodology the librarian invokes. Indexed by METHODOLOGY name, never by person. The figures who originated each methodology are credited in `frameworks_attribution.md` — reference only, never invoked in output.
type: frameworks-index
agent: librarian
version: "2.0.0"
---

## For future Claude (TL;DR — pinned HEAD as of 2026-05-14)

**Rule:** Every framework below is callable by its METHODOLOGY NAME. The agent invokes the methodology, never the person who originated it. Attribution lives in the sister file; output does not name attributions.

**Status:** active.

**Apply when:** authoring any audit verdict that invokes a named framework. If the framework isn't in this index, scaffold it via `scaffold_skill` or add it here with a versioned-append entry.

---

## Vigilance-Pole frameworks (what's drifted?)

### `graph_diff_audit(scope)`

**Signature:** `graph_diff_audit(scope: str) -> DriftReport`
**Returns:** Drift list — orphan nodes, broken edges, contradiction subgraphs, low-read nodes, files past stale-after.
**When invoked:** Every `digest-write` and `drift-audit` run. The primary instrument.
**Failure mode caught:** Silent drift — files that became stale or contradicted without surfacing because no one was watching.
**Mechanism:** Graphify (`pip install graphifyy`) auto-updates the knowledge graph on vault changes; this function diffs graph state against vault state. Fallback: parallel file-by-file scan via Drift Detector sub-agents.

### `last_verified_gate(file)`

**Signature:** `last_verified_gate(file: Path) -> {pass: bool, days_stale: int}`
**Returns:** Pass/fail + days past the `stale_after_days` frontmatter gate.
**When invoked:** On every state-bearing file during the audit. Required for posture, status, brand, positioning, voice, doctrine, project status, and methodology files.
**Failure mode caught:** Silence read as "still true." A file unchanged for 42 days with no `last_verified` date and no stale-after trigger gets treated as authoritative.
**Mechanism:** Read frontmatter; compare `last_verified` to current date; flag if delta exceeds `stale_after_days`.

### `head_block_contract(file)`

**Signature:** `head_block_contract(file: Path) -> {has_head: bool, contradicts_body: bool}`
**Returns:** Whether the `## For future Claude (TL;DR)` HEAD block exists; whether HEAD contradicts body.
**When invoked:** On every state-bearing file. Required for feedback, posture, brand, positioning, voice, doctrine, project status, methodology. NOT required for append-only logs, capture-keyword mirrors, index files, starter-kit templates.
**Failure mode caught:** Cold agent reads top-to-bottom; first content read becomes load-bearing; historical/superseded content gets treated as current.
**Mechanism:** Parse for the HEAD block; if present, compare HEAD claim to most recent versioned-append entry in body.

### `routing_enforcer_false_positive_audit(prompt_log)`

**Signature:** `routing_enforcer_false_positive_audit(prompt_log: list) -> SemanticExcludeProposal[]`
**Returns:** Proposed semantic excludes for `routing-rules.json`.
**When invoked:** Monthly deep audit OR when a hook over-fires twice on the same kind of prompt.
**Failure mode caught:** Hook over-fires on weak keyword match; agents burn tokens reasoning around false positives.
**Mechanism:** Scan UserPromptSubmit log for fires that the agent decided were false positives; cluster by phrase pattern; propose excludes.

### `index_size_audit(index_files)`

**Signature:** `index_size_audit(index_files: list[Path]) -> SplitRecommendation[]`
**Returns:** Split-by-topic recommendations for any index passing 200 lines or 24KB.
**When invoked:** Every `digest-write`. Index health is a HIGH-severity finding when crossed.
**Failure mode caught:** Index outgrows load limit silently; cold sessions get partial, non-deterministic recall.
**Mechanism:** Read each index; check line count and byte size; if either exceeds threshold, propose a split by topic.

---

## Pruning-Pole frameworks (what can be archived?)

### `read_frequency_audit(scope, threshold_days)`

**Signature:** `read_frequency_audit(scope: str, threshold_days: int) -> ArchiveCandidate[]`
**Returns:** Files that have not been loaded in any session for `threshold_days`.
**When invoked:** Every `digest-write` and `archive-pass`.
**Failure mode caught:** Bloat — files that no agent reads continue to slow session-start scans and inflate the active vault.
**Mechanism:** Pull load history from agent session logs; filter for files with zero loads in the threshold window; intersect with vault manifest to exclude declared-load-bearing files.

### `duplicate_concept_detect(scope)`

**Signature:** `duplicate_concept_detect(scope: str) -> ConceptCluster[]`
**Returns:** Concept clusters with multiple files saying the same thing under different names.
**When invoked:** Monthly deep audit OR on user request.
**Failure mode caught:** Two files on the wedge, three on the canonical stack — agents read the wrong one and the lock drifts across copies.
**Mechanism:** Graphify entity-cluster query; surface clusters with 2+ files; propose a canonical pick + pointer-stub conversion for the duplicates.

### `completed_project_sprawl_audit(projects_dir)`

**Signature:** `completed_project_sprawl_audit(projects_dir: Path) -> ProjectArchiveProposal[]`
**Returns:** Projects past SHIPPED status with cooldown elapsed; working files → archive; methodology files → promote to active vault.
**When invoked:** Monthly deep audit.
**Failure mode caught:** Shipped projects accumulate working files indefinitely; future projects can't surface the reusable methodology buried in them.
**Mechanism:** Scan projects directory for SHIPPED status; check cooldown; classify each file as working-file (archive) or methodology (promote).

### `index_split_recommendation(file)`

**Signature:** `index_split_recommendation(file: Path) -> SplitPlan`
**Returns:** Split plan — by topic, with target file names and migration mapping.
**When invoked:** Whenever `index_size_audit` flags an index.
**Failure mode caught:** An index trimmed instead of split loses information.
**Mechanism:** Topic-cluster the index entries; propose 2-3 target files; both halves remain in active path; small master index links to all.

---

## Continuity-Pole frameworks (what compounds?)

### `archive_vs_delete_contract(file)`

**Signature:** `archive_vs_delete_contract(file: Path) -> {action: "archive" | "supersede" | "refuse"}`
**Returns:** Archive action (move + tombstone), supersede action (replace + retain history), or refuse (file is currently load-bearing).
**When invoked:** Every prune action. The gate.
**Failure mode caught:** Deletion breaks the compounding loop. Even killed ideas stay in `idea_log.md` forever — that's how re-litigation gets blocked at intake.
**Mechanism:** Confirm not load-bearing; confirm reversibility; choose archive vs. supersede based on whether a replacement file exists.

### `contradiction_surface(file_a, file_b)`

**Signature:** `contradiction_surface(file_a: Path, file_b: Path) -> ResolutionProposal`
**Returns:** A drafted resolution — which file's HEAD wins, which becomes historical body, what versioned-append entry captures the change.
**When invoked:** On every contradiction subgraph found.
**Failure mode caught:** Silent rewrite — resolving a contradiction by quietly changing one file to match the other erases the audit trail of the decision.
**Mechanism:** Read both HEADs; diagnose the load-bearer (most recent, most-cited, most-load-bearing); draft the resolution; surface in digest as awaiting-nod.

### `vault_manifest_write(state)`

**Signature:** `vault_manifest_write(state: VaultState) -> Path`
**Returns:** Path to the written `memory/vault_manifest.md`.
**When invoked:** Every `digest-write` and `manifest-update`.
**Failure mode caught:** Other agents have no current-state stub to inherit at session start; each runs its own audit and burns tokens.
**Mechanism:** HEAD-rewrite (state file pattern): pull current vault size, last-verified by domain, drift count, broken-link count, contradiction count, index health; write the stub.

### `head_rewrite_with_versioned_append(file, new_head, history_append)`

**Signature:** `head_rewrite_with_versioned_append(file: Path, new_head: str, history_append: str) -> Diff`
**Returns:** Diff with the new HEAD block and the versioned-append entry to the body.
**When invoked:** Every contradiction resolution; every state file update where the HEAD must change.
**Failure mode caught:** Silent overwrite — methodology drifts without an audit trail.
**Mechanism:** Replace the HEAD block; append a dated entry to the body capturing what changed and why; preserve the original body content below the new append.

### `compound_append(file, entry)`

**Signature:** `compound_append(file: Path, entry: VersionedEntry) -> Path`
**Returns:** Path to the updated file.
**When invoked:** Every state/posture/feedback/project file update.
**Failure mode caught:** Losing the audit trail. Future-you needs to see what changed and when.
**Mechanism:** Append a dated, versioned entry; never overwrite existing entries.

---

## Synthesis frameworks (cross-pole, routing)

### `hook_tier_classifier(finding)`

**Signature:** `hook_tier_classifier(finding: Finding) -> {tier: "passive" | "mutating" | "blocking", justification: str}`
**Returns:** Tier classification per the 3-tier autonomy cut (v3 locked 16:14).
**When invoked:** On every hook authoring action.
**Failure mode caught:** A blocking hook wired live without the operator approval; a passive hook over-engineered into a soft gate that requires attention.
**Mechanism:**
- Passive → warnings, surface-on-load, audit-on-schedule, staleness reminders. Low blast radius. Autonomous.
- Mutating → auto-rewrite memory, auto-archive, auto-resolve contradiction. Medium blast radius. Draft + run on next session unless the operator rejects in digest (soft gate).
- Blocking → prevents tool calls, refuses dispatches, requires preconditions. High blast radius. Draft only; surface in digest for explicit approval (hard gate).

### `librarian_digest_assemble(findings, hooks_created, hooks_proposed)`

**Signature:** `librarian_digest_assemble(...) -> DigestPath`
**Returns:** Path to the written `memory/librarian_digest.md`.
**When invoked:** Every `digest-write` mode run.
**Failure mode caught:** Findings scattered across chat windows instead of consolidated in a scannable weekly report.
**Mechanism:** HEAD = current week. Three sections: Findings (HIGH / MEDIUM / LOW severity), Hooks-created (passive, live, no action needed), Hooks-proposed (mutating + blocking, awaiting the operator Y/N). Compound-append: prior weeks live below the divider with month-folded summaries.

### `severity_classifier(finding)`

**Signature:** `severity_classifier(finding: Finding) -> "HIGH" | "MEDIUM" | "LOW"`
**Returns:** Severity tier.
**When invoked:** On every finding before digest assembly.
**Mechanism:**
- HIGH = downstream miss already happened OR imminent (load-bearing file past stale-after; contradiction subgraph two agents both read; index past load limit).
- MEDIUM = drift not yet causing damage but compounding (file past stale-after but not load-bearing; orphan node; broken edge with replacement candidate).
- LOW = noise floor (low-read node, archive candidate not yet past threshold).

### `monday_anchor_anti_pattern_check(trigger)`

**Signature:** `monday_anchor_anti_pattern_check(trigger: str) -> {valid: bool, reason: str}`
**Returns:** Pass/fail. Refuses "weekly anchor session" as a default trigger.
**When invoked:** Every time the librarian proposes a trigger for an audit recommendation.
**Failure mode caught:** Default-to-weekly-anchor-session is the someday-punt failure mode (per `feedback_dont_default_park_to_monday.md`). weekly anchor session is the digest-scan cadence, NOT a trigger.
**Mechanism:** Reject if trigger is "weekly anchor session" or any variant. Require date / event / signal / dependency.

---

## Frameworks-as-tools usage pattern

The librarian does not "explain" these frameworks in output. It invokes them silently and surfaces the result.

Bad: *"Running the `graph_diff_audit` function on the full vault scope, we find that..."*
Good: *"11 drift findings across the vault. 3 HIGH severity. Digest written."*

The framework name appears in the audit log, the digest body, and the registry — never in user-facing prose. The principle is the same as voice-spine § 3.7: *the work loses its concept the moment you point at it.*

---

## Adding a new framework

When a new pattern emerges and warrants a callable name:

1. Add an entry to this file with full spec (signature, returns, when invoked, failure mode caught, mechanism).
2. Versioned-append the change at the bottom (date + one-sentence summary).
3. If the framework has objective verifiable output, scaffold a child skill via `scaffold_skill` mode.
4. If the framework involves a hook, register it in `memory/hooks_registry.md` with its autonomy tier.

---

## Versioned append (history)

- **2026-05-14** — Initial v2.0 lock. 15 frameworks across Vigilance/Pruning/Continuity/synthesis. Source: librarian build pass per v3 generator spec.

---

## Cross-references

- Frameworks attribution (academic credit, reference only): `frameworks_attribution.md`
- Bench (which pole each framework gates for): `_bench.md`
- SKILL.md (the master agent skill): `../SKILL.md`
- Voice spine (the "work loses its concept" rule): `.claude/voice-spine.md` § 3.7
- Memory failure modes: `.claude/memory/feedback_memory_architecture_failure_modes.md`
- File-type pattern: `.claude/memory/feedback_memory_pattern_per_file_type.md`
- Autonomy cut lock: `agents/chief-of-staff/memory/idea_log.md` (2026-05-14 16:14)
