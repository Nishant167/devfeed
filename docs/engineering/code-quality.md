# Code Quality Standards

> **State: Current Design.** These are standards to build *against* — no code exists yet to measure them against, so nothing below describes verified current behavior. They come directly from `DEVFEED.md` §25 and `CONTRIBUTING.md`, not invented generic best practices.

## Module boundaries

- No business logic lives inside API route handlers — routes call into `core/ranking/` or a thin service function, nothing more.
- `core/ranking/` never imports FastAPI, SQLAlchemy, `requests`, or any GitHub client — it stays a pure, framework-independent module (see [ADR-0002](../decisions/ADR-0002-ranking-engine-isolation.md)).
- No giant `utils.py` — if a helper doesn't clearly belong to one module, that's a signal the module boundary is wrong, not a reason to create a dumping ground.

## Implementation completeness

- Placeholder implementations don't stand in for core functionality — `return []` is not an implementation of anything.
- Errors are handled explicitly and never silently swallowed.

## Dependency discipline

- Dependencies aren't introduced without a reason.
- Infrastructure isn't introduced before it solves a problem that's actually been demonstrated — simple architecture is preferred until complexity is justified by evidence, not anticipation. See [ADR-0011](../decisions/ADR-0011-rejected-technologies-current-stage.md) for concrete examples of technology explicitly held back on this principle.

## Definition of done

For production-facing work, a feature is complete when implementation, validation, error handling, tests, API contracts, migrations, logging, security, and performance have all been addressed, and documentation reflects the change. For Stage 0-style experimental work, unnecessary productionization is deliberately avoided — throwaway code stays throwaway. Source: [`DEVFEED.md` §25](../../DEVFEED.md#25-development-workflow).

## Documentation discipline

If a change affects behavior, the API, or the database schema, the corresponding section of `DEVFEED.md` — or, going forward, the relevant file under `docs/` — is updated in the same pull request. Documentation describing something the code no longer does is treated as worse than no documentation. Source: [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Architecture-change process

If a contribution changes an established architectural decision — the pagination model, the ranking signal set, the database schema, an API contract, a technology choice — the reasoning is explained in the pull-request description *before* implementing the change, not after. A one-paragraph explanation of what's changing and why is enough; this isn't a formal RFC process. Source: [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Repository content safety (applies to any code touching ingested data — Current Design, no such code exists yet)

DevFeed is designed to process content originating from public GitHub repositories, and that content must always be treated as untrusted input, once ingestion and analysis code exists:

- Contributors must not execute code obtained from repositories being ingested, analyzed, classified, or displayed.
- Parsing and analysis components must use appropriate limits for file size, processing time, and supported content types.

Source: [`CONTRIBUTING.md`](../../CONTRIBUTING.md), and see [`threat-model.md`](../security/threat-model.md) for the fuller security rationale.
