# Privacy

> **State: Current Design.** No data is currently being collected, since nothing is deployed or implemented. What follows is the collection principle the system is designed to follow once it exists.

## Principle: collect only what maps to a defined metric

Analytics are designed to be minimal — only the three Stage 3 event types (`PROJECT_VIEW`, `PROJECT_OPEN_GITHUB`, `PROJECT_SAVE`), tied to an anonymous session ID, with no free-text personal information in event metadata. `DEVFEED.md` is explicit that only information that maps to an actually-defined metric gets collected — this ruled out, for example, adding fields to `user_events` "speculatively." Source: [`DEVFEED.md` §19](../../DEVFEED.md#19-database-architecture), [§21](../../DEVFEED.md#21-security-and-data-handling).

## What identifies a user today: nothing

At Stage 2, there is no user account, no email, no name, no IP-based tracking, and no device fingerprinting designed into the system. The only identifier is `session_id` — a client-generated UUID v4 stored in `localStorage`, containing no embedded identifying information, carrying no privilege. See [`../api/authentication.md`](../api/authentication.md) for its full lifecycle.

## `metadata` field constraints

The `user_events.metadata` column is `jsonb`, explicitly documented as intended to be "small, structured, no free-text PII" — a constraint on what event metadata is allowed to contain, not just a data-type note.

## What isn't addressed yet

- No documented policy exists for what happens to `user_events` data over time (see [`../data/data-retention.md`](../data/data-retention.md) — this is a genuine gap, not a decision).
- No cookie-consent or privacy-notice mechanism is described, though at Stage 2 there's arguably nothing requiring one beyond a `localStorage`-stored anonymous ID and no cookies at all (`session_id` is explicitly never a cookie).
- Once Stage 4 introduces accounts and potentially GitHub OAuth, real personal data (at minimum, a GitHub identity) enters the system for the first time — no privacy design exists yet for that transition, only the stated intent to request OAuth permissions minimally ("without over-requesting permissions").

Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification), [§21](../../DEVFEED.md#21-security-and-data-handling).
