# Shopify Agent Reference Pack

> **Domain:** Shopify platform — admin / theme / app dev / Polaris / App Bridge / Functions / agentic commerce  
> **Verified:** 2026-05 — all URLs live and confirmed against official first-party docs  
> **Source quality:** All entries are official Shopify first-party documentation (shopify.dev, polaris.shopify.com)

---

## 1. Agentic Commerce — Universal Commerce Protocol (UCP)

**URL:** https://shopify.dev/docs/agents  
**Type:** Official developer documentation — canonical landing page  
**Recency:** Current (2026); newly launched platform surface

### What it covers
The authoritative developer entry point for building AI shopping agents on Shopify using the **Universal Commerce Protocol (UCP)** — Shopify's open standard co-developed with Google, also supporting REST, MCP (Model Context Protocol), Agent Payments Protocol (AP2), and Agent2Agent (A2A).

The page organises the full agent buyer journey into four capabilities:

| Capability | Description |
|---|---|
| **Negotiate & authenticate** | Define agent profiles hosted at a well-known URL; capability negotiation and trust-tier assignment (higher tiers unlock direct checkout completion) |
| **Discover products** | Global Catalog (`catalog.shopify.com/api/ucp/mcp`) searches hundreds of millions of listings across all merchants; Storefront Catalog (`{storeDomain}/api/ucp/mcp`) scopes to a single store |
| **Carts & checkout** | Cart MCP for multi-turn cart building (line items, localization, totals); Checkout MCP to convert carts and hand off to payment or complete directly |
| **Monitor orders** | UCP-shaped webhooks for fulfillment, refunds, returns, exchanges; `get_order` MCP tool for on-demand order state |

**Why essential:** This is the ground-truth entry point for any agent that touches Shopify commerce end-to-end. It defines the authentication model, rate limits, trust tiers, and all MCP tool signatures.

**Related:** Catalog detail page — https://shopify.dev/docs/agents/catalog

---

## 2. Shopify Admin GraphQL API

**URL:** https://shopify.dev/docs/api/admin-graphql  
**Type:** Official API reference — canonical landing page  
**Current version:** 2026-04

### What it covers
The primary programmatic interface for reading and mutating all Shopify store data from app backends. All requests require an OAuth-issued `X-Shopify-Access-Token` header.

| Detail | Value |
|---|---|
| **Endpoint** | `POST https://{store}.myshopify.com/admin/api/2026-04/graphql.json` |
| **Auth** | OAuth access token (`X-Shopify-Access-Token`) |
| **Rate limiting** | Cost-based (calculated query cost in points) |
| **Versioning** | Quarterly (January, April, July, October) |
| **Explorer tool** | Shopify GraphiQL app |

**Why essential:** Nearly every app that reads or writes shop data (products, orders, customers, inventory, metafields, discounts, fulfillment, B2B) uses this API. Understanding its cost-based rate limits and OAuth scopes is foundational.

---

## 3. Storefront API

**URL:** https://shopify.dev/docs/api/storefront  
**Type:** Official API reference — canonical landing page  
**Current version:** 2026-04

### What it covers
GraphQL API for building custom storefronts, headless commerce, and AI-powered shopping agents. Exposes product/collection discovery, cart management, checkout, and customer accounts.

| Detail | Value |
|---|---|
| **Endpoint** | `POST https://{store}.myshopify.com/api/2026-04/graphql.json` |
| **Auth** | Tokenless (complexity ≤ 1,000) or public/private Storefront API token |
| **Framework** | Hydrogen (React-based headless commerce) |
| **Rate limiting** | Real buyer traffic: no fixed rpm limit; bots/automated: rate-limited; Web Bot Auth required for higher limits |
| **Versioning** | Quarterly |

**Key distinction from Admin API:** No write access to store admin data — purpose-built for buyer-facing frontends. The Storefront MCP endpoint (`/api/ucp/mcp`) is the UCP-native equivalent for agent scenarios.

**Why essential:** Powers all custom storefront, headless, and agentic product discovery / cart / checkout use cases. The Storefront Catalog MCP for agents is built on top of this surface.

---

## 4. Shopify Functions — Function APIs

**URL:** https://shopify.dev/docs/api/functions  
**Type:** Official API reference — canonical landing page

### What it covers
Shopify Functions allow developers to run custom backend logic within the Shopify checkout pipeline, compiled to **WebAssembly (WASM)**. Rust is the strongly preferred language; any language that targets Wasm is supported.

**Function execution order in checkout:**
1. Cart-price and presentation functions (cart transforms, B2B pricing)
2. Discount calculation functions
3. Cart/checkout validation functions

**Available extension target types** (selected):

| Function API | Use case |
|---|---|
| Cart Transform | Rewrite line items, bundles, custom pricing |
| Discount | Automatic and code-based discount logic |
| Payment Customization | Hide/reorder/rename payment methods |
| Delivery Customization | Custom shipping rates and rules |
| Order Routing | Fulfillment location routing logic |
| Cart & Checkout Validation | Block checkout based on custom rules |

**Resource limits (≤200 line items):**

