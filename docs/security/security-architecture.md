# Security Architecture

> **State: Current Design.** Rules are defined, but no implementation exists yet to enforce them — no code, no deployed service, no ingestion job. This documents the security posture `DEVFEED.md` and `SECURITY.md` commit to building toward. None of the controls described below should be read as currently operating.

## Repository content is always untrusted input

Every ingested GitHub repository is treated as untrusted, at every stage:

- Repository code is never executed — no dependency installs, no build scripts, no binaries, no `docker build`, under any circumstance, at any stage.
- Any future parsing (README analysis, codebase understanding — Stage 7+) is designed to be sandboxed, with file size limits, parser timeouts, memory limits, and path traversal protection.
- This rule applies regardless of how confident an analysis pipeline is that a given repository looks safe.

Source: [`DEVFEED.md` §16](../../DEVFEED.md#16-ai-project-intelligence), [§21](../../DEVFEED.md#21-security-and-data-handling), `SECURITY.md`.

## GitHub API compliance

Ingestion is designed to respect GitHub's rate limits and use conditional requests to avoid unnecessary load (see [`github-data.md`](../data/github-data.md)). Repository license information is captured and preserved; content is meant to be linked back to its GitHub source rather than reproduced, with attribution following each repository's own license terms.

## Secrets and configuration

No secrets are ever committed. Configuration is designed to live in environment files (`.env.local`, `.env.production`, and a committed `.env.example` with placeholders only) and would determine database credentials, the GitHub token, and provider selection — never hard-coded into application code. See [`secrets-management.md`](./secrets-management.md).

## Authentication and authorization

No authentication exists at Stage 2, and none is required for the core feed to work. `session_id` carries no privilege and no identifying information. Authentication, authorization, and API-level rate limiting are planned to arrive together at Stage 4, alongside accounts. See [`authentication-authorization.md`](./authentication-authorization.md).

## Input validation and rate limiting

Request validation is designed to run through Pydantic schemas at the API boundary. Rate limiting on the API itself is a Stage 4 addition, tied to authentication — see [`../api/rate-limits.md`](../api/rate-limits.md).

## CORS and security headers

Design intent: locked to known origins, standard security headers applied once the API is public-facing. Not yet exercised, since nothing is deployed.

## Auditability

Internal errors are designed to always be logged server-side with full context; the client only ever sees a generic message (see [`../api/errors.md`](../api/errors.md)). Audit logging for administrative actions is part of the Stage 4+ observability buildout, introduced alongside the admin tooling it would need to cover — neither exists yet.

Source: [`DEVFEED.md` §21](../../DEVFEED.md#21-security-and-data-handling), `SECURITY.md`.
