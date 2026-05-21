# Cal.com API v2 — agent-facing reference

**Status:** stub — verify against https://cal.com/docs/api-reference on first connector use.
**Base URL:** `https://api.cal.com/v2`

## Authentication

Header: `Authorization: Bearer <CALCOM_API_KEY>`
API version pinning: `cal-api-version: 2024-08-13` (or current as of first-use date)

## Endpoints

| Endpoint | Method | Purpose | Reversibility |
|---|---|---|---|
| `/event-types` | GET | List operator's event types | Y |
| `/event-types/{id}` | GET | Read one event type | Y |
| `/event-types` | POST | Create event type | N |
| `/event-types/{id}` | PATCH | Update event type | N |
| `/event-types/{id}` | DELETE | Delete event type | N |
| `/slots` | GET | Get available time slots for an event type | Y |
| `/bookings` | GET | List bookings (filter by status, date range) | Y |
| `/bookings/{uid}` | GET | Read one booking | Y |
| `/bookings` | POST | Create booking | **N** (sends confirmation email) |
| `/bookings/{uid}/cancel` | POST | Cancel booking | **N** (sends cancellation email) |
| `/bookings/{uid}/reschedule` | POST | Reschedule booking | **N** |
| `/me` | GET | Read authenticated user profile | Y |
| `/schedules` | GET | List availability schedules | Y |

## Webhooks (inbound, consumed by inbox-manager)

| Event | Payload | Action |
|---|---|---|
| `BOOKING_CREATED` | booking object | inbox-manager sends prep email; calendar event auto-created |
| `BOOKING_CANCELLED` | booking object | inbox-manager sends acknowledgement; if internal, archive thread |
| `BOOKING_RESCHEDULED` | new booking object | inbox-manager sends updated confirmation |
| `MEETING_ENDED` | booking object | account-manager fires follow-up draft (N — confirm before send) |

Configure webhooks at https://app.cal.com/settings/developer/webhooks. Target the operator's inbox-manager inbound endpoint.

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 200 / 201 | OK | proceed |
| 400 | Bad request — invalid event-type ID, slot already taken | surface to operator, do NOT retry blindly |
| 401 | API key invalid / expired | re-auth via env var refresh |
| 403 | Insufficient permission (Team plan feature on Free plan) | check plan tier |
| 404 | Booking / event type not found | confirm UID with operator |
| 429 | Rate limit (60 req/min on free tier) | exponential backoff 2s, 4s, 8s |
| 500-599 | Cal.com server side | exponential backoff, fall back to direct calendar invite |

## Reversibility per endpoint

All `POST` / `PATCH` / `DELETE` operations are N (external state change — emails sent, calendar invites created, customer receives notification). Agents stage these as drafts and require operator confirm before executing.

Reads (`GET /event-types`, `GET /slots`, `GET /bookings`) are Y — agents invoke autonomously.

## Notes for first-use

When the consuming agent invokes this connector for the first time:
1. Verify the live API docs at https://cal.com/docs/api-reference
2. Update endpoint table with the calls you actually need
3. Confirm operator's plan tier supports your endpoints (some are Team-plan-only)
4. Implement `client.py` using `.claude/connectors/perplexity/client.py` as the pattern
5. Smoke test: `GET /me` should return operator profile
6. Wire webhook endpoint to inbox-manager before any booking-creation call goes live
