# Drawing Rigor

## What This Framework Is

Drawing rigor is the discipline of producing engineering
documentation — CAD drawings, line diagrams, rack elevations,
network diagrams, equipment schedules, cable lists — that
accurately represent reality and survive contact with
installation. The framework holds that **drawings are not
illustrations; they are the build instructions** — and that the
single most expensive failure mode in integration is the gap
between what the drawings show and what the install team can
actually build from them.

The discipline operates across the project lifecycle:

- **Design-phase drawings** — represent the engineering intent
  with enough detail that the install team can build to spec.
- **Issued-for-construction (IFC) drawings** — the contractually
  binding set the install team uses.
- **As-built drawings** — the accurate post-install record that
  reflects actual installed state, including any field changes.
- **O&M drawings** — the maintenance-phase reference that
  operators and service techs rely on for the system's lifetime.

Each drawing carries information at multiple levels of fidelity:
- **Layout fidelity** — what is where (physical placement,
  spatial relationships).
- **Detail fidelity** — what specific component (make, model,
  part number, serial when relevant).
- **Connection fidelity** — what connects to what (cable lists,
  signal paths, network addressing).
- **Configuration fidelity** — how the system is set up
  (settings, calibrations, software versions).

Drawings that lack any layer fail their job in specific ways.

## Why It Matters For This Agent

Engineering Lead's Drawing-Rigor-Pole gates every drawing output
on whether it carries all four fidelity layers at the level the
project phase requires.

- The pole catches the failure mode where drawings look polished
  but lack the detail required for actual install.
- The pole catches the failure mode where as-built drawings
  match the design intent rather than the installed reality.
- The pole catches the failure mode where O&M drawings are
  produced from incomplete memory months after the install.

For the operator's [your employer] work, drawing rigor is what produces
proposals that win on technical credibility, install packages
that the field team can execute without escalation, and as-built
records that survive client team turnover.

The discipline also serves the [example enterprise customer] Tower work specifically (per
the locked `bsa-formatting` skill), where the registry standard
requires accuracy across portal categories, device tags, network
addressing, and rack elevations.

## Core Concepts

### 1. The Four-Layer Fidelity Model

Every drawing carries four fidelity layers:

**Layout fidelity:**
- Physical placement of components within rooms, racks, walls,
  ceilings.
- Spatial relationships (clearances, sight lines, cable runs).
- Coordinate references (architectural grid, room numbers,
  ceiling tile positions).

**Detail fidelity:**
- Specific component identification: manufacturer, model number,
  part number, configuration tier.
- Quantities and unit-of-measure.
- Required accessories and mounting hardware.

**Connection fidelity:**
- Signal paths from source to destination.
- Cable identification (cable ID, type, length, termination).
- Patch panel positions and port assignments.
- Network connectivity (VLAN, IP, switch port).

**Configuration fidelity:**
- Software versions and configuration files.
- Calibration data and setup procedures.
- Operating parameters and presets.

Design-phase drawings emphasize layout + detail. IFC drawings
add connection. As-built drawings update all four to installed
reality. O&M drawings emphasize connection + configuration for
maintenance use.

### 2. The "Read by a Stranger" Test

The test: can a competent stranger to the project, given only
the drawings, install or troubleshoot the system?

For design-phase drawings, the stranger should be able to
estimate cost and schedule.

For IFC drawings, the install foreman should be able to mobilize
without additional verbal context.

For as-built drawings, a service tech who has never seen the
system should be able to diagnose and repair issues.

If the stranger needs verbal context (the original engineer's
explanation), the drawings have failed their job. Engineering
lore that lives only in the original engineer's head is a
single-point-of-failure that the discipline eliminates.

### 3. The CAD Extraction Discipline (Per [example enterprise customer]-Skill)

Per the `drawing-reader` discipline: visual reading of CAD PDFs
misses model numbers and gets manufacturers wrong. The discipline
requires PyPDF2 text extraction FIRST, every time, no exceptions.

The mechanism:
- Open the CAD PDF.
- Run PyPDF2 text extraction.
- Review extracted text for equipment schedules, cable lists,
  device tags, configuration data.
- Cross-reference visual layout with text-extracted detail.
- Visual reading supplements the text data; never substitutes
  for it.

