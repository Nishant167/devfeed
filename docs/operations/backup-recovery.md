# Backup and Recovery

> **State: Not established — neither Current Design nor Planned.** `DEVFEED.md` does not define a backup or disaster-recovery policy at all, for any stage. This document says so plainly rather than inventing one.

## What is documented

- **PostgreSQL is the one dependency the system cannot degrade around.** Per the failure-mode table in [`../architecture/architecture-overview.md`](../architecture/architecture-overview.md), a PostgreSQL outage is a full outage — there's no fallback path, unlike GitHub API failures (served stale) or AI provider failures (feature degrades gracefully). This makes database durability and recoverability materially important, even though no concrete backup mechanism is specified.
- **Raw GitHub payloads are designed to be preserved and never discarded**, specifically so the project can re-derive/re-score repository data without re-fetching from GitHub — this is the closest thing to a recovery mechanism that DEVFEED.md describes, and it covers ingested raw data, not the processed database itself. No ingestion code exists yet to actually do this.
- **Proposed hosting providers** (Neon or Supabase for Postgres, per [ADR-0012](../decisions/ADR-0012-deployment-hosting-approach.md), status Proposed) typically offer their own managed backup features, but `DEVFEED.md` doesn't specify relying on, configuring, or testing them — this would need to be a deliberate decision made at Stage 2 deployment time, not something to assume comes free.

## What is not established

- No backup frequency, retention window, or restore-testing process is defined for the PostgreSQL database.
- No disaster-recovery runbook or RTO/RPO targets exist.
- No policy exists for recovering from a corrupted or lost `repositories` table beyond re-running ingestion from scratch (which is possible in principle, given raw payload preservation, but not documented as a tested recovery procedure).

## Recommendation for when this becomes relevant

This should be defined no later than Stage 2, when a real deployed database with real (even if anonymous) event data first exists — currently there's nothing deployed, so there's nothing to back up, but that changes as soon as Stage 2 ships.
