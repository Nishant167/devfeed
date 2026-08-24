# Monitoring

> **State: No production monitoring is currently implemented.** Nothing is deployed, so there is nothing to monitor. Everything below is Current Design (Stage 2) or Planned (Stage 4+), not running capability.

## Current Design — Stage 2 (not implemented)

Structured application logs, a `/health` liveness endpoint, and per-repository `sync_status`/`sync_error` fields are designed to make ingestion failures visible without digging through logs. None of this exists as running infrastructure yet — see [`logging.md`](./logging.md) for the logging half of this.

## Planned — Stage 4+ (arrives only after a real incident)

Metrics, tracing, and error-tracking infrastructure are designed to arrive once the first production incident is genuinely hard to diagnose without them — explicitly not built preemptively. Once introduced, the things worth tracking:

```
github_api_requests
github_rate_limit_remaining
ingestion_success_rate
ingestion_failure_rate
feed_latency
ranking_latency
database_latency
ai_request_count
ai_failure_rate
cache_hit_rate
```

Source: [`DEVFEED.md` §23](../../DEVFEED.md#23-observability).

## Why there's no monitoring stack yet

There's no deployed system to monitor. Building metrics/tracing infrastructure ahead of any production traffic would be exactly the kind of premature infrastructure `DEVFEED.md` argues against elsewhere (see [ADR-0011](../decisions/ADR-0011-rejected-technologies-current-stage.md)) — the documented trigger is a real incident that's hard to diagnose without it, not a calendar date or a "best practice" default.
