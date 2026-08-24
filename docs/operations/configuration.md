# Configuration

> **State: Current Design.** No configuration files exist yet; this is the specified environment-file convention for the Stage 0–2 build, not deferred future work.

## Current Design: environment file layout

```
.env.example      # committed, placeholders only
.env.local
.env.test
.env.production    # never committed
```

None of these files currently exist in the repository. Once introduced, `.gitignore` already excludes the non-example variants from version control (see [`../security/secrets-management.md`](../security/secrets-management.md)).

## What configuration is intended to control

- Database connection string
- GitHub API credentials (personal access token for ingestion)
- AI provider selection (future — no provider is chosen yet, since nothing depends on one)
- Embedding provider selection (future)
- Log level

Source: [`DEVFEED.md` §25](../../DEVFEED.md#25-development-workflow).

## Design principle

Infrastructure providers are treated as configuration, not something baked into application code — swapping a Postgres host, hosting platform, or object-storage provider later is designed to be a configuration change, not a code change. This is why interfaces like `RawPayloadStore` are designed provider-independently from the start (see [`../data/github-data.md`](../data/github-data.md)). Source: [`DEVFEED.md` §22](../../DEVFEED.md#22-deployment-and-infrastructure).

## What's not yet decided

No configuration schema, validation approach, or secrets-injection mechanism (beyond "environment variables") is specified. This will need to be defined when Stage 0/2 code actually introduces its first configurable component.
