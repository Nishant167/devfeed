# Architectural Tradeoffs

> **State: Current Design.** These are documented tradeoffs behind decisions recorded as Accepted — Design Decision in the [ADRs](../decisions/README.md), not retrospectives on running code. Nothing described here has been built, deployed, or measured yet.

## Modular monolith vs. microservices

**Choice:** modular monolith, domain boundaries enforced by module structure rather than network boundaries.

**Makes easier:** single deployable to reason about, no distributed-systems failure modes (partial failures, network partitions, service discovery) to design around before there's any evidence they're needed, faster iteration during Stage 0–3.

**Makes harder:** independent scaling of any one component (e.g., ranking under heavy load) without extracting it first; a very large team would eventually hit contention on a single codebase, though that's not a near-term concern at current team size.

**Why chosen:** no component has demonstrated a need for independent scaling or deployment. See [ADR-0001](../decisions/ADR-0001-modular-monolith.md).

## Ranking engine isolated from the API vs. embedded in route handlers

**Choice:** `core/ranking/` as a pure, framework-independent module; the API calls into it.

**Makes easier:** ranking can be unit-tested without spinning up FastAPI, a database, or the network; it can be reused by feed, search, trending, and recommendations later without duplicating scoring logic; ranking correctness can be evaluated (Precision@K, junk rate) completely independent of API concerns.

**Makes harder:** an extra layer of indirection between an API request and a ranking call; changes to ranking's input shape must be coordinated with the API layer's candidate-retrieval code.

**Why chosen:** ranking is the core technical asset of the product and is expected to be shared across multiple future surfaces (search, trending, recommendations). See [ADR-0002](../decisions/ADR-0002-ranking-engine-isolation.md).

## Synchronous ranking vs. precomputed/cached ranking

**Choice:** rank synchronously in the request path against a bounded (500–1,000 row) candidate set.

**Makes easier:** always up-to-date ranking with no cache invalidation to manage, no staleness concerns, simpler system overall for the current candidate-set size.

**Makes harder:** every feed request pays the full ranking + MMR cost; this stops being viable once candidate-set size or personalization complexity grows enough to make it measurably slow.

**Why chosen:** at Stage 2 volumes and candidate-set bounds, the cost is small enough that a cache layer would be complexity without a demonstrated problem. Source: [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination).

## Position-cursor pagination vs. offset or naive score-based keyset pagination

**Choice:** a cursor encoding an integer position in one deterministic MMR-ordered pass over the full candidate set.

**Makes easier:** stable pagination even though the underlying sort key (`final_score`) is mutable (ingestion rewrites `stars`/`pushed_at`/`quality_score` regularly) and even though MMR's diversity adjustment is page-dependent (a repo's score isn't a stable property it can carry across requests).

**Makes harder:** requires computing one full ordering over the whole candidate set before any page can be sliced, rather than answering page 2 independently of page 1; needs an explicit `stale_cursor` flag and `INVALID_CURSOR` handling for the case where ingestion lands mid-session.

**Why chosen:** neither offset pagination (breaks when the corpus changes between requests) nor a naive score-keyset (breaks because the score isn't stable across pages, since MMR depends on what's already been selected) actually works for a feed that re-ranks on every request. See [ADR-0009](../decisions/ADR-0009-position-cursor-pagination.md) and [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination).

## Star velocity as excluded-and-renormalized vs. imputed-as-zero

**Choice:** when stargazer history is unavailable, the star-velocity signal is excluded from the weighted sum entirely, with remaining weights renormalized — never guessed or scored as zero.

**Makes easier:** a repository with genuinely unmeasured velocity isn't penalized relative to one with a confirmed-zero velocity; the API can honestly report `excluded_signals` rather than presenting a fabricated number as real.

**Makes harder:** the scoring function is slightly more complex (renormalization logic) than a flat weighted sum; if more than ~20% of the corpus ends up with excluded signals, that's a signal to fix ingestion coverage rather than something the scoring rule alone can fix.

**Why chosen:** zero is the minimum of a `[0,1]` signal, so substituting it would actively penalize missing data rather than treating it neutrally. Source: [`DEVFEED.md` §12](../../DEVFEED.md#12-ranking-engine).
