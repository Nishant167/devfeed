# Success Metrics

> **State: Current Design.** These are defined gate criteria, not yet measured — no ingestion, ranking, or product usage exists yet to measure against them.

DEVFEED.md doesn't define success as a set of ongoing KPIs from day one. It defines success as a sequence of **stage gates** — each stage has a concrete, falsifiable pass condition, and nothing past it gets built until the gate is cleared. This is the actual metrics framework in the repository; nothing below is invented.

## Stage gates (defined)

| Stage | Metric | Threshold |
|---|---|---|
| 0 — Scroll Test | Repos worth clicking, out of 100 | ≥ 15 |
| 0 — Scroll Test | Previously-unknown, genuinely interesting repos | ≥ 3 |
| 0 — Scroll Test | Obvious junk in top 100 | < 20 |
| 1 — Ranking Engine | Precision@25 against hand-labeled set | ≥ 0.50 |
| 1 — Ranking Engine | Junk rate in top 50 | < 10% |
| 1 — Ranking Engine | Distinct categories in top 25 | ≥ 5 |
| 2 — Public Product | Browsable repositories live | ≥ 200 |
| 2 — Public Product | Personal daily use | 5 consecutive days |
| 3 — User Validation | Repository opens per session | ≥ 2 |
| 3 — User Validation | Save rate | ≥ 5% |
| 3 — User Validation | Day-7 return rate | ≥ 30% |

Source: [`DEVFEED.md` §5](../../DEVFEED.md#5-development-strategy), [§26](../../DEVFEED.md#26-milestones-and-gates). Full stage-by-stage roadmap in [`roadmap.md`](./roadmap.md).

## Kill criteria (defined in advance, deliberately)

These exist so a failing signal can't be argued away once code has already been written:

- If Stage 0 fails after a real week of iterating on ranking heuristics, the problem is the corpus or filtering approach — narrow the domain before writing more code.
- If repository opens per session stay below ~2 after several ranking revisions, the ranking approach isn't working — consider search-first instead of feed-first.
- If there are no meaningful returning users by the end of Stage 3, the product may be useful without being habitual — see the Stage 3 pivot in [`roadmap.md`](./roadmap.md).
- If active personal use of the product stops for two weeks, that's real product evidence and doesn't get overridden just because code already exists.

Source: [`DEVFEED.md` §2](../../DEVFEED.md#2-vision-and-problem).

## Metrics explicitly not being optimized for

Session length / time-in-app is explicitly named as **not** an optimization target at any stage. The stated target is useful discoveries per session, not engagement time. Source: [`DEVFEED.md` §2](../../DEVFEED.md#2-vision-and-problem), [§23](../../DEVFEED.md#23-observability).

## Planned future metrics (Stage 3+, explicitly named as future scope in `DEVFEED.md` §23)

Once real usage data exists (Stage 3+), `DEVFEED.md` §23 sketches a fuller analytics scope — discovery metrics (views, opens, unique discoveries/session), retention metrics (WAU/MAU, returning users), and, once recommendations exist, offline evaluation metrics (Precision@K, Recall@K, NDCG@K, diversity, novelty, coverage). These are **Planned** rather than Current Design because `DEVFEED.md` itself labels this section "future, full scope" — they are documented intent, not yet collected, and not yet wired to any actual event pipeline beyond the three Stage 3 event types (`PROJECT_VIEW`, `PROJECT_OPEN_GITHUB`, `PROJECT_SAVE`).
