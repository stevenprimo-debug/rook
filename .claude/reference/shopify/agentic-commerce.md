---
title: Agentic commerce
source: https://shopify.dev/docs/agents
author: []
published: []
created: 2026-05-11
description: Learn how to build AI agents that can search hundreds of millions of Shopify products, manage universal carts across multiple merchants, and deliver seamless checkout experiences using the Shopify Catalog MCP server and web components.
tags: [clippings]
---

![UCP logo](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/agents/ucp_logo_dark-DUGx5m5X.svg)

## Anchor to The Universal Commerce ProtocolThe Universal Commerce Protocol

The [Universal Commerce Protocol (UCP)](https://ucp.dev/documentation/core-concepts/) is an open standard that establishes a common language and a set of primitives that allow agents, merchants, Payment Service Providers (PSPs), and Credential Providers (CPs) to communicate consistently and securely across the web.

Shopify provides MCP tools that are UCP-compliant to build with this interoperable and extensible protocol.

[View the spec](https://ucp.dev/2026-04-08/specification/overview/)

## Anchor to How Shopify does UCPHow Shopify does UCP

UCP defines how agents, merchants, credential providers, and payment service providers work together across the commerce lifecycle.

Shopify provides MCP tools that implement UCP's core capabilities:

- **Discovery**: Search products across the Shopify platform and surface results buyers can act on.
- **Cart**: Build and iterate on carts with line items, localization, and buyer context.
- **Checkout**: Convert carts into checkout sessions, collect buyer information, and complete purchases.

![Discovery, cart, and checkout flow](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/agents/ucp-flow-BGvvWUNh.png)

Discovery, cart, and checkout flow

## Anchor to Build your commerce flowBuild your commerce flow

Combine Shopify MCP tools at each step of the buyer journey. Negotiate access with a profile, help buyers discover products across Shopify, then build carts and checkouts that move them from intent to purchase.

Define a profile so Shopify can verify your agent and apply the right rate limits and tool access. Higher trust tiers unlock broader access, including direct checkout completion.

![Agent negotiation and authentication](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/agents/agentsUCPdark-CEbsjwWb.png)

Agent negotiation and authentication

Query products across all Shopify merchants and surface results buyers can interact with. When buyers pick a product, fetch the variant details you need to build a cart or checkout.

![Catalog overview](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/agents/catalog-DdJdITex.png)

Catalog overview

Build carts as buyers iterate. Add line items, apply localization, and estimate totals.

When buyers are ready, convert the cart to a checkout and refer them to the merchant storefront to complete payment. Trusted agents can complete checkouts directly.

![Checkout overview](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/agents/zoomedcheckout-DxucSVFn.png)

Checkout overview

---
