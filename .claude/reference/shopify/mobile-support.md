---
title: Mobile support
source: https://shopify.dev/docs/apps/build/mobile-support
author: []
published: []
created: 2026-05-11
description: Learn about best practices when you're developing a mobile app.
tags: [clippings]
---

When you develop a mobile-first solution, consider the following mobile app best practices.

---

## Anchor to Create responsive designsCreate responsive designs

- The app UI should adjust automatically to fit a smaller mobile screen to ensure a consistent experience on any device.
- Prioritize vertical scroll over horizontal scroll, and avoid using any horizontal scrolling elements if possible.

---

## Anchor to Ensure core features are availableEnsure core features are available

- The core functionality of the app or theme should be available using a mobile device.
- Apps should notify users when features are not available on mobile.

---

## Anchor to Provide seamless setupProvide seamless setup

- Apps that require theme setup should use [theme app extension](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions) [app blocks](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions/configuration#app-blocks-for-themes) and [app embed blocks](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions/configuration#app-embed-blocks) so that the user doesn’t need to manually make changes to their theme’s code.
- Configuration and onboarding should be easy to follow and primarily take place inside the app.
- Minimize the number of external web properties users are redirected to post installation.

---

---
