---
name: overview
source: https://code.claude.com/docs/en/overview
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Claude Code Overview

## What it is

Agentic coding tool — reads/edits codebases, runs commands, integrates with dev tools. Available in Terminal CLI, VS Code, Desktop app, Web, JetBrains IDEs. The runtime ROOK lives in.

## Key concepts + config

### Install
```bash
# macOS/Linux/WSL
curl -fsSL https://claude.ai/install.sh | bash
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
# Homebrew
brew install --cask claude-code
# WinGet
winget install Anthropic.ClaudeCode
```

### Project memory
`CLAUDE.md` at project root — Claude reads at session start. Coding standards, architecture decisions, preferred libraries.

### Skills
Reusable workflows packaged for sharing (`/review-pr`, `/deploy-staging`).

### Hooks
Shell commands triggered before/after Claude actions — auto-format, lint, validate.

### CLI patterns
```bash
claude "write tests for auth module"
claude -p "review changed files for security issues"  # headless
tail -200 app.log | claude -p "flag anomalies"
git diff main --name-only | claude -p "review these"
```

### Integration points
- **MCP**: Google Drive, Jira, Slack, custom servers
- **CI/CD**: GitHub Actions, GitLab CI/CD
- **IDE**: VS Code (inline diffs, @-mentions), Cursor, JetBrains
- **Chat**: Slack `@Claude` mentions route to PRs
- **Sub-agents**: multiple Claude instances coordinating
- **Background agents**: parallel sessions monitored from one screen
- **Routines** (cloud-scheduled), **`/loop`** (in-session repeat)

### Session portability
- `claude --teleport` — pull web/iOS sessions into terminal
- `/desktop` — hand off terminal to Desktop for visual diffs
- Remote Control — continue from phone

## ROOK applicability

This IS the ROOK runtime. Every agent in the 20-agent OS runs inside Claude Code. CLAUDE.md is how ROOK injects vault rules; hooks are how routing-enforcer fires; skills are the agent skill files. The headless `claude -p` mode is what enables CI/automation use cases.

## Cross-references
- [[settings]] — settings.json shapes
- [[hooks]] — routing-enforcer hook lives here
- [[skills]] — agent SKILL.md spec
- [[../agent-sdk/overview]] — SDK for custom orchestration
