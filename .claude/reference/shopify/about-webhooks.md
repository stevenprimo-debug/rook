---
title: About webhooks
source: https://shopify.dev/docs/apps/build/webhooks
author: []
published: []
created: 2026-05-11
description: Use event data delivered through webhooks to stay in sync with Shopify or execute code after a specific event occurs in a shop.
tags: [clippings]
dept_secondary: [SOFTWARE DEV]
---

When your app needs information about specific events that have occurred on a shop, it can subscribe to Shopify webhook topics as a mechanism for receiving near-real-time data about these events.

Shopify webhooks are useful for keeping your app in sync with Shopify data, or as a trigger to perform an additional action after that event has occurred. They're also a performant alternative to continuously polling for changes to a shop's data.

This guide provides a quick primer on when to use APIs versus webhooks, as well as key terminology and behaviors that are specific to Shopify webhooks.

### Anchor to Examples of when your app might use webhooksExamples of when your app might use webhooks

- Sending notifications about changes in inventory levels to inventory management clients and pagers
- Informing shipping companies about changes in orders, returns, or refunds
- Removing customer data from a database for app uninstalls
- Integrating data about orders with accounting software
- Updating a product's warranty price based on changes to the product's price

---

## Anchor to APIs for continuous polling vs. webhooks for events dataAPIs for continuous polling vs. webhooks for events data

The following example uses the `orders/create` webhook topic to illustrate the difference between polling an API for data about events, versus subscribing to a webhook topic to receive data about events.

![Diagram showing how webhooks work compared to continuous polling](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/how-webhooks-work-Dhi08wMg.png)

Diagram showing how webhooks work compared to continuous polling

1. The app subscribes to the `orders/create` topic for a shop and listens for order creation events.
2. The app specifies an endpoint to receive webhooks for the `orders/create` topic. For example, this might be an HTTPS endpoint hosted by the app server. This endpoint is where the app listens for webhooks.
3. Suppose now that an order is created from that shop.
4. This triggers a webhook to be published to the `orders/create` topic.
5. Shopify sends that webhook, which includes headers and an order payload, to the specified subscription endpoint.

---

## Anchor to Key terminologyKey terminology

### Anchor to Webhook topicWebhook topic

Webhooks are organized into topics. Your app subscribes to one or more topics to receive webhooks. After installed on a shop, your app receives webhooks each time that type of event is triggered for that shop.

The **webhook topic** defines the kind of event messages that your app receives. For example, your app can subscribe to the `products/create` topic to be notified about new products that are created. The topic name identifies the nature of the event that's occurred.

Info

Webhooks are divided by topic. Refer to the [Webhooks references](https://shopify.dev/docs/api/webhooks) for the complete list of supported webhook topics.

### Anchor to Webhook subscriptionWebhook subscription

A **webhook subscription** declares the app's intention to receive webhooks for a topic. A subscription is defined by:

- The topic name
- The subscription endpoint
	The endpoint is the destination that Shopify sends the webhooks to. This can be either a cloud-based event bus, or HTTPS. Today, Shopify provides support for, and is integrated with, Google Pub/Sub and Amazon EventBridge. Shopify recommends using Google Pub/Sub whenever possible.

Each webhook is made up of **headers** and a **payload**. Headers contain metadata about the webhook, like the shop that the app was installed on and where the event occurred.

X-Shopify-Topic: \`orders/create\`

X-Shopify-Hmac-Sha256: \`XWmrwMey6OsLMeiZKwP4FppHH3cmAiiJJAweH5Jo4bM=\`

X-Shopify-Shop-Domain: \`{shop}.myshopify.com\`

X-Shopify-API-Version: \`2026-04\`

X-Shopify-Webhook-Id: \`b54557e4-bdd9-4b37-8a5f-bf7d70bcd043\`

X-Shopify-Triggered-At: \`2023-03-29T18:00:27.877041743Z\`

X-Shopify-Event-Id: \`98880550-7158-44d4-b7cd-2c97c8a091b5\`

X-Shopify-Name: \`{developer-supplied-subscription-name}\`

Caution

Like all HTTP headers, webhook header names are case-insensitive. Your app can break if it relies on a particular casing. For example, your app might receive `X-Shopify-Topic`, `x-shopify-topic`, or `X-shopify-topic` (or any other casing) and should treat them interchangeably.

Every Shopify webhook includes the following headers. Some topics may have additional headers containing more context, and some headers are optional depending on subscription configuration.

| Header | What it is |
| --- | --- |
| `X-Shopify-Topic` | The name of the topic. Use the webhooks references to match this to the enum value when configuring webhook subscriptions using the GraphQL Admin API. |
| `X-Shopify-Hmac-Sha256` | Verification, when using HTTPS delivery. |
| `X-Shopify-Shop-Domain` | Identifying the associated store. Especially useful when configuring webhook subscriptions using the GraphQL Admin API. |
| `X-Shopify-Webhook-Id` | Identifying unique webhooks. |
| `X-Shopify-Triggered-At` | Identifying the date and time when Shopify triggered the webhook. |
| `X-Shopify-Event-Id` | Identifying the event that occurred. |
| `X-Shopify-Name` (Optional) | Developer-supplied subscription name. Especially useful to differentiate multiple subscriptions to the same topic. |

Caution

When you're using Google Cloud Pub/Sub or Amazon EventBridge for delivery of your webhooks, you receive a JSON payload for topics, but there are additional fields included beyond the sample payloads displayed in the [Webhooks reference](https://shopify.dev/docs/api/webhooks).

---

## Anchor to What to expect when working with Shopify event dataWhat to expect when working with Shopify event data

Below are some key things to remember when working with Shopify event data and webhooks.

### Anchor to Ordering event dataOrdering event data

As with other webhook systems, Shopify doesn't guarantee ordering within a topic, or across different topics for the same resource. For example, it's possible that a `products/update` webhook might be delivered before a `products/create` webhook.

Shopify recommends using timestamps provided in the header (`X-Shopify-Triggered-At`) or in the payload itself (`updated_at`) to organize webhooks.

### Anchor to Working with versionsWorking with versions

The header `X-Shopify-API-Version` specifies which version of the GraphQL Admin API was used to serialize the webhook event payload.

If an app is set to use an API version that's no longer supported, then Shopify falls forward to use the oldest supported version.

You can learn more about [configuring your app to use a specific API version for all webhook subscriptions](https://shopify.dev/docs/apps/build/webhooks/subscribe/use-newer-api-version).

### Anchor to Handling duplicate webhooksHandling duplicate webhooks

In rare instances, your app might receive the same webhook event more than once. Shopify recommends detecting duplicate webhook events by comparing the `X-Shopify-Event-Id` header to previous events' `X-Shopify-Event-Id` header.

---

- Get your app set up quickly with [its first webhook subscription](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started).
- Consult the [webhooks reference](https://shopify.dev/docs/api/webhooks) to explore a full list of topics and sample payloads.
- After your app is set up with subscriptions, learn how to [customize webhooks](https://shopify.dev/docs/apps/build/webhooks/customize) to meet your bespoke needs.

---

---
