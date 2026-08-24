# ADR-0010: Bounded Candidate Retrieval Before Ranking

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

Ranking involves an MMR diversity pass that computes pairwise similarity across candidates, which scales poorly if run against the full repository corpus (a planning estimate of 10,000–20,000+ repositories) on every feed request.

## Decision

PostgreSQL pre-filters to a bounded candidate set of 500 to 1,000 rows — via an indexed query on topic, language, and recency, pre-sorted by a cheap heuristic like recency and stars — before any candidate reaches the ranking engine or the MMR pass.

## Alternatives considered

`DEVFEED.md` doesn't document a considered alternative (e.g., running MMR against the full corpus, or a different bound size) beyond stating the chosen bound and the reason for bounding at all. This ADR records the decision and its stated rationale rather than inventing a comparison the source material doesn't contain.

## Rationale

Running the diversity pass against tens of thousands of candidates on every request would blow the feed's performance budget. A bounded, indexed pre-filter keeps the expensive part of ranking (MMR) operating over a fixed, small-enough input regardless of how large the total corpus grows.

## Consequences

**Easier:** ranking cost per request stays roughly constant as the corpus grows, since the bound (500–1,000) doesn't scale with corpus size; the same bound underlies the position-cursor pagination approach (ADR-0009), since MMR needs to run once over a fixed candidate set to produce one deterministic ordering.

**Harder:** the pre-filter itself (topic/language/recency) determines which repositories are even eligible to be ranked for a given request — a poor pre-filter could exclude relevant repositories before ranking ever sees them, which is a correctness concern distinct from ranking quality itself.

Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture), [§12](../../DEVFEED.md#12-ranking-engine).
