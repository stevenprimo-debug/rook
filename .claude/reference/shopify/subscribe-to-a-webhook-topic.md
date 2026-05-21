---
title: Subscribe to a webhook topic
source: https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started?deliveryMethod=pubSub
author: []
published: []
created: 2026-05-11
description: Learn how to set up and configure a webhook subscription using the app configuration file and GCP PubSub.
tags: [clippings]
dept_secondary: [SHOPIFY]
---

Subscribe your app to Shopify webhook topics so that it will be alerted when an event occurs on a merchant store.

Suppose you are building a warranty pricing app that determines which warranty options a customer can add to their cart, based on the cost of an order.

When a customer is checking out, the total order cost is used to determine which warranty options a customer can select from.

In this tutorial, you'll subscribe your app to a webhook topic to be alerted whenever a new order is created.

## Anchor to What you'll learnWhat you'll learn

In this tutorial, you'll learn how to do the following tasks:

- Use your [app configuration file](https://shopify.dev/docs/apps/tools/cli/configuration#webhooks) to set up a webhook subscription.
- Use cloud-based delivery methods like [Google Cloud's Pub/Sub event bus](https://cloud.google.com/pubsub) to receive webhooks.
- Test your subscription is configured correctly and you are receiving webhooks.

Info

Shopify recommends using [Google Pub/Sub](https://cloud.google.com/pubsub) as a cloud-based solution for delivering webhooks. You can also use [Amazon EventBridge](https://aws.amazon.com/eventbridge/).

In instances where you want to hand-roll your own webhooks infrastructure, you may prefer your webhooks be delivered through [HTTPS](https://shopify.dev/docs/apps/webhooks/configuration/https).

During development, you may choose to use your app's URL or external mock server sites like [webhook.site](https://webhook.site/) and [Beeceptor](https://beeceptor.com/). These are not recommended for production.

## Requirements

[Use the latest version of Shopify CLI](https://shopify.dev/docs/api/shopify-cli)

Ensure you have the [latest version of Shopify CLI](https://shopify.dev/docs/api/shopify-cli#upgrade) installed to configure app-specific webhook subscriptions.

[Set up a Google Cloud console project](https://cloud.google.com/pubsub/docs/quickstart-console)

Set up your Google Cloud account to use Pub/Sub.

[Development tools](https://shopify.dev/docs/apps/build/webhooks/subscribe/get-started)

For development, you can use mock servers like [Hookdeck Console](https://console.hookdeck.com/) or [webhook.site](https://webhook.site/) can be used for development.

## Project[View on GitHub](https://github.com/Shopify/shopify-app-template-react-router/blob/webhooks-subscribe-example-pubSub/shopify.app.toml)

## Anchor to Set your app up to receive webhooks from Google Pub/SubSet your app up to receive webhooks from Google Pub/Sub

To receive webhooks via a cloud-based event bus like Pub/Sub from Google Cloud, you must first set up a connection between your app and Pub/Sub.

### Anchor to Grant Shopify access to publish webhooks to your Google Pub/Sub topicGrant Shopify access to publish webhooks to your Google Pub/Sub topic

1. Click on **Topics** in the left panel.
2. Click on the **Create a topic** button. Enter in a name, keep the remaining defaults and click on **Create**.
3. Next to the Google Pub/Sub topic you just created, click `⋮` and then click **View permissions**.
4. Click on **ADD PRINCIPAL**.
5. Paste `delivery@shopify-pubsub-webhooks.iam.gserviceaccount.com` (the Shopify service account address) into the **New principals** text box.
6. In the **Role** drop-down list, select **Pub/Sub** as the type, and specify the role as **Pub/Sub Publisher**.
7. Click **Save**.

## Anchor to Configure your webhook subscriptionConfigure your webhook subscription

### Anchor to Update your access scopesUpdate your access scopes

Some webhook topics require scopes in order to be used. Since we want to know about when an order has been created, we need to include the `read_orders` scope in the configuration file.

- To determine which scopes are required for each topic, use the [Webhooks reference](https://shopify.dev/docs/api/webhooks).
- The complete list of Shopify API access and approval scopes are listed [here](https://shopify.dev/docs/api/usage/access-scopes).

Info

Scopes that access private customer data, such as `read_orders`, require manual steps in your Partner Dashboard. Go to your app > **API access requests** > **Protected customer data access**, fill out only the first step, and then save. Reinstall your app in the Shopify admin to register the granted scope.

### Anchor to Select the API versionSelect the API version

The API version impacts which topics are available to subscribe to. The React Router template defaults to the latest version in your app configuration file. However, you can [update the API version](https://shopify.dev/docs/apps/webhooks/versioning) as needed.

### Anchor to Confirm the subscription has been added to this version of your appConfirm the subscription has been added to this version of your app

When working in development mode, webhook subscriptions are automatically updated when you save your TOML file.

1. Save your TOML file.
2. If `app dev` is running, the webhook subscription will be automatically created or updated.
3. The webhook subscription is now active in your dev store.

Info

This step abstracts away calls to the [`webhookSubscriptionCreate`](https://shopify.dev/docs/api/admin-graphql/latest/mutations/webhookSubscriptionCreate) GraphQL mutation

Learn more about [subscribing to webhook topics using the GraphQL Admin API](https://shopify.dev/docs/apps/build/webhooks/subscribe/subscribe-using-api).

## Anchor to Test your subscriptionTest your subscription

### Anchor to Manually trigger an event in your test shopManually trigger an event in your test shop

Most webhook topics will fire immediately if you trigger the corresponding event your dev store.

1. Navigate to your test shop and create a new order.
2. The webhook payload should print to your Google Pub/Sub console.

Info

A small number of webhook topics will not fire immediately if you trigger an event in your test shop. They include:

- The [customers/redact topic](https://shopify.dev/docs/apps/build/privacy-law-compliance#customers-redact)
- The [shop/redact topic](https://shopify.dev/docs/apps/build/privacy-law-compliance#shop-redact)

### Anchor to Simulate an event using the command lineSimulate an event using the command line

You can use the CLI to simulate specific events occurring on a shop. This lets you test your processing logic by sending a POST request to your endpoint with a synthetic webhook. Note that it does not test your subscription configuration!

[`shopify app webhook trigger`](https://shopify.dev/docs/api/shopify-cli/app/app-webhook-trigger)

The address inputted for the `--address` flag should follow the following format:

pubsub://{project-id}:{topic-id}

## Anchor to Deploy your appDeploy your app

When you're ready to release your webhook subscriptions to production:

When you're ready to release your changes to users, you can create and release an [app version](https://shopify.dev/docs/apps/launch/deployment/app-versions). An app version is a snapshot of your app configuration and all extensions.

1. Navigate to your app directory.
2. Run the following command.
	Optionally, you can provide a name or message for the version using the `--version` and `--message` flags.
	shopify app deploy

Releasing an app version replaces the current active version that's served to stores that have your app installed. It might take several minutes for app users to be upgraded to the new version.

Tip

If you want to create a version, but avoid releasing it to users, then run the `deploy` command with a `--no-release` flag. You can release the unreleased app version using Shopify CLI's [`release`](https://shopify.dev/docs/api/shopify-cli/app/app-release) command, or through the Dev Dashboard.

## Anchor to Tutorial complete!Tutorial complete!

Congratulations! You subscribed your app to a webhook topic using React Router, Google PubSub, and Shopify webhooks. Keep the momentum going with these related tutorials and resources.

### Anchor to Next stepsNext steps

[Deploy your app](https://shopify.dev/docs/apps/deployment/web)

[Follow our guide to deploy your React Router app to a testing or production environment.](https://shopify.dev/docs/apps/deployment/web)

[Explore the Shopify Webhooks reference](https://shopify.dev/docs/api/webhooks)

[Explore the Webhooks reference to learn about the full list of topics Shopify has, required access and approval scopes, and sample payloads.](https://shopify.dev/docs/api/webhooks)

[Learn about customizing your webhooks](https://shopify.dev/docs/apps/build/webhooks/customize)

[Customize your webhooks experience by using filters or modifying the payload per webhook.](https://shopify.dev/docs/apps/build/webhooks/customize)

[Select an app distribution method](https://shopify.dev/docs/apps/distribution)

[Decide how you want to share your app with users. For example, you might make your app available in the Shopify App Store, and bill customers for usage.](https://shopify.dev/docs/apps/distribution)

Was this page helpful?

---
