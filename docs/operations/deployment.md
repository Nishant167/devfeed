# Deployment

> **State: Production deployment is not currently implemented.** There is no production environment, no staging environment, and no deployed instance of any DevFeed component anywhere. This documents the Current Design for the Stage 2 deployment topology from `DEVFEED.md` §22 — see also [`../architecture/deployment-architecture.md`](../architecture/deployment-architecture.md) for the architectural rationale.

## Implemented: none

Production deployment is not currently implemented. There is no hosting account, no CI/CD deployment pipeline, and no infrastructure-as-code in this repository.

## Current Design: Stage 2 production topology

```
Frontend   -> Vercel (free tier)
API        -> Fly.io or Railway (free tier)
Database   -> Neon or Supabase Postgres (free tier)
Ingestion  -> a separately scheduled job - platform scheduler or GitHub Actions cron,
              never a process riding inside the API server
```

The exact provider within each category (Fly.io vs. Railway; Neon vs. Supabase) is not finalized — see [ADR-0012](../decisions/ADR-0012-deployment-hosting-approach.md), status Proposed. No container orchestration, multi-region setup, or CDN configuration beyond hosting-platform defaults is planned.

## Current Design: local development

```
Web (Next.js) --+
                 +--> API (FastAPI) --> PostgreSQL (Docker Compose)
Ingestion -------+         ^
                     GitHub API
```

Only PostgreSQL runs in a container locally; the API and frontend run natively.

## Deployment sequencing rule

An API redeploy is designed to never affect whether ingestion runs, and the reverse should hold too — this is why ingestion is architected as its own deployment target even if hosted on the same underlying provider as the API (see [ADR-0003](../decisions/ADR-0003-ingestion-separate-deployment.md)).

## Proposed: future production infrastructure (directional sketch only)

```
Frontend → API → Application Services → PostgreSQL → Redis → Background Workers → GitHub / AI Providers
```

None of this exists, and `DEVFEED.md` is explicit that distributed architecture is not introduced ahead of a demonstrated need.

Source: [`DEVFEED.md` §22](../../DEVFEED.md#22-deployment-and-infrastructure).
