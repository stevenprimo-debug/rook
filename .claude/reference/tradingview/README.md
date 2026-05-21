# TradingView Advanced Charts (Charting Library) — shared reference

**Sources:**
- https://www.tradingview.com/charting-library-docs/latest/introduction
- https://www.tradingview.com/charting-library-docs/latest/api/
- https://www.tradingview.com/charting-library-docs/latest/connecting_data/
- https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed_API.IDatafeed

**Files in this folder** (all clipped from official docs, 2026-05-20):

| File | Source page | When to load |
|---|---|---|
| `README.md` | (this file) | Always — overview, modules, embedding, ROOK integration, the "no public data API" reality |
| `intro.md` | `/introduction` | First read — key features, system requirements |
| `getting-started.md` | `/getting_started/` | When standing up a new chart embed for the first time |
| `connecting-data.md` | `/connecting_data/` | When wiring Tradovate/Schwab data INTO the chart via Datafeed adapter |
| `widget-constructor.md` | `/widget_constructor/` | When instantiating the widget — config options |
| `widget-methods.md` | `/widget_methods/` | When interacting with the widget at runtime (change symbol, save layout) |
| `ui-elements.md` | `/ui_elements/` | When customizing the chart UI (chart types, indicators, drawings, sessions) |
| `api-reference.md` | `/api/` | Full top-level API surface — interfaces, modules, type index |
| `datafeed-api.md` | `/api/interfaces/Datafeed_API.IDatafeed` | The Datafeed interface itself (46 lines, the contract you implement) |
| `module-datafeed.md` | `/api/modules/Datafeed_API` | **Authoritative implementation guide — 395 lines** — full module spec with types, methods, callback shapes. The file you live in when actually wiring data. |
| `trading-platform-methods.md` | `/api/...Trading_Platform_API` | Broker module methods — only needed if enabling in-chart execution |
| `best-practices.md` | `/best_practices/` | Read before building — the patterns TradingView recommends |
| `build-ai-library-assistant.md` | `/tutorials/build-ai-library-assistant/` | TradingView's own guidance on building an AI assistant against the library — relevant to ROOK's positioning |

**Status:** v1 reference, live-link these on every fresh use — the API evolves quarterly.
**Use case:** Embed live TradingView Advanced Charts into ROOK product surfaces (operator dashboard, cohort customer dashboards, trade-review tools). NOT for webhooks — webhooks are a separate inbound surface handled by an alert receiver.

## What TradingView is NOT

