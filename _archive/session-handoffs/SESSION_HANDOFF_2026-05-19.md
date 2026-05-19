# Session handoff — 2026-05-19

**What landed:** ~17,000 lines of work across roster lock, sanitization, connector buildout, supervisor + session-segregation patterns.

## Shipped this session

### Roster + structure
- **20-agent roster locked.** Removed `prospecting-agent` + `sales-outreach` as peer agents; folded into `agents/sales-director/skills/prospecting/` and `agents/sales-director/skills/outreach/`. Old memory + CLAUDE.md archived to `_archive/2026-05/sales-lane-fold/`.
- **2 new custodial agents written:** `account-manager` (Account-Memory / Deal-Architecture / Renewal-Window bench) and `inbox-custodian` (Voice-Fidelity / Inbox-Reduction / Reversibility-Discipline bench).
- **Tier 1 / Tier 2 split:** `vault-agents/ops-engineer/` created — vault-only, excluded from cohort zip. Reliability-Over-Cleverness / Observable-By-Default / Contamination-Is-A-Bug bench.

### Sanitization
- Three sanitizer scripts now cover the surface: `sanitize-context-folders.py`, `sanitize-repo-wide.py`, `sanitize-brand-bleed.py`.
- Stripped: operator names, family names, employer, location, internal code-names (PROMETHEUS, Q360, BSA), vertical-lock terms (Ableton, Stage Pro, Savant Playback, touring engineer, playback software, Max for Live, LiveAPI, M4L), exit-path framing (Dec 2026, 4-pillar doctrine, exit math, bridge income), `_FROM_CLAUDE` references, Razer 18, Domotz.
- 54+ files in `agents/*/context/`, 27 files in registry skills + agents, 5 in archive, all clean.
- `av-touring.yaml` keyword pack archived (operator-domain example, not generic).

### Connectors (27 services, sub-folder pattern)
- New convention: `.claude/connectors/<service>/{README.md, api-reference.md, client.py?}`.
- **`client.py` fully implemented:** Perplexity, HubSpot, Stripe, GitHub. Pattern: env-var auth, `from_env()` constructor, urllib-based (no third-party deps), read methods autonomous, write methods return `WriteRequest` requiring `execute_write(confirmed=True)` for explicit operator confirm.
- **Stubs (README + api-reference):** quickbooks, discord, adobe-acrobat, adobe-sign, apollo, autodesk, obsidian, twitter-x, linkedin, meta-graph, figma, google-search-console, google-analytics + 7 MCP-reference pages (gmail, gcal, zoominfo, vercel, cloudflare, supabase, drive-sharepoint).
- **No minimum consumer count** — any service the operator actively uses gets a vault-level connector.

### Patterns built in (not deferred)
- **Hierarchical Supervisor** — Chief of Staff distills subagent returns to ≤2K tokens (verdict + named action + reasoning summary + source pointer). Documented in `agents/chief-of-staff/SKILL.md` § Distilled Return rule. Mirrored in `hooks/routing-rules.json` `_global_rules.distilled_subagent_returns`.
- **Session segregation** — `ROOK_SESSION_MODE=operator` env var toggles operator-mode writes to `memory/operator/` and `context/operator/` subpaths. `hooks/session-mode-injector.{ps1,sh}` surfaces active mode at every session start. `package-for-cohort.py` excludes `operator/` paths with a P0 sanity check that aborts the zip on any leak.

### Tools
- **`scripts/ppx.py`** — Perplexity ping-pong CLI. `python scripts/ppx.py "query"` returns synthesized answer + citations. Works against the real `/v1/responses` Agent API endpoint Primo verified.
- **`scripts/sync-child-skills.py`** — mirrors `agents/<a>/skills/<s>/` to `.claude/skills/<a>-<s>/` for Claude Code discovery.
- **`scripts/scaffold-connector-stubs.py`** — generates README + api-reference scaffolds for new connectors from a service registry.
- **`scripts/package-for-cohort.py`** — produces clean cohort zip with 5 pre-flight gates (all sanitizers + 3 regen scripts in `--check` mode). Zip went from 252MB → **52MB** after excluding vendor dirs (`obsidian-cli/vendor/`, `markitdown/` source). Customer install does `pip install -r requirements.txt`.

