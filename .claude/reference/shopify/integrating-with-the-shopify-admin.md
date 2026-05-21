---
title: Integrating with the Shopify admin
source: https://shopify.dev/docs/apps/build/integrating-with-shopify
author: []
published: []
created: 2026-05-11
description: Learn about app best practices, the parts of your app that should always be in the Shopify admin, and the parts of your app that you can surface elsewhere.
tags: [clippings]
---

Integrating your app into the Shopify admin makes it feel familiar, gives you access to Shopify UI elements, and lets users use it easily on mobile devices.

When you integrate your app, you should design it so that the user isn't forced to leave the Shopify admin on a regular basis. All of its primary functionality should be available within the Shopify admin.

Tip

Apps are eligible for [Built for Shopify](https://shopify.dev/docs/apps/launch/built-for-shopify) status if they follow all best practices on this page and meet all other [Built for Shopify criteria](https://shopify.dev/docs/apps/launch/built-for-shopify/achievement-criteria). These guidelines have been updated and were previously called the "Best practices for Embedding in Shopify".

To be properly integrated with the Shopify admin, apps must do the following:

## Anchor to Keep primary app workflows within ShopifyKeep primary app workflows within Shopify

By default, apps should be embedded in the Shopify admin with the latest version of [App Bridge](https://shopify.dev/docs/api/app-home). Merchants should be able to complete primary app workflows inside the Shopify admin. Merchants should not need to access an external website or external surface to complete a primary workflow.

| Example | Details |
| --- | --- |
| The [Search & Discovery](https://apps.shopify.com/search-and-discovery) app follows this guideline. | The app includes all workflows, such as customizing filters, search, and recommendations, as pages in the app.  ![Screenshot of the recommendations workflow in Shopify Search & Discovery.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/best-practices/embedding/sd-recs-DR5lE7oc.png) |

### Anchor to ExceptionsExceptions

Apps that contain more functionality than can be reasonably integrated into the Shopify admin do not have to integrate all of their primary workflows into the Shopify admin. For example, apps that handle ad buying or enterprise resource planning (ERP) require a standalone site to enable access to their functionality in a user-friendly manner.

However, some workflows must always be present in the Shopify admin. These workflows include setup, configuration, status, dashboards, and other features that help a merchant use the app on a day-to-day basis.

| Example | Details |
| --- | --- |
| The [Shopify Inbox](https://apps.shopify.com/inbox) app follows this guideline. | The app is a messaging tool that lets app users communicate with customers. Most basic workflows, such as setting up a chat widget, creating automated replies, and configuring notifications are included as pages in the app.  ![Screenshot of the chat settings in the Shopify Inbox app.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/best-practices/embedding/inbox-admin-D6IzWvne.png)  However, users want to continuously monitor their conversation inbox, and continue to access other areas of the Shopify admin at the same time. Because of this, it's acceptable that the customer conversation workflows in Shopify Inbox are available on an external website.  ![Screenshot of the inbox of the Shopify Inbox app.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/best-practices/embedding/inbox-C5l3mKYJ.png) |

---

Apps should make sign up seamless for merchants. Apps should be usable without having an additional login or sign-up prompt.

| Example | Details |
| --- | --- |
| The [Search & Discovery](https://apps.shopify.com/search-and-discovery) app follows this guideline. | Users can begin using the app immediately without having to complete another sign up.  ![Screenshot of the recommendations workflow in Shopify Search & Discovery.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/best-practices/embedding/sd-recs-DR5lE7oc.png) |
| This example app does not follow the guideline. | This app requires users to complete another sign up before they can use the app. Instead, the app should use the merchant's existing Shopify credentials. This is only acceptable if the app cannot be obtained by merchants in a self-service manner.  ![Screenshot of an app asking the current user to log in.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/best-practices/embedding/seamless-sign-up-DZv87TEa.png) |

### Anchor to ExceptionsExceptions

Access to some apps cannot be easily obtained by merchants in a self-service manner, and require a more complex sign-up, often involving a business-to-business contract. Examples of this include connecting to ad networks or allowing non-merchants to log in. These apps aren't required to enable seamless sign up using a merchant’s credentials. The first step to the in-admin onboarding of these apps must always be a workflow that enables a merchant to link the current store with their existing credentials.

If your app offers both self-service and business-to-business sign up, then the app's onboarding must include an option to sign up for the service using the merchant's existing Shopify credentials.

---

## Anchor to Include simplified monitoring or reportingInclude simplified monitoring or reporting

Expose key metrics that are helpful for merchants on the app’s home page. If your app includes monitoring or complex reports that can only exist on an external website or app surface, then you must include a simplified version of the monitoring or reporting in the Shopify admin.

| Example | Details |
| --- | --- |
| The [Search & Discovery](https://apps.shopify.com/search-and-discovery) app follows this guideline. | The app exposes key metrics about search and recommendation performance, including the click rate and purchase rate, on the app's home page.  ![Screenshot of key metrics on the home page of the Shopify Search & Discovery app.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/best-practices/embedding/sd-recs-DR5lE7oc.png) |

---

## Anchor to Keep third-party connection settings within ShopifyKeep third-party connection settings within Shopify

Any settings or configurations that control the connection between Shopify and a third-party system must be available inside the Shopify admin.

---
