# Rate Limits

> **State:** Two separate concerns, neither implemented. Neither is running code — the repository has no ingestion job and no deployed API.

## DevFeed's own API rate limiting (client-facing) — Planned, Stage 4

There is currently no rate limiting on DevFeed's own API endpoints, implemented or otherwise. `DEVFEED.md` explicitly ties API-level rate limiting to Stage 4, arriving alongside authentication — the reasoning is that meaningful per-client rate limiting needs an identity to limit against, which doesn't exist until accounts do. At Stage 2, the only real defenses against abuse would be input validation (Pydantic schemas at the boundary) and the fact that most endpoints are read-only and cheap — neither of which exists yet either, since no API code has been written. Source: [`DEVFEED.md` §21](../../DEVFEED.md#21-security-and-data-handling).

## GitHub's rate limits on DevFeed's ingestion (outbound) — Current Design

This is the rate limit DevFeed has to respect, not enforce. GitHub's authenticated API access grants 5,000 requests/hour. The ingestion design (once built):

- Monitors `X-RateLimit-Remaining` on every response.
- Sleeps proactively before exhaustion, rather than reacting only after a `403`.
- Backs off with jitter on `403` and `5xx` responses, with retries.
- Uses conditional requests (`If-None-Match` with a stored ETag) so a `304 Not Modified` response — meaning nothing changed — costs no further processing.

GitHub's Search API additionally caps any single query at 1,000 results, which is why the ingestion query strategy slices across language, star-band, and date range rather than issuing broad queries. See [`github-data.md`](../data/github-data.md) for the full query-slicing design.

Source: [`DEVFEED.md` §9](../../DEVFEED.md#9-github-ingestion).

## What's not addressed anywhere in the source document

`DEVFEED.md` doesn't specify per-endpoint rate-limit numbers for the future Stage 4 API rate limiting (requests/minute, burst allowances, etc.) — only that it arrives "tied to authentication." Those figures don't exist yet and shouldn't be invented; they'll need to be defined when Stage 4 authentication work actually begins.
