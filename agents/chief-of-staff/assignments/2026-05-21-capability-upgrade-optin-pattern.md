---
name: Capability Upgrade Opt-In Pattern
description: >
  Cross-cutting spec for the optional-plugin upgrade prompt pattern.
  When an agent detects a prompt matching an optional plugin's keyword
  triggers AND that plugin is available, it surfaces an AskUserQuestion
  opt-in per Rule #14. Operator's choice is cached for the session.
  If plugin unavailable, agent shows install instructions and falls back
  to baseline. Generalizes the AskUserQuestion-only operator input rule
  (Rule #14) to optional-plugin upgrade paths.
type: assignment
from: product-manager
to: chief-of-staff
date: 2026-05-21
confidence: high
ai-first: true
status: draft
priority: high
reversibility: Y
affects_agents:
  - designer
  - creative-director
  - marketing-director
  - social-media-manager
  - product-manager
  - content-strategist
  - shopify-agent
  - engineering-lead
  - sales-director
proposed_rule: "18"
---

## For future Claude (TL;DR)

This spec defines how any ROOK agent handles OPTIONAL plugin upgrades. Detection → availability check → AskUserQuestion opt-in (Rule #14 shape) → session cache → graceful degradation. Affects 9 agents. Proposes Rule #18 for `_CLAUDE.md` Section 0. No agent SKILL.md files modified by this brief — implementation is a follow-on assignment.

---

## 1. Proposed Rule #18 (exact text for `_CLAUDE.md` Section 0)

> **18. Capability upgrades use the opt-in pattern.** When an agent detects a prompt matching an optional-plugin upgrade path AND the plugin is confirmed available, it MUST surface the choice via AskUserQuestion (per Rule #14) before proceeding. Operator's choice is cached per session at `.claude/session/optin-cache.json` (gitignored). If the plugin is unavailable, the agent shows install instructions and falls back to baseline gracefully — no error, no abort.

---

## 2. The 9-Agent Table

| Agent | Optional Upgrade | Plugin ID | Example Keyword Triggers |
|---|---|---|---|
| designer | claude-design (anthropics/frontend-design) | `claude-design` | any visual prompt — offer by default |
| creative-director | claude-design | `claude-design` | mockup, deck, poster, landing-page |
| marketing-director | claude-design | `claude-design` | landing page, campaign creative, ad creative |
| social-media-manager | claude-design | `claude-design` | reel, carousel, post graphic, Instagram |
| product-manager | claude-design | `claude-design` | UI, wireframe, screen, prototype |
| content-strategist | claude-design | `claude-design` | hero image, cover, blog header |
| shopify-agent | claude-design + UCP-buyer | `claude-design`, `ucp-buyer` | product page design, storefront, agentic-commerce |
| engineering-lead | freecad-mcp | `freecad-mcp` | DWG, parametric, FreeCAD, 3D model |
| sales-director | zoominfo-mcp | `zoominfo-mcp` | enrich, prospect list, ICP scoring, lookup |

---

## 3. Detection Logic

### 3a. Standard regex pattern per agent

Each agent's SKILL.md `## Optional Upgrades` section declares a `keyword_regex` per upgrade. Pattern is matched case-insensitively against the raw operator prompt at Step 1 of context load.

```yaml
optional_upgrades:
  - plugin_id: claude-design
    keyword_regex: "\\b(ui|screen|wireframe|prototype|design|visual|layout|mockup)\\b"
    offer_always: false   # set true for designer — offer on ANY visual prompt
    plugin_check: path_exists
    plugin_path: "~/.claude/skills/anthropic-skills/frontend-design/"
```

**Special case — `designer` agent:** `offer_always: true` — the designer agent offers claude-design upgrade on every prompt because visual fidelity is always relevant to its domain.

### 3b. Regex examples per upgrade type

| Upgrade | Regex |
|---|---|
| claude-design (named triggers) | `\b(mockup|deck|poster|landing.?page|hero|carousel|reel|post.graphic|wireframe|ui|screen|prototype|ad.creative|campaign.creative)\b` |
| claude-design (designer default) | match-always (offer_always: true) |
| freecad-mcp | `\b(dwg|dxf|parametric|freecad|3d.model|cad|bracket|flange|housing|sheet.metal|step.export)\b` |
| zoominfo-mcp | `\b(enrich|prospect.list|icp.scor|lookup|contact.data|zoominfo|lead.enrich)\b` |
| ucp-buyer (shopify) | `\b(agentic.commerce|buyer.agent|storefront|product.page.design|ucp)\b` |

---

## 4. Plugin Availability Check

Each plugin type has a deterministic availability check. Run at first-trigger detection per session; result is cached alongside the opt-in decision.

| Plugin | Check Method | Command / Path |
|---|---|---|
| `claude-design` | Path existence | `~/.claude/skills/anthropic-skills/frontend-design/SKILL.md` |
| `freecad-mcp` | MCP config presence | grep `freecad-mcp` in `~/.claude/mcp-servers.json` OR `.claude/settings.json` |
| `zoominfo-mcp` | MCP config presence | grep `zoominfo` in `~/.claude/mcp-servers.json` OR `.claude/settings.json` |
| `ucp-buyer` | Node + npm global | `node --version` returns >= 18 AND `npm list -g @shopify/ucp-cli` exits 0 |

Check implementation (pseudocode):
```python
def plugin_available(plugin_id: str) -> bool:
    if plugin_id == "claude-design":
        return Path("~/.claude/skills/anthropic-skills/frontend-design/SKILL.md").expanduser().exists()
    elif plugin_id in ("freecad-mcp", "zoominfo-mcp"):
        config = load_mcp_config()  # reads .claude/settings.json
        return plugin_id in config.get("mcpServers", {})
    elif plugin_id == "ucp-buyer":
        node_ok = subprocess.run(["node", "--version"], capture_output=True).returncode == 0
        ucp_ok = subprocess.run(["npm", "list", "-g", "@shopify/ucp-cli"], capture_output=True).returncode == 0
        return node_ok and ucp_ok
    return False
```

---

## 5. AskUserQuestion Shape (Rule #14 compliant)

All opt-in questions follow the GStack decision-brief format: header chip ≤12 chars, question ending in `?`, 2-4 options each ≥40 chars, one "(Recommended)" flag, "Other" auto-included.

### Template — claude-design upgrade

```
[UPGRADE] Use claude-design for this? (better visual fidelity, requires plugin)

Option A (Recommended): Yes — activate claude-design for higher-fidelity visual output this session (~2 min extra)
Option B: No — continue with baseline output using standard markdown + inline styles
Other: [free text]
```

### Template — freecad-mcp upgrade

```
[UPGRADE] Use FreeCAD MCP for this? (parametric 3D modeling, requires FreeCAD running)

Option A (Recommended): Yes — drive FreeCAD directly for full parametric model output this session
Option B: No — produce a structured spec/script the operator can run manually in FreeCAD
Other: [free text]
```

### Template — zoominfo-mcp upgrade

```
[UPGRADE] Use ZoomInfo MCP for this? (live contact enrichment, consumes API credits)

Option A: Yes — enrich contacts live via ZoomInfo API (uses enrichment credits)
Option B (Recommended): No — use cached/baseline prospecting approach with available data
Other: [free text]
```

### Template — ucp-buyer upgrade (shopify-agent)

```
[UPGRADE] Use UCP agentic-commerce for this? (live Shopify buyer agent, requires Node 18+)

Option A (Recommended): Yes — activate UCP buyer agent for agentic storefront interaction
Option B: No — design product page spec and Shopify theme code without live buyer agent
Other: [free text]
```

---

## 6. Session-Level Caching

Cache file: `.claude/session/optin-cache.json` (gitignored — add to `.gitignore` if not already present).

Cache key format: `<agent-slug>-<plugin-id>-<session-id>`

Cache entry shape:
```json
{
  "designer-claude-design-abc123": {
    "choice": "yes",
    "timestamp": "2026-05-21T10:32:00Z",
    "plugin_available": true
  }
}
```

**Rules:**
- Cache is written on first AskUserQuestion response per `(agent, plugin, session)` triplet.
- If cache hit exists for the session, skip AskUserQuestion and proceed per cached choice.
- Cache is ephemeral — scoped to session. Not persisted across Claude Code restarts.
- If `plugin_available` was `false` at cache time and operator chose "yes", agent re-checks availability on next invocation (plugin may have been installed mid-session).

---

## 7. Graceful Degradation

When operator selects "Yes — use upgrade" AND plugin is unavailable:

1. Agent does NOT error out or abort.
2. Agent surfaces install instructions (one-time, inline):

```
[PLUGIN UNAVAILABLE] claude-design is not installed at the expected path.

To install:
  claude mcp add anthropic-skills

After install, restart Claude Code and re-invoke this task.

Continuing with baseline output now.
```

3. Agent proceeds with baseline capability immediately.
4. Cache records `{ "choice": "yes", "plugin_available": false, "fell_back": true }` — so the question is not re-asked this session.

---

## 8. Per-Agent SKILL.md Addition Format

Add a new `## Optional Upgrades` section to each affected agent's SKILL.md, placed after `## Routing Keywords` and before `## Routing Enforcement Manifest`.

Standard section shape:

```markdown
## Optional Upgrades

> Governed by Rule #18. On keyword match: check availability → AskUserQuestion → cache for session → proceed.

| Plugin | Trigger | Availability Check | Fallback |
|---|---|---|---|
| claude-design | mockup, deck, poster, landing-page | path: `~/.claude/skills/anthropic-skills/frontend-design/SKILL.md` | baseline markdown + inline CSS |

**Detection regex:** `\b(mockup|deck|poster|landing.?page)\b`
**Offer always:** false
**Session cache key:** `<agent-slug>-claude-design-<session-id>`
**Install instructions:** `claude mcp add anthropic-skills`
```

Shopify-agent gets TWO entries in the table (claude-design + ucp-buyer). All other agents get ONE entry.

---

## 9. Open Questions for Operator Decision

**Q1 — designer agent offer-always behavior.** The spec proposes `offer_always: true` for the designer agent (claude-design offered on every prompt). This means the opt-in fires even on text-only tasks like "write copy for this page." Alternatives:

- **A. Keep offer-always** — designer is a visual agent; the question is always relevant.
- **B. Require at least one visual keyword** — reduces noise on pure-text tasks; use the same regex as other agents.
- **Recommended:** A (offer-always). If Primo finds it noisy, flip to B.

**Q2 — zoominfo opt-in recommended flag.** The template above marks "No — baseline" as Recommended for ZoomInfo because it consumes API credits. If ZoomInfo credits are plentiful, flip the recommended flag to "Yes."

- **A. Keep "No" as Recommended** — protects credits by default.
- **B. Flip to "Yes" as Recommended** — assumes credits are available and enrichment quality is worth it.
- **Recommended:** A. Operator can flip per project.

**Q3 — Cache persistence.** Currently cache is ephemeral (session-scoped, not persisted across restarts). If Primo wants to "always use claude-design for designer tasks" without re-answering every session:

- **A. Keep ephemeral** — clean default, no state leakage across sessions.
- **B. Add a persistent preference layer** — `~/.claude/upgrade-prefs.json` (gitignored) that stores cross-session defaults; AskUserQuestion only fires on first-ever use per `(agent, plugin)` pair.
- **Recommended:** A for now. B is a follow-on if the question becomes noisy.

**Q4 — UCP-buyer node check strategy.** Current check runs `npm list -g` which can be slow (~1-2s). Alternative: check for the binary directly at `$(npm root -g)/@shopify/ucp-cli/bin/ucp`.

- **Recommended:** use binary path check — faster, same signal.

---

## 10. Implementation Checklist (for follow-on assignment)

- [ ] Add `## Optional Upgrades` section to 9 agent SKILL.md files
- [ ] Add `.claude/session/` to `.gitignore`
- [ ] Add Rule #18 to `_CLAUDE.md` Section 0 (after Rule #17)
- [ ] Write `scripts/optin-cache.py` — read/write helper for the cache JSON
- [ ] Write `scripts/check-plugin-availability.py` — per-plugin check logic
- [ ] Test AskUserQuestion shape in designer and engineering-lead first (highest-frequency paths)
- [ ] Update `hooks/routing-rules.json` if keyword arrays change per agent

---

## Version History

### v1.0 — 2026-05-21
Initial spec. Product Manager agent. Covers 9 agents, 4 plugin types, full opt-in lifecycle.
