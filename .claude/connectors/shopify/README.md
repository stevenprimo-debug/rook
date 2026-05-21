# Shopify connector

**Status:** stub — v1.0 ships scaffolding; auth wire-up is per-operator setup.

## Consumers
- `shopify-agent` (theme work, app integration, customer flows, admin scripts)
- `account-manager` (read store state for accounts that have a Shopify store)

## Credentials

Two auth modes — Custom App (preferred for single-operator use) or Public App
(for marketplace distribution).

### Custom App (preferred)
- Env var: `SHOPIFY_ADMIN_API_ACCESS_TOKEN`
- Env var: `SHOPIFY_STORE_DOMAIN` (e.g., `mystore.myshopify.com`)
- Setup: Shopify Admin → Apps → Develop apps → Create custom app → grant
  scopes → install on store → copy admin API access token.

### Public App (marketplace)
- Env var: `SHOPIFY_API_KEY`
- Env var: `SHOPIFY_API_SECRET`
- OAuth2 flow for per-merchant install.

## Endpoints
- Base URL: `https://<shop>.myshopify.com/admin/api/2024-01`
- Auth: `X-Shopify-Access-Token: <token>`
- Common methods:
  - `GET /products.json` — list products
  - `GET /orders.json?status=any` — list orders
  - `POST /products.json` — create product — **N**
  - `PUT /products/<id>.json` — update product — **N**
  - `POST /themes/<theme_id>/assets.json` — write theme file — **N**

## GraphQL alternative
- Endpoint: `POST /api/2024-01/graphql.json`
- Preferred for nested reads (avoids waterfall REST calls)

## Rate limits
- REST: 2 calls/sec per store (Plus: 4)
- GraphQL: cost-based, 50 points/sec bucket
- Backoff: respect `X-Shopify-Shop-Api-Call-Limit` header

## Reversibility class
- GET (read products / orders / customers / themes): **Y**
- POST/PUT on product, order, customer, theme: **N** — store-visible change;
  confirm before invoking
- DELETE: **N** — always confirm
- App / theme installation: **N**

## Multi-store note (multi-client engagements)

When the operator runs multiple Shopify engagements (the client + other client
sites), each store needs its own credentials block. Convention:

```
~/.claude/credentials/shopify/
  ├── client-store.json
  ├── client-2.json
  └── client-3.json
```

The connector loads the matching credential block based on the active engagement
context. `account-manager` reads the engagement-to-store mapping from
`accounts/<client>/shopify.md`.

## Error patterns
- `401 Unauthorized`: token revoked, scope missing, or store domain wrong
- `402 Payment Required`: store unpaid — surface to operator
- `429 Too Many Requests`: rate limited — back off
- `423 Locked`: store closed or fraud-flagged

## Operator setup checklist
- [ ] Shopify Partners account
- [ ] Custom app created per store
- [ ] Scopes granted (products, orders, customers, themes, content as needed)
- [ ] Token stored per-store
- [ ] Env vars set or per-store credential file in place
- [ ] Tested `list_products()` against each store
