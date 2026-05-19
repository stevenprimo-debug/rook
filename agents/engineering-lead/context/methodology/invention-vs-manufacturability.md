# Invention vs. Manufacturability

## What This Framework Is

Invention vs. manufacturability is the engineering-leadership
discipline that distinguishes between **designs that solve the
problem on paper** and **designs that can be built, installed,
commissioned, supported, and maintained over the system's
lifetime**. The framework holds that **most engineering failures
happen at the boundary** — a clever design that's hard to source,
hard to install, hard to commission, hard to troubleshoot, hard
to support — and that the engineering lead's job is to manage
this boundary deliberately, not retroactively.

For the operator's domain (commercial AV/LED integration at the [your employer]
scale), the framework operates on six manufacturability
dimensions:

1. **Sourcing** — are all components currently available at
   acceptable lead times, from suppliers with track records?
2. **Installability** — can the named integrator's team install
   this in the specified timeline with the specified labor
   skills?
3. **Commissionability** — can the system be configured, tested,
   and brought into operation reliably?
4. **Operability** — can the named operator team run the system
   day-to-day without escalation to specialized engineers?
5. **Maintainability** — can the system be serviced over its
   expected lifetime, including parts availability for end-of-
   life replacements?
6. **Documentability** — can the as-built state be captured in
   drawings and SOPs that survive the original team's tenure?

Each dimension carries a pass/fail check at the design stage. A
design that passes invention (solves the problem) but fails one
or more manufacturability dimensions gets revised before
proposal, not discovered during installation.

The framework distinguishes engineering leadership from individual
engineering: individual engineers may produce elegant inventions
that fail manufacturability; the engineering lead's job is to
catch this before the design becomes a commitment.

## Why It Matters For This Agent

Engineering Lead's bench gates on three principles: Buildability-Pole,
Drawing-Rigor-Pole, and Vendor-Reality-Pole. The invention vs.
manufacturability framework is the operating implementation of
the first and third poles.

- **Buildability-Pole** asks: "Can this design be built, installed,
  commissioned, and supported on the named timeline with the
  named team?" The framework's six dimensions are the gate.

- **Vendor-Reality-Pole** asks: "Do all named vendors actually
  exist, deliver on time, and have the support infrastructure
  the system requires?" The framework's sourcing dimension is
  the gate.

For the operator's [your employer] work, the framework prevents the most expensive
failure mode in integration: a beautiful design that wins the
proposal, then discovers during execution that key components have
12-week lead times, the install requires labor skills the team
doesn't have, or the commissioning process is fundamentally
fragile. These discoveries during execution produce schedule slips,
budget overruns, and client trust damage.

## Core Concepts

### 1. The Six Manufacturability Dimensions

Each dimension is checked explicitly during design review:

**Sourcing:**
- Are all components available? (Confirmed with vendor, not
  assumed from catalog.)
- Lead times within the project window?
- Vendor stability — financial state, track record?
- Single-point-of-failure dependencies (only one supplier;
  proprietary parts)?

**Installability:**
- Required labor skills available on the integrator's team?
- Physical access for installation (cable runs, hardware
  placement, weight loads)?
- Sequence dependencies (what must be installed before what)?
- Specialized tools or equipment required?

**Commissionability:**
- Network/AV configuration process documented?
- Test procedures validated on similar systems?
- Required commissioning expertise on the team?
- Time-to-commission realistic for the project window?

**Operability:**
- Client operator team can run the system without escalation?
- Routine operations documented and trainable?
- Failure modes graceful (system degrades, doesn't catastrophic
  fail)?
- Escalation paths clear (who to call when something breaks)?

**Maintainability:**
- Parts availability over expected lifetime?
- Service contracts and SLA realistic?
- Software update paths defined?
- End-of-life replacement strategy?

**Documentability:**
- As-built drawings produced?
- SOPs for operations and maintenance?
- Network diagrams and configuration backups?
- Knowledge transfer to client team complete?

