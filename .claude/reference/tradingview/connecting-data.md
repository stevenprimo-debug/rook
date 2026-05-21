---
title: Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/troubleshooting/
author: []
published: []
created: 2026-05-12
description: Overview
tags: [clippings]
---
## Overview

This article is a starting point for diagnosing and resolving issues you might encounter while implementing the library.

> [!-success] -success
> tip
> For almost any issue, [enabling the debug mode](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/enable-debug-mode) is the most effective way to gather more information.

## API-specific troubleshooting

If your issue is related to a specific API, check the dedicated guides, as they cover the most common issues.

## Memory leaks

If you observe increasing memory consumption that never decreases, you may have a memory leak. Here are the recommended steps to troubleshoot the issue:

### 1\. Verify proper chart cleanup logic

The most common source of memory leaks occurs when the chart widget is removed, but its resources are not fully released because your code holds a reference to it. Ensure your cleanup code does all of the following:

- Calls the [`remove`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#remove) method when trying to remove the chart.
- Unsubscribes from all data subscriptions.
- Removes any references to the chart or parts of its API from your application's scope.

For a technical background in JavaScript, see the [Memory management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management) guide.

### 2\. Check for high-frequency data updates

High memory consumption can also be caused by an excessive number of real-time updates. This forces the library to a constant, resource-intensive re-rendering.

1. Enable debug mode to see the flow of data. Refer to our guide: [How to enable debug mode](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/enable-debug-mode).
2. In the debug logs, look for a very high volume of updates in a short period.

If you find excessive updates, the solution is to throttle or batch them on your end before sending them to the library.

### 3\. Isolate the library component

Once you've confirmed that your cleanup logic and data flow are correct, check if the issue is caused by the library or your application.

1. Create an isolated test page with only the library and the simplest configuration needed.
2. Remove all other frameworks, components, and third-party scripts from the page.
3. Monitor the memory usage.

If the memory leak disappears, the issue lies within your application or another integration, not the library. You should investigate your application's code to find the source of the leak.

If you can still reproduce the leak with only the library on a blank page, proceed with the following step.

### 4\. Record memory heap snapshot

If you have completed all the steps above and are confident the issue lies within the library, capture the leak-proof and report a GitHub issue.

1. Open your browser's Developer Tools and go to the Memory tab.
2. Click the record button to take a heap snapshot.
3. [Open an issue](#still-stuck) on our GitHub repository.
4. Attach the snapshot file you recorded.

## Content Security Policy errors

If you see errors mentioning CSP or `blob`, your Content Security Policy (CSP) may be blocking some library features such as displaying screenshots, logos, or emojis/icons.

A typical error message looks like:

```javascript
Refused to load the image '<URL>' because it violates the following Content Security Policy directive: "img-src 'self' blob data"
```

We recommend adjusting your CSP rules to allow the required sources. Refer to the [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) article for guidance.

If changing CSP is not possible, enable the [`iframe_loading_compatibility_mode`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#iframe_loading_compatibility_mode) featureset. This uses `about:blank` as the source URL and builds the iframe HTML using `document.write`, providing a fallback for environments with strict CSP rules.

## Still stuck?

If you didn't find a solution in the documentation, first make sure you are using the [latest version](https://www.tradingview.com/charting-library-docs/latest/releases/Update-Library) of the library — the issue may already be resolved in a newer release. If the issue persists, report it through [GitHub Issues](https://github.com/tradingview/charting_library/issues "The repository is private.") 🔐 (access is [restricted](https://www.tradingview.com/charting-library-docs/latest/quick-start#1-get-access "Click to open the 'Getting Access' section.")).

To help us and the community understand your issue, include the following details:

- A clear and concise description of what the issue is.
- Any error messages encountered.
- Step-by-step instructions to reproduce it.
- The library version you are using.
- The full logs with [debug mode enabled](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/enable-debug-mode).
- The symbol your issue is related to.