# Graph Report - .claude\reference  (2026-05-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 124 nodes · 167 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1b5caa7a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]

## God Nodes (most connected - your core abstractions)
1. `Tradovate API Reference` - 11 edges
2. `TradingView API Structure (3 modules)` - 10 edges
3. `Tradovate Connector` - 10 edges
4. `Templates README` - 8 edges
5. `Datafeed API` - 7 edges
6. `TradingView Advanced Charts Overview` - 7 edges
7. `Datafeed Module` - 7 edges
8. `Shopify App Package for React Router` - 7 edges
9. `Subscribe to a Topic Using GraphQL Admin API` - 7 edges
10. `Featuresets` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Operator Confirm Gate` --semantically_similar_to--> `Operator Confirm Gate (Tradovate)`  [INFERRED] [semantically similar]
  tradingview/README.md → tradovate/README.md
- `MyTradovateDatafeed (example adapter)` --conceptually_related_to--> `Tradovate Connector`  [INFERRED]
  tradingview/README.md → tradovate/README.md
- `MyTradovateBroker (example adapter)` --conceptually_related_to--> `Tradovate Connector`  [INFERRED]
  tradingview/README.md → tradovate/README.md
- `IDatafeedChartApi Interface` --conceptually_related_to--> `Required Methods`  [INFERRED]
  tradingview/README.md → tradingview/datafeed-api.md
- `TradingView Advanced Charts Overview` --references--> `Tradovate Connector`  [EXTRACTED]
  tradingview/README.md → tradovate/README.md

## Communities (17 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (18): GET /account/list, POST /auth/accesstokenrequest, GET /auth/renewaccesstoken, Bearer Token Auth, POST /order/cancelorder, POST /order/liquidateposition, POST /order/modifyorder, POST /order/placeorder (+10 more)

### Community 1 - "Community 1"
Cohesion: 0.22
Nodes (18): Amazon EventBridge, App Configuration File, FulfillmentOrder Object, Google Cloud Pub/Sub, GraphQL Admin API, React Router, Shopify CLI Tool, Shopify Functions (+10 more)

### Community 2 - "Community 2"
Cohesion: 0.16
Nodes (15): Additional Methods, Asynchronous Callbacks Pattern, Datafeed API, Required Methods, Trading Platform Methods (Datafeed), UDF Adapter, Widget Constructor, Featuresets (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (13): IBrokerConnectionAdapterHost, IDatafeedQuotesApi, LibrarySymbolInfo (SymbolInfo), SingleBrokerMetaInfo, TradingTerminalWidgetOptions, TradingView API Structure (3 modules), Charting Module, ChartingLibraryWidgetOptions (+5 more)

### Community 4 - "Community 4"
Cohesion: 0.23
Nodes (13): Non-Disclosure Agreement, SaaS Subscription Agreement, Software Development Agreement, Statement of Work, Master Software Development Agreement (Pro-customer), Confidentiality and Non-Disclosure Agreement, Templates README, SaaS License Agreement (+5 more)

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (11): Tradovate WebSocket Market Data, Bar interface (OHLCV), Datafeed Module Authoritative Spec, DOMData / DOMLevel (Depth of Market), HistoryMetadata, Datafeed Module, IDatafeedChartApi Interface, IDatafeedQuotesApi Interface (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (6): Broker Module, IBrokerConnectionAdapterHost Interface, IBrokerTerminal Interface, MyTradovateBroker (example adapter), Operator Confirm Gate, ROOK In-Chart Execution

### Community 7 - "Community 7"
Cohesion: 0.7
Nodes (5): Model Context Protocol (MCP), Universal Commerce Protocol (UCP), Agentic Commerce, Build a Storefront AI Agent, Storefront MCP

### Community 8 - "Community 8"
Cohesion: 0.4
Nodes (5): Content Security Policy, frame-ancestors Directive, Secure Your Network Service Ports, Set Up iframe Protection, Shorten URLs with Care

### Community 9 - "Community 9"
Cohesion: 0.6
Nodes (5): TradingView Charting Library, TradingView Datafeed API, TradingView Advanced Charts Best Practices, Build AI Library Assistant for Advanced Charts, TradingView Advanced Charts Troubleshooting

### Community 10 - "Community 10"
Cohesion: 0.5
Nodes (4): App Bridge, Customize Shopify Inbox Chat Settings and Appearance, Integrating with the Shopify Admin, Mobile Support

### Community 11 - "Community 11"
Cohesion: 0.67
Nodes (3): Fibonacci/Gann drawing tools, Heikin Ashi chart type, TradingView Advanced Charts Introduction

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (3): Resolution widget (timeframe), Symbol Search widget, TradingView UI Elements Guide

## Knowledge Gaps
- **42 isolated node(s):** `TradingTerminalWidgetOptions`, `IDatafeedQuotesApi`, `IBrokerConnectionAdapterHost`, `SingleBrokerMetaInfo`, `LibrarySymbolInfo (SymbolInfo)` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TradingView Advanced Charts Overview` connect `Community 2` to `Community 0`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `Tradovate Connector` connect `Community 0` to `Community 2`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `TradingView API Structure (3 modules)` connect `Community 3` to `Community 5`, `Community 6`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Tradovate Connector` (e.g. with `MyTradovateDatafeed (example adapter)` and `MyTradovateBroker (example adapter)`) actually correct?**
  _`Tradovate Connector` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `TradingTerminalWidgetOptions`, `IDatafeedQuotesApi`, `IBrokerConnectionAdapterHost` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._