# Alerting

> **State: Implemented — none. Proposed — everything below.** Alerting is not named anywhere in `DEVFEED.md` as its own deliverable, unlike monitoring metrics (which are explicitly Planned, Stage 4+). So this document's content is this documentation set's own reasonable inference about what will eventually be needed, not a decision `DEVFEED.md` itself has made — it should carry less weight than a Current Design or Planned label would.

## Implemented: none

No alerting exists. There's nothing deployed to alert on.

## Proposed: what would need to happen first

Per `DEVFEED.md` §26, structured logging, metrics, and health checks — the prerequisites for any real alerting — are Planned to be introduced "once the first production incident that was hard to diagnose without them" occurs. Alerting itself isn't named as a separate deliverable anywhere in `DEVFEED.md`; it would logically follow once the metrics listed in [`monitoring.md`](./monitoring.md) exist, but no alerting thresholds, on-call process, or notification channel is specified anywhere in the source document.

## What this means in practice

Until Stage 4+, the only "alerting" mechanism that exists at all is the `/health` liveness endpoint (Current Design, not implemented) and the per-repository `sync_status`/`sync_error` fields (also Current Design), both of which would require someone to actively check them — there is no push-based notification of any kind designed into the current build.

Source: [`DEVFEED.md` §23](../../DEVFEED.md#23-observability), [§26](../../DEVFEED.md#26-milestones-and-gates).
