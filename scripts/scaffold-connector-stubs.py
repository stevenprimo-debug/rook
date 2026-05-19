#!/usr/bin/env python3
"""Scaffold connector README + api-reference stubs in one pass.

For each (service_slug, metadata) entry, writes:
- .claude/connectors/<slug>/README.md
- .claude/connectors/<slug>/api-reference.md

Skips files that already exist (won't overwrite hand-written content).
Re-runnable.

Idempotent. Stdlib only.

Usage:
    python scripts/scaffold-connector-stubs.py             # write missing stubs
    python scripts/scaffold-connector-stubs.py --check     # dry-run; exit 1 if any missing
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONNECTORS_DIR = REPO / ".claude" / "connectors"

# Each entry: (slug, display_name, integration_kind, consumers, auth_pattern, reversibility_note)
SERVICES = [
    # ---- API-direct (need client.py) ----
    ("stripe", "Stripe", "API-direct (Anthropic MCP also available)", ["finance-manager", "shopify-agent"],
     "Restricted API key. Env var STRIPE_API_KEY (live) and STRIPE_API_KEY_TEST (sandbox).",
     "Charge / refund / subscription mutations are N — explicit operator confirm. Reads are Y."),
    ("quickbooks", "QuickBooks Online", "API-direct", ["finance-manager"],
     "OAuth2 flow. Env vars QBO_CLIENT_ID, QBO_CLIENT_SECRET, QBO_REFRESH_TOKEN, QBO_REALM_ID.",
     "All POST/PUT/DELETE (journal entries, invoices, bills) are N. Reads are Y."),
    ("discord", "Discord", "API-direct (Bot token)", ["inbox-custodian", "marketing-director", "creative-director"],
     "Bot token from Developer Portal. Env var DISCORD_BOT_TOKEN. Bot must be invited to the server with required intents.",
     "Sending messages, role changes, kicks, bans are N. Reads (channel history, member list) are Y. WhatsApp-style voice-fidelity rule applies to drafts."),
    ("adobe-acrobat", "Adobe Acrobat / PDF Services API", "API-direct", ["sales-director", "account-manager", "designer"],
     "OAuth2 client credentials. Env vars ADOBE_CLIENT_ID, ADOBE_CLIENT_SECRET.",
     "PDF generation and form-fill are Y (output is local). Submission to e-sign workflows is N — use the adobe-sign connector for that."),
    ("adobe-sign", "Adobe Sign", "API-direct", ["sales-director", "account-manager"],
     "OAuth2. Env vars ADOBE_SIGN_CLIENT_ID, ADOBE_SIGN_CLIENT_SECRET, ADOBE_SIGN_REFRESH_TOKEN.",
     "Sending agreements for signature is N. Reading agreement status is Y."),
    ("apollo", "Apollo.io", "API-direct", ["sales-director"],
     "API key. Env var APOLLO_API_KEY.",
     "List enrichment, person search are Y (Apollo's own data). Pushing to operator's CRM is N — use the hubspot connector for that."),
    ("autodesk", "Autodesk (Fusion / AutoCAD)", "API-direct (Forge / Platform Services)", ["engineering-lead"],
     "OAuth2 3-legged or 2-legged depending on use. Env vars AUTODESK_CLIENT_ID, AUTODESK_CLIENT_SECRET.",
     "Reading files, extracting BOM data, querying model state are Y. Writing changes back to a hosted model is N."),
    ("obsidian", "Obsidian (via obsidian-cli)", "wrapper around existing skill", ["librarian", "chief-of-staff", "all agents (vault I/O)"],
     "No external auth — local vault path via VAULT_ROOT env var. Wraps the obsidian-cli skill already shipped.",
     "Vault reads are Y. Vault writes are reversible at the filesystem level but should still be logged to librarian's append log."),
    ("twitter-x", "Twitter / X", "API-direct (v2 API)", ["social-media-manager"],
     "Bearer token + OAuth1 for write endpoints. Env vars X_BEARER_TOKEN, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.",
     "Tweets, replies, DMs, follows are N. Read endpoints (search, user lookup, mentions) are Y. Heavy rate-limits on v2 free tier."),
    ("linkedin", "LinkedIn", "API-direct (LinkedIn API v2)", ["social-media-manager", "sales-director"],
     "OAuth2. Env vars LI_CLIENT_ID, LI_CLIENT_SECRET, LI_ACCESS_TOKEN.",
     "Posts, comments, connection invites are N. Profile reads are Y but limited by LinkedIn's API scope (most data requires partner approval)."),
    ("meta-graph", "Meta Graph API (Instagram + Facebook)", "API-direct", ["social-media-manager"],
     "OAuth2 with Page-scoped tokens. Env vars META_APP_ID, META_APP_SECRET, META_PAGE_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID.",
     "Posts, comments, replies, DMs are N. Insights and read-only profile data are Y. IG and FB share one connector via Meta's unified API."),
    ("figma", "Figma", "API-direct + community MCP available", ["designer", "creative-director"],
     "Personal access token. Env var FIGMA_PAT.",
     "Reads (file structure, components, variants) are Y. Comments and webhook setup are N."),
    ("google-search-console", "Google Search Console", "API-direct + Google MCP", ["seo-specialist"],
     "OAuth2 service account or user OAuth. Env vars GSC_SERVICE_ACCOUNT_JSON OR GSC_OAUTH_REFRESH_TOKEN + property URL.",
     "All endpoints are Y (read-only on indexed data + crawl errors). Submitting sitemaps is technically a write but reversible."),
    ("google-analytics", "Google Analytics (GA4)", "API-direct + Google MCP", ["seo-specialist", "marketing-director"],
     "OAuth2. Env vars GA4_SERVICE_ACCOUNT_JSON, GA4_PROPERTY_ID.",
     "All endpoints are Y (read-only on already-collected events)."),
    ("github", "GitHub", "Anthropic official MCP available", ["software-dev-team", "software-dev-team/skills/github-ops"],
     "Personal access token or GitHub App. Env vars GITHUB_TOKEN (PAT) or app-credentials JSON.",
     "Reads (repo / issue / PR / commit) are Y. Writes (commits, PRs, merges, releases, issue creation) are N. The github-ops child skill enforces this gate."),

    # ---- MCP-reference only (no client.py needed) ----
    ("google-calendar", "Google Calendar", "Anthropic MCP (already wired)", ["account-manager", "inbox-custodian", "chief-of-staff"],
     "Wired via Anthropic MCP setup. No new credentials needed — use the existing MCP namespace.",
     "Event creation / update / delete are N (external state change). Reads are Y."),
    ("zoominfo", "ZoomInfo", "Anthropic MCP (already wired)", ["sales-director/skills/prospecting"],
     "Wired via Anthropic MCP setup. No new credentials needed.",
     "All ZoomInfo MCP tools are Y (read-only enrichment / research)."),
    ("vercel", "Vercel", "Anthropic MCP (already wired)", ["software-dev-team"],
     "Wired via Anthropic MCP setup.",
     "Deployments and project mutations are N. Reads (logs, build status, project list) are Y."),
    ("cloudflare", "Cloudflare", "Anthropic MCP (already wired)", ["software-dev-team"],
     "Wired via Anthropic MCP setup.",
     "D1 query writes, KV writes, R2 bucket changes, Workers deploys are N. Reads are Y."),
    ("supabase", "Supabase", "Anthropic MCP (already wired)", ["software-dev-team"],
     "Wired via Anthropic MCP setup.",
     "apply_migration, execute_sql with mutations, branch creation are N. Reads (list_tables, get_logs, search_docs) are Y."),
    ("drive-sharepoint", "Google Drive / SharePoint", "Anthropic MCP (already wired)", ["account-manager", "librarian", "inbox-custodian"],
     "Wired via Anthropic MCP setup.",
     "File create / overwrite / delete are N. Reads (search, list, read_file_content) are Y."),
]

README_TEMPLATE = """# {display_name} connector

