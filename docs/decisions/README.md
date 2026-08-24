# Architecture Decision Records

This directory records the architecturally significant decisions made in `DEVFEED.md`, in standard ADR format, so the reasoning behind each one is traceable independent of the main specification document.

**Scope note:** every ADR here documents a decision that is already explicit in `DEVFEED.md` — none are speculative or invented for this documentation pass. Where `DEVFEED.md` leaves a choice genuinely open (e.g., the exact hosting provider within a category, or the stargazer-data source for star velocity), the ADR status is marked `Proposed` rather than `Accepted — Design Decision`, and the open sub-decision is called out explicitly.

No ADR exists yet for caching strategy, because `DEVFEED.md` §22 explicitly defers that decision to when a caching need actually materializes — there is no decision to record yet, only a list of potential future cache targets.

**Decision made ≠ implementation completed.** Every ADR below records a decision about the target architecture for the Stage 0–3 build (Current Design, in the terminology used across this documentation set). None of them describes running code — the repository contains no `core/`, `api/`, or `web/` directories, so nothing in this index has been built or validated yet. `Accepted — Design Decision` means the decision itself is settled and isn't expected to be relitigated without a documented reason; it does not mean the decision has been implemented. The status column would only ever read `Accepted / Implemented` once the repository actually contains the corresponding code — none currently qualify.

## Index

| ADR | Decision | Status |
|---|---|---|
| [ADR-0001](./ADR-0001-modular-monolith.md) | Modular monolith over microservices | Accepted — Design Decision |
| [ADR-0002](./ADR-0002-ranking-engine-isolation.md) | Ranking engine as an isolated, pure module | Accepted — Design Decision |
| [ADR-0003](./ADR-0003-ingestion-separate-deployment.md) | Ingestion as a separate deployment target from the API | Accepted — Design Decision |
| [ADR-0004](./ADR-0004-backend-framework.md) | Backend framework: FastAPI + Pydantic | Accepted — Design Decision |
| [ADR-0005](./ADR-0005-frontend-framework.md) | Frontend framework: Next.js, React, TypeScript, Tailwind | Accepted — Design Decision |
| [ADR-0006](./ADR-0006-database-postgresql.md) | Database: PostgreSQL (with `pgvector` path instead of a separate vector store) | Accepted — Design Decision |
| [ADR-0007](./ADR-0007-deterministic-ranking.md) | Deterministic ranking before machine learning | Accepted — Design Decision |
| [ADR-0008](./ADR-0008-search-postgres-fulltext.md) | Search: PostgreSQL full-text search instead of a dedicated search engine | Accepted — Design Decision |
| [ADR-0009](./ADR-0009-position-cursor-pagination.md) | Position-cursor pagination over a deterministic total order | Accepted — Design Decision |
| [ADR-0010](./ADR-0010-bounded-candidate-retrieval.md) | Bounded candidate retrieval (500–1,000 rows) before ranking | Accepted — Design Decision |
| [ADR-0011](./ADR-0011-rejected-technologies-current-stage.md) | Explicitly rejected technologies for the current stage (Kafka, dedicated vector DB, GraphQL) | Accepted — Design Decision |
| [ADR-0012](./ADR-0012-deployment-hosting-approach.md) | Deployment approach: free-tier hosting split across frontend/API/database | Proposed |

Source of truth for all decisions: `DEVFEED.md`, primarily [§7](../../DEVFEED.md#7-system-architecture), [§8](../../DEVFEED.md#8-technology-stack), [§12](../../DEVFEED.md#12-ranking-engine)–[§14](../../DEVFEED.md#14-search), [§22](../../DEVFEED.md#22-deployment-and-infrastructure).
