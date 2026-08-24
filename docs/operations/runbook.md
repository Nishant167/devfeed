# Runbook

> **State: Proposed.** There is no deployed system, so there is no real runbook yet, and — unlike monitoring or logging — `DEVFEED.md` doesn't name a runbook as a deliverable at any stage. This document is this documentation set's own outline of scenarios worth having runbook entries for, built by cross-referencing the failure-handling behavior specified elsewhere in `DEVFEED.md`. It is not an actual incident-response procedure, and it shouldn't be read as carrying the same weight as a Current Design or Planned item that `DEVFEED.md` itself defines.

## Why this is thin today

A runbook describes how to respond to real operational incidents in a running system. Nothing is running, and nothing is implemented. Writing detailed step-by-step incident procedures now would describe operations against infrastructure that doesn't exist — this document instead lists the scenarios `DEVFEED.md`'s design already anticipates, so they aren't forgotten once deployment happens.

## Scenarios the design specifies handling for (Current Design; need real runbook entries once implemented and deployed)

| Scenario | What the design specifies (not yet implemented) | What still needs a human runbook entry |
|---|---|---|
| GitHub API rate limit exhausted mid-ingestion | Ingestion is designed to sleep proactively before exhaustion and back off with jitter on `403`/`5xx` | Confirming ingestion actually recovered on the next scheduled run; no documented manual-intervention procedure yet |
| A single repository fails to parse or fetch | Designed to be marked `sync_status: error` with a reason, skipped, batch continues | A documented process for triaging accumulated `error` rows doesn't exist yet |
| Ingestion runs mid-user-session (feed cursor goes stale) | API designed to return `stale_cursor: true`; a fully-invalid cursor designed to return `INVALID_CURSOR` | No runbook for verifying this behavior in production once deployed |
| PostgreSQL becomes unavailable | Full outage — explicitly the one dependency the system is designed to be unable to degrade around | No documented recovery procedure — see the gap noted in [`backup-recovery.md`](./backup-recovery.md) |
| AI provider unavailable (future, Stage 7+) | Explainer/summary features designed to degrade gracefully; feed/search/saves designed to be unaffected | Not applicable yet — feature doesn't exist |

## What this document is not

This is not a substitute for real, tested runbook procedures once Stage 2 ships. It exists to record that the underlying architecture already anticipates several failure modes at the design level (see the failure-mode table in [`../architecture/architecture-overview.md`](../architecture/architecture-overview.md)), and to flag that operational procedures for a human to follow during an actual incident still need to be written once there's an actual incident-capable system.

Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture), [§9](../../DEVFEED.md#9-github-ingestion), [§13](../../DEVFEED.md#13-feed-generation-and-pagination).
