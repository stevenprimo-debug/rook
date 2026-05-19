---
title: "Module: Datafeed | Advanced Charts Documentation"
source: "https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed"
author:
published:
created: 2026-05-12
description: "Datafeed JS API for TradingView Advanced Charts"
tags:
  - "clippings"
---
## Enumerations

- [SearchInitiationPoint](https://www.tradingview.com/charting-library-docs/latest/api/enums/Datafeed.SearchInitiationPoint)

## Interfaces

- [Bar](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Bar)
- [CurrencyItem](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.CurrencyItem)
- [DOMData](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DOMData)
- [DOMLevel](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DOMLevel)
- [DatafeedConfiguration](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DatafeedConfiguration)
- [DatafeedQuoteValues](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DatafeedQuoteValues)
- [DatafeedSymbolType](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DatafeedSymbolType)
- [Exchange](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Exchange)
- [HistoryMetadata](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.HistoryMetadata)
- [IDatafeedChartApi](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.IDatafeedChartApi)
- [IDatafeedQuotesApi](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.IDatafeedQuotesApi)
- [IExternalDatafeed](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.IExternalDatafeed)
- [LibrarySubsessionInfo](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.LibrarySubsessionInfo)
- [LibrarySymbolInfo](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.LibrarySymbolInfo)
- [Mark](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Mark)
- [MarkCustomColor](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.MarkCustomColor)
- [PeriodParams](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.PeriodParams)
- [QuoteDataResponse](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.QuoteDataResponse)
- [QuoteErrorData](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.QuoteErrorData)
- [QuoteOkData](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.QuoteOkData)
- [SearchSymbolResultItem](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SearchSymbolResultItem)
- [SymbolInfoPriceSource](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SymbolInfoPriceSource)
- [SymbolResolveExtension](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SymbolResolveExtension)
- [SymbolSearchPaginatedOptions](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SymbolSearchPaginatedOptions)
- [TimescaleMark](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.TimescaleMark)
- [Unit](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Unit)

## Type Aliases

### CustomTimezones

Ƭ **CustomTimezones**: `"Africa/Cairo"` | `"Africa/Casablanca"` | `"Africa/Johannesburg"` | `"Africa/Lagos"` | `"Africa/Nairobi"` | `"Africa/Tunis"` | `"America/Anchorage"` | `"America/Argentina/Buenos_Aires"` | `"America/Bogota"` | `"America/Caracas"` | `"America/Chicago"` | `"America/El_Salvador"` | `"America/Halifax"` | `"America/Juneau"` | `"America/Lima"` | `"America/Los_Angeles"` | `"America/Mexico_City"` | `"America/New_York"` | `"America/Phoenix"` | `"America/Santiago"` | `"America/Sao_Paulo"` | `"America/Toronto"` | `"America/Vancouver"` | `"Asia/Almaty"` | `"Asia/Ashkhabad"` | `"Asia/Bahrain"` | `"Asia/Bangkok"` | `"Asia/Chongqing"` | `"Asia/Colombo"` | `"Asia/Dhaka"` | `"Asia/Dubai"` | `"Asia/Ho_Chi_Minh"` | `"Asia/Hong_Kong"` | `"Asia/Jakarta"` | `"Asia/Jerusalem"` | `"Asia/Kabul"` | `"Asia/Karachi"` | `"Asia/Kathmandu"` | `"Asia/Kolkata"` | `"Asia/Kuala_Lumpur"` | `"Asia/Kuwait"` | `"Asia/Manila"` | `"Asia/Muscat"` | `"Asia/Nicosia"` | `"Asia/Qatar"` | `"Asia/Riyadh"` | `"Asia/Seoul"` | `"Asia/Shanghai"` | `"Asia/Singapore"` | `"Asia/Taipei"` | `"Asia/Tehran"` | `"Asia/Tokyo"` | `"Asia/Yangon"` | `"Atlantic/Azores"` | `"Atlantic/Reykjavik"` | `"Australia/Adelaide"` | `"Australia/Brisbane"` | `"Australia/Perth"` | `"Australia/Sydney"` | `"Europe/Amsterdam"` | `"Europe/Athens"` | `"Europe/Belgrade"` | `"Europe/Berlin"` | `"Europe/Bratislava"` | `"Europe/Brussels"` | `"Europe/Bucharest"` | `"Europe/Budapest"` | `"Europe/Copenhagen"` | `"Europe/Dublin"` | `"Europe/Helsinki"` | `"Europe/Istanbul"` | `"Europe/Lisbon"` | `"Europe/London"` | `"Europe/Luxembourg"` | `"Europe/Madrid"` | `"Europe/Malta"` | `"Europe/Moscow"` | `"Europe/Oslo"` | `"Europe/Paris"` | `"Europe/Prague"` | `"Europe/Riga"` | `"Europe/Rome"` | `"Europe/Stockholm"` | `"Europe/Tallinn"` | `"Europe/Vienna"` | `"Europe/Vilnius"` | `"Europe/Warsaw"` | `"Europe/Zurich"` | `"Pacific/Auckland"` | `"Pacific/Chatham"` | `"Pacific/Fakaofo"` | `"Pacific/Honolulu"` | `"Pacific/Norfolk"` | `"US/Mountain"`

---

### DOMCallback

Ƭ **DOMCallback**: (`data`: [`DOMData`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DOMData)) => `void`

#### Type declaration

▸ (`data`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `data` | [`DOMData`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DOMData) |

##### Returns

`void`

---

### DatafeedErrorCallback

Ƭ **DatafeedErrorCallback**: (`reason`: `string`) => `void`

#### Type declaration

▸ (`reason`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `reason` | `string` |

##### Returns

`void`

---

### GetMarksCallback

Ƭ **GetMarksCallback** < `T` >: (`marks`: `T` \[\]) => `void`

#### Type parameters

| Name |
| --- |
| `T` |

#### Type declaration

▸ (`marks`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `marks` | `T` \[\] |

##### Returns

`void`

---

### HistoryCallback

Ƭ **HistoryCallback**: (`bars`: [`Bar`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Bar) \[\], `meta?`: [`HistoryMetadata`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.HistoryMetadata)) => `void`

#### Type declaration

▸ (`bars`, `meta?`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `bars` | [`Bar`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Bar) \[\] |
| `meta?` | [`HistoryMetadata`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.HistoryMetadata) |

##### Returns

`void`

---

### LibrarySessionId

Ƭ **LibrarySessionId**: `"regular"` | `"extended"` | `"premarket"` | `"postmarket"`

---

### MarkConstColors

Ƭ **MarkConstColors**: `"red"` | `"green"` | `"blue"` | `"yellow"`

---

### Nominal

Ƭ **Nominal** < `T`, `Name` >: `T` & { `[species]`: `Name` }

This is the generic type useful for declaring a nominal type, which does not structurally matches with the base type and the other types declared over the same base type

Usage:

**`Example`**

```ts
type Index = Nominal<number, 'Index'>;
// let i: Index = 42; // this fails to compile
let i: Index = 42 as Index; // OK
```

**`Example`**

```ts
type TagName = Nominal<string, 'TagName'>;
```

#### Type parameters

| Name | Type |
| --- | --- |
| `T` | `T` |
| `Name` | extends `string` |

---

### OnReadyCallback

Ƭ **OnReadyCallback**: (`configuration`: [`DatafeedConfiguration`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DatafeedConfiguration)) => `void`

#### Type declaration

▸ (`configuration`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `configuration` | [`DatafeedConfiguration`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.DatafeedConfiguration) |

##### Returns

`void`

---

### QuoteData

Ƭ **QuoteData**: [`QuoteOkData`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.QuoteOkData) | [`QuoteErrorData`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.QuoteErrorData)

---

### QuotesCallback

Ƭ **QuotesCallback**: (`data`: [`QuoteData`](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotedata) \[\]) => `void`

#### Type declaration

▸ (`data`): `void`

Callback to provide Quote data.

##### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `data` | [`QuoteData`](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotedata) \[\] | Quote Data |

##### Returns

`void`

---

### QuotesErrorCallback

Ƭ **QuotesErrorCallback**: (`reason`: `string`) => `void`

#### Type declaration

▸ (`reason`): `void`

Error callback for quote data request.

##### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `reason` | `string` | message describing the reason for the error |

##### Returns

`void`

---

### ResolutionString

Ƭ **ResolutionString**: [`Nominal`](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#nominal) < `string`, `"ResolutionString"` >

Resolution or time interval is a time period of one bar. Advanced Charts supports tick, intraday (seconds, minutes, hours), and DWM (daily, weekly, monthly) resolutions. The table below describes how to specify different types of resolutions:

| Resolution | Format | Example |
| --- | --- | --- |
| Ticks | `xT` | `1T` — one tick, `5T` — five ticks, `100T` — one hundred ticks |
| Seconds | `xS` | `1S` — one second |
| Minutes | `x` | `1` — one minute |
| Hours | `x` minutes | `60` — one hour |
| Days | `xD` | `1D` — one day |
| Weeks | `xW` | `1W` — one week |
| Months | `xM` | `1M` — one month |
| Years | `xM` months | `12M` — one year |

Refer to [Resolution](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Resolution) for more information.

---

### ResolveCallback

Ƭ **ResolveCallback**: (`symbolInfo`: [`LibrarySymbolInfo`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.LibrarySymbolInfo)) => `void`

#### Type declaration

▸ (`symbolInfo`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `symbolInfo` | [`LibrarySymbolInfo`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.LibrarySymbolInfo) |

##### Returns

`void`

---

### SearchSymbolsCallback

Ƭ **SearchSymbolsCallback**: (`items`: [`SearchSymbolResultItem`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SearchSymbolResultItem) \[\]) => `void`

#### Type declaration

▸ (`items`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `items` | [`SearchSymbolResultItem`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SearchSymbolResultItem) \[\] |

##### Returns

`void`

---

### SearchSymbolsPaginatedCallback

Ƭ **SearchSymbolsPaginatedCallback**: (`items`: [`SearchSymbolResultItem`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SearchSymbolResultItem) \[\], `symbolsRemaining`: `number`) => `void`

#### Type declaration

▸ (`items`, `symbolsRemaining`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `items` | [`SearchSymbolResultItem`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.SearchSymbolResultItem) \[\] |
| `symbolsRemaining` | `number` |

##### Returns

`void`

---

### SeriesFormat

Ƭ **SeriesFormat**: `"price"` | `"volume"`

---

### ServerTimeCallback

Ƭ **ServerTimeCallback**: (`serverTime`: `number`) => `void`

#### Type declaration

▸ (`serverTime`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `serverTime` | `number` |

##### Returns

`void`

---

### SubscribeBarsCallback

Ƭ **SubscribeBarsCallback**: (`bar`: [`Bar`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Bar)) => `void`

#### Type declaration

▸ (`bar`): `void`

##### Parameters

| Name | Type |
| --- | --- |
| `bar` | [`Bar`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Datafeed.Bar) |

##### Returns

`void`

---

### TimeScaleMarkShape

Ƭ **TimeScaleMarkShape**: `"circle"` | `"earningUp"` | `"earningDown"` | `"earning"`

---

### Timezone

Ƭ **Timezone**: `"Etc/UTC"` | [`CustomTimezones`](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#customtimezones)

---

### VisiblePlotsSet

Ƭ **VisiblePlotsSet**: `"ohlcv"` | `"ohlc"` | `"c"` | `"hlc"`