# Authentication

> **State: Implemented fact (no authentication exists); Current Design (the `session_id` model for Stage 2); Planned (Stage 4 authentication, named explicitly as future work in `DEVFEED.md`).** No authentication is implemented anywhere in the repository, and none is required for Stage 0–3.

## Current Design: no authentication, an anonymous session identifier instead

The core feed, search, and save functionality are designed to work with no account and no login. Instead, requests carry an anonymous, client-generated `session_id`.

### `session_id` lifecycle

| Property | Definition |
|---|---|
| Format | Random UUID v4 |
| Generation | Client-side, on first app load, before any network request |
| Storage | `localStorage`, under a single fixed key — never a cookie, never derived from IP or device characteristics |
| Lifetime | Persists across sessions until the user clears site storage |
| Regeneration | Only if the stored value is missing or fails UUID-format validation |
| Contents | No embedded identifying information of any kind |

`session_id` is explicitly not a credential and carries no privilege — it exists only to support the Stage 3 usage metrics (opens/session, save rate, day-7 return) described in [`success-metrics.md`](../product/success-metrics.md), consistent with the product's general stance of collecting only what's actually needed. Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification), [§21](../../DEVFEED.md#21-security-and-data-handling).

## Why there's no auth yet

`DEVFEED.md` treats "complex authentication" as an explicit non-goal for the current build, not an oversight — see [`DEVFEED.md` §3](../../DEVFEED.md#3-goals-and-non-goals). The core feed doesn't require an account to prove or disprove the product's central hypothesis (Stage 0–3), so building auth ahead of that would be infrastructure before a demonstrated need.

## Planned: Stage 4 authentication (explicitly named future work; mechanics not designed in detail)

The documented trigger for introducing authentication is: users ask for saves to persist across devices. Once that happens:

- New endpoints appear under `/api/v1/auth/*`.
- Existing endpoints gain an optional `Authorization: Bearer <token>` header.
- `session_id`-scoped saves and events migrate to `user_id` scope on login.
- Optional GitHub OAuth is mentioned as a path for deeper personalization "without over-requesting permissions."

None of this has a concrete design (token format, session model, OAuth scopes) yet — `DEVFEED.md` states the trigger and the intended shape, not an implementation plan. This should be treated as directional intent, not a specification to build against today.

Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification), [§21](../../DEVFEED.md#21-security-and-data-handling), [§26](../../DEVFEED.md#26-milestones-and-gates).
