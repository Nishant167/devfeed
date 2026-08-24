# API Overview

> **State: Current Design.** The repository contains no `api/` directory, no FastAPI application, and no route code — this is not deferred future work, it is the defined specification for the immediate Stage 2 build, not yet implemented. Everything in this `api/` documentation section describes the Stage 2 API specification from `DEVFEED.md` §20, not a running service. There is no live endpoint, no deployed instance, and no OpenAPI document being served anywhere yet.

## Design

Base path: `/api/v1/` — versioned so breaking changes get a new prefix without disturbing existing clients. Once implemented, OpenAPI documentation is generated automatically by FastAPI and intended to be served at `/docs`.

## Endpoint summary

| Method | Path | Purpose | Auth required |
|---|---|---|---|
| `GET` | `/api/v1/feed` | Ranked, paginated repository feed | No — anonymous `session_id` only |
| `GET` | `/api/v1/repositories/{id}` | Full detail for one repository | No |
| `GET` | `/api/v1/topics` | List of topics with repository counts | No |
| `POST` | `/api/v1/events` | Record an anonymous interaction event | No |
| `GET` | `/api/v1/search` | Full-text search over repositories | No |
| `GET` | `/health` | Liveness check (unversioned) | No |

Full parameter, request, and response detail for each is in [`endpoints.md`](./endpoints.md).

## What doesn't exist in this API surface yet

- **Authentication** — no endpoint requires or accepts credentials at this stage. See [`authentication.md`](./authentication.md).
- **Rate limiting on DevFeed's own API** — not implemented; arrives at Stage 4 tied to authentication. See [`rate-limits.md`](./rate-limits.md).
- **Any endpoint under `/api/v1/auth/*`, `/recommendations`, `/collections`, `/learning`, or `/ai`** — all future, arriving alongside the feature each one serves, none of which is built.

## CORS

Design intent: configured per environment — local dev allows `localhost:3000`; production allows only the deployed frontend origin, never wildcarded once real event data is flowing. Not yet exercised because there is no deployed API to configure.

Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification).
