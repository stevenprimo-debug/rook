# Discord connector

**Status:** v1 stub — README + api-reference scaffolded; API-direct (Bot token).

## Consumers
- `inbox-manager`
- `marketing-director`
- `creative-director`

## Integration kind
API-direct (Bot token)

## Credentials
Bot token from Developer Portal. Env var DISCORD_BOT_TOKEN. Bot must be invited to the server with required intents.

## Reversibility class
Sending messages, role changes, kicks, bans are N. Reads (channel history, member list) are Y. WhatsApp-style voice-fidelity rule applies to drafts.

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/discord.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
