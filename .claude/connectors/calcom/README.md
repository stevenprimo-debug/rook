# Cal.com connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (no MCP).
**ROOK scheduling standard:** This is the canonical booking/scheduling layer for ROOK-deployed agents. Branded as the operator's scheduling rail; cohort customers using ROOK inherit Cal.com as the default.

## Consumers
- `account-manager` (client meeting booking, follow-up scheduling)
- `chief-of-staff` (operator calendar coordination)
- `inbox-manager` (booking-link insertion in outbound email drafts)
- `sales-director` (discovery-call scheduling on cold outreach)
- `social-media-manager` (community office-hours booking from DMs)

## Integration kind
API-direct (Cal.com REST API v2). Cal.com offers webhooks for inbound events (booking created, cancelled, rescheduled) — wire those into `inbox-manager` for confirmation handling.

## Credentials
- `CALCOM_API_KEY` — generated from Cal.com → Settings → Developer → API Keys
- Stored at `~/.claude/credentials/calcom.json` OR PowerShell profile env var
- Optional: `CALCOM_BASE_URL` (defaults to `https://api.cal.com/v2`) for self-hosted Cal.com instances

## Reversibility class
- **Y (reversible)**: list event types, list bookings, get availability, list users
- **N (irreversible)**: create booking, cancel booking, reschedule booking, send confirmation email, delete event type

Agents NEVER invoke N-class operations without explicit operator confirm.

## Operator setup checklist
- [ ] Cal.com account created (free tier works for v1; Team plan for shared availability)
- [ ] API key generated at https://app.cal.com/settings/developer/api-keys
- [ ] Stored at `~/.claude/credentials/calcom.json` OR env var `CALCOM_API_KEY` set
- [ ] At least one event type configured (15-min discovery, 30-min consult, etc.)
- [ ] Tested with `GET /event-types` before any write
- [ ] Webhook endpoint configured (if using inbox-manager booking confirmation flow)
- [ ] `client.py` implemented against this README (template at `.claude/connectors/perplexity/client.py`)

## Branding note (ROOK-deployed)
When `account-manager` or `chief-of-staff` shares a booking link in client comms, the link format should be `cal.com/<operator-handle>/<event-slug>` — the Cal.com brand is acceptable here (operator's professional booking tool). Do NOT attempt to vanity-domain Cal.com bookings unless the operator has explicitly configured a custom domain (Team plan feature).

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
