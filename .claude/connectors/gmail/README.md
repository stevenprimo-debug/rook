# Gmail connector

**Status:** stub — v1.0 ships scaffolding; auth wire-up is per-operator setup.

## Consumers
- `inbox-manager` (read inbox, write drafts)
- `account-manager` (read inbound from accounts; never write)
- `sales-director/skills/outreach` (write drafts)
- `sales-director/skills/reply-handling` (read + write drafts)

## Credentials
- Env var: `GMAIL_OAUTH_REFRESH_TOKEN` (preferred) or `GMAIL_API_KEY` (legacy)
- Scope: `gmail.readonly` for read-only consumers (account-manager);
  `gmail.compose` for draft-writing consumers; `gmail.send` ONLY for explicit
  send actions (always operator-confirmed).
- Setup: Google Cloud project → OAuth2 client → refresh token via
  `https://developers.google.com/oauthplayground`. Store refresh token in
  `~/.claude/credentials/gmail.json` (gitignored).

## Endpoints
- Base URL: `https://gmail.googleapis.com/gmail/v1`
- Auth: `Authorization: Bearer <access_token>` (refresh on 401)
- Common methods:
  - `GET /users/me/messages?q=is:unread` — list unread
  - `GET /users/me/messages/<id>` — read full thread
  - `POST /users/me/drafts` — create draft
  - `POST /users/me/messages/send` — **N — gated**

## Rate limits
- 250 quota units per user per second (typical method = 5–10 units)
- Backoff: exponential, max 60s
- Daily cap: 1B quota units (functionally unlimited for single-operator use)

## Reversibility class
- `GET` (read messages, list threads, read labels): **Y**
- `POST /drafts` (create draft): **Y** — draft saved, not sent
- `PUT /drafts/<id>` (update draft): **Y**
- `POST /messages/send`: **N** — explicit operator confirm required
- `DELETE /messages/<id>`: **N** — explicit confirm; prefer archive (label move)
- `POST /labels` (create label): **Y**
- `POST /threads/<id>/modify` (apply/remove labels): **N** if removing `INBOX`
  label (archives the thread)

## Error patterns
- `401 invalid_grant`: refresh token expired or revoked — re-auth required
- `403 quotaExceeded`: hit per-user rate — back off
- `429 RESOURCE_EXHAUSTED`: hit short-term burst limit — back off
- `400 Failed Precondition`: usually means a label or message ID went stale

## Invocation pattern

```python
from claude_connectors.gmail import GmailClient

gmail = GmailClient.from_env()  # reads GMAIL_OAUTH_REFRESH_TOKEN

# Read (autonomous)
threads = gmail.list_threads(query="is:unread newer_than:1d")

# Draft (autonomous)
draft_id = gmail.create_draft(
    to="prospect@example.com",
    subject="Re: your question",
    body=composed_reply,
    thread_id=threads[0].id,
)

# Send (gated — never call without operator confirm)
# gmail.send_draft(draft_id)   # uncomment only after explicit confirm
```

## Operator setup checklist
- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth2 client created (Desktop application type)
- [ ] Refresh token obtained
- [ ] Token stored at `~/.claude/credentials/gmail.json`
- [ ] Env var `GMAIL_OAUTH_REFRESH_TOKEN` set
- [ ] Verified `gmail.list_threads()` returns expected data
