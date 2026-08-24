# GitHub Data

> **State: Current Design.** No ingestion code exists in the repository yet. This documents the specified ingestion design from `DEVFEED.md` §9 — the concrete Stage 0 build target.

## Source

GitHub's REST/Search API, authenticated with a personal access token. GitHub is treated architecturally as an unreliable external dependency, not a data source under the project's control — rate limits, partial fields, downtime, and stale data are the expected case, and ingestion code is designed to handle them defensively throughout, not as an afterthought.

## Ingestion method: query slicing

GitHub's Search API caps results at 1,000 per query, so a single query like `language:python` can't enumerate every matching repository. The planned corpus-building approach slices the search space across language, star range, and date so each individual query stays well under the cap:

- **Languages:** Python, TypeScript, Rust, Go
- **Star bands:** `50..100`, `100..250`, `250..1000`, `1000..5000`, `>5000`
- **Date ranges:** concrete calendar-month ranges across the trailing 12 months — real dates, not a symbolic placeholder

```python
query = f"language:{lang} stars:{stars} pushed:{date_range}"
# e.g. "language:python stars:250..1000 pushed:2026-07-01..2026-07-31"
```

This produces roughly 240 queries. The expected order of magnitude is 10,000–20,000 unique repositories on the first run — explicitly labeled in the source document as a sizing estimate to plan the work, not something the architecture depends on. Actual yield is meant to be measured empirically during Stage 0, not assumed in advance.

## API dependency and pagination

Ingestion is designed to paginate up to 1,000 results per sliced query, monitoring `X-RateLimit-Remaining` on every response. Authenticated access grants 5,000 requests/hour.

## Rate limits and retries

- Ingestion is designed to sleep proactively before rate-limit exhaustion, rather than reacting only after a `403`.
- Backs off with jitter on `403` and `5xx` responses, with retries.
- Every re-fetch of a known repository sends `If-None-Match` with the stored ETag; a `304 Not Modified` response means there's nothing to do, and unchanged data is never re-fetched.

## Freshness

Every repository row is designed to track `last_synced_at`, `etag`, `last_modified`, `sync_status` (`pending`/`ok`/`error`), and `sync_error`. Freshness for ranking purposes is driven by `pushed_at_github` (GitHub's own push timestamp), not by DevFeed's own sync cadence.

## Failure handling

A repository that fails to parse or fetch is designed to be marked `error` in `sync_status`, with a reason in `sync_error`, and skipped — it's designed to never abort the whole ingestion batch. GitHub API responses are treated as partial by default: every field access is meant to tolerate `null`, missing keys, and unexpected types, and nothing downstream is meant to assume `description`, `license`, `topics`, or `homepage` is present. README content and contributor/release information are designed to be fetched as a secondary step, only for repositories that survive the initial metadata-based filter, to avoid doubling the request count unnecessarily.

## Raw payload preservation

Raw API responses are designed to be stored before any transformation and never discarded — this is what would let the project re-score or re-classify repositories later without re-fetching from GitHub. Access is designed to go through a small `RawPayloadStore` interface rather than direct filesystem calls, so the backing store can change without touching ingestion logic:

```python
class RawPayloadStore(Protocol):
    def put(self, key: str, payload: bytes) -> None: ...
    def get(self, key: str) -> bytes: ...
    def exists(self, key: str) -> bool: ...
    # key convention: "github/{YYYY-MM-DD}/{search|repositories}/{identifier}.json"
```

| Stage | Implementation | Durability |
|---|---|---|
| 0 (local experimentation) | `FilesystemRawPayloadStore` → local disk | Adequate — nothing is deployed |
| 2+ (anything deployed) | Object storage (any S3-compatible option) via `ObjectStorageRawPayloadStore` | Durable across redeploys |

Local disk is planned as adequate for Stage 0 specifically because nothing is expected to survive between runs at that stage; it stops being sufficient once ingestion runs on hosted infrastructure, since free-tier platform filesystems are typically ephemeral. The specific object-storage provider isn't decided — it's deferred to when Stage 2 deployment actually happens (see [ADR-0012](../decisions/ADR-0012-deployment-hosting-approach.md)).

Source: [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion), [§10](../../DEVFEED.md#10-repository-data-model).