| Resource | Limit |
|---|---|
| Compiled binary | 256 kB |
| Execution instructions | 11 million |
| Input | 128 kB |
| Output | 20 kB |
| Runtime linear memory | 10,000 kB |

**Availability:** All plans for App Store public apps; Shopify Plus only for custom apps.

**Why essential:** The only way to customize Shopify checkout business logic (discounts, validation, delivery, payment). Critical for any app that extends checkout.

---

## 5. Polaris Design System

**URL:** https://polaris.shopify.com  
**Type:** Official design system — canonical landing page

### What it covers
Polaris is Shopify's design system for building the **merchant admin experience**. It defines the visual language, interaction patterns, and component library used across the Shopify admin and all embedded apps.

| Category | Description |
|---|---|
| **Foundations** | Design principles, accessibility, motion, spacing, typography guidance for quality admin UIs |
| **Components** | 100+ reusable React components (`@shopify/polaris`) — Button, DataTable, Modal, ResourceList, etc. |
| **Tokens** | Design tokens representing color, spacing, and typography decisions (CSS custom properties) |
| **Icons** | 400+ commerce-focused SVG icons (`@shopify/polaris-icons`) |

**Key architectural note (2025-10+):** Admin UI extensions migrated from React-based Polaris components to **native web components** in API version 2025-10. App surfaces (app home) still use Polaris React directly; App Bridge web components handle admin chrome (nav, title bar, save bar).

**Why essential:** Any app that renders UI in the Shopify admin must follow Polaris guidelines to pass App Store review. It defines the entire visual contract for embedded apps.

---

## 6. Shopify App Bridge

**URL:** https://shopify.dev/docs/api/app-bridge  
**Type:** Official API reference — canonical landing page

### What it covers
App Bridge is the SDK that enables **embedded apps to communicate with and render UI within the Shopify admin** host. It acts as a bridge between the app's iframe (web) or WebView (mobile) and the Shopify admin shell.

| Environment | Rendering method |
|---|---|
| Web browser | iframe |
| Shopify mobile app | WebView |

**Core App Bridge capabilities:**

| Capability | Description |
|---|---|
| Navigation menu | Render a left-nav menu inside the Shopify admin |
| Title bar | Render a title bar with primary/secondary actions |
| Save bar | Render a save/discard bar above the top bar |
| Session tokens | Authenticate embedded app requests using signed JWTs |

**Architecture:** App Bridge components are React-like wrappers around JavaScript messages. The Shopify admin performs the actual UI rendering — apps do not render admin chrome themselves.

**Latest version:** Vanilla JavaScript / web components API (invoked via standard JS functions). The `@shopify/app-bridge-react` package provides React wrappers.

**Why essential:** Every embedded Shopify app must use App Bridge for authentication (session tokens) and admin surface integration. It is the foundational SDK for the embedded app model.

---

## 7. Liquid Template Language Reference

**URL:** https://shopify.dev/docs/api/liquid  
**Type:** Official language reference — canonical landing page

### What it covers
The complete reference for **Liquid**, Shopify's open-source template language used to build all Shopify themes. This reference specifically covers the **Shopify-extended variant** of Liquid used in Online Store themes.

**Language fundamentals:**

| Feature | Syntax |
|---|---|
| Output | `{{ variable }}` |
| Logic/Tags | `{% tag %}` |
| Filters | `{{ value \| filter_name }}` |
| Variable assignment | `{% assign %}`, `{% capture %}` |

**Reference scope:**
- **Tags** — control flow (`if`, `for`, `unless`, `case`), iteration, HTML output
- **Filters** — string, array, math, URL, color, money, date manipulation (100+ filters)
- **Objects** — all Shopify theme objects: `product`, `collection`, `cart`, `customer`, `shop`, `request`, `theme`, `settings`, `content_for_header`, and more

**Scope:** Covers theme Liquid only — _not_ notification templates, Shopify Flow, or Order Printer Liquid variants.

**Why essential:** Liquid is the only way to build or modify Shopify themes. Every `.liquid` file in a theme (layouts, templates, sections, snippets) uses this language.

---

## 8. Theme Architecture — Online Store 2.0

**URL:** https://shopify.dev/docs/storefronts/themes/architecture  
**Type:** Official developer documentation — canonical landing page

### What it covers
The definitive reference for Shopify's **Online Store 2.0 theme architecture** — the modern theme system introduced in 2021 that replaced legacy monolithic themes with a section-everywhere, JSON-template model.

**Theme directory structure:**

```
assets/          # Images, CSS, JS files
blocks/          # Reusable block definitions
config/          # settings_schema.json, settings_data.json
layout/          # theme.liquid (required), password.liquid
locales/         # Translation JSON files
sections/        # Section .liquid files + section group JSON
snippets/        # Reusable Liquid code fragments
templates/       # JSON templates (section wrappers) or Liquid templates
  customers/     # Account pages
  metaobject/    # Metaobject page templates
```

**Page composition model:**

