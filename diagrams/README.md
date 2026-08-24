# Diagrams

Standalone Mermaid source files for the diagrams referenced throughout `docs/`. All of them describe **planned** architecture — none of the systems shown are deployed or implemented yet. Each file notes its source section in `DEVFEED.md`.

| File | Shows | Referenced from |
|---|---|---|
| [`system-context.mmd`](./system-context.mmd) | External actors and the system boundary | [`docs/architecture/system-context.md`](../docs/architecture/system-context.md) |
| [`architecture-overview.mmd`](./architecture-overview.mmd) | Full ingestion → ranking → API → web pipeline | [`docs/architecture/architecture-overview.md`](../docs/architecture/architecture-overview.md) |
| [`ingestion-flow.mmd`](./ingestion-flow.mmd) | GitHub query → conditional fetch → raw storage flow | [`docs/data/github-data.md`](../docs/data/github-data.md) |
| [`ranking-pipeline.mmd`](./ranking-pipeline.mmd) | Candidate retrieval → scoring → MMR → pagination | [`docs/architecture/data-flow.md`](../docs/architecture/data-flow.md), [`docs/decisions/ADR-0009`](../docs/decisions/ADR-0009-position-cursor-pagination.md) |
| [`database-erd.mmd`](./database-erd.mmd) | Planned entity relationships, current and future-stage tables | [`docs/data/data-model.md`](../docs/data/data-model.md) |
| [`deployment-topology.mmd`](./deployment-topology.mmd) | Planned Stage 2 hosting split | [`docs/architecture/deployment-architecture.md`](../docs/architecture/deployment-architecture.md), [`docs/operations/deployment.md`](../docs/operations/deployment.md) |

To render any of these, paste the file contents into a Mermaid-compatible renderer (GitHub itself renders `.mmd`-style code blocks embedded in Markdown automatically; these standalone files are provided for reuse in other tooling, such as diagram-editing apps or documentation generators, without extracting them from prose each time).
