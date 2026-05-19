---
title: "Widget methods | Advanced Charts Documentation"
source: "https://www.tradingview.com/charting-library-docs/latest/configuration/widget-methods"
author:
published:
created: 2026-05-12
description: "Overview"
tags:
  - "clippings"
---
## Overview

After you create a widget with [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/configuration/Widget-Constructor), you can control the `widget` object using the methods defined in the `IChartingLibraryWidget` interface. This article describes the most commonly used methods. Refer to the [`IChartingLibraryWidget`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget) page to see the full list of methods.

## Advanced Charts methods

### onChartReady

The [`onChartReady`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#onchartready) method calls a callback when all data is loaded and the widget is ready. Therefore, you should call other widget methods only after the `onChartReady` callback.

```javascript
const widget = new TradingView.widget(/* Widget properties */);

widget.onChartReady(function() {
    widget.getChartLanguage();
});
```

### chart

The [`chart`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#chart) method returns an instance of the [`IChartWidgetApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi) interface that provides an extensive API for controlling the specific chart. For example, you can handle chart events, create indicators and drawings, change chart properties on the fly, and more. Consider the code sample below that adds the Bollinger Bands [indicator](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/) at the launch.

```javascript
widget.onChartReady(() => {
    const chart = widget.chart();
    chart.createStudy(
      "Bollinger Bands", // Indicator's name
      true,              // forceOverlay
      false,             // lock
      {
        in_0: 25,        // length
        in_1: 1,         // 'mult' indicator setting
      }
    );
});
```

The `chart` method has an optional `index` parameter. If you want to interact with a certain chart on the multiple-chart layout, you should call the `chart` method with the corresponding index as a parameter.

### activeChart

The [`activeChart`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#activechart) method retrieves [`IChartWidgetApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi) to interact with the currently selected chart. For example, the code sample below draws a vertical line on the chart.

```javascript
widget.activeChart().createMultipointShape(
  [{ price: 168, time: Date.UTC(2017, 10, 13) / 1000 }],
  { shape: 'vertical_line'}
);
```

You can also subscribe to events on the active chart, such as [`onIntervalChanged`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi#onintervalchanged).

```javascript
widget.activeChart().onIntervalChanged().subscribe(null, (interval, timeframeObj) =>
    timeframeObj.timeframe = {
        value: "12M",
        type: "period-back"
});
```

Note that the library does not manage the event subscriptions when users switch between the charts on the [multiple-chart layout](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#multiple-chart-layout). If necessary, you should manually unsubscribe from the previous chart and subscribe to the newly selected one using the corresponding [methods](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ISubscription). To track the currently active chart, use the [`activeChartChanged`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.SubscribeEventsMap#activechartchanged) event.

You can also find out the active chart's index using the [`activeChartIndex`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#activechartindex) method and subscribe to this chart using the [`chart`](#chart) method.

```javascript
const index = widget.activeChartIndex();
const chart = widget.chart(index);
```

### subscribe / unsubscribe

To listen to widget events, use the [`subscribe`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#subscribe) method on the widget instance. To stop listening, use [`unsubscribe`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#unsubscribe). The complete list of available event names and their callback signatures is defined in the [`SubscribeEventsMap`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.SubscribeEventsMap) interface.

For example, the code sample below handles an event when an indicator is added to the chart and prints the indicator's name to the console.

```javascript
widget.subscribe('study', (event) => { console.log(\`A ${event.value} indicator was added\`) });
```

For specific chart events (like symbol changes, data loading, or visible range updates), refer to the [Events and subscriptions](https://www.tradingview.com/charting-library-docs/latest/configuration/events-and-subscriptions) article.

### applyOverrides

The [`applyOverrides`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#applyoverrides) method allows you to change [Overrides](https://www.tradingview.com/charting-library-docs/latest/customization/overrides/) on the fly. The code sample below hides the main [series](https://www.tradingview.com/charting-library-docs/latest/resources/glossary#series).

```js
widget.applyOverrides({ "mainSeriesProperties.visible": false });
```

To apply overrides to a specific chart in a [multiple-chart layout](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#multiple-chart-layout), access the chart by its index:

```js
widget.chart(0).applyOverrides({ "mainSeriesProperties.visible": false });
```

### applyStudiesOverrides

The [`applyStudiesOverrides`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#applystudiesoverrides) method allows you to change [Overrides](https://www.tradingview.com/charting-library-docs/latest/customization/overrides/indicator-overrides) that affect [indicators](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/) (studies) on the fly. The code sample below changes the color of the Bollinger Bands indicator.

```js
widget.applyStudiesOverrides({
    'bollinger bands.median.color': '#33FF88'
});
```

Note that this method only changes the indicator's properties before the indicator is created. You should use the [`applyOverrides`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IStudyApi#applyoverrides) method in [`IStudyApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IStudyApi) to change an indicator that is already on the chart.

### setSymbol

The [`setSymbol`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#setsymbol) method sets a symbol and resolution of the active chart.

```javascript
widget.setSymbol('IBM', '1D', () => {
  // Your callback function
});
```

Note that a callback is evoked when the data for the new symbol is loaded.

### changeTheme

The [`changeTheme`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#changetheme) method allows you to change the [theme](https://www.tradingview.com/charting-library-docs/latest/customization/theme) on the fly. This method returns a promise that is resolved once the theme is applied. You can apply other style modifications after the promise is fulfilled.

```javascript
widget.changeTheme('Dark').then(() => {
    widget.chart().applyOverrides({ 'paneProperties.backgroundGradientStartColor': 'red' });
});
```

### onShortcut

The [`onShortcut`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#onshortcut) method allows you to override the built‑in [shortcuts](https://www.tradingview.com/charting-library-docs/latest/configuration/Shortcuts) or specify custom ones. For example, the code sample below specifies a shortcut that opens [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search).

```javascript
widget.onShortcut("alt+q", function() {
    widget.chart().executeActionById("symbolSearch");
});
```

Refer to the [Manage shortcuts](https://www.tradingview.com/charting-library-docs/latest/configuration/Shortcuts#manage-shortcuts) section for more examples.

### takeClientScreenshot

The [`takeClientScreenshot`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#takeclientscreenshot) method creates a snapshot of the chart and returns it as a canvas. You can then take the canvas element and create an image from it. The code sample below saves a screenshot as PNG.

```javascript
async function saveChartToPNG() {
  const screenshotCanvas = await widget.takeClientScreenshot();
  const linkElement = document.createElement('a');
  linkElement.download = 'screenshot';
  linkElement.href = screenshotCanvas.toDataURL(); // Alternatively, use \`toBlob\` which is a better API
  linkElement.dataset.downloadurl = ['image/png', linkElement.download, linkElement.href].join(':');
  document.body.appendChild(linkElement);
  linkElement.click();
  document.body.removeChild(linkElement);
}
saveChartToPNG(); // Call the screenshot function
```

### customThemes

The [`customThemes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#customthemes) method retrieves [`ICustomThemesApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ICustomThemesApi) that allows you to manage [custom themes](https://www.tradingview.com/charting-library-docs/latest/customization/styles/custom-themes). For example, you can reset the applied themes to the default values.

```javascript
let customThemesAPI = (await widget.customThemes());
customThemesAPI.resetCustomThemes();
```

### closePopupsAndDialogs

The [`closePopupsAndDialogs`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#closepopupsanddialogs) method closes any active dialog or [context menu](https://www.tradingview.com/charting-library-docs/latest/ui_elements/context-menu) on the chart.

```js
widget.closePopupsAndDialogs();
```

## Trading Platform methods

The methods below are available in [Trading Platform](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/) only.

### widgetbar

The [`widgetbar`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#widgetbar) method retrieves [`IWidgetbarApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IWidgetbarApi) that allows you to interact with the widget bar.

```javascript
widget.onChartReady(() => {
    widget.widgetbar().then(widgetbarApi => {
       widgetbarApi.isPageVisible('data_window');
    });
});
```

### watchList

The [`watchList`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#watchlist) method retrieves [`IWatchListApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IWatchListApi) that allows you to interact with the [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List) widget.

```javascript
const watchlistApi = await widget.watchList();
const activeListId = watchlistApi.getActiveListId();
const currentListItems = watchlistApi.getList(activeListId);
// Adds a new section and item to the current Watchlist
watchlistApi.updateList(activeListId, [...currentListItems, '###NEW SECTION', 'AMZN']);
```

### news

The [`news`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#news) method retrieves [`INewsApi`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.INewsApi) that allows you to interact with the [News](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/news) widget.

```javascript
widget.onChartReady(() => {
    widget.news().then(newsApi => {
        // newsApi is ready to use
    });
});
```

### chartsCount

The [`chartsCount`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartingLibraryWidget#chartscount) method counts a number of charts on the multiple-chart layout. In the code sample below, this method is used to interact with all the charts on the layout one by one.

```javascript
for (let i = 0; i < widget.chartsCount(); i++) { console.log(widget.chart(i).symbolExt().name) }
```