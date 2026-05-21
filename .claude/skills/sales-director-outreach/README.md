# Sales Director — Outreach Skill

**Parent agent:** `sales-director`
**Status:** Operational

## What it does
Drafts first-touch + follow-up outreach sequences. Subject-line testing patterns, opener variations, CTA discipline. Outputs `.eml` drafts staged for operator review — never sends. Pulls prospect context from sales-director memory + deep-researcher pre-meeting briefs when available.

## When to invoke
- `sales-director draft outreach for <prospect>`
- `sales-director write a follow-up sequence for <stage>`
- `sales-director cold email to <ICP segment>`

## Output contract
Every draft includes: subject line, opener, body, CTA, sign-off. No bullet points in client emails. Executive tone, complete sentences. Output is a draft file path — operator opens, reviews, sends manually.

## Reversibility
- DRAFT: Y (reversible — file write only)
- SEND: N (handled by inbox-manager send-gate)