### Customer-facing
- **`INSTALL.md`** — full customer onboarding guide (prereqs, deps, connector credentials, verify step, troubleshooting).
- **`requirements.txt`** — Python deps customer installs at install-time (markitdown, playwright, weasyprint, pypdf2, pyyaml, requests, pytest).
- **`.claude/agents/_ROSTER.md`** — rewritten with lane grouping (Custodial, Revenue, Content/Brand, Product/Eng, Finance, Intelligence), child-skill table, archive log.

### Cross-cutting fixes
- BOM + CRLF handling in `regenerate-claude-agents.py` (18 of 20 SKILL.md files had UTF-8 BOM that broke parsing).
- UTF-8 stdout enforcement in `scripts/ppx.py` (Windows cp1252 was choking on common API response chars).
- Perplexity client uses the real endpoint surface: `/v1/responses` with `{preset, input}` shape (not the OpenAI-shaped `/chat/completions` I'd guessed first).
- Naming convention locked: directors (strategic) / managers (domain stewards) / leads (technical IC) / specialists (niche IC) / custodians (operational). No forced standardization.

## Open for next session

### High-priority
1. **Push to GitHub** — happening now this session.
2. **Rotate Perplexity API key** — exposed in chat history via screenshot. Not blocking; key never ships (env-var only), but rotate before the repo goes public.
3. **`managed-agents-2026-04-01` beta header documentation** — Anthropic's Managed Agents API requires this header. Not currently documented in any connector. Should land in ops-engineer connector-health mode + relevant agent SKILL.md inheritance.

### Medium-priority
4. **WhatsApp Business capture pipeline** — image-to-markdown was deferred. Basic send/receive ships in v1 inbox-custodian; the full capture pipeline (webhook listener + media downloader + markdown generation + account routing) belongs at `agents/inbox-custodian/skills/whatsapp-capture/` and is a separate session.
5. **Pre-commit hook for sanitizers + regen scripts** — currently the gates only fire in `package-for-cohort.py`. Should fire on every `git commit` too. ops-engineer's domain.
6. **Verify the 20-agent cap claim** — Perplexity ping-pong revealed there's no documented Anthropic "20-agent-per-coordinator cap" in current docs. Memory at `CLAUDE CODE/MEMORY/feedback_org_architecture_v3_locked.md` line 16 says there is. Worth confirming against live Anthropic docs and updating the memory.

### Low-priority / v1.1
7. **Remaining `client.py` implementations** — Adobe Acrobat, Adobe Sign, Apollo, QuickBooks, Discord, Autodesk, Figma, Twitter/X, LinkedIn, Meta Graph, Obsidian wrapper, GSC, GA4. Each follows the Perplexity/HubSpot/Stripe/GitHub pattern.
8. **Hierarchical multi-coordinator architecture** — Perplexity recommended sharded coordinators (multiple chief-of-staff-style routers) as the scaling pattern beyond single-coordinator. Worth designing before customer #2.
9. **`scripts/check-operator-paths.py`** — utility that scans the repo for accumulated operator-mode data accidentally living in shipped paths.
10. **Connector health checks** — ops-engineer's connector-health mode currently stubbed; needs actual ping-the-endpoint implementation.

### Patterns to honor going forward
- **Build-time estimates against AI-time, not human-dev-team-time** ([feedback_build_time_estimates_exaggerated.md](CLAUDE CODE/MEMORY/feedback_build_time_estimates_exaggerated.md)). Today's "30 minutes realistically" was right.
- **No minimum consumer threshold on connectors** — any operator-active service gets a vault-level connector.
- **API reference as context, not as duplicated agent context** — single `.claude/connectors/<service>/api-reference.md` per service; agents reference, don't duplicate.

## State at session close

- 20 Tier 1 agents + 1 Tier 2 agent (ops-engineer, vault-only)
- 27 connectors with consistent README + api-reference structure; 4 with full `client.py` (Perplexity, HubSpot, Stripe, GitHub)
- Zero brand-bleed across `.claude/`, `agents/`, `hooks/`, `scripts/`, `vault-agents/`
- All 5 pre-flight gates pass; cohort packager produces clean 52MB zip
- Perplexity ping-pong working end-to-end via `python scripts/ppx.py "query"`
- Git: pushed to `github.com/stevenprimo-debug/rook` (this session's commit)
