# ADR-0006: Database — PostgreSQL (with a `pgvector` Path Instead of a Separate Vector Store)

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

DevFeed needs a relational store for repository metadata, and eventually needs full-text search and, further out, semantic/embedding-based similarity search once keyword matching stops being sufficient.

## Decision

PostgreSQL as the single data store, using full-text search (`tsvector`) now, with `pgvector` planned inside the same database for embeddings once semantic search is justified (Stage 6) — deliberately avoiding a second data store until it's genuinely needed.

## Alternatives considered

- A dedicated search engine (Elasticsearch/OpenSearch) for full-text search.
- A dedicated vector database for embeddings, once semantic search arrives.

Both are explicitly named in `DEVFEED.md` as rejected for the current stage.

## Rationale

Six endpoints and Stage 2 traffic volumes don't justify operating a second data store just for full-text search — Postgres `tsvector` covers it. The same logic extends forward: `pgvector` running inside the same Postgres instance covers embeddings when Stage 6 arrives, avoiding the operational cost of a dedicated vector database unless `pgvector` genuinely can't keep up at whatever scale is reached by then.

## Consequences

**Easier:** one data store to operate, back up, and reason about consistency for, at every stage from 0 through at least Stage 6; infrastructure providers (e.g., swapping Neon for another Postgres host) are a configuration change, not a data-model change.

**Harder:** if `pgvector` does turn out not to keep up at scale, migrating to a dedicated vector store later means moving data out of Postgres rather than having built on one from the start — that migration cost is deferred, not avoided, if the assumption proves wrong.

**Trigger for revisiting:** external search infrastructure is introduced "only if scale genuinely requires it," per `DEVFEED.md` §22 — not by default.

Source: [`DEVFEED.md` §8](../../DEVFEED.md#8-technology-stack), [§15](../../DEVFEED.md#15-personalization-and-recommendations), [§22](../../DEVFEED.md#22-deployment-and-infrastructure).
