# User Flows

> **State:** Mixed — flows are labeled individually. None are implemented yet (no frontend or API code exists in the repository); Flows 1–4 are Current Design (the Stage 2 build target), Flow 5 is Planned (explicitly named future work, Stage 8).

## Flow 1 — Onboarding and topic selection *(Current Design, Stage 2)*

```
Open DevFeed → select 3–5 interests from a topic list → personalized feed
```

This is the entire personalization mechanism at Stage 2 — the feed filters and ranks against the selected topics, with no behavioral weighting yet. Source: [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination), [§15](../../DEVFEED.md#15-personalization-and-recommendations).

## Flow 2 — Discovering and receiving a ranked feed *(Current Design, Stage 2)*

```
1. Client requests GET /api/v1/feed?topics=...&cursor=...
2. PostgreSQL pre-filters to a bounded candidate set (≤1,000 rows)
3. rank() scores candidates (quality, freshness, popularity, star velocity, topic relevance, novelty)
4. MMR runs over the full candidate set for diversity
5. The requested page is returned as a slice of one deterministic ordering
```

Every returned item carries a `score_breakdown` so ranking is explainable, not a black box. Full detail in [`endpoints.md`](../api/endpoints.md) and [`DEVFEED.md` §12](../../DEVFEED.md#12-ranking-engine)–[§13](../../DEVFEED.md#13-feed-generation-and-pagination).

## Flow 3 — Exploring a repository *(Current Design, Stage 2)*

```
Card in feed → view detail (GET /api/v1/repositories/{id}) → open on GitHub or save locally
```

At Stage 2, "save" is `localStorage`-only — there is no server-side save until Stage 4 introduces accounts. Opening on GitHub and saving both emit an anonymous event (`PROJECT_OPEN_GITHUB`, `PROJECT_SAVE`) used for Stage 3 validation metrics. Source: [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination), [§20](../../DEVFEED.md#20-api-specification).

## Flow 4 — Searching directly *(Current Design, Stage 2)*

```
Query → GET /api/v1/search?q=... → PostgreSQL full-text relevance ranking (not core/ranking/)
```

Distinct code path from the feed: search results are ranked by Postgres directly, without the ranking engine or `score_breakdown`. Source: [`DEVFEED.md` §14](../../DEVFEED.md#14-search).

## Flow 5 — Learning from a project *(Planned — explicitly named future work, Stage 8, not designed beyond concept)*

```
Project → concepts → technologies → related projects → learning path → build
```

No implementation, data model, or API surface exists for this flow. The only detail available is the conceptual walk-through in [`DEVFEED.md` §17](../../DEVFEED.md#17-learning-and-knowledge-layer) (e.g., a RAG project connecting to a learning path covering embeddings, chunking, vector search, retrieval, reranking, and evaluation). This flow is included here only because the task brief asked for it — it should not be read as a near-term deliverable.

## The intended full loop *(aspirational — spans Current Design through Planned)*

```
Discover → Understand → Save → Learn → Build → Contribute → Discover again
```

DEVFEED.md is explicit that only the first half of this loop — discover, understand at a glance, save, open — belongs to the current build. Learn/Build/Contribute are future-stage concepts. Source: [`DEVFEED.md` §4](../../DEVFEED.md#4-users-and-core-experience).
