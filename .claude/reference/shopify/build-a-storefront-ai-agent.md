---
title: Build a Storefront AI agent
source: https://shopify.dev/docs/apps/build/storefront-mcp/build-storefront-ai-agent?framework=reactRouter
author: []
published: []
created: 2026-05-11
description: Create an AI-powered shopping assistant that helps customers find products and complete purchases.
tags: [clippings]
dept_secondary: [PERSONAL]
---

Build an AI chat agent that helps shoppers find products faster and complete purchases through natural conversation. The agent can answer questions about products, shipping policies, and manage shopping carts using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) to connect with Shopify's commerce features.

Use natural language to search for products, get recommendations, ask questions about store policies, and complete checkout—all within a chat window.

## Requirements

[Node.js v18.20 or higher](https://nodejs.org/)

Download from nodejs.org and install.

[Shopify Partner account](https://www.shopify.com/partners)

Sign up at shopify.com/partners.

[Shopify dev store with sample products](https://shopify.dev/docs/apps/build/dev-dashboard/development-stores)

Create a dev store for testing - see the dev stores guide. Make sure to add some sample products.

[Claude API Key](https://docs.anthropic.com/en/api/admin-api/apikeys/get-api-key)

Generate a key in the Claude Console and store it securely. This template uses Claude, but you can swap in any LLM by updating the code.

[Latest version of Shopify CLI](https://shopify.dev/docs/api/shopify-cli)

Install the [latest version of Shopify CLI](https://shopify.dev/docs/api/shopify-cli#upgrade). You'll need this before starting the tutorial.

## Project[View on GitHub](https://github.com/Shopify/shop-chat-agent)

## Anchor to InstallationInstallation

### Anchor to Set up environment variablesSet up environment variables

Rename the `.env.example` file to `.env` and make sure it has your Claude API key:

CLAUDE\_API\_KEY=your\_claude\_api\_key

Note

See the [Change the AI provider](#change-the-ai-provider) section if you want to use a different LLM.

## Anchor to Create your appCreate your app

### Anchor to Select your organizationSelect your organization

? Which organization is this work for?

\> Organization name

### Anchor to Select Yes to create this project as a new appSelect Yes to create this project as a new app

? Create this project as a new app on Shopify?

\> (y) Yes, create it as a new app

### Anchor to Accept the default app nameAccept the default app name

Hit enter to accept the default name `shop-chat-agent`. All references in the code use this name.

? App name:

\> shop-chat-agent

### Anchor to Keep the configuration file name blankKeep the configuration file name blank

? Configuration file name:

✔ (empty)

### Anchor to Overwrite existing configuration fileOverwrite existing configuration file

Select **no** and overwrite your existing configuration file:

? Configuration file shopify.app.toml already exists. Do you want to choose a different configuration name?

✔ No, overwrite my existing configuration file

### Anchor to Select your dev storeSelect your dev store

Choose the dev store you would like to use:

? Which store would you like to use to view your project?

✔ your-store

### Anchor to Enter your store passwordEnter your store password

You can get your store password from the URL that is in your terminal:

? Incorrect store password (

https://your-store.myshopify.com/admin/online\_store/preferences ). Please

try again:

\> \*\*\*\*\*█\_\_\_\_\_\_\_\_

Note

At this stage, you will see `Preview URL: https://your-store.myshopify.com/...` in your terminal. You can now proceed to the next step. If you get an error, restart from the [Shopify CLI installation step](#install-shopify-cli).

### Anchor to Generate a certificate for localhostGenerate a certificate for localhost

? --use-localhost requires a certificate for \`localhost\`. Generate it now?

\> Yes, use mkcert to generate it

### Anchor to Allow automatic URL updatesAllow automatic URL updates

Select yes to automatically update your app's URL:

Have Shopify automatically update your app's URL in order to create a preview experience?

\> Yes, automatically update

## Anchor to Run your appRun your app

### Anchor to Access your storeAccess your store

Follow the `Preview URL: https://your-store.myshopify.com/...` in your terminal to open your store in your browser.

### Anchor to Enable the theme extensionEnable the theme extension

In your Shopify admin, navigate to Online Store > Themes

- Click the **Customize** button
- Click the **App embeds** icon in the sidebar
- Enable the toggle
- Click **Save**

Congratulations!

Your AI shopping assistant is now fully functional for product search, cart management, and store policy questions.

You can start [testing and customizing your app](https://shopify.dev/docs/apps/build/storefront-mcp/testing-and-examples), or continue to the next section to enhance it with the [customer accounts MCP server](https://shopify.dev/docs/apps/build/storefront-mcp/servers/customer-account).

## Anchor to (Optional) Configure customer accounts authentication(Optional) Configure customer accounts authentication

Add order history and account management features to your AI assistant:

You'll need Level 2 protected customer data permissions to use the Customer accounts MCP server. See [Shopify's guidelines](https://shopify.dev/docs/apps/launch/protected-customer-data).

### Anchor to Verify Next-Gen Dev Platform accessVerify Next-Gen Dev Platform access

Verify that you have access to the [Next-Gen dev platform](https://shopify.dev/docs/beta/next-gen-dev-platform). This is required for the customer accounts authentication features.

### Anchor to Create your app on the Next-Gen Dev PlatformCreate your app on the Next-Gen Dev Platform

Follow the steps on the Next-Gen dev platform page to create a [Storefront AI agent app](https://shopify.dev/docs/beta/next-gen-dev-platform/apps) using a partner organization. You can use the code from the [reference app repo](https://github.com/Shopify/shop-chat-agent).

### Anchor to Set up your dev storeSet up your dev store

Create a [dev store](https://shopify.dev/docs/beta/next-gen-dev-platform/development-stores) on the Next-Gen Dev Platform. Make sure to add some sample products to test the AI agent functionality.

### Anchor to Request protected data accessRequest protected data access

Click **Request access** under the Protected customer data section.

### Anchor to Provide a reason for accessing protected dataProvide a reason for accessing protected data

Click **select** on **protected customer data**. Provide a clear reason for requesting this data.

### Anchor to Provide a reason for accessing specific data fieldsProvide a reason for accessing specific data fields

Click **select** for each data field: `name`, `email`, `phone`, and `address`. Provide a clear reason for requesting each field.

### Anchor to Update your app's TOML fileUpdate your app's TOML file

\# Add customer accounts MCP configurations

\[customer\_authentication\]

redirect\_uris = \[

"https://your-app-domain.com/callback"

\]

Replace `your-app-domain.com` with your actual app domain.

## Anchor to Next stepsNext steps

Now that you've built your AI shopping assistant, you can:

[Test and customize your agent](https://shopify.dev/docs/apps/build/storefront-mcp/testing-and-examples)

[Learn how to test your AI agent with example workflows and customize it to match your brand.](https://shopify.dev/docs/apps/build/storefront-mcp/testing-and-examples)

[Customer accounts MCP server](https://shopify.dev/docs/apps/build/storefront-mcp/servers/customer-account)

[Enable personalized experiences with order lookup, reordering, and account information.](https://shopify.dev/docs/apps/build/storefront-mcp/servers/customer-account)

Was this page helpful?

---
