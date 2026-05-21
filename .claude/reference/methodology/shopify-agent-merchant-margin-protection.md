# Merchant Margin Protection

## What This Framework Is

Merchant margin protection is the discipline of structuring
ecommerce decisions to preserve and grow the merchant's gross
margin, recognizing that **revenue growth at the cost of margin
collapse is not growth — it is faster failure**. The framework
holds that many ecommerce optimization tactics (discounting,
free shipping, return guarantees, customer acquisition
spending) can be margin-positive or margin-negative depending
on execution — and that the discipline of running the margin
math is what separates merchants who scale sustainably from
merchants who scale into bankruptcy.

The framework operates on six margin levers:

1. **Pricing strategy** — where the product sits in the price-
   value matrix, and how price changes affect demand and
   margin.
2. **Discount discipline** — when discounts make margin sense
   (acquiring new customers, clearing inventory) vs. when they
   destroy margin (training customers to wait for sales).
3. **Shipping economics** — who pays for shipping, how it
   affects conversion, and how it affects margin.
4. **Return economics** — return rates, return costs, return-
   driven inventory recovery.
5. **Customer acquisition cost (CAC) discipline** — what merchants
   can sustainably pay to acquire customers given LTV.
6. **Bundling and upsell economics** — how product mix affects
   average order margin.

For Shopify work (first paying engagement, future client builds), the
framework operates on each merchant's specific margin profile —
custom products, made-to-order, services-attached — and
recognizes that merchants in different categories have
different margin physics.

## Why It Matters For This Agent

Shopify Agent's Merchant-Margin-Pole gates every recommendation
on whether the proposed change preserves or grows merchant
margin. The pole catches three specific failure modes:

1. **Discount-driven volume.** Discounting to drive conversion
   without margin math. Volume rises; margin falls; net profit
   may decline despite higher revenue.

2. **Free-shipping margin erosion.** Offering free shipping
   without absorbing the cost into product price or order
   minimums. Margin per order quietly disappears.

3. **CAC creep.** Customer acquisition costs rising over time
   without LTV rising correspondingly. Merchant is buying
   customers at a loss; the loss compounds.

For custom made-to-order work specifically (per locked
project facts), the margin physics differ from mass-produced
DTC: lead times, material costs, and labor costs all affect
margin per order. The framework protects against margin
erosion from generic ecommerce tactics applied to custom-product
economics.

## Core Concepts

### 1. The Gross Margin Math

Gross margin = (Revenue - COGS) / Revenue.

For each product:
- **Revenue** — selling price after any discounts.
- **COGS** — direct costs: materials, manufacturing labor, packaging,
  inbound freight, payment processing fees.
- **Gross margin %** — the lever everything else operates on.

Healthy DTC margins typically run 60-80% gross margin to support
the operational overhead and customer acquisition costs that
follow. Lower margins (40-50%) require massive volume to be
profitable; merchants in this zone are vulnerable to any cost
increase or CAC rise.

For made-to-order custom work, margin math is per-order:
- Material cost per order.
- Labor hours per order × hourly cost.
- Packaging and shipping inputs per order.
- Payment processing.
- Allocated overhead.

Each order's margin gets calculated; pricing is structured to
maintain target margin per order, not target revenue.

### 2. The Pricing Strategy

Pricing communicates value AND determines margin. Three pricing
approaches:

- **Cost-plus pricing**: Cost × markup multiple. Predictable
  margin but ignores willingness-to-pay.
- **Competitive pricing**: Match or beat competitors. Risks
  margin collapse in price wars.
- **Value-based pricing**: Set price based on value delivered
  to customer. Highest margin potential but requires
  understanding customer willingness-to-pay.

For made-to-order custom work, value-based pricing usually applies:
custom craft commands a premium over mass-produced equivalents
because the value delivered (specificity, craftsmanship,
exclusivity) is qualitatively different.

The discipline: pricing decisions are evaluated against margin
implications, not just competitive positioning.

