# Testing Strategy

> **State: Implemented coverage is zero, by necessity — there is no code to test.** Everything below documents the current-design testing scope from `DEVFEED.md` §24 and `CONTRIBUTING.md` for the Stage 0–3 build; only the end-to-end section is genuinely Planned (Stage 4+, deferred until accounts exist).

## Implemented coverage

None. The repository contains no source code, so there are no unit tests, integration tests, or CI runs to report on. Any test-coverage percentage stated here would be fabricated — `DEVFEED.md`'s own standard is not to claim coverage numbers that haven't been measured, and none exist yet.

## Testing scope by module (Current Design unless marked Planned)

| Module | Test type | Bar (a target, not a measured result) | What it covers | Status |
|---|---|---|---|---|
| `core/ranking/` | Unit | Highest in the codebase — target 80%+ coverage | Signal correctness, weighting, MMR behavior, and the shape of the explainability output (`score_breakdown`). The module least allowed to regress silently. | Current Design |
| Ingestion | Integration, against recorded fixtures | Not numerically specified | Defensive parsing of missing fields, rate-limit backoff behavior. Fixtures are clearly marked as fixtures, never presented as live data. | Current Design |
| API | Contract tests | Not numerically specified | Response shapes, the error envelope, pagination cursor stability (including the position-cursor behavior — see [ADR-0009](../decisions/ADR-0009-position-cursor-pagination.md)). | Current Design |
| Database | Integration | Not numerically specified | Migration correctness and constraint behavior, exercised through integration tests rather than assumed. | Current Design |
| Frontend | Light at this stage | Not numerically specified | Grows once Stage 4 introduces more complex client state. | Current Design (Stage 2), Planned (Stage 4 growth) |
| End-to-end | Future — once accounts exist | Not designed yet | The full loop: sign up, choose interests, browse the feed, open a project, save it, ask for an explanation, browse a learning path, create a collection. | Planned — Stage 4+, explicitly deferred |

Source: [`DEVFEED.md` §24](../../DEVFEED.md#24-testing-and-evaluation).

## Ranking evaluation — distinct from unit tests

This is the actual quality gate for ranking changes, separate from and in addition to unit tests, covered fully in [`DEVFEED.md` §12](../../DEVFEED.md#12-ranking-engine):

- At least 200 hand-labeled repositories (`good`/`meh`/`junk`), sampled across the full score range, not just top results.
- An evaluation script (`scripts/eval_ranking.py`, not yet written) reports Precision@10/25/50, junk rate in the top 50, category diversity in the top 25, intra-list diversity (mean pairwise TF-IDF distance), the taxonomy version used, and the share of repositories with excluded signals.
- **Acceptance thresholds:** Precision@25 ≥ 0.50, junk rate under 10%, at least 5 categories in the top 25 — starting targets, explicitly revisable as the labeled set grows.
- No ranking change ships without running through this harness — tuning by intuition alone is not acceptable once the labeled dataset exists.

Per `CONTRIBUTING.md`: changes to the ranking algorithm itself must run through this harness before merging, in addition to unit tests.

## Implemented vs. Current Design, restated plainly

| | Implemented | Current Design (target, once Stage 0–1 code lands) |
|---|---|---|
| Unit tests | None exist | `core/ranking/` at 80%+ coverage |
| Integration tests | None exist | Ingestion fixtures, DB migration tests |
| Contract tests | None exist | API response shape, error envelope, pagination |
| Ranking evaluation harness | Does not exist | `scripts/eval_ranking.py` against a 200+ labeled dataset |
| CI enforcement | None exists (no CI workflow file in `.github/`) | Lint, type check, unit tests, integration tests, build — once there are real contributors beyond a single person (see [`git-workflow.md`](./git-workflow.md)) |
