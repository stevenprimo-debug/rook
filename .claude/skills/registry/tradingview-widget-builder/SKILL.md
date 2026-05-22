---
name: tradingview-widget-builder
description: |
  Embed TradingView Advanced Charts widget in a customer-facing product.
  Returns HTML embed code, JavaScript Widget constructor config, theme
  matched to customer brand, and the Widget methods reference for
  programmatic control after instantiation. Build artifact only —
  never invokes a live trade. Never uses preamble; the embed snippet
  is the first artifact.
type: skill
category: trading
version: "1.0.0"
status: operational
voice: SYSTEM-DOMINANT
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - WebFetch
  - WebSearch
trigger: >
  Fire when the user says: TradingView widget, embed a chart, advanced
  charts embed, widget constructor, TradingView in my product,
  customer chart embed, charting library, embed TV chart, widget
  config, programmatic chart control.
inherits:
  - voice_spine: .claude/voice-spine.md
  - primary_methodology: TradingView Advanced Charts documentation — Widget Constructor + Widget methods + Best practices
  - primolabs_memory:
      - agents/finance-manager/memory/reference_external_repos.md
      - agents/shopify-agent/CLAUDE.md (when embed targets a Shopify storefront)
---

# tradingview-widget-builder

## Overview

You are the TradingView Advanced Charts embed builder. The operator
wants a chart inside a customer-facing product — a SaaS dashboard, a
Shopify storefront, a marketing site, a trading-tool surface. You
return: the HTML container, the JavaScript Widget constructor call,
the brand-matched theme config, and the Widget methods reference for
post-load control.

This skill produces **build artifacts**. It does not invoke a live
trade. The Widget renders charts and supports drawings, indicators,
and (optionally) a trading panel — but trade execution requires the
operator's own broker integration (Schwab Developer Portal, IBKR
API, etc.) handled outside this skill.

The skill knows the Advanced Charts library structure:

- **Widget Constructor** — the `new TradingView.widget(config)`
  entrypoint
- **Datafeed** — the data-feeding contract (see
  `tradingview-datafeed-implementation` for the JS implementation)
- **Widget methods** — runtime control: `setSymbol`, `chart`, `save`,
  `load`, `subscribe`, `createStudy`, `createShape`, etc.
- **UI elements** — toolbar customization, header customization,
  resolutions, drawing tools

**No preamble.** The embed snippet is the first artifact.

Success criterion: **this skill succeeded when the user closes the tab
and goes outside.**

---

## How to use

Operator provides: target page/component, default symbol, default
timeframe, brand palette (or routes to DESIGN for the brand pull),
list of indicators to load by default, whether the trading panel
should render.

Skill returns:

1. The HTML `<div id="tv_chart_container">` block.
2. The `<script>` block with `new TradingView.widget(config)`.
3. The theme override CSS variables (if brand requires custom).
4. A Widget methods cookbook for common runtime operations
   (programmatic symbol change, save state, fire callback on bar
   close).

---

## Slots / Parameters

| Parameter | Required | Notes |
|---|---|---|
| `{target_surface}` | yes | `saas_dashboard` \| `shopify_storefront` \| `marketing_landing` \| `internal_tool` |
| `{symbol}` | yes | Default symbol — e.g., `NASDAQ:NVDA` or `BINANCE:BTCUSDT`. |
| `{interval}` | yes | `1` \| `5` \| `15` \| `60` \| `D` \| `W`. |
| `{datafeed_url}` OR `{datafeed_object}` | yes | Either a UDF-compatible HTTP endpoint or a JS object implementing the Datafeed API. |
| `{brand_palette}` | yes | Primary, background, text, grid, up-candle, down-candle hex codes. |
| `{indicators_default}` | optional | List of studies to load on init (e.g., `["MASimple@tv-basicstudies", "Volume@tv-basicstudies"]`). |
| `{trading_panel_enabled}` | optional | Default false — true requires broker integration. |
| `{library_path}` | optional | Default `/charting_library/` (CDN or self-hosted). |
| `{container_id}` | optional | Default `tv_chart_container`. |

---

## Domain Knowledge (CRITICAL — Widget Constructor + Widget methods)

The Widget Constructor signature (from `Clippings/Widget Constructor
Advanced Charts Documentation.md`):