### 3. The Discount Discipline

Discounts can be margin-positive or margin-negative depending on
context.

Margin-positive discount scenarios:
- **New customer acquisition** — first-purchase discount that
  pays back in LTV over multiple repeat purchases.
- **Inventory clearing** — discount on slow-moving SKU to free
  working capital for higher-margin SKUs.
- **Seasonal/promotional** — calendar-driven discount with
  clear time bounds.
- **Bundle promotion** — discount on bundle that increases
  average order value enough to net positive on margin.

Margin-negative discount scenarios:
- **Constant-discount training** — site permanently in discount
  mode; customers wait for sales; full-price purchases
  disappear.
- **Margin-eroding free shipping** — free shipping threshold
  set too low to recover shipping cost from margin.
- **Acquisition-only thinking** — discount to acquire customer
  without LTV evidence that the customer will repeat-purchase.

The discipline: every discount decision is evaluated against
both the immediate-margin impact and the long-term customer
behavior impact.

### 4. The Shipping Economics

Shipping is a frequent margin destroyer. Three approaches:

- **Customer pays full shipping**: highest margin retention but
  may suppress conversion.
- **Free shipping with margin absorption**: convert better but
  margin erodes per order.
- **Free shipping above order threshold**: balances conversion
  with average-order-value uplift.

The math: free shipping cost should be ≤ the AOV uplift it
produces. If free shipping above $50 produces orders averaging
$65 vs. previous $35 average, the shipping cost ($X) needs to
be less than the margin on the additional $30 of order value.

For custom orders (lower order volume, higher order
value), shipping cost is more easily absorbed in margin — but
the calculation still applies.

### 5. The Return Economics

Returns affect margin in multiple ways:

- **Direct cost**: return shipping, restocking labor, possibly
  product write-off.
- **Indirect cost**: customer service time, fraud risk on
  return abuse.
- **Indirect benefit**: liberal return policies increase conversion
  upstream.

For made-to-order custom work, returns are typically
non-refundable or restocking-fee-applied because the custom item
cannot be resold. The policy needs clear upfront communication
during the consideration stage.

For standard products, return rate × average return cost gets
factored into per-order margin calculations.

### 6. The CAC-LTV Ratio

Customer acquisition cost (CAC) is what the merchant pays to
acquire a customer. Lifetime value (LTV) is what the customer
generates in margin over their lifetime.

Sustainable ratio: LTV / CAC ≥ 3. Below this, the merchant is
acquiring customers faster than they pay back.

For custom work, LTV calculation:
- First-order margin.
- Probability of repeat purchase × repeat-order margin.
- Probability of referral × referred-customer LTV (with discount
  for indirect attribution).

CAC measurement: total acquisition spend / new customers
acquired in period. Includes paid ads, content marketing
allocated to acquisition, agency/freelance fees, software
costs allocated to acquisition.

If CAC exceeds 1/3 of LTV, acquisition needs to slow until
either CAC drops or LTV rises (through better product, better
post-purchase, or pricing optimization).

### 7. The Bundling and Upsell Economics

Bundles and upsells can be margin-positive levers:

- **Bundle discount that increases AOV more than the discount
  costs**: net margin gain.
- **Upsell to higher-margin variant**: net margin gain.
- **Cross-sell complementary product**: net margin gain if the
  complementary product has comparable margin.

The discipline: bundle/upsell decisions are evaluated on
incremental margin, not just AOV uplift.

## Common Applications

