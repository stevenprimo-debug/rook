---
title: Set up iframe protection
source: https://shopify.dev/docs/apps/build/security/set-up-iframe-protection
author: []
published: []
created: 2026-05-11
description: Before you submit your app to the Shopify App Store, you must make sure that your app is only frameable by the authenticated shop domain.
tags: [clippings]
---

Apps on the Shopify App Store must set the proper Content Security Policy `frame-ancestors` directive to avoid clickjacking attacks. If the Content Security Policy `frame-ancestors` directive is missing or set incorrectly when you submit your app to the Shopify App Store, then your app might be rejected. You'll be required to address this before re-submitting your app for review.

Tip

To learn more about clickjacking, refer to [Portswigger's Web Academy](https://portswigger.net/web-security/clickjacking) or [OWASP Clickjacking](https://owasp.org/www-community/attacks/Clickjacking). To learn more about the `frame-ancestors` directive, refer to [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors).

---

## Anchor to Apps rendered in the Shopify adminApps rendered in the Shopify admin

If your app is [rendered in the Shopify admin](https://shopify.dev/docs/apps/build/admin), then you need to make sure that your app is only frameable by the authenticated shop domain. Set the `frame-ancestors` directive dynamically based on the current shop domain and the Shopify admin domain. Setting this directive guarantees that your app can be framed only within the shop admin.

For example, if the shop `shopify-dev.myshopify.com` installs your app, then the response headers from your app when being rendered by this shop will contain the following `frame-ancestors` declaration:

Content-Security-Policy: frame-ancestors https://shopify-dev.myshopify.com https://admin.shopify.com;

You can include other declarations in your `Content-Security-Policy` header besides `frame-ancestors`.

Note

The `frame-ancestors` declaration must be different for every shop, and these headers must be present in any routes that render HTML content.

---

## Anchor to Standalone appsStandalone apps

If your app isn't rendered in the Shopify admin, we recommend setting the `frame-ancestors` directive to `'none'` in order to disallow framing.

Content-Security-Policy: frame-ancestors 'none';

---

## Anchor to TroubleshootingTroubleshooting

Apps can fail to meet the iframe protection requirement in the following ways:

- The app isn't rendered in the Shopify admin, but is configured as if it is
- The app is rendered in the Shopify admin, but isn't following the expected `frame-ancestors` guidelines
	The following scenarios explain how to correct these issues.

### Anchor to The app shouldn't be rendered in the Shopify admin, but is configured to beThe app shouldn't be rendered in the Shopify admin, but is configured to be

If your app isn't rendered in the Shopify admin, then it shouldn't be configured to be.

#### Anchor to Configure via the CLIConfigure via the CLI

If you're managing your app with [Shopify CLI](https://shopify.dev/docs/apps/build/cli-for-apps), you can set the embedded configuration in your `shopify.app.toml` file:

1. Open your `shopify.app.toml` file in the root of your app directory.
2. Set the `embedded` property to `false`:
	embedded = false
3. To make your app configuration changes live, release a new app version with [`shopify app deploy`](https://shopify.dev/docs/api/shopify-cli/commands/app/deploy). Learn more about [app configuration](https://shopify.dev/docs/apps/build/cli-for-apps/app-configuration).

#### Anchor to Configure via the Dev DashboardConfigure via the Dev Dashboard

If you're managing your app with Dev Dashboard, you can set the embedded configuration in the UI:

1. Log in to your [Dev Dashboard](https://dev.shopify.com/dashboard).
2. Click **Apps**.
3. Select your app from the list.
4. Click **Versions**, then **Create a version**.
5. In the **URLs** section, ensure the **Embed app in Shopify admin** option is not selected.
6. Click **Release** and enter an optional version name and message.
7. Click **Release** again to confirm the release of a new version.

### Anchor to The app is rendered in the Shopify admin, but isn't following the expected,\[object Object\], guidelinesThe app is rendered in the Shopify admin, but isn't following the expected frame-ancestors guidelines

This scenario uses the following example values:

- `Fraud Filter` as the app
- `cambridgetestshop-staging.myshopify.com` as the shop
	To validate whether `Fraud Filter` implements the expected headers, follow these steps:
1. Log in to the `cambridgetestshop-staging` shop.
2. Click **Apps**.
	![Screenshot showing how to navigate to the apps page](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/apps_sidebar-DQKAHPk4.png)
3. Right-click anywhere on the page and select **Inspect**.
	![Screenshot showing how to inspect a web page](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/inspect_page-PnHXzdV-.png)
4. Select the **Network** tab.
5. Load your app by clicking on its name. The content of the **Network** tab will start to change.
	![Screenshot showing the fraud filter app within the apps page](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/fraud_filter_app-DOuxrwek.png) ![Screenshot showing requests in the network inspector](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/requests_network_inspector-R5cAp3vz.png)
6. Click **Doc** in the **Network** tab to filter requests for documents.
	![Screenshot showing how to filter requests for documents in the network inspector](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/doc_filter-Rk11Zb0E.png)
7. Click the document to load a panel with more details.
	- If there's more than one document, then select the last one in the list.
![Screenshot showing filtered requests for documents in the network inspector](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/filtered_docs-BU7r3Z2K.png)
8. Check the **Request URL**. The URL should be from the app's domain. In this scenario, the **Request URL** is from the *Fraud Filter* app domain.
	![Screenshot showing the filtered request for fraud filter](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/fraud_filter_response-DnIP8EEd.png)
9. Check that the "frame-ancestors" directive is included in the "Content-Security-Policy" header.
	![Screenshot showing the response headers for fraud filter](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/security/fraud_filter_response_headers-CD0xornj.png)

In this scenario, the directive is correctly included for the `cambridgetestshop-staging.myshopify.com` shop.

---

---
