# ADR-0008: Search — PostgreSQL Full-Text Search Instead of a Dedicated Search Engine

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

Search needs to run over repository name, description, and topics, filterable by language and topic, with reasonable relevance ranking.

## Decision

PostgreSQL full-text search (`tsvector`) is the Stage 2 search implementation — a genuinely separate code path from the feed, with results ranked by Postgres relevance directly rather than by `core/ranking/`.

## Alternatives considered

- A dedicated search engine (Elasticsearch/OpenSearch) — explicitly named as "not introduced unless scale genuinely requires it" and rejected for the current stage.
- GraphQL as an alternative API query layer for flexible filtering — also explicitly rejected for the current stage, on the grounds that REST is sufficient for six endpoints.

## Rationale

At Stage 2 traffic and corpus size, Postgres `tsvector` is sufficient and avoids standing up and operating a second search infrastructure component. Search and feed are treated as genuinely different problems right now — search is a direct query for known intent; feed is personalized, ranked discovery — so having them use different ranking mechanisms (Postgres relevance vs. `core/ranking/`) isn't considered a gap to close immediately.

## Consequences

**Easier:** one fewer piece of infrastructure to deploy and operate; search pagination uses a simpler Postgres-native keyset (`ts_rank`, `id`) since search results aren't re-ranked by MMR and have no page-dependency problem, unlike the feed (see ADR-0009).

**Harder:** search and feed will eventually need to converge onto one retrieval-and-ranking pipeline once search grows into natural-language queries ("beginner-friendly Python projects for learning RAG") that need the same candidate-generation-plus-ranking approach the feed uses — that convergence is future work, not designed yet.

**Trigger for revisiting:** external search infrastructure is introduced only if scale genuinely requires it.

Source: [`DEVFEED.md` §8](../../DEVFEED.md#8-technology-stack), [§13](../../DEVFEED.md#13-feed-generation-and-pagination), [§14](../../DEVFEED.md#14-search).
