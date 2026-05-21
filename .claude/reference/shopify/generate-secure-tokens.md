---
title: Generate secure tokens
source: https://shopify.dev/docs/apps/build/security/generate-secure-tokens
author: []
published: []
created: 2026-05-11
description: You must ensure that any tokens that your app generates are secure and protected before you submit your app to be reviewed by Shopify.
tags: [clippings]
---

If your app relies on tokens to authenticate users, then you must ensure the token is randomly generated with 128 bits of [entropy](https://en.wikipedia.org/wiki/Entropy) to ensure the security of Shopify merchant data. In some cases, we allow 64 bits where token length is a concern.

If the token will be publicly accessible (for example, included as a parameter in a URL), then you must ensure that the token has an expiration date of no longer than seven days, and you must prevent the token from being leaked to, or indexed, by third parties.

If we detect the use of tokens in your app without sufficient entropy, or tokens that don't expire or can be leaked or indexed by third parties, then your app will be rejected. You'll be required to fix the identified problem before submitting your app for another review.

The following links can be used to generate secure random tokens for several popular programming languages:

- [Python](https://docs.python.org/3/library/secrets.html)
- [Ruby](https://ruby-doc.org/stdlib-2.5.1/libdoc/securerandom/rdoc/SecureRandom.html)
- [PHP](https://www.php.net/manual/en/function.random-bytes.php)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues)
- [Go](https://pkg.go.dev/crypto/rand)
- [Java](https://docs.oracle.com/javase/8/docs/api/java/security/SecureRandom.html)
	When a token is used to authenticate access to private information, you must ensure that the private information can't be indexed by search engines. Google's guide [Block Search indexing with 'noindex'](https://developers.google.com/search/docs/advanced/crawling/block-indexing) explains how to properly configure a HTML meta tag to prevent search indexing. Additionally, any app URL which accepts a token must ensure it includes a [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) header in the HTTP response with a value of *origin-when-cross-origin* or, preferably, *no-referrer*.

---

---