**There is no general-purpose REST or WebSocket API for users to extract raw market data or indicator values from TradingView.** TradingView's official APIs are exclusively for:
1. **Brokers integrating into the TradingView platform** (broker sends data TO TradingView for display in their hosted UI)
2. **Developers embedding Advanced Charts into custom applications** (this doc — embed TV's UI in your app)

For programmatic raw-data access, traders rely on unofficial community packages (`tvdatafeed`, Apify TradingView scrapers) — these fall outside TradingView's site policies and are NOT part of ROOK's supported stack. ROOK pulls market data from broker APIs (Tradovate, Schwab) and FEEDS it into the Advanced Charts widget via the Datafeed contract.

## Key features (from official Advanced Charts intro)

- Mobile-friendly, multi-touch
- 13+ chart types (Candles, Bars, Area, Baseline, Heikin Ashi, etc.)
- 100+ indicators (build custom in JS)
- 110+ drawing tools
- Symbol comparison (multi-series with auto timezone/session alignment)
- Extended hours (pre/post/regular market sessions)
- Flexible resolutions (ticks → years, custom resolutions auto-built from 1-min)
- Theming (dark/light defaults, brand-custom colors/fonts)
- Framework-agnostic (React, Angular, Vue, vanilla JS)
- Mobile WebView embeddable (iOS, Android)

## System requirements

- **Hosting:** server to host the library files (TV does not provide a CDN — gated download via license portal)
- **Data source:** **you provide it.** The library has no market data — it expects a Datafeed adapter you implement
- **Browser:** all major modern browsers + mobile variants

## What it is

A JavaScript widget library that drops a full TradingView chart into your own web app. You provide:
- **The chart shell** (`ChartingLibraryWidgetOptions` + `IChartingLibraryWidget`) — appearance, layout, theming
- **The data** (Datafeed module) — your OHLC/quotes feed, can come from Tradovate, Schwab, or any source
- **Trading hooks** (Broker module, optional) — connect the chart's order buttons to your broker so users trade directly from the chart

TradingView hosts NONE of your data. The library is a UI shell + a data-adapter contract. You implement the contracts.

## Three modules

### Charting module (the widget itself)

| Object | Purpose |
|---|---|
| `ChartingLibraryWidgetOptions` | Config object passed at widget construction — symbol, interval, theme, locale, container element ID |
| `IChartingLibraryWidget` | The widget handle — methods to change symbol, save/load layouts, attach event listeners |
| `IChartWidgetApi` | Per-chart API for drawing tools, indicators, study events |

### Datafeed module (you implement)

| Interface | What you implement | Reversibility |
|---|---|---|
| `IExternalDatafeed` | Entry point — TradingView calls this first | N/A (read-only data shape) |
| `SymbolInfo` | Symbol metadata struct (ticker, exchange, timezone, session, pricescale) | N/A |
| `IDatafeedChartApi` | `onReady`, `searchSymbols`, `resolveSymbol`, `getBars`, `subscribeBars`, `unsubscribeBars` | Read-only — Y |
| `IDatafeedQuotesApi` | Real-time quotes for watchlist / DOM | Read-only — Y |

The datafeed contract is the integration work. For Tradovate-backed feed: implement `getBars` calling Tradovate's historical bars endpoint, implement `subscribeBars` against Tradovate's WebSocket market-data stream.

### Broker module (you implement, optional)

| Interface | What you implement | Reversibility |
|---|---|---|
| `IBrokerTerminal` | Account state, positions, orders, trading actions | **N (mixed — reads Y, writes N)** |
| `IBrokerConnectionAdapterHost` | Receives broker push events back into the chart | Y (events only) |
| `SingleBrokerMetaInfo` | Capability flags (which order types, sessions, etc.) | N/A |

If the broker adapter is wired, users see Buy/Sell buttons inside the chart and can place orders without leaving the chart UI. This is the path to "one-click trading from chart" — and the operator-confirm gate has to live inside the broker adapter's `placeOrder` method, NOT in TradingView's UI (which can't know your reversibility class).

## Auth / licensing

- Free for personal / non-commercial embeds
- Commercial use (cohort product surfaces, anything monetized) requires TradingView's Charting Library license — apply at https://www.tradingview.com/charting-library-getting-started/
- License grants access to the JS bundle (not on public CDN — gated download via the license portal)
- Tradingview.com SDK assets are pulled from `s3.tradingview.com` once the bundle is hosted on your origin

## Embedding pattern (the integration sequence)

```javascript
// 1. Page loads tv.js (TradingView's bundle, served from your origin)
// 2. Instantiate the widget with config + datafeed adapter
const widget = new TradingView.widget({
  symbol: "AAPL",
  interval: "5",
  container_id: "chart",
  datafeed: new MyTradovateDatafeed(),  // your adapter, conforms to IDatafeedChartApi
  broker_factory: (host) => new MyTradovateBroker(host),  // optional — enables in-chart trading
  library_path: "/charting_library/",
  locale: "en",
  theme: "dark",
});

// 3. Widget calls your datafeed's onReady() first
// 4. User picks a symbol → resolveSymbol → getBars (historical) → subscribeBars (live)
// 5. If broker_factory provided → user sees Buy/Sell → IBrokerTerminal.placeOrder → operator-confirm gate → Tradovate/Schwab order endpoint
```

## ROOK integration points

| Surface | Module needed | Owning agent |
|---|---|---|
| Operator trading dashboard | Charting + Datafeed (Tradovate-backed) | trading-analyst (builds), r-and-d-lead (designs the dashboard) |
| Cohort customer trading view (read-only) | Charting + Datafeed (whatever the customer's broker exposes) | r-and-d-lead (productizes), shopify-agent (if sold as ROOK add-on) |
| In-chart execution (operator only) | Charting + Datafeed + Broker (Tradovate or Schwab adapter) | trading-analyst with reversibility gate enforced in `placeOrder` |
| Trade-review tooling | Charting + Datafeed (replays from historical) | trading-analyst |

## What this does NOT cover

- Pine Script publishing (no public API — browser-only workflow)
- TradingView alert webhooks (separate inbound system; handled by a Cloudflare Worker alert receiver — see `agents/trading-analyst/memory/api-docs/tradingview-webhooks.md` when that exists)
- Public chart screenshot URLs (`s3.tradingview.com/snapshots/...`) — separate scraping target

## Notes for first-use

1. Apply for Charting Library license via the URL above; commercial use requires it
2. Implement `IExternalDatafeed` + `IDatafeedChartApi` against the operator's data source (Tradovate first — see sibling `tradovate/` folder)
3. Test against TradingView's UDF reference implementation before wiring live data
4. Broker adapter is optional v1; defer to v1.1 unless in-chart execution is on the launch list
5. Theme matches ROOK brand — dark default, accent colors from `.claude/memory/rook_brand.md`
6. Re-verify endpoint shapes against the live URL (top of this file) on every fresh build — the lib's API is versioned but not strict-semver
