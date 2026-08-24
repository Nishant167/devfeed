# User Personas

> **State: Current Design (product definition).** These personas are drawn directly from the "who it's for" list in [`DEVFEED.md` §4](../../DEVFEED.md#4-users-and-core-experience) — no persona detail (goals, quotes, demographics) beyond what the source document supports has been invented. No product exists yet for any persona to actually use.

DEVFEED.md defines six developer segments the product targets. They're kept here as short, realistic descriptions rather than expanded personas with fabricated backstories, because the source document doesn't go further than naming the segment and its interests.

### AI enthusiast

Interested in LLMs, agents, RAG, computer vision, and AI infrastructure. Wants to see what's actively being built in the fast-moving parts of the AI ecosystem, distinct from a curated "top AI projects" list that's usually a few months stale.

### Data engineer

Interested in Spark, Airflow, dbt, lakehouses, ETL, and data platform tooling. Underserved by general "trending" feeds, which skew toward web frameworks and AI projects and rarely surface data infrastructure work at all.

### Software developer

General backend, frontend, API, and system-design interest, including general open source work not tied to a specific niche. The broadest segment and the one most likely to use DevFeed as a general discovery habit rather than for a narrow technical interest.

### Student

Looking for projects and research at an appropriate skill level. DEVFEED.md is explicit that a reliable "difficulty" signal doesn't exist yet ([`DEVFEED.md` §11](../../DEVFEED.md#11-repository-quality-and-classification)), so this persona's needs are only partially served by the current design — skill-level filtering is a known gap, not a shipped capability.

### Researcher

Looking for implementations of papers and research tooling. This persona is most directly connected to the future "Research mode" concept (paper → implementation → related work) described in [`DEVFEED.md` §27](../../DEVFEED.md#27-future-roadmap), which is not built.

### Open source contributor

Looking for active repositories worth contributing to. Served today mainly by the freshness and quality signals in ranking (recent activity, contributor count, CI presence) rather than any contribution-specific feature — there's no "good first issue" surfacing or contribution-matching functionality planned in the current build.

## What's deliberately not modeled

DEVFEED.md doesn't define personas around monetization, enterprise use, or team/organization accounts, and none are invented here — those don't appear anywhere in the product definition.
