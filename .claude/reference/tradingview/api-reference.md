---
title: API Reference | Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/api/
author: []
published: []
created: 2026-05-12
description: Structure
tags: [clippings]
category: vendor-api-reference
rook-relevance: high
rook-consumers: trading-analyst, software-dev-team
---
## Structure

The API is structured as a modular system of types, interfaces, and enumerations. The library's API is divided into three modules, where each module consists of interfaces that define properties and methods specific to its functionality.

### Charting Library module

The [Charting Library module](https://www.tradingview.com/charting-library-docs/latest/api/modules/Charting_Library) is designed to manage chart creation, customize the UI appearance, and handle user interactions.

#### Key features

- Manage drawings and indicators displayed on the chart.
- Customize chart themes, layouts, and behaviors.
- Handle user interactions through events and methods.

#### Common interfaces

## [Advanced Charts Widget Options](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/)

Properties for Advanced Chart widget to customize its appearance and behavior

## [Trading Platform Widget Options](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/)

Properties for Trading Platform widget to customize its appearance and behavior

## [IChartingLibrary Widget](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget/)

Primary interface for library interactions

## [IChart Widget](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/)

Primary interface for chart interactions, such as creating drawings and indicators

### Datafeed module

The [Datafeed module](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed) is designed to integrate custom data sources and controlling data flow to the chart.

#### Key features

- Connect any market data source to Advanced Charts.
- Handle custom symbology logic to map your backend symbols to TradingView's requirements.
- Synchronize chart data with live market data updates.

#### Common interfaces

## [SymbolInfo](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/)

Defines the structure and metadata for symbols, including properties like ticker and exchange

## [IExternal Datafeed](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.IExternalDatafeed)

Acts as the entry point for connecting custom datafeeds to the library

## [IDatafeed Chart](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.IDatafeedChartApi)

Provides methods for fetching and managing historical and real-time data

## [IDatafeed Quotes](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.IDatafeedQuotesApi)

Enables the retrieval and management of real-time market quotes

### Broker module

The [Broker module](https://www.tradingview.com/charting-library-docs/latest/api/modules/Broker) is designed to integrate trading capabilities provided by [Trading Platform](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/).

#### Key features

- Enable creating market, limit, and other order types directly from the chart interface.
- Provide real-time market quotes to power trading features like the [Order Ticket](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/order-ticket), [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List), and [Depth of Market](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/depth-of-market).
- Support multiple account setups for users with diverse trading needs.

#### Common interfaces

## [Broker API](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IBrokerTerminal)

Enables trading features and connects the charts with your trading logic

## [Trading Host](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IBrokerConnectionAdapterHost)

Receives trading information from your backend server and provides the library with updates

## [Broker configuration](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.SingleBrokerMetaInfo)

Defines configuration for additional Trading Platform features

## Best practices for navigation

1. Identify the module relevant to your task: [creating charts](#charting-library-module), [managing datafeeds](#datafeed-module), or [enabling trading](#broker-module).
2. Examine the available interfaces within the module. Each interface defines a set of properties and methods relevant to a specific feature or functionality.
3. Follow type links and explore enumerations. If a property uses a non-primitive type, follow the link to the corresponding type definition. This will reveal additional properties and their relationships.
4. Get back into the context and use your browser’s navigation to return to higher-level modules or interfaces when needed.

### Browse TypeScript definition

Alternatively, if you are more comfortable browsing the API through a TypeScript definition file, you can use the following links:

- [Charting Library and Broker TypeScript definition](https://github.dev/tradingview/charting_library/blob/master/charting_library/charting_library.d.ts)
- [Datafeed TypeScript definition](https://github.dev/tradingview/charting_library/blob/master/charting_library/datafeed-api.d.ts)

#### Keyboard shortcuts for Visual Studio Code

| Action | Windows shortcut | macOS shortcut |
| --- | --- | --- |
| Find | Ctrl + F | Cmd + F |
| Go to definition | F12 or Ctrl + Click | F12 or Cmd + Click |
| Go back | Ctrl + \- | Cmd + \- |