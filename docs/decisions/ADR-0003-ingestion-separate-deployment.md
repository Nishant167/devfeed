# ADR-0003: Ingestion as a Separate Deployment Target from the API

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

GitHub ingestion needs to run on a schedule (nightly at Stage 2), independent of when the API is redeployed. A common shortcut is to run ingestion as a cron job or background thread riding inside the same process as the API server.

## Decision

Ingestion runs as its own scheduled job — the hosting platform's scheduler or a GitHub Actions cron trigger — never as a background process inside the API server. It's a distinct deployment target even if it happens to run on the same underlying hosting provider as the API.

## Alternatives considered

- **A cron process or background thread inside the API server**, redeployed alongside API changes.
- **A single combined "backend" deployment** covering both request-serving and scheduled ingestion.

## Rationale

An API redeploy should never silently affect whether ingestion runs, and the reverse should hold too — the two have genuinely different failure domains (a bad API deploy shouldn't stop the corpus from updating; a stuck ingestion run shouldn't take down feed requests) and different cadences (continuous request-serving vs. a nightly batch job).

## Consequences

**Easier:** ingestion failures are isolated and visible (via `sync_status`/`sync_error` per repository) without needing to correlate them with API deploy history; the API can be redeployed freely without touching the ingestion schedule.

**Harder:** requires the hosting setup to support two independently deployable/schedulable targets rather than one, which is marginally more operational surface area for a small team at Stage 2.

Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture), [§9](../../DEVFEED.md#9-github-ingestion), [§22](../../DEVFEED.md#22-deployment-and-infrastructure).
