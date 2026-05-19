# SOP Skeleton (Universal — Dual-Axis Variants Inherit)

> Universal 12-section frame for Standard Operating Procedures. Variants in
> `variants/` set tone/style (rd-experiment / qa-process / business-operational
> / safety-procedure); use-cases in `use-cases/` set the process domain
> (customer-onboarding / employee-onboarding / etc.). Customer slots marked
> `{LIKE_THIS}`.
>
> **Black text** = generic boilerplate that may apply across implementations.
> **Red text** (in the rendered output) = process-specific content that MUST
> be reviewed and replaced for each context.

---

# {SOP_TITLE}

**Document Number:** {DOC_NUMBER}
**Version:** {VERSION}
**Effective Date:** {EFFECTIVE_DATE}
**Process Owner:** {PROCESS_OWNER}
**Last Reviewed:** {LAST_REVIEWED_DATE}
**Next Review:** {NEXT_REVIEW_DATE}

## 1. Purpose

{One paragraph stating WHY this SOP exists. What outcome does following this procedure produce? What goes wrong if no SOP exists?}

## 2. Scope

**Applies to:** {ROLES_OR_TEAMS this SOP governs — e.g., "All this system onboarding specialists" or "Any operator running the weekly close process"}

**Triggers on:** {WHEN this SOP fires — e.g., "A new customer signs up for the the product subscription Stack plan" or "Friday EOD, weekly"}

**Out of scope:** {What this SOP does NOT cover — directs reader elsewhere if needed}

## 3. Responsibilities

| Role | Accountability |
|---|---|
| {Role 1 — e.g., Process Leader} | {What this role owns — typically setting the SOP up, training operators, signing off on output} |
| {Role 2 — e.g., Operator} | {What this role executes — typically the step-by-step work in Section 6} |
| {Role 3 — e.g., Reviewer/Manager} | {What this role verifies — typically Acceptance criteria, quality checks, escalation routing} |

## 4. Materials & Preparation

**Required before starting:**
- {Material/access 1 — e.g., "Customer signup data exported from Shopify"}
- {Material/access 2 — e.g., "Stack admin credentials for the customer's tenant"}
- {Material/access 3}

**Recommended tools:**
- {Tool 1}
- {Tool 2}

**Pre-flight checks:**
- [ ] {Check 1}
- [ ] {Check 2}

## 5. Definitions (if any)

{Domain-specific terms used in this SOP. Define them up front so a new operator isn't guessing.}

- **{Term 1}** — {definition}
- **{Term 2}** — {definition}

## 6. Procedure

The step-by-step. Every step is atomic and verifiable. If the procedure
branches, the branch logic is explicit.

### Step 1 — {STEP_TITLE}

**Action:** {Specific action — what the operator does}

**Verification:** {Specific verification — how the operator confirms the step succeeded. "Check the system" is too vague; "Verify the dashboard shows status=green for the last 15 minutes" is right.}

**On success:** Proceed to Step 2.

**On failure:** {Specific recovery action — escalate to {role}, retry with {parameters}, etc.}

### Step 2 — {STEP_TITLE}

**Action:** {Specific action}

**Verification:** {Specific verification}

**Decision point (if applicable):**
- If {condition A}, proceed to Step 3a.
- If {condition B}, proceed to Step 3b.

### Step 3 — {STEP_TITLE}

{...continue as needed}

### Final Step — Acceptance & Sign-Off

**Acceptance criteria:** {Specific, measurable criteria for the SOP to be considered successfully completed. Example: "All Stack agents in the customer's tenant respond to a test prompt within 5 seconds, and the customer's first-run digest is generated."}

**Sign-off:** {WHO signs off + WHERE the sign-off is recorded — e.g., "Operator records completion in the operations log; Manager reviews within 24 hours"}

## 7. Decision Points & Flow Chart

{If the procedure has 3+ decision branches, reference the flow chart in Attachment A. For simpler procedures, the decision points in Section 6 suffice.}

See: `attachments/flow-chart.svg`

## 8. Training & Clearance

**Who can run this SOP:**
- {Role/credential required — e.g., "Trained this system onboarding specialist with 2+ live runs under supervision"}

**Training required:**
- {Training step 1 — e.g., "Read this SOP end-to-end"}
- {Training step 2 — e.g., "Shadow one live run before solo execution"}
- {Training step 3}

**Clearance recorded in:** {WHERE — e.g., "Training log at /memory/training-clearance.md"}

## 9. Limitations & Edge Cases

This SOP does NOT cover:
- {Edge case 1 — direct reader to alternate SOP or escalation path}
- {Edge case 2}

**Known issues:**
- {Issue 1 — workaround in the meantime}

## 10. Maintenance & Disposal

**Records to file:** {WHAT gets recorded after each run — e.g., "Run log with timestamp, operator name, customer ID, acceptance status"}

**Records retention:** {HOW LONG — e.g., "12 months in active store, then archive to cold storage for 7 years per data retention policy"}

**Disposal:** {How to securely dispose of any sensitive artifacts produced — typically not applicable for software SOPs}

## 11. References

- {Related SOP or document 1}
- {Related SOP or document 2}
- {Source documentation — manufacturer manuals, standards, regulations}

## 12. Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | {DATE} | {AUTHOR} | Initial release |

---

## Attachments

- **Attachment A:** Flow chart (decision tree visualization)
- **Attachment B:** Checklist (printable version of Section 6 steps)
- **Attachment C:** {Other attachments as needed}

---

## Slot Glossary

| Slot | Description | Example |
|---|---|---|
| `{SOP_TITLE}` | Title of the procedure | "this system — Customer Onboarding" |
| `{DOC_NUMBER}` | Tracking identifier | "OPS-001" |
| `{VERSION}` | Semver | "1.0" |
| `{PROCESS_OWNER}` | Role accountable for the SOP itself | "Head of Customer Operations" |
| `{NEXT_REVIEW_DATE}` | When SOP gets re-validated | typically 12 months from effective date |

## Variant Pattern (dual-axis)

This skeleton is variant-agnostic. The tone/style variant in
`variants/{rd-experiment | qa-process | business-operational | safety-procedure}.md`
shapes:
- Section 5 (Definitions) — sparse for business-operational, dense for rd-experiment
- Section 6 (Procedure) — narrative steps for business-operational, controlled-conditions for rd-experiment, hazard-flagged for safety-procedure
- Section 8 (Training) — light for business-operational, heavy for safety-procedure (mandatory clearance + recertification)
- Section 11 (References) — internal-only for business-operational, regulatory-citations for safety-procedure

The use-case in `use-cases/{customer-onboarding | employee-onboarding | etc.}.md`
shapes:
- Section 2 (Scope — triggers on) — domain-specific event
- Section 6 (Procedure — step sequence) — domain-specific actions
- Section 6 (Acceptance criteria) — domain-specific success state

Customer mixes one tone variant + one use-case → fills skeleton → SOP shipped.
