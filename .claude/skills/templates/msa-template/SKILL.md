---
name: MSA Template Generator
description: |
  Generate a Master Services Agreement (MSA) — the umbrella legal contract
  signed ONCE per customer relationship. Individual SOWs sit underneath the
  MSA and reference its terms. Two variants: pro-customer (drafted in
  customer's favor) and pro-provider (drafted in this system's favor — the
  default for this system-authored MSAs). Carries the legal boilerplate that
  shouldn't be relitigated per engagement: IP ownership, indemnification,
  liability cap, confidentiality, force majeure, governing law, dispute
  resolution. Never uses preamble. Right-sized legal depth is full-quality
  legal depth at the right depth.
type: skill
category: contracts
version: "1.0.0"
status: operational
voice: SYSTEM-DOMINANT
tools:
  - Read
  - Write
  - Edit
  - Glob
trigger: >
  Fire when the user says: write an MSA, draft an MSA, master services
  agreement, master agreement, umbrella contract, legal terms, terms and
  conditions, IP agreement, services contract, work-for-hire agreement,
  pre-existing IP carve-out, indemnification, limitation of liability.
inherits:
  - skeleton: skeleton.md
  - variants: variants/
  - references: references/
---

# MSA Template Generator

## Overview

MSA = Master Services Agreement = the umbrella legal contract. Signed ONCE
per customer relationship; SOWs sit underneath and reference the MSA's terms.
For one-off small engagements (sub-$25K freelancer-scale), an MSA may be
overkill — use `sow-template` standalone with embedded legal terms. For
repeat or scaling customer relationships, the MSA + multi-SOW pattern is
standard professional services practice.

## How to use

1. Customer says "draft an MSA for {customer}" or "we need umbrella legal terms"
2. Skill asks: pro-customer (default if customer is large enterprise) or pro-provider (default for this system-authored)?
3. Skill loads matching variant from `variants/{pro-customer | pro-provider}.md`
4. Skill asks for slot fills (provider/customer legal names, addresses, governing law state, key contacts)
5. Skill writes filled MSA to `out/YYYY-MM-DD-{customer}-msa.md`
6. Skill offers html2pdf conversion

## Sections (PLC Master Software Development Agreement structure — legal-grade)

1. Definitions (30+ defined terms — Acceptance / Background Technology / Confidential Information / Deliverables / etc.)
2. Services & Statements of Work (this MSA's relationship to individual SOWs)
3. Changes & Change Orders (formal Project Change Request procedure)
4. Customer Responsibilities (timely access, decision authority within agreed SLA)
5. Developer Personnel & Subcontractors (right to subcontract / restrictions)
6. Acceptance & Testing (acceptance procedure + deemed-acceptance window)
7. Fees, Expenses & Invoicing (Net 15 / 30 + late fees + suspension rights)
8. Taxes (Customer pays all taxes except Provider income tax)
9. Intellectual Property & License (work-for-hire + Background Technology / Pre-existing IP carve-out + Approved Open-Source / Third-Party Materials)
10. Confidentiality (3-year survival)
11. Warranties (workmanship + disclaimer of implied warranties)
12. Indemnification (Customer indemnity for content + Developer indemnity for IP infringement)
13. Limitation of Liability (no indirect/consequential + capped at fees paid)
14. Force Majeure (subcontractor failures, third-party outages, acts of God, etc.)
15. Term & Termination (initial term + termination for cause with 30-day cure)
16. Governing Law & Venue (specific state + courts + attorneys' fees)
17. Notices, Assignment, Entire Agreement, Severability (standard boilerplate)

## Variants

- `variants/pro-customer.md` — drafted in customer's favor (based on PLC Master Software Development Agreement). Use when the customer is a large enterprise that will mark up anything weaker.
- `variants/pro-provider.md` — drafted in this system's favor (flipped clauses). The DEFAULT for this system-authored MSAs sent to mid-market customers.

The two variants are NOT 50% different — they share ~80% of clauses verbatim
(definitions, force majeure, governing law boilerplate). The flip happens in:
IP ownership (work-for-hire vs license-back), liability cap (10x fee vs 1x
fee), indemnification scope, change-order judgment authority, termination
for convenience rights.

## References (legal-grade source material, cited not embedded)

- `references/plc-master-software-dev-agreement.md` — pointer to clipped PLC pro-customer MSA (the gold-standard 30+ defined terms reference)
- `references/indian-us-software-dev-agreement.md` — pointer to clipped Indian/US Software Dev Agreement (enterprise legal-grade clauses)
- `references/yc-form-msa.md` — Y Combinator standard MSA template (pending clip)
- `references/b2b-saas-msa.md` — B2B SaaS Master Subscription Agreement (pending clip)

## Critical legal carve-outs (this system-specific)

**Background Technology / Pre-existing IP clause (mandatory in every MSA):**
this system retains all methodology, agent patterns, skill libraries, and
reusable code authored before or independent of the engagement. Customer owns
ONLY the Work Product specifically created under their engagement. This
protects the this system as a reusable asset across customers.

**Force Majeure includes AI provider outages:** Anthropic API downtime,
provider deprecations, model changes. Standard force majeure doesn't cover
this; this system MSAs do.

## Anti-patterns (refuse list)

- **Preamble** in the MSA body. First section is Parties; second is Recitals
  (WHEREAS clauses). No warm-up.
- **Vague IP clauses.** Always explicit work-for-hire language + Background
  Technology carve-out. Vague IP = future dispute.
- **Unlimited liability.** Always include a cap (typically 1x fees paid during
  term).
- **No termination cure period.** Always allow 30-day cure before termination
  for cause.
- **Forbidden vocabulary** per CD voice-spine § 4 — even in legal docs, no
  "elegant" / "premium" / "delightful."

## Success criterion (universal)

This skill succeeded when the customer's counsel reviews the MSA and either
signs without redlines or returns minor redlines that don't touch the core
this system protections (Background Technology, liability cap, governing law).
Counsel signing without major fuss is the win.

## Cross-references

- Sister skill: `sow-template` (SOWs reference this MSA's terms)
- Sister skill: `saas-msa-template` (SaaS-subscription equivalent for the product subscription Stack customers)
- Sister skill: `nda-template` (often signed BEFORE the MSA, during discovery)
- Reference clipping: `Clippings/1 Master Software Development Agreement  PDF  Specification (Technical Standard).md`
- Reference clipping: `Clippings/Sample Software Development Agreement Indian Developer  US Client   PDF  Indemnity.md`
