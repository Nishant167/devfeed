# ADR-0012: Deployment Approach — Free-Tier Hosting Split Across Frontend/API/Database

## Status

Proposed *(the overall split-by-concern approach is a design decision in `DEVFEED.md`; the specific provider within each category is explicitly left open, and no deployment of any kind exists in the repository)*

## Context

DevFeed needs a deployed Stage 2 target with a ₹0 initial infrastructure budget, split across a frontend, an API, a database, and a separately-scheduled ingestion job (see ADR-0003).

## Decision

Split hosting across free tiers by concern: frontend on Vercel, API on Fly.io *or* Railway, database on Neon *or* Supabase Postgres, and ingestion as a separately scheduled job (the hosting platform's scheduler or GitHub Actions cron) — never a process riding inside the API server.

## Alternatives considered

- A single combined hosting provider running frontend, API, and database together.
- Self-hosting on a VPS instead of managed free-tier platforms.

`DEVFEED.md` doesn't document a detailed comparison between these and the chosen split — it states the intended split and the reasoning (budget, and keeping ingestion independent) directly.

## Rationale

The ₹0 budget goal rules out paid infrastructure until the product proves demand. Splitting by concern (frontend / API / database / ingestion) rather than one combined host keeps each piece swappable independently — infrastructure providers are treated as configuration, not something baked into application code, so moving from Neon to a different Postgres host later shouldn't touch business logic.

## Open sub-decision

The exact provider within each category (Fly.io vs. Railway for the API; Neon vs. Supabase for Postgres) is explicitly **not yet decided** in `DEVFEED.md` — both options are presented as acceptable, and the specific pick is deferred to when Stage 2 deployment actually happens. Similarly, the object storage provider behind the `RawPayloadStore` interface (any S3-compatible option) is unpicked until deployment happens. This ADR's status is `Proposed` rather than `Accepted` specifically because of this open point.

## Consequences

**Easier:** each layer can be swapped without touching application code, since the interfaces are already designed provider-independently (e.g., `RawPayloadStore`); staying on free tiers keeps costs at zero until there's real demand.

**Harder:** free-tier platforms come with their own operational quirks (cold starts, ephemeral filesystems — the reason raw payloads move to object storage at Stage 2+ rather than staying on local disk) that need to be worked around rather than assumed away.

Source: [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion), [§22](../../DEVFEED.md#22-deployment-and-infrastructure).
