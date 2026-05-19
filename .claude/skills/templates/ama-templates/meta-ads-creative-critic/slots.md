# Meta Ads Creative Critic — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name (appears in AMA name) |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |
| `{META_ADS_MCP_CREDS}` | Customer's Meta Ads Business Manager access via meta-ads MCP |

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{DEFAULT_KPI}` | ROAS | Yes — CTR, CPC, hook-rate, thumbstop, etc. |
| `{DATE_RANGE_DEFAULT}` | last 90 days | Yes — customize per analysis |
| `{WINNER_PERCENTILE}` | top 20% | Yes — adjust to top 10% or top 30% |
| `{UNDERPERFORMER_PERCENTILE}` | bottom 20% | Yes |
| `{VARIANTS_PER_WINNER}` | 3-5 | Yes — fewer for tight budgets, more for testing-heavy accounts |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + auto-derive `{CUSTOMER_SHORT_NAME}`
2. "Default KPI for ranking — ROAS (recommended), CTR, or other?" → `{DEFAULT_KPI}`
3. "Date range default — accept 90 days or customize?" → `{DATE_RANGE_DEFAULT}`
4. "Has CREATIVE DIRECTOR been dispatched to lock brand voice for variant briefs? (Recommended for new customer.)" → if N, offer to spawn CD subagent first

## Upstream dispatch chain (mandatory if voice/brand matters)

Per `dispatch_chains.DESIGN`: CREATIVE DIRECTOR → MARKETING → this AMA.
- CREATIVE DIRECTOR briefs voice / narrative / forbidden vocabulary additions
- MARKETING validates positioning + funnel alignment
- This AMA executes the analytical work

For ad-hoc analysis (no brand voice consideration), skip the chain and
deploy directly.
