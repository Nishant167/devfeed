# Data Retention

> **State: Mostly undefined — neither Current Design nor Planned.** `DEVFEED.md` does not specify a retention or deletion policy for most data, and this is not simply an unimplemented design — no design exists yet either. This document says so explicitly rather than inventing numbers or timelines the source material doesn't contain.

## What is documented

| Data | Retention behavior | Source |
|---|---|---|
| Raw GitHub API payloads | Never discarded — stored before transformation specifically so the project can re-score or re-classify later without re-fetching from GitHub | [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion) |
| Repository records (`repositories` table) | Updated in place on re-sync (`updated_at` bumped); no deletion policy is described for repositories that go archived, are deleted upstream on GitHub, or stop appearing in query results | Not specified |
| `user_events` | No retention period, aggregation, or deletion schedule is described | Not specified |
| `.env.local` / `.env.production` | Never committed to version control (see [`secrets-management.md`](../security/secrets-management.md)) — this is a handling rule, not a retention period | [`DEVFEED.md` §22](../../DEVFEED.md#22-deployment-and-infrastructure), [`.gitignore`](../../.gitignore) |

## What is not established

`DEVFEED.md` does not define:

- A retention period or deletion schedule for `user_events` (anonymous interaction data).
- Whether or how repository rows are removed if a repository is deleted, made private, or transferred on GitHub.
- A backup retention window for the database itself (see [`backup-recovery.md`](../operations/backup-recovery.md), which is similarly undefined).
- Any data-subject deletion request process — reasonable, since Stage 2 collects no personal information tied to an identifiable person (only an anonymous `session_id`), but worth noting as an open question once Stage 4 accounts exist.

These gaps are worth resolving before Stage 4 introduces accounts and real user data, since retention questions become materially more consequential once personal information is involved. They are listed here as open items, not as decisions already made.

Source: [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion), [§21](../../DEVFEED.md#21-security-and-data-handling).
