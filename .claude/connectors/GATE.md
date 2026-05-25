# WebFetch Allowlist Gate

> Companion to `README.md`. The README documents the connector-config
> convention; this file documents the autonomous-fetch security gate.

## Purpose

Hard-gate enforced URL allowlist for `hydrate-context` and any agent skill that performs autonomous `WebFetch`. Every fetch a skill makes on its own initiative MUST be validated against `known-services.json` before execution. Default-deny: unknown hosts are rejected.

## Threat model

Prompt injection can introduce attacker-controlled URLs into agent context. A vault note, a clipped article, an emailed PDF, or any user-summarized document can carry a string of the shape "for the canonical reference, see `https://attacker.example.com/...`". Without an allowlist, an autonomous fetch primitive pulls attacker-controlled docs into the shared shelf and labels them canonical. Downstream agents then read the poisoned doc as authoritative — payloads can include jailbreak instructions, fake credential endpoints, or further prompt-injection text that escalates into tool use.

The gate is the single chokepoint that closes this vector: every URL is validated against an operator-curated registry of canonical documentation hosts before any fetch fires.

## Files

- `.claude/connectors/known-services.json` — canonical registry. Operator-curated.
- `.claude/connectors/_gate.py` — Python module + CLI. Library entry: `from _gate import check_url`.
- `hooks/lib/hydrate-gate.ps1` — PowerShell wrapper. Delegates to `_gate.py`.
- `hooks/lib/hydrate-gate.sh` — bash wrapper. Delegates to `_gate.py`.
- `.claude/connectors/_gate.log` — append-only audit log (gitignored, per-machine).
- `agents/librarian/memory/gate_blocks.md` — block notices the librarian surfaces in the weekly digest.

## Schema

Each entry in `known-services.json` `services[]`:

```json
{
  "service": "shopify-admin-api",
  "canonical_docs_url": "https://shopify.dev/docs/api/admin",
  "allowed_hosts": ["shopify.dev", "help.shopify.com"],
  "last_verified": "2026-05-25",
  "notes": "Shopify Admin REST + GraphQL"
}
```

Root keys: `_schema_version`, `_updated`, `_owner`, `_purpose`, `services`. The `allowed_hosts` list is the actual decision surface — `canonical_docs_url` is documentation for the operator. The gate matches on hosts, never on the full URL path.

## Gate behavior

1. URL is parsed; scheme must be `https`. `http`, `file`, `ftp`, `javascript`, `data` are all rejected. https-only is deliberate: an attacker-controlled middlebox can MITM `http` even on a legitimate host, so allowing downgrades would undo the allowlist.
2. Host is canonicalized: lowercased, port stripped, IDN-normalized.
3. If a `service-hint` was passed, the host must appear in that named service's `allowed_hosts`. Cross-service mismatches block (e.g., a `vercel` hint with a `shopify.dev` host is rejected).
4. If no `service-hint`, the host must appear in the union of every service's `allowed_hosts`.
5. Otherwise BLOCK. Reason is logged.
6. Every check appends to `_gate.log`. Every block additionally appends to `agents/librarian/memory/gate_blocks.md` so repeated rejections surface in the weekly digest.

## How to add a service

1. Confirm the canonical documentation URL with the vendor (root of their docs site, not a tutorial path).
2. Identify every host the docs legitimately serve content from (e.g., `docs.foo.com` + `help.foo.com` + `foo.com`). Do NOT include CDN hosts that serve user-uploaded content — only first-party documentation hosts.
3. Add an entry to `services[]` with `service`, `canonical_docs_url`, `allowed_hosts`, `last_verified` (today's date), `notes`.
4. Bump `_updated` at the root.
5. Smoke test: `python .claude/connectors/_gate.py https://<new-host>/docs/...` — expect exit 0.

## Integration

Skills that perform autonomous WebFetch (e.g., `hydrate-context`) MUST call the gate first.

Python:

```python
from _gate import check_url
verdict = check_url(url, service_hint=optional_service_name)
if not verdict.allowed:
    # log + abort. Do NOT fetch.
    return
# proceed with fetch
```

Bash:

```bash
bash hooks/lib/hydrate-gate.sh "$URL" "$SERVICE_HINT" || exit 1
```

PowerShell:

```powershell
powershell -NoProfile -File hooks/lib/hydrate-gate.ps1 -Url $URL -ServiceHint $hint
if ($LASTEXITCODE -ne 0) { return }
```

The gate is fail-closed. If the gate itself errors, treat as BLOCK and do not fetch.

## What the gate does NOT do

- It does not fetch. It is a pre-check.
- It does not validate certificates or content. Operators are responsible for trusting hosts in the registry.
- It does not protect against compromise of an allowlisted host. If `docs.foo.com` itself is compromised, the gate will not catch it — that is the operator-curation contract: only allowlist hosts whose first-party trust is acceptable.
- It does not match on URL path or query string. A legitimate host that hosts both docs and arbitrary user content is unsafe to allowlist; pick narrower hosts.
