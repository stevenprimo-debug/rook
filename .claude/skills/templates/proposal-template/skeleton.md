# Proposal — Universal Content Skeleton

> **Purpose:** Content skeleton for the `proposal-template` skill (Saturday build). Distinct from `sow-template` — proposal is PRE-CONTRACT (pitch + scope options + risks), SOW is POST-CONTRACT (defined scope of work to execute).
>
> **Visual frame:** [example enterprise customer] v4 is the canonical HTML template — `agents/sales-director/COMPANIES/[CLIENT_REPO]/[CLIENT_PROJECTS]/[ENTERPRISE_CLIENT]/[ENTERPRISE_CLIENT]/[ENTERPRISE_CLIENT_HQ]/PROPOSAL/[enterprise client]_Proposal_v4.html`. Reference: [`reference_proposal_master_template_bsa_v4.md`](.claude/memory/reference_proposal_master_template_bsa_v4.md). This skeleton defines the CONTENT structure that maps into [example enterprise customer] v4's visual components.
>
> **Distinction from SOW:** Proposal = sales pitch (why us, what we propose, what it costs, what could go wrong). SOW = execution scope (what we'll do, on what date, for what price). A signed proposal becomes the basis for an SOW.

---

## Document type

**This is a proposal.** It is presented to the customer BEFORE contract signing. It exists to:

1. Demonstrate we understand their situation (proves we listened)
2. Lay out 1-3 paths forward at different investment levels (scaled proposal — good/better/best)
3. Surface risks honestly with mitigation strategies (builds trust; not boilerplate)
4. Articulate why us specifically (qualifications, case studies, differentiators)
5. Make the buying decision easy (clear next step, clear investment, clear timeline)

If the customer accepts, a separate SOW is drafted from the accepted proposal scope.

---

# Content sections (mapped to [example enterprise customer] v4 visual components)

| # | Content section | [example enterprise customer] v4 visual component | Notes |
|---|---|---|---|
| 1 | Cover page | `.cover` (dark) | Logo + client name + service line + submitter |
| 2 | Executive letter | `.letter` (light) | The "Cheers," sign-off pattern; 3-4 paragraphs |
| 3 | Executive summary | Section 1 — feature cards / callout | One-page TL;DR — the whole proposal in 300 words |
| 4 | Our understanding | Section 2 — body text + callouts | Proves we listened |
| 5 | Proposed approach | Section 3 — feature cards / role groups | The HOW |
| 6 | Investment & options (scaled) | Section 4 — **tier cards (good/better/best)** + investment callout | THIS is "proposal scale" |
| 7 | Risks & mitigation | Section 5 — table + callouts | Honest, not boilerplate |
| 8 | Why us | Section 6 — bio cards + pull quotes | Qualifications + case studies |
| 9 | Timeline | Section 7 — **timeline** or **gantt** | Visual schedule |
| 10 | Next steps | Section 8 — callout | Single CTA, easy to say yes |
| 11 | Appendix (optional) | Section 9 — feature cards / tables | Case studies, team bios, references |
| 12 | Doc footer | `.doc-footer` (dark) | Brand close |

---

# Section-by-section content guide

## 1. Cover

- `{LOGO}` (visual asset, not CSS-rendered text)
- "Proposal For" kicker
- **`{CLIENT_NAME}`** — the big visible thing
- Service line: `{ONE_LINE_OFFER}` (e.g., "Shopify Storefront Optimization & Backlog Clearance")
- Location(s): `{LOCATIONS}`
- "Prepared by:" `{PROVIDER_NAME}` / `{SUBMITTER_NAME, TITLE}`
- Date + "Confidential" footer
- Brand tag bottom-right (e.g., "Powered by Claude")

## 2. Executive Letter

3-4 short paragraphs, conversational. The "Cheers," sign-off. Pattern:

- Paragraph 1: Why we're writing (you mentioned X; we listened; here's what we propose)
- Paragraph 2: What this proposal contains (3 paths, investment range, timeline window)
- Paragraph 3: Our genuine excitement / fit for the work (one sentence — no fluff)
- Paragraph 4: Next step (single ask — usually "let's talk through Section 6 together")
- Sign-off: "Cheers," / Name / Title line

## 3. Executive Summary (the one-page TL;DR)

If the customer reads only this section, they get:

- **The problem in one sentence:** `{PROBLEM_STATEMENT}`
- **The proposed solution in one sentence:** `{SOLUTION_STATEMENT}`
- **The investment range:** `${LOW_TIER} – ${HIGH_TIER}` across {N} options
- **The timeline:** `{TOTAL_DURATION}` start to acceptance
- **What's NOT in scope:** `{TOP_3_EXCLUSIONS}` (matters as much as inclusions)
- **The recommended path:** `{TIER_RECOMMENDATION}` and why

Render as a feature-card grid (4-6 cards) for visual scan-ability. Don't bury this in prose.

## 4. Our Understanding

Demonstrates we listened. NOT a regurgitation of the RFP / customer email — a synthesis that adds value.