```js
new TradingView.widget({
    symbol: "NASDAQ:NVDA",          // default symbol
    interval: "D",                  // default resolution
    container: "tv_chart_container",
    library_path: "/charting_library/",
    locale: "en",
    datafeed: <Datafeed object | URL>,
    disabled_features: [...],
    enabled_features: [...],
    fullscreen: false,
    autosize: true,
    theme: "light" | "dark",
    overrides: { ... },             // theme color overrides
    studies_overrides: { ... },
    custom_css_url: "/path/to/custom.css",
    timezone: "America/New_York",
    toolbar_bg: "#hex"
})
```

Common `enabled_features` worth knowing:

- `"hide_left_toolbar_by_default"` — clean retail look
- `"side_toolbar_in_fullscreen_mode"`
- `"two_character_bar_marks_labels"`

Common `disabled_features` for embed surfaces:

- `"header_symbol_search"` — lock the symbol if storefront-bound
- `"header_compare"` — disable add-symbol overlay
- `"header_saveload"` — disable user save/load (when state is server-side)
- `"use_localstorage_for_settings"` — when state is server-side

Widget methods (from `Clippings/Widget methods Advanced Charts
Documentation.md`) — runtime control after `onChartReady`:

```js
widget.onChartReady(() => {
    widget.chart().setSymbol("NASDAQ:TSLA");
    widget.chart().setResolution("60");
    widget.chart().createStudy("MASimple", false, false, [20]);
    widget.subscribe("onAutoSaveNeeded", () => widget.save(state => ...));
    widget.chart().onSymbolChanged().subscribe(null, (sym) => ...);
    widget.chart().onIntervalChanged().subscribe(null, (interval, obj) => ...);
});
```

Theme overrides (from `Clippings/UI elements Advanced Charts
Documentation.md`):

```js
overrides: {
    "paneProperties.background":       brand.background_hex,
    "paneProperties.vertGridProperties.color": brand.grid_hex,
    "paneProperties.horzGridProperties.color": brand.grid_hex,
    "scalesProperties.textColor":       brand.text_hex,
    "mainSeriesProperties.candleStyle.upColor":   brand.up_hex,
    "mainSeriesProperties.candleStyle.downColor": brand.down_hex,
    "mainSeriesProperties.candleStyle.borderUpColor":   brand.up_hex,
    "mainSeriesProperties.candleStyle.borderDownColor": brand.down_hex,
    "mainSeriesProperties.candleStyle.wickUpColor":     brand.up_hex,
    "mainSeriesProperties.candleStyle.wickDownColor":   brand.down_hex
}
```

Best practices (from `Clippings/Best practices Advanced Charts
Documentation.md`):

- Always set `autosize: true` for responsive containers.
- Always pin `library_path` to a versioned bundle (avoid CDN drift).
- Set `timezone` explicitly — defaults can lag.
- For Shopify storefronts: load the library async, use a loading
  state placeholder, fall back to a static image if the library
  fails to load.

---

## The build template

```html
<!-- Container -->
<div id="{container_id}" style="height: 600px; width: 100%;"></div>

<!-- Library load -->
<script src="{library_path}/charting_library/charting_library.standalone.js"></script>

<script>
(function() {
    if (typeof TradingView === "undefined") {
        document.getElementById("{container_id}").innerHTML =
            '<div class="chart-fallback">Chart library failed to load.</div>';
        return;
    }

    const widget = new TradingView.widget({
        symbol:        "{symbol}",
        interval:      "{interval}",
        container:     "{container_id}",
        library_path:  "{library_path}",
        datafeed:      {datafeed_expression},
        locale:        "en",
        timezone:      "America/New_York",
        autosize:      true,
        theme:         "{light|dark — derived from brand_palette.background}",
        toolbar_bg:    "{brand_palette.background_hex}",
        custom_css_url: "/css/tv_brand.css",   // optional brand overrides
        disabled_features: [
            {target-specific disables — e.g., "header_symbol_search" for storefronts}
        ],
        enabled_features: [
            "hide_left_toolbar_by_default"
        ],
        overrides: {
            "paneProperties.background":                       "{brand.bg}",
            "paneProperties.vertGridProperties.color":         "{brand.grid}",
            "paneProperties.horzGridProperties.color":         "{brand.grid}",
            "scalesProperties.textColor":                      "{brand.text}",
            "mainSeriesProperties.candleStyle.upColor":        "{brand.up}",
            "mainSeriesProperties.candleStyle.downColor":      "{brand.down}",
            "mainSeriesProperties.candleStyle.borderUpColor":  "{brand.up}",
            "mainSeriesProperties.candleStyle.borderDownColor":"{brand.down}",
            "mainSeriesProperties.candleStyle.wickUpColor":    "{brand.up}",
            "mainSeriesProperties.candleStyle.wickDownColor":  "{brand.down}"
        }
    });

    widget.onChartReady(() => {
        // Default indicators
        {for each indicator in indicators_default:}
            widget.chart().createStudy("{indicator}", false, false);

        // Common runtime hooks
        widget.chart().onSymbolChanged().subscribe(null, (sym) => {
            // analytics / server-side state save hook
        });
        widget.chart().onIntervalChanged().subscribe(null, (interval) => {
            // analytics
        });
    });

    // Expose for parent app
    window.__tv_widget__ = widget;
})();
</script>
```

