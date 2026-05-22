# `.claude/reference/contract-templates/` — shared contract & document templates

Cross-cutting legal/commercial/operational templates that ANY agent can read. Locked here per `_CLAUDE.md` § 0 rule #12 (universal context-load gate) — when sales-director, account-manager, shopify-agent, or any other agent needs an NDA, MSA, SOW, or SaaS template, it loads from THIS shelf, not from an agent-scoped duplicate.

## What's here

| Category | What it covers | When to load |
|---|---|---|
| `nda/` | Mutual + one-way NDAs, confidentiality agreements | Any new engagement before scoping discussion (sales-director, shopify-agent, r-and-d-lead) |
| `contracts/` | Software development agreements, SaaS license agreements, MSAs | Closing an engagement (sales-director, account-manager) |
| `sow/` | Statement of Work templates — professional services, SEC-flavored, generic | Scoping a defined deliverable (sales-director, account-manager) |
| `saas/` | YC-form SaaS subscription agreements | When operator-controlled SaaS product needs a master subscription (sales-director, finance-manager) |
| `partnerships/` | Partnership agreements, memoranda of agreement (placeholder — populated when first partnership lands) | Joint go-to-market or referral-share deals |

## How to use these

**Templates are STRUCTURE + PATTERN — not legal advice.** Per `feedback_no_inferring_entities.md`, do NOT carry over names, jurisdictions, or terms from the source documents. Sanitize before use:

1. Read the template to understand the structure (sections, definitions, indemnity shape, IP treatment)
2. Identify which terms need operator's actual values (entity name, jurisdiction, dollar amounts, term length)
3. Generate a draft with operator's values — flag every field that needs operator confirmation
4. Operator reviews → operator signs (legal review recommended on any agreement >$10K or that touches IP assignment)

## Reversibility class

All template generation is Y (reversible — it's just a draft file). The N gate fires when:
- The draft becomes a signed document (DocuSign/Adobe Sign envelope sent → see `.claude/connectors/docusign/` or `.claude/connectors/adobe-sign/`)
- The agreement is sent to counterparty for signature

Convention for signed documents: brand cover page + WHITE body (Times New Roman 12pt). Legal-doc bodies (contracts, NDAs, MSAs, SOWs sent for signature) use **double line spacing** for clause readability and red-line markup space.

## Cross-references

- `agents/sales-director/SKILL.md` — primary consumer; closing-mode dispatches templates
- `agents/account-manager/SKILL.md` — renewals + amendment generation
- `agents/finance-manager/SKILL.md` — reviews terms for revenue recognition + payment schedules
- `.claude/connectors/docusign/` — envelope dispatch (N — operator confirm before send)
- `.claude/connectors/adobe-sign/` — alternate signing platform

## Adding a new template category

1. `mkdir .claude/reference/contract-templates/<category>/` (e.g., `vendor-agreements/`, `nda-mutual-strict/`)
2. Drop the template `.md` file(s)
3. Update this README's table
4. The librarian sweeps the shelf into the master index on next run
