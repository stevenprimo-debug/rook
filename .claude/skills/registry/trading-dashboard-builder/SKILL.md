---
name: trading-dashboard-builder
description: |
  Generate a trading dashboard UI surface — positions, P&L, watchlist,
  alerts, embedded chart. Returns layout (grid / panel arrangement),
  component spec for each panel, data-binding contract (datafeed +
  positions API), and the design tokens that match the operator's
  brand. Cross-references the designer agent's frontend-design skills
  for taste; cross-references tradingview-widget-builder for the chart
  panel. Never uses preamble; the layout spec is the first artifact.
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
  Fire when the user says: trading dashboard, build a dashboard,
  positions panel, P&L widget, watchlist, alerts panel, dashboard
  layout, trader UI, charting tool UI, build the trader interface,
  Schwab dashboard, broker dashboard.
inherits:
  - voice_spine: .claude/voice-spine.md
  - primary_methodology: TradingView Advanced Charts UI elements + Schwab Developer Portal patterns (read-only patterns for positions/orders/quotes) + frontend-design skills via designer agent
  - primolabs_memory:
      - agents/finance-manager/memory/trading_rules.md
      - agents/finance-manager/memory/reference_external_repos.md
      - agents/shopify-agent/CLAUDE.md (when dashboard is product-facing)
---

# trading-dashboard-builder

## Overview

You are the dashboard builder. The operator wants a trader-facing UI
that surfaces: positions, P&L (realized + unrealized), watchlist,
alerts, and an embedded chart. You return:

1. **Layout** — the grid / panel arrangement and responsive
   breakpoints.
2. **Per-panel component spec** — what each panel renders, what data
   it binds to, what interactions it supports.
3. **Data-binding contract** — the API shape each panel needs
   (positions endpoint, quote stream, alerts endpoint, account
   summary endpoint).
4. **Design tokens** — colors, typography, spacing, density level
   (compact vs comfortable) — sourced from the brand palette.

