---
title: Apps in orders and fulfillment
source: https://shopify.dev/docs/apps/build/orders-fulfillment
author: []
published: []
created: 2026-05-11
description: Create fulfillment apps that integrate into order management, shipping, and the fulfillment processes.
tags: [clippings]
---

You can create fulfillment apps that integrate into inventory management, order management, shipping, and fulfillment processes.

This guide describes the different types of apps that you can build with Shopify. It also provides information about migrating your app to use fulfillment order-based workflows, and offers related developers tools and resources to get you started.

Note

Checkouts and orders can include multiple delivery methods, such as shipping and pickup in the same order. When your app uses delivery or fulfillment data, iterate over all delivery groups or fulfillment orders to determine the delivery method for each one. Don't assume one method for the order. For more information, refer to [split carts in checkout](https://shopify.dev/docs/apps/build/orders-fulfillment/split-carts).

---

## Anchor to Inventory management appsInventory management apps

[Inventory management apps](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps) automate the inventory management process by querying and adjusting inventory quantities on behalf of merchants.

Inventory apps can help merchants organize and manage goods throughout the supply chain, manage what customers can purchase on the merchant's sales channels, determine when to make a purchase order, and centralize inventory and order data.

The following diagram shows some of the inventory management activities that an app or third-party logistics provider can perform in the context of an order lifecycle:

![A diagram showing some of the inventory management activities that an app or third-party logistics provider can perform in the context of an order cycle.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/fulfillments/inventory-management-apps/lifecycle-Ck_sH0VU.png)

A diagram showing some of the inventory management activities that an app or third-party logistics provider can perform in the context of an order cycle.

---

## Anchor to Order management appsOrder management apps

[Order management apps](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps) fulfill orders on behalf of merchants. Apps can automate fulfillment, or merchants can directly fulfill orders through the app.

Order management apps can help merchants with complicated shipping workflows that include multiple steps like buying shipping labels, reassigning inventory based on availability, or rescheduling upcoming shipments for a different date.

The following diagram shows an example lifecycle of fulfilling an order using an order management app:

![A diagram showing an example lifecycle of fulfilling an order using an order management app.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/fulfillments/order-management-apps/lifecycle-FUyF48jM.png)

A diagram showing an example lifecycle of fulfilling an order using an order management app.

---

## Anchor to Order routing appsOrder routing apps