A design that fails any dimension gets revised before commitment.

### 2. The Sourcing Reality Check

Most design-stage failures are sourcing failures. The check:

- **Confirm availability** with the vendor directly, not from
  catalog assumption.
- **Verify lead times** in writing where stakes warrant.
- **Identify alternates** for every key component (what's the
  backup if the primary fails to deliver?).
- **Check vendor stability** — recent layoffs? Acquisition?
  Discontinuation announcements?
- **Flag single-source dependencies** — proprietary parts that
  bottleneck the project on one vendor.

For the operator's domain, vendor-reality concerns include LED panel
manufacturers (consolidating industry; some lines discontinued),
specialized AV processors (lead times can spike during industry
events), structural mounting hardware (specialty items with long
lead times).

### 3. The Installability Audit

Designs that look clean on paper may be impossible to install
practically. Common failures:

- **Cable runs that can't physically reach** — the cable path
  exceeds product spec, or the conduit run is too tight.
- **Hardware that can't physically be hung** — structural
  capacity insufficient, or rigging access blocked.
- **Sequence conflicts** — Component A must be installed first
  but Component B is required to test it.
- **Labor mismatch** — design requires specialist labor (e.g.,
  high-rigging, electrical certification) the integrator team
  doesn't have.

The audit walks through the install sequence mentally (or with
the install foreman directly): can each step be done with
available labor, tools, and access?

### 4. The Commissioning Risk Profile

Commissioning is the highest-risk phase of integration. Common
failures:

- **Network configuration** that works in test environment but
  fails in client environment (firewall rules, VLANs, DNS).
- **AV signal chains** that demonstrate in lab but produce
  artifacts in production environment (cable lengths, EMI,
  ground loops).
- **Software integration** between systems that documented
  protocols don't actually implement consistently.
- **Calibration** required by specialized expertise the client
  team doesn't have post-handoff.

The risk profile asks: what could go wrong during commissioning,
and is the team prepared? Designs with high commissioning risk
require either commissioning support contracts or design
revisions to reduce risk.

### 5. The Operability Test

Operability is whether the client's team can actually run the
system day-to-day. The test:

- **Routine operations documented** — startup, shutdown, normal
  use cases.
- **Graceful failure modes** — when something breaks, the
  system shows a useful error message and continues functioning
  in degraded mode, rather than going dark.
- **Self-service troubleshooting** — common issues have
  documented resolution paths.
- **Escalation clarity** — when self-service fails, who does
  the client call?

Operability failures produce post-launch support burden that the
integrator absorbs (warranty/service contracts) or the client
absorbs (training and escalation). Either way, expensive.

### 6. The Maintainability Lifetime View

Systems are maintained over 5-15+ year lifetimes. The view:

- **Component lifetime** — what's the expected service life?
- **Parts availability** — will replacement parts be available
  in year 7? Year 10?
- **Software update paths** — does the system have a credible
  software-maintenance future?
- **End-of-life planning** — when key components reach EOL,
  what's the replacement strategy?

Designs that optimize only for initial install (capex) without
considering lifetime (opex) produce systems that become
maintenance burdens. The maintainability view balances both.

### 7. The Documentation Standard

As-built documentation is the artifact that survives the team
that built the system. The standard:

- **As-built drawings** — accurate to actual installed state,
  not design-stage intent.
- **Network diagrams** — physical and logical, with addressing.
- **Equipment inventory** — make, model, serial, location, network
  config.
- **Configuration backups** — for all configurable equipment,
  with restore procedures.
- **SOPs** — operations, maintenance, and troubleshooting
  procedures.
- **Training records** — who has been trained on what.

The standard exists because the team that built it eventually
moves on. The next team relies entirely on documentation.

## Common Applications

**Pre-proposal manufacturability review:**
Before [your employer] submits a proposal, the engineering lead runs the
manufacturability audit on the design. Sourcing: all components
confirmed with vendors. Installability: install sequence walked
through with foreman. Commissionability: similar systems
referenced. Operability: client team capability assessed.
Maintainability: lifetime plan documented. Documentability:
standard included in scope. Pass: proposal proceeds. Fail: design
revised before submission.

