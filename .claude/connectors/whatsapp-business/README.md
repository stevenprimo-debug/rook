# WhatsApp Business connector

**Status:** stub — v1.0 ships scaffolding; auth wire-up is per-operator setup.

## Consumers
- `inbox-manager` (read messages, draft replies; voice-preserving)
- `account-manager` (read inbound from accounts that message via WhatsApp)

## Credentials
- Env var: `WHATSAPP_BUSINESS_ACCESS_TOKEN`
- Env var: `WHATSAPP_BUSINESS_PHONE_NUMBER_ID`
- Env var: `WHATSAPP_BUSINESS_VERIFY_TOKEN` (for webhook verification)
- Setup: Meta Business Suite → WhatsApp Business Platform → app + phone number
  registration. Token + phone number ID issued at app creation.

## Endpoints
- Base URL: `https://graph.facebook.com/v18.0`
- Auth: `Authorization: Bearer <access_token>`
- Common methods:
  - `GET /<phone_number_id>/messages` — list (via webhook or polling)
  - `POST /<phone_number_id>/messages` — send message — **N — gated**

## Rate limits
- Tier-based (Tier 1: 1K unique customers/24h; Tier 2: 10K; Tier 3: 100K)
- Per-conversation: 1K business-initiated messages per 24h
- Backoff: exponential, max 60s

## Reversibility class
- Webhook receive / poll for new messages: **Y**
- Draft reply (local-only, NOT sent until confirmed): **Y**
- `POST /messages` (actual send): **N** — explicit operator confirm required
- Template message creation: **Y** (template approval is async, no harm to draft)
- Template send: **N** — confirm required

## Voice-fidelity note (critical for inbox-manager)

WhatsApp tone is materially different from email tone — shorter, more casual,
emoji-tolerant on the operator side, no formal sign-offs. The voice corpus
in `agents/inbox-manager/memory/voice_corpus.md` MUST sample WhatsApp threads
separately from email threads. A reply drafted in email-voice on a WhatsApp
thread reads wrong.

## Error patterns
- `190 OAuth Exception`: token expired or revoked
- `131008 Unsupported message type`: incoming has media/format the connector
  doesn't handle yet — log and skip; surface to operator
- `131047 Re-engagement message`: 24h window closed; need template send

## Invocation pattern

```python
from claude_connectors.whatsapp_business import WhatsAppClient

wa = WhatsAppClient.from_env()

# Receive (autonomous; webhook or poll)
messages = wa.list_recent_messages(hours=24)

# Draft (autonomous; local-only)
draft = wa.compose_reply(
    to=messages[0].sender,
    body=composed_reply,   # SHORT — WhatsApp voice
)

# Send (gated)
# wa.send(draft)   # uncomment only after explicit operator confirm
```

## Operator setup checklist
- [ ] Meta Business Suite account
- [ ] WhatsApp Business Platform app created
- [ ] Phone number registered
- [ ] Access token obtained
- [ ] Webhook URL configured (or polling fallback enabled)
- [ ] Verify token set
- [ ] Env vars set
- [ ] Tested send to operator's own number first (template message)