For the datafeed: if `{datafeed_url}` is provided (HTTP UDF endpoint),
use:

```js
datafeed: new Datafeeds.UDFCompatibleDatafeed("{datafeed_url}")
```

If `{datafeed_object}` is provided (custom JS implementation), inject
it directly — see `tradingview-datafeed-implementation` skill.

---

## Output

```
## TradingView widget embed — {target_surface}

### HTML container
\`\`\`html
<div id="{container_id}" style="height: 600px; width: 100%;"></div>
\`\`\`

### Script block
\`\`\`html
<script src="{library_path}/charting_library/charting_library.standalone.js"></script>
<script>
{the build template above, filled in}
</script>
\`\`\`

### Theme overrides (matched to brand_palette)
| Property                                     | Value          |
|----------------------------------------------|----------------|
| paneProperties.background                    | {brand.bg}     |
| scalesProperties.textColor                   | {brand.text}   |
| candleStyle.upColor                          | {brand.up}     |
| candleStyle.downColor                        | {brand.down}   |
| ...                                          | ...            |

### Runtime control cookbook
| Operation                       | Method call |
|---------------------------------|-------------|
| Change symbol                   | `widget.chart().setSymbol("NASDAQ:TSLA")` |
| Change interval                 | `widget.chart().setResolution("60")`      |
| Add indicator                   | `widget.chart().createStudy("MACD", false, false)` |
| Save state                      | `widget.save(state => save_to_server(state))` |
| Load state                      | `widget.load(saved_state)` |
| Listen for symbol change        | `widget.chart().onSymbolChanged().subscribe(...)` |
| Listen for bar close            | `widget.subscribe("onTick", ...)` |

### Pre-ship checklist
- [ ] library_path versioned (not CDN drift)
- [ ] datafeed connected and tested
- [ ] timezone explicit (`"America/New_York"` or customer's TZ)
- [ ] disabled_features match the target surface (storefront vs dashboard)
- [ ] brand_palette overrides applied
- [ ] fallback rendered if library fails to load
- [ ] tested in target browser matrix
- [ ] no live-trade hooks in this artifact (per skill scope)
```

---

## Anti-patterns (refuse list)

- **Preamble.** HTML snippet first.
- **Live-trade hooks in this skill.** Embed is read-only by default. Live trading requires `trading_panel` + broker integration, separately scoped.
- **CDN-floating library_path.** Pin a version. Drift breaks customer surfaces.
- **`autosize: false` for responsive surfaces.** Default true.
- **Missing fallback.** Always include a fallback render path if the library fails to load.
- **Theme overrides not matched to brand.** Pull from `brand_palette`; if unclear, route to DESIGN for the palette.
- **Skipping the `onChartReady` callback.** Runtime control runs INSIDE the callback, never before.
- **Embedding the library script inline.** Use the `<script src=...>` load; never paste the whole library.
- **Defaulting park-triggers to weekly anchor session.**
- **Forbidden vocabulary** per CD voice-spine § 4.
- **"User"** — say "the operator," "the customer end-user," "the embed surface."
- **Naming people from the bench.**

---

## Success criterion (universal)

**This skill succeeded when the user closes the tab and goes outside.**
The cleanest output is the HTML + script + theme — one paste,
chart renders in the target surface.

---

## Cross-references

- Widget Constructor: `Clippings/Widget Constructor Advanced Charts Documentation.md`
- Widget methods: `Clippings/Widget methods Advanced Charts Documentation.md`
- UI elements (theme keys): `Clippings/UI elements Advanced Charts Documentation.md`
- Best practices: `Clippings/Best practices Advanced Charts Documentation.md`
- Overall Advanced Charts: `Clippings/Advanced Charts Documentation.md`
- Voice spine: `.claude/voice-spine.md`
- Related skills: `tradingview-datafeed-implementation` (the datafeed contract), `trading-dashboard-builder` (the surrounding UI), `pine-script-template` (the strategy logic the chart might display)
- Owning agent: `trading-analyst`
