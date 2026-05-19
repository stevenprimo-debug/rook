# Software Engineering — Progression Path

## Who This Is For

The operator who ships code — web / SaaS surfaces, internal tools, agent infrastructure — and refuses to confuse "it runs on my machine" with "it survives real users at real load with real adversaries." Solo founders, technical co-founders, product engineers, and full-stack operators owning the build end-to-end.

By the end of this path you should be able to:
- Architect a system you understand at 2am.
- Ship to production with confidence.
- Debug a stack trace without panic.
- Run a security audit.
- Operate the inner loop fast enough that learning is not gated on tooling.
- Develop observability deep enough to answer any production question in 5 minutes.

## Stage 1: Foundations (weeks 1-4)

**Goal:** Internalize TDD discipline. Read code fluently. Ship one feature with tests.

**Read / Watch:**
- *The Pragmatic Programmer* — David Thomas and Andrew Hunt. The working-engineer's career manual. Read once; re-read annually.
- *Clean Code* — Robert C. Martin. Controversial in places; the chapters on naming, functions, and tests are canon.
- *Code* — Charles Petzold. The bottom-up "how does a computer work" book. The chapters on logic gates and CPUs make abstraction stop being magic.
- *Test-Driven Development by Example* — Kent Beck. The original; short; mandatory.
- *Refactoring* — Martin Fowler. The catalog of refactorings; read for the technique, reference forever.
- **The MIT 6.001 / 6.0001 lectures on YouTube** — the classic intro-to-CS lecture archive; the lessons on abstraction and program structure compound.
- **Julia Evans's zines and blog** (jvns.ca) — the most accessible deep-technical writing on the internet; the debugging zine alone justifies the visit.

**Practice:**
- Build one CRUD app end-to-end in your chosen stack. Tests first. Test coverage above 70%. Deploy to a real domain. The exercise teaches that "build" includes "deploy."
- Read 500 lines of someone else's production code (pick a popular open-source repo: React, Stripe SDK, Tailwind, Next.js, Supabase). Annotate every section: what does it do, why is it structured this way, what would break if you removed it.
- Develop a personal coding-style guide: naming conventions, file structure, test conventions, comment policies. The style guide is for you; consistency-with-yourself is the gate.
- Configure your inner loop: editor + LSP + auto-test-on-save + auto-format-on-save + hot-reload. The inner-loop time target is <5 seconds for any change in any file.

**Skill check:**
- Your CRUD app is in production.
- You can deploy a change in <5 minutes end-to-end (commit → CI → deploy).
- Your test suite catches regressions.
- Your inner loop is fast enough that you don't lose flow.

## Stage 2: Applied Practice (weeks 5-12)

**Goal:** Architecture decisions. Code review discipline. Ship a multi-feature system with measurable performance.

**Read / Watch:**
- *Designing Data-Intensive Applications* — Martin Kleppmann. The modern data-systems textbook; the chapters on replication, consensus, and stream processing are canon.
- *Database Internals* — Alex Petrov. The companion; goes deeper on storage engines and B-trees.
- *Domain-Driven Design* — Eric Evans. The "big blue book"; the bounded-context discipline is the keeper.
- *Patterns of Enterprise Application Architecture* — Martin Fowler. The catalog of system patterns; reference forever.
- *Site Reliability Engineering* — Google (free at sre.google/books). The operational discipline.
- *Release It!* — Michael Nygard. The patterns for production-readiness; the stability patterns chapter is mandatory.
- **The Pragmatic Engineer newsletter** — Gergely Orosz. Engineering-org and architecture case studies at scale.
- **High Scalability blog** (highscalability.com) — architecture case studies of real systems at scale.
- **Stripe Engineering blog and the Cloudflare blog** — two of the highest-signal engineering blogs publicly available.
- **The Changelog podcast** — open-source-craft conversations.

