# Mechanical Engineering — Progression Path

## Who This Is For

The operator who scopes mechanical / structural / fabrication work — reads drawing sets, validates vendor BOMs, runs DFM audits, manages clash detection, writes specs that the field will not deviate silently from. Mechanical engineers, fabrication shop owners, design-build operators, and anyone whose business gates revenue on producing drawings that survive contact with a contractor.

By the end of this path you should be able to:
- Read a CAD set in minutes.
- Extract a BOM via text-first PyPDF2 (never visual).
- Challenge a vendor quote line by line.
- Write a drawing rigorous enough that the install team has nothing to "interpret."
- Run a multi-discipline clash detection cycle.
- Issue a spec that survives contract review and field execution.

## Stage 1: Foundations (weeks 1-4)

**Goal:** Read 2D drawings fluently. Understand standards (ANSI / ISO / GD&T). Run your first BOM extraction with text-first discipline.

**Read / Watch:**
- *Engineering Drawing and Design* — David Madsen. The textbook; the standards reference. Read chapters 1-8 first; the rest is reference.
- *Machinery's Handbook* — Erik Oberg et al. The mechanical-engineering reference; not for cover-to-cover reading, but the sections on tolerances, fits, and fastener specifications are mandatory.
- *Geometric Dimensioning and Tolerancing for Mechanical Design* — Gene Cogorno. The GD&T primer; the symbols are the language of drawing-rigor.
- **ASME Y14.5** — the GD&T standard itself. Buy it; read it slowly; reference it forever.
- *Drafting for Architects, Designers and Engineers* — Cecil Jensen. The cross-discipline drawing-reading primer.
- **Industry-specific systems engineering training** — for AV-specific systems engineering. The CTS / CTS-D / CTS-I certification paths; the courseware is the AV industry's only common curriculum.
- *Audio System Design and Installation* — Philip Giddings. AV-specific; dated in places but the system-design discipline holds.

