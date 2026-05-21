---
name: tradingview-datafeed-implementation
description: |
  Build a custom JavaScript Datafeed for TradingView Advanced Charts.
  Returns a complete Datafeed object implementing the required methods
  (onReady, searchSymbols, resolveSymbol, getBars, subscribeBars,
  unsubscribeBars) per the TradingView UDF / JS Datafeed protocol.
  Defaults to UDF-compatible REST shape; JS-object variant for
  proprietary streams. Never uses preamble; the Datafeed code is the
  first artifact.
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
  Fire when the user says: datafeed, TradingView datafeed, UDF, custom
  datafeed, getBars, subscribeBars, resolveSymbol, datafeed API, build
  a feed, custom data source, proprietary chart data.
inherits:
  - voice_spine: .claude/voice-spine.md
  - primary_methodology: TradingView Datafeed API + Module Datafeed reference
  - primolabs_memory:
      - agents/finance-manager/memory/reference_external_repos.md
---

# tradingview-datafeed-implementation

## Overview

You are the Datafeed implementer. The operator has a custom data
source — a REST API, a WebSocket, a database, a proprietary feed —
and needs to plug it into a TradingView Advanced Charts widget. You
return: the JS Datafeed object (or UDF-compatible HTTP endpoint
spec), every required method implemented against the operator's
source, and the WebSocket subscription pattern for real-time bar
updates.

The Datafeed contract is the single most consequential implementation
detail in any TradingView embed. Get it wrong and the chart shows
nothing (or worse, stale data). The skill ships a complete
implementation, not a snippet.

Two implementation variants:

1. **UDF-compatible REST** — JSON over HTTP, follows TradingView's
   Universal Data Feed contract. Easiest when the data already lives
   behind an HTTP API. The widget consumes it via
   `new Datafeeds.UDFCompatibleDatafeed(url)`.

2. **JS object** — direct implementation of the Datafeed interface
   in JavaScript. Required when:
   - Data source is a WebSocket / Server-Sent Events stream
   - Data source needs auth headers / token refresh
   - Data source returns a non-UDF shape and you don't want a
     translation layer

The skill defaults to **UDF-compatible** if the source is REST and
returns JSON in a TradingView-shaped form; otherwise it produces the
JS object.

**No preamble.** The Datafeed code is the first artifact.

Success criterion: **this skill succeeded when the user closes the tab
and goes outside.**

---

## How to use

Operator provides: data source URL or WebSocket endpoint, symbol-
resolution shape, supported resolutions, supported exchanges,
historical-bars endpoint, real-time stream endpoint, auth
requirements.

Skill returns:

1. The Datafeed implementation (UDF spec OR JS object).
2. The widget Constructor call snippet that wires it in.
3. The error-handling matrix (network errors, missing bars, auth
   failures).
4. A test harness for verifying each method returns the right shape.

---

## Slots / Parameters

| Parameter | Required | Notes |
|---|---|---|
| `{source_type}` | yes | `rest` \| `websocket` \| `mixed` |
| `{historical_url}` | yes | Endpoint returning historical bars. |
| `{realtime_url}` | optional | WebSocket / SSE endpoint for live bars. |
| `{symbol_search_url}` | optional | Endpoint for `searchSymbols`. |
| `{symbol_resolve_url}` | optional | Endpoint for `resolveSymbol`. |
| `{supported_resolutions}` | yes | List, e.g., `["1", "5", "15", "60", "1D", "1W"]`. |
| `{supported_exchanges}` | optional | List of exchange descriptors. |
| `{auth_header}` | optional | If the source needs auth, the header name + token strategy. |
| `{response_shape}` | yes | Whether the source already matches TradingView's shape or needs translation. |

---

## Domain Knowledge (CRITICAL — Datafeed contract)

Quoted from the methodology source (`Clippings/Datafeed API
Advanced Charts Documentation.md` + `Clippings/Module Datafeed
Advanced Charts Documentation.md`):

The Datafeed interface requires these methods:

```
onReady(callback)
    Called once. Callback receives a Configuration object describing
    supported_resolutions, exchanges, symbols_types, supports_marks,
    supports_time, supports_search, supports_group_request.

searchSymbols(userInput, exchange, symbolType, onResultReadyCallback)
    User typing in symbol search box. Return an array of SymbolInfo-
    lite objects.

resolveSymbol(symbolName, onSymbolResolvedCallback, onResolveErrorCallback, extension)
    Map a symbol string to a full SymbolInfo (description, exchange,
    timezone, minmov, pricescale, has_intraday, supported_resolutions,
    volume_precision, data_status).

getBars(symbolInfo, resolution, periodParams, onHistoryCallback, onErrorCallback)
    Historical bars. periodParams = {from, to, countBack, firstDataRequest}.
    Return: array of {time, open, high, low, close, volume}; time in
    milliseconds since epoch (UTC).

subscribeBars(symbolInfo, resolution, onRealtimeCallback, subscriberUID, onResetCacheNeededCallback)
    Real-time stream. Call onRealtimeCallback(bar) on each new tick
    or bar update.

unsubscribeBars(subscriberUID)
    Stop the real-time stream for a given UID.
```

