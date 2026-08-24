# Performance Requirements

> **State: Target — TBD across the board.** No performance targets are set anywhere in `DEVFEED.md`, and no benchmark has been established, because nothing is built or deployed. See [`benchmarking.md`](./benchmarking.md).

## Why there are no numbers here

Inventing latency budgets, throughput targets, or SLAs for a system with zero lines of application code would misrepresent the project's maturity. `DEVFEED.md` doesn't set numeric performance targets — its acceptance criteria are all *quality* gates (ranking precision, junk rate, category diversity — see [`../product/success-metrics.md`](../product/success-metrics.md)), not latency or throughput SLAs.

## What is documented as a performance-relevant design constraint

Even without numeric targets, several architectural choices exist specifically to bound performance risk:

| Constraint | Why it exists | Source |
|---|---|---|
| Candidate retrieval bounded to 500–1,000 rows before ranking | Running MMR diversity scoring against the full corpus (tens of thousands of rows) on every request "would blow the feed's performance budget" | [ADR-0010](../decisions/ADR-0010-bounded-candidate-retrieval.md) |
| Ranking is designed to run synchronously only "at Stage 2 volumes" | Explicitly conditional — the plan is to move to a precomputed/cached path once this is measurably too slow, not preemptively; no ranking code exists yet to be measured | [`../architecture/scalability.md`](../architecture/scalability.md) |
| GitHub authenticated rate limit: 5,000 requests/hour | A hard external constraint on ingestion throughput, not a DevFeed-chosen target | [`../data/github-data.md`](../data/github-data.md) |

## How targets will eventually be set

Once the API and ranking engine exist and are deployed (Stage 2), `DEVFEED.md`'s own logic implies latency should be measured against real candidate-set sizes rather than assumed in advance — see [`benchmarking.md`](./benchmarking.md) for how that measurement is meant to happen. Numeric NFR targets (see [`../product/product-requirements.md`](../product/product-requirements.md)) should be filled in from that measured data, not guessed now.
