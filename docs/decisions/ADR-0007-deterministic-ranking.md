# ADR-0007: Deterministic Ranking Before Machine Learning

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

Ranking repositories by relevance and quality is the core technical problem of the product. Machine-learning-based ranking/recommendation approaches are an obvious default for a "personalized feed" product.

## Decision

Ranking at the current stage is deterministic Python — a weighted sum of independently-normalized signals (quality, freshness, popularity, star velocity, topic relevance, novelty), followed by an MMR diversity pass — with no machine learning involved.

## Alternatives considered

- Deep-learning-based recommendation from the start (explicitly named as a non-goal for now in `DEVFEED.md` §3).
- Collaborative filtering (documented as V4 in the future recommendation-engine version table, §15) — deferred until there's enough usage data to support it.

## Rationale

Every ranked result must be able to answer "why is this here?" — a requirement that's straightforward for a weighted, explainable scoring function and much harder for an ML model without dedicated explainability work. There's also no training data yet (no usage history, no labeled preferences at scale), so an ML approach would have nothing real to learn from at this stage. Deterministic ranking can be evaluated immediately against a hand-labeled dataset (Precision@K, junk rate) without needing a model-training pipeline first.

## Consequences

**Easier:** every ranked item ships with a `score_breakdown` for free; ranking bugs are debuggable by inspecting signal values directly; the evaluation harness (Precision@K against labels) is simple to build and run on every change.

**Harder:** ranking quality is capped by how well hand-tuned weights capture actual relevance — it won't improve from user behavior the way a learned model eventually could, until later stages (V2–V5 in the recommendation roadmap) introduce content-based similarity, behavioral profiles, and collaborative filtering in sequence.

**Trigger for revisiting:** feed quality is proven and there's enough real usage/interaction data to support learned approaches — not before.

Source: [`DEVFEED.md` §3](../../DEVFEED.md#3-goals-and-non-goals), [§8](../../DEVFEED.md#8-technology-stack), [§12](../../DEVFEED.md#12-ranking-engine), [§15](../../DEVFEED.md#15-personalization-and-recommendations).