- **What you're trying to achieve:** `{BUSINESS_OUTCOME}` (in customer's language, not provider's)
- **What's making it hard right now:** `{CURRENT_OBSTACLE_OR_CONSTRAINT}`
- **What success looks like 6 months out:** `{SUCCESS_STATE}` (gives the customer a future to point to)
- **Why now:** `{WHY_THIS_IS_THE_RIGHT_MOMENT}` (urgency without manufactured urgency)

If you can quote the customer back to themselves accurately, you've earned the right to propose a solution.

## 5. Proposed Approach

The HOW. This is where the work gets named without being SOW-detail level.

- **Phase 1:** `{PHASE_DESCRIPTION}` — outcome: `{PHASE_OUTCOME}`
- **Phase 2:** `{PHASE_DESCRIPTION}` — outcome: `{PHASE_OUTCOME}`
- **Phase 3:** `{PHASE_DESCRIPTION}` — outcome: `{PHASE_OUTCOME}`

Use [example enterprise customer] v4 **role groups** to attribute work to specific roles/team members where appropriate. If the team is solo, use one role group titled "Engagement Lead" and own it.

## 6. Investment & Options — SCALED PROPOSAL (the key section)

> This is what the operator means by "proposal scale." Customer chooses among 1-3 paths at different investment levels. Each tier has a clear scope delta from the one above/below. Making the choice obvious is the proposal's job.

Render as [example enterprise customer] v4 **tier cards** (good / better / best). The middle (best-fit) tier is the recommended default — visually distinct via the `.best` modifier.

### Tier 1 — `{TIER_1_NAME}` (Essentials)

**Investment:** `${TIER_1_PRICE}`
**Timeline:** `{TIER_1_DURATION}`
**Includes:**
- `{deliverable 1}`
- `{deliverable 2}`
- `{deliverable 3}`

**Best for:** `{BUYER_TYPE_OR_USE_CASE}`
**Trade-off:** `{WHAT_THIS_TIER_DOESNT_DO}`

### Tier 2 — `{TIER_2_NAME}` (Recommended) ⭐

**Investment:** `${TIER_2_PRICE}`
**Timeline:** `{TIER_2_DURATION}`
**Includes:** Everything in Tier 1, plus —
- `{additional deliverable 1}`
- `{additional deliverable 2}`

**Why this tier:** `{ONE_SENTENCE_RATIONALE_FOR_RECOMMENDATION}`

### Tier 3 — `{TIER_3_NAME}` (Comprehensive)

**Investment:** `${TIER_3_PRICE}`
**Timeline:** `{TIER_3_DURATION}`
**Includes:** Everything in Tier 2, plus —
- `{additional deliverable 1}`
- `{additional deliverable 2}`
- `{additional deliverable 3}`

**Best for:** `{LARGER_USE_CASE_OR_LONGER_HORIZON}`

### Investment Callout

Use [example enterprise customer] v4 **investment callout** (dark gradient + light accent text) to anchor the recommended tier's headline number. Visual gravitas.

---

**Payment structure (applies to selected tier):**

| Milestone | Amount | Trigger |
|---|---|---|
| Deposit | `{X}%` | On signing |
| Mid-engagement | `{Y}%` | On Phase 2 acceptance |
| Final | `{Z}%` | On final acceptance |

## 7. Risks & Mitigation (the trust-builder section)

> This section is where most proposals lie or duck — generic boilerplate ("communication is key!") instead of honest risk surfacing. Don't. Real risks named with real mitigations builds more trust than a clean-looking proposal that hides them.

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | `{specific risk}` | Low / Med / High | Low / Med / High | `{specific mitigation step}` | Provider / Customer / Shared |
| R2 | `{specific risk}` | L/M/H | L/M/H | `{mitigation}` | {owner} |
| R3 | `{specific risk}` | L/M/H | L/M/H | `{mitigation}` | {owner} |

