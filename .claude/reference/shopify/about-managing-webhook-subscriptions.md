---
title: About managing webhook subscriptions
source: https://shopify.dev/docs/apps/build/webhooks/subscribe
author: []
published: []
created: 2026-05-11
description: Learn how to configure webhook subscription using the app config file, Shopify's recommended method and format for subscription management, and compares this method to subscriptions using the Admin API. Also provides guidance for custom apps subscribing to webhook topics.
tags: [clippings]
category: doc-clipping
rook-relevance: high
rook-consumers: shopify-agent, software-dev-team
---

You can configure your app to subscribe to webhook topics in the following ways:

1. **If your app was created with the Shopify CLI, then use your [app configuration file](https://shopify.dev/docs/apps/build/cli-for-apps/app-configuration)**. This is the recommended method for getting started quickly and for subscribing to webhooks for all shops that your app is installed on.
2. **If your app was created with the Shopify CLI, then you can also use the [GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql/unstable/mutations/webhookSubscriptionCreate)**. This is most useful in cases where your webhook subscriptions might depend on which shop your app is installed on.
3. **If your app is a [custom app](https://help.shopify.com/en/manual/apps/app-types/custom-apps)**, then use the Shopify admin to create your app and manage scopes, and the GraphQL Admin API to subscribe to webhook topics.

Once a subscription has been configured correctly, Shopify will send webhooks to your app with data about events that have occurred on a shop, related to the topics you have subscribed to.

### Anchor to What you'll learnWhat you'll learn

In this section, you will learn about:

- How to quickly get started and create your first webhook subscription
- This includes details about the use cases, trade-offs, and constraints for each. Shopify's recommendations across different subscription mechanisms (using your app configuration file vs. the Admin API), delivery methods (cloud-based vs. HTTPS) and technologies available to you. This includes details about the use cases, trade-offs, and constraints for each.

Info

Webhooks are divided by topic. Refer to the [Webhooks references](https://shopify.dev/docs/api/webhooks) for the complete list of supported webhook topics.

---

## Anchor to App-specific subscriptionsApp-specific subscriptions

You can subscribe your app to webhook topics using your app configuration file, rather than using the Admin API. This allows your subscriptions to be configured and managed across all shops that your app is installed on. This also makes subscription configuration and management easy when you are getting started with Shopify's webhooks. Shopify recommends subscribing to webhooks using this approach.

---

## Anchor to Shop-specific subscriptionsShop-specific subscriptions

To subscribe your app to webhook topics where the configuration depends on the shop your app is installed on, use the [GraphQL Admin API](https://shopify.dev/docs/apps/build/webhooks/subscribe/subscribe-using-api).

---

## Anchor to App-specific vs. Shop-specific subscriptionsApp-specific vs. Shop-specific subscriptions

If you use the Shopify CLI to build your app, then there are important differences to be aware of when configuring app-specific subscriptions using your [app configuration file](https://shopify.dev/docs/apps/build/cli-for-apps/app-configuration) versus configuring shop-specific subscriptions using the [Admin API](https://shopify.dev/docs/api/admin-graphql/latest/mutations/webhookSubscriptionCreate).

Warning

If you have shop-specific subscriptions already, and are migrating your app to app-specific subscriptions, then make sure you first remove any existing webhook subscriptions to the same topics. This avoids potential conflicts and duplicate notifications.

1. Check the list of existing shop-specific webhook topics your app is subscribed to by using the [GraphQL Admin API `webhookSubscriptions` query](https://shopify.dev/docs/api/admin-graphql/latest/queries/webhookSubscriptions).
2. Delete the relevant queries, subscription, and handler code from your app.
3. Deploy a new version of your app by running `shopify app deploy`. You can check that your subscriptions have been deleted by checking the **Versions** page for your app in the Dev Dashboard.
4. Configure your app to subscribe to app-specific subscriptions. Refer to the [create a subscription](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started) tutorial to get started.

|  | App-specific | Shop-specifc | Additional Resources |
| --- | --- | --- | --- |
| **Interface for management** | Your app configuration file | GraphQL Admin API |  |
| **Troubleshooting** | Failing webhook subscriptions that are not fixed will **not** be deleted by Shopify | Failing webhook subscriptions that are not fixed will be deleted by Shopify | [Troubleshoot your webhooks](https://shopify.dev/docs/apps/build/webhooks/troubleshooting-webhooks). |
| **Viewing subscriptions** | Available under **Subscriptions** in your app dashboard > **Versions** > **Configuration** | You can query the GraphQL Admin API to get a list of all webhook subscriptions | [GraphQL Admin API Query example](https://shopify.dev/docs/api/admin-graphql/latest/queries/webhookSubscriptions). |
| **Differentiating between methods** | Available in the **Subscription Method** field, per delivery log in your app dashboard > **Insights** > **Delivery logs** | Available in the "Subscription Method" field, per delivery log in your app dashboard > Insights > Delivery logs |  |
| **Identifying your subscriptions** | No ID, denoted **config-managed** | Available as the **Subscription ID** field, in your app dashboard > Insights > Webhooks > Select a topic to view Delivery Logs | Subscription IDs are only available for API-managed configurations. [A subscription ID can be used to query the subscription](https://shopify.dev/docs/api/admin-graphql/latest/queries/webhookSubscription). |
| **Scopes** | Requires scopes to be specified in your app configuration file | Scopes can be configured in your app configuration file or in your Dev Dashboard. They **cannot** be subscribed to using the Admin API | [Learn more about Shopify access and approval scopes](https://shopify.dev/docs/api/usage/access-scopes). |
| **Metafield Namespaces** | Does not support using `metafieldNamespaces` | `metafieldNamespaces` can be used as an input field for a webhook subscription in the Admin API | Learn how in the [GraphQL Admin API examples](https://shopify.dev/docs/api/admin-graphql/latest/mutations/webhookSubscriptionCreate#argument-webhooksubscription). |
| **Configuring compliance webhook topics** | Compliance topics can be subscribed to using your app configuration file | Compliance topics can be configured in your app configuration file. They **cannot** be subscribed to using the Admin API | Refer to examples in the [Privacy law compliance documentation](https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance#subscribe-to-compliance-webhooks) and see which scopes are required for these topics in the [Webhooks reference](https://shopify.dev/docs/api/webhooks). |
| **Topics** | Supports every topic except for `product_feeds/full_sync`, `product_feeds/full_sync_finish`, and `product_feeds/incremental_sync` | Supports every topic | Refer to the list of [webhook topics](https://shopify.dev/docs/api/webhooks). |

---

## Anchor to Subscribing to topics as a custom appSubscribing to topics as a custom app

Webhooks are available for all custom apps to use. However, custom apps created in the Shopify admin cannot take advantage of the tooling available through the Shopify CLI, including subscribing to webhook topics using the app configuration file.

This means that webhook subscriptions must be set up and configured using the GraphQL Admin API.

1. Create an app in the Shopify Admin and install it on your test shop to get your Admin API Access token.
2. Configure your Admin API scopes by selecting the scopes that you'll need for each webhook topic that you intend to subscribe to. Learn more about which topics require which Shopify scopes in the [Webhooks reference](https://shopify.dev/docs/api/webhooks).
3. Subscribe to webhook topics [using the Admin API](https://shopify.dev/docs/apps/build/webhooks/subscribe/subscribe-using-api) and your Admin API access token.

---

- Get started by [setting up your first webhook subscription](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started).
- Learn how to subscribe to webhooks [using the GraphQL Admin API](https://shopify.dev/docs/apps/build/webhooks/subscribe/subscribe-using-api).
- Understand the differences between cloud-based event bus delivery of webhooks, and [HTTPS delivery](https://shopify.dev/docs/apps/build/webhooks/subscribe/https).

---

---
