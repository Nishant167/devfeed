# Database Schema

> **State: Current Design.** No PostgreSQL instance, no Alembic migrations, and no schema exist in the repository. Everything below is the Stage 2 specification from `DEVFEED.md` §19 — decided, not implemented.

## `repositories`

The system of record for ingested GitHub data.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | `bigint` | PK | Internal ID |
| `github_id` | `bigint` | UNIQUE, NOT NULL | GitHub's own repo ID — stable across renames |
| `owner` | `text` | NOT NULL | |
| `name` | `text` | NOT NULL | |
| `full_name` | `text` | UNIQUE, NOT NULL | `owner/name`, indexed |
| `description` | `text` | NULLABLE | |
| `url` | `text` | NOT NULL | |
| `homepage` | `text` | NULLABLE | |
| `primary_language` | `text` | NULLABLE | |
| `stars` | `integer` | NOT NULL, DEFAULT 0 | |
| `forks` | `integer` | NOT NULL, DEFAULT 0 | |
| `watchers` | `integer` | NOT NULL, DEFAULT 0 | |
| `open_issues` | `integer` | NOT NULL, DEFAULT 0 | |
| `license` | `text` | NULLABLE | SPDX identifier where available |
| `is_fork` | `boolean` | NOT NULL, DEFAULT false | Hard-excluded from ranking candidates |
| `is_archived` | `boolean` | NOT NULL, DEFAULT false | Hard-excluded from ranking candidates |
| `default_branch` | `text` | NULLABLE | |
| `readme_excerpt` | `text` | NULLABLE | |
| `has_tests` | `boolean` | NULLABLE | Heuristically detected |
| `has_ci` | `boolean` | NULLABLE | `.github/workflows` presence |
| `contributor_count` | `integer` | NULLABLE | |
| `quality_score` | `numeric(4,3)` | NULLABLE | Precomputed on ingest/refresh |
| `raw_star_growth_30d` | `integer` | NULLABLE | `null` when stargazer history is unavailable |
| `star_growth_ratio_30d` | `numeric(6,4)` | NULLABLE | `raw_star_growth_30d / max(stars, 1)`, precomputed |
| `created_at_github` | `timestamptz` | NOT NULL | |
| `pushed_at_github` | `timestamptz` | NULLABLE | Primary freshness input |
| `last_synced_at` | `timestamptz` | NOT NULL | |
| `etag` | `text` | NULLABLE | For conditional requests |
| `last_modified` | `text` | NULLABLE | |
| `sync_status` | `text` | NOT NULL, DEFAULT 'pending' | `pending` / `ok` / `error` |
| `sync_error` | `text` | NULLABLE | |
| `created_at` | `timestamptz` | NOT NULL, DEFAULT now() | |
| `updated_at` | `timestamptz` | NOT NULL, DEFAULT now() | |

```sql
CREATE UNIQUE INDEX idx_repositories_github_id ON repositories(github_id);
CREATE UNIQUE INDEX idx_repositories_full_name ON repositories(full_name);
CREATE INDEX idx_repositories_primary_language ON repositories(primary_language);
CREATE INDEX idx_repositories_stars ON repositories(stars DESC);
CREATE INDEX idx_repositories_pushed_at ON repositories(pushed_at_github DESC);
CREATE INDEX idx_repositories_sync_status ON repositories(sync_status) WHERE sync_status != 'ok';
CREATE INDEX idx_repositories_last_synced ON repositories(last_synced_at DESC);
```

The last index supports the `stale_cursor` check (see [ADR-0009](../decisions/ADR-0009-position-cursor-pagination.md)) by making `MAX(last_synced_at)` cheap. No separate ingestion-run table is planned at this stage — one is only worth adding if ingestion needs its own audit trail for other reasons.

## `repository_topics` and `repository_languages`

Many-to-many join tables.

```sql
-- repository_topics
repository_id  bigint  FK -> repositories.id, NOT NULL
topic          text    NOT NULL
PRIMARY KEY (repository_id, topic);
CREATE INDEX idx_repository_topics_topic ON repository_topics(topic);

-- repository_languages
repository_id  bigint  FK -> repositories.id, NOT NULL
language       text    NOT NULL
bytes          bigint  NOT NULL, DEFAULT 0
PRIMARY KEY (repository_id, language);
```

The topic index is what's meant to power `?topics=ai,rag` filtering on the feed endpoint.

## `user_events`

Anonymous interaction tracking for Stage 3 validation.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | `bigint` | PK | |
| `session_id` | `text` | NOT NULL | Client-generated, anonymous |
| `event_type` | `text` | NOT NULL | `PROJECT_VIEW` / `PROJECT_OPEN_GITHUB` / `PROJECT_SAVE` |
| `repository_id` | `bigint` | FK → `repositories.id`, NULLABLE | Null for non-repo events |
| `metadata` | `jsonb` | NULLABLE | Small, structured, no free-text PII |
| `created_at` | `timestamptz` | NOT NULL, DEFAULT now() | |

```sql
CREATE INDEX idx_user_events_session ON user_events(session_id, created_at);
CREATE INDEX idx_user_events_type ON user_events(event_type, created_at);
```

No column here is speculative — every field maps to a metric actually defined in [`success-metrics.md`](../product/success-metrics.md).

## Migration workflow (planned)

```bash
alembic revision --autogenerate -m "add raw_star_growth_30d and star_growth_ratio_30d to repositories"
# reviewed by hand - autogenerate is a draft, not a decision
alembic upgrade head
```

Source: [`DEVFEED.md` §19](../../DEVFEED.md#19-database-architecture).
