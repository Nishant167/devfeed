# Development Guide

> **State: Implemented fact (no application code exists); Current Design (the repository layout and local dev topology below).** This guide documents the prerequisites and current-design repository layout from `README.md` and `DEVFEED.md` §25. There is currently nothing to run, no dependencies to install, and no local environment to set up beyond a clone of this repository — Stage 0 code hasn't landed.

## Prerequisites (for when application code lands)

- Python 3.11+
- Node.js 18+
- PostgreSQL
- A GitHub personal access token, for API ingestion

Nothing needs to be installed yet for documentation-only contributions. Source: `README.md` ("Getting started").

## What contributing today actually looks like

Right now, contributing to DevFeed means working on documentation, project planning, or the Stage 0 script described in [`roadmap.md`](../product/roadmap.md) — there is no `pip install`, `npm install`, or `docker compose up` command to run, because no manifest files (`requirements.txt`, `package.json`, `docker-compose.yml`) exist in the repository yet.

## Current-design repository structure (once Stage 0 code lands)

```
core/
  ranking/            # pure - not owned by the API
api/
  main.py             # FastAPI app, route registration only
  models.py           # SQLAlchemy models
  schemas.py          # Pydantic request/response schemas
  ingest.py           # ingestion pipeline
  pagination.py       # keyset/position cursor encode-decode
web/                  # Next.js frontend, feature-organized
data/
  raw/github/         # local raw payload storage (Stage 0)
  taxonomy/           # category lookup table
  eval/               # labeled ranking dataset
scripts/
  eval_ranking.py     # ranking evaluation harness
docker-compose.yml
```

See [`component-design.md`](../architecture/component-design.md) for what each part is responsible for.

## Current-design local development topology

```
Web (Next.js) --+
                 +--> API (FastAPI) --> PostgreSQL (Docker Compose)
Ingestion -------+         ^
                     GitHub API
```

Only PostgreSQL is intended to run in a container locally — the API and frontend are meant to run natively. Source: [`DEVFEED.md` §22](../../DEVFEED.md#22-deployment-and-infrastructure).

## Environment configuration (planned convention)

```
.env.example      # committed, placeholders only
.env.local
.env.test
.env.production    # never committed
```

Configuration is intended to determine database connection, GitHub credentials, AI provider selection, embedding provider selection, and log level. None of these files currently exist in the repository. Source: [`DEVFEED.md` §25](../../DEVFEED.md#25-development-workflow).

## Commands that don't exist yet

There is no documented `run`, `test`, `lint`, or `format` command in this repository, because there is no package manifest defining them. This document will be updated with real commands the moment Stage 0 code (and its `requirements.txt`/`package.json`/lint config) lands — inventing plausible-looking commands now would misrepresent the repository's actual state.

## Database setup

No database schema is migrated anywhere yet. See [`database-schema.md`](../data/database-schema.md) for the planned schema and [`data-model.md`](../data/data-model.md) for the planned entities.

## Git workflow for contributing right now

See [`git-workflow.md`](./git-workflow.md) — this part *is* fully defined and already in effect, since it governs documentation and planning contributions too.
