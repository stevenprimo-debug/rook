# Cold Outreach Personalizer — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |
| `{MAILERLITE_SEQUENCE_ID}` | Target MailerLite automation/sequence to trigger per prospect |
| `{CLAY_TABLE_ID}` | Clay table where enrichment records land |

## MCP credentials required

- apollo (API key)
- clay (API key + table access)
- mailerlite (API key + automation/sequence access)

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{FIRST_LINE_MAX_WORDS}` | 25 (per system prompt) | Yes — stricter for some campaigns |
| `{INSUFFICIENT_DATA_THRESHOLD}` | "fewer than 2 verifiable details" | Yes — adjust strictness |
| `{VOICE_NOTES}` | "Conversational, not salesy. Anchor to specific verifiable detail." | Strong recommend: dispatch CD first to lock voice |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + `{CUSTOMER_SHORT_NAME}`
2. "MailerLite sequence ID to trigger per prospect?" → `{MAILERLITE_SEQUENCE_ID}`
3. "Clay table ID for enrichment records?" → `{CLAY_TABLE_ID}`
4. "Has CREATIVE DIRECTOR been dispatched to lock voice? (Strong recommend.)" → if N, offer to spawn CD subagent first
5. "First line max word count — 25 default or stricter?" → `{FIRST_LINE_MAX_WORDS}`
6. "MCP credentials configured for apollo + clay + mailerlite?" → confirm

## Composability with other sales AMAs

Two compositions worth knowing:

**Composition A (full outbound stack):**
1. lead-to-deal-pipeline runs Apollo search + HubSpot creation
2. cold-outreach-personalizer enriches via Clay + writes personalized first lines + triggers MailerLite

**Composition B (lean MailerLite-only stack):**
1. Customer uploads prospect CSV to Clay manually
2. cold-outreach-personalizer pulls from Clay + writes first lines + triggers MailerLite (skip HubSpot entirely)

Customer picks composition based on their CRM stack.

## Upstream dispatch chain

Per `dispatch_chains.MARKETING`: CREATIVE DIRECTOR → MARKETING → sales-director
deploys this AMA. CD locks brand voice for the first lines; MARKETING
validates funnel + audience fit; sales-director runs the deployment.