Critical shape rules:

- **Time is in milliseconds since epoch, UTC.** Source data in
  seconds = multiply by 1000. Source data in ISO 8601 = parse + UTC.
- **Bars must be sorted ascending by time.**
- **No duplicate timestamps.** Deduplicate before returning.
- **`noData: true` flag** in the `onHistoryCallback` if the range
  has no bars — DO NOT pass an empty array silently.
- **`pricescale`** is a power of 10 representing tick size — e.g.,
  pricescale=100 = 2 decimal places, pricescale=10000 = 4 decimal
  places.

UDF REST endpoints (from `Clippings/Datafeed API Advanced Charts
Documentation.md`):

```
GET /config          → Configuration object
GET /symbols?symbol=NASDAQ:NVDA → SymbolInfo
GET /search?query=NV&type=stock&exchange=NASDAQ&limit=10 → array
GET /history?symbol=NASDAQ:NVDA&resolution=D&from={ts}&to={ts}&countback={n}
    → { s: "ok" | "no_data" | "error",
        t: [...], o: [...], h: [...], l: [...], c: [...], v: [...],
        nextTime: <next-valid-ts-if-no-data> }
GET /marks?symbol=NASDAQ:NVDA&from={ts}&to={ts}&resolution=D
    → { id, time, color, text, label, labelFontColor, minSize }
```

Real-time subscriptions are not part of UDF over plain HTTP — they
require either WebSocket or polling. The skill produces the WebSocket
pattern for real-time.

---

## The implementation template (JS object variant)

```js
const Datafeed = {
    onReady: (cb) => {
        setTimeout(() => cb({
            supported_resolutions: {supported_resolutions},
            exchanges: {supported_exchanges_descriptors},
            symbols_types: [{ name: "All", value: "" }, { name: "Stock", value: "stock" }],
            supports_marks: false,
            supports_timescale_marks: false,
            supports_time: true,
            supports_search: true,
            supports_group_request: false
        }), 0);
    },

    searchSymbols: async (userInput, exchange, symbolType, onResult) => {
        try {
            const r = await fetch(`{symbol_search_url}?query=${encodeURIComponent(userInput)}&exchange=${exchange}&type=${symbolType}`, {
                headers: { {auth_header_if_any} }
            });
            const symbols = await r.json();
            onResult(symbols.map(s => ({
                symbol: s.symbol,
                full_name: `${s.exchange}:${s.symbol}`,
                description: s.description,
                exchange: s.exchange,
                type: s.type
            })));
        } catch (err) {
            console.error("searchSymbols", err);
            onResult([]);
        }
    },

    resolveSymbol: async (symbolName, onResolved, onError, extension) => {
        try {
            const r = await fetch(`{symbol_resolve_url}?symbol=${encodeURIComponent(symbolName)}`, {
                headers: { {auth_header_if_any} }
            });
            if (!r.ok) throw new Error("resolve failed");
            const s = await r.json();
            onResolved({
                ticker: s.symbol,
                name: s.symbol,
                description: s.description,
                type: s.type,
                session: s.session || "0930-1600",
                timezone: s.timezone || "America/New_York",
                exchange: s.exchange,
                minmov: 1,
                pricescale: s.pricescale || 100,
                has_intraday: true,
                has_no_volume: false,
                has_weekly_and_monthly: true,
                supported_resolutions: {supported_resolutions},
                volume_precision: 0,
                data_status: "streaming"
            });
        } catch (err) {
            onError("Cannot resolve symbol");
        }
    },

    getBars: async (symbolInfo, resolution, periodParams, onHistory, onError) => {
        const { from, to, countBack, firstDataRequest } = periodParams;
        try {
            const url = `{historical_url}?symbol=${encodeURIComponent(symbolInfo.ticker)}&resolution=${resolution}&from=${from}&to=${to}&countback=${countBack}`;
            const r = await fetch(url, { headers: { {auth_header_if_any} } });
            if (!r.ok) throw new Error("history failed");
            const data = await r.json();

            if (data.s === "no_data") {
                onHistory([], { noData: true, nextTime: data.nextTime });
                return;
            }
            if (data.s !== "ok") {
                onError("Bad data status");
                return;
            }

            const bars = data.t.map((ts, i) => ({
                time:   ts * 1000,                  // UDF returns seconds; widget expects ms
                open:   data.o[i],
                high:   data.h[i],
                low:    data.l[i],
                close:  data.c[i],
                volume: data.v ? data.v[i] : 0
            }))
            .sort((a, b) => a.time - b.time)
            .filter((b, i, arr) => i === 0 || b.time !== arr[i-1].time);   // dedupe

            onHistory(bars, { noData: bars.length === 0 });
        } catch (err) {
            onError(err.message);
        }
    },

    subscribeBars: (symbolInfo, resolution, onRealtime, subscriberUID, onResetCacheNeeded) => {
        const ws = new WebSocket("{realtime_url}");
        ws.addEventListener("open", () => {
            ws.send(JSON.stringify({
                action: "subscribe",
                symbol: symbolInfo.ticker,
                resolution: resolution,
                uid: subscriberUID
            }));
        });
        ws.addEventListener("message", (ev) => {
            const msg = JSON.parse(ev.data);
            if (msg.type !== "bar") return;
            onRealtime({
                time:   msg.time * 1000,
                open:   msg.open,
                high:   msg.high,
                low:    msg.low,
                close:  msg.close,
                volume: msg.volume
            });
        });
        Datafeed._subscriptions = Datafeed._subscriptions || {};
        Datafeed._subscriptions[subscriberUID] = ws;
    },

    unsubscribeBars: (subscriberUID) => {
        const ws = Datafeed._subscriptions && Datafeed._subscriptions[subscriberUID];
        if (ws) {
            try { ws.close(); } catch (e) {}
            delete Datafeed._subscriptions[subscriberUID];
        }
    }
};
```

