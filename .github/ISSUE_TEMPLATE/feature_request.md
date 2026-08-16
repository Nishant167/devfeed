---
name: Feature request
about: Propose a new capability or change to DevFeed
title: "[Feature] "
labels: enhancement
---

Before opening this, check whether the idea is already covered as future roadmap in `DEVFEED.md` (§6 Feature Scope, §15–18, §27 Future Roadmap). If it is, comment on why it should move up rather than opening a duplicate.

## Problem / use case

What's missing or broken about the current discovery experience that this addresses. Not "it would be nice to have" — an actual situation where DevFeed falls short today.

## Proposed solution

What you're suggesting, concretely enough that someone else could evaluate it.

## Why it matters to DevFeed

How this serves the product thesis — useful discoveries per session, explainable ranking, quality over popularity (`DEVFEED.md` §1–3). A feature that increases engagement without increasing discovery quality is out of scope by design.

## Possible implementation considerations

Which part of the system this touches (ingestion, ranking, API, frontend, database), and whether it fits the current stage or belongs in a later one. If it implies new infrastructure (a queue, a new data store, authentication), say so explicitly — infrastructure is added only when a demonstrated problem requires it (`DEVFEED.md` §26).
