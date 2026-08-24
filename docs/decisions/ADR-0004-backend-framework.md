# ADR-0004: Backend Framework — FastAPI + Pydantic

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

The backend needs to serve a small, versioned REST API (`/api/v1/feed`, `/repositories/{id}`, `/topics`, `/events`, `/search`, `/health`) with request validation, and needs to generate API documentation without a separate maintenance burden.

## Decision

Python backend using FastAPI for the web framework, Pydantic for request/response validation, and SQLAlchemy + Alembic for the database layer.

## Alternatives considered

`DEVFEED.md` does not document an explicit alternative-framework evaluation (e.g., Flask, Django) for the backend framework choice itself — the rationale given is about validation and documentation ergonomics, not a head-to-head comparison. This ADR records the decision and its stated rationale rather than inventing an alternatives analysis the source document doesn't contain.

## Rationale

Pydantic validation lets request/response schemas double as the OpenAPI contract, and FastAPI generates that OpenAPI documentation automatically, served at `/docs` — meaningful for a six-endpoint API where hand-maintained API documentation would be redundant with the schema definitions already required for validation.

## Consequences

**Easier:** request validation and API documentation stay in sync automatically; async request handling is available if ingestion or future AI calls need it without a framework change.

**Harder:** ties the backend to Python's async ecosystem and FastAPI's specific conventions; no consequence beyond that is documented, since no alternative was seriously weighed against it in the source material.

Source: [`DEVFEED.md` §8](../../DEVFEED.md#8-technology-stack), [§20](../../DEVFEED.md#20-api-specification).
