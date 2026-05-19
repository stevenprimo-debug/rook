# Software Dev Team — Reference Pack

**Domain:** Software craft — TDD, clean architecture, code review discipline, ship-velocity vs production-readiness tension.

**Purpose:** Authoritative canonical sources for an AI agent supporting software development teams. Every URL verified live.

---

## 1. Test-Driven Development: By Example — Kent Beck

**Concept:** The canonical exposition of the TDD cycle (Red → Green → Refactor). Beck demonstrates how writing a failing test before any production code drives organic, loosely coupled design and eliminates fear in development.

**Key ideas:**
- The two rules: write a failing automated test before writing code; remove all duplication
- Red/Green/Refactor loop as a rhythm for incremental design
- Worked examples in Money and xUnit, followed by a patterns catalogue (Red Bar Patterns, Green Bar Patterns, xUnit Patterns, Design Patterns for TDD)
- "Clean code that works" (Ron Jeffries) as the goal

**Source:** Kent Beck, *Test Driven Development: By Example*, Addison-Wesley / InformIT, 2002 (ISBN 9780321146533)
**URL:** https://www.informit.com/store/test-driven-development-by-example-9780321146533

---

## 2. The Clean Architecture — Robert C. Martin (Uncle Bob)

**Concept:** A unifying architecture model that subsumes Hexagonal Architecture, Onion Architecture, and BCE (Boundary-Control-Entity). Defines four concentric layers (Entities, Use Cases, Interface Adapters, Frameworks & Drivers) governed by a single Dependency Rule: source code dependencies may only point inward.

**Key ideas:**
- Independence from frameworks, UI, database, and any external agency
- Business rules testable without infrastructure
- The Dependency Inversion Principle as the mechanism for crossing layer boundaries
- Data must cross boundaries in the form most convenient for inner circles (no Entity objects or database rows in outer-to-inner direction)

**Source:** Robert C. Martin, "The Clean Architecture", *The Clean Code Blog*, 13 August 2012
**URL:** https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

---

## 3. Hexagonal Architecture (Ports & Adapters) — Alistair Cockburn

**Concept:** The original 2005 pattern paper that inspired Clean Architecture, Onion Architecture, and every modern "ports-and-adapters" implementation. Defines an application as an inside/outside system: the app communicates via *ports* (purpose-defined interfaces it owns), and *adapters* convert between port protocols and external technologies (UI, database, message queue, test harness). Eliminates the traditional left/right layered asymmetry.

**Key ideas:**
- Create your application to work without either a UI or a database — run automated regression tests, survive database outages, and link apps together
- Primary (driving) ports vs. secondary (driven) ports
- Test harnesses (FIT) as left-side adapters; mock databases as right-side adapters
- Write use cases at the application boundary, not at the technology layer
- "Ports & Adapters" is the implementation name; "Hexagonal Architecture" describes the visual shape

**Source:** Alistair Cockburn, "Hexagonal Architecture (Ports & Adapters)", HaT Technical Report 2005.02, 4 September 2005
**URL:** https://alistair.cockburn.us/hexagonal-architecture

---

## 4. Accelerate + DORA Research — Forsgren, Humble, Kim

**Concept:** The most rigorous empirical study of software delivery performance. Four years of survey research with thousands of organizations, using structural equation modeling to identify which capabilities actually *cause* better outcomes — not just correlate. Defines the four DORA metrics (Deployment Frequency, Lead Time for Change, Change Failure Rate, Time to Restore Service) and the cluster-based performance bands (Low → Medium → High → Elite).

**Key ideas:**
- DORA metrics measure two dimensions: throughput (Deployment Frequency, Lead Time) and stability (Change Failure Rate, Time to Restore) — high performers excel at both simultaneously
- Specific technical capabilities that predict Elite performance: trunk-based development, continuous integration, test automation, loosely coupled architecture, monitoring/observability
- Generative organizational culture (Westrum model) is both a predictor and an outcome
- Software delivery performance predicts organizational performance (profitability, market share, productivity)
- The Shingo Publication Award–winning text on lean and DevOps

