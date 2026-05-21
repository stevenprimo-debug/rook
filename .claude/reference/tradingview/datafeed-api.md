---
title: Datafeed API | Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/
author: []
published: []
created: 2026-05-12
description: The library allows connecting market data to the chart in two ways:
tags: [clippings]
dept_secondary: [FINANCE]
---
- By using the built-in [UDF adapter](https://www.tradingview.com/charting-library-docs/latest/connecting_data/UDF).
- By implementing your own datafeed via the Datafeed API.

> [!-info] -info
> info
> Note that neither Advanced Charts nor Trading Platform contains any market data. You should use data from your own source or third-party providers.

This documentation section describes the Datafeed API methods and their implementation details. You can also refer to the [How to connect data via Datafeed API](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/implement_datafeed_tutorial/) tutorial for a step-by-step guide.

## Overview

The Datafeed API is a set of methods that you should implement in JavaScript and assign to the [`datafeed`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions#datafeed) property in the [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/configuration/Widget-Constructor). The library calls these methods to access and process data. In response, you should evoke the provided callbacks to pass the data to the library. The diagram below illustrates how the Datafeed API should be integrated with the library and your backend server.

[![Diagram illustrating datafeed architecture](https://www.tradingview.com/charting-library-docs/img/datafeed-architecture-diagram-dark.svg)](https://www.tradingview.com/charting-library-docs/img/datafeed-architecture-diagram-light.svg)

### Asynchronous callbacks

As mentioned [above](#overview), you should evoke callbacks to pass data to the library. Note that all callbacks should be evoked **asynchronously**. In context of the JavaScript Event Loop, the callbacks can only be evoked within different MacroTask. Otherwise, the *Uncaught RangeError: Maximum call stack size exceeded* [issue](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Datafeed-Issues#maximum-call-stack-size-exceeded) might occur.

If you have data ready at the time of a request, you can set a delay as demonstrated below to ensure that a callback is only evoked when the library is ready.

```javascript
setTimeout(() => { historyCallback(data); }, 0);
```

Note that the library can modify bar data that you provide utilizing callbacks. Pass a copy of the data to avoid potential issues.

## List of methods

All Datafeed API methods are divided into three groups:

- [Required methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/required-methods) — a minimum set of methods that you should implement to connect data to the chart.
- [Trading Platform methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/trading-platform-methods) — the methods that are required to enable most of the [Trading Platform](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/) features including the [Order Ticket](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/order-ticket), [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List), and [Depth of Market](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#depth-of-market).
- [Additional methods](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/additional-methods) — the methods that allow you to enable additional features such as marks on the chart and a countdown to the bar close.