This skill is **not** the chart itself (that's
`tradingview-widget-builder`) and **not** the broker integration
(that's an Anthropic Managed Agent — Schwab Developer Portal). It is
the **UI surface that surrounds** the chart and consumes the broker's
read APIs.

The skill knows the standard trader-dashboard archetypes:

- **Pro layout** — chart-dominant (60-70% of viewport), positions
  strip across bottom, watchlist sidebar, alerts as a corner widget.
- **Compact layout** — for mobile / tablet — chart on top, positions
  as a swipeable section, watchlist + alerts as tabs.
- **Multi-chart layout** — 4-up grid, no watchlist, status bar only.

Default archetype is **Pro layout** unless the target surface is
mobile-first.

**No preamble.** The layout spec is the first artifact.

Success criterion: **this skill succeeded when the user closes the tab
and goes outside.**

---

## How to use

Operator provides: target surface (web / mobile / desktop), target
archetype (pro / compact / multi-chart), broker API capabilities
(read-only positions / quotes / alerts; trading panel optional),
brand palette (or routes to DESIGN for the brand pull), density
preference, and the watchlist seed.

Skill returns:

1. The layout (grid + responsive breakpoints).
2. Per-panel spec (positions / P&L / watchlist / alerts / chart).
3. The API contract each panel needs.
4. The design-token block.
5. The pre-ship checklist.

The actual frontend code (React / Vue / Svelte) is downstream — this
skill specs the surface; designer agent's frontend-design skills
implement.

---

## Slots / Parameters

| Parameter | Required | Notes |
|---|---|---|
| `{target_surface}` | yes | `web_desktop` \| `web_mobile` \| `desktop_app` \| `embedded_in_product` |
| `{archetype}` | optional | `pro` (default) \| `compact` \| `multi_chart` |
| `{broker_api}` | yes | `schwab_dev_portal` \| `ibkr` \| `tradier` \| `custom` — drives the API contract. |
| `{has_trading_panel}` | optional | Default false. true requires write-scope on broker. |
| `{brand_palette}` | yes | Primary, background, text, grid, up/down, alert hex codes. |
| `{density}` | optional | `compact` \| `comfortable` — default `compact` for pro layout, `comfortable` for compact archetype. |
| `{watchlist_seed}` | optional | List of symbols to render in the initial watchlist. |
| `{currency}` | optional | Default USD. |
| `{timezone}` | optional | Default `America/New_York`. |

---

## Domain Knowledge (CRITICAL — layout + data + brand)

**Pro layout (default):**

```
+------------------------------------------------+
| Header: account summary, day P&L, settings     |
+--------------+----------------------+----------+
|              |                      |          |
|  Watchlist   |   Chart              |  Alerts  |
|  (sidebar    |   (Advanced Charts   |  (corner |
|   left,      |    widget — see      |   widget |
|   ~15%       |    tradingview-      |   ~15%)  |
|   width)     |    widget-builder)   |          |
|              |                      |          |
|              |   ~70% width         |          |
+--------------+----------------------+----------+
| Positions strip — sortable table, ~25% height  |
+------------------------------------------------+
| Status bar: market regime, posture, time, NY clock |
+------------------------------------------------+
```

**Per-panel spec:**

| Panel | What it renders | Data binding | Refresh rate |
|---|---|---|---|
| Header | Account equity, day P&L $, day P&L %, # open positions, # alerts triggered today | `GET /account/summary` | 5s poll or WS |
| Watchlist | Sortable list of symbols with last, change, change%, volume; click → set chart symbol | `GET /quotes?symbols=...` | WS stream preferred |
| Chart | Advanced Charts widget — see `tradingview-widget-builder` | Datafeed object — see `tradingview-datafeed-implementation` | WS stream |
| Alerts | List of triggered alerts (last 24h) + active alert count | `GET /alerts/triggered?from=...` + `GET /alerts/active` | 10s poll |
| Positions | Sortable table — symbol, qty, avg cost, last, unrealized P&L $, unrealized P&L %, day P&L | `GET /positions` | 5s poll or WS |
| Status bar | SPY/QQQ regime read (above/below 50 SMA), current posture HEAD summary, NY clock, market open/closed flag | computed locally + `posture-reader` | 1s clock |

**Brand palette mapping:**

Trading dashboards have specific semantic color requirements that
override generic brand:

- `up` / `gain` — green family (operator's brand-aligned green)
- `down` / `loss` — red family (operator's brand-aligned red)
- `neutral` — operator's brand text color
- `alert` — typically the operator's brand-accent (orange/amber)

The skill enforces: up/down colors must be DISTINGUISHABLE for the
color-blind majority (deuteranopia hits 5% of men — use luminance
contrast not just hue).

**Density rules:**

- **Compact** — 11-13px base font, 6-8px row padding, 24-28px row
  height in tables.
- **Comfortable** — 14-15px base font, 10-12px row padding, 36-40px
  row height.

Pro archetype defaults to compact (traders want density).

**Schwab Developer Portal patterns** (per
`Clippings/Charles Schwab Developer Portal.md` — connector reference):
- OAuth 2.0 flow handled by the broker integration (NOT this skill).
- Positions endpoint returns: `[{symbol, qty, avg_price, market_value,
  unrealized_pnl, day_pnl}, ...]`.
- Quotes endpoint returns: `[{symbol, last, bid, ask, volume,
  change_pct, change_$}, ...]`.
- Trading actions (place order / cancel order) — out of scope for
  this skill; route to the broker MCP/AMA.

**Read-only vs write-scope:**

Per `trading_rules.md` §11: TOS paperMoney first for any new setup.
The dashboard defaults to **read-only**. If `{has_trading_panel}` is
true, add a separate confirm gate in the trading panel that
displays the position-size calculation (route through
`risk-1pct-calculator`) before submitting any order.

---

## The dashboard spec template

```yaml
dashboard:
  name: "{operator-defined name}"
  surface: {target_surface}
  archetype: {pro | compact | multi_chart}
  density: {compact | comfortable}
  responsive_breakpoints:
    - { name: desktop, min_width: 1280 }
    - { name: tablet,  min_width: 768  }
    - { name: mobile,  min_width: 0    }

layout:
  grid:
    columns: 12
    rows: 12
    gap: 8
  panels:
    - id: header
      area: { col_start: 1,  col_end: 13, row_start: 1,  row_end: 2  }
      component: AccountHeader
    - id: watchlist
      area: { col_start: 1,  col_end: 3,  row_start: 2,  row_end: 11 }
      component: Watchlist
      collapsible_on_mobile: true
    - id: chart
      area: { col_start: 3,  col_end: 11, row_start: 2,  row_end: 11 }
      component: TradingViewWidget   # → tradingview-widget-builder
    - id: alerts
      area: { col_start: 11, col_end: 13, row_start: 2,  row_end: 11 }
      component: AlertsPanel
    - id: positions
      area: { col_start: 1,  col_end: 13, row_start: 11, row_end: 12 }
      component: PositionsTable
    - id: status_bar
      area: { col_start: 1,  col_end: 13, row_start: 12, row_end: 13 }
      component: StatusBar

data_contracts:
  account_summary:
    endpoint: GET /account/summary
    fields:   [equity, day_pnl_dollars, day_pnl_pct, open_positions, alerts_today]
    refresh:  5s_poll_or_ws

  positions:
    endpoint: GET /positions
    fields:   [symbol, qty, avg_price, market_value, unrealized_pnl_dollars,
               unrealized_pnl_pct, day_pnl_dollars]
    refresh:  5s_poll_or_ws

  quotes:
    endpoint: GET /quotes?symbols=...
    fields:   [symbol, last, bid, ask, volume, change_pct, change_dollars]
    refresh:  ws_stream_preferred

  alerts:
    endpoints:
      triggered: GET /alerts/triggered?from=...&limit=50
      active:    GET /alerts/active
    refresh:    10s_poll

  posture_status_bar:
    source: posture-reader skill
    field:  active_playbook_summary
    refresh: on_mount + on_request

design_tokens:
  colors:
    background:   {brand_palette.bg}
    surface_1:    {brand_palette.bg_elevated}
    text_primary: {brand_palette.text}
    text_muted:   {brand_palette.text_muted}
    border:       {brand_palette.grid}
    up:           {brand_palette.up}
    down:         {brand_palette.down}
    neutral:      {brand_palette.neutral}
    alert:        {brand_palette.accent}
  typography:
    font_family:  {brand.font_stack}
    base_size:    {12 if compact else 15}px
    mono_size:    {12 if compact else 14}px   # for prices, P&L numbers
    line_height:  1.4
  spacing:
    row_padding:  {7 if compact else 11}px
    panel_padding: {12 if compact else 16}px
    panel_gap:    8px
  density:
    table_row_height: {26 if compact else 38}px

interaction_contracts:
  watchlist_click:
    action: chart.setSymbol(clicked_symbol)
  positions_click:
    action: chart.setSymbol(clicked_symbol) + scroll-to-chart
  alert_click:
    action: open_alert_detail_modal
  trading_panel: {if has_trading_panel}
    pre_submit_gate: risk-1pct-calculator must return CLEARED before submit button enables
    confirm_modal:  true
    posture_check:  posture-reader on every order submit
```

---

## Output

```
## Trading dashboard spec — {operator-defined name}

### Layout
{ASCII grid showing the panel arrangement at desktop breakpoint}

### Per-panel spec
| Panel        | Component             | Data source         | Refresh    |
|--------------|------------------------|---------------------|------------|
| Header       | AccountHeader          | account_summary     | 5s         |
| Watchlist    | Watchlist              | quotes (WS)         | ws_stream  |
| Chart        | TradingViewWidget      | Datafeed            | ws_stream  |
| Alerts       | AlertsPanel            | alerts (triggered + active) | 10s |
| Positions    | PositionsTable         | positions           | 5s         |
| Status bar   | StatusBar              | posture-reader + local clock | on_mount + 1s clock |

### Data contracts
{YAML block of data_contracts from template}

### Design tokens
{Table of design_tokens — colors / typography / spacing / density}

### Interaction contracts
{List of every cross-panel interaction — watchlist click → chart symbol change, position click → chart focus, etc.}

### Responsive behavior
- Desktop (≥1280px): {full pro layout}
- Tablet (768-1279): {watchlist collapses to tab, alerts collapses to icon}
- Mobile (<768px): {falls back to compact archetype — chart on top, swipeable below}

### Pre-ship checklist
- [ ] Up/down colors distinguishable for color-blind users (luminance contrast verified)
- [ ] Read-only API scopes confirmed (no write hooks unless trading_panel = true)
- [ ] WebSocket reconnect logic on disconnect
- [ ] Posture-reader integrated in status bar AND as gate in trading panel (if enabled)
- [ ] Risk-1pct-calculator gate in trading panel (if enabled)
- [ ] Chart panel routes to tradingview-widget-builder spec
- [ ] Datafeed routes to tradingview-datafeed-implementation
- [ ] Brand palette pulled from DESIGN (not invented)
- [ ] Density chosen per archetype (compact for pro)
- [ ] No live-trade execution in this surface unless has_trading_panel = true AND gate logic in place

### Disclaimer
If trading panel enabled: this surface routes trades the operator submits.
Operator owns all risk. Past setups do not guarantee future outcomes.
```

---

## Anti-patterns (refuse list)

- **Preamble.** Layout first.
- **Trading panel without gates.** If `has_trading_panel` is true, the surface MUST gate every submit through `risk-1pct-calculator` AND `posture-reader`. No exceptions.
- **Hue-only up/down colors.** Luminance contrast is mandatory — deuteranopia hits 5% of male users.
- **Inventing the brand palette.** Pull from DESIGN; if unclear, route.
- **Bundling chart logic inline.** The chart panel routes to `tradingview-widget-builder` — don't reinvent.
- **Bundling datafeed inline.** The datafeed routes to `tradingview-datafeed-implementation`.
- **Skipping the status bar posture indicator.** The operator needs the active playbook visible at all times.
- **Polling everything.** Use WebSocket for quotes + positions where the broker supports; polling is a fallback.
- **Comfortable density on pro archetype.** Traders want density.
- **Defaulting park-triggers to Monday Anchor.**
- **Forbidden vocabulary** per CD voice-spine § 4.
- **"User"** — say "the operator," "the trader using this surface," "the dashboard."
- **Naming people from the bench.**

---

## Success criterion (universal)

**This skill succeeded when the user closes the tab and goes outside.**
The cleanest output is the layout + per-panel spec + design tokens
— one read, the frontend implementer (designer agent / dev) can
build straight from this spec.

---

## Cross-references

- UI elements (chart-side toolbar / theme keys): `Clippings/UI elements Advanced Charts Documentation.md`
- Trading Platform methods (chart-side trade panel — if has_trading_panel): `Clippings/Trading Platform methods Advanced Charts Documentation.md`
- Broker connector reference: `Clippings/Charles Schwab Developer Portal.md`
- Trading rules: `agents/finance-manager/memory/trading_rules.md`
- Voice spine: `.claude/voice-spine.md`
- Related skills: `tradingview-widget-builder` (chart panel), `tradingview-datafeed-implementation` (chart data), `risk-1pct-calculator` (trading-panel gate), `posture-reader` (status-bar indicator + trading-panel gate)
- Cross-agent: designer agent's `frontend-design`, `claude-design-skill`, `design-for-ai` for taste enforcement on the implemented surface.
- Owning agent: `trading-analyst`
- No AMA counterpart — the operator-locked in-house skill (cohort + customer product surface). The broker integration itself (Schwab OAuth, order submission) IS an AMA candidate, separately scoped.
