# Anthropic Deployment Notes

Reference for operators deploying ROOK via Anthropic Managed Agents or direct Claude API integration. Current as of 2026-05-19; verify against live docs before deployment-critical decisions.

## Managed Agents API — current state (research preview, 2026)

The Anthropic **Managed Agents** API is the canonical deployment surface for multi-agent systems like ROOK. As of May 2026 it remains in research preview — operators need explicit access. Public beta launched April 2026.

### Required beta header

Every call to the Managed Agents API endpoints MUST include:

```http
anthropic-beta: managed-agents-2026-04-01
```

Without this header, calls return 404 or 400 depending on endpoint. The header is the activation gate for the entire Managed Agents surface.

Sources cited in 2026-05-19 ping-pong: anthropic.com/engineering/managed-agents, platform.claude.com/docs/managed-agents/overview.

### Rate limits (per organization)

| Operation type | Limit |
|---|---|
| Create endpoints (agents, sessions, environments, etc.) | 60–300 req/min |
| Read endpoints (retrieve, list, stream) | 600 req/min |

Org-level spend limits and tier-based rate limits also apply. No hard documented "agent-per-coordinator cap" — see "Roster size assumptions" below.

### Billing

- **Session runtime:** $0.08 per session-hour (in addition to token costs)
- **Token costs:** standard per-model rates (Sonnet $3/$15 per M, Opus $5/$25 per M, Haiku $1/$5 per M as of 2026)
- Long-horizon sessions (hours to days) are the supported use case

### Supported models

Flagship models with default 1M context windows:
- Claude 4.6 Sonnet
- Claude 4.6 Opus
- Claude 4.5 Haiku

Agent SKILL.md frontmatter `model: claude-opus-latest` / `claude-sonnet-latest` resolves to current flagship at invocation time.

## Roster size assumptions

**Status:** unverified as of 2026-05-19.

Internal memory previously stated a "hard cap of 20 agents per coordinator." Live Anthropic docs do NOT document a numeric agent-per-coordinator cap — only the rate limits above. ROOK currently sits at 20 Tier 1 agents (cohort-shipped) + 1 Tier 2 agent (operator-only `ops-engineer`), which is well-formed regardless of cap.

If the roster grows beyond 20, the Anthropic-recommended scaling pattern is **multiple coordinators with sharded rosters** rather than a single mega-coordinator. ROOK's chief-of-staff is currently a single coordinator; multi-coordinator sharding is a v2+ design problem, not a v1 ship blocker.

## Recommended best-practice patterns (per Anthropic + Perplexity 2026-05-19 ping-pong)

1. **Harness Decoupling** — separate sandboxes for operator-internal vs customer-facing agents. ROOK implements this via the `agents/` (Tier 1, ships) vs `vault-agents/` (Tier 2, operator-only) split, with `scripts/package-for-cohort.py` enforcing the exclusion at package time.
2. **Hierarchical Supervisor with scoped context** — the customer-facing interface agent receives distilled summaries (1–2K tokens) from worker agents, never raw tool outputs. ROOK's chief-of-staff implements this via the "Distilled Return rule" — see [agents/chief-of-staff/SKILL.md](../agents/chief-of-staff/SKILL.md).
3. **Boundary guardrails + audit trails** — zero-trust between agents, secret detection on outputs, session segregation via the beta header and distinct `session_id` paths. ROOK implements this via the Reversibility-Discipline pole on every agent, the operator-vs-customer session-mode segregation ([`.claude/session-modes.md`](session-modes.md)), and ops-engineer's contamination-audit mode.

## Security posture for hosted deployment

Three pre-requisites before ROOK deploys via Anthropic Managed Agents (vs local Claude Code). These were surfaced by Perplexity ping-pong red-team 2026-05-19 against the v3.1 ship state. They do NOT block local Claude Code installs; they DO block hosted Managed Agents deployment.

### 1. Cross-Agent Prompt Injection Propagation (CAPP) defense

