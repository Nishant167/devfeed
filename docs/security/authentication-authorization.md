# Authentication and Authorization

> **State: Implemented fact (neither exists); Current Design (why, by intent, not by omission); Planned (Stage 4, explicitly named future work).** See [`../api/authentication.md`](../api/authentication.md) for the full API-facing detail; this document covers the security-policy framing specifically.

## Implemented posture: no authentication, none required

No authentication exists at Stage 2, and none is required for the core feed, search, or save functionality to work. There is no login, no password, no session cookie, and no user account anywhere in the system. `DEVFEED.md` treats this as an explicit non-goal for the current build, not a gap — see [`DEVFEED.md` §3](../../DEVFEED.md#3-goals-and-non-goals).

## What replaces it: an unprivileged session identifier

`session_id` is a client-generated UUID v4, stored in `localStorage`, sent with feed and event requests. It exists solely to support Stage 3 usage-validation metrics (opens/session, save rate, day-7 return). It carries **no privilege** — nothing in the system grants access, elevates permissions, or unlocks functionality based on `session_id` — and no identifying information is embedded in it. It should not be treated as an authentication mechanism, and none of the current API surface performs authorization checks against it.

## Authorization

There is currently no concept of "who is allowed to do what" in the system, because there's no concept of "who" beyond an anonymous session. Every endpoint in the current design (`GET /feed`, `GET /repositories/{id}`, `GET /topics`, `POST /events`, `GET /search`, `GET /health`) is designed to be equally accessible to any caller.

## Planned: Stage 4

Authentication, authorization, and API-level rate limiting are designed to arrive together, triggered specifically by users asking for saves to persist across devices. Once introduced:

- New endpoints appear under `/api/v1/auth/*`.
- Existing endpoints gain an optional `Authorization: Bearer <token>` header.
- `session_id`-scoped saves and events migrate to `user_id` scope on login.
- Optional GitHub OAuth is mentioned for deeper personalization "without over-requesting permissions."

No token format, session model, permission model, or OAuth scope list is specified yet — this is a documented trigger and rough shape, not an implementation-ready design. Admin tooling (Stage 4+, per [`DEVFEED.md` §18](../../DEVFEED.md#18-social-and-community)) is explicitly designed to be "protected by strong authorization from the start," but that tooling and its authorization model don't exist yet either.

Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification), [§21](../../DEVFEED.md#21-security-and-data-handling), [§26](../../DEVFEED.md#26-milestones-and-gates).
