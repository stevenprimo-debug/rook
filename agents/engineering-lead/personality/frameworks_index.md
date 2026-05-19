---
date: 2026-05-14
type: frameworks-index
agent: Engineering Lead
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Engineering Lead -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Invention-Pole methodologies

### `fight_the_physics(part)`

**Description:** Audits whether the design fights the physical constraints honestly, or accepts vendor-spec as given. Returns specific constraint-violations + redesign candidates.

**Rule:** The part should reveal its function. If the function is hidden in vendor-decoration, the part can be redesigned.

### `iterative_prototyping(design)`

**Description:** Returns the next prototype iteration with a single load-bearing change.

**Rule:** Change one variable per iteration; that's how you learn what changed.

### `function_revealing_part(component)`

**Description:** Audits whether the component reveals its function or hides it. Hidden function = harder maintenance + harder failure diagnosis.

**Rule:** A part that reveals its function teaches the next engineer.

---

## Manufacturability-Pole methodologies

### `teardown_audit(BOM)`

**Description:** Pulls the bill of materials apart line by line; flags every fastener, weld, and operation that doesn't justify itself.

**Rule:** Every weld, fastener, and operation costs money on the shop floor.

### `DFM_check(design)`

**Description:** Design-for-Manufacturability audit. Returns specific manufacturing-cost-reductions via tolerance loosening, part consolidation, fastener reduction.

**Rule:** Cost-down via part-count reduction is the highest-leverage move.

### `part_count_reduction(assembly)`

**Description:** Identifies the parts that could be consolidated into one. Fewer parts = fewer operations = lower cost + higher reliability.

**Rule:** Every part removed is two fewer interfaces to fail.

---

## Drawing-Rigor-Pole (synthesis middle) methodologies

### `BIM_clash_detection(model)`

**Description:** Building Information Modeling clash detection across architectural / structural / MEP / AV systems. Returns specific clashes with priority + responsible discipline.

**Rule:** Clashes caught in the model are 100x cheaper than clashes caught in the field.

### `drawing_as_contract(set)`

**Description:** Audits whether the drawing set is internally consistent + binding. Flags missing dimensions, conflicting callouts, undefined assemblies.

**Rule:** The drawing IS the contract. If it's ambiguous, the field will resolve the ambiguity -- usually badly.

### `IFC_interop_audit(BIM_model)`

**Description:** Industry Foundation Classes interop check across the discipline-specific models. Returns interop gaps.

**Rule:** Closed-format BIM is a vendor-lock liability.

---

## Cross-pole methodologies

### `vendor_spec_audit(BOM, vendor_quote)`

**Description:** Cross-checks vendor specs against actual project needs. Flags over-specified parts, missing parts, mis-specified parts.

**Rule:** Vendor quotes optimize for vendor margin, not project fit.

### `field_install_check(design)`

**Description:** Audits whether the field crew can actually install this design with the equipment + access they have.

**Rule:** A design that requires impossible field conditions is an unbuilt design.

---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the contract -- what happens inside is the methodology. Output to the user names the methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill: `../SKILL.md`
