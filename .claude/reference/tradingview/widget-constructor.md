---
title: Widget Constructor | Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/configuration/Widget-Constructor
author: []
published: []
created: 2026-05-12
description: The Widget Constructor is the entry point to the library. It allows you to embed the library within your web page. You can use the Widget Constructor parameters to customize the widget's appearance and behavior. All parameters are listed in the ChartingLibraryWidgetOptions interface. If you use Trading Platform, you can specify some additional parameters.
tags: [clippings]
---
The Widget Constructor is the entry point to the library. It allows you to embed the library within your web page. You can use the Widget Constructor parameters to customize the widget's appearance and behavior. All parameters are listed in the [`ChartingLibraryWidgetOptions`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions) interface. If you use [Trading Platform](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/), you can specify some [additional parameters](#trading-platform-parameters).

The following video tutorial describes Widget Constructor parameters and demonstrates how to use them.

![](https://www.youtube.com/watch?v=bdvmM3FNnSY)
  

The code sample below shows how to adjust some basic parameters using Widget Constructor.

<iframe width="100%" height="375" src="https://jsfiddle.net/TradingView/8301r7nc/embedded/js,result/" allowfullscreen="" frameborder="0"></iframe>

[View Example on JSFiddle](https://jsfiddle.net/TradingView/8301r7nc)

## Advanced Charts parameters

The following parameters relate to Advanced Charts and Trading Platform.

### Widget configuration

Use the parameters below to configure basic widget settings:

| Parameter | Description |
| --- | --- |
| [`container`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#container)  [#](#container "Direct link to this Featureset") | Represents either a reference to an attribute of a DOM element inside which the iframe with the chart will be placed or the HTMLElement itself. |
| [`library_path`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#library_path)  [#](#library_path "Direct link to this Featureset") | A path to a static folder. |
| [`debug`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#debug)  [#](#debug "Direct link to this Featureset") | Makes the library write detailed Datafeed API logs into the browser console. Refer to [How to enable debug mode](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/enable-debug-mode) for more information. |

### Chart configuration

Use the parameters below to configure basic chart settings:

| Parameter | Description |
| --- | --- |
| [`symbol`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#symbol)  [#](#symbol "Direct link to this Featureset") | The default chart symbol. |
| [`interval`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#interval)  [#](#interval "Direct link to this Featureset") | The default chart interval. |
| [`timeframe`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#timeframe)  [#](#timeframe "Direct link to this Featureset") | The default chart time frame. |
| [`time_frames`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#time_frames)  [#](#time_frames "Direct link to this Featureset") | The list of visible time frames that can be selected at the bottom of the chart. |
| [`timezone`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#timezone)  [#](#timezone "Direct link to this Featureset") | The default chart time zone. |
| [`locale`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#locale)  [#](#locale "Direct link to this Featureset") | The default chart [`locale`](https://www.tradingview.com/charting-library-docs/latest/configuration/Localization/#supported-languages). |
| [`favorites`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#favorites)  [#](#favorites "Direct link to this Featureset") | Items that should be marked as favorite by default. |

### Data configuration

Use the parameters below to [connect data](https://www.tradingview.com/charting-library-docs/latest/connecting_data/) to the chart:

| Parameter | Description |
| --- | --- |
| [`datafeed`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#datafeed)  [#](#datafeed "Direct link to this Featureset") | A JavaScript object that implements the [`IBasicDataFeed`](https://www.tradingview.com/charting-library-docs/latest/api/modules/Charting_Library#ibasicdatafeed) interface to supply the chart with data. |
| [`additional_symbol_info_fields`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#additional_symbol_info_fields)  [#](#additional_symbol_info_fields "Direct link to this Featureset") | An optional field containing an array of custom symbol info fields to be shown in the Security Info dialog. |
| [`snapshot_url`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#snapshot_url)  [#](#snapshot_url "Direct link to this Featureset") | A URL that is used to send a POST request with binary chart snapshots when a user presses the snapshot button. |

### Chart size

Use the parameters below to customize the chart size:

| Parameter | Description |
| --- | --- |
| [`width`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#width)  [#](#width "Direct link to this Featureset") | The desired width of the widget. |
| [`height`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#height)  [#](#height "Direct link to this Featureset") | The desired height of the widget. |
| [`fullscreen`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#fullscreen)  [#](#fullscreen "Direct link to this Featureset") | A Boolean value showing whether the chart should use all the available space in the window. |
| [`autosize`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#autosize)  [#](#autosize "Direct link to this Featureset") | A Boolean value showing whether the chart should use all the available space in the container and resize when the container itself is resized. |

### UI customization

Use the parameters below to customize colors, fonts, price and date formats, and more:

| Parameter | Description |
| --- | --- |
| [`toolbar_bg`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#toolbar_bg)  [#](#toolbar_bg "Direct link to this Featureset") | A background color of the toolbars. |
| [`theme`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#theme)  [#](#theme "Direct link to this Featureset") | The predefined custom theme color for the chart. |
| [`custom_themes`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#custom_themes)  [#](#custom_themes "Direct link to this Featureset") | The custom color palette. |
| [`custom_css_url`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#custom_css_url)  [#](#custom_css_url "Direct link to this Featureset") | Adds your custom CSS to the chart. |
| [`custom_font_family`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#custom_font_family)  [#](#custom_font_family "Direct link to this Featureset") | Changes the font family used on the chart. |
| [`custom_formatters`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#custom_formatters)  [#](#custom_formatters "Direct link to this Featureset") | Custom formatters for adjusting the display format of price, date, and time values. |
| [`custom_translate_function`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#custom_translate_function)  [#](#custom_translate_function "Direct link to this Featureset") | Use this property to set [custom translations](https://www.tradingview.com/charting-library-docs/latest/configuration/Localization#custom-translations) for UI elements. |
| [`numeric_formatting`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#numeric_formatting)  [#](#numeric_formatting "Direct link to this Featureset") | An object that contains formatting options for numbers. |
| [`overrides`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#overrides)  [#](#overrides "Direct link to this Featureset") | Overrides values for the default widget properties. |
| [`settings_overrides`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#settings_overrides)  [#](#settings_overrides "Direct link to this Featureset") | An object that contains new values for values saved to the settings. |
| [`loading_screen`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#loading_screen)  [#](#loading_screen "Direct link to this Featureset") | An object that allows you to customize the loading spinner. |
| [`context_menu`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#context_menu)  [#](#context_menu "Direct link to this Featureset") |  |
| [`time_scale`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#time_scale)  [#](#time_scale "Direct link to this Featureset") | An additional optional field to add more bars on screen. |
| [`header_widget_buttons_mode`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#header_widget_buttons_mode)  [#](#header_widget_buttons_mode "Direct link to this Featureset") | An additional optional field to change the look and feel of buttons on the top toolbar. |

### Chart features

If you want to change the chart's behavior or show/hide UI elements, you should use [featuresets](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets). The following parameters allow you to enable/disable a certain featureset:

| Parameter | Description |
| --- | --- |
| [`enabled_features`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#enabled_features)  [#](#enabled_features "Direct link to this Featureset") | The array containing names of features that should be enabled by default. |
| [`disabled_features`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#disabled_features)  [#](#disabled_features "Direct link to this Featureset") | The array containing names of features that should be disabled by default. |

### Indicators and drawings

Use the parameters below to customize [indicators](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/) (studies) and [drawings](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/):

| Parameter | Description |
| --- | --- |
| [`study_count_limit`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#study_count_limit)  [#](#study_count_limit "Direct link to this Featureset") | Maximum amount of studies allowed at one time within the layout. |
| [`studies_access`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#studies_access)  [#](#studies_access "Direct link to this Featureset") | An object that allows you to specify indicators available for users. |
| [`studies_overrides`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#studies_overrides)  [#](#studies_overrides "Direct link to this Featureset") | Use this option to customize the style or inputs of the indicators. Refer to [Indicator Overrides](https://www.tradingview.com/charting-library-docs/latest/customization/overrides/indicator-overrides#specify-default-properties) for more information. |
| [`custom_indicators_getter`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#custom_indicators_getter)  [#](#custom_indicators_getter "Direct link to this Featureset") | A function that returns the Promise object with the array of your [custom indicators](https://www.tradingview.com/charting-library-docs/latest/custom_studies/#add-indicators). |
| [`drawings_access`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#drawings_access)  [#](#drawings_access "Direct link to this Featureset") | An object that allows you to specify drawing tools available for users. |

### Symbol search and comparison

Use the parameters below to customize the [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search):

| Parameter | Description |
| --- | --- |
| [`symbol_search_request_delay`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#symbol_search_request_delay)  [#](#symbol_search_request_delay "Direct link to this Featureset") | A threshold delay in milliseconds that is used to reduce the number of search requests when the user enters the symbol name in the *Symbol Search*. |
| [`symbol_search_complete`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#symbol_search_complete)  [#](#symbol_search_complete "Direct link to this Featureset") | Takes an additional search result object parameter, and returns an additional human-friendly symbol name. |
| [`compare_symbols`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#compare_symbols)  [#](#compare_symbols "Direct link to this Featureset") | An array of custom compare symbols for the Compare window. |

### Saving and loading chart

The following properties are used for saving and loading charts. For a detailed guide on which save/load approach to choose, see [Saving and loading charts](https://www.tradingview.com/charting-library-docs/latest/saving_loading/).

#### High-level APIs

Specify the following parameters to save/load a chart using the high-level APIs ([REST API](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-rest-api/) or [API handlers](https://www.tradingview.com/charting-library-docs/latest/saving_loading/save-load-adapter)).

| Parameter | Description | API type |
| --- | --- | --- |
| [`charts_storage_url`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#charts_storage_url)  [#](#charts_storage_url "Direct link to this Featureset") | A storage URL endpoint. | REST API |
| [`charts_storage_api_version`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#charts_storage_api_version)  [#](#charts_storage_api_version "Direct link to this Featureset") | A version of your backend. Supported values are: `1.0` or `1.1`. | REST API |
| [`client_id`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#client_id)  [#](#client_id "Direct link to this Featureset") | A client ID that represents a user group. | REST API |
| [`user_id`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#user_id)  [#](#user_id "Direct link to this Featureset") | A user ID that uniquely identifies each user within a `client_id` group. | REST API |
| [`save_load_adapter`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#save_load_adapter)  [#](#save_load_adapter "Direct link to this Featureset") | An object containing your custom save/load functions. | API handlers |
| [`load_last_chart`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#load_last_chart)  [#](#load_last_chart "Direct link to this Featureset") | A Boolean value showing whether the library should [load the last saved chart](https://www.tradingview.com/charting-library-docs/latest/saving_loading/#restore-last-saved-chart) for a user. | REST API or API handlers |

#### Low-level API

Specify the following parameters to save/load a chart using the [low-level API](https://www.tradingview.com/charting-library-docs/latest/saving_loading/low-level-api):

| Parameter | Description |
| --- | --- |
| [`auto_save_delay`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#auto_save_delay)  [#](#auto_save_delay "Direct link to this Featureset") | A threshold delay in seconds that is used to reduce the number of [`onAutoSaveNeeded`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.SubscribeEventsMap/#onautosaveneeded) calls. |
| [`saved_data`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#saved_data)  [#](#saved_data "Direct link to this Featureset") | An object containing saved chart layout. |
| [`saved_data_meta_info`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions/#saved_data_meta_info)  [#](#saved_data_meta_info "Direct link to this Featureset") | An object containing saved chart content meta info. |

#### User settings

[User settings](https://www.tradingview.com/charting-library-docs/latest/saving_loading/user-settings) are stored independently of chart layouts to ensure that users have control over their specific preferences. Use [`settings_adapter`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions#settings_adapter) to save user settings.

## Trading Platform parameters

All Trading Platform parameters are listed in the [`TradingTerminalWidgetOptions`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions) interface. Most of them duplicate the [Advanced Charts](#advanced-charts-parameters) parameters. Additional parameters are listed below:

| Parameter | Description |
| --- | --- |
| [`broker_config`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#broker_config)  [#](#broker_config "Direct link to this Featureset") | Configuration flags for Trading Platform. Refer to [Trading features configuration](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/trading-concepts#trading-features-configuration) for more information. |
| [`debug_broker`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#debug_broker)  [#](#debug_broker "Direct link to this Featureset") | Makes the library write detailed Broker API and Trading Host logs into the browser console. Refer to [How to enable debug mode](https://www.tradingview.com/charting-library-docs/latest/tutorials/tutorials/enable-debug-mode) for more information. |
| [`restConfig`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#restConfig)  [#](#restConfig "Direct link to this Featureset") | Connection configuration settings for the [Broker API](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/trading-concepts#broker-api). |
| [`widgetbar`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#widgetbar)  [#](#widgetbar "Direct link to this Featureset") | Settings for the widget panel on the right side of the chart. You can enable [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List), [News](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/news), [Details](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#details) and Data Window widgets on the right side of the chart using this property. |
| [`rss_news_feed`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#rss_news_feed)  [#](#rss_news_feed "Direct link to this Featureset") | Use this property to change the RSS feed for news. |
| [`rss_news_title`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#rss_news_title)  [#](#rss_news_title "Direct link to this Featureset") | Use this property to change the title for news widget when using a RSS feed. |
| [`news_provider`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#news_provider)  [#](#news_provider "Direct link to this Featureset") | Use this property to set your own news getter function. |
| [`trading_customization`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.TradingTerminalWidgetOptions/#trading_customization)  [#](#trading_customization "Direct link to this Featureset") | Overrides order and position lines created using the [`createOrderLine`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createorderline) and [`createPositionLine`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IChartWidgetApi/#createpositionline) methods. |