# ADR-0005: Frontend Framework — Next.js, React, TypeScript, Tailwind

## Status

Accepted — Design Decision *(decided for the planned architecture; no implementation exists in the repository yet)*

## Context

The frontend is a scrollable feed of repository cards with feature areas (feed, repository detail, search) that need to feel dense and technical rather than like a generic social app, with dark mode as the default visual mode.

## Decision

Next.js, React, TypeScript, and Tailwind CSS, organized by feature (`feed/`, `repository/`, `search/`) rather than one large `components/` directory, built on reusable design tokens (typography, spacing, color, buttons, cards, badges, navigation, dialogs) with both dark and light mode supported from the start.

## Alternatives considered

`DEVFEED.md` doesn't document a considered alternative to this stack (e.g., a different meta-framework or plain React SPA) — the frontend section states the choice and its intended visual/organizational qualities directly, without a comparison. This ADR records what was decided and why, without fabricating alternatives the source material doesn't mention.

## Rationale

Feature-based organization keeps feed, repository-detail, and search code independently understandable as the frontend grows, instead of collapsing into an undifferentiated component directory. Design tokens (rather than ad hoc per-component styling) are meant to keep the visual language consistent and dense/technical — explicitly *not* a copy of Instagram or TikTok's visual style, since the product is meant to read as a tool for builders, not an entertainment feed.

## Consequences

**Easier:** feature boundaries in the frontend mirror the product's conceptual boundaries (feed vs. repository detail vs. search); consistent theming (dark/light) is centralized rather than scattered.

**Harder:** requires discipline to keep new components inside their feature directory and using design tokens rather than one-off styles, which has to be enforced through review since nothing in the tooling enforces it automatically.

Source: [`DEVFEED.md` §8](../../DEVFEED.md#8-technology-stack).
