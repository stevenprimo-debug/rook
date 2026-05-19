---
name: SOP Template Generator
description: |
  Generate a Standard Operating Procedure (SOP) — internal-process
  documentation, NOT external-facing legal contracts. Dual-axis variant
  pattern: tone/style axis (rd-experiment / qa-process /
  business-operational / safety-procedure) × use-case axis
  (customer-onboarding / employee-onboarding / incident-response /
  weekly-rhythm / launch-checklist / handoff-procedure). Codifies
  recurring patterns so they survive turnover and scale beyond one operator's
  head. Never uses preamble.
type: skill
category: operations
version: "1.0.0"
status: operational
voice: SYSTEM-DOMINANT
tools:
  - Read
  - Write
  - Edit
  - Glob
trigger: >
  Fire when the user says: write an SOP, document this process, standard
  operating procedure, runbook, playbook, codify this workflow, onboarding
  checklist, incident response, handoff procedure, weekly rhythm, document
  the process so anyone can run it.
inherits:
  - skeleton: skeleton.md
  - variants: variants/
---

# SOP Template Generator

## Overview

SOP = Standard Operating Procedure = internal process documentation. Different
category from contracts (sow / msa / nda) — SOPs are operational, not legal.
Used to codify recurring workflows so they survive turnover, scale beyond one
operator's head, and serve as training material.

Dual-axis variants:

| Axis | Options | Effect |
|---|---|---|
| **Tone/Style** | rd-experiment / qa-process / business-operational / safety-procedure | Sets the procedural rigor + section depth |
| **Use-case** | customer-onboarding / employee-onboarding / incident-response / weekly-rhythm / launch-checklist / handoff-procedure | Sets the process domain + step structure |

Customer picks one from each axis → skeleton + tone + use-case = filled SOP.

## How to use

1. Customer says "write an SOP for {process}" or describes a recurring workflow
2. Skill asks for tone/style axis (rd-experiment / qa-process / business-operational / safety-procedure)
3. Skill asks for use-case axis (customer-onboarding / employee-onboarding / etc.)
4. Skill loads skeleton + matching variant content
5. Skill asks for process-specific slots (purpose, scope, roles, step sequence, success definition)
6. Skill writes filled SOP to `_FROM_CLAUDE/YYYY-MM-DD-{process}-sop.md`
7. Skill offers html2pdf conversion + Obsidian Vault sync via obsidian-cli

## Core sections (universal across variants)

1. Header (SOP title, document number, version, effective date, process owner)
2. Purpose (1 paragraph — WHY this SOP exists)
3. Scope (WHO this SOP applies to + WHEN it fires)
4. Responsibilities (named roles + their accountabilities — Process Leader / Operator / Manager / Reviewer)
5. Materials & Preparation (what's needed before starting)
6. Procedure (the step-by-step — numbered, atomic, verifiable)
7. Decision Points (where the operator chooses; flow chart references)
8. Training & Clearance (who can run this SOP + what training is required)
9. Limitations & Edge Cases (what this SOP does NOT cover)
10. Maintenance & Disposal (closing-out steps + records to file)
11. References (related SOPs, manuals, source docs)
12. Attachments (flow charts, checklists, forms)

## Variants ship with

**Tone/Style axis:**
- `variants/rd-experiment.md` — hypothesis-driven, controls, deviation handling
- `variants/qa-process.md` — input acceptance criteria, atomic verification, sign-off
- `variants/business-operational.md` — purpose-scope-roles-procedure cadence
- `variants/safety-procedure.md` — risk-assessed (PPE SOP pattern)

**Use-case axis:**
- `use-cases/customer-onboarding.md`
- `use-cases/employee-onboarding.md`
- `use-cases/incident-response.md`
- `use-cases/weekly-rhythm.md`
- `use-cases/launch-checklist.md`
- `use-cases/handoff-procedure.md`

Customer adds their own via `variants/_template.md` + `use-cases/_template.md`.

## Convention: black text vs red text

Per the PPE SOP reference (Jay Vee, 2026-05-14 clip): **black text** = generic
boilerplate that may apply across facilities; **red text** = facility-specific
content that MUST be reviewed and replaced. SOPs ship with this convention so
the customer knows what to keep and what to localize.

## Anti-patterns (refuse list)

- **Preamble.** SOP body starts with Purpose. No introduction paragraph.
- **Vague step instructions.** Every step is atomic + verifiable. "Check the
  system" is too vague; "Verify the dashboard shows status=green for the last
  15 minutes" is right.
- **Missing decision points.** If the procedure branches, the branch logic is
  explicit (with flow chart or numbered conditionals).
- **No success definition.** Section 6 ends with explicit acceptance criteria
  for the SOP completing successfully.
- **Forbidden vocabulary** per CD voice-spine § 4.

## Success criterion (universal)

This skill succeeded when a new operator can execute the SOP independently
without asking the original author a single question. The cleanest SOP is
the one that lets the author go on vacation.

## Cross-references

- Sister skill (cross-category): `nda-template`, `sow-template`, `msa-template`, `proposal-template`
- Reference clipping: `Clippings/PPE Standard Operating Procedure  PDF  Personal Protective Equipment.md` (safety-procedure variant seed)
- Reference clipping: `Clippings/SOP Word Template  PDF  Clinical Research.md` (rd-experiment / clinical-research variant seed)
- Reference clippings (pending): R&D SOP, SOP Overview QA, SOP Development Guidelines, Writing Effective SOPs
