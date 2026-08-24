# ADR-0009: Position-Cursor Pagination Over a Deterministic Total Order

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

The feed re-ranks candidates on every request. `final_score` depends on `stars`, `pushed_at`, and `quality_score`, which ingestion rewrites regularly, and the MMR diversity pass makes a repository's score depend on what's already been selected on earlier pages — so the score isn't a stable, page-independent property of a repository at all.

## Decision

MMR runs once across the entire bounded candidate set, producing one deterministic total ordering. The feed cursor encodes an integer **position** in that ordering plus a `repository_id` — never a score, and never a floating-point value used for comparison:

```json
{ "ingest_watermark": "2026-08-15T02:00:00Z", "position": 20, "repository_id": 1234 }
```

## Alternatives considered

- **Offset-based pagination** (`OFFSET 20 LIMIT 20`) — breaks because the underlying corpus and scores change between requests, causing duplicates or skips.
- **A naive score-based keyset cursor** (`WHERE score < last_score`) — breaks for two reasons: the sort key (`final_score`) is mutable between requests, and MMR's diversity adjustment is page-dependent, so the same repository can get a different score on page 2 than it would have on page 1.

## Rationale

Encoding a position in one deterministic ordering, computed once across the whole bounded candidate set, sidesteps both failure modes: as long as no ingestion run happens between page 1 and page 2, the ordering is exactly consistent. If ingestion does land in between, the response flags `stale_cursor: true` rather than silently producing duplicates or skips, and a cursor that no longer resolves returns `INVALID_CURSOR` rather than silently restarting from page 1.

## Consequences

**Easier:** correct pagination without needing snapshot isolation; the same rule (never round ordering values used for comparison) applies consistently to search's simpler Postgres-native keyset too.

**Harder:** requires computing one full ordering over the entire candidate set (500–1,000 rows) before any page can be sliced from it, rather than answering each page's query independently; this is explicitly *not* full snapshot isolation — at Stage 2 ingestion cadence (nightly) and typical browsing-session length (minutes), the drift window is accepted as small.

**Trigger for revisiting:** ingestion frequency increasing to the point where mid-session re-ingestion becomes common — not before.

Source: [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination).
