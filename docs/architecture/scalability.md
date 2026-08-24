# Scalability

> **State: Current Design.** No load has ever been placed on this system because no version of it is deployed or implemented. This document describes the scalability mechanisms designed into the target architecture, not measured or observed scaling behavior.

## The core scalability lever: bounded candidate retrieval

Ranking never touches the full corpus. PostgreSQL pre-filters to a bounded candidate set — 500 to 1,000 rows — via an indexed query on topic, language, and recency, before anything reaches the ranking engine. This exists specifically because running the diversity pass (MMR) against tens of thousands of candidates on every request would blow the feed's performance budget. Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture), [§12](../../DEVFEED.md#12-ranking-engine).

## Why ranking is designed to run synchronously, and when that's expected to change

Ranking is designed to run in-process, synchronously, in the request path at Stage 2 volumes, against the bounded candidate set — not the full corpus. This is a design decision, not an observed behavior — no ranking code exists yet, so nothing currently "runs" at all. The documented plan is to move to a precomputed or cached ranking path only once candidate-set size or personalization complexity makes synchronous ranking *measurably* too slow, not preemptively. No such measurement exists, and none can, until the ranking engine and API are implemented and deployed. Source: [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination).

## Ingestion scale considerations

GitHub's Search API caps results at 1,000 per query, so the corpus is built from roughly 240 sliced queries (4 languages × 5 star bands × 12 monthly date ranges). The planning estimate is 10,000–20,000 unique repositories on the first run — explicitly labeled in the source document as a sizing estimate, not a measured or architecture-dependent number. Authenticated GitHub API access is rate-limited to 5,000 requests/hour; ingestion is designed to sleep proactively before exhaustion and use conditional requests (ETags) to avoid re-fetching unchanged repositories. Source: [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion).

## What triggers a scale-driven architecture change

| Signal | Documented response |
|---|---|
| Ingestion or AI calls start blocking request latency | Introduce Redis + background workers |
| Candidate-set ranking becomes measurably too slow synchronously | Move to a precomputed/cached ranking path |
| Keyword topic-matching visibly fails on nuanced interests | Introduce `pgvector` + embeddings (Stage 6) |
| A specific component provably needs independent scaling | Extract it from the modular monolith |

Source: [`DEVFEED.md` §26](../../DEVFEED.md#26-milestones-and-gates).

## What is explicitly not being solved for yet

Multi-region deployment, container orchestration, CDN configuration beyond hosting-platform defaults, and any distributed data store are all out of scope until a demonstrated need exists. There is currently no traffic, no deployed instance, and therefore no scalability problem to solve — this document exists to record the design intent for when that changes, not to claim the system has been proven at any scale.
