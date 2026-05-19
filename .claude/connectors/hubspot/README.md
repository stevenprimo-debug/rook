# HubSpot connector

**Status:** stub — v1.0 ships scaffolding; auth wire-up is per-operator setup.

## Consumers
- `sales-director` (pipeline state, deal stages, contact records)
- `account-manager` (post-close account state, renewal dates, contract refs)
- `marketing-director` (campaign performance, attribution, list state)

## Credentials
- Env var: `HUBSPOT_PRIVATE_APP_TOKEN`
- Setup: HubSpot Settings → Integrations → Private Apps → create app with
  scopes: `crm.objects.contacts.read/write`, `crm.objects.deals.read/write`,
  `crm.objects.companies.read/write`, `crm.lists.read`.

## Endpoints
- Base URL: `https://api.hubapi.com`
- Auth: `Authorization: Bearer <private_app_token>`
- Common methods:
  - `GET /crm/v3/objects/deals?properties=...` — list deals
  - `PATCH /crm/v3/objects/deals/<id>` — update deal stage / properties — **N**
  - `GET /crm/v3/objects/contacts/<id>` — read contact
  - `POST /crm/v3/objects/contacts` — create contact — **N**

## Rate limits
- 100 req/10s burst, 250K req/day on Professional+
- Backoff: exponential on 429

## Reversibility class
- GET (read deals/contacts/companies): **Y**
- PATCH on deal stage: **N** — pipeline state change visible to whole team;
  requires operator confirm
- PATCH on contact properties: **Y** if internal-only fields; **N** if
  customer-visible
- DELETE: **N** — always confirm; prefer archive

## Error patterns
- `401 invalid_authentication`: token revoked or scope mismatch
- `429 too_many_requests`: hit burst — back off
- `409 conflict`: optimistic locking failed; reload + retry

## Invocation pattern

```python
from claude_connectors.hubspot import HubSpotClient

hs = HubSpotClient.from_env()

# Read (autonomous)
deals = hs.list_deals(stage="contractsent", limit=50)

# Stage change (gated)
# hs.update_deal_stage(deal_id, "closedwon")   # confirm before invoking
```

## Operator setup checklist
- [ ] HubSpot portal access (Professional+ recommended for API limits)
- [ ] Private app created
- [ ] Scopes granted
- [ ] Token stored
- [ ] Env var set
- [ ] Tested `list_deals()` returns expected data