Wire it into the widget:

```js
new TradingView.widget({
    ...,
    datafeed: Datafeed
});
```

---

## Output

```
## Datafeed implementation — {source_type}

### Implementation
\`\`\`js
{the Datafeed object above, with all placeholders filled}
\`\`\`

### Widget Constructor wiring
\`\`\`js
new TradingView.widget({
    symbol:    "{symbol}",
    interval:  "{interval}",
    container: "{container_id}",
    library_path: "{library_path}",
    datafeed:  Datafeed
});
\`\`\`

### Error-handling matrix
| Failure mode             | Where surfaced     | Behavior                |
|--------------------------|--------------------|-------------------------|
| Network error on history | onError callback   | Chart shows "loading…" |
| No bars in range         | onHistoryCallback  | Pass {noData: true, nextTime: ...} — NEVER empty array silently |
| Auth failure             | onError callback   | Token refresh hook (operator's responsibility) |
| WebSocket disconnect     | reconnect logic    | Exponential backoff in subscribeBars |
| Source returns sec, widget expects ms | getBars | Multiply by 1000 — already in template |

### Test harness
\`\`\`js
// Quick verify before paste-into-prod:
Datafeed.onReady(cfg => console.log("config:", cfg));
Datafeed.resolveSymbol("NASDAQ:NVDA", info => console.log("resolved:", info), err => console.error(err));
Datafeed.getBars({ticker:"NASDAQ:NVDA"}, "D", {from: 1700000000, to: 1730000000, countBack: 300, firstDataRequest: true},
    (bars, meta) => console.log("bars:", bars.length, "meta:", meta),
    err => console.error("history error:", err));
\`\`\`

### Pre-ship checklist
- [ ] Time fields in milliseconds since epoch (UTC).
- [ ] Bars sorted ascending and deduplicated.
- [ ] `noData: true` returned on empty ranges (never silent empty array).
- [ ] `pricescale` reflects the instrument's tick size.
- [ ] Auth header strategy in place if source requires.
- [ ] WebSocket reconnect logic on disconnect.
- [ ] No live-trade hooks — read-only by skill scope.
```

---

## Anti-patterns (refuse list)

- **Preamble.** Code first.
- **Time in seconds returned to the widget.** The widget expects milliseconds. Multiply.
- **Silent empty array on no-data.** Pass `{noData: true}` explicitly — empty array hides errors.
- **Unsorted bars.** Sort ascending before return.
- **Duplicate timestamps.** Dedupe.
- **Missing `pricescale`.** Wrong scale = wrong decimal display.
- **WebSocket without unsubscribe.** Memory leak. Track subscriptions by UID.
- **No reconnect on WebSocket close.** Real-time silently dies.
- **Hard-coded auth tokens.** Token strategy is the operator's responsibility — surface the hook, don't inline a secret.
- **Live-trade hooks in this skill.** Datafeed is read-only.
- **Defaulting park-triggers to weekly anchor session.**
- **Forbidden vocabulary** per CD voice-spine § 4.
- **"User"** — say "the operator," "the customer end-user," "the datafeed."
- **Naming people from the bench.**

---

## Success criterion (universal)

**This skill succeeded when the user closes the tab and goes outside.**
The cleanest output is the Datafeed code + the wiring snippet + the
test harness — one paste, the chart renders real data.

---

## Cross-references

- Datafeed API: `Clippings/Datafeed API Advanced Charts Documentation.md`
- Module Datafeed: `Clippings/Module Datafeed Advanced Charts Documentation.md`
- Widget Constructor (consumer): `Clippings/Widget Constructor Advanced Charts Documentation.md`
- Best practices: `Clippings/Best practices Advanced Charts Documentation.md`
- Voice spine: `.claude/voice-spine.md`
- Related skills: `tradingview-widget-builder` (the consumer of this Datafeed), `trading-dashboard-builder` (the surrounding UI), `pine-script-template` (strategy logic drawn on charts powered by this feed)
- Owning agent: `trading-analyst`
- No AMA counterpart — the operator-locked in-house skill.
