# ADR-0011: Explicitly Rejected Technologies for the Current Stage

## Status

Accepted — Design Decision *(the rejection itself is trivially true today, since the repository contains no code of any kind — but the decision governs the planned architecture, not just the current empty state)*

## Context

`DEVFEED.md` names several specific technologies as considered and rejected for the current build, rather than simply omitted — worth recording as a decision in its own right so a future contributor doesn't re-propose them without knowing they were already weighed.

## Decision

For the current stage, the following are explicitly not used:

| Technology | Reason rejected |
|---|---|
| Kafka / event streaming | No event-streaming need exists yet |
| A dedicated vector database | `pgvector` covers embeddings inside Postgres once genuinely needed (see ADR-0006) |
| GraphQL | REST is sufficient for a six-endpoint API |
| Kubernetes | No container-orchestration need exists at current scale (zero deployed traffic) |
| Redis / Celery / background task queues | No background-processing need exists yet; introduced only once ingestion or AI calls start blocking request latency |
| Elasticsearch / OpenSearch | Postgres full-text search covers Stage 2 search needs (see ADR-0008) |

## Alternatives considered

Each rejected technology *is* the alternative under consideration here — this ADR exists to record that these were named and rejected, not to compare further options against them.

## Rationale

`DEVFEED.md`'s stated engineering principle: don't introduce a dependency or piece of infrastructure without a reason, and don't introduce infrastructure before it solves a problem that's actually been demonstrated. Every item above solves a real problem this project may eventually have, but none of those problems currently exist in a demonstrated form.

## Consequences

**Easier:** a smaller, simpler stack to build, operate, and onboard new contributors to; less speculative infrastructure to maintain before there's any usage to justify it.

**Harder:** if any of these needs materializes suddenly rather than gradually, there's some integration lag while the corresponding piece gets added — accepted as a reasonable tradeoff against building all of it upfront on the chance it's needed.

**Trigger for revisiting each:** listed individually in [`roadmap.md`](../product/roadmap.md#what-triggers-each-piece-of-stage-4-infrastructure).

Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture), [§8](../../DEVFEED.md#8-technology-stack), [§22](../../DEVFEED.md#22-deployment-and-infrastructure).
