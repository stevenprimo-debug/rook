---
title: Shopify App package for React Router
source: https://shopify.dev/docs/api/shopify-app-react-router/latest
author: []
published: []
created: 2026-05-11
description: The @shopify/shopify-app-react-router package enables React Router apps to authenticate with Shopify and make API calls.
tags: [clippings]
category: vendor-sdks
rook-relevance: high
rook-consumers: shopify-agent, software-dev-team
---

## Anchor to Quick startQuick start

The quickest way to create a new app is using the Shopify CLI, and the Shopify App Template.

Check out the [getting started guide](https://shopify.dev/docs/apps/build/scaffold-app), or the [app template](https://github.com/Shopify/shopify-app-template-react-router).

---

## Anchor to Configure the packageConfigure the package

Using the `shopifyApp` function, you can configure the package's functionality for different app distributions types, access tokens, logging levels and future flags.[shopifyApp](https://shopify.dev/docs/api/shopify-app-react-router/entrypoints/shopifyapp)

---

## Anchor to Make Admin API GraphQL requestsMake Admin API GraphQL requests

Authenticated requests with the Admin API GraphQL client are made by calling the `admin.graphql` function. This function returns a GraphQL client that is authenticated with the Admin API.[admin.graphql](https://shopify.dev/docs/api/shopify-app-react-router/v0/guide-admin#graphql-api)

---

## Anchor to Add a new route to your appAdd a new route to your app

Routes embedded in the Shopify Admin must be nested under an Admin layout route for proper authentication and functionality.

The template includes an admin route at `/app/routes/app.tsx` that handles App Bridge initialization, authenticates requests via `authenticate.admin`, provides error boundaries and headers required by the admin.

When creating new routes, place them in the `/app/routes/` directory with the `app.` prefix (e.g., `app.products.tsx`) to ensure they inherit these features. This structure ensures your app behaves correctly within the Shopify Admin and has access to authenticated API clients.

---

## Anchor to Authenticate Webhook RequestsAuthenticate Webhook Requests

The package provide functions to authenticate webhook requests. This function returns a webhook client that is authenticated with the Admin API.

Note

Ensure your webhook route is not nested under you app layout route.[authenticate.webhook](https://shopify.dev/docs/api/shopify-app-react-router/v0/authenticate/webhook)

---

## Anchor to Session StorageSession Storage

When using this package, installed shops access tokens will be stored in session storage.You can configure the storage mechanism by passing a custom storage object to the `shopifyApp` function.By default, the template will use Prisma and SQLite, but other session storage adapters are available.

Note

The type of session storage you use may impact how your app will be deployed.[Session Storage](https://github.com/Shopify/shopify-app-js/tree/main/packages/apps/session-storage)

---

## Anchor to Deploy your appDeploy your app

You can deploy your app to your preferred hosting service that is compatible with JavaScript apps. Review our deployment guide to learn about the requirements for deploying your app.

---