**Source:** Dr. Nicole Forsgren, Jez Humble, Gene Kim, *Accelerate: The Science of Lean Software and DevOps*, IT Revolution Press, 2018 (ISBN 9781942788331)
**URL:** https://itrevolution.com/product/accelerate/

**Annual updates:** DORA publishes the *State of DevOps Report* annually at dora.dev. The 2024 report adds findings on AI as an amplifier, platform engineering tradeoffs, and stable organizational priorities as the #1 predictor of developer well-being.
**URL:** https://dora.dev/research/2024/dora-report/

---

## 5. Software Engineering at Google — Winters, Manshreck, Wright (eds.)

**Concept:** A practitioner's account of how Google scales engineering practices across a monorepo of billions of lines of code and tens of thousands of engineers. Covers the full lifecycle: culture, processes (code review, testing, documentation), and tooling. The Code Review chapter is the canonical industry reference for structured review discipline.

**Key ideas from the Code Review chapter:**
- Three required approval signals: LGTM (correctness/comprehension), ownership, and readability (language-style credential)
- Changes should target ~200 lines — ~35% of Google changes touch a single file
- Most reviews use exactly one reviewer; additional reviewers yield diminishing returns
- Automate everything automatable (linters, formatters, static analysis) so humans focus on design and logic
- 24-working-hour expected turnaround; prompt, professional, non-piecemeal feedback
- Code reviews as a permanent historical record (why decisions were made), accessible via code search

**Source:** Titus Winters, Tom Manshreck, Hyrum Wright (eds.), *Software Engineering at Google*, O'Reilly, March 2020. Free HTML edition licensed CC BY-NC-ND 4.0.
**URL (book landing):** https://abseil.io/resources/swe-book
**URL (Code Review chapter):** https://abseil.io/resources/swe-book/html/ch09.html

---

## 6. Microservices — Martin Fowler & James Lewis

**Concept:** The seminal 2014 article that named and defined the microservices architectural style. Describes nine characteristics of the approach, contrasts it with monolithic deployables, and sets out the conditions under which the tradeoffs favor microservices over a monolith.

