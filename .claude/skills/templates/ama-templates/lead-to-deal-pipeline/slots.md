# Lead-to-Deal Pipeline — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |
| `{SLACK_TEAM_CHANNEL}` | Where prospect summaries land (e.g., `#sales-pipeline`) |
| `{CALENDLY_BOOKING_LINK}` | The Calendly URL to send to prospects |
| `{HUBSPOT_DEFAULT_LIFECYCLE_STAGE}` | Stage for new contacts (typical: "Lead" or "Marketing Qualified Lead") |
| `{HUBSPOT_DEFAULT_OWNER}` | Default rep owner for new contacts (HubSpot user ID or email) |

## MCP credentials required

- apollo (API key)
- hubspot (private app token w/ contact + deal scopes)
- slack (bot token with `chat:write` on `{SLACK_TEAM_CHANNEL}`)
- calendly (API key; access to event types)

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{DEFAULT_BATCH_SIZE}` | 50 prospects per Apollo search | Yes — adjust for volume |
| `{DEDUPE_LOOKBACK_DAYS}` | 90 (don't re-prospect anyone touched in last 90 days) | Yes |
| `{CALENDLY_DELIVERY_MODE}` | "hubspot_email" (send via HubSpot) | Alt: "slack_to_rep" (DM the rep, they send manually) |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + `{CUSTOMER_SHORT_NAME}`
2. "Apollo search ICP — what industries, company sizes, titles, geographies?" → captured as default search criteria
3. "Slack channel for prospect-summary notifications?" → `{SLACK_TEAM_CHANNEL}`
4. "Calendly booking link to send to prospects?" → `{CALENDLY_BOOKING_LINK}`
5. "Default HubSpot lifecycle stage for new contacts?" → `{HUBSPOT_DEFAULT_LIFECYCLE_STAGE}`
6. "Default contact owner in HubSpot (rep email)?" → `{HUBSPOT_DEFAULT_OWNER}`
7. "Calendly delivery — send to prospect via HubSpot email, or DM the rep so they send manually?" → `{CALENDLY_DELIVERY_MODE}`
8. "MCP credentials configured for apollo + hubspot + slack + calendly?" → confirm

## Pairing with sales-triage-squad

If the customer wants BOTH outbound + inbound:
- Deploy lead-to-deal-pipeline (this one) for outbound batches
- Deploy sales-triage-squad for inbound lead handling
- Both write to the same HubSpot; deduplication across them is handled by HubSpot's contact-merge logic

Customer pays Anthropic for both AMAs' session-hours separately; this system
subscription covers the templates themselves.
