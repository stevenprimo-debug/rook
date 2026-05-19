# Shopify Platform — Progression Path

## Who This Is For

The operator building on the Shopify platform — themes, apps, custom merchant features, agentic commerce flows, ecommerce automation, or a DTC store of their own. Founders, developers, agency operators, and merchants who refuse to delegate the platform itself to a black-box partner.

By the end of this path you should be able to:
- Navigate the admin fluently.
- Customize a theme without breaking it.
- Build a public or custom app against the Admin API and the Storefront API.
- Follow Polaris design conventions.
- Ship a Shopify Function (Rust or AssemblyScript).
- Engage the agentic commerce frontier with confidence.

## Stage 1: Foundations (weeks 1-3)

**Goal:** Master the Shopify admin. Customize a theme via Online Store 2.0. Understand Liquid.

**Read / Watch:**
- **Shopify Academy** (academy.shopify.com) — free; the merchant-side training. The "Sell Online with Shopify" and "Theme Customization" tracks first.
- **Shopify Help Center** (help.shopify.com) — the canonical reference for every admin feature; bookmark; read top-to-bottom over the first month.
- **Shopify.dev** (shopify.dev) — the developer documentation hub; the foundational reads are the Liquid reference, the Online Store 2.0 architecture overview, and the theme architecture guide.
- *The Definitive Guide to Shopify Themes* — Shopify's official documentation; free, comprehensive.
- **Tobi Lütke interviews** (Lenny's Podcast, How I Built This, The Tim Ferriss Show) — for the founder's frame on why Shopify is built the way it is.
- **Shopify Partners blog** (shopify.com/partners/blog) — daily/weekly platform updates.

**Practice:**
- Spin up a Shopify development store (free via the Shopify Partners program). Walk every admin page: products, collections, customers, orders, discounts, apps, marketing, online store. Note what's there and what's not.
- Pick a free theme (Dawn is the reference) and customize it through the theme editor: sections, blocks, settings, theme.liquid. The exercise teaches Online Store 2.0 architecture.
- Read 500 lines of theme Liquid in Dawn or a similar reference theme. Annotate every block: what does it render, what data does it bind, where would you change it.
- Build a metafield-driven feature: add a custom metafield to products, surface it in the theme. The exercise teaches the modern data-model side of Shopify.

**Skill check:**
- You can complete a merchant-flow end-to-end from a cold dev store: add a product, configure checkout, install a payment provider in test mode, place a test order, fulfill it.
- Your theme customization survives without breaking when you change a setting.
- You can read Liquid fluently and trace where any rendered piece of content comes from in the theme.

## Stage 2: Applied Practice (weeks 4-10)

**Goal:** Build a custom app. Use Admin API and Storefront API. Apply Polaris design conventions.

**Read / Watch:**
- **Shopify.dev's "Build an App" tutorial** — the canonical first-app walkthrough; use the Shopify CLI and the Remix template.
- **Shopify Admin GraphQL API documentation** (shopify.dev/docs/api/admin-graphql) — the modern API surface; REST is deprecated for most new work.
- **Shopify Storefront API documentation** (shopify.dev/docs/api/storefront) — for headless and custom-storefront work.
- **Polaris design system** (polaris.shopify.com) — the design language for embedded apps; free; mandatory if you're shipping to the App Store.
- **App Bridge documentation** (shopify.dev/docs/api/app-bridge) — the embedded-app communication layer.
- *Building Shopify Apps* — Tony Foliaco (independent Udemy course; pair with the official docs).
- **The Liquid Weekly newsletter** (liquidweekly.com) — Karl Meisterheim; weekly platform pulse.
- **The Unofficial Shopify Podcast** — Kurt Elster; merchant-and-app-developer interviews.
- **Caroline Schnapp's Liquid resources** — the most-cited theme-developer reference.

**Practice:**
- Build one custom app: connect to a dev store via OAuth, use the Admin GraphQL API to read products, write one mutation (e.g., update inventory levels), render an embedded admin page using Polaris components. Deploy.
- Build one Storefront API integration: a headless React or Next.js page that pulls products and renders a custom collection page. Add Shopify checkout via the Storefront Cart API.
- Apply Polaris fluently: use Cards, Pages, Layouts, FormLayout, Banners, IndexTable. Build one full app-admin page that looks indistinguishable from a native Shopify page.
- Run a webhook-driven automation: subscribe to `orders/create`, process the payload, trigger a side effect (Slack notification, custom email, downstream API call). The discipline of webhook reliability — retries, idempotency, signature verification — is the production gate.

**Skill check:**
- Your app passes the App Store review checklist (or the equivalent internal checklist if it's for a single merchant).
- Your Polaris pages look native.
- Your webhook processor handles retries and signature verification correctly.
- You can build an OAuth flow without copy-pasting.

## Stage 3: Advanced Mastery (months 3-9)

**Goal:** Ship a production app at scale. Master the modern platform extensions. Engage with agentic commerce.

**Read / Watch:**
- **Shopify Functions** (shopify.dev/docs/api/functions) — the modern back-end-extension surface that replaces Shopify Scripts. Built in Rust or AssemblyScript. The future of checkout extensibility.
- **Shopify Hydrogen and Oxygen** (hydrogen.shopify.dev) — the headless-storefront framework and the edge-hosting platform; the modern alternative to building on Liquid for high-traffic stores.
- **Checkout Extensibility** documentation — the post-Checkout-Liquid extension model; the UI extensions framework.
- **Shop App and Shop Pay** developer documentation — for the Shop ecosystem integration.
- **Shop AI / Shopify Magic / agentic commerce** announcements and developer documentation — the agentic-commerce frontier as of 2025-2026. Shopify is investing heavily in agent-mediated checkout (AI agents that complete purchases on behalf of users); follow shopify.engineering and the partner program announcements.
- **Shopify Engineering blog** (shopify.engineering) — for the platform's technical-direction signals.
- **The Shopify Partners' Build a Business / Build a Bigger Business** materials and case studies.
- *Headless Commerce* — various authors; the high-level architecture frame for headless DTC.
- **Tom Brown's Shopify Magic content** (Tom is one of the more concentrated voices on the agentic-commerce frontier).
- **Shopify Unite recorded sessions** (annual partner conference; recordings free) — the deepest platform-direction signal of the year.

**Practice:**
- Ship one app to the Shopify App Store: production-grade, billing-integrated (recurring application charges via the BillingAPI), Polaris-native, App Bridge-compliant, properly localized, accessibility-audited. Pass the review.
- Build one Shopify Function: a discount Function or a delivery customization Function in Rust. Deploy via the CLI. The exercise teaches the modern back-end-extension model.
- Build one Hydrogen storefront for a real (or demo) merchant. Deploy on Oxygen. Measure Core Web Vitals against a Liquid theme baseline. The headless tradeoffs are the lesson.
- Develop an agentic-commerce experiment: integrate one AI-agent-mediated flow (cart-recovery agent, product-discovery agent, support agent) into a Shopify store using the Storefront API. Measure the conversion delta.
- Run a quarterly platform-direction review: read Shopify's last-quarter platform changelog, the engineering blog, the Unite announcements. Identify the three changes that affect your build. Update the build.

**Skill check:**
- Your App Store app is generating recurring revenue.
- Your Hydrogen storefront measurably outperforms its Liquid baseline.
- You can articulate Shopify's agentic-commerce direction and the developer-surface implications.
- Your Shopify Function passed CLI validation and is shipping in production for a real merchant.

## Ongoing Development

**Stay current:**
- **Shopify.dev changelog** — weekly platform updates.
- **Shopify Partners blog** — partner-side updates.
- **Shopify Engineering blog** — technical-direction signal.
- **The Liquid Weekly newsletter** — Karl Meisterheim; weekly.
- **The Unofficial Shopify Podcast** — Kurt Elster; weekly.
- **Shopify Editions** — biannual platform releases (summer, winter); each Editions is the canonical platform-direction artifact.
- **Shopify Unite** — annual partner conference; recordings free.
- **ShopTalk** and **DTC Newsletter** for the broader DTC industry pulse.
- **2pm.so newsletter** — Web Smith; DTC industry analysis.
- **DTC Index** — annual DTC industry benchmarks.
- **The DTC Podcast** — interview format with DTC operators.
- **Lenny's Newsletter (Shopify-relevant case studies)** — irregular but useful.
- **The Caroline Schnapp newsletter** — Liquid + theme + merchant-engineering depth.

**Communities to join:**
- **Shopify Partners Slack** — free; gated by Partners program enrollment; the most concentrated developer community.
- **Shopify Community Forums** (community.shopify.com) — variable but useful for merchant-side support questions.
- **r/shopify** — variable but useful for tool questions.
- **The Shopify Partner Town Hall** events — quarterly; in-person and virtual.
- A small peer-app-developer circle (3-5 partners) — monthly platform-change swap and code review.

**Quarterly cadence:**
- Pull your app's installation, churn, MRR data.
- Pull Shopify's last-quarter platform changes.
- Identify the changes that affect your app. Build the next quarter's roadmap from what shifted.
- Re-audit theme / app accessibility against WCAG 2.1; Shopify's App Store enforces; merchant trust depends on it.
- Score Core Web Vitals against the previous quarter; identify the worst-performing templates.
- Audit the merchant-feedback log: which features got requested most; which got complaints; build the next quarter from the pattern.

## Cross-References

- The the Stack agent that operates in this domain: `agents/shopify-agent/SKILL.md`
- Methodology framework(s) cited: `agents/shopify-agent/context/methodology/` (in development)
- Reference clippings: `agents/shopify-agent/context/references/` (vendored as Phase 1 expands)
- Related agents:
  - `agents/software-dev-team/SKILL.md` — the generic web-dev discipline underneath
  - `agents/product-manager/SKILL.md` — specs for merchant features
  - `agents/designer/SKILL.md` — theme and storefront design that respects Shopify's checkout patterns
  - `agents/marketing-director/SKILL.md` — the DTC-marketing layer your store serves
  - `agents/seo-specialist/SKILL.md` — Shopify-native technical SEO (product schema, collection pages, sitemaps)
  - `agents/copywriter/SKILL.md` — product description and PDP copy
- Three-principle gate (per SKILL.md): Commerce-Flow, Merchant-Margin, Customer-Trust held in productive tension.
- Department-level reference: `agents/shopify-agent/CLAUDE.md` — the dept-level Shopify operating rules and the first-customer engagement context.
- For a first paying Shopify engagement: a Cloudflare Workers email-agent is a battle-tested pattern; Shopify integrations layer on top via webhook + API patterns.
- For HubSpot ↔ Shopify bridge work: pair this learning path with the HubSpot agent loops in `agents/marketing-director/HUBSPOT/CLAUDE.md`.
- For agentic commerce: Shop AI / Magic / agent-mediated checkout is the frontier. Track shopify.engineering and partner-program announcements. Build for the protocol direction, not the current state.
- For Shopify Functions: discount Functions and delivery customization Functions are the highest-ROI surfaces; build in Rust for performance, AssemblyScript for accessibility.
- For Polaris fluency: use Cards, Pages, Layouts, FormLayout, Banners, IndexTable, Filters, ResourceList. The component library is the design system; respect it.
- For App Store revenue: the public app catalog is competitive; the custom-app pricing model offers higher ARPU but lower scale. Solo developers usually start with custom apps and graduate.
- For made-to-order merchant builds (the Stack-context "first-customer engagement"): the custom-app + bespoke-theme combination is the operating model; document every customization for handoff and renewal.
- For HubSpot ↔ Shopify automation: webhook from Shopify (`orders/create`, `customers/create`) → HubSpot deal / contact via the HubSpot API; the loop is well-trodden; reference patterns are public.
- For merchant-side coaching: every custom build includes operator-training on the admin surfaces the merchant will touch; the documentation lives in the store's notes.
- For deployment / hosting (headless): Oxygen is Shopify's hosting; Vercel and Netlify are common alternatives; the choice gates on latency, edge-cache integration, and CI/CD discipline.
- For Shopify-native security: PCI compliance is handled by Shopify; the app developer's surface is OAuth, scope minimization, secrets handling, and webhook signature verification.
