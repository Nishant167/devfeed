# Secrets Management

> **State: Implemented (the `.gitignore` exclusion rule, below); Current Design (the fuller environment-file convention, not yet in place). No actual secrets exist yet, since nothing is deployed or implemented.**

## Rule

No secrets are ever committed to the repository — no API keys, tokens, credentials, passwords, private keys, or `.env` files containing real values. Source: `CONTRIBUTING.md`, `SECURITY.md`.

## Implemented: what's protected today

`.gitignore` already excludes environment files from version control — this is real, committed, and in effect today, not a design intention:

```
.env
.env.local
.env.*.local
.env.production
!.env.example
```

Only `.env.example`, containing placeholders only, is meant to be committed. No `.env.example` currently exists in the repository, because no code that would need configuration exists yet.

## Current Design: configuration convention (not yet in place)

```
.env.example      # committed, placeholders only
.env.local
.env.test
.env.production    # never committed
```

Configuration is intended to determine database credentials, the GitHub token, AI provider selection, embedding provider selection, and log level — always via environment variables or the project's approved secret-management mechanism, never hard-coded into application code. Source: [`DEVFEED.md` §21](../../DEVFEED.md#21-security-and-data-handling), [§25](../../DEVFEED.md#25-development-workflow).

## GitHub credentials specifically (Current Design)

The GitHub API token used for ingestion is designed to be treated as configuration, injected at runtime, never hard-coded — this applies regardless of whether ingestion runs locally (Stage 0) or on hosted infrastructure (Stage 2+). No ingestion code exists yet to verify this against. Source: `SECURITY.md`.

## If a secret is discovered committed, or a vulnerability is found

Per `SECURITY.md`: report privately, not through a public GitHub issue. Use GitHub's private vulnerability reporting if enabled on this repository; otherwise contact maintainers directly. Do not open a public issue for a security concern until it's been addressed.

## What's not yet decided

No secret-management service (e.g., a cloud secrets manager, Vault) is named anywhere in `DEVFEED.md` — the design relies on environment files at every stage described so far. Whether that changes at Stage 4+ (alongside authentication) isn't specified.