**Pricing review for new product launch:**
The agent calculates COGS for a new custom piece. Reviews target
margin (per merchant's target). Sets initial price. Surfaces
the value-based pricing alternative (where price reflects
delivered value, not cost plus markup) for the merchant's
decision.

**Discount analysis for promotional campaign:**
A holiday sale is proposed. The agent runs the margin math:
proposed discount × expected volume vs. baseline-no-discount
margin × baseline volume. Surfaces the net margin impact. If
the campaign is margin-negative, surfaces the trade-off (new
customer acquisition value, inventory clearing benefit) for
the merchant's decision.

**Free shipping threshold optimization:**
Current free-shipping threshold of $50 produces $X cost per
free-shipped order. Average order value at threshold is $65.
The agent models alternative thresholds: $75 produces higher
AOV ($85 avg) and lower free-shipping cost per order;
$30 produces lower AOV ($45 avg) but higher conversion.
Identifies the threshold that maximizes net margin per
visitor.

**CAC-LTV monitoring:**
The agent runs the monthly CAC-LTV calculation. Surfaces trend:
CAC rising or stable, LTV rising or stable, ratio rising or
falling. Trend analysis surfaces issues before they compound.

**Return-policy audit:**
The agent reviews the return policy against the product mix.
For custom work, surfaces return policy clarity (made-to-
order non-returnable, custom variations non-refundable) and
checks that the policy is visible during consideration stage,
not surprise at post-purchase.

**Per locked feedback: "Verify Project Status Before Speaking."**
Margin recommendations rest on actual current cost data. Stale
COGS data produces stale margin recommendations.

**Per locked memory: example-project facts.** Custom-fab-merchant margin
constraints (custom work economics, materials, labor) get
loaded before applying generic ecommerce margin frameworks.

## Anti-patterns (when this framework is misapplied)

**Revenue-only optimization.** Growing revenue without margin
discipline. Bigger top-line but smaller bottom-line. The
framework requires margin as the primary lens.

**Discount addiction.** Site permanently in discount mode.
Customers train to wait for sales; full-price purchases collapse;
margin compounds downward.

**Free shipping math skipped.** Free shipping without absorbing
the cost into product price or threshold AOV uplift. Quiet
margin erosion.

**Per locked feedback: "Numbers-Honest-Pole."** Margin
analysis uses verified actuals, not optimistic projections.
Honest math is the discipline.

**CAC creep accepted.** CAC rising without LTV rising
correspondingly. The ratio breakdown produces a slow-motion
failure that compounds over quarters.

**Acquisition cost ignored on first purchase.** Treating
first-order margin as the relevant number when acquisition spend
came from broader budget. The CAC needs to be attributed to
specific acquired customers, not absorbed into "marketing
overhead."

**Per locked feedback: "Match Execution Mode."** Margin
protection doesn't get punted when execution-mode is fast.
The math runs anyway, perhaps faster.

**Bundle/upsell margin-blind.** Adding bundles or upsells
because they "boost AOV" without checking incremental margin.
Some bundles cannibalize higher-margin single-product
purchases.

**Return policy permissiveness for custom work.** Applying
mass-DTC return policies to made-to-order custom work. The
inventory cannot be recovered; the return cost is total
write-off. custom-fab economics require custom-fab
return policy.

**Per locked feedback: "Filter — Personal-Tool Patterns vs
Agent-Team Patterns."** Margin data must be team-readable.
The merchant's CFO, the agent, and the operator all need to access
margin state — not just live in one head.

## Cross-references

- Agent skill: `agents/shopify-agent/SKILL.md`
- Bench: `agents/shopify-agent/personality/_bench.md` (Merchant-Margin-Pole)
- Frameworks index: `agents/shopify-agent/personality/frameworks_index.md`
- Companion methodology: `.claude/reference/methodology/shopify-agent-commerce-flow-fundamentals.md`
- Companion methodology: `.claude/reference/methodology/shopify-agent-customer-trust-pattern.md`
- Related agent: `.claude/reference/methodology/finance-manager-accounting-framework.md`
- Memory: `agents/<agent>/memory/client_project_facts.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `.claude/memory/feedback_match_execution_mode.md`
- Memory: `.claude/memory/feedback_filter_personal_vs_agent_team_patterns.md`
- Dept: `agents/shopify-agent/CLAUDE.md`
