---
name: NDA Template Generator
description: |
  Generate a Non-Disclosure Agreement (NDA). Four variants: employee
  (employer→employee one-way), mutual (two parties, both directions),
  multi-party (3+ signers with related-agreement cross-references), one-way
  generic (single-direction, no employment relationship, common for vendor
  or prospect conversations). Ships fast — most NDAs need to be sent within
  hours of a first conversation, not days. Never uses preamble.
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
  Fire when the user says: send an NDA, draft an NDA, NDA for {customer},
  mutual NDA, employee NDA, confidentiality agreement, pre-meeting NDA,
  protect this idea, before I share, before they share, non-disclosure.
inherits:
  - skeleton: skeleton.md
  - variants: variants/
---

# NDA Template Generator

## Overview

NDA = Non-Disclosure Agreement. Most NDAs need fast turnaround — the operator gets
a meeting request, needs to send an NDA before sharing IP. This skill
generates a signable NDA in under a minute once the four variant choice + 5
slots are filled.

## Four variants

| Variant | When to use | Direction |
|---|---|---|
| **employee** | Hiring contractor / employee who'll see internal IP | One-way (employer → employee) |
| **mutual** | Two companies exploring partnership where both share IP | Two-way (symmetric) |
| **multi-party** | 3+ signers (talent + manager + studio pattern) with related Subject Agreements | Multi-way, cross-referenced |
| **one-way generic** | Vendor / prospect / advisor who needs to see IP before deciding | One-way (discloser → recipient) |

## How to use

1. Customer says "send an NDA to {recipient}" or "draft an NDA for {scenario}"
2. Skill asks for variant if not clear from context
3. Skill asks for slots: discloser legal name, recipient legal name + role, effective date, term length (default 2 years for confidentiality survival), governing law state
4. Skill loads matching variant from `variants/{name}.md`
5. Skill writes filled NDA to `out/YYYY-MM-DD-{recipient}-nda.md`
6. Skill offers html2pdf conversion + e-signature via DocuSign

## Core sections (universal across variants)

1. Parties (variant determines structure — 2 signers, 3+ signers, etc.)
2. Recitals (WHEREAS clauses establishing context)
3. Definition of Confidential Information (5 explicit categories: technical / business / employees / customer-submitted / other not-public)
4. Confidentiality Obligations (don't disclose to third parties, use reasonable care, return-or-destroy on termination)
5. Carve-outs (5 categories of what's NOT confidential: public domain at disclosure, becomes public other than by breach, independently developed, received from third party without restriction, compelled by legal process)
6. Term & Survival (engagement term + confidentiality survives 2-3 years)
7. Remedies (irreparable harm + injunctive relief + waiver of bond requirement)
8. Governing Law & Jurisdiction
9. Boilerplate (notices, assignment, entire agreement, severability)
10. Sign-off (variant determines signer count)

## Variants ship with

- `variants/employee.md` — based on clipped Employee NDA reference
- `variants/mutual.md` — based on clipped Mutual NDA reference
- `variants/multi-party.md` — based on clipped Confidentiality and Non Disclosure Agreement (Filipino-law, 3-party talent/agency pattern)
- `variants/one-way-generic.md` — based on clipped generic Non-Disclosure Agreement Template

Optional industry-specific overlays:
- `variants/construction.md` — construction-industry-specific (clipped)
- `variants/business-idea.md` — pre-investment idea-pitch (clipped)

## Anti-patterns (refuse list)

- **Preamble.** NDA body starts with Parties + Recitals. No introduction paragraph.
- **Vague Confidential Information definition.** Always specify categories — vague NDAs are unenforceable.
- **No survival clause.** Always specify how long confidentiality survives after termination (2-3 years standard).
- **No carve-outs.** Always specify the 5 standard carve-outs or the NDA over-reaches and gets challenged.
- **Forbidden vocabulary** per CD voice-spine § 4 — even in legal docs.

## Success criterion (universal)

This skill succeeded when the recipient signs and returns the NDA in under
24 hours and the substantive conversation can begin. Speed matters; the NDA
is the unblock to the real work.

## Cross-references

- Sister skill: `msa-template` (often follows the NDA once partnership solidifies)
- Reference clipping: `Clippings/Confidentiality and Non Disclosure Agreement  PDF  Confidentiality.md`
- Reference clippings (pending): Employee NDA, Mutual NDA, Construction NDA, Business Idea NDA, generic NDA Template