**Practice:**
- Pull a real CAD drawing set from a past job (or download a free sample set from a manufacturer like a manufacturer's published documentation (most major equipment vendors publish sample drawing sets)). Read every sheet. Note: title block, revision history, datum references, GD&T callouts, BOM table, section views, detail views.
- Extract a BOM from a vendor quote PDF using PyPDF2 text-first (`python -c "import PyPDF2; ..."`). Never visual reading; never copy-paste. The discipline is named in the engineering-lead agent's SKILL.md for a reason — visual reading gets model numbers and manufacturer names wrong.
- Identify every fastener in one assembly drawing. Look up the spec for each in *Machinery's Handbook*. The exercise teaches that "M6 bolt" is not a spec — head type, thread pitch, length, grade, finish are.
- Learn the difference between detail view and section view. Sketch both for one assembly. The kinesthetic memory makes drawing-reading faster forever.

**Skill check:**
- Hand a peer a drawing sheet from one of your jobs. They can ask any clarifying question and you can answer it from the sheet alone — datum references, tolerance zones, BOM line items, revision changes since last issue.
- You can read a title block and infer the drawing's revision history and approval chain.
- You can identify GD&T symbols on a sheet and explain what each one constrains.

## Stage 2: Applied Practice (weeks 5-12)

**Goal:** Run DFM audits. Validate vendor quotes line-by-line. Produce drawings that survive field execution.

**Read / Watch:**
- *Design for Manufacturability* — David Anderson. The DFM bible; the rules-of-thumb chapters carry across industries.
- *Manufacturing Processes for Engineering Materials* — Serope Kalpakjian and Steven Schmid. The textbook; the chapters on sheet-metal forming, welding, machining are the ones to know.
- *Sheet Metal Handbook* — Ron and Sue Fournier. Hands-on shop reference; pair with Anderson's DFM for the rules-and-shop combination.
- *Welding: Principles and Applications* — Larry Jeffus. AWS-aligned; the welding chapters that any design has to respect.
- **eMachineShop's DFM guidelines** (emachineshop.com) — free; ruthlessly practical; the gold standard for "what manufacturers actually need."
- **Protolabs design guidelines** (protolabs.com) — free; quick-turn-CNC and injection-molding DFM rules.
- **Xometry instant-quote configurator** — observe how a real manufacturer interprets a drawing; useful pressure-test on your own files.
- **The industry design reference manual** — for AV-specific DFM equivalents (rack airflow, cable management, sightline math).
- *BIM Handbook* — Eastman, Teicholz, Sacks, Liston. Building Information Modeling for cross-discipline coordination; the clash-detection chapters are the keepers.

**Practice:**
- Run a DFM audit on a sheet-metal part: bend radii, hole-to-edge distances, fastener clearance, material thickness, finish-callouts. Document every flag. Send the audit to a real shop for pricing. Compare your audit's flags to the shop's flags.
- Validate a vendor quote line by line: every line item, model number verified against manufacturer datasheet, quantity logic-checked against the BOM, price benchmarked against at least one competitive source. Flag every discrepancy.
- Nest one sheet-metal job for material efficiency. Run the same drawing through two nesting passes — one optimized for material yield, one optimized for setup time. Compare cost. The exercise teaches that "efficiency" is plural.
- Run a BIM clash-detection cycle on one project (Navisworks, BIM 360, or free Revit / IFC viewers). Surface clashes; route to the responsible trade; track to resolution.

**Skill check:**
- Your DFM audit caught flags the manufacturer also caught.
- Your vendor-quote validation surfaced at least one discrepancy that saved real money.
- Your drawings shipped to the field and the field did not call back with "what does this mean?"
- Your BIM clash-detection cycle resolved at least three clashes before they hit the field.

## Stage 3: Advanced Mastery (months 3-9)

**Goal:** Lead multi-discipline coordination. Develop spec-writing rigor. Run a fabrication-shop-floor cycle.

**Read / Watch:**
- *Mechanical Engineering Design* — Shigley. The mechanical-engineering textbook; the standard of rigor for design calculations.
- *Roark's Formulas for Stress and Strain* — Warren Young. The reference for everything load-bearing.
- *Marks' Standard Handbook for Mechanical Engineers* — the desk reference that lives within arm's reach.
- *Specification Writing for Architects and Engineers* — Donald Watson. The CSI MasterFormat / SectionFormat discipline that makes specs survive litigation.
- **industry rack-build standard** (rack-build standard) and the broader industry technical-standards library — for AV-specific spec rigor.
- *The Project Manager's Guide to Mastering Agile and Lean Construction* — for the coordination side of design-build delivery.
- *Built to Last* — Cary Lewandowski (industry-specific) or industry-equivalent texts on long-arc fabrication shop operations.
- **Fabrication trade journals**: *Fabricator* magazine (FMA International), *Welding Journal* (AWS), *Modern Machine Shop*. Subscribe to one; read the case-study features.
- **The Engineering Drawing course on MIT OpenCourseWare** — free; technical drawing depth.
- **Autodesk University recorded sessions** — free; Revit, Inventor, Navisworks workflow depth.

**Practice:**
- Write a complete specification (Division 27 for low-voltage / AV, or the discipline equivalent) for one project. Use CSI MasterFormat structure. Pressure-test against an A/E peer; revise.
- Lead a multi-discipline coordination cycle: MEP + structural + AV + IT. Run the clash-detection. Run the punch-list. Document the lessons-learned.
- Run a fabrication-shop floor cycle: hand a drawing package to a shop, watch them quote, watch them cut, watch them weld, watch them ship. The field-side learning is more concentrated than any classroom.
- Develop a personal drawing-review checklist: 30+ items you check on every sheet before issuing. The checklist is your QA gate. Refine it after every job by adding the things you missed.

**Skill check:**
- A project you scoped delivered without an RFI on the BOM or the drawings.
- Your spec survived without scope creep.
- Your shop relationship is preferred — they bid lower for you because your drawings save them time.
- Your personal drawing-review checklist has grown to 30+ items and is documented for handoff.

## Ongoing Development

**Stay current:**
- **industry association** — newsletters, certification-renewal courseware, technical standards releases.
- **AWS (American Welding Society)** — for welding-spec updates.
- **ASME** — for mechanical-engineering standards updates.
- **The Fabricator** magazine — monthly.
- **Modern Machine Shop** — monthly.
- **AECbytes** newsletter — for BIM and design-tech.
- **EngineerLive** — daily engineering news.
- **Autodesk University** annual conference — recorded sessions free.
- **NSCA (National Systems Contractors Association)** — for AV integration industry pulse.
- **CEDIA** — for residential AV integration.
- **Commercial Integrator and Systems Contractor News** — trade press; monthly.
- **AVNation podcasts** — AV-industry talk; weekly.
- **The IEEE Spectrum and IEEE engineering journals** — for academic-side updates.
- **The CSI (Construction Specifications Institute) newsletter** — for spec-writing discipline.

**Communities to join:**
- **professional association local chapters** — in-person matters; the community is small.
- **ASME local chapters** — mechanical-engineering peer network.
- **r/AskEngineers** and **r/MechanicalEngineering** — variable but useful for spot questions.
- **Eng-Tips Forums** — old-school but the deep-dive threads on GD&T and DFM are some of the best on the internet.
- **The CSI (Construction Specifications Institute)** local chapters — for spec writing.
- **NSCA local chapters** — for AV integration peer community.
- **AVNation Slack / Discord** — variable but useful for tool talk.
- **industry trade show / ISE conferences** — annual; the trade-show floor is where the real intel lives.
- A small peer-engineer circle (3-5 leads) — monthly drawing-package swaps with structured peer review.

**Quarterly cadence:**
- Pull every drawing-package you issued. Score the field execution: zero RFIs (10), minor RFIs (7), major rework (3).
- Identify the patterns. Update your drawing-review checklist with the lesson.
- Re-audit one BOM-extraction case study against the text-first discipline; identify drift points.
- Score vendor relationships: who priced fairly, who didn't; who saved you time on RFIs.
- Re-read one foundational text (Madsen, Anderson DFM, industry design reference manual); identify what you can use now.

## Cross-References

- The agent that operates in this domain: `agents/engineering-lead/SKILL.md`
- Methodology framework(s) cited: `agents/engineering-lead/context/methodology/` (in development)
- Reference clippings: `agents/engineering-lead/context/references/` (vendored as Phase 1 expands)
- Related agents: `agents/sales-director/SKILL.md` (engineering scoping informs deal qualification — load both for high-value-deal review), `agents/product-manager/SKILL.md` (for productized engineering offerings), `agents/deep-researcher/SKILL.md` (vendor-research before validation)
- Critical SKILL.md rule: BOMs extracted via PyPDF2 text-first ALWAYS, never visual reading. See SKILL.md and `feedback_lmg_cad_reading` for the reasoning.
- Three-principle gate (per SKILL.md): Invention, Manufacturability, Drawing-Rigor held in productive tension.
- For [your employer] work: the BOM → SOW → [your CRM] import pipeline lives in `agents/sales-director/[your sales-ops platform]/`. Engineering Lead delegates to [your sales-ops platform] for the import-file generation; [your sales-ops platform] does NOT delegate to customer-facing depts.
- For multi-discipline coordination: MEP + structural + AV + IT clash-detection runs in BIM 360 / Navisworks; the punch-list lives in the spec.
- For RFP response work: pair this learning path with the RFP-response methodology in `agents/sales-director/[your sales-ops platform]/memory/methodology_rfp_response_pipeline.md`.
- Engineering Lead is downstream of Sales (deal qualified) and upstream of fabrication / install (drawings issued). The drawing is the contract.
- For RFP technical-scope work: validate every requirement against industry standards (e.g., CSI) before agreeing to it; flag the requirements that conflict with each other.
- For projection / LED-wall projects: pair with sightline-math, brightness-budget, and pixel-pitch-vs-viewing-distance calcs before specifying.
- For network-AV (Dante / NDI / SDVoE / AVB): the network spec is half the AV spec. Coordinate with IT trade early.
- For sustainability / LEED-credit work: align with LEED v4 EQ credits where AV / IT contribute (acoustic comfort, daylighting integration with shading, low-emitting materials).
- Critical discipline carryover: every vendor quote validated text-first, never visual. Visual reading on vendor PDFs gets model numbers and manufacturer names wrong. PyPDF2 is the gate.
- For one-person engineering operations: the agent + the discipline + the checklist together replace a CAD checker. Trust the discipline; verify with the checklist.
- For mentoring junior engineers: the checklist + the drawing-package archive + the post-mortem entries together produce more competence per quarter than any formal course.
- For sheet-metal nesting and CNC programming: Inventor and SolidWorks are the dominant tools; Fusion 360 for the lower-budget operations.
- Audit trail: every drawing-package is archived with revision metadata. The audit trail is the contract.
