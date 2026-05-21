---
title: Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets
author: []
published: []
created: 2026-05-12
description: Featureset is a string literal that allows showing or hiding UI elements and changing the chart's behavior.
tags: [clippings]
---
**Featureset** is a string literal that allows showing or hiding UI elements and changing the chart's behavior.

## How to use

To enable or disable a feature, include it in the [`enabled_features`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions#enabled_features) or [`disabled_features`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions#disabled_features) array of the [Widget Constructor](https://www.tradingview.com/charting-library-docs/latest/configuration/Widget-Constructor) object.

```html
<script>
    new TradingView.widget({
        container: 'chartContainer',
        locale: 'en',
        library_path: 'charting_library/',
        datafeed: new Datafeeds.UDFCompatibleDatafeed("https://demo-feed-data.tradingview.com"),
        symbol: 'AAPL',
        interval: '1D',
        enabled_features: ["show_spread_operators"],
        disabled_features: ["items_favoriting", "show_object_tree"]
    });
</script>
```

This code sample enables the spread operators in the [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search) dialog and disables [*Add to favorites*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/#favorite-tools) and *Show Object tree* buttons in the UI.

## Simple and complex featuresets

Featuresets can be simple and complex where complex consists of the simple ones. Note that disabling complex featureset disables all its simple parts as well.

In the table below, simple featuresets are nested within complex featuresets using indentation.

| Featureset | Default state | Description |
| --- | --- | --- |
| `context_menus` [#](#context_menus "Direct link to this Featureset") | On | Shows any context menu when users right-click anywhere in the UI. |
| `legend_context_menu` [#](#legend_context_menu "Direct link to this Featureset") | On |  |
| `pane_context_menu` [#](#pane_context_menu "Direct link to this Featureset") | On |  |
| `scales_context_menu` [#](#scales_context_menu "Direct link to this Featureset") | On |  |
| `edit_buttons_in_legend` [#](#edit_buttons_in_legend "Direct link to this Featureset") | On | Shows the *Hide*, *Settings*, and *Remove* buttons in the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) for indicators and additional series. When disabled, only the ellipsis menu remains visible, and also all buttons in the main series legend are disabled. |
| `legend_inplace_edit` [#](#legend_inplace_edit "Direct link to this Featureset") | On | Enables in-place editing of indicators and series in the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend).   Note that disabling this featureset also hides the Symbol Search within the Legend. |
| `delete_button_in_legend` [#](#delete_button_in_legend "Direct link to this Featureset") | On | Shows the *Remove* button on the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) widget. |
| `format_button_in_legend` [#](#format_button_in_legend "Direct link to this Featureset") | On | Shows the *Settings* button on the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) widget. |
| `show_hide_button_in_legend` [#](#show_hide_button_in_legend "Direct link to this Featureset") | On | Shows the *Hide* and *Show* buttons on the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) widget. |
| `header_widget` [#](#header_widget "Direct link to this Featureset") | On |  |
| `header_chart_type` [#](#header_chart_type "Direct link to this Featureset") | On |  |
| `header_compare` [#](#header_compare "Direct link to this Featureset") | On | Shows the *Compare or Add Symbol* button on the header panel. |
| `header_fullscreen_button` [#](#header_fullscreen_button "Direct link to this Featureset") | On |  |
| `header_indicators` [#](#header_indicators "Direct link to this Featureset") | On |  |
| `header_resolutions` [#](#header_resolutions "Direct link to this Featureset") | On |  |
| `show_interval_dialog_on_key_press` [#](#show_interval_dialog_on_key_press "Direct link to this Featureset") | On | Opens the *Change Interval* dialog when users type digits or press the comma key. |
| `header_screenshot` [#](#header_screenshot "Direct link to this Featureset") | On | Shows the *Take a snapshot* button on the header panel. |
| `header_settings` [#](#header_settings "Direct link to this Featureset") | On |  |
| `header_symbol_search` [#](#header_symbol_search "Direct link to this Featureset") | On |  |
| `header_undo_redo` [#](#header_undo_redo "Direct link to this Featureset") | On |  |
| `header_quick_search` [#](#header_quick_search "Direct link to this Featureset") | On |  |
| `symbol_search_hot_key` [#](#symbol_search_hot_key "Direct link to this Featureset") | On | Allows opening [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search/) using the typing keys. |
| `use_localstorage_for_settings` [#](#use_localstorage_for_settings "Direct link to this Featureset") | On | Allows storing chart properties and [user settings](https://www.tradingview.com/charting-library-docs/latest/saving_loading/user-settings), including favorites, in the browser's [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).   Refer to the [Customization precedence](https://www.tradingview.com/charting-library-docs/latest/customization/customization-precedence/) article to learn more about the application order of `localStorage` among other approaches. |
| `save_chart_properties_to_local_storage` [#](#save_chart_properties_to_local_storage "Direct link to this Featureset") | On | Can be disabled to forbid storing chart properties in the [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) while allowing to save other properties. The other properties include favorites in Advanced Charts, and [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List) symbols and some panel states in Trading Platform. |

## Visibility of controls and visual elements

| Featureset | Default state | Description |
| --- | --- | --- |
| `adaptive_logo` [#](#adaptive_logo "Direct link to this Featureset") | On | Shows the *Chart by TradingView* text on small-screen devices. |
| `always_show_legend_values_on_mobile` [#](#always_show_legend_values_on_mobile "Direct link to this Featureset") | Off | Shows legend values when on mobile. |
| `border_around_the_chart` [#](#border_around_the_chart "Direct link to this Featureset") | On | Adds a 2px padding to the chart. |
| `chart_style_hilo` [#](#chart_style_hilo "Direct link to this Featureset") | Off | Adds *High-Low* option to the chart style controls. |
| `chart_style_hilo_last_price` [#](#chart_style_hilo_last_price "Direct link to this Featureset") | Off | Enables last price line and price axis label on the *High-Low* chart style. |
| `chart_property_page_right_margin_editor` [#](#chart_property_page_right_margin_editor "Direct link to this Featureset") | On | Shows the *Right margin* field in *Settings → Appearance* |
| `chart_property_page_scales` [#](#chart_property_page_scales "Direct link to this Featureset") | On | Allows [Overrides](https://www.tradingview.com/charting-library-docs/latest/customization/overrides/) for the *Price Scale*. |
| `clear_price_scale_on_error_or_empty_bars` [#](#clear_price_scale_on_error_or_empty_bars "Direct link to this Featureset") | On | Clears the pane price scales when the main series has an error or no bars. |
| `compare_symbol_search_spread_operators` [#](#compare_symbol_search_spread_operators "Direct link to this Featureset") | Off | Shows the [spread operators](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/#enable-spread-operators) in the *Compare symbol* dialog. Note that you must also enable [`show_spread_operators`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_spread_operators). |
| `control_bar` [#](#control_bar "Direct link to this Featureset") | On | Shows the *Zoom In/Out* and *Scroll to the Left/Right* navigation buttons at the bottom of the chart. |
| `countdown` [#](#countdown "Direct link to this Featureset") | On | Shows the *Countdown to bar close* option on the [*Price Scale*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Price-Scale). |
| `display_data_mode` [#](#display_data_mode "Direct link to this Featureset") | Off | Enables an icon and the [*Data is delayed*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend#display-delayed-data-information) section in the *Legend*. |
| `display_legend_on_all_charts` [#](#display_legend_on_all_charts "Direct link to this Featureset") | Off | Display the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) widget on all diagrams regardless of the crosshair synchronization. |
| `display_market_status` [#](#display_market_status "Direct link to this Featureset") | On | Shows the market status on the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) widget. |
| `dont_show_boolean_study_arguments` [#](#dont_show_boolean_study_arguments "Direct link to this Featureset") | Off | Shows true and false [indicator](https://www.tradingview.com/charting-library-docs/latest/custom_studies/) arguments. |
| `go_to_date` [#](#go_to_date "Direct link to this Featureset") | On | Shows the *Go to* option that allows jumping to a particular bar. |
| `header_saveload` [#](#header_saveload "Direct link to this Featureset") | On | Shows the *Save layout* and *Load layout* buttons (the feature is not part of the `header_widget` featureset). |
| `hide_image_invalid_symbol` [#](#hide_image_invalid_symbol "Direct link to this Featureset") | Off | Hides the image that is shown to illustrate an invalid symbol. |
| `hide_last_na_study_output` [#](#hide_last_na_study_output "Direct link to this Featureset") | Off | Shows last N/A [indicator](https://www.tradingview.com/charting-library-docs/latest/custom_studies/) output data. |
| `hide_left_toolbar_by_default` [#](#hide_left_toolbar_by_default "Direct link to this Featureset") | Off | Shows left toolbar when a user opens the chart for the first time. |
| `hide_main_series_symbol_from_indicator_legend` [#](#hide_main_series_symbol_from_indicator_legend "Direct link to this Featureset") | On | Hides the optional symbol input value from the indicator legend if the *Main chart symbol* option is selected. |
| `hide_price_scale_global_last_bar_value` [#](#hide_price_scale_global_last_bar_value "Direct link to this Featureset") | Off | Hides the global last price label on the [*Price Scale*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Price-Scale) if the last bar is outside of the visible range. |
| `hide_exponentiation_spread_operator` [#](#hide_exponentiation_spread_operator "Direct link to this Featureset") | Off | Shows the exponentiation spread operator (^) in the [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search) dialog. |
| `hide_reciprocal_spread_operator` [#](#hide_reciprocal_spread_operator "Direct link to this Featureset") | Off | Shows reciprocal spread operator (1/x) in the [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search) dialog. |
| `hide_object_tree_and_price_scale_exchange_label` [#](#hide_object_tree_and_price_scale_exchange_label "Direct link to this Featureset") | Off | Hides the exchange label from the displayed label. |
| `hide_resolution_in_legend` [#](#hide_resolution_in_legend "Direct link to this Featureset") | Off | Shows the interval (D, 2D, W, M, etc.) in the chart legend and the data window. |
| `hide_unresolved_symbols_in_legend` [#](#hide_unresolved_symbols_in_legend "Direct link to this Featureset") | Off | Shows unresolved symbols in the chart legend and the data window. |
| `items_favoriting` [#](#items_favoriting "Direct link to this Featureset") | On | Shows the *Add to favorites* icon for chart types, drawings, indicators, and resolutions. |
| `left_toolbar` [#](#left_toolbar "Direct link to this Featureset") | On | Shows the [*Drawings*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/) toolbar on the left panel. |
| `legend_widget` [#](#legend_widget "Direct link to this Featureset") | On | Shows the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend#hide-legend) widget on the top-left corner of any chart. |
| `main_series_scale_menu` | On | Shows the *Settings* button in the right-bottom corner of the chart. |
| `object_tree_legend_mode` [#](#object_tree_legend_mode "Direct link to this Featureset") | On | Shows the [*Show Object tree*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/object-tree) button in the legend at a small width. |
| `pricescale_currency` [#](#pricescale_currency "Direct link to this Featureset") | Off | Shows the *Currency* context menu in *Chart Settings → Scales*. The menu allows selecting the visibility of the currency in which the instrument is traded on the price scale. Refer to the [Instrument currency](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Price-Scale#instrument-currency) section for more information. |
| `pricescale_unit` [#](#pricescale_unit "Direct link to this Featureset") | Off | Shows the *Unit* context menu in *Chart Settings → Scales*. The menu allows selecting the visibility of the unit in which the instrument is traded on the [*Price Scale*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Price-Scale). |
| `pre_post_market_sessions` [#](#pre_post_market_sessions "Direct link to this Featureset") | Off | Enables pre- and post-market session support. For more information, refer to [*Extended sessions*](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Extended-Sessions). |
| `property_pages` [#](#property_pages "Direct link to this Featureset") | On | Shows all *Settings* pages. |
| `popup_hints` [#](#popup_hints "Direct link to this Featureset") | On | Shows pop-up hints about possible mouse/shortcut/UI actions. |
| `remove_library_container_border` [#](#remove_library_container_border "Direct link to this Featureset") | On | Sets the border style to 0px and padding to 1px. |
| `scales_date_format` [#](#scales_date_format "Direct link to this Featureset") | On | Shows the *Date format* selector in *Chart settings*. |
| `scales_time_hours_format` [#](#scales_time_hours_format "Direct link to this Featureset") | On | Shows the *Time hours format* selector in *Chart settings*. |
| `show_chart_property_page` [#](#show_chart_property_page "Direct link to this Featureset") | On | Enables the *Chart settings* page. |
| `show_average_close_price_line_and_label` [#](#show_average_close_price_line_and_label "Direct link to this Featureset") | Off | Shows the visibility settings of the label and the average close price line. |
| `show_exchange_logos` [#](#show_exchange_logos "Direct link to this Featureset") | Off | Shows logos for the exchanges within the [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search) dialog. |
| `show_right_widgets_panel_by_default` [#](#show_right_widgets_panel_by_default "Direct link to this Featureset") | On | Opens the right widget toolbar on the first launch. |
| `show_symbol_logos` [#](#show_symbol_logos "Direct link to this Featureset") | Off | Shows logos for the symbols within [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search), the [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List) widget, the *Cancel order* dialog, and the *Close position* dialog. |
| `show_symbol_logo_for_compare_studies` [#](#show_symbol_logo_for_compare_studies "Direct link to this Featureset") | On | Shows the symbol's logo within the legend for compare studies. Note that you must also enable [`show_symbol_logos`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_symbol_logos) and [`show_symbol_logo_in_legend`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_symbol_logo_in_legend). |
| `show_symbol_logo_in_legend` [#](#show_symbol_logo_in_legend "Direct link to this Featureset") | On | Display the main symbol's logo within the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend). Note that you must also enable [`show_symbol_logos`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_symbol_logos). |
| `show_object_tree` [#](#show_object_tree "Direct link to this Featureset") | On | Shows the [*Show Object tree*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/object-tree) button on the left or right toolbar depending on the product and configuration. |
| `show_percent_option_for_right_margin` [#](#show_percent_option_for_right_margin "Direct link to this Featureset") | Off | Shows the option to specify the default right margin in percentage in the *Appearance → Chart settings* dialog. |
| `show_spread_operators` [#](#show_spread_operators "Direct link to this Featureset") | Off | Shows the spread operators in the [*Symbol Search*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search#enable-spread-operators) dialog. |
| `show_zoom_and_move_buttons_on_touch` [#](#show_zoom_and_move_buttons_on_touch "Direct link to this Featureset") | Off | On touch devices, shows the zoom and move buttons at the bottom of the chart. Note that these buttons appear only when the [time scale](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Time-Scale) is pressed. |
| `snapshot_trading_drawings` [#](#snapshot_trading_drawings "Direct link to this Featureset") | Off | Includes orders, positions, and executions in the screenshot. |
| `source_selection_markers` [#](#source_selection_markers "Direct link to this Featureset") | On | Enables selection markers for series and indicators. |
| `studies_symbol_search_spread_operators` [#](#studies_symbol_search_spread_operators "Direct link to this Featureset") | Off | Shows the spread operators for some indicators (for example Volume and Moving Average) in the *Settings → Inputs → Another symbol → Change symbol* dialog. Note that you should also enable [`show_spread_operators`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_spread_operators). |
| `symbol_info` [#](#symbol_info "Direct link to this Featureset") | On | Shows the *Symbol Info* option on the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend) widget. |
| `symbol_info_long_description` [#](#symbol_info_long_description "Direct link to this Featureset") | Off | Enables long symbol descriptions to be shown in the main series and compare studies legends if provided in the symbol info data. |
| `symbol_info_price_source` [#](#symbol_info_price_source "Direct link to this Featureset") | Off | Shows symbol price source in the main series and *Compare* indicator legends. You should also provide the [`price_source_id`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/#price_source_id) and [`price_sources`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.LibrarySymbolInfo/#price_sources) properties in the `LibrarySymbolInfo` object. |
| `timeframes_toolbar` [#](#timeframes_toolbar "Direct link to this Featureset") | On | Shows the [*Time frame*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Time-Scale#time-frame-toolbar) toolbar at the bottom of the chart. |
| `timezone_menu` [#](#timezone_menu "Direct link to this Featureset") | On | Enables the *Time zone* dropdown list that allows switching the time zone from the bottom toolbar. |
| `use_na_string_for_not_available_values` [#](#use_na_string_for_not_available_values "Direct link to this Featureset") | Off | Shows a literal "N/A" for not available values instead of "∅". |
| `use_symbol_name_for_header_toolbar` [#](#use_symbol_name_for_header_toolbar "Direct link to this Featureset") | Off | Uses the name of a symbol rather than its ticker name in the Symbol Search dialog and header button.   Available from version 29.4.0. |
| `always_show_study_symbol_input_values_in_legend` [#](#always_show_study_symbol_input_values_in_legend "Direct link to this Featureset") | Off | Keeps symbol-type [indicator inputs](https://www.tradingview.com/charting-library-docs/latest/custom_studies/metainfo/Custom-Studies-Inputs) (`StudySymbolInputInfo`) visible in the legend, even when other indicator inputs are hidden. |

## Elements placement

| Featureset | Default state | Description |
| --- | --- | --- |
| `move_logo_to_main_pane` [#](#move_logo_to_main_pane "Direct link to this Featureset") | Off | Places the logo on the main [series](https://www.tradingview.com/charting-library-docs/latest/resources/glossary#series/) pane instead of the bottom pane. |

## Behavior

| Featureset | Default state | Description |
| --- | --- | --- |
| `accessible_keyboard_shortcuts` [#](#accessible_keyboard_shortcuts "Direct link to this Featureset") | Off | Changes the keyboard navigation shortcut from Alt + Z to Tab. Refer to [Keyboard navigation](https://www.tradingview.com/charting-library-docs/latest/configuration/accessibility#keyboard-navigation) for more information. |
| `allow_arbitrary_symbol_search_input` [#](#allow_arbitrary_symbol_search_input "Direct link to this Featureset") | Off | Enables or disables the ability for users to enter arbitrary input in the [Symbol Search](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Symbol-Search) dialog. When this feature is **disabled** (default behavior), pressing the \_Enter\_ key without selecting a search result will automatically select the top search result as the input value. If no results are available, pressing \_Enter\_ will have no effect.   When this feature is **enabled**, the user's direct input will be used as the selected value, regardless of whether it matches any search results. This input will then be passed to the data feed for resolution and loading. |
| `aria_crosshair_price_description` [#](#aria_crosshair_price_description "Direct link to this Featureset") | Off | Announces, via the screen reader, the price when the crosshair is moved on the chart. Currently only supported for the English language. |
| `aria_detailed_chart_descriptions` [#](#aria_detailed_chart_descriptions "Direct link to this Featureset") | Off | Generates a more detailed ARIA description of the chart for screen readers when the active chart is changed by the user. The more detailed description includes a brief description of the price values for the main series.   ARIA descriptions are currently only provided for the English language. You can use the [custom\_chart\_description\_function](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.ChartingLibraryWidgetOptions#custom_chart_description_function) constructor option if you wish to add support for additional languages. |
| `auto_enable_symbol_labels` [#](#auto_enable_symbol_labels "Direct link to this Featureset") | On | Shows the symbol name label when comparing symbols. |
| `axis_pressed_mouse_move_scale` [#](#axis_pressed_mouse_move_scale "Direct link to this Featureset") | On | Enables axis scaling with the left mouse button pressed. |
| `chart_drag_export` [#](#chart_drag_export "Direct link to this Featureset") | Off | Enables chart drag event handling. See [Enable drag-to-export feature](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Chart#enable-drag-to-export-feature) for more implementation details. |
| `chart_scroll` [#](#chart_scroll "Direct link to this Featureset") | On | Enables chart scrolling. |
| `chart_zoom` [#](#chart_zoom "Direct link to this Featureset") | On | Enables chart zooming. |
| `charting_library_debug_mode` [#](#charting_library_debug_mode "Direct link to this Featureset") | Off | Enables logs. |
| `confirm_overwrite_if_chart_layout_with_name_exists` [#](#confirm_overwrite_if_chart_layout_with_name_exists "Direct link to this Featureset") | Off | By default, many chart layouts can be saved with the same name. If this feature is enabled, the library will prompt to confirm overwriting chart layouts with the same name when saving, renaming, or cloning *(Save as)*. |
| `create_volume_indicator_by_default` [#](#create_volume_indicator_by_default "Direct link to this Featureset") | On | Adds the [*Volume* indicator](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/#volume-indicator/) upon the chart initialization. |
| `create_volume_indicator_by_default_once` [#](#create_volume_indicator_by_default_once "Direct link to this Featureset") | On | Prevents the [*Volume* indicator](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/#volume-indicator/) from being recreated when an instrument or a resolution is switched. |
| `constraint_dialogs_movement` [#](#constraint_dialogs_movement "Direct link to this Featureset") | On | Keeps the dialogs within the chart. |
| `cropped_tick_marks` [#](#cropped_tick_marks "Direct link to this Featureset") | On | Shows partially visible price labels on price axis. |
| `custom_resolutions` [#](#custom_resolutions "Direct link to this Featureset") | Off | Allows adding [custom resolutions](https://www.tradingview.com/charting-library-docs/latest/configuration/Resolution/#enable-custom-resolutions) in the UI. |
| `datasource_copypaste` [#](#datasource_copypaste "Direct link to this Featureset") | On | Enables copying of [drawings](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/) and [indicators](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/). |
| `determine_first_data_request_size_using_visible_range` [#](#determine_first_data_request_size_using_visible_range "Direct link to this Featureset") | Off | By default, the chart requests a small, fixed number of bars for the initial data request when the chart is first created. If this feature is enabled, the library will calculate the request size based on the number of bars that will be visible on the chart. |
| `disable_pulse_animation` [#](#disable_pulse_animation "Direct link to this Featureset") | Off | Disables the pulse animation when chart type is set to Line. |
| `disable_resolution_rebuild` [#](#disable_resolution_rebuild "Direct link to this Featureset") | Off | Shows bar time exactly as provided by the datafeed, without adjustments. For more information, refer to [Resolution](https://www.tradingview.com/charting-library-docs/latest/configuration/Resolution/#disable-resolution-rebuilding). |
| `end_of_period_timescale_marks` [#](#end_of_period_timescale_marks "Direct link to this Featureset") | Off | Toggles the timeline marks to display the bar's end time. |
| `fix_left_edge` [#](#fix_left_edge "Direct link to this Featureset") | Off | Prevents scrolling to the left of the first historical bar. |
| `header_in_fullscreen_mode` [#](#header_in_fullscreen_mode "Direct link to this Featureset") | Off |  |
| `hide_price_scale_if_all_sources_hidden` [#](#hide_price_scale_if_all_sources_hidden "Direct link to this Featureset") | Off | Hides the [price scale](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Price-Scale/) if all indicators or series attached to the price scale are hidden. |
| `horz_touch_drag_scroll` [#](#horz_touch_drag_scroll "Direct link to this Featureset") | On | Enables the chart to handle the horizontal pointer movements on touch screens. In this case, the webpage is not scrolled. If disabled, the webpage is scrolled instead.      Note that if the user starts scrolling the chart vertically or horizontally, scrolling is continued in any direction until the user releases the finger. |
| `inactivity_gaps` [#](#inactivity_gaps "Direct link to this Featureset") | Off | Allows displaying inactivity gaps on charts. These gaps represent periods within the trading session when there has been no trading activity. For more information, refer to the [Show/hide gaps](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Chart/#showhide-gaps-on-the-chart) section. |
| `iframe_loading_compatibility_mode` [#](#iframe_loading_compatibility_mode "Direct link to this Featureset") | Off | Enables alternative loading mode for the library, which can be used to support older browsers and a few non-standard browsers. |
| `iframe_loading_same_origin` [#](#iframe_loading_same_origin "Direct link to this Featureset") | Off | Enables an alternative loading mode for the library, which can be used when the iframe content must be served from the same origin.   Available from version 28. |
| `insert_indicator_dialog_shortcut` [#](#insert_indicator_dialog_shortcut "Direct link to this Featureset") | On | Enables the *Open indicator* [shortcut](https://www.tradingview.com/charting-library-docs/latest/configuration/Shortcuts#chart) (/). |
| `disable_legend_inplace_resolution_change` [#](#disable_legend_inplace_resolution_change "Direct link to this Featureset") | Off | Disables the ability to in-place change the resolution of a series in the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend). |
| `disable_legend_inplace_symbol_change` [#](#disable_legend_inplace_symbol_change "Direct link to this Featureset") | Off | Disables the ability to in-place change the symbol of a series or study in the [*Legend*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend). |
| `legend_bar_change_colors_based_on_value` [#](#legend_bar_change_colors_based_on_value "Direct link to this Featureset") | Off | Enables dynamic coloring of bar change values in the legend. For non-OHLC chart types, colors are based on the value (positive, negative, or zero). For OHLC types, the library uses the colors defined for the series. |
| `library_custom_color_themes` [#](#library_custom_color_themes "Direct link to this Featureset") | On | Enables [*Custom Themes API*](https://www.tradingview.com/charting-library-docs/latest/customization/styles/custom-themes).   Available from version 28. |
| `lock_visible_time_range_on_resize` [#](#lock_visible_time_range_on_resize "Direct link to this Featureset") | Off | Prevents changing visible time area on chart resizing. |
| `lock_visible_time_range_when_adjusting_percentage_right_margin` [#](#lock_visible_time_range_when_adjusting_percentage_right_margin "Direct link to this Featureset") | Off | Lock the visible range when adjusting the percentage right margin via the settings dialog. This applies when the chart is already at the current default margin position. |
| `long_press_floating_tooltip` [#](#long_press_floating_tooltip "Direct link to this Featureset") | On | Enables the floating tooltip on long press. The tooltip displays detailed OHLC values and the price change for the selected bar. |
| `low_density_bars` [#](#low_density_bars "Direct link to this Featureset") | Off | Allows zooming in to one bar in the viewport. |
| `mouse_wheel_scale` [#](#mouse_wheel_scale "Direct link to this Featureset") | On | Enables series scaling with a mouse wheel. |
| `mouse_wheel_scroll` [#](#mouse_wheel_scroll "Direct link to this Featureset") | On | Enables chart scrolling with a horizontal mouse wheel. |
| `no_min_chart_width` [#](#no_min_chart_width "Direct link to this Featureset") | Off | Disables the minimum chart width limit. |
| `pinch_scale` [#](#pinch_scale "Direct link to this Featureset") | On | Enables series scaling with pinch/zoom gestures. This feature is supported on touch devices only. |
| `pressed_mouse_move_scroll` [#](#pressed_mouse_move_scroll "Direct link to this Featureset") | On | Enables chart scrolling with the left mouse button pressed. |
| `pre_post_market_price_line` [#](#pre_post_market_price_line "Direct link to this Featureset") | Off | Enables the [pre-/post-market price lines](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Extended-Sessions#enable-the-price-line).   Available from version 29.1. |
| `request_only_visible_range_on_reset` [#](#request_only_visible_range_on_reset "Direct link to this Featureset") | Off | When the [chart data is reset](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Datafeed-Issues#internet-connection-issues), this featureset enables re-requesting the data for just the visible range, instead of the entire range of the existing loaded data. |
| `right_bar_stays_on_scroll` [#](#right_bar_stays_on_scroll "Direct link to this Featureset") | On | Determines the behavior of the *Zoom* feature: the bar under the mouse cursor stays in the same place if this feature is disabled |
| `save_shortcut` [#](#save_shortcut "Direct link to this Featureset") | On | Enables the *Save chart layout* [shortcut](https://www.tradingview.com/charting-library-docs/latest/configuration/Shortcuts#chart) (Ctrl + S). |
| `saveload_separate_drawings_storage` [#](#saveload_separate_drawings_storage "Direct link to this Featureset") | Off | Enables an [alternative saving and loading mode](https://www.tradingview.com/charting-library-docs/latest/saving_loading#save-drawings-separately) for the library. This mode saves the state of the drawings separately from the [chart layout](https://www.tradingview.com/charting-library-docs/latest/saving_loading#chart-templates). |
| `seconds_resolution` [#](#seconds_resolution "Direct link to this Featureset") | Off | Enables the support of [resolutions](https://www.tradingview.com/charting-library-docs/latest/configuration/Resolution/) in seconds. |
| `secondary_series_extend_time_scale` [#](#secondary_series_extend_time_scale "Direct link to this Featureset") | Off | Allows an additional series to [extend the time scale](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Studies-Extending-The-Time-Scale/#for-overlay-study). |
| `shift_visible_range_on_new_bar` [#](#shift_visible_range_on_new_bar "Direct link to this Featureset") | On | If disabled, adding a new bar zooms the chart out preserving the first visible point. Otherwise, when a new bar appears, the chart is scrolled one point to the left. |
| `side_toolbar_in_fullscreen_mode` [#](#side_toolbar_in_fullscreen_mode "Direct link to this Featureset") | Off | Enables the [*Drawings*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/) toolbar in the full screen mode. |
| `studies_extend_time_scale` [#](#studies_extend_time_scale "Direct link to this Featureset") | Off | Enables custom indicators to [extend the time scale](https://www.tradingview.com/charting-library-docs/latest/custom_studies/Studies-Extending-The-Time-Scale) if `canExtendTimeScale` is set to `true` in the indicator's metainfo. |
| `study_templates` [#](#study_templates "Direct link to this Featureset") | Off | Enables a button in the header to load/save *Indicator template*. |
| `study_symbol_ticker_description` [#](#study_symbol_ticker_description "Direct link to this Featureset") | Off | Applies the symbol display mode (ticker/description) to the indicator inputs in the status line. |
| `study_overlay_compare_legend_option` [#](#study_overlay_compare_legend_option "Direct link to this Featureset") | Off | Applies the symbol display mode (ticker/description) to overlay/compare indicators in the status line. |
| `tick_resolution` [#](#tick_resolution "Direct link to this Featureset") | Off | Enables the support of [resolutions](https://www.tradingview.com/charting-library-docs/latest/configuration/Resolution/) in ticks. |
| `two_character_bar_marks_labels` [#](#two_character_bar_marks_labels "Direct link to this Featureset") | Off | Allows displaying up to two characters in bar marks. The default behavior is to only display one character. |
| `uppercase_instrument_names` [#](#uppercase_instrument_names "Direct link to this Featureset") | On | When disabled, this feature allows a user to enter case-sensitive symbols. |
| `use_last_visible_bar_value_in_legend` [#](#use_last_visible_bar_value_in_legend "Direct link to this Featureset") | Off | By default, the legend shows the most recent "global" bar value. When this featureset is enabled, the rightmost bar in the visible range is used instead. |
| `vert_touch_drag_scroll` [#](#vert_touch_drag_scroll "Direct link to this Featureset") | On | Enables the chart to handle the vertical pointer movements on touch screens. In this case, the webpage is not scrolled. If disabled, the webpage is scrolled instead.      Note that if the user starts scrolling the chart vertically or horizontally, scrolling is continued in any direction until the user releases the finger. |
| `volume_force_overlay` [#](#volume_force_overlay "Direct link to this Featureset") | On | Places the [*Volume* indicator](https://www.tradingview.com/charting-library-docs/latest/ui_elements/indicators/#volume-indicator/) on the same pane with the main [series](https://www.tradingview.com/charting-library-docs/latest/resources/glossary#series/). |

## Trading Platform

> [!-info] -info
> info
> These featuresets are only available in [Trading Platform](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/).

| Featureset | Default state | Description |
| --- | --- | --- |
| `add_to_watchlist` [#](#add_to_watchlist "Direct link to this Featureset") | On | Enables the *Add symbol to Watchlist* option in the menu. |
| `always_pass_called_order_to_modify` [#](#always_pass_called_order_to_modify "Direct link to this Featureset") | Off | If a bracket order is modified, the terminal passes its parent order to [`modifyOrder`](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IBrokerTerminal?_highlight=modifyorder#modifyorder). The featureset disables this behavior. |
| `buy_sell_buttons` [#](#buy_sell_buttons "Direct link to this Featureset") | On | Shows the *Buy/Sell* buttons in the [Legend](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend). |
| `broker_button` [#](#broker_button "Direct link to this Featureset") | On | Shows the *Broker* button () in the [Legend](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Legend). |
| `chart_crosshair_menu` [#](#chart_crosshair_menu "Direct link to this Featureset") | On | Shows the *Plus* button on the price scale for [quick trading](https://www.tradingview.com/charting-library-docs/latest/ui_elements/Price-Scale#quick-trading). Note that this menu will be empty unless you implement the [Broker API](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/trading-concepts/#broker-api). |
| `chart_hide_close_position_button` [#](#chart_hide_close_position_button "Direct link to this Featureset") | Off | Hides the close button for positions. |
| `chart_hide_close_order_button` [#](#chart_hide_close_order_button "Direct link to this Featureset") | Off | Hides the close button for orders. |
| `chart_property_page_trading` [#](#chart_property_page_trading "Direct link to this Featureset") | On | Shows the *Trading* section in *Chart settings*. |
| `chart_template_storage` [#](#chart_template_storage "Direct link to this Featureset") | Off | Enables saving/loading [chart templates](https://www.tradingview.com/charting-library-docs/latest/saving_loading/#chart-templates). To store chart templates, implement the logic for [API handlers](https://www.tradingview.com/charting-library-docs/latest/saving_loading/). |
| `drawing_templates` [#](#drawing_templates "Direct link to this Featureset") | On | Enables [Drawing Templates](https://www.tradingview.com/charting-library-docs/latest/ui_elements/drawings/#templates) on the Drawing toolbar. |
| `dom_widget` [#](#dom_widget "Direct link to this Featureset") | Off | Enables the [Depth of Market](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/depth-of-market) widget visibility. |
| `static_dom` [#](#static_dom "Direct link to this Featureset") | Off | Enables the [Depth of Market](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/depth-of-market) widget's static mode. This means that the price series is fixed, while the current price moves within, above, or below the designated range. |
| `header_layouttoggle` [#](#header_layouttoggle "Direct link to this Featureset") | On | Shows the *Select Layout* button on the top toolbar. Using this button, users can select [multiple-chart layouts.](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#multiple-chart-layout) |
| `hide_right_toolbar` [#](#hide_right_toolbar "Direct link to this Featureset") | Off | Hides the right toolbar when initializing the chart to free up space. The toolbar can be shown/hidden later using the [WidgetBar API](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.IWidgetbarApi). |
| `hide_right_toolbar_tabs` [#](#hide_right_toolbar_tabs "Direct link to this Featureset") | Off | Hides the tabs within the right toolbar. |
| `keep_object_tree_widget_in_right_toolbar` [#](#keep_object_tree_widget_in_right_toolbar "Direct link to this Featureset") | Off | Keeps the [*Object tree*](https://www.tradingview.com/charting-library-docs/latest/ui_elements/object-tree) in the right toolbar. If the [`right_toolbar`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#right_toolbar) featureset is not enabled, this feature will not work. |
| `legend_last_day_change` [#](#legend_last_day_change "Direct link to this Featureset") | Off | Adds the *Last day change values* option to the *Chart Settings* dialog in the UI. This option allows users to show/hide the last day change values in the main series legend. |
| `multiple_watchlists` [#](#multiple_watchlists "Direct link to this Featureset") | On | Enables creating multiple [Watchlists](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List). |
| `open_account_manager` [#](#open_account_manager "Direct link to this Featureset") | On | Keeps the [Account Manager](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/account-manager) opened by default. |
| `order_info` [#](#order_info "Direct link to this Featureset") | On | Shows the order information section in the *Order Ticket*. |
| `order_panel` [#](#order_panel "Direct link to this Featureset") | On | Shows the [Order Ticket](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/order-ticket). Note that disabling this featureset also hides the *Trade* button in the [Account Manager](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/account-manager). |
| `order_panel_close_button` [#](#order_panel_close_button "Direct link to this Featureset") | On | Shows the *Close Order Ticket* button. |
| `order_panel_undock` [#](#order_panel_undock "Direct link to this Featureset") | On | Shows the *Undock* button in the *Order Ticket* settings. |
| `prefer_symbol_name_over_fullname` [#](#prefer_symbol_name_over_fullname "Direct link to this Featureset") | On | Displays the symbol name instead of the `exchange:name` combination in the UI.   Available from version 28. |
| `right_toolbar` [#](#right_toolbar "Direct link to this Featureset") | On | Shows the right toolbar with buttons. |
| `show_dom_first_time` [#](#show_dom_first_time "Direct link to this Featureset") | Off | Shows the [Depth of Market](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/depth-of-market) widget when a user opens the chart for the first time. |
| `show_last_price_and_change_only_in_series_legend` [#](#show_last_price_and_change_only_in_series_legend "Direct link to this Featureset") | Off | Shows only the last price and change values in the main series legend. |
| `show_order_panel_on_start` [#](#show_order_panel_on_start "Direct link to this Featureset") | Off | Shows the *Order Ticket* when the chart opens. |
| `show_symbol_logo_in_account_manager` [#](#show_symbol_logo_in_account_manager "Direct link to this Featureset") | On | Displays the symbol's logo within the [Account Manager](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/account-manager). Note that you must also enable [`show_symbol_logos`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_symbol_logos). |
| `show_symbol_logo_in_close_position_dialog` [#](#show_symbol_logo_in_close_position_dialog "Direct link to this Featureset") | On | Shows the symbol's logo in the *Close position* dialog. Note that you must also enable [`show_symbol_logos`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_symbol_logos). |
| `show_symbol_logo_in_cancel_order_dialog` [#](#show_symbol_logo_in_cancel_order_dialog "Direct link to this Featureset") | On | Shows the symbol's logo in the *Cancel order* dialog. Note that you must also enable [`show_symbol_logos`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets#show_symbol_logos). |
| `show_trading_notifications_history` [#](#show_trading_notifications_history "Direct link to this Featureset") | On | Enables the *Notifications log* tab on the bottom panel. |
| `support_multicharts` [#](#support_multicharts "Direct link to this Featureset") | On | Enables context menu actions (for example *Sync in layout* for drawings) related to [multiple-chart layout](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#multiple-chart-layout).   Note that disabling this featureset does not remove the *Select Layout* button on the top toolbar. To hide this button, disable the [`header_layouttoggle`](https://www.tradingview.com/charting-library-docs/latest/customization/Featuresets/#header_layouttoggle) featureset. |
| `trading_account_manager` [#](#trading_account_manager "Direct link to this Featureset") | On | Shows the [Account Manager](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/account-manager). |
| `trading_notifications` [#](#trading_notifications "Direct link to this Featureset") | On | Shows trading notifications on the chart. |
| `watchlist_context_menu` [#](#watchlist_context_menu "Direct link to this Featureset") | On |  |
| `watchlist_import_export` [#](#watchlist_import_export "Direct link to this Featureset") | On | Enables [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List) export and import. |
| `watchlist_sections` [#](#watchlist_sections "Direct link to this Featureset") | On | Display UI (buttons and context menu options) for creating sections within the watchlist. |
| `prefer_quote_short_name` [#](#prefer_quote_short_name "Direct link to this Featureset") | On | Displays the [short\_name](https://www.tradingview.com/charting-library-docs/latest/api/interfaces/Charting_Library.DatafeedQuoteValues/#short_name) value as a symbol name in the [Watchlist](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/Watch-List) and [Details](https://www.tradingview.com/charting-library-docs/latest/trading_terminal/#details). |
| `watchlist_cross_tab_sync` [#](#watchlist_cross_tab_sync "Direct link to this Featureset") | On | Enables the cross-tab synchronization for watchlists.   Available from version 29.2.0. |