---
title: "2026-03 API reference"
source: "https://developers.hubspot.com/docs/api-reference/latest/overview"
author:
published:
created: 2026-05-22
description: "Reference documentation for HubSpot's date-versioned APIs, introduced with the 2026-03 release."
tags:
  - "clippings"
---
The 2026-03 APIs use a date-based versioning scheme that replaces the previous numeric version paths (e.g., `/crm/v3/`). All endpoints in this section follow the pattern:

```text
/api-name/2026-03/resource
```

For example, to retrieve all contacts:

```shellscript
GET /crm/objects/2026-03/contacts
```

All APIs, whether legacy, new, or beta, use the same root path as before: `https://api.hubapi.com/`.

This versioning model gives HubSpot the ability to ship updates on a predictable schedule. When a new date version is released, the previous version continues to work until its end-of-life date, giving you time to migrate. For new integrations, always use the latest date version. Learn more about this change on [HubSpot’s Developer Changelog](https://developers.hubspot.com/changelog/introducing-date-based-api-versioning).

Across the API reference section, use the versioning dropdown menu in the top bar to switch versions. If there’s an equivalent endpoint to the one you’re currently viewing, you’ll automatically be sent there. Otherwise, you’ll land on that version’s home page.

![Using the version selector in the developer docs to explore versions of HubSpot APIs](https://developers.hubspot.com/hubfs/Knowledge_Base_2023-24-25/developer/hs-docs-version-selector.png)

Using the version selector in the developer docs to explore versions of HubSpot APIs