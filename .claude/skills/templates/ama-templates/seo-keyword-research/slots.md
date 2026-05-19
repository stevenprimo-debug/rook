# SEO Keyword Research — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name (appears in AMA name) |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |
| `{EXA_API_KEY}` | Customer's Exa API key (set via MCP credentials, not embedded) |

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{MIN_SEARCHES_PER_SEED}` | 3 (system prompt says "aim for at least 3–5") | Yes — customize |
| `{INTENT_CATEGORIES}` | informational / transactional / navigational / commercial-investigation | Yes — add domain-specific |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + auto-derive `{CUSTOMER_SHORT_NAME}`
2. "Do you have Exa MCP access? (https://exa.ai/api)" → confirm credentials are set
3. "Any custom intent categories to add beyond the 4 defaults?" → optional
