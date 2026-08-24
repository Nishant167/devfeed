# Component Design

> **State: Current Design.** This is the defined target repository/module layout from `DEVFEED.md` §25, not an implemented structure — none of the directories or files below exist in the repository yet. Documented here so contributors know where new code should land once implementation starts.

## Current-design repository structure

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

Source: [`DEVFEED.md` §25](../../DEVFEED.md#25-development-workflow).

## Module responsibilities

| Module | Responsibility | Constraints |
|---|---|---|
| `core/ranking/` | Scores and orders candidate repositories; produces `score_breakdown` | Pure function, no I/O. Never imports FastAPI, SQLAlchemy, `requests`, or any GitHub client. |
| `api/main.py` | FastAPI app and route registration only | No business logic in route handlers — routes call into `core/ranking/` or a thin service function. |
| `api/models.py` | SQLAlchemy ORM models | Mirrors the schema in [`database-schema.md`](../data/database-schema.md). |
| `api/schemas.py` | Pydantic request/response validation | All request validation runs through this layer at the API boundary. |
| `api/ingest.py` | GitHub ingestion pipeline | Defensive parsing throughout; never assumes a field is present. See [`github-data.md`](../data/github-data.md). |
| `api/pagination.py` | Cursor encode/decode | Encodes integer position + repository ID; never a floating-point score. See [ADR-0009](../decisions/ADR-0009-position-cursor-pagination.md). |
| `web/` | Next.js frontend | Feature-organized (`feed/`, `repository/`, `search/`), not one large `components/` directory. Built on reusable design tokens (typography, spacing, color, buttons, cards). |
| `data/taxonomy/` | Category lookup table (topic → category) | Hand-maintained, versioned; a taxonomy edit is never conflated with a ranking regression. |
| `data/eval/` | Hand-labeled ranking evaluation dataset | At least 200 labeled repositories (`good`/`meh`/`junk`) once Stage 1 begins. |
| `scripts/eval_ranking.py` | Ranking evaluation harness | The actual quality gate for ranking changes — required before any ranking change merges. |

## Engineering standards enforced by this structure

- No giant `utils.py` — if a helper doesn't clearly belong to one module, that's a signal the module boundary is wrong, not a reason to create a dumping ground.
- Placeholder implementations don't stand in for core functionality — `return []` is not an implementation of anything.
- Dependencies and infrastructure aren't introduced without a reason; simple architecture is preferred until complexity is justified by an actual, demonstrated problem.

Source: [`DEVFEED.md` §25](../../DEVFEED.md#25-development-workflow), [`CONTRIBUTING.md`](../../CONTRIBUTING.md).
