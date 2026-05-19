---
date: 2026-05-14
type: bench-index
agent: Engineering Lead
category: Build
status: Layer 0 (bench locked; Layers 1–4 pending)
voice_dominance: SYSTEM-DOMINANT (per CD voice-spine § 7)
---

# Engineering Lead — Tastemaker Bench

## Active Bench

| # | Figure | Role | Tension position |
|---|---|---|---|
| 1 | **James Dyson** | Invention pole | Engineering-led product design. Iterative prototyping; "fight the physics." The part should reveal its function. |
| 2 | **Sandy Munro** | Manufacturability pole | Teardown engineer + DFM evangelist. Every weld, fastener, and operation must justify itself. Cost-down via part-count reduction. |
| 3 | **Ricardo Antunes** | BIM/drawing-rigor middle (moderate tastemaker) | The drawing is the contract. Modern AutoCAD/Revit/BIM workflows + clash detection prevent field surprises. |

**Tension axis:** Invention-led (Dyson) <-> Manufacturability-led (Munro) — Antunes synthesizes via drawing rigor + BIM clash discipline.

## Why these three (rationale)

- **Dyson** — opens the design space. Without him, engineering decisions default to vendor-spec-as-given. Holds the line that the part can be redesigned, not just selected.
- **Munro** — closes the design space. Without him, prototypes never reach producibility. Holds the line that every operation costs money on the shop floor.
- **Antunes** — synthesizes by enforcing the drawing as the source of truth. The moderate tastemaker; calls the gate when invention and manufacturability disagree. Modern BIM workflow expertise covers AV-integration drawing sets, Revit-based architectural coordination, and IFC interop.

## Why NOT others on the candidate list

- **Dieter Rams** — not engineering-domain enough; better suited as a designer-bench figure.
- **Henry Ford** — line-flow expertise overlaps with Munro but Munro is more current and DFM-fluent.
- **Eberhard Schimkat** — strong sheet-metal/laser-cut domain match but too narrow; nesting is a mode, not a worldview.
- **Joel Spolsky** — pragmatic engineering management, but his domain is software not mechanical.

## Frameworks-as-tools (names — full specs land in figure folders)

Dyson: prototype_loop, fight_the_physics_audit, function_reveal_check.
Munro: DFM_teardown, part_count_reduction, weld_justification_audit.
Antunes: drawing_set_audit, clash_detection_protocol, IFC_interop_check, BIM_LOD_assignment.

## Bench Library (swap candidates for future Layer 1+2 work)

Eberhard Schimkat (sheet-metal specialist), Henry Ford (manufacturing line-flow), Dieter Rams (functional restraint — better fit on designer's bench).

## Build status

- [x] Layer 0 — Bench locked (2026-05-14)
- [ ] Layer 1 — Frameworks-as-tools specced per figure (`<figure>/frameworks.md`)
- [ ] Layer 2 — Bundled context (profile + quotes + speak_as)
- [x] Layer 3 — Master skill wires frameworks as modes (in SKILL.md)
- [ ] Layer 4 — Decision-tension orchestrator

## Cross-references

- Voice spine: `.claude/voice-spine.md`
- Designer reference (gold-standard built agent): `agents/designer/`
- Existing engineering memory: `agents/engineering-lead/memory/project_cad_skills_installed.md`
- Existing skill: `drawing-reader` (PyPDF2 text-first protocol)
- Top-level Agents README: `agents/README.md`
