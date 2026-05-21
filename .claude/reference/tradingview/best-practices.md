---
title: Best practices | Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/resources/Best-Practices
author: []
published: []
created: 2026-05-12
description: This article describes the best practices for integrating the library into your website or mobile application.
tags: [clippings]
---
This article describes the best practices for integrating the library into your website or mobile application.

## Separate additional features from the library

The library is used to display charts, prices, and technical analysis tools. You can find a list of included features in the [Key features](https://www.tradingview.com/charting-library-docs/latest/introduction#key-features) article.

If you need additional features like chats, special symbol lists, hot deals, advertisements, etc., you should implement them outside of the library. You can still integrate them to the library using the [API](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi).

## Choose an appropriate data connection approach

Pay attention to the differences between implementing a datafeed in JavaScript via the [Datafeed API](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/) and using the predefined implementation with a server that responds in the [UDF](https://www.tradingview.com/charting-library-docs/latest/connecting_data/UDF) format. Refer to the following topic for more information: [Connecting Data](https://www.tradingview.com/charting-library-docs/latest/connecting_data/). If you need really fast data updates or data streaming, you can use WebSockets.

## Provide correct amount of data

Most issues with the library appear because data is provided incorrectly. Consider the following topic for more information: [Datafeed API](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/required-methods#correct-amount-of-data). Note that when you specify [Marks](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Marks), you should provide data that matches the requested range.

## Consider the chart's size

The smallest meaningful size that the library supports is 500×500 px. Avoid making charts smaller because they look messy. We recommend that you hide some UI elements if you need charts smaller than those mentioned above. Refer to the [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/configuration/Widget-Constructor#chart-size) topic for more information on how to specify the chart's size.

## Localize your chart

The library [supports a variety of languages](https://www.tradingview.com/charting-library-docs/latest/configuration/Localization). Use the one that fits your users' needs.

## Enable debug logs during development

Set the [`debug`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions#debug) property to `true` in [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/configuration/Widget-Constructor) to enable logs. We recommend that you enable the debug mode during the development and disable this mode in the production to speed up the code execution.

## If you face issues

First, [update](https://www.tradingview.com/charting-library-docs/latest/releases/Update-Library) the library to the latest version — many issues are resolved in newer releases. If the issue persists, [enable debug mode](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/enable-debug-mode) to gather detailed logs and refer to the [Troubleshooting](https://www.tradingview.com/charting-library-docs/latest/troubleshooting/) guide for diagnostic steps and reporting instructions.

## Avoid using undocumented features

All features that are not mentioned in the documentation are subject to change without any warnings and backward compatibility. Also, altering the source code is strictly prohibited by the legal agreement you signed.

## Avoid using demo datafeed on a production website

The demo datafeed is not designed for real usage. It might be unstable and cannot withstand high loads.

## Speed up load times

We recommend that you use the following protocols to speed up load times:

- HTTP/2 or higher
- TLS 1.3 or higher

Additionally, consider the following optimizations to reduce the library size:

- Compress the library's HTML files using Gzip or Brotli when sending them to a client.
- Remove unused locales from the [bundle](https://www.tradingview.com/charting-library-docs/latest/quick-start#package-structure) if your app does not support them.

> [!-warning] -warning
> caution
> The library does not support Rocket Loader by Cloudflare. Avoid using it.

## Set minimum expiration time for charting\_library.js

All files in the library contain hash in their names except `charting_library.js` that you add to your HTML files. When you update the library to a newer version, all file names are changed as well. If a browser loads `charting_library.js` from the cache, then all the links in this file are broken. The expiration time for this file should be set to the minimum to prevent its caching.