**Practice:**
- Architect one system from scratch on paper before writing code. Draw the data model, the API surface, the deployment topology, the failure modes. Defend the architecture against a peer's critique.
- Run a code-review discipline on your own work: every commit must be reviewable by you in 24 hours; if it's not, the PR is too big — split it. Use a pre-commit hook for linting / type-checking.
- Ship one multi-feature system (3+ features, real users). Add observability: structured logging, error tracking (Sentry / Honeybadger), metrics (Posthog / Plausible / DataDog). Watch real traffic.
- Run a perf-audit: measure p50 / p95 / p99 latency on the three highest-traffic endpoints. Identify the bottleneck. Fix it. Re-measure.
- Develop a debugging muscle: when something breaks, do not guess. Reproduce reliably. Add logging. Isolate variables. The discipline of root-cause vs. band-aid is the entire game.

**Skill check:**
- Your multi-feature system handles real users without on-call surprises.
- Your perf metrics are visible in a dashboard.
- Your code-review (of yourself) is producing readable diffs.
- You can debug a production issue without panic.

## Stage 3: Advanced Mastery (months 3-9)

**Goal:** Production-grade systems. Security discipline. Ship-velocity at scale.

**Read / Watch:**
- *The Effective Engineer* — Edmond Lau. The leverage-thinking applied to engineering work.
- *Staff Engineer* — Will Larson. The technical-leadership track; the patterns of staff-level work transfer to solo founders.
- *An Elegant Puzzle* — Will Larson. The engineering-management companion.
- *Software Engineering at Google* — Titus Winters et al. The operational discipline at scale.
- *Working in Public* — Nadia Eghbal. Open-source-as-infrastructure; the maintainer-burden chapter matters.
- *The Phoenix Project* — Gene Kim et al. DevOps as novel; the lessons land harder in fiction format.
- *The DevOps Handbook* — Gene Kim et al. The non-fiction companion.
- *Web Application Hacker's Handbook* — Dafydd Stuttard and Marcus Pinto. The security textbook; the OWASP Top 10 is in here in case-study form.
- *Threat Modeling* — Adam Shostack. The discipline of "how does this break under adversary?"
- **The Pragmatic Engineer's archive** — all of it.
- **Charity Majors's writing on observability** (charity.wtf and the Honeycomb blog) — the modern observability discipline.
- **Hillel Wayne's "Computer Things" newsletter** — formal-methods-adjacent; teaches a different way of thinking.
- **The Architecture of Open Source Applications** (free books at aosabook.org) — case studies of real systems.

**Practice:**
- Run a security audit on your shipped system: OWASP Top 10 walkthrough, dependency-supply-chain scan (npm audit, snyk, dependabot), secrets-scan (gitleaks), authn/authz review. Fix every high-severity finding.
- Build observability deep: structured logging at every layer, distributed tracing (OpenTelemetry), real-user-monitoring, synthetic-monitoring on critical paths. The discipline of "I can answer any question about production in <5 min" is the gate.
- Develop a release-engineering discipline: feature flags, gradual rollout, instant rollback, dark-launch for risky changes. Ship one change behind a flag end-to-end.
- Run a chaos-engineering exercise: take down one component intentionally; watch how the system degrades. Fix the worst failure mode. Document the learning.
- Ship-velocity audit: time-to-merge, time-from-merge-to-prod, time-to-revert. Measure them. Optimize the slowest.

**Skill check:**
- Your system handles real adversarial traffic.
- Your observability answers production questions in <5 min.
- Your release process supports same-day rollback.
- You can debug at 2am because the code is legible at 2am.
- Your security audit caught at least one issue before it hit production.

## Ongoing Development

