# Errors

> **State: Current Design.** No error-handling code exists yet; this documents the specified error contract for the Stage 2 build.

## Error envelope

All non-2xx responses are designed to use one consistent shape:

```json
{ "error": { "code": "REPOSITORY_NOT_FOUND", "message": "Repository could not be found." } }
```

## Error codes

| Code | HTTP status | Meaning |
|---|---|---|
| `REPOSITORY_NOT_FOUND` | 404 | Requested repository ID does not exist |
| `INVALID_CURSOR` | 400 | Malformed or expired pagination cursor |
| `VALIDATION_ERROR` | 422 | Request failed schema validation |
| `INTERNAL_ERROR` | 500 | Unexpected server error — generic client message, full context logged server-side |

## Design principles

- Internal stack traces are never exposed to clients — the client sees a generic message; full context is logged server-side only. This is a stated security requirement, not just an error-formatting preference (see [`security-architecture.md`](../security/security-architecture.md)).
- Request validation runs through Pydantic schemas at the API boundary, so malformed requests are expected to surface as `VALIDATION_ERROR` (422) before reaching business logic.
- A pagination cursor that no longer resolves (e.g., after an ingestion run shifted the ordering it referenced) returns `INVALID_CURSOR` rather than silently restarting from page 1 — see [ADR-0009](../decisions/ADR-0009-position-cursor-pagination.md).

Source: [`DEVFEED.md` §20](../../DEVFEED.md#20-api-specification), [§21](../../DEVFEED.md#21-security-and-data-handling).
