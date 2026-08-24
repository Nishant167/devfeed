# DevFeed Documentation

This is the documentation entry point for DevFeed. **`DEVFEED.md`, at the repository root, remains the canonical source of truth** — everything under `docs/` is that specification reorganized into a browsable structure, with explicit current/planned/future labeling on every page. If something here and `DEVFEED.md` ever disagree, `DEVFEED.md` wins, and the discrepancy should be fixed.

## Read this first: where the project actually is

The repository currently contains **documentation and governance files only** — no application code, no dependencies, no deployed infrastructure. `README.md` calls this **Stage 0**. Nearly everything technical described in this documentation set — the API, the database schema, the ranking engine, deployment — is a **specification for Stage 0–3**, not a description of running software. Each page states its status using one of four terms, applied precisely and never used interchangeably:

- **Implemented** — the repository actually contains this. Used only when real, committed code or configuration exists (e.g., `.gitignore` secret exclusion, the git/PR workflow itself, the fact that no authentication exists).
- **Current Design** — the architecture or product decision has been defined (usually in `DEVFEED.md`), but no implementation exists in the repository. This covers the entire Stage 0–3 build target: the API spec, database schema, ranking engine, ingestion pipeline, and most product/architecture documentation. Decision made ≠ implementation completed.
- **Planned** — the repository (specifically `DEVFEED.md`) explicitly identifies this as future work, typically Stage 4+, usually with a named trigger condition. This is deferred by design, not merely unimplemented.
- **Proposed** — an engineering recommendation or open sub-decision that hasn't been formally settled — either because `DEVFEED.md` leaves a specific choice open (e.g., which hosting provider), or because this documentation set inferred a reasonable scenario (e.g., alerting, the runbook) that `DEVFEED.md` itself never names as a deliverable.

A statement with no tag, or a bare "current," should be treated as an error in this documentation — flag it. See each ADR's status line for how this applies to architecture decisions specifically: an ADR being `Accepted — Design Decision` means the decision won't be relitigated without cause, not that it has been built.

## Product

What DevFeed is, who it's for, and how success is measured.

- [Product Vision](./product/product-vision.md) — what DevFeed is, the problem, and what it deliberately doesn't try to solve
- [Product Requirements](./product/product-requirements.md) — functional and non-functional requirements, with honest TBDs
- [User Personas](./product/user-personas.md) — the six developer segments the product targets
- [User Flows](./product/user-flows.md) — onboarding, discovery, search, and (future) learning flows
- [Success Metrics](./product/success-metrics.md) — stage gates, kill criteria, and what isn't optimized for
- [Roadmap](./product/roadmap.md) — Stage 0 through Stage 12, and what triggers each future addition

## Architecture

How the system is structured and why.

- [Architecture Overview](./architecture/architecture-overview.md) — the full diagram and the reasoning behind each component
- [System Context](./architecture/system-context.md) — external actors and the system boundary
- [Data Flow](./architecture/data-flow.md) — ingestion, processing, and feed-request pipelines
- [Component Design](./architecture/component-design.md) — the planned repository layout and module responsibilities
- [Deployment Architecture](./architecture/deployment-architecture.md) — local dev and planned Stage 2 hosting
- [Scalability](./architecture/scalability.md) — bounded candidate retrieval and what triggers scale-driven changes
- [Tradeoffs](./architecture/tradeoffs.md) — what each major architectural choice makes easier and harder

## Decisions

Architecture Decision Records for every significant, already-made technical decision.

- [Decision index](./decisions/README.md) — 12 ADRs covering monolith vs. microservices, ranking isolation, framework choices, database, search, pagination, and deployment

## API

The planned Stage 2 API surface — not implemented.

- [API Overview](./api/api-overview.md) — versioning, endpoint summary, what's not built yet
- [Authentication](./api/authentication.md) — the anonymous `session_id` model and the Stage 4 auth plan
- [Endpoints](./api/endpoints.md) — full request/response detail for every planned endpoint
- [Errors](./api/errors.md) — the error envelope and error codes
- [Rate Limits](./api/rate-limits.md) — GitHub's limits on ingestion vs. DevFeed's own (not-yet-built) API limiting

## Data

The planned data model and GitHub ingestion design.

- [Data Model](./data/data-model.md) — entities, relationships, and why some tables don't exist yet
- [Database Schema](./data/database-schema.md) — full column-level DDL for the planned Stage 2 tables
- [GitHub Data](./data/github-data.md) — ingestion source, query strategy, rate limits, failure handling
- [Data Pipeline](./data/data-pipeline.md) — the discover → fetch → validate → normalize → enrich → classify → index sequence
- [Data Retention](./data/data-retention.md) — what's defined (not much) and what's genuinely open

## Engineering

How to contribute, and the standards contributions are held to.

- [Development Guide](./engineering/development-guide.md) — prerequisites and the planned repo layout (no commands exist yet)
- [Testing Strategy](./engineering/testing-strategy.md) — current coverage (zero) vs. planned testing per module
- [Code Quality](./engineering/code-quality.md) — module boundaries, implementation completeness, dependency discipline
- [Git Workflow](./engineering/git-workflow.md) — branching, commits, PRs, and branch protection (already in effect)
- [Dependency Management](./engineering/dependency-management.md) — principles, and what's genuinely not decided yet

## Security

- [Security Architecture](./security/security-architecture.md) — the full security posture, by design
- [Threat Model](./security/threat-model.md) — threat → impact → mitigation → remaining risk, for realistic threats to this project
- [Authentication & Authorization](./security/authentication-authorization.md) — none today, by design; the Stage 4 plan
- [Secrets Management](./security/secrets-management.md) — environment file conventions and what's already enforced
- [Privacy](./security/privacy.md) — minimal-collection principle and what's genuinely unresolved

## Operations

What's deployed today (nothing) and what's designed for when something is.

- [Deployment](./operations/deployment.md) — planned Stage 2 topology
- [Configuration](./operations/configuration.md) — planned environment file conventions
- [Monitoring](./operations/monitoring.md) — current minimal design and the Stage 4+ metrics list
- [Logging](./operations/logging.md) — structured logs and per-repository sync status
- [Alerting](./operations/alerting.md) — doesn't exist yet, no trigger hit
- [Backup & Recovery](./operations/backup-recovery.md) — genuinely undefined; flagged as a gap
- [Runbook](./operations/runbook.md) — scenarios the design anticipates, pending real incident procedures

## Performance

No benchmarks exist. This section documents what's designed to bound performance risk and how targets will eventually be set.

- [Performance Requirements](./performance/performance-requirements.md) — TBD, and why
- [Benchmarking](./performance/benchmarking.md) — no benchmark established; how one should eventually be run
- [Capacity Planning](./performance/capacity-planning.md) — corpus-size estimates and the bounded-retrieval lever

## Diagrams

Standalone Mermaid source files for reuse outside this documentation — see [`diagrams/README.md`](../diagrams/README.md).