**Status:** v1 stub — README + api-reference scaffolded; {integration_kind}.

## Consumers
{consumers_list}

## Integration kind
{integration_kind}

## Credentials
{auth_pattern}

## Reversibility class
{reversibility_note}

## Operator setup checklist
- [ ] Credentials created
- [ ] Stored at `~/.claude/credentials/{slug}.json` OR env var(s) set
- [ ] Tested with smallest read call before any write
- [ ] If MCP-backed: verify the Anthropic MCP tools are listed in your deferred-tools set
- [ ] If API-direct: implement `client.py` against this README (template at `.claude/connectors/perplexity/client.py`)

## Notes
- See `api-reference.md` (same folder) for endpoint details.
- See `.claude/connectors/README.md` for the global connector convention.
"""

API_REF_TEMPLATE = """# {display_name} API — agent-facing reference

**Status:** stub — fill in on first connector use against the live docs.

## Authentication
{auth_pattern}

## Endpoints

| Endpoint | Method | Purpose | Reversibility |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 200 | OK | proceed |
| 401 | Auth failed | rotate / re-auth |
| 429 | Rate limit | exponential backoff |
| 500-599 | Vendor-side | exponential backoff |

## Reversibility per endpoint

{reversibility_note}

## Notes for first-use

When the consuming agent invokes this connector for the first time:
1. Verify the live API docs against this stub
2. Update endpoint table with the calls you actually need
3. Add error patterns specific to this service
4. If implementing `client.py`, copy `.claude/connectors/perplexity/client.py` as the pattern
"""


def consumers_block(consumers: list[str]) -> str:
    return "\n".join(f"- `{c}`" for c in consumers)


def write_stub(path: Path, content: str, check_only: bool) -> bool:
    """Write content to path if it doesn't exist or is empty. Return True if written/would-write."""
    if path.exists() and path.stat().st_size > 0:
        return False
    if not check_only:
        path.write_text(content, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    written = 0
    skipped = 0
    for slug, display_name, integration_kind, consumers, auth_pattern, reversibility_note in SERVICES:
        folder = CONNECTORS_DIR / slug
        folder.mkdir(parents=True, exist_ok=True)

        readme = folder / "README.md"
        api_ref = folder / "api-reference.md"

        params = {
            "slug": slug,
            "display_name": display_name,
            "integration_kind": integration_kind,
            "consumers_list": consumers_block(consumers),
            "auth_pattern": auth_pattern,
            "reversibility_note": reversibility_note,
        }
        readme_content = README_TEMPLATE.format(**params)
        api_ref_content = API_REF_TEMPLATE.format(**params)

        if write_stub(readme, readme_content, check_only):
            print(f"  {'would write' if check_only else 'wrote'}: {readme.relative_to(REPO).as_posix()}")
            written += 1
        else:
            skipped += 1

        if write_stub(api_ref, api_ref_content, check_only):
            print(f"  {'would write' if check_only else 'wrote'}: {api_ref.relative_to(REPO).as_posix()}")
            written += 1
        else:
            skipped += 1

    action = "would write" if check_only else "wrote"
    print(f"\nSummary: {action} {written} stub files, skipped {skipped} (already present).")
    if check_only and written > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
