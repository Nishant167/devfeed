# Security Policy

## Reporting a vulnerability

Report security vulnerabilities privately, not through a public issue. If this repository has GitHub's private vulnerability reporting enabled, use that. Otherwise, contact the repository maintainers directly rather than disclosing publicly. Please don't open a public issue for a security concern until it's been addressed.

## Security principles

DevFeed's full security requirements are defined in [`DEVFEED.md` §21](./DEVFEED.md#21-security-and-data-handling) and [§16](./DEVFEED.md#16-ai-project-intelligence). The rules below are the ones that apply to every contribution, summarized here for visibility:

- **Never commit secrets.** No API keys, tokens, credentials, or database connection strings in code, commit history, or configuration files. Use `.env.local` / `.env.production`, which are never committed — only `.env.example`, with placeholders, is.
- **Never expose GitHub credentials.** The GitHub API token used for ingestion is configuration, injected at runtime, never hard-coded.
- **Repository content is untrusted input, always.** Every GitHub repository DevFeed ingests or analyzes is treated as untrusted. This matters now for ingestion (defensive parsing of API responses) and will matter more once repository analysis (Stage 7) is built.
- **Never execute untrusted repository code.** No running `npm install`, `pip install`, `make`, arbitrary scripts, or binaries from an ingested repository, under any circumstance, at any stage.
- **Internal errors never leak implementation detail.** The API returns generic error messages to clients; full context is logged server-side only.
- **No unnecessary data collection.** Analytics are scoped to what's explicitly needed for the current stage — see `DEVFEED.md` §21 for what that includes today.

## Dependencies

Keep dependencies current and avoid adding a new one without a reason. Flag any dependency with a known vulnerability in its current pinned version.

## Scope

This policy covers the DevFeed codebase, its infrastructure configuration, and its CI/CD setup as they exist at each stage of development (see `DEVFEED.md` §5). It does not cover the security of third-party services DevFeed depends on (GitHub, hosting providers) beyond how DevFeed itself uses them.
