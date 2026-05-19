# Engineering Lead — Reference Pack
## Mechanical, Structural, and CAD Engineering

**Domain:** Mechanical and CAD engineering, structural design, DFM (design for manufacturability), sheet-metal fabrication, BIM coordination, drawing-set rigor.

**Context:** Canonical reference library for the engineering-lead agent. Sources reflect commercial/industrial engineering practice — metal fabrication, structural steel, welding, GD&T, BIM/Revit coordination. Operator-specific sources belong in `agents/engineering-lead/context/` alongside this file.

---

## Source 1 — ASME Y14.5-2018 · Dimensioning and Tolerancing (GD&T)

**Publisher:** American Society of Mechanical Engineers (ASME)
**Standard Number:** ASME Y14.5-2018
**Format:** Purchasable PDF/print ($175 USD; free via institutional library access)

**What it covers:**
The definitive standard for geometric dimensioning and tolerancing (GD&T) in the United States. Defines symbolic language for communicating part geometry, form, orientation, location, and runout tolerances on engineering drawings. Governs how tolerances are interpreted on the shop floor, in inspection, and in vendor quotes.

**Why it belongs here:**
GD&T is the contract language between designers and fabricators. Misreading a tolerance callout — confusing ± bilateral with unilateral, or misapplying a flatness vs. parallelism control — causes scrapped parts and field RFIs. This standard is the reference the agent uses to validate tolerance callouts on any drawing set.

**Key sections for agent use:**
- Section 4: Symbology (flatness, straightness, circularity, cylindricity, profile, orientation, location, runout)
- Section 7: Form tolerances
- Section 8: Orientation tolerances — parallelism, perpendicularity, angularity
- Section 9: Location tolerances — true position, concentricity, symmetry
- Appendix B: Datum reference frame rules

---

## Source 2 — ASME Y14.100-2017 · Engineering Drawing Practices

**Publisher:** ASME
**Standard Number:** ASME Y14.100-2017
**Format:** Purchasable PDF

**What it covers:**
General rules for the preparation and revision of engineering drawings. Covers title block requirements, drawing views, scale notation, revision blocks, and drawing release procedures. The companion to Y14.5 — Y14.5 governs tolerancing; Y14.100 governs drawing format and interpretation.

**Why it belongs here:**
Title block reading is the first move on any incoming drawing set. Scale, revision, material, and finish callouts live in the title block. Missing or ambiguous title block data is a HARD STOP — the agent must surface it before extraction or quoting.

---

## Source 3 — AWS D1.1/D1.1M · Structural Welding Code — Steel

**Publisher:** American Welding Society (AWS)
**Standard Number:** AWS D1.1/D1.1M:2020
**Format:** Purchasable PDF (~$370 USD; free via institutional access)

**What it covers:**
The primary welding code for structural steel fabrication in the United States. Covers weld joint design, prequalified joint types, welder qualification, inspection requirements, and acceptance criteria. Referenced in virtually every structural steel shop drawing set.

**Why it belongs here:**
The manufacturability audit's weld-justification step requires knowing what welds are prequalified vs. engineered — a prequalified fillet weld at the right throat size needs no further justification; a non-prequalified joint needs an engineer-of-record stamp. The agent uses D1.1 to evaluate weld callouts on shop drawings before flagging DFM issues.

**Key sections for agent use:**
- Part A: General requirements (applicability, definitions)
- Part B: Design of welded connections (joint geometry, stress)
- Part C: Prequalification of WPS (prequalified joint types — the fast path)
- Part D: Qualification (when prequalification doesn't apply)
- Annex A: Weld symbols reference

---

## Source 4 — *BIM Handbook: A Guide to Building Information Modeling* (3rd Ed.)

**Authors:** Chuck Eastman, Paul Teicholz, Rafael Sacks, Lior Shohet
**Publisher:** Wiley, 2018
**ISBN:** 978-1119287537

**What it covers:**
Comprehensive reference on BIM workflows across architecture, structural engineering, MEP, and construction. Covers LOD (Level of Development) definitions, IFC interoperability, clash detection methodology, and BIM execution planning. Includes case studies on multi-discipline coordination and owner requirements.

**Why it belongs here:**
The revit-bim-coordinate mode uses LOD 100–500 as a framework for assigning model completeness and evaluating clash detection scope. This handbook is the source of the LOD definitions the agent applies.

---

## Source 5 — *Machinery's Handbook* (31st Ed.)

**Publisher:** Industrial Press
**ISBN:** 978-0831132996

**What it covers:**
The comprehensive mechanical engineering reference — 2,800+ pages covering materials, tolerances, fasteners, threads, gears, springs, machining processes, tooling, and shop mathematics. Standard reference on the shop floor and in mechanical design teams.

**Why it belongs here:**
When the manufacturability audit evaluates fastener selections, thread callouts, material grades, or machining operations, Machinery's Handbook is the authoritative source for specification ranges, material properties, and process trade-offs.

---

## Source 6 — ASTM Standards (A36, A572, A992, A500)

**Publisher:** ASTM International
**Format:** Individual standards purchasable ($50–75 each); institutional access available

**Key standards:**
- **ASTM A36** — Standard carbon structural steel (Fy=36 ksi). Most common plate and bar stock.
- **ASTM A572 Gr.50** — High-strength low-alloy (Fy=50 ksi). Common for structural shapes.
- **ASTM A992** — Wide-flange shapes for structural use (Fy=50 ksi, Fu=65 ksi). Standard for W-shapes.
- **ASTM A500 Gr.C** — Cold-formed hollow structural sections (HSS/tube steel).

**Why it belongs here:**
Vendor-spec-check mode requires verifying that quoted materials match the drawing callout. A36 vs. A572 substitution changes yield strength by 39% — a live-load violation on a structural member. The agent uses these ASTM grades as the baseline for material substitution flags.

---

## TODO — Operator context expansion

The following reference slots are reserved for operator-specific context. Populate `agents/engineering-lead/context/` with relevant sources for your domain:

1. **Industry vertical standards** — ASHRAE (MEP), NFPA 70 (electrical), OSHA 29 CFR 1910 Subpart O (machinery guarding), IEEE Std 100, or domain-specific codes
2. **CAM/CNC reference** — feeds/speeds, tooling, G-code dialect for your machine fleet
3. **Vendor qualification docs** — approved vendor list, material certifications, weld procedure specs (WPS) for your shop
4. **Project baseline data** — nesting utilization baselines, preferred material specs, standard hardware library
5. **Drawing convention notes** — firm-specific title block formats, abbreviation lists, standard detail library

Each reference added here becomes a cross-checked source in BOM extraction, vendor-spec-check, and manufacturability audit modes.
