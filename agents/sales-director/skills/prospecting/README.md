# Sales Director — Prospecting Skill

**Parent agent:** `sales-director`
**Status:** Operational

## What it does
Defines ICP segments, builds prospect lists from connectors (ZoomInfo when available, manual research otherwise), enriches contacts with role + recent-activity signals, scores against ICP fit before they enter outreach.

## When to invoke
- `sales-director build a prospect list for <segment>`
- `sales-director enrich this contact list`
- `sales-director score this lead against ICP`

## Output contract
Structured CSV or markdown table: name, title, company, score, last-activity-signal, recommended outreach angle. Never auto-pushes to CRM — operator reviews + decides which to import.

## Reversibility
- LIST BUILD: Y (output is a file)
- CRM IMPORT: N (operator-confirm required; usually done in CRM UI directly)
