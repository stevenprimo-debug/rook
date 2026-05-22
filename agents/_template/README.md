# ROOK Master Skill Template v2

**Status:** v2.0.0 — operational
**Path:** `agents/_template/SKILL.md`
**License:** MIT (curated catalog — fork-only, no external contributions)

## What it is

The ROOK Master Skill Template is the proprietary 7-section scaffold every agent in the ROOK line inherits. It is what makes a roster of 20 domain specialists behave as one coherent system instead of 20 unrelated chatbots. The template solves three problems at once: consistency across the agent line (every agent loads context the same way, gates the same way, surfaces contradictions the same way), customer-extensibility (voice modes, bench composition, and routing keywords are slots the operator fills, not code the operator rewrites), and voice-spine inheritance (the anti-AI-slop voice contract propagates by reference, not by copy-paste).

The Master Skill Template v2 and the bundled `skill-creator` at `.claude/skills/core/skills/skill-creator/` are both proprietary ROOK IP. The template defines what a master skill IS in the ROOK system — the 7-section scaffold, the 3-pole principle bench, the voice-spine inheritance, the Step 1 context-load gate. The bundled `skill-creator` is the file generator that scaffolds new child skills against that contract — the XML-aware builder that writes SKILL.md frontmatter and the progressive-disclosure body. ROOK ships both. No upstream Anthropic dependency required: the template defines what the file means; the bundled skill-creator writes it.

## The 7 sections

| # | Section | What it carries |
|---|---|---|
| 1 | **Frontmatter contract** | YAML block with `name`, `description` (pushy enough to trigger reliably), `agent`, `category`, `version`, `voice` dominance, `default_mode`, `tools`, `skills` (universal stack + per-agent), `memory` tier, `trigger` keywords, `inherits` (voice spine + philosophy bench + bench file + frameworks index + frameworks attribution). |
| 2 | **3-pole principle bench** | Three orthogonal principles in productive tension, named by methodology (not by person). Each pole gates on a different question; the synthesis pole arbitrates. The named tension axis is required — if you can't name a real tension, the bench is decorative. |
| 3 | **Step 1 context-load gate** | Mandatory before any work. Loads agent identity (bench, frameworks, memory, child skills), queries the shared shelf via graphify, reads external-service docs from the Connectors or Reference shelf, cross-references the voice spine. Prevents the failure mode where the agent answers from training-data recall when the vault has the indexed content. |
| 4 | **Parameters** | `{mode}`, `{artifact}`, `{context}`, `{reversibility}`, `{user_state}`, `{depth}`, `{success_criterion}`. Presets per common scenario. The reversibility parameter wires directly into the gate that fires before any irreversible action. |
| 5 | **Routing keywords** | Per-agent primary + secondary + exclude arrays. The block auto-mirrors into `hooks/routing-rules.json` via `scripts/regenerate-routing-rules.py`, so the runtime routing-enforcer hook stays in sync with the agent's declared triggers. |
| 6 | **The prompt** | XML-structured prompt with `<role>` (three principles named, anti-patterns refused, forbidden vocabulary), `<parameters>`, `<knowledge_base>`, `<task>` (mode-specific procedures), `<subagent_strategy>`, `<reversibility_gate>`, `<domain_knowledge>`, `<output>` (mode-specific output structure). |
| 7 | **Worked examples** | Quick reference, delegation table, success criterion (universal: tab closes + user goes outside), cross-references. Concrete enough that a customer scaffolding a new agent has a working pattern to copy. |

## Why it's the moat

