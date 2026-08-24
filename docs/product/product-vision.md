# Product Vision

> **State: Current Design (product definition).** The product described here is a decided definition, not implemented software — it is what Stage 0–3 is being built toward. See [`roadmap.md`](./roadmap.md) for what's actually implemented today (nothing — this repository is documentation only).

## What DevFeed is

DevFeed is a personalized discovery feed for developers, built on top of GitHub's repository ecosystem. A user picks a handful of interests and gets a ranked stream of GitHub repositories worth knowing about — AI/ML projects, developer tools, data engineering pipelines, research implementations, infrastructure and security tools, robotics, general engineering work. Each entry explains what the project is, what it's built with, how healthy it looks, and why it was ranked there.

"Instagram for GitHub" describes the format quickly, but it isn't the product. DevFeed is a discovery engine for builders — GitHub's repository ecosystem turned into something personalized and explorable, not just searchable.

Source: [`DEVFEED.md` §1](../../DEVFEED.md#1-project-overview), [§2](../../DEVFEED.md#2-vision-and-problem).

## The problem

There's an enormous amount of valuable technical work on GitHub, and discovery for it is fragmented. People currently find projects through GitHub search, GitHub Trending, Hacker News, Reddit, X, newsletters, Discord, blogs, YouTube, "awesome" lists, and word of mouth. Every one of these is search-driven, community-driven, or popularity-driven — none of them personalize well. GitHub itself is built for managing and collaborating on software, not for helping someone discover software they didn't know they were looking for.

## Who it's for

- AI enthusiasts — LLMs, agents, RAG, computer vision, AI infrastructure
- Data engineers — Spark, Airflow, dbt, lakehouses, ETL, data platforms
- Software developers — backend, frontend, APIs, system design, open source
- Students looking for projects and research at the right skill level
- Researchers looking for implementations of papers and research tooling
- Open source contributors looking for active repositories worth contributing to

See [`user-personas.md`](./user-personas.md) for detail.

## Why GitHub project discovery is hard

GitHub Trending and star counts collapse "popular" and "good" into one signal. A well-built 200-star project and a poorly-maintained 100,000-star project are treated identically by any interface that sorts on stars. Search requires already knowing what to search for, which doesn't help with the "I didn't know I wanted this" case. None of the existing channels (Trending, HN, newsletters, "awesome" lists) rank for relevance to an individual — they rank for aggregate popularity or recency.

## What makes DevFeed different

- Ranking optimizes for useful discoveries per session, not time spent in the app.
- Stars are one input among several — quality is scored separately and explainably (see [ADR-0007](../decisions/ADR-0007-deterministic-ranking.md)).
- No fake notifications, artificial scarcity, or engagement bait.
- Ranking is deterministic and explainable before any machine learning is introduced — every result can answer "why is this here?"

Source: [`DEVFEED.md` §1](../../DEVFEED.md#1-project-overview).

## What DevFeed explicitly does not try to solve

- It is not a GitHub search replacement or a GitHub client.
- It is not a social network — social features (follows, comments, profiles) are deliberately last on the roadmap ([`DEVFEED.md` §18](../../DEVFEED.md#18-social-and-community)) and only get built once the discovery engine has proven itself on its own.
- It does not optimize for screen time, notification volume, or vanity metrics — the explicit target is useful discoveries per session, not minutes spent in the app.
- It is not attempting deep codebase understanding or AI project intelligence at this stage — that is future work gated on the core feed proving itself first ([`DEVFEED.md` §16](../../DEVFEED.md#16-ai-project-intelligence)).
- It is not monetized and has no payment or enterprise features planned in the current build.

## Product thesis and the open question

The core thesis: developers should have a personalized technical discovery feed that answers "what interesting thing should I know about today?" There's a genuinely unresolved second question the project doesn't assume an answer to: do developers want a *recurring* feed, or is this closer to an on-demand search tool reached for when there's a specific need? Stage 3 (real user validation) exists specifically to answer this before anything is built that assumes one or the other. If the answer turns out to be "search tool, not daily feed," the documented pivot is to make search the primary surface and the feed secondary — not to force the feed model regardless of evidence.

Source: [`DEVFEED.md` §2](../../DEVFEED.md#2-vision-and-problem).
