---
title: Shopify CLI
source: https://shopify.dev/docs/api/shopify-cli#upgrade
author: []
published: []
created: 2026-05-11
description: Shopify CLI is a command-line interface tool that helps you generate and work with Shopify apps, themes and custom storefronts.
tags: [clippings]
---

## Anchor to InstallationInstallation

This installs Shopify CLI globally on your system, so you can run `shopify` commands from any directory. Find out more about the available commands by running `shopify` in your terminal.

---

## Anchor to CommandsCommands

Shopify CLI groups commands into topics. The command syntax is: `shopify [topic] [command]`. Refer to each topic section in the sidebar for a list of available commands.

Or, run the `help` command to get this information right in your terminal.

---

## Anchor to Upgrade Shopify CLIUpgrade Shopify CLI

We recommend that you always use the latest version of Shopify CLI if possible. To upgrade, run `version` to check the current version and determine if there are any updates available. Run the [install](#installation) command to upgrade to the latest CLI version.

---

## Anchor to Network proxy configurationNetwork proxy configuration

When working behind a network proxy, you can configure Shopify CLI (version 3.78+) to route connections through it:

1. Set the proxy for HTTP traffic:
	export SHOPIFY\_HTTP\_PROXY=http://proxy.com:8080
2. Optionally, set a different proxy for HTTPS traffic:
	export SHOPIFY\_HTTPS\_PROXY=https://secure-proxy.com:8443
	If not specified, the HTTP proxy will be used for all traffic.
3. For authenticated proxies, include credentials in the URL:
	export SHOPIFY\_HTTP\_PROXY=http://username:password@proxy.com:8080

---

## Anchor to Usage reportingUsage reporting

Anonymous usage statistics are collected by default. To opt out, you can use the environment variable `SHOPIFY_CLI_NO_ANALYTICS=1`.

---

## Anchor to Contribute to Shopify CLIContribute to Shopify CLI

Shopify CLI is open source. [Learn how to contribute](https://github.com/Shopify/cli/wiki/Contributors:-Introduction) to our GitHub repository.

---

## Anchor to Where to get helpWhere to get help

- [Shopify CLI and Libraries](https://community.shopify.dev/c/shopify-cli-libraries/14) - Report any issues with the CLI.
- [Dev Platform](https://community.shopify.dev/c/dev-platform/32) - Ask any questions and learn more about the Dev Platform powering the CLI.

---

## Anchor to ResourcesResources

[Start building a theme](https://shopify.dev/docs/themes/getting-started/create)

[Learn how to set up your theme development environment and create a new theme](https://shopify.dev/docs/themes/getting-started/create)

[Start building an app](https://shopify.dev/docs/apps/getting-started/create)

[Learn how to set up your app development environment and start building](https://shopify.dev/docs/apps/getting-started/create)

---
