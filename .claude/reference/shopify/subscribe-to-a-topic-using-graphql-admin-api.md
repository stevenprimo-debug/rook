---
title: Subscribe to a topic using GraphQL Admin API
source: https://shopify.dev/docs/apps/build/webhooks/subscribe/subscribe-using-api
author: []
published: []
created: 2026-05-11
description: Create and manage your webhook subscriptions using the GraphQL Admin API.
tags: [clippings]
category: vendor-api-reference
rook-relevance: high
rook-consumers: shopify-agent, software-dev-team
---

To configure shop-specific subscriptions, use the GraphQL Admin API. Shopify recommends using your app configuration file in most instances, and when configuring app-specific subscriptions. Refer to the tutorial for [setting up a subscription](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started) to learn how.

---

## Anchor to RequirementsRequirements

- You have created an app either using the Shopify CLI and the [React Router template](https://github.com/Shopify/shopify-app-template-react-router), or if you are creating a custom app in the Shopify Admin.
- You have [Google Cloud Pub/Sub](https://cloud.google.com/pubsub) or [Amazon EventBridge](https://aws.amazon.com/eventbridge/) set up, or a server available for HTTPS delivery. To learn more about setting these event buses up, find the first steps in [the tutorial for setting up a webhook subscription](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started).

Note

Shopify recommends using Google Pub/Sub as a cloud-based solution for delivering webhooks. You can also use Amazon EventBridge. In instances where you want to build your own webhooks infrastructure, you might prefer your webhooks be delivered through HTTPS - just know there are [extra considerations you'll need to take into account](https://shopify.dev/docs/apps/build/webhooks/subscribe/https).

---

## Anchor to What you'll learnWhat you'll learn

In this guide, you'll learn how to do the following tasks:

1. Use the GraphQL Admin API to create a webhook subscription.
2. Test your subscription is configured correctly and you are receiving webhooks.

---

## Anchor to Step 1: Create a webhook subscriptionStep 1: Create a webhook subscription

Shopify recommends that you use the Shopify CLI and React Router template when subscribing to webhooks using the GraphQL Admin API. The template abstracts away the actual GraphQL mutation you would otherwise have to write.

1. You might want to create a subscription to the `ORDERS_CREATE` topic using the GraphQL Admin API. Specify the topic name using GraphQL's enum screaming case syntax, as well as the subscription endpoint you want to use to receive webhooks.

Info

Webhooks are divided by topic. Refer to the [Webhooks references](https://shopify.dev/docs/api/webhooks) for the complete list of supported webhook topics.

1. Add this information and the following code to your app in the `app/shopify.server.ts` file.

const shopify = shopifyApp({

...,

webhooks: {

ORDERS\_CREATED: {

deliveryMethod: DeliveryMethod.PubSub,

pubSubProject: "<GCP-PROJECT>",

pubSubTopic: "<PUB\_SUB\_TOPIC>",

},

},

hooks: {

afterAuth: async ({ session }) => {

shopify.registerWebhooks({ session });

},

},

...

});

const shopify = shopifyApp({

...,

webhooks: {

ORDERS\_CREATED: {

deliveryMethod: DeliveryMethod.EventBridge,

arn: "<ARN>"

},

},

hooks: {

afterAuth: async ({ session }) => {

shopify.registerWebhooks({ session });

},

},...

});

Note

If you are using Amazon EventBridge, set `arn` to the ARN that you retrieved when you associated your event bus during setup.

### Anchor to Developing with GraphQL mutations directlyDeveloping with GraphQL mutations directly

For apps that are not using the React Router template, to create a new webhook subscription, you'll use the webhook subscription mutations found in our [GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest/queries/webhookSubscription).

1. You might want to create a subscription to the `ORDERS_CREATE` topic using the GraphQL Admin API. Specify the topic name using GraphQL's enum screaming case syntax, as well as the subscription endpoint you want to use to receive webhooks.

Info

Webhooks are divided by topic. Refer to the [Webhooks references](https://shopify.dev/docs/api/webhooks) for the complete list of supported webhook topics.

1. Add this information and the following code to your app, wherever you process your after-authentication hooks. This would be the equivalent to the `app/shopify.server.ts` file in the React Router template, because this is where the `afterAuth` code lives.
2. You might want to test out your code or [example GraphQL queries](https://shopify.dev/docs/api/admin-graphql/latest/queries/webhookSubscriptions#section-examples) before adding it to your app. In this case, you can use the [`GraphiQL`](https://shopify.dev/docs/api/usage/api-exploration/admin-graphiql-explorer) interface by pressing `g` in the console where your app is running. You must include values for the variables in order to execute the mutations.

**Request**: `POST /admin/api/2026-04/graphql.json`

mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {

webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {

userErrors {

field

message

}

webhookSubscription {

id

format

includeFields

metafieldNamespaces

topic

uri

}

}

}

Note

If you're using Amazon EventBridge, then set `uri` to the ARN that you retrieved when you associated your event bus during setup. For Google Pub/sub the `uri` format is `pubsub://{project-id}:{topic-id}`.

---

You can use Shopify CLI's [`webhook trigger`](https://shopify.dev/docs/api/shopify-cli/app/app-webhook-trigger) command to test webhook delivery. When using this command, note the difference in the URI that you should input for the `--address` flag:

For Google Pub/Sub, the address is:

pubsub://{project-id}:{topic-id}

- `{project-id}`: The ID of your Google Cloud Platform project
- `{topic-id}`: The ID of the topic that you set up in Google Cloud Pub/Sub

For Amazon EventBridge, the address is:

arn:aws:events:{aws\_region}::event-source/aws.partner/shopify.com/{app\_id}/{event\_source\_name}

- This is your ARN. You can find details in your Amazon EventBridge console: **Partner Event Sources** > **Select your event source** > **Partner event source ARN**.

Caution

When you're using cloud-based event buses like Google Cloud Pub/Sub or Amazon EventBridge for delivery of your webhooks:

- You receive a JSON payload for topics, but there will be additional fields included beyond the sample payloads displayed in the [Webhooks reference](https://shopify.dev/docs/api/webhooks).
- You don't need to perform HMAC verification.

---

---