**Categories worth surfacing (pick 3-5 actually relevant to THIS engagement — don't pad):**

- **Scope creep** — what we'll do if customer asks for X mid-engagement
- **Dependency risk** — what happens if customer-side input isn't available on time
- **Technology risk** — what if the platform doesn't support what we plan
- **Timeline risk** — what if a phase takes longer than estimated
- **Personnel risk** — what if a key person becomes unavailable
- **Acceptance risk** — what if "done" is contested
- **Budget risk** — what if scope changes blow the fixed-fee
- **External risk** — what if a third-party (Shopify, vendor, regulator) changes terms

**Each risk gets an honest mitigation, not a hand-wave.** "Communication will be frequent" is not a mitigation. "Weekly Friday status emails with explicit blocker callouts; any blocker >48 hours triggers a 30-minute escalation call" is a mitigation.

## 8. Why Us

This section earns the engagement. NOT a brag sheet — proof.

- **Relevant experience:** `{2-3 specific past engagements similar to this one}` (NDA-permitting; anonymize as needed)
- **Methodology:** `{specific framework or approach we use that the customer benefits from}`
- **Team composition:** [example enterprise customer] v4 **bio cards** — headshot + name + role + 2-sentence bio per key person. If solo, one bio card.
- **Differentiators:** What we do that competitors don't (factual, not marketing-claim)

**Optional:** Pull quote from a past customer (using [example enterprise customer] v4 `.pull-quote` component).

## 9. Timeline

Use [example enterprise customer] v4 **timeline** (vertical dotted line + date + event) or **gantt** (horizontal bars across phases) depending on engagement complexity.

- For ≤3 phases: timeline component
- For 4+ phases with overlap: gantt component

Show start → milestones → end. Mark customer-side dependencies (e.g., "stakeholder review window") explicitly so timeline risk is visible.

## 10. Next Steps

ONE clear call-to-action. The proposal's job is to make saying yes easy.

> **Recommended next step:** A 30-minute call to walk through Section 6 (Investment & Options) together and lock the tier that fits. Schedule via `{CALENDAR_LINK}` or reply to this email.

If the customer should sign and return, say so explicitly. If a follow-up call is preferred, say that. Don't end with "let us know your thoughts" — that loses momentum.

## 11. Appendix (optional)

Case studies, detailed team bios, references, sample work, supporting research. Only include what reinforces the buying decision — don't dump everything.

## 12. Doc Footer

[example enterprise customer] v4 dark footer:
- Logo (semi-opacity)
- Brand name
- Tagline: "Powered by Claude" or "Built with this system" or brand-appropriate
- Confidentiality marker if applicable

---

# Proposal vs SOW — when each is used

| | Proposal | SOW |
|---|---|---|
| When | Before contract signing | After contract signing |
| Audience | Decision-maker (often non-technical) | Project team (often technical) |
| Job | Win the engagement | Execute the engagement |
| Tone | Persuasive, qualified, scope-flexible | Precise, contractual, scope-locked |
| Format | Visual ([example enterprise customer] v4 HTML → PDF) | Document (markdown / PDF) |
| Pricing | Tiered options | One locked number |
| Risks | Surfaced, mitigated, transparent | Out-of-scope rate + change-order process |
| Timeline | Phases + estimated durations | Exact dates + milestone owners |
| Length | 8-15 pages | 6-12 pages |

**Workflow:** RFP / discovery → Proposal (1-3 tier options) → Customer accepts a tier → SOW (locked scope of accepted tier) → Execute.

---

# Slot Glossary (for skill build)

Same provider slots as SOW skeleton (`{PROVIDER_LEGAL_NAME}`, `{PROVIDER_ADDRESS}`, `{PROVIDER_CONTACT_*}`, `{END_CUSTOMER_NAME}`), plus proposal-specific:

| Slot | Description | Example |
|---|---|---|
| `{ONE_LINE_OFFER}` | Service line for cover | "Shopify Storefront Optimization & Backlog Clearance" |
| `{PROBLEM_STATEMENT}` | One sentence — what's broken | "Order backlog is growing 12% MoM with no relief in sight" |
| `{SOLUTION_STATEMENT}` | One sentence — what we propose | "A 4-week embedded engagement to clear backlog and stabilize ops" |
| `{LOW_TIER}` / `{HIGH_TIER}` | Investment range | "$10,000 – $40,000" |
| `{TIER_N_NAME}` | Tier label | "Essentials" / "Recommended" / "Comprehensive" |
| `{TIER_N_PRICE}` | Tier $ | "$10,000" |
| `{TIER_N_DURATION}` | Tier timeline | "4 weeks" |
| `{BUYER_TYPE_OR_USE_CASE}` | When this tier fits | "Single-store backlog with no platform changes needed" |
| `{TRADE_OFF}` | What tier doesn't do | "Doesn't include the cost-calc system" |
| `{RECOMMENDATION_RATIONALE}` | Why this tier | "Balances quick relief with foundation for Phase 2" |
| `{RISK}` / `{MITIGATION}` / `{OWNER}` | Risks table inputs | per-row |
| `{CALENDAR_LINK}` | Next-step scheduling URL | calendly.com/primolabs or similar |

---

# Variants (Saturday build — same pattern as SOW)

Same skeleton works across industries; sections 5 (Approach), 6 (Investment scale), and 8 (Why Us) need domain-specific variant content:

- `proposal-template/variants/av-integration.md` ([enterprise client]-style — physical install proposals)
- `proposal-template/variants/shopify-services.md` (the example merchant-style — software services)
- `proposal-template/variants/software-saas.md` (build-and-ship product proposals)
- `proposal-template/variants/consulting-services.md` (advisory engagements)
- `proposal-template/variants/rfp-response.md` (modifier — adds RFP section refs and compliance matrix to any base variant)

---

# Saturday build dependencies

Pairs with:
- `sow-template` skill (for the post-proposal contract phase)
- [example enterprise customer] v4 HTML template (the visual frame this skeleton fills)
- `html2pdf` (output — always seamless, never --paginated, per locked rule)
- `feedback_no_mono_in_proposals.md` (no monospace fonts in client-facing proposals)
- `feedback_design_quality_standard.md` (anti-AI-slop standards)

Both `sow-template` and `proposal-template` bake into **sales-director** agent. Optional: also marketing-director (for inbound proposal generation).
