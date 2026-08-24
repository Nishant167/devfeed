# ADR-0001: Modular Monolith Over Microservices

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

DevFeed has multiple distinct domains — GitHub ingestion, repository quality/classification, ranking, feed serving, search, and (later) personalization and AI analysis. A team building a product with this many eventual domains often defaults to microservices, splitting each domain into its own deployed service from day one.

## Decision

Build a modular monolith: domain boundaries are enforced by module structure (`core/ranking/`, `api/`, `web/`), not by network boundaries or separate deployments, until a specific component demonstrably needs independent scaling or deployment.

## Alternatives considered

- **Microservices from the start** — a separate service per domain (ingestion service, ranking service, feed API, etc.), communicating over the network.
- **A single undifferentiated codebase with no enforced module boundaries** — everything in one API app with no `core/ranking/` separation.

## Rationale

At Stage 0–3 there is no demonstrated need for independent scaling of any one component, and no team-size pressure that would justify the operational overhead of multiple deployed services (service discovery, network failure modes, distributed tracing, inter-service versioning). A modular monolith gets the organizational benefit (clear module ownership, enforced boundaries) without the operational cost. The one exception already made is ingestion, which is a separate deployment target — not because it's microservices, but because its failure and redeploy cadence is genuinely different from the API's (see ADR-0003).

## Consequences

**Easier:** faster iteration, simpler local development and deployment, no distributed-systems failure modes to design around prematurely.

**Harder:** if a specific component (most plausibly ranking, under heavy load, or AI analysis, once it exists) later needs independent scaling, it has to be extracted — that extraction cost is deferred, not eliminated.

**Trigger for revisiting:** a specific component provably needing independent scaling or deployment (`DEVFEED.md` §26).

Source: [`DEVFEED.md` §7](../../DEVFEED.md#7-system-architecture).