**Stay current:**
- **The Pragmatic Engineer** — Gergely Orosz; weekly.
- **Hacker News** — daily; filter ruthlessly.
- **The Changelog podcast** — weekly.
- **Stripe and Cloudflare engineering blogs** — irregular but high signal.
- **Julia Evans's blog** — irregular; always educational.
- **Hillel Wayne's "Computer Things"** — weekly.
- **Sourcegraph's "Dev Tools"** newsletter.
- **The Pragmatic Engineer Deep Dives** (paid) — for the deeper org and architecture case studies.

**Communities to join:**
- **r/programming, r/ExperiencedDevs, r/learnprogramming** — variable but useful for spot questions.
- **The Pragmatic Engineer Slack / Discord** — paid; high signal.
- **Local meetups** (any tech-stack-specific group) — in-person matters.
- **Hacker News read-only** is fine; the threads are where most learning happens.

**Quarterly cadence:**
- Pull your last quarter's commits. Read your own code cold.
- Identify the three patterns you'd refactor today with current knowledge. Refactor one. Document the others as known-debt.
- Re-audit dependencies: outdated, vulnerable, unused. Update or remove.
- Score the observability stack: which questions could you answer; which got blocked.
- Re-audit the security posture: any new vulnerabilities; any new attack surface from shipped features.
- Re-read one foundational text (Kleppmann, Fowler, SRE book, Pragmatic Programmer); identify what you can use now.

## Cross-References

- The the Stack agent that operates in this domain: `agents/software-dev-team/SKILL.md`
- Methodology framework(s) cited: `agents/software-dev-team/context/methodology/` (in development)
- Reference clippings: `agents/software-dev-team/context/references/` (vendored as Phase 1 expands)
- Related agents:
  - `agents/product-manager/SKILL.md` — specs the build
  - `agents/r-and-d-lead/SKILL.md` — graduated experiments become production
  - `agents/engineering-lead/SKILL.md` — cross-discipline for hardware-software integration
  - `agents/shopify-agent/SKILL.md` — ecommerce-specific software-dev variant
  - `agents/seo-specialist/SKILL.md` — technical SEO implementation (Core Web Vitals, schema, programmatic)
  - `agents/designer/SKILL.md` — UI implementation against design specs
- Three-principle gate (per SKILL.md): Ship-Velocity, Production-Readiness, Debuggability held in productive tension.
- For the Stack canonical stack: Vercel (Next.js or SPA) + Supabase (Postgres + RLS + Auth + Storage) by default. NOT Cloudflare Workers (except [example email agent]), Netlify, or Heroku. See `memory/project_canonical_stack.md`.
- For agent-infrastructure dev: MCP server pattern (FastMCP for Python, MCP SDK for TS); see `anthropic-skills:mcp-builder` for the canonical guide.
- For security audit: OWASP Top 10, dependency-supply-chain (npm audit / snyk / dependabot), secrets-scan (gitleaks), authn/authz review. Run before any launch.
- For observability: structured logging at every layer; OpenTelemetry tracing; Sentry / Honeybadger error tracking; PostHog / Plausible / DataDog metrics; real-user-monitoring; synthetic-monitoring on critical paths.
- For release engineering: feature flags (LaunchDarkly, GrowthBook, or homegrown); gradual rollout; instant rollback; dark-launch for risky changes.
- For solo-operator scale: optimize the inner loop ruthlessly. <5 second feedback on any file change. The fast loop is the asset.
- For pair-with-AI workflow: use Claude Code (gstack) or Cursor as the agent layer; humans drive architecture and code review; the AI drives implementation and refactoring; the audit trail lives in git.
- The Software Dev Team agent coordinates four sub-roles internally: front-end, back-end, security, QA. Dispatch each sub-role for the appropriate task surface.
- Critical SKILL.md gates: every shipped feature passes (a) test coverage threshold, (b) code review, (c) security checklist, (d) perf regression check, (e) accessibility audit where applicable.
- For AI-coding-agent context: prefer gstack's `/autoplan`, `/review`, `/qa`, `/ship` chain (per user CLAUDE.md) — the gauntlet catches what a solo dev would miss.