- **Consistency across the 20-agent roster.** Every agent loads context the same way, gates reversibility the same way, surfaces contradictions the same way, writes back to memory the same way. The operator's experience is one OS, not 20 disconnected agents.
- **Anti-AI-slop voice spine inheritance.** The voice contract at `.claude/voice-spine.md` propagates by reference. Forbidden vocabulary, complete-sentence rule, no-preamble rule, no-trailing-summary rule — all inherited, never re-written per agent.
- **Customer-extensible voice modes.** Each agent ships with `personality/voice_modes/_default.md` plus a folder the customer extends. Drop a `<your-mode>.md` in, set `{voice_mode}=<your-mode>` at invocation, and the agent loads that file as its voice spine for the session. No code changes.
- **Contradiction-surfacer memory pattern baked into Step 1.** The compounding-append-with-contradiction-surfacer pattern is the default memory shape for every agent. New learnings append, contradictions surface as questions for the operator to lock (never silent rewrites). History is the moat.
- **Routing-enforcer auto-mirror via `## Routing Keywords` block.** Edit the keywords in the SKILL.md, run `scripts/regenerate-routing-rules.py`, and `hooks/routing-rules.json` updates. No drift between the agent's declared triggers and the runtime hook that fires them.

## How to scaffold a new agent from it

```bash
# Copy the template into a new agent slot.
cp -r agents/_template agents/<agent-slug>

# Edit agents/<agent-slug>/SKILL.md:
#   1. Replace <AGENT NAME>, <agent-slug>, <category>, voice-dominance pick.
#   2. Write the 3-pole principle bench — name each pole by principle, not by person.
#      Confirm the tension axis is real (orthogonal poles, not three flavors of the same idea).
#   3. Fill the trigger keywords + routing-keywords block.
#   4. Write the <role> section of the prompt — name the principles, the anti-patterns,
#      the forbidden vocabulary specific to this domain.
#   5. Write the mode-specific procedures in <task>.
#   6. Define delegation routes (Routes TO / Receives FROM).

# Mirror the routing keywords into the routing-enforcer.
python scripts/regenerate-routing-rules.py

# Smoke test.
# @<agent-slug> <a representative trigger phrase>
```

Checklist before shipping a new agent:
- [ ] All `<PLACEHOLDER>` tokens replaced.
- [ ] 3 poles named by principle, not by person.
- [ ] Tension axis stated as a one-line orthogonal opposition.
- [ ] Routing keywords mirrored into `hooks/routing-rules.json`.
- [ ] Voice spine reference resolves (`.claude/voice-spine.md`).
- [ ] Bench file present at `agents/<agent-slug>/personality/_bench.md`.
- [ ] Frameworks index + attribution present (methodologies named, people credited separately).
- [ ] Memory folder present with `_template_memory.md` as the seed scaffold.
- [ ] Reversibility gate copy-pasted intact (do not customize the gate language).
- [ ] Success criterion preserved verbatim: "this agent succeeded when the user closes the tab and goes outside."

## Versioning

- **v2.0.0 (current)** — 3-pole principle bench, Step 1 context-load gate with graphify shared-shelf query, contradiction-surfacer memory pattern, auto-mirror routing-keywords block. This is the version every agent in the current line builds against.
- **v1 (pre-2026-04)** — single-bench scaffold without contradiction-surfacer. Archived at `_archive/2026-05/template_SKILL_v1_named_figures.md`. Named-figure pole composition (poles were named by person, not by principle) — superseded for voice cleanliness and customer-extensibility.
- **v1 → v2 migration note** — `_archive/2026-05/template_SKILL_v1_to_v2_migration.md`.

## Cross-references

- **Vault operating rules** — [`_CLAUDE.md`](../../_CLAUDE.md) at vault root. Compounding-append + contradiction-surfacer pattern, training-data-recall rule, reversibility gate definition.
- **Voice contract** — [`.claude/voice-spine.md`](../../.claude/voice-spine.md). Sections 3-4 mandatory; section 7 confirms voice-dominance mapping per agent.
- **Routing auto-mirror target** — [`hooks/routing-rules.json`](../../hooks/routing-rules.json). The runtime hook the `## Routing Keywords` block mirrors into.
- **Reference build (designer)** — `agents/designer/`. v1 gold-standard; migrates to v2 on next touch.
- **Reference build (engineering-lead)** — `agents/engineering-lead/`. v1, same migration path.
- **Top-level agents README** — `agents/README.md`.

## License

MIT (curated catalog — fork freely, no external contributions accepted).
