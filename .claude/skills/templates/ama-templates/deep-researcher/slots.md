# Deep Researcher — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name (appears in AMA name) |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{MIN_SUB_QUESTIONS}` | 3 (system prompt says "3-5") | Yes — customize |
| `{MAX_SUB_QUESTIONS}` | 5 | Yes |
| `{PRIMARY_SOURCE_PREFERENCE_ORDER}` | "primary sources > official docs > peer-reviewed > blogs > aggregators" | Customer can reorder by domain |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + auto-derive `{CUSTOMER_SHORT_NAME}`
2. "Any domain-specific source preferences? (e.g., for medical: prefer NIH/PubMed; for legal: prefer Westlaw)" → optional

## No MCP servers required

Uses built-in web search via `agent_toolset_20260401`. Customer doesn't need
to provision Exa, Apollo, or any external MCP for this AMA.
