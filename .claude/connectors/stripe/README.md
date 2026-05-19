# Stripe connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (Anthropic MCP also available).

## Consumers
- `finance-manager`
- `shopify-agent`

## Integration kind
API-direct (Anthropic MCP also available)

## Credentials
Restricted API key. Env var STRIPE_API_KEY (live) and STRIPE_API_KEY_TEST (sandbox).

## Reversibility class
Charge / refund / subscription mutations are N — explicit operator confirm. Reads are Y.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/stripe.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
