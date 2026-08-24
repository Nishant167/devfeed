# Benchmarking

> **State: Benchmark not yet established.** No code exists to benchmark. Everything below is Current Design (methodology for how performance will eventually be measured), not results.

## What exists instead: a ranking *quality* evaluation harness (not a performance benchmark)

`DEVFEED.md` §12 defines a rigorous evaluation methodology for ranking, but it measures ranking *quality* (precision, junk rate, diversity), not latency or throughput. It's worth distinguishing clearly, since the two are easy to conflate:

| | Ranking evaluation (`scripts/eval_ranking.py`, not yet written) | Performance benchmark |
|---|---|---|
| Measures | Precision@10/25/50, junk rate, category diversity, intra-list diversity, against a 200+ hand-labeled dataset | Latency, throughput, resource usage |
| Exists today | No — script not written, dataset not labeled | No — nothing to benchmark |
| Required before | Any ranking algorithm change ships | Not specified as a merge gate anywhere |

## How performance should eventually be measured (method, not results)

Once the API and ingestion pipeline exist and are deployed, a real benchmark would need to measure, at minimum:

- Feed request latency at realistic candidate-set sizes (500–1,000 rows, per the bounded-retrieval design — see [ADR-0010](../decisions/ADR-0010-bounded-candidate-retrieval.md)).
- Ranking + MMR computation time in isolation, since `core/ranking/` is a pure function that can be benchmarked without the API or database in the loop.
- Ingestion throughput against GitHub's 5,000 requests/hour authenticated rate limit, and how close the ~240-query slicing strategy comes to that ceiling on a full run.
- Database query latency for the candidate pre-filter (indexed on topic/language/recency).

None of this has been run. Any specific number presented here would be fabricated.

## What not to do

Do not report percentile latencies, requests-per-second figures, or "handles N concurrent users" claims for DevFeed anywhere until they've actually been measured against deployed infrastructure under realistic load. `DEVFEED.md` itself never makes such claims, and this documentation set follows the same discipline.
