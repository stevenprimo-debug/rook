# Research-then-Write — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |
| `{NOTION_DATABASE_ID}` | Target Notion database where articles publish as Drafts |
| `{EXA_API_KEY}` | Customer's Exa MCP credentials |
| `{NOTION_API_KEY}` | Customer's Notion MCP credentials |

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{DEFAULT_TARGET_LENGTH}` | 1500 words | Yes — per article via payload |
| `{DEFAULT_AUDIENCE}` | "general professional" | Yes — per article via payload |
| `{DEFAULT_STYLE_NOTES}` | (empty — uses CD voice spine baseline) | Strong recommend: dispatch CD first to lock voice |

## Notion pre-flight (customer sets up before deploy)

| Setup item | Where |
|---|---|
| Target database with `Status` property (text/select) | Notion |
| Default Status value `Draft` exists in select options | Notion |
| `Generated` date property | Notion |
| Database shared with Notion MCP integration | Notion settings |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + auto-derive `{CUSTOMER_SHORT_NAME}`
2. "Notion database ID where articles publish?" → `{NOTION_DATABASE_ID}`
3. "Default target length — 1500 words, or customize?" → `{DEFAULT_TARGET_LENGTH}`
4. "Default audience profile — 'general professional' or customize?" → `{DEFAULT_AUDIENCE}`
5. "Has CREATIVE DIRECTOR been dispatched to lock brand voice? (Strong recommend.)" → if N, offer to spawn CD subagent first
6. "MCP credentials configured for Exa + Notion?" → confirm

## Upstream dispatch chain (mandatory per `dispatch_chains.MARKETING`)

CREATIVE DIRECTOR → MARKETING → content-strategist → this AMA.

- CREATIVE DIRECTOR briefs voice, narrative arc, "what NOT to make it look like"
- MARKETING validates positioning + funnel logic + hero copy patterns
- content-strategist invokes this AMA with the brief embedded as `{DEFAULT_STYLE_NOTES}`

For autonomous-only deployments (customer doesn't need brand-voice oversight),
skip the chain — but expect off-voice output.
