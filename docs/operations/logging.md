# Logging

> **State: Current Design.** No application exists to emit logs from yet, so no logging is implemented at any level.

## Current Design — Stage 2

Structured application logs are the designed baseline — no specific logging library or log-shipping destination is named in `DEVFEED.md`. Internal errors are designed to always be logged server-side with full context, while the client only ever sees a generic error message (see [`../api/errors.md`](../api/errors.md)). Source: [`DEVFEED.md` §21](../../DEVFEED.md#21-security-and-data-handling), [§23](../../DEVFEED.md#23-observability).

## Ingestion-specific visibility

Rather than requiring log-digging to find ingestion problems, each repository row is designed to carry its own status: `sync_status` (`pending`/`ok`/`error`) and `sync_error` (a reason, when applicable). A failed repository is marked and skipped, never allowed to abort the whole ingestion batch — this is a data-model-level observability mechanism, distinct from application logs. Source: [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion), [§19](../../DEVFEED.md#19-database-architecture).

## What's not decided

No log retention period, log aggregation service, or structured-logging schema (field names, log levels policy) is specified anywhere in `DEVFEED.md`. These will need to be decided when the first component that emits logs is actually built.
