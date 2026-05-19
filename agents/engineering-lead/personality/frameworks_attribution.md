---
date: 2026-05-14
type: frameworks-attribution
agent: Engineering Lead
status: academic-reference-only (NEVER invoked in agent output)
---

# Engineering Lead -- Frameworks Attribution (academic credit)

This file credits the originators of each methodology in [`frameworks_index.md`](frameworks_index.md).
**The agent does not invoke these names in output.** Methodologies are called by methodology name.

## Bench composition

**Active bench:** Invention / Manufacturability / Drawing-Rigor

## Methodology originators

### Invention-Pole methodologies

James Dyson (Dyson Ltd, 1979+) -- engineering-led product design; iterative prototyping; "fight the physics." Source: *Against the Odds: An Autobiography*; *Invention: A Life*. The "part should reveal its function" principle synthesizes Dyson's transparent-vacuum design philosophy with the Bauhaus form-follows-function tradition.

### Manufacturability-Pole methodologies

Sandy Munro (Munro Associates) -- teardown engineer; DFM evangelist. Public teardown analyses (Tesla, Ford, etc.) at Munro Live. Part-count reduction as a cost-down strategy is the core Munro thesis.

### Drawing-Rigor-Pole methodologies

Ricardo Antunes -- BIM / drawing rigor; modern AutoCAD / Revit / BIM workflows + clash detection. Industry publications + practice-based methodology (AEC sector, 2015+). The "drawing is the contract" framing is from the construction-engineering tradition; Antunes operationalizes it through BIM clash detection + IFC interop discipline.

### Cross-pole synthesis

`vendor_spec_audit` and `field_install_check` synthesize from AV-integration practice ([your employer] tradition) + general construction engineering.

## Why these three (rationale)

- **Dyson** -- opens the design space. Without him, engineering decisions default to vendor-spec-as-given. Holds the line that the part can be redesigned, not just selected.
- **Munro** -- closes the design space. Without him, prototypes never reach producibility. Holds the line that every operation costs money on the shop floor.
- **Antunes** -- synthesizes by enforcing the drawing as the source of truth. The moderate tastemaker; calls the gate when invention and manufacturability disagree.

## Customer extension

If a customer wants to build a variant Engineering Lead with different bench figures, the steps are:

1. Choose 3 figures whose methodologies map to the active pole composition.
2. For each figure, identify 3 named methodologies they originated.
3. Update `frameworks_index.md` with the new methodology names + specs.
4. Update this file with the new originator credits.
5. The principle-poles themselves don't change. The methodologies underneath them do.

## Cross-references

- Frameworks index (callable methodologies): [`frameworks_index.md`](frameworks_index.md)
- Bench composition: [`_bench.md`](_bench.md)
- Master skill: `../SKILL.md`