[Order routing apps](https://shopify.dev/docs/apps/build/orders-fulfillment/order-routing-apps) provide a way for merchants with complex or highly custom needs to take control over their fulfillment and delivery strategy needs. Order routing apps use [Shopify Functions](https://shopify.dev/docs/apps/build/functions) to customize fulfillment and delivery strategies.

Apps can register custom [location rules](https://shopify.dev/docs/apps/build/orders-fulfillment/order-routing-apps/location-rules) for use with order routing, or generate [fulfillment constraints](https://shopify.dev/docs/apps/build/orders-fulfillment/order-routing-apps/build-fulfillment-constraints-function) to determine how items are to be fulfilled.

The following diagram shows an example lifecycle of registering and executing a Shopify Function using an order routing app:

![A diagram showing an example registering and executing a Shopify Function using an order routing app.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/fulfillments/order-routing-apps/lifecycle-DkfmHiiv.png)

A diagram showing an example registering and executing a Shopify Function using an order routing app.

---

## Anchor to Fulfillment service appsFulfillment service apps

[Fulfillment service apps](https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps) are services that perform the fulfillment of physical products for merchants. These apps enable high-quality communication between fulfillment centers and merchants and transparent reporting about order status through the Shopify admin.

Merchants and other apps can submit requests to fulfill orders, and fulfillment services can subsequently approve or reject requests to fulfill. After a request is approved, merchants can also submit requests to cancel the fulfillment order before the order is shipped.

The following diagram shows an example lifecycle of fulfilling an order using a fulfillment service app:

![A diagram showing an example lifecycle of fulfilling an order using a fulfillment service app.](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/fulfillments/fulfillment-service-apps/lifecycle-CB2gNMKi.png)

A diagram showing an example lifecycle of fulfilling an order using a fulfillment service app.

---

## Anchor to Returns appsReturns apps

[Return apps](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps) capture the financial, logistical, and business intent of a return. These apps provide merchants with various ways to manage their returns.

Merchants manage their returns in Shopify, and returns apps can take actions on behalf of merchants. For example, a returns app can identify eligible items for a return and issue customers a refund for returned items on behalf of the merchant.

The following diagram shows an example lifecycle of a return:

![A diagram showing the lifecycle of a return](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/fulfillments/return-apps/return-lifecycle-BWgLBKoJ.png)

A diagram showing the lifecycle of a return

---

## Anchor to Where you can buildWhere you can build

Orders and fulfillment apps integrate with multiple Shopify surfaces. Choose where you want to add functionality:

[Admin](https://shopify.dev/docs/apps/build/admin)

[Automate inventory, order management, order routing, fulfillment, and returns workflows for merchants.](https://shopify.dev/docs/apps/build/admin)

[Customer accounts](https://shopify.dev/docs/apps/build/customer-accounts)

[Let customers request self-serve returns and manage orders directly from their account.](https://shopify.dev/docs/apps/build/customer-accounts)

---

## Anchor to Migrating your appMigrating your app

In Shopify, the [`FulfillmentOrder`](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder) object models an end-to-end fulfillment process and is available in the GraphQL Admin API. The `FulfillmentOrder` object enables fulfillment data to sync accurately between Shopify and apps.

Deprecated

By API version 2023-07, all apps should be using the [`FulfillmentOrder`](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder) object to manage fulfillments. Apps using the following GraphQL Admin API objects to fulfill orders are using a legacy workflow that is no longer supported as of API version 2022-07:

- [`Order`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order)
- [`Fulfillment`](https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment)

### Anchor to BenefitsBenefits

Migrating your app to the fulfillment orders workflow provides the following benefits:

- You can fetch the assigned location of a given group of unfulfilled line items to determine where fulfillment should occur.
- You no longer need to match SKUs or filter out the items on an order that don’t apply to you before you can determine which items you need to fulfill.
- App users and apps can both add notes to requests, which can improve communication throughout the fulfillment process.
- The process of making fulfillment and cancellation requests is formalized.

To learn how to migrate your app, refer to [Migrate to fulfillment orders](https://shopify.dev/docs/apps/build/orders-fulfillment/migrate-to-fulfillment-orders).

If you maintain a third-party app or Shopify Flow workflow that relies on `Order` and `Fulfillment` API resources for order automation, then refer to [Track orders placed through third-party marketplaces](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/track-orders-other-platforms).

---

## Anchor to Developer tools and resourcesDeveloper tools and resources

Explore the following developer tools and resources to learn more about fulfillment apps.

[InventoryLevel object](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel)

[Consult the GraphQL Admin API reference to learn more about the InventoryLevel object.](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel)

[FulfillmentOrder object](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder)

[Consult the GraphQL Admin API reference to learn more about the FulfillmentOrder object.](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder)

[Split carts in checkout](https://shopify.dev/docs/apps/build/orders-fulfillment/split-carts)

[Learn how Shopify represents orders that split across multiple shipments or delivery methods.](https://shopify.dev/docs/apps/build/orders-fulfillment/split-carts)

[FulfillmentService object](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentService)

[Consult the GraphQL Admin API reference to learn more about the FulfillmentService object.](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentService)

[Return object](https://shopify.dev/docs/api/admin-graphql/latest/objects/Return)

[Consult the GraphQL Admin API reference to learn more about the Return object.](https://shopify.dev/docs/api/admin-graphql/latest/objects/Return)

---

- Learn how [inventory management apps](https://shopify.dev/docs/apps/build/orders-fulfillment/inventory-management-apps) query and adjust inventory quantities on behalf of merchants.
- Learn how [order management apps](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps) fulfill orders on behalf of merchants.
- Learn how [fulfillment service app](https://shopify.dev/docs/apps/build/orders-fulfillment/fulfillment-service-apps) prepare and ship orders on behalf of store owners.
- Learn how [returns apps](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps) can provide a return management workflow for merchants and customers.

---

---
