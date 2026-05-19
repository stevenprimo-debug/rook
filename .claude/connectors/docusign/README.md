# DocuSign connector

**Status:** stub — v1.0 ships scaffolding; auth wire-up is per-operator setup.

## Consumers
- `sales-director/skills/closing` (send contracts for signature)
- `account-manager` (read contract state, surface signed vs pending)

## Credentials
- Env var: `DOCUSIGN_INTEGRATION_KEY`
- Env var: `DOCUSIGN_USER_ID`
- Env var: `DOCUSIGN_ACCOUNT_ID`
- Env var: `DOCUSIGN_PRIVATE_KEY_PATH` (path to RSA private key)
- Setup: DocuSign Admin → Apps & Keys → create integration → JWT grant flow →
  consent grant on first connection.

## Endpoints
- Base URL: `https://demo.docusign.net/restapi/v2.1` (sandbox)
  or `https://www.docusign.net/restapi/v2.1` (production)
- Auth: JWT bearer token (per request; cache for 1h)
- Common methods:
  - `POST /accounts/<account_id>/envelopes` — create + send envelope — **N**
  - `GET /accounts/<account_id>/envelopes/<id>` — read envelope state
  - `GET /accounts/<account_id>/envelopes/<id>/documents/combined` — download
    signed PDF

## Rate limits
- 1K envelopes/hr per account (production)
- API: 300 req/min burst
- Backoff: exponential on 429

## Reversibility class
- GET (read envelope state, list envelopes, download signed docs): **Y**
- `POST /envelopes` with `status: created`: **Y** — saved as draft, not sent
- `POST /envelopes` with `status: sent`: **N** — counterparty receives email;
  ALWAYS confirm before invoking
- `PUT /envelopes/<id>` with `status: voided`: **N** — counterparty sees void
- Webhook setup: **N** — modifies external state

## Operator setup checklist
- [ ] DocuSign developer or production account
- [ ] Integration key created
- [ ] JWT consent granted (one-time per user)
- [ ] Private key generated + stored
- [ ] Env vars set
- [ ] Tested envelope creation in `status: created` (no send) first
- [ ] Production env only after sandbox verification

## Account-manager handoff

When sales-director/closing sends an envelope, account-manager subscribes to
the envelope's status changes (via webhook or polling) and surfaces signed
status into the account's record. The signed PDF lands in
`accounts/<client>/contracts/<YYYY-MM-DD>-<envelope-id>.pdf`.
