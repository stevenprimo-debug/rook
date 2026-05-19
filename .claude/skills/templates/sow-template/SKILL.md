---
name: SOW Template Generator
description: |
  Generate a customer-ready Statement of Work (SOW) for a defined engagement. Asks
  for engagement model (fixed-fee project / time-and-materials / retainer /
  rev-share / SaaS-subscription), engagement size (freelancer / professional /
  enterprise — sets legal depth), and domain (av-integration / shopify-services /
  software-saas / consulting / design-build). Loads the universal 12-section
  skeleton, fills the matching variant content, and slots in customer-specific
  details. Outputs a markdown SOW ready for html2pdf seamless render. Never
  uses preamble. Never describes a route as "cheap" — right-sized scope is
  full-quality scope at the right depth.
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
  Fire when the user says: write a SOW, draft a SOW, statement of work, scope
  document, services agreement scope, project scope, engagement scope, draft
  the scope, write the engagement doc, lock down scope, customer SOW, contract
  scope. Also fires when the user has accepted a proposal and needs the
  execution-phase document.
inherits:
  - skeleton: skeleton.md
  - variants: variants/
  - references: references/
---

# SOW Template Generator

## Overview

SOW = Statement of Work = the **post-contract execution document**. A signed
proposal becomes an SOW; the SOW defines exactly what will be done, for what
price, on what schedule, with what acceptance criteria. Distinct from
`proposal-template` (pre-contract pitch) and `msa-template` (umbrella legal
terms that an SOW references).

Three axes determine the output:

| Axis | Options | Effect |
|---|---|---|
| **Engagement model** | fixed-fee project / time-and-materials / retainer / rev-share / SaaS-subscription | Sets the pricing section shape and payment schedule pattern |
| **Engagement size** | freelancer / professional / enterprise | Sets the legal-protection depth (light → heavy clauses) |
| **Domain** | av-integration / shopify-services / software-saas / consulting / design-build | Sets the technical/methodological sections (sections 2-4 + 8) |

## How to use

1. Customer says "draft a SOW for {customer} on {engagement scope}"
2. Skill loads `skeleton.md` (universal 12-section frame)
3. Skill asks the three axis questions if not specified
4. Skill loads matching variant from `variants/{domain}.md` to fill sections 2-4 + 8
5. Skill asks for slot fills (provider/customer details, dates, pricing, deliverables)
6. Skill writes the filled SOW to the path the customer specifies (default:
   `out/YYYY-MM-DD-{customer}-sow.md`)
7. Skill offers to convert to PDF via html2pdf (seamless, never --paginated)

## 12-section universal skeleton (from references/skeleton.md)

1. Project Overview — parties + contacts + background + purpose + engagement model
2. Approach & Methodology (domain-coded; variant fills)
3. Deliverables, Milestones & Tasks — granular tables (deliverable / objective / due date / format; milestones with start+finish; phase schedule; task-level breakdown)
4. Customer-Side Dependencies (domain-coded; variant fills)
5. Scope of Work — IN / OUT (most important section; be specific)
6. Implementation Plan — Pre / Execution / Acceptance phases
7. Pricing & Terms — total fee + payment schedule + out-of-scope rate + reimbursables
8. Training & Knowledge Transfer (domain-coded; variant fills)
9. Support, Warranty & SLA — warranty period + third-party warranties + post-warranty plan + single point of contact
10. Reporting, Standards & Success Definition — communications cadence + standards/tests + verbatim sponsor success criteria + requirements
11. Acceptance & Sign-Off — acceptance criteria + closure document table
12. Disclaimer — purpose + source + change triggers + scope-revision boundary

## Variants ship with

- `variants/shopify-services.md` — Shopify services engagement seed (clean fixed-fee Shopify services pattern) (clean fixed-fee Shopify services)
- `variants/av-integration.md` — based on [Prime Contractor]/AMH 2026-03-24 LED simulation suite (design-build physical integration)
- `variants/software-saas.md` — Vercel + Supabase build-and-ship pattern
- `variants/consulting-services.md` — advisory engagement, no physical/digital deliverable
- `variants/design-build.md` — creative agency / brand work

Customer adds their own variants via `variants/_template.md` (skeleton + 6
domain-coded slots).

## Reference library (cited, not embedded)

Saved at `references/`:
- `references/sec-kleverex-sow.md` — pointer to SEC-filed Kleverex SOW (mid-market formal SOW pattern, SLA tiers, Provider/Customer Tasks split)
- `references/projectmanager-template.md` — operational PM-frame SOW (Parties / Background / Phases / Deliverables / Milestones / Tasks tables)
- `references/professional-services-tm.md` — Time-and-Materials variant reference
- `references/pandatip-software-dev.md` — freelancer-scale SOW with PandaTip pedagogical notes
- `references/indian-us-software-dev.md` — enterprise legal-grade clauses (work-for-hire, pre-existing IP, indemnification, limitation of liability)

## Output

The skill writes a self-contained markdown SOW with:
- Provider & customer info table at top
- Numbered sections (1-12) per skeleton
- Slot-filled content per variant + customer specifics
- Acceptance signature block at the bottom
- "Cheers," sign-off (no name, no emojis, plain text per the operator email rules)

Then offers html2pdf conversion (seamless, never --paginated, per
`feedback_html2pdf_always_seamless.md`).

## Anti-patterns (refuse list)

- **Preamble** in the SOW body. First line is the title; second line is parties.
  No warm-up paragraphs.
- **"Cheap" / "shortcut" / "lazy" framing** anywhere in the SOW. Right-sized
  scope = full-quality scope at the right depth.
- **Generic AI warmth** — "We're delighted to partner with..." Cut.
- **Vague scope IN/OUT.** Section 5 is the contractual heart; if it's vague,
  the engagement bleeds money. Be specific.
- **Naked PARK in deliverables.** Every deferred item has an idea-specific
  trigger (date / event / dependency).

## Success criterion (universal)

This skill succeeded when the customer signs the SOW and the engagement starts
on the agreed milestones. The customer closing their laptop and going outside
because the contract is locked is the win. Engagement (in the negative
ChatGPT-style sense) is the failure mode.

## Cross-references

- Universal skeleton: `references/skeleton.md` (the master 12-section frame)
- Sister skill: `proposal-template` (pre-contract pitch this SOW is downstream of)
- Sister skill: `msa-template` (Master Services Agreement this SOW can reference if customer has one signed)
- [example enterprise customer] v4 visual frame: `agents/sales-director/COMPANIES/[CLIENT_REPO]/[CLIENT_PROJECTS]/[ENTERPRISE_CLIENT]/[ENTERPRISE_CLIENT]/[ENTERPRISE_CLIENT_HQ]/PROPOSAL/[enterprise client]_Proposal_v4.html` (if customer wants branded SOW cover)
- Shopify-services SOW seed pattern: customer engagement template
- SOW skeleton seed: `out/2026-05-14-sow-template-skeleton.md`
- Anti-pattern source: `.claude/memory/feedback_no_mono_in_proposals.md`, `feedback_design_quality_standard.md`, `feedback_html2pdf_always_seamless.md`