Subagent returns can carry hidden instructions designed to survive summarization and reach the coordinator as system directives. ROOK's defense: **provenance tagging** in the chief-of-staff Distilled Return rule. Every fact in a distilled return carries an `[Origin: <agent>:<source-type>]` tag. Untrusted-tagged content is reference-only — never executed as instruction. See [`agents/chief-of-staff/SKILL.md`](../agents/chief-of-staff/SKILL.md) § Provenance tagging.

This is a CONVENTION the agent runtime enforces. For Managed Agents hosted deployment, the runtime should additionally tag inbound content from external connectors with `[Origin: untrusted-*]` automatically before passing to any agent.

### 2. Credential isolation via Managed Tool Proxy

Connector credentials (HubSpot API key, Stripe API key, GitHub PAT, etc.) currently read from environment variables. In a sandboxed Managed Agents environment, a compromised agent can read its own process environment and exfiltrate credentials.

**Pattern for hosted deployment:** the agent never holds raw API keys. Instead, calls go through a **tool proxy** (operator-controlled service outside the agent sandbox) that injects credentials server-side and forwards the request. The agent sees only the proxy endpoint; the credentials never enter the sandbox.

ROOK's v1 connector `client.py` implementations read env vars directly — fine for local install (operator's own machine). For hosted deployment, the operator wraps each `client.py` with a proxy layer OR uses Anthropic's managed-credential-injection feature (when available).

**v1.1 task:** stub a reference proxy implementation at `.claude/connectors/_lib/proxy.py` so hosted deployers have a starting point.

### 3. Network egress allowlist

Default-deny on agent network egress. Allow only the specific domains documented at [`.claude/connectors/_egress-allowlist.md`](../.claude/connectors/_egress-allowlist.md). This prevents a compromised agent from exfiltrating vault contents via arbitrary outbound HTTP calls, even if it bypasses the operator-confirm gates on known connectors.

For Managed Agents deployment: paste the egress allowlist domains into the agent network policy at deploy time. For local Claude Code installs: this is the customer's machine; standard local-app security applies.

### Summary table — what these mean for v1 cohort vs hosted

| Risk | Local Claude Code install (v1) | Anthropic Managed Agents (hosted) |
|---|---|---|
| Prompt injection | low (customer's own data sources) | HIGH — needs CAPP defense via provenance tags |
| Credential exposure | low (customer's own env vars) | HIGH — needs tool proxy pattern |
| Egress exfiltration | low (customer's own network) | HIGH — needs allowlist enforcement |

## What this means for ROOK agent SKILL.md files

Agents that interact with the Anthropic API directly (rare — most agents use Claude Code's session-level integration, not the raw API) should:

- Inherit the beta header from a shared config rather than declaring it per-agent
- Document the model they expect (`claude-opus-latest` / `claude-sonnet-latest`) in frontmatter
- Reference this doc rather than restating Managed Agents specifics inline

For deployment via Anthropic Managed Agents specifically, the operator's hosting layer (whatever Anthropic-provided runtime is in use) handles the header injection — individual agents don't need to set it. Documenting it here is for the operator's awareness when wiring up Managed Agents, not for runtime agent behavior.

## Cohort customer install considerations

Customers running ROOK locally via Claude Code (not via Managed Agents) don't need the beta header at all — Claude Code handles the API surface and the header is irrelevant. The beta header only matters when:

- The operator deploys ROOK as a hosted multi-agent system via Anthropic Managed Agents (production option)
- An agent directly calls `claude.ai/api/v1/messages` or the Managed Agents endpoints (rare)

For v1 cohort ship (everyone runs locally via Claude Code), this doc is reference, not a setup gate.

## Sources

- anthropic.com/engineering/managed-agents (2026-04-08)
- platform.claude.com/docs/en/managed-agents/overview
- the-ai-corner.com/p/claude-managed-agents-guide-2026
- verdent.ai/guides/claude-managed-agents-pricing
- siliconangle.com 2026-04-08 launch announcement

Verified via Perplexity ping-pong 2026-05-19 in this session.

## Update cadence

This doc should be re-verified against live Anthropic docs before each major ROOK release. Ops-engineer's connector-health mode is the canonical place to wire that check.
