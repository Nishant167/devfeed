# Dependency Management

> **State: Implemented fact (no dependencies exist); Current Design (the principles that will govern them).** There is no `requirements.txt`, `pyproject.toml`, or `package.json` in the repository — nothing has been installed or pinned. This documents the stated principles that will govern dependencies once code lands.

## Guiding principle

Don't introduce a dependency without a reason, and don't introduce infrastructure before it solves a demonstrated problem. This is stated repeatedly across `DEVFEED.md` §25 and `CONTRIBUTING.md`'s code-quality section, and is the reasoning behind [ADR-0011](../decisions/ADR-0011-rejected-technologies-current-stage.md) (Kafka, a dedicated vector database, GraphQL, Kubernetes, Redis/Celery, and Elasticsearch/OpenSearch are all explicitly held back until their named trigger).

## Expected ecosystems (from `.gitignore`, not yet from actual manifests)

The repository's `.gitignore` anticipates two dependency ecosystems, even though neither has a manifest file yet:

- **Python/FastAPI backend** — ignores `__pycache__/`, `*.egg-info/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, virtual environment directories (`venv/`, `.venv/`, `env/`). The presence of `.ruff_cache/` suggests `ruff` is the intended lint/format tool, though this isn't stated anywhere in prose — it's an inference from tooling cache patterns, not a documented decision.
- **Node.js/Next.js/TypeScript frontend** — ignores `node_modules/`, `.next/`, `out/`, `dist/`, `build/`, `.turbo/`, `next-env.d.ts`.

## Security requirements for dependencies

From `SECURITY.md`: keep dependencies current, avoid adding a new one without a reason, and flag any dependency with a known vulnerability in its currently pinned version. No dependency-scanning tooling (e.g., Dependabot, `pip-audit`, `npm audit` in CI) is configured yet — this is listed in `DEVFEED.md` §25 as something CI grows into over time, not as an existing control.

## What's not yet decided

- Exact package versions/pins for FastAPI, Pydantic, SQLAlchemy, Alembic, Next.js, React, or Tailwind — `DEVFEED.md` names the technologies (see [ADR-0004](../decisions/ADR-0004-backend-framework.md) and [ADR-0005](../decisions/ADR-0005-frontend-framework.md)) but not specific version numbers.
- The lint/format toolchain isn't documented in prose anywhere, only implied by `.gitignore` cache directories.
- Any automated dependency-update or vulnerability-scanning tool.

These will need to be decided when Stage 0 code actually begins, not inferred or invented here.
