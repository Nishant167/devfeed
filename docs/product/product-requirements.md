# Product Requirements

> **State: Current Design.** These requirements describe the Stage 0–3 build target documented in `DEVFEED.md` — a defined target, not deferred future work, and not implemented in the repository yet. See [`roadmap.md`](./roadmap.md).

## Functional requirements

| Requirement | Target stage | Status | Source |
|---|---|---|---|
| Ingest GitHub repositories across language, star-band, and date-range slices | Stage 0 | Current Design | [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion) |
| Filter out junk repositories (tutorials, awesome-lists, dead forks, etc.) before ranking | Stage 0 | Current Design | [`DEVFEED.md` §11](../../DEVFEED.md#11-repository-quality-and-classification) |
| Score repositories deterministically on quality, freshness, popularity, star velocity, topic relevance, and novelty | Stage 0–1 | Current Design | [`DEVFEED.md` §12](../../DEVFEED.md#12-ranking-engine) |
| Serve a ranked, paginated feed filtered by selected topics | Stage 2 | Current Design | [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination), [`endpoints.md`](../api/endpoints.md) |
| Let a user select 3–5 topic interests at onboarding | Stage 2 | Current Design | [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination) |
| Full-text search over repository name, description, and topics | Stage 2 | Current Design | [`DEVFEED.md` §14](../../DEVFEED.md#14-search) |
| Save a repository locally (no account required) | Stage 2 | Current Design | [`DEVFEED.md` §13](../../DEVFEED.md#13-feed-generation-and-pagination) |
| Record anonymous view/open/save events for validation | Stage 2–3 | Current Design | [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification) |

None of the above is implemented — "Current Design" here means decided and specified for the near-term build, not deferred future work and not running code.

Functionality outside the Stage 0–3 build — behavioral personalization, recommendations, AI project explanation, learning paths, collections, social features — is described in [`DEVFEED.md` §15–18](../../DEVFEED.md#15-personalization-and-recommendations) and is explicitly Planned future work, not part of these requirements.

## Non-functional requirements

DevFeed has not been implemented, deployed, or load-tested, so none of the figures below are measured targets — they are stated as **TBD**, with a note on how each will eventually be established. Inventing numbers here would misrepresent a documentation-stage project as having done performance work it hasn't done.

| Category | Status | How it will eventually be measured |
|---|---|---|
| **Latency** | TBD | Once the API exists, feed and search request latency under real candidate-set sizes (500–1,000 rows pre-filtered) will be measured directly, not estimated in advance. |
| **Reliability** | TBD | No uptime target exists because nothing is deployed. The one hard architectural commitment today is that GitHub API failures must not take down the feed — see the failure-mode table in [`architecture-overview.md`](../architecture/architecture-overview.md). |
| **Scalability** | Not yet applicable | The architecture bounds ranking to 500–1,000 pre-filtered candidates per request specifically so it doesn't need to scale against the full corpus (see [`scalability.md`](../architecture/scalability.md)). Real scale questions are deferred until Stage 4+ triggers in [`DEVFEED.md` §26](../../DEVFEED.md#26-milestones-and-gates) are hit. |
| **Maintainability** | Current Design | Concrete engineering standards exist (module boundaries, no business logic in route handlers, no placeholder implementations) — see [`code-quality.md`](../engineering/code-quality.md). These are standards to build against, not evidence about existing code, because there is no code yet. |
| **Security** | Current Design | Concrete rules exist (never execute repository code, never commit secrets, repository content is always untrusted) — see [`security-architecture.md`](../security/security-architecture.md). Same caveat: rules to build against, not implemented controls. |
| **Data freshness** | Current Design | Ingestion is designed to run nightly at Stage 2 via conditional requests (`If-None-Match`/ETag) against the GitHub API. No ingestion job currently runs against any environment. See [`github-data.md`](../data/github-data.md). |

## What "done" looks like at each current stage

Rather than fixed NFR numbers, the project uses stage gates as its acceptance criteria — a repository-ranking quality bar for Stage 0–1, and usage-behavior thresholds for Stage 2–3. These are documented in full in [`success-metrics.md`](./success-metrics.md) and [`DEVFEED.md` §5](../../DEVFEED.md#5-development-strategy)/[§26](../../DEVFEED.md#26-milestones-and-gates).
