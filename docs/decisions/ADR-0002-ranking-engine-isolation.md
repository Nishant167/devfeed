# ADR-0002: Ranking Engine as an Isolated, Pure Module

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

Ranking is described in `DEVFEED.md` as "the core of the product. Everything else is delivery mechanism around it." It's expected to eventually be reused across the feed, search, trending, and recommendations — surfaces that don't yet exist but are on the documented roadmap.

## Decision

`rank()` lives in `core/ranking/`, outside the API layer, as a pure function: no I/O, no framework imports (no FastAPI, SQLAlchemy, `requests`, or GitHub client). It takes candidates and a user profile as plain data and returns a ranked, explainable list. The API depends on ranking; ranking never depends on the API.

## Alternatives considered

- **Ranking logic inside API route handlers** — score candidates directly in the FastAPI request handler, using ORM models and database session objects.
- **Ranking as a database-level computation** (e.g., a complex SQL scoring query) rather than an application-level pure function.

## Rationale

A pure, dependency-free ranking function can be unit-tested exhaustively (signal correctness, weighting, MMR behavior) without spinning up a database, a web server, or the network — the highest test-coverage bar in the codebase (80%+ target) depends on this being feasible cheaply. It can also be evaluated for ranking *quality* (Precision@K, junk rate, diversity) completely independent of API concerns, and reused without duplication once search and trending eventually converge onto the same ranking pipeline (`DEVFEED.md` §14).

## Consequences

**Easier:** ranking correctness is testable in isolation; ranking logic can be shared across future surfaces without duplication; the module boundary makes "business logic in route handlers" an easy code-review violation to spot.

**Harder:** candidates and user profiles have to be marshalled into plain data structures at the API boundary before reaching ranking — an extra translation layer compared to operating directly on ORM objects.

Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture), [§12](../../DEVFEED.md#12-ranking-engine), [§25](../../DEVFEED.md#25-development-workflow).
