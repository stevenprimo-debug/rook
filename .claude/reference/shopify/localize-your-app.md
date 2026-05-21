---
title: Localize your app
source: https://shopify.dev/docs/apps/build/localize-your-app
author: []
published: []
created: 2026-05-11
description: Learn how to start internationalizing your app by externalizing, formatting, and translating strings.
tags: [clippings]
dept_secondary: [PERSONAL, MARKETING]
---

Shopify helps merchants expand their business to a global audience, sell to multiple countries, and scale internationally. This means that many merchants need to sell in multiple languages and currencies.

This guide explains how internationalization works, and provides key terms and example use cases for internationalization.

You'll also learn how to begin internationalizing your app by externalizing, formatting, and translating strings.

---

## Anchor to Why internationalize your app?Why internationalize your app?

### Anchor to Market opportunityMarket opportunity

Shopify’s priority European markets are growing rapidly—at nearly 3x the rate of the US. Yet only 5–7% of all public apps are available in these priority markets. Merchants typically experience Shopify as a combination of Shopify itself and apps: 82% of active merchants have at least one app installed, and virtually all merchants with sales use apps. This gap between international merchant adoption and localized app availability represents a significant opportunity for developers who localize their apps.

Additionally, different markets have unique needs, presenting specific opportunities for app developers:

European markets:

- **Payment solutions**: Cash on delivery is especially important in Spain and Italy, where trust concerns make this payment method essential.
- **Compliance**: Features related to invoice formatting, tax reporting, and product reviews are highly sought-after due to complex regional regulations.
- **Ad measurement**: European merchants invest more in advertising tools and require improved measurement solutions to address GDPR-related challenges.

Japan:

- **Messaging integrations**: LINE messaging support is critical for Japanese merchants, who use it for marketing and customer support.
- **Loyalty programs**: Reward systems are culturally important and expected by Japanese customers.
- **Page customization**: Japanese merchants show higher demand for store customization tools to make their storefronts stand out.

Cross-market:

- **Shipping integrations**: Merchants in France, Italy, and Japan require solutions that support key local shipping carriers.
- Features developed for one international market often apply to others, enabling you to scale your solution across multiple regions.

### Anchor to Business impactBusiness impact

Internationalization can deliver measurable benefits for your app:

- **Reduced churn rates**: Localized apps have demonstrated lower user churn in non-English markets.
- **Increased visibility**: Well-localized apps are more likely to be featured prominently in the Shopify App Store and admin.
- **Expanded user base**: Localization helps you reach merchants who prefer or require apps in their native language.
- **Competitive advantage**: Localizing your app lets you stand out in markets where merchants have limited localized options.

### Anchor to Merchant experienceMerchant experience

Without localized apps, international merchants face several challenges:

- **Inaccurate translations**: Merchants must rely on browser-based translation tools, which are often inaccurate and disruptive.
- **Dependence on third-party solutions**: They may need external tools or specialized support to understand and use English-only apps.
- **Disjointed workflows**: Switching between the localized Shopify admin and non-localized apps creates a fragmented user experience.
- **App abandonment**: Merchants may stop using apps entirely if they're not available in their native language.

---

## Anchor to Internationalize your appInternationalize your app

### Anchor to How it worksHow it works

Internationalization helps merchants expand their business to a global audience by creating shopping experiences in local languages and currencies.

Tip