**Vendor confirmation cycle:**
The engineering lead confirms availability and lead times with
named vendors for every line item over a threshold ($5K+ or
schedule-critical). Confirmations are documented; reliance on
catalog data without confirmation is flagged as risk.

**Install-sequence walkthrough:**
For complex installs, the engineering lead walks the install
foreman through the sequence step-by-step. Identifies physical
conflicts, labor mismatches, sequencing problems before
mobilization. Revisions captured in pre-mobilization meeting
notes.

**Commissioning risk mitigation:**
For systems with high commissioning risk (novel integrations,
complex network requirements), the engineering lead specs
commissioning support in the SOW. Either [your employer] retains
commissioning expertise post-handoff, or the design is revised
to reduce risk.

**Post-handoff operability check:**
After client handoff, the engineering lead reviews early-life
support tickets. Categories of tickets reveal operability gaps —
issues that should have been self-service but weren't, escalation
paths that weren't clear. Findings feed back into the next
design cycle.

**Per locked memory: [example enterprise customer] registry standards.** When generating
[example enterprise customer] Tower equipment registry data, the engineering lead applies
the documentation standard — accurate to as-built state, not
design intent. Per `bsa-formatting` skill.

## Anti-patterns (when this framework is misapplied)

**Invention without manufacturability check.** A design that
solves the problem on paper but fails one or more of the six
dimensions. Discovered during execution; produces schedule slips,
budget overruns, trust damage.

**Catalog-trust without vendor confirmation.** Assuming a
component is available because it appears in a vendor catalog.
Catalogs lag inventory reality; the confirmation cycle is the
prevention.

**Per locked feedback: "No Patches — Full Fix Only."** Applied
to engineering: manufacturability failures get redesigned, not
patched. A patched-together install accumulates technical debt
that resurfaces during commissioning or operations.

**Per locked feedback: "Don't Infer Client Entity Names."** The
engineering lead uses the exact names the client uses for
facilities, spaces, equipment. Inferred names produce drawing
errors that compound through documentation.

**Per locked feedback: "Verify Project Status Before Speaking."**
Engineering status reports reflect actual current state, not
optimistic recollections. Honest status enables honest
risk management.

**Per locked feedback: "Check Dept Memory + Conventions Before
Guessing."** Engineering questions check ENGINEERING dept memory
and conventions (e.g., [example enterprise customer] registry standards, vendor data,
[your sales-ops platform] SOW patterns) before guessing.

**Documentation as afterthought.** Producing as-built
documentation after the team has already moved on, from
incomplete memory. The standard requires documentation as part
of the install scope, not a post-hoc reconstruction.

**Vendor-stability blindness.** Specifying vendors without
checking financial state, layoffs, acquisition rumors. Vendor
collapse during the project window is a foreseeable risk that
gets caught with due diligence.

**Maintainability deferred.** Optimizing only for initial install
without lifetime planning. Produces systems that become
maintenance burdens within 3-5 years.

**Per locked feedback: "Mechanical / Sheet-Metal / CNC CAD
Toolkit."** Custom fabrication scope leverages the toolkit's
free/OSS tools to validate manufacturability before commitment.

## Cross-references

- Agent skill: `agents/engineering-lead/SKILL.md`
- Bench: `agents/engineering-lead/personality/_bench.md` (Buildability-Pole, Vendor-Reality-Pole)
- Frameworks index: `agents/engineering-lead/personality/frameworks_index.md`
- Companion methodology: `agents/engineering-lead/context/methodology/drawing-rigor.md`
- Memory: `agents/engineering-lead/memory/reference_mechanical_cad_toolkit.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `.claude/memory/feedback_no_inferring_entities.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `.claude/memory/feedback_check_dept_memory_first.md`
- Skills: `drawing-reader` (text-first PDF extraction discipline)
