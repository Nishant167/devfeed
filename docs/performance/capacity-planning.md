# Capacity Planning

> **State: Proposed target (an estimate for planning purposes, explicitly not measured).** `DEVFEED.md` is careful to label its own corpus-size figure as a sizing estimate, not an architectural dependency — this document preserves that distinction.

## Expected corpus size (planning estimate, not measured)

The ingestion query strategy slices across 4 languages × 5 star bands × 12 monthly date ranges, producing roughly 240 queries. The expected order of magnitude is **10,000–20,000 unique repositories on the first run** — `DEVFEED.md` explicitly frames this as "a planning estimate to size the work, not something the architecture depends on." Actual yield is meant to be measured empirically during Stage 0, not assumed. Source: [`../data/github-data.md`](../data/github-data.md).

## The hard external constraint: GitHub's rate limit

Authenticated GitHub API access is capped at 5,000 requests/hour. This is an external ceiling on ingestion throughput that DevFeed doesn't control and must design around (conditional requests, proactive backoff) rather than a capacity figure DevFeed can plan past. See [`../api/rate-limits.md`](../api/rate-limits.md).

## The capacity lever that matters most: bounded candidate retrieval

Regardless of how large the total corpus grows (thousands or eventually tens of thousands of repositories), the ranking engine only ever operates on a pre-filtered candidate set of 500–1,000 rows per request. This is the primary reason feed-serving capacity is designed to not scale linearly with corpus size — see [ADR-0010](../decisions/ADR-0010-bounded-candidate-retrieval.md).

## Stage-gated capacity targets (quality gates, not load targets)

The closest thing to a "capacity" target in the current build is qualitative, not a load figure: Stage 2's gate requires "200+ browsable repositories" live in the deployed feed. This is a product-completeness bar, not a performance or scale benchmark. Source: [`../product/success-metrics.md`](../product/success-metrics.md).

## What's genuinely undefined — neither Current Design nor Planned

No capacity plan exists for concurrent user load, database connection pooling, or ingestion frequency beyond "nightly" at Stage 2. These become relevant once there's a deployed system generating real traffic to plan around — currently there's none, and `DEVFEED.md` doesn't specify targets for any of them even at the design level.