You can speed up internationalizing new and existing apps by using [i18n-ally](https://marketplace.visualstudio.com/items?itemName=Lokalise.i18n-ally), an open source Visual Studio Code extension that makes it easier to externalize strings, view and navigate to translation strings from code, and perform machine translation.

The following diagram illustrates the different stages in the process of internationalizing your app:

![Stages in the process of internationalizing your app](https://cdn.shopify.com/shopifycloud/shopify-dev/production/assets/assets/images/apps/internationalization/stages-B-brMiH_.png)

Stages in the process of internationalizing your app

#### Anchor to DefinitionsDefinitions

The following definitions provide a starting point for understanding key terms associated with internationalizing your app:

| Term | Definition |
| --- | --- |
| Internationalization | Building your app and interface so it can be used in different locales. This includes creating flexible interfaces that allow for text expansion and changes to word order. |
| Localization | Adapting your app and interface for different locales to make them a good cultural fit. This includes adapting features, changing visuals, and translating text. |
| Translation | Converting text from one language to another. Not to be confused with localization, translation is just one part of localizing a product. |

#### Anchor to Use casesUse cases

- The app user is going global as their addressable market is growing, and their buyers live in different parts of the world.
- The app user has staff that use the Shopify admin in multiple languages.
- You want to promote your app in the Shopify community. Shopify promotes localized apps in the App Store over apps that aren’t localized.
- You want to sell your app cross-border in other markets.

### Anchor to What you'll learnWhat you'll learn

In this guide, you'll learn how to do the following tasks:

- Externalize strings so that they're available for localization
- Format strings, including names and lists to support regional variation
- Translate strings and test your UI

### Anchor to RequirementsRequirements

- You're a [user with app development permissions](https://shopify.dev/docs/apps/build/dev-dashboard/user-permissions) and have created [a dev store](https://shopify.dev/docs/apps/build/dev-dashboard/development-stores).
- You understand the different ways of [distributing your app](https://shopify.dev/docs/apps/launch/distribution).

### Anchor to Step 1: Externalize stringsStep 1: Externalize strings

Translation is foundational to localization. The first step of translation involves externalizing any hard-coded strings from your app into translation files.

When your app renders its UI, it looks up the corresponding strings from the translation file that's associated with the requested locale.

#### Anchor to Source filesSource files

The following example shows a hard-coded `greeting` string from an app:

function greeting(casual\_name) {

return \`Hello ${casual\_name}\`;

}

The following example shows how to externalize the hard-coded `greeting` string in a translation file:

{

"greeting": "Hello {casual\_name}"

}

function greeting(casual\_name) {

return i18n.translate("greeting", { casual\_name: casual\_name });

}

Tip

Even if you don't intend to initially translate your app, you should still externalize strings in your app during initial development. It can be difficult to externalize strings in an existing app that wasn't originally structured with externalized strings.

#### Anchor to GraphicsGraphics

Text within graphics and images should also be externalized for translation.

Instead of having flat graphics that include text, externalize the text and overlay it on the graphic. Alternatively, you can generate flat graphics for each locale, and switch between them based on the requested locale.

### Anchor to Step 2: Get access to the user's localeStep 2: Get access to the user's locale

Depending on the audience, the lookup of a translation string uses the preferred locale of either an app user or a buyer.

The mechanism for receiving the locale depends on the type of app or app extension being developed.

For example, apps rendered in the Shopify admin receive the app user's chosen locale in the `locale` request parameter in Shopify's `GET` requests to the app.

Refer to the documentation for your [type of app extension](https://shopify.dev/docs/apps/build/app-extensions/list-of-app-extensions) for more information.

### Anchor to Step 3: Format stringsStep 3: Format strings

Beyond language translation, parts of your app's strings should adapt dynamically to different locales.

For example, dates and times, names, numbers, prices, and lists are elements that should be formatted differently based not on language, but on the user's region or preferences.

Remove these elements from your app's strings, use a localization library to generate the formatted versions, and inject the formatted versions dynamically using string interpolation. The following sections describe how to format the following parts of strings:

- [Dates and times](#format-dates-and-times)
- [Numbers](#format-numbers)
- [Prices](#format-prices)
- [Lists](#format-lists)
- [Names](#format-names)

#### Anchor to Format dates and timesFormat dates and times

The format of dates and times varies by region, not by language. As a result, dates and times, such as the following examples, don't belong in translation strings:

| Locale | Formatted datetime |
| --- | --- |
| `en-US` | `12/19/2020, 10:23 PM` |
| `en-GB` | `19/12/2020, 22:23` |
| `en-CA` | `2020-12-19, 10:23 p.m.` |

Use an API or library to format dates and times. For example, you can use [`Intl.DateTimeFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) and inject the formatted dates and times into your translations using string interpolation:

{

"last\_sale\_day": "All orders must be placed by 2022-10-30"

}

{

"last\_sale\_day": "All orders must be placed by {date}" // 2022-10-30, 10/30/2022, 30/10/2022

}

#### Anchor to Format numbersFormat numbers

The format of numbers varies by region, not by language. As a result, numbers, such as the following examples, don't belong in translation strings:

| Locale | Formatted number |
| --- | --- |
| `en-US` | `123,000` |
| `en-NL` | `123.000` |
| `en-IN` | `1,23,000` |

Use an API or library to format numbers. For example, you can use [`Intl.NumberFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat) and inject the formatted numbers into your translations using string interpolation:

{

"congrats": "Congratulations on 100,000 orders"

}

{

"congrats": "Congratulations on {formatted\_number} orders" // 100,000, 100.000, 1,00,000

}

Note

If the number is a variable, then you should also make use of pluralization features to make sure that the correct grammar can be used for each number.

#### Anchor to Format pricesFormat prices

The format of prices varies by currency and region, not by language. As a result, prices, such as the following examples, don't belong in translation strings:

| Locale | Currency | Formatted price |
| --- | --- | --- |
| `en-US` | `USD` | `$123,456.00` |
| `en-CH` | `USD` | `US$ 123’456.00` |
| `en-IN` | `USD` | `$1,23,456.00` |

Use an API or library to format prices. For example, you can use [`Intl.NumberFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat) and inject the formatted prices into your translations using string interpolation:

{

"order\_total": "Your total order is ${price}"

}

{

"order\_total": "Your total order is {formatted\_price}", // $15.50, USD 15.5, 15,50 $US

}

#### Anchor to Format listsFormat lists

The way that items are combined into lists varies by region, not by language. As a result, lists, such as the following examples, don't belong in translation strings:

| Locale | Formatted list |
| --- | --- |
| `en-US` | `User, Product, or Variant` |
| `en-GB` | `User, Product or Variant` |

Use an API or library to format lists of items. For example, you can use [`Intl.ListFormat`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/ListFormat) and inject the formatted lists into your translations using string interpolation:

{

"prompt": "Please select one of: {nouns}",

"nouns": {

"user": "User",

"product": "Product",

"variant": "Variant",

...

}

}

function selection\_prompt() {

nouns = fetch\_nouns().map(function (noun) {

return i18n.translate(\`nouns.${noun}\`);

});

return i18n.translate("prompt", {

nouns: new Intl.ListFormat(locale, {

style: "long",

type: "disjunction",

}).format(nouns),

});

}

#### Anchor to Format namesFormat names

The way that you address a person varies by context and region.

For example, for a person with the given name "Quinn" and surname "Ishida" might be addressed in the following ways:

| Locale | Formatted full name | Formatted casual name |
| --- | --- | --- |
| `en-US` | `Quinn Ishida` | `Quinn` |
| `en-JP` | `IshidaQuinn-sama` | `Ishida-sama` |

Don't encode the name formatting conventions of North American English. Instead, use an API or library to format a person's name based on the context, and inject the formatted name into your translations using string interpolation:

{

"greeting": "Hello {first\_name} {last\_name}",

"casual\_greeting": "Hey {first\_name}!"

}

{

"greeting": "Hello {full\_name}", // Quinn Ishida, IshidaQuinn-sama

"casual\_greeting": "Hey {casual\_name}!" // Quinn, Ishida-sama

}

### Anchor to Example promptExample prompt

LLMs can significantly streamline internationalization efforts by automatically handling many of the steps described above. Here's a sample prompt to help you get started:

You are an expert software developer, specializing in software localization, specifically for Shopify Apps. You possess a deep understanding of localization tooling and how to build software to work across languages and locales. I have a Shopify app that needs to be localized. It currently has no localization middleware installed and all UIs have hardcoded english strings.

Your primary goal is to localize this app so that it can work seamlessly for users in different languages and regions. Approach this translation as an expert software developer would, following these steps:

1\. Install the i18n-next localization middleware

2\. Extract hardcoded strings from all UIs to public/locales/en.json. Don't translate them into any other languages yet. Give each hardcoded string an descriptive key.

3\. Localize the display of numbers. For example, 1,000 in English is written as 1.000 in Spanish. Extract them from UIs and apply the intlNumber method for that.

4\. Localize any displays of currency using the i18n-next library.

5\. Localize dates using the i18n-next helpers, so we get the correct dates in every language. For example, Spanish uses DD/MM/YYY and US English uses MM/DD/YYY.

6\. Configure this app to use the value of the 'locale' request parameter as the current user's preferred locale.

As you make changes, log actions to a file called 'i18nupdates.md' that includes one row for each file updated with internationalized strings. Include the folder, filename and the count of strings internationalized.

### Anchor to Step 4: Translate stringsStep 4: Translate strings

Translating strings involves accounting for text expansion in different languages, and providing your source strings to someone that can translate the content.

#### Anchor to Step 4.1: Use pseudolocalization (Optional)Step 4.1: Use pseudolocalization (Optional)

When interfaces are localized, the content often expands in length. In most languages, text is up to 50% longer on average than English. Some non-Latin languages, such as Japanese, take up more vertical space. For character-based languages, text wrapping and line breaking can’t always rely on spaces to separate words. Your interface needs to be flexible enough to accommodate language formatting and text expansion without changing its context of use.

The [Polaris i18n documentation](https://polaris.shopify.com/foundations/internationalization) has more information about, and examples of, text expansion issues.

You can use pseudolocalization tools ([example](https://github.com/Shopify/pseudolocalization)) to simulate text expansion before translation is completed. This enables you to test your app's UI for common text expansion issues. For example, you might want to test for overflowing strings or word wrapping.

#### Anchor to Step 4.2: Choose the languages to translate intoStep 4.2: Choose the languages to translate into

The Shopify admin can be used in any of the [supported languages](https://help.shopify.com/en/manual/your-account/languages).

Shopify also translates some buyer-facing strings (first-party themes, checkout, and system messages) into additional languages (for example, refer to the [language list in the Dawn theme](https://github.com/Shopify/dawn/blob/0ea3e2780876ff81d599bffac5f6c790dac567b0/translation.yml#LL2)).

When deciding on which languages to translate into, consider starting with those most common in the regions or markets that your app supports.

#### Anchor to Step 4.3: Translate contentStep 4.3: Translate content

Translating content involves providing your source strings to someone that can translate the content into each language.

Note

Because you'll need to make changes to translations as you develop new features, you should expect the relationship with the provider of your translations to be a continuous partnership.

There are several options for getting translations. The options vary on cost, turn-around time, and quality.

##### Anchor to Third party translation serviceThird party translation service

The highest quality, but often most costly, option is to engage a third party translation service to manage the work of providing translations for your app.

Translation providers manage the relationships with the translators so that you can have confidence in the quality and turnaround time of the translations.

Shopify recommends using one of the following translation providers:

- [Blend](https://www.getblend.com/)
- [Crowdin](https://crowdin.com/)
- [TranslateCI](https://translateci.com/)

##### Anchor to Machine translationMachine translation

Machine translation, such as [Google Translate](https://translate.google.com/), is artificial intelligence software that can generate translations on-demand.

Machine translation can be quick and cost-effective, but the quality of the translations can vary because strings are often translated without context about your app or business.

##### Anchor to Crowdsourced translationCrowdsourced translation

If your app already has a large community, then sometimes community members are willing to contribute translations.

This method relies on managing and engaging your app's community in an ongoing manner, which can be time-consuming. Depending on the diversity of your community, it might be difficult to find enough people with fluency in the languages that you're translating your content into.

##### Anchor to Do it yourselfDo it yourself

If you or an acquaintance knows another language, then translations for that language can be manually provided.

- Promote your app to a global audience by [writing](https://shopify.dev/docs/apps/launch/app-requirements-checklist#writing-a-shopify-app-store-listing) and [translating](https://shopify.dev/docs/apps/launch/app-requirements-checklist#translate-your-app-listing) an app listing.

---

---