The discipline exists because visual reading of small drawing
text at typical CAD scales produces errors at scale — and those
errors compound through the project lifecycle (wrong part ordered,
wrong cable spec'd, wrong drawing produced).

### 4. The Registry Standard (Per [example enterprise customer]-Skill)

Per the locked `bsa-formatting` skill for [enterprise client tower] work,
the registry standard requires:

- **Portal categories** correctly applied (specific to the [example enterprise customer]
  taxonomy).
- **Device tags** matching the actual installed equipment.
- **Domotz monitoring** state captured accurately.
- **Rack elevations** representing actual rack contents.
- **Room directory** reflecting current naming conventions.
- **Strict formatting** — every cell matters; deviation breaks
  the registry's downstream uses.

The [example enterprise customer] registry is the canonical example of drawing rigor
applied to a specific high-stakes client. The discipline
generalizes to other clients: each major client may have its
own standard, and that standard is locked.

### 5. The Field-Change Capture

During install, field changes happen — components substituted,
routes adjusted, configurations modified. The discipline:

- **Field changes documented in real-time** — not reconstructed
  from memory weeks later.
- **As-installed photos** of key install moments — provide
  ground truth for as-built drawing reconciliation.
- **Change orders signed** for field changes that affect scope,
  schedule, or cost.
- **As-built drawings updated** to reflect installed reality,
  not design intent.

Field changes captured at the time of install produce accurate
as-builts. Field changes deferred to post-install reconstruction
produce as-builts that drift from reality.

### 6. The Network Documentation Standard

Networked AV systems require specific documentation:

- **Physical network diagram** — switches, cabling, port
  assignments.
- **Logical network diagram** — VLANs, subnets, IP addresses,
  multicast configuration.
- **Device inventory** — IP, MAC, hostname, function, owner.
- **Firewall rules** — what flows where, why.
- **Backup configurations** — saved switch and device configs
  with restore procedures.

Network documentation failures produce the slowest, most
expensive troubleshooting cycles in commercial AV. A drawing
package without network detail leaves the operator team unable
to diagnose connectivity issues.

### 7. The O&M Package Standard

The operations and maintenance package delivered at handoff:

- **As-built drawings** (all four fidelity layers).
- **Equipment manuals and specs** for every component.
- **Cable lists** with end-to-end identification.
- **Configuration backups** with restore procedures.
- **Network diagrams** (physical and logical).
- **SOPs** for routine operations.
- **Troubleshooting procedures** for common issues.
- **Escalation contacts** for non-self-service issues.
- **Warranty registration** confirmations.
- **Training records** of who has been trained on what.

The O&M package is the artifact the client uses for the system's
lifetime. Incomplete O&M packages produce post-handoff support
burden that gets absorbed somewhere — usually by the integrator
in warranty claims, or by the client in operational friction.

## Common Applications

**Proposal-stage drawing development:**
The engineering lead develops design-phase drawings that
represent the proposed solution. Layout and detail fidelity are
high; connection and configuration fidelity emerge during design
development. Drawings support the proposal narrative and enable
accurate cost estimation.

**CAD-reading for vendor BOM validation:**
When validating a vendor's BOM against an existing CAD set, the
engineering lead applies the locked PyPDF2 extraction discipline.
Extracted text from drawings is cross-referenced against the BOM
to verify part numbers, quantities, and configurations match.
Discrepancies surface before commitment.

**[example enterprise customer] registry updates:**
Per the locked [example enterprise customer]-skill, registry updates apply strict
formatting — portal categories, device tags, Domotz state, rack
elevations all updated to actual installed state. Visual reading
of drawing PDFs is supplemented by text extraction; every cell
audited.

**Issued-for-construction drawing review:**
Before drawings go to the install team, the engineering lead
applies the "read by a stranger" test. Are layout, detail, and
connection layers complete enough for the install foreman to
mobilize without verbal context? Gaps get filled before issue.

**Field-change documentation cycle:**
During install, the engineering lead reviews daily field reports
from the install foreman. Field changes get captured in
real-time updates to the drawing set, not deferred to
post-install reconstruction. As-installed photos archived as
ground-truth.

**As-built handoff package:**
At project close, the engineering lead assembles the O&M
package per the standard. All four fidelity layers updated to
installed reality. Client training records included. Package
delivered as a single coherent artifact, not assembled piecemeal
from email attachments.

## Anti-patterns (when this framework is misapplied)

**Drawings as illustration.** Drawings polished to look good in
the proposal but lacking the detail required for install. Proposal
wins; install team escalates; engineering lead has to fill the
gap from memory.

**Visual-only CAD reading.** Per the locked feedback, reading
CAD PDFs by eye produces model-number errors. The text-extraction
discipline is the prevention.

**Per locked feedback: "[example enterprise customer] Formatting" skill must fire.** Any
[enterprise client]-related work loads the [example enterprise customer]-skill formatting rules.
Deviation breaks the registry's downstream uses.

**As-built drawings matching design intent.** Drawings that
reflect what was supposed to be installed, not what actually was
installed. Field changes invisible. Service teams troubleshoot
against incorrect documentation.

**Per locked feedback: "Don't Infer Client Entity Names."**
Drawings use the exact names the client uses for facilities,
spaces, equipment. Inferred names produce drawing errors that
compound.

**O&M package as afterthought.** Producing O&M documentation in
the days before close-out, from memory, with key install team
members already moved to next project. The package is incomplete;
the client absorbs the gap.

**Per locked feedback: "Check Dept Memory + Conventions Before
Guessing."** Drawing questions check ENGINEERING dept memory
(vendor data, registry standards, project conventions) before
guessing.

**Network documentation neglected.** Drawing packages strong on
physical layout, weak on network. Operations team can't
troubleshoot connectivity issues without escalation.

**Field-change capture deferred.** Field changes happen and
nobody captures them in real-time. Weeks later, as-built
reconstruction is impossible from memory. As-built drift baked
in.

**Per locked feedback: "No Patches — Full Fix Only."** Applied
to drawings: when an error is found, the drawing is corrected
properly with the change tracked. Patching one corner without
propagating the change through related drawings produces drift
across the drawing set.

**Per locked feedback: "Verify Project Status Before Speaking."**
Drawing status reports reflect actual current state. Honest
status enables honest schedule management.

## Cross-references

- Agent skill: `agents/engineering-lead/SKILL.md`
- Bench: `agents/engineering-lead/personality/_bench.md` (Drawing-Rigor-Pole)
- Frameworks index: `agents/engineering-lead/personality/frameworks_index.md`
- Companion methodology: `agents/engineering-lead/context/methodology/invention-vs-manufacturability.md`
- Skill: `drawing-reader` (PyPDF2 text-first extraction discipline)
- Skill: `anthropic-skills:bsa-formatting` ([example enterprise customer] registry standards)
- Skill: `anthropic-skills:lmg-engineering-scope`
- Memory: `.claude/memory/feedback_no_inferring_entities.md`
- Memory: `.claude/memory/feedback_check_dept_memory_first.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `agents/engineering-lead/memory/reference_mechanical_cad_toolkit.md`
