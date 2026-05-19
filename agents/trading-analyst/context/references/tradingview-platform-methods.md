---
title: "Trading Platform methods | Advanced Charts Documentation"
source: "https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/trading-platform-methods"
author:
published:
created: 2026-05-12
description: "Trading Platform is a standalone client-side solution that provides trading capabilities. To use Trading Platform, in addition to the required Datafeed API methods, you should implement the quote-related methods, including getQuotes, subscribeQuotes, and unsubscribeQuotes. The library calls these methods to request quotes, which are data sets that show the most recent bid and ask prices, opening and closing prices, price changes, and other market data. Quotes are used in most Trading Platform features including the following:"
tags:
  - "clippings"
---
[Trading Platform](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/) is a standalone client-side solution that provides trading capabilities. To use Trading Platform, in addition to the [required](https://www.tradingview.com/charting-library-docs/latest/connecting_data/datafeed-api/required-methods) Datafeed API methods, you should implement the quote-related methods, including [`getQuotes`](#getquotes), [`subscribeQuotes`](#subscribequotes), and [`unsubscribeQuotes`](#unsubscribequotes). The library calls these methods to request [quotes](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/trading-concepts/quotes), which are data sets that show the most recent bid and ask prices, opening and closing prices, price changes, and other market data. Quotes are used in most Trading Platform features including the following:

- [Order Ticket](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/order-ticket)
- [Legend](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend)
- [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List)
- [Details](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#details)
- [News](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/news)
- [Depth of Market (DOM)](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#depth-of-market)

For [DOM](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#depth-of-market), you should also implement the [`subscribeDepth`](#subscribedepth) and [`unsubscribeDepth`](#unsubscribedepth) methods.

> [!-success] -success
> tip
> 
> For Trading Platform, along with implementing the Datafeed API methods, you also need to implement the Broker API. For more information, refer to [Core trading concepts](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/trading-concepts/), or jump into the [step-by-step tutorial](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/implement-broker-api/) to start implementing the Broker API.

## getQuotes

Trading Platform calls [`getQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#getquotes) to request quote data that is used to display the [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List), [Details](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#details), [Order Ticket](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/order-ticket), [DOM](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#depth-of-market) widgets, and the [Legend](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend). To transfer the requested data, pass an array of [QuoteData](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotedata) objects as a parameter to [QuotesCallback](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotescallback). The library expects to receive necessary data in a single callback.

> [!-warning] -warning
> caution
> 
> Note that if you integrate the library with [mobile applications](https://www.tradingview.com/charting-library-docs/latest/mobile_specifics/), `getQuotes` is required to avoid [NaN values](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend#nan-values-in-legend) appearing in the legend.

The example of [QuoteData](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotedata) is demonstrated below:

```json
{
    {
        "s": "ok",
        "n": "NasdaqNM:AAPL",
        "v": {
            "ch": 0,
            "chp": 0,
            "short_name": "AAPL",
            "exchange": "",
            "original_name": "NasdaqNM:AAPL",
            "description": "NasdaqNM:AAPL",
            "lp": 173.68,
            "ask": 173.68,
            "bid": 173.68,
            "open_price": 173.68,
            "high_price": 173.68,
            "low_price": 173.68,
            "prev_close_price": 172.77,
            "volume": 173.68
        }
    }
}
```

Note that **Percentage change** value, **Ask/Bid buttons** and **lines** also require quote data. They are **not displayed** on the chart if [`getQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#getquotes) is not implemented.

![Datafeed API buttons](https://www.tradingview.com/charting-library-docs/assets/images/datafeed_api_buttons-be5493fec764700c98c1651ad24eae53.png)

The following piece of code is just a snippet to begin with. You will have to change it to fit your requirements but copying & pasting the code below should enable displaying values in the Legend when on mobile along with values for `ask` and `bid` buttons (if activated within the Chart settings) when using Trading Platform. [`subscribeQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#subscribequotes) will however update the values on regular basis.

```javascript
// In this example we are returning random values (which probably don't make any sense from a trading purpose)
// but it is just to illustrate how to structure the function and returned object.
getQuotes(symbols, onDataCallback, onErrorCallback) {
    const data = [];

    symbols.forEach((symbol)=>{
        data.push({
            n: symbol,
            s: 'ok',
            v: {
                ch: Math.random() * (5 - 1) + 1,
                chp: Math.random() * (5 - 1) + 1,
                lp: Math.random() * (10 - 1) + 1,
                ask: Math.random() * (10 - 1) + 1,
                bid: Math.random() * (10 - 1) + 1,
                spread: 0.20,
                open_price: Math.random() * (5 - 1) + 1,
                high_price: Math.random() * (5 - 1) + 1,
                low_price: Math.random() * (5 - 1) + 1,
                prev_close_price: Math.random() * (5 - 1) + 1,
                original_name: symbol,
                volume: Math.random() * (5 - 1) + 1,
            },
        });
    });

    // To ensure the callback is only evoked when the library is ready - see Asynchronous callbacks
    setTimeout(() => onDataCallback(data), 0);
}
```

## subscribeQuotes

The library calls [`subscribeQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#subscribequotes) to receive real-time quote updates for certain symbols. Call [QuotesCallback](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotescallback) every time you want to update the quotes and pass an array of [QuoteData](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#quotedata) objects as a parameter.

The following piece of code is just a snippet to begin with. You will have to change it to fit your requirements but copying & pasting the code below should render different values in the Legend when on mobile along with values for `ask` and `bid` buttons (if activated within the Chart settings). [`unsubscribeQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#unsubscribequotes) will however update the values on regular basis.

```javascript
subscribeQuotes(symbols, fastSymbols, onRealtimeCallback, listenerGUID) {
    // In this example, \`_quotesSubscriptions\` is a global variable used to clear the subscription in \`unsubscribeQuotes\`
    this._quotesSubscriptions[listenerGUID] = setInterval(() => this.getQuotes(symbols.concat(fastSymbols), onRealtimeCallback, () => undefined), 5000);
}
```

## unsubscribeQuotes

The library calls [`unsubscribeQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#unsubscribequotes) to stop receiving updates for the symbol when the user removes it from the [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List) or selects another symbol on the chart. The `listenerGuid` argument contains the same object that was passed to [`subscribeQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#subscribequotes) before.

The following piece of code is just a snippet to begin with. You will have to change it to fit your requirements but copying & pasting the code below should stop updating the values created by [`subscribeQuotes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedQuotesApi#subscribequotes).

```javascript
unsubscribeQuotes(listenerGUID) {
    clearInterval(this._quotesSubscriptions[listenerGUID]);
}
```

## subscribeDepth

The library calls [`subscribeDepth`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedChartApi#subscribedepth) to receive real-time [Level 2](https://www.investopedia.com/terms/l/level2.asp) (DOM) data for a symbol. Call [DOMCallback](https://www.tradingview.com/charting-library-docs/latest/api/modules/Datafeed#domcallback) every time you want to update the quotes and pass a [DOMData](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.DOMData) object as a parameter.

Note that you should specify the [broker\_config](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions#broker_config) property in the [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions) and set [supportLevel2Data](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.BrokerConfigFlags#supportlevel2data) to `true`. Otherwise, the library does not call the [`subscribeDepth`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedChartApi#subscribedepth) / [`unsubscribeDepth`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedChartApi#unsubscribedepth) methods.

This method should return a unique identifier (`subscriberUID`) that is used to unsubscribe from updates.

## unsubscribeDepth

The library calls [`unsubscribeDepth`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedChartApi#unsubscribedepth) to stop receiving DOM data updates. The `subscriberUID` argument contains the same object that was returned by [`subscribeDepth`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IDatafeedChartApi#subscribedepth).