| Component | Role |
|---|---|
| Layout (`.liquid`) | Persistent shell — `<head>`, header/footer section groups |
| Template (`.json` or `.liquid`) | Page-type controller — wraps sections for each page type |
| Section groups (`.json`) | Containers for sections outside templates (header, footer) |
| Sections (`.liquid`) | Reusable, merchant-customizable content modules |
| Blocks | Nested, reorderable content units within sections |
| Snippets (`.liquid`) | Non-merchant-visible reusable Liquid partials |

**Key OS 2.0 capabilities:**
- JSON templates act as section wrappers — merchants can add/remove/reorder sections on any page type
- Every section and block exposes a `{% schema %}` JSON tag defining merchant-customizable settings
- `settings_schema.json` defines theme-wide settings accessible via the `{{ settings }}` object
- JSON files in `templates/`, section groups, and `settings_data.json` do **not** persist comments or trailing commas

**Why essential:** Understanding this architecture is required for building, modifying, or reviewing any Shopify theme. It defines how every page is assembled and how the theme editor works.

---

## 9. Shopify AI Toolkit (Dev MCP Server)

**URL:** https://shopify.dev/docs/apps/build/ai-toolkit  
**Type:** Official developer tooling documentation

### What it covers
The **Shopify AI Toolkit** connects AI coding assistants (Claude Code, Cursor, VS Code, Gemini CLI, Codex) to the Shopify developer platform — giving AI agents access to official Shopify docs, API schemas, and code validation tools.

**Three installation modes:**

| Mode | Description |
|---|---|
| Plugin (recommended) | Auto-updating bundle; available for Claude Code, Cursor, Gemini CLI, VS Code |
| Agent Skills | Individual skill files for specific capabilities (e.g., GraphQL Admin API skill); manual updates |
| Dev MCP Server | Local MCP server (`@shopify/dev-mcp`) providing docs + API schema access; no auth required |

**Dev MCP Server quick setup (any MCP-compatible agent):**
```json
{
  "mcpServers": {
    "shopify-dev-mcp": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"]
    }
  }
}
```

**Capabilities exposed:**
- Shopify documentation search
- Admin GraphQL API schema access
- Hydrogen / Storefront API references
- Code validation for Shopify-specific patterns
- CLI `store execute` for store management operations

**Why essential:** This is the official tool for grounding a `shopify-agent` AI system in accurate, current Shopify knowledge. Using `@shopify/dev-mcp` avoids hallucinated API syntax and ensures the agent works with the actual current schema.

---

## Summary Table

| # | Source | URL | Domain | Recency |
|---|---|---|---|---|
| 1 | Agentic Commerce (UCP) | https://shopify.dev/docs/agents | shopify.dev | 2026 — newly launched |
| 2 | Admin GraphQL API | https://shopify.dev/docs/api/admin-graphql | shopify.dev | 2026-04 (current) |
| 3 | Storefront API | https://shopify.dev/docs/api/storefront | shopify.dev | 2026-04 (current) |
| 4 | Shopify Functions | https://shopify.dev/docs/api/functions | shopify.dev | Current |
| 5 | Polaris Design System | https://polaris.shopify.com | polaris.shopify.com | Current (web components 2025-10+) |
| 6 | App Bridge | https://shopify.dev/docs/api/app-bridge | shopify.dev | Current |
| 7 | Liquid Reference | https://shopify.dev/docs/api/liquid | shopify.dev | Current |
| 8 | Theme Architecture (OS 2.0) | https://shopify.dev/docs/storefronts/themes/architecture | shopify.dev | Current |
| 9 | Shopify AI Toolkit / Dev MCP | https://shopify.dev/docs/apps/build/ai-toolkit | shopify.dev | 2025-2026 |

---

## Supplementary / Deep-Dive Links

These are verified sub-pages worth indexing for deeper reference:

| Resource | URL |
|---|---|
| Shopify Dev Hub (home) | https://shopify.dev |
| Build a Storefront AI Agent (tutorial) | https://shopify.dev/docs/apps/build/storefront-mcp/build-storefront-ai-agent |
| Agentic Commerce — Catalog reference | https://shopify.dev/docs/agents/catalog |
| Global Catalog MCP | https://shopify.dev/docs/agents/catalog/global-catalog |
| Storefront Catalog MCP | https://shopify.dev/docs/agents/catalog/storefront-catalog |
| App Home / App Bridge APIs | https://shopify.dev/docs/api/app-home |
| Admin UI Extensions (web components) | https://shopify.dev/docs/api/admin-extensions |
| Polaris React npm (`@shopify/polaris`) | https://www.npmjs.com/package/@shopify/polaris |
| Hydrogen (headless React framework) | https://shopify.dev/docs/storefronts/headless/hydrogen |
| Shopify CLI reference | https://shopify.dev/docs/api/shopify-cli |
| Functions — Discount API | https://shopify.dev/docs/api/functions/reference/discount |
| Functions — Cart Transform API | https://shopify.dev/docs/api/functions/reference/cart-transform |
| Shopify Changelog | https://shopify.dev/changelog |
| UCP Spec (open standard, co-developed with Google) | https://ucp.dev |
| Agentic Commerce — news/announcement | https://www.shopify.com/news/ai-commerce-at-scale |