**Key ideas:**
- Componentization via services (not libraries): independently deployable, explicit Published Interfaces
- Organized around business capabilities, not technology layers (aligns with Conway's Law)
- "You build it, you run it" (Amazon model): teams own their product through its lifetime
- Smart endpoints, dumb pipes: simple RESTish protocols or lightweight messaging; avoid ESBs
- Decentralized data management: polyglot persistence; eventual consistency over distributed transactions
- Design for failure: circuit breakers, semantic monitoring, chaos engineering
- Microservice Premium: complexity cost that is only justified for sufficiently complex systems

**Source:** Martin Fowler & James Lewis, "Microservices", martinfowler.com, 25 March 2014
**URL:** https://martinfowler.com/articles/microservices.html

**Companion piece — Monolith First:** Fowler's follow-up argues almost all successful microservice stories started as monoliths. Recommends the monolith-first strategy to discover stable Bounded Context boundaries before the "treacle" of multi-service refactoring sets in.
**URL:** https://martinfowler.com/bliki/MonolithFirst.html

---

## 7. Building Microservices — Sam Newman

**Concept:** The practical book-length treatment of how to design, build, deploy, test, observe, and evolve microservice architectures. The 2nd edition (2021) covers containers, Kubernetes, serverless, Backends for Frontends (BFF), consumer-driven contracts, sagas, observability, and stream-aligned teams. Paired with *Monolith to Microservices* for teams decomposing existing systems.

**Key ideas:**
- Information hiding, coupling, and cohesion as the core design forces for service boundaries
- Domain-Driven Design (Bounded Contexts) as the primary modeling tool
- Communication styles: synchronous request/response vs. asynchronous event-driven collaboration
- Four axes of scaling; the organizational implications of microservices (stream-aligned teams, enabling teams)
- When *not* to use microservices: greenfield projects before stable boundaries are known

**Source:** Sam Newman, *Building Microservices*, 2nd edition, O'Reilly, August 2021
**URL:** https://samnewman.io/books/building_microservices_2nd_edition/

---

## 8. The Twelve-Factor App — Adam Wiggins (Heroku)

**Concept:** A methodology for building SaaS applications that are portable, CI/CD-friendly, scalable without architecture changes, and minimally divergent between dev and production. Originally distilled from Heroku's operational experience; now a standard baseline for cloud-native and microservice deployments.

**Key factors (selected):**
- **Codebase** — one codebase tracked in version control, many deploys
- **Dependencies** — explicitly declare and isolate all dependencies
- **Config** — store config in the environment (not in code)
- **Backing services** — treat databases, queues, caches as attached resources
- **Build/Release/Run** — strict separation of build and run stages
- **Processes** — stateless, share-nothing processes; persist state in backing services
- **Logs** — treat logs as event streams; never manage logfiles in the app

**Source:** Adam Wiggins et al., *The Twelve-Factor App*, Heroku, 2011–2012
**URL:** https://12factor.net

---

## 9. Refactoring Catalog — Martin Fowler

**Concept:** A companion to the *Refactoring* book (1st ed. Java 1999; 2nd ed. JavaScript 2018), providing a named, searchable catalog of behavior-preserving code transformations. Defines refactoring precisely as restructuring internal code structure without changing external behavior, through small, safe steps verified by frequent test runs.

**Key ideas:**
- Refactoring (noun) vs. refactoring (verb): a specific, named transformation vs. the activity of applying transformations
- The catalog provides a shared vocabulary for code review comments and PR descriptions
- Refactoring precedes feature work ("preparatory refactoring") to make changes easier
- Automated IDE support is useful but not required: small steps + frequent testing suffice
- Reinforces the TDD/clean architecture principle that test coverage is the safety net enabling confident restructuring

**Source:** Martin Fowler, *Refactoring* (2nd edition) + online catalog, refactoring.com
**URL:** https://refactoring.com

---

## Quick-Reference Matrix

| Source | Expert | Core Concept | Year | Type |
|---|---|---|---|---|
| [TDD: By Example](https://www.informit.com/store/test-driven-development-by-example-9780321146533) | Kent Beck | Red/Green/Refactor cycle | 2002 | Book |
| [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | Robert C. Martin | Dependency Rule, four layers | 2012 | Blog post |
| [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture) | Alistair Cockburn | Ports & Adapters pattern | 2005 | Pattern paper |
| [Accelerate](https://itrevolution.com/product/accelerate/) | Forsgren / Humble / Kim | DORA metrics, Elite performers | 2018 | Book / research |
| [DORA 2024 Report](https://dora.dev/research/2024/dora-report/) | Google DORA team | AI tradeoffs, platform eng | 2024 | Annual report |
| [SWE at Google](https://abseil.io/resources/swe-book) | Winters / Manshreck / Wright | Code review, testing at scale | 2020 | Book (free HTML) |
| [Microservices](https://martinfowler.com/articles/microservices.html) | Fowler & Lewis | Microservice definition & tradeoffs | 2014 | Article |
| [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) | Martin Fowler | When to avoid microservices | 2015 | Bliki |
| [Building Microservices 2e](https://samnewman.io/books/building_microservices_2nd_edition/) | Sam Newman | Practical microservice design | 2021 | Book |
| [Twelve-Factor App](https://12factor.net) | Adam Wiggins | Cloud-native app methodology | 2011 | Methodology site |
| [Refactoring Catalog](https://refactoring.com) | Martin Fowler | Named code transformations | 1999/2018 | Catalog + book |

---

*All URLs verified live. Foundational pre-2020 texts included where they remain the definitive primary source (TDD 2002, Hexagonal Architecture 2005, Microservices 2014). DORA research updated annually at dora.dev.*
