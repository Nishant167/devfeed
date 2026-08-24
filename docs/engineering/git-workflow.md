# Git Workflow

> **State: Implemented (as governance process, not as application code).** `CONTRIBUTING.md`, the issue templates, and the PR template are real, committed files already in effect — this workflow governs contributions today, including this documentation itself. It is not a design decision awaiting implementation; it is the actual contribution process. The one exception is noted below: branch protection is followed by convention, not yet enforced by a technical GitHub ruleset.

## Workflow

```
Issue → branch → implementation → tests → pull request → review → CI → merge
```

Every non-trivial change starts from an issue, so the "why" is recorded before the "how." Work happens on a branch off `main`. Direct pushes to `main` aren't used — everything goes through a pull request, even small changes. Source: [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

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

Example commits: `feat: add GitHub repository ingestion`, `fix: handle GitHub rate limit backoff correctly`, `docs: update API reference for pagination cursor`. Commits stay scoped to one logical change — a commit mixing a bug fix with an unrelated refactor makes review and `git blame` harder than it needs to be.

## Pull requests

- Keep PRs focused on one thing. If review reveals an unrelated problem, open a separate issue rather than expanding the PR.
- Reference the related issue when one exists.
- Explain what changed and why — not just a restatement of the diff — and how the change was tested.
- Call out architectural implications explicitly (see [`code-quality.md`](./code-quality.md)).
- No unrelated changes bundled in — formatting-only changes to untouched files, drive-by renames, etc. belong in their own PR.
- Everything merges through review; no direct pushes to `main`.
- The [PR template](../../.github/pull_request_template.md) is applied automatically and includes a checklist covering tests, documentation, unrelated-change scope, and self-review.

## Main branch protection

`main` is the shared stable branch. Contributors should not push directly to it, force-push to it, delete it, or bypass the pull-request/review process. As of this documentation pass, these rules are enforced by team practice, not yet by a technical GitHub ruleset — `CONTRIBUTING.md` is explicit that "until these rules are technically enforced by the repository configuration, the team should follow the same workflow manually." Source: [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## CI/CD

Once there are real contributors beyond a single person, every pull request is intended to run lint, type checking, unit tests, integration tests, and a build, with dependency scanning, security checks, and deployment checks added over time. **No CI workflow file currently exists in `.github/`** (only issue and PR templates do) — this is consistent with Stage 0 deliberately not investing in elaborate CI until there's a codebase worth protecting, not an oversight. Source: [`DEVFEED.md` §25](../../DEVFEED.md#25-development-workflow).

## Issue templates in use

Three issue templates exist and are already active: [Bug report](../../.github/ISSUE_TEMPLATE/bug_report.md), [Feature request](../../.github/ISSUE_TEMPLATE/feature_request.md), and [Task](../../.github/ISSUE_TEMPLATE/task.md). The feature-request template specifically asks contributors to check whether an idea is already covered as future roadmap in `DEVFEED.md` before opening a duplicate, and to justify why it should move up the sequence rather than wait for its documented trigger.
