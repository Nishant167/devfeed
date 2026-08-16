# Contributing to DevFeed

This guide covers how to work on DevFeed day to day. For what the product is and how the system is architected, read [`DEVFEED.md`](./DEVFEED.md) first — it's the source of truth, and this document assumes familiarity with it.

## Development workflow

```
Issue → branch → implementation → tests → pull request → review → CI → merge
```

Every non-trivial change starts from an issue, so the "why" is recorded before the "how." Work happens on a branch off `main`. Direct pushes to `main` aren't used — everything goes through a pull request, even small changes.

## Branch naming

```
feat/<short-description>
fix/<short-description>
refactor/<short-description>
docs/<short-description>
test/<short-description>
chore/<short-description>
```

Examples: `feat/github-ingestion`, `feat/ranking-v1`, `fix/rate-limit-backoff`, `docs/api-reference-update`, `test/ranking-eval-harness`.

## Commit conventions

```
feat:      new functionality
fix:       bug fix
refactor:  code change that doesn't alter behavior
docs:      documentation only
test:      adding or updating tests
chore:     tooling, dependencies, config
```

DevFeed-specific examples:

```
feat: add GitHub repository ingestion
feat: add repository quality scoring
feat: implement feed ranking
fix: handle GitHub rate limit backoff correctly
refactor: extract star velocity calculation from quality.py
docs: update API reference for pagination cursor
test: add ranking evaluation harness
chore: add Alembic migration tooling
```

Keep commits scoped to one logical change. A commit that mixes a bug fix with an unrelated refactor makes review and, later, `git blame`, harder than it needs to be.

## Pull requests

- Keep PRs focused on one thing. If a review comment reveals an unrelated problem, open a separate issue rather than expanding the PR.
- Reference the related issue when one exists.
- Explain what changed and why — not just a restatement of the diff.
- Explain how the change was tested.
- If the change has architectural implications (see below), call that out explicitly.
- No unrelated changes bundled in — formatting-only changes to untouched files, drive-by renames, etc. belong in their own PR.
- Everything is merged through review. No direct pushes to `main`.

## Main Branch Protection

`main` is the shared stable branch for the project.

Contributors should not push directly to `main`. All changes should be developed on a separate branch and submitted through a Pull Request.

The repository's GitHub ruleset is intended to protect `main` by requiring Pull Requests and preventing destructive operations such as force-pushing or deleting the branch.

Until these rules are technically enforced by the repository configuration, the team should follow the same workflow manually.

### Main branch rules

- Do not push directly to `main`.
- Do not force-push to `main`.
- Do not delete `main`.
- Do not bypass the Pull Request and review process.
- Merge changes into `main` only after the required review and validation is complete.

Use the [pull request template](.github/pull_request_template.md) — it's applied automatically.

## Code quality

- No business logic inside API route handlers — routes call into `core/ranking/` or a thin service function, nothing more.
- `core/ranking/` never imports FastAPI, SQLAlchemy, `requests`, or any GitHub client — it stays a pure, framework-independent module.
- No placeholder implementations for core functionality. `return []` is not an implementation.
- Errors are handled explicitly and never silently swallowed.
- No giant `utils.py` — if a helper doesn't clearly belong to one module, that's a sign the module boundary is wrong.
- Don't introduce a dependency or a piece of infrastructure without a reason. Simple architecture is preferred until complexity is justified by a demonstrated problem, not anticipated ahead of time.

Full engineering standards are in [`DEVFEED.md` §25](./DEVFEED.md#25-development-workflow).

## Testing

New functionality should include tests appropriate to what it touches:

- Changes to `core/ranking/` need tests covering signal correctness, weighting, and MMR behavior — this module carries the highest coverage bar in the codebase (target 80%+).
- Ingestion changes need integration tests against recorded fixtures, clearly marked as fixtures.
- API changes need contract tests covering response shape, the error envelope, and pagination behavior.
- Changes to the ranking algorithm itself must be run through the evaluation harness (`scripts/eval_ranking.py`) against the labeled dataset before merging — this is separate from and in addition to unit tests.

Full testing scope is in [`DEVFEED.md` §24](./DEVFEED.md#24-testing-and-evaluation).

## Architecture changes

If a contribution changes an established architectural decision — the pagination model, the ranking signal set, the database schema, an API contract, a technology choice — explain the reasoning in the PR description before implementing the change, not after. A one-paragraph explanation of what's changing and why is enough; this isn't a formal proposal process.

## Documentation

If a change affects behavior, the API, or the database schema, update the corresponding section of `DEVFEED.md` in the same PR. Documentation that describes something the code no longer does is worse than no documentation.

## Security

Never commit secrets or credentials to the repository, including:

- GitHub tokens
- API keys
- Database credentials
- Passwords
- Private keys
- `.env` files containing secrets
- Production configuration containing sensitive values

Use environment variables or the project's approved secret-management mechanism instead.

If you discover a security vulnerability, do not disclose sensitive details in a public GitHub issue. Follow the process described in [`SECURITY.md`](./SECURITY.md).

## Repository Content Safety

DevFeed processes content originating from public GitHub repositories. Repository content must always be treated as untrusted input.

Contributors must not execute code obtained from repositories being ingested, analysed, classified, or displayed by DevFeed.

Parsing and analysis components must use appropriate limits for file size, processing time, and supported content types.


