---
name: Proposal Template Generator
description: |
  Generate a customer-facing proposal — the PRE-CONTRACT pitch document.
  Maps content to the [example enterprise customer] v4 visual frame (cover → exec letter → exec summary →
  understanding → approach → investment & options (scaled tier cards) → risks
  & mitigation → why us → timeline → next steps → footer). Outputs branded
  HTML that html2pdf renders seamless. Distinct from `sow-template` (post-
  contract execution doc this proposal becomes). Never uses preamble. The
  recommended tier is named, not hidden in three-equal-weight options.
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
  Fire when the user says: write a proposal, draft a proposal, send a proposal,
  pitch deck, sales pitch, scaled proposal, investment options, RFP response,
  proposal for {customer}, three-tier proposal, good/better/best. Also fires
  when the user has had a discovery call and wants to follow up with a
  proposal document.
inherits:
  - skeleton: skeleton.md
  - variants: variants/
  - visual_frame: agents/sales-director/COMPANIES/[CLIENT_REPO]/[CLIENT_PROJECTS]/[ENTERPRISE_CLIENT]/[ENTERPRISE_CLIENT]/[ENTERPRISE_CLIENT_HQ]/PROPOSAL/[enterprise client]_Proposal_v4.html
---

# Proposal Template Generator

## Overview

Proposal = pre-contract pitch. Demonstrates the provider listened, lays out
1-3 paths forward at different investment levels, surfaces real risks with
real mitigations, articulates why the provider specifically. A signed
proposal triggers downstream SOW work (use `sow-template`).

**Visual frame is locked: [example enterprise customer] v4 HTML template.** Reference:
`reference_proposal_master_template_bsa_v4.md`. Skill fills content into
existing visual components — never invents new visual patterns.

## How to use

1. Customer says "draft a proposal for {customer} on {engagement type}"
2. Skill loads `skeleton.md` (universal 12-section content frame)
3. Skill asks for variant (av-integration / shopify-services / software-saas / consulting / design-build / rfp-response)
4. Skill loads matching variant from `variants/{name}.md`
5. Skill asks for the three pricing tiers + recommended tier
6. Skill asks for 3-5 specific risks the customer cares about (not boilerplate)
7. Skill fills [example enterprise customer] v4 HTML template with content
8. Skill writes filled HTML to `out/YYYY-MM-DD-{customer}-proposal.html`
9. Skill offers html2pdf conversion (seamless, never --paginated)

## 12 content sections mapped to [example enterprise customer] v4 visual components

| # | Content | [example enterprise customer] v4 component |
|---|---|---|
| 1 | Cover page | `.cover` (dark — logo + client name + service line + submitter) |
| 2 | Executive letter | `.letter` (light, "Cheers," sign-off pattern) |
| 3 | Executive summary (one-page TL;DR) | Section 1 — feature cards or callout |
| 4 | Our understanding (proves we listened) | Section 2 — body + callouts |
| 5 | Proposed approach (the HOW) | Section 3 — feature cards / role groups |
| 6 | Investment & options (SCALED tier cards) | Section 4 — **tier cards** + investment callout |
| 7 | Risks & mitigation table | Section 5 — table + callouts |
| 8 | Why us (qualifications + case studies) | Section 6 — bio cards + pull quotes |
| 9 | Timeline (visual schedule) | Section 7 — timeline or gantt |
| 10 | Next steps (one CTA) | Section 8 — callout |
| 11 | Appendix (optional) | Section 9 — feature cards / tables |
| 12 | Doc footer | `.doc-footer` (dark) |

## Pricing tier pattern (the scaled proposal — section 6)

```
Tier 1 — Essentials       Tier 2 — Recommended ⭐    Tier 3 — Comprehensive
${LOW}                    ${MID}                       ${HIGH}
${T1_DURATION}            ${T2_DURATION}              ${T3_DURATION}
{T1 deliverables}         {T1 + extras}                {T2 + more extras}
Best for: {use case}      Why this: {rationale}       Best for: {bigger use case}
Trade-off: {what's out}                                Best for: {longer horizon}
```

Recommended tier is visually distinct ([example enterprise customer] v4 `.best` modifier on the card).
Don't equalize the three tiers — name the recommendation and explain it.

## Risks & mitigation pattern (section 7 — the trust-builder)

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | {specific risk} | L/M/H | L/M/H | {specific mitigation step} | Provider / Customer / Shared |

**Anti-pattern refused:** boilerplate mitigations like "communication will be
frequent." Real mitigations are specific: "Weekly Friday status emails with
explicit blocker callouts; any blocker >48 hours triggers a 30-minute
escalation call." If the mitigation isn't actionable, the risk isn't really
mitigated.

## Variants ship with

- `variants/shopify-services.md` — Shopify-services-style pitch
- `variants/av-integration.md` — [enterprise client]-style physical install pitch
- `variants/software-saas.md` — build-and-ship product proposals
- `variants/consulting-services.md` — advisory engagements
- `variants/rfp-response.md` — modifier (adds RFP section refs + compliance matrix to any base variant)

## Output

Filled [example enterprise customer] v4 HTML with content slots replaced + html2pdf seamless conversion.
"Cheers," sign-off on the executive letter (no name, no emojis, plain text per
the operator email rules).

## Anti-patterns (refuse list)

- **Preamble** in the executive letter. The first paragraph names what was
  heard and what's proposed. No "We're so excited to..."
- **Hidden recommended tier.** The middle tier is visually distinct and named
  as the recommendation with a one-sentence rationale.
- **Boilerplate risk mitigations.** Generic "we communicate well" mitigations
  are refused.
- **Forbidden vocabulary** (CD voice-spine § 4): elegant, premium, luxury,
  delightful, magical, elevate (verb), leverage (verb-as-filler), deep dive,
  as an AI.
- **Mono fonts on client surfaces.** Per `feedback_no_mono_in_proposals.md`.
- **AI-slop visuals.** No glassmorphism, no neon-glow, no gradient-wash. Per
  `feedback_design_quality_standard.md`.

## Success criterion (universal)

This skill succeeded when the customer says yes and signs. The cleanest
proposal is the one that makes saying yes the obvious move within the smallest
number of words.

## Cross-references

- Universal skeleton: `skeleton.md` (12-section content frame)
- Sister skill: `sow-template` (post-contract execution doc this proposal becomes)
- Visual frame lock: `.claude/memory/reference_proposal_master_template_bsa_v4.md`
- Anti-pattern sources: `feedback_no_mono_in_proposals.md`, `feedback_design_quality_standard.md`, `feedback_html2pdf_always_seamless.md`
- Proposal skeleton seed: `out/2026-05-14-proposal-template-skeleton.md`
