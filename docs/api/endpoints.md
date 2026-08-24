# API Endpoints

> **State: Current Design.** No route in this document exists as running code. Everything below is the Stage 2 specification from `DEVFEED.md` §20 — decided, not deferred, and not implemented.

## `GET /api/v1/feed`

Returns a ranked, paginated list of repositories.

**Query parameters**

| Param | Type | Required | Notes |
|---|---|---|---|
| `topics` | string, comma-separated | No | e.g. `ai,rag,agents` — filters the candidate set before ranking |
| `cursor` | string | No | Opaque cursor from a previous response; omit for the first page |
| `limit` | integer | No | Default 20, max 50 |
| `session_id` | string | Yes | Anonymous client-generated ID |

**Response `200`**

```json
{
  "items": [
    {
      "id": "1234",
      "full_name": "owner/example-project",
      "description": "An AI-powered research workflow using agents and retrieval.",
      "url": "https://github.com/owner/example-project",
      "primary_language": "Python",
      "topics": ["ai", "rag", "agents"],
      "stars": 2400,
      "raw_star_growth_30d": 320,
      "star_growth_ratio_30d": 0.1333,
      "quality_score": 0.84,
      "score_breakdown": {
        "signals": {
          "quality": 0.84,
          "topic_match": 0.92,
          "freshness": 0.71,
          "popularity": 0.44,
          "star_velocity": 0.63,
          "novelty": 0.87
        },
        "excluded_signals": [],
        "base_score": 0.84,
        "diversity_adjustment": -0.03,
        "final_score": 0.81
      }
    }
  ],
  "next_cursor": "eyJpbmdlc3Rfd2F0ZXJtYXJrIjoiMjAyNi0wOC0xNVQwMjowMDowMFoiLCJwb3NpdGlvbiI6MjAsInJlcG9zaXRvcnlfaWQiOjEyMzR9",
  "has_more": true,
  "stale_cursor": false
}
```

`excluded_signals` lists any signal that couldn't be computed for this repository and was dropped from the weighted sum, with remaining weights renormalized (see [`DEVFEED.md` §12](../../DEVFEED.md#12-ranking-engine)). `stale_cursor` is `true` when an ingestion run landed between this request and the one that issued the cursor — see [ADR-0009](../decisions/ADR-0009-position-cursor-pagination.md).

Not exposed at this stage: `difficulty` has no deterministic definition yet; `category` exists internally for the evaluation harness but has no product decision yet about UI exposure.

## `GET /api/v1/repositories/{id}`

Full detail for a single repository.

```json
{
  "id": "1234",
  "full_name": "owner/example-project",
  "description": "An AI-powered research workflow using agents and retrieval.",
  "url": "https://github.com/owner/example-project",
  "homepage": null,
  "primary_language": "Python",
  "languages": [{"language": "Python", "bytes": 84210}, {"language": "Shell", "bytes": 1204}],
  "topics": ["ai", "rag", "agents"],
  "stars": 2400,
  "forks": 210,
  "license": "MIT",
  "quality_score": 0.84,
  "pushed_at_github": "2026-08-01T12:00:00Z",
  "last_synced_at": "2026-08-15T02:00:00Z"
}
```

Returns `404` with the standard error envelope (see [`errors.md`](./errors.md)) if the repository doesn't exist.

## `GET /api/v1/topics`

```json
{
  "topics": [
    {"name": "ai", "repository_count": 3210},
    {"name": "rag", "repository_count": 412},
    {"name": "data-engineering", "repository_count": 891}
  ]
}
```

## `POST /api/v1/events`

A single synchronous insert into `user_events`, returning `201` once persisted. No queue, no background processing at Stage 2 — the insert is fast because it's a single indexed write, not because anything is deferred. A failed insert fails visibly rather than being swallowed.

**Request**

```json
{
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "event_type": "PROJECT_SAVE",
  "repository_id": "1234",
  "metadata": {}
}
```

`event_type` is restricted to the Stage 3 vocabulary: `PROJECT_VIEW`, `PROJECT_OPEN_GITHUB`, `PROJECT_SAVE`. A larger vocabulary (`PROJECT_LIKE`, `PROJECT_SHARE`, `TOPIC_FOLLOW`, `USER_FOLLOW`, `SEARCH`, `AI_EXPLANATION_REQUEST`, and others) gets added only as each corresponding feature actually ships.

**Response `201`**

```json
{ "recorded": true }
```

## `GET /api/v1/search`

Full-text search over repository name, description, and topics (PostgreSQL `tsvector`, not semantic at this stage).

| Param | Type | Required |
|---|---|---|
| `q` | string | Yes |
| `cursor` | string | No |
| `limit` | integer | No |

Same item shape as `/feed`, without `score_breakdown`, since results are ranked by Postgres relevance rather than `core/ranking/` at this stage — see [ADR-0008](../decisions/ADR-0008-search-postgres-fulltext.md).

## `GET /health`

Liveness check, unauthenticated, unversioned.

```json
{ "status": "ok" }
```

## Future API surface (not built)

At Stage 4, new endpoints appear under `/api/v1/auth/*`, existing endpoints gain an optional `Authorization: Bearer <token>` header, and `session_id`-scoped saves/events migrate to `user_id` scope on login. Further out, the API is expected to grow `/api/v1/recommendations`, `/api/v1/collections`, `/api/v1/learning`, and `/api/v1/ai` — each arriving alongside the feature it serves. None of these exist today.

Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification).
