"""Stage 0 CLI entrypoint. Orchestrates: probed query grid -> paced GitHub
Search -> junk filter -> metadata-only pre-sort + secondary-fetch cap ->
quality/freshness scoring -> top ~100 -> static HTML.

See DEVFEED.md section 28 ("Immediate Next Steps -- Stage 0 -- Scroll Test").

Each invocation is a clean run: a fresh run_id is generated every time, and if
the process is interrupted the fix is simply to re-run the script from
scratch. Resume/checkpoint support was explicitly decided against for Stage 0
and is not implemented here.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from datetime import date
from math import log1p
from pathlib import Path

from dotenv import load_dotenv

from stage0.config import MONTHS_BACK_DEFAULT, SECONDARY_FETCH_CAP
from stage0.filter import is_junk
from stage0.ingest import FilesystemRawPayloadStore, GitHubClient, make_run_id
from stage0.query_grid import build_query_grid
from stage0.render import render_html
from stage0.scoring import base_score, freshness_score, quality_score

TOP_N = 100
DEFAULT_OUTPUT = "stage0/output/index.html"

# Characters forbidden in Windows filenames (and awkward on POSIX): < > : " / \ | ? *
# Star bands like ">5000" and slash-bearing full_names ("org/repo") both need
# this before becoming part of a RawPayloadStore key/filename.
_UNSAFE_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\s]+')


def _sanitize_identifier(s: str) -> str:
    return _UNSAFE_FILENAME_CHARS.sub("_", s).strip("_")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="stage0",
        description="DevFeed Stage 0 scroll-test: build a ranked, junk-filtered "
        "GitHub repo feed and render it as a static HTML page.",
    )
    parser.add_argument(
        "--months-back",
        type=int,
        default=MONTHS_BACK_DEFAULT,
        help=f"How many trailing months to query (default: {MONTHS_BACK_DEFAULT}).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"Path to write the rendered HTML page (default: {DEFAULT_OUTPUT}).",
    )
    return parser.parse_args(argv)


def _require_github_token() -> str:
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print(
            "ERROR: GITHUB_TOKEN is not set.\n"
            "Stage 0 needs an authenticated GitHub token to call the Search "
            "and REST APIs. Create a personal access token on GitHub, then "
            "either:\n"
            "  1. export it in your shell: GITHUB_TOKEN=ghp_xxx\n"
            "  2. or copy .env.example to .env and fill it in.\n",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def _metadata_only_score(item: dict, today: date) -> float:
    """Stars + recency, no secondary data needed -- used only to rank
    survivors before the secondary-fetch cap (DEVFEED.md section 9,
    "Defensive parsing"). Not one of the tested pure scoring functions;
    purely an internal pre-sort heuristic."""
    stars = item.get("stargazers_count") or 0
    recency = freshness_score({"pushed_at": item.get("pushed_at")}, now=today)
    # log-scale stars so a handful of mega-repos don't dominate the pre-sort.
    return log1p(max(stars, 0)) * 0.5 + recency * 0.5


def _fetch_search_results(
    client: GitHubClient,
    raw_store: FilesystemRawPayloadStore,
    run_id: str,
    today: str,
    grid: list[tuple[str, str, str]],
) -> dict[str, dict]:
    """Runs every (language, star_band, date_range) query in the grid,
    paginating up to GitHub's 1,000-result cap per query, storing every raw
    page and deduplicating repositories by full_name across queries."""
    repos: dict[str, dict] = {}
    for lang, star_band, date_range in grid:
        query = f"language:{lang} stars:{star_band} pushed:{date_range}"
        page = 1
        while True:
            data = client.search(query, page=page)
            identifier = _sanitize_identifier(f"{lang}_{star_band}_{date_range}_p{page}")
            raw_store.put(
                f"github/{today}/{run_id}/search/{identifier}.json",
                json.dumps(data).encode("utf-8"),
            )
            items = data.get("items", []) or []
            for item in items:
                full_name = item.get("full_name")
                if full_name and full_name not in repos:
                    repos[full_name] = item
            total_count = data.get("total_count", 0) or 0
            fetched_so_far = page * 100
            if len(items) < 100 or fetched_so_far >= min(total_count, 1000):
                break
            page += 1
    return repos


def _secondary_fetch(
    client: GitHubClient,
    raw_store: FilesystemRawPayloadStore,
    run_id: str,
    today: str,
    full_name: str,
) -> dict:
    """README, contributors, releases, and a couple of common-path checks for
    tests/CI. Best-effort: any individual failure degrades the repo's signals
    to 'missing' rather than aborting the whole repo (defensive parsing,
    DEVFEED.md section 9)."""
    safe_name = _sanitize_identifier(full_name)

    readme = client.get_readme(full_name)
    readme_has_code_blocks = False
    if readme is not None:
        raw_store.put(
            f"github/{today}/{run_id}/repositories/{safe_name}_readme.json",
            json.dumps(readme).encode("utf-8"),
        )
        content_b64 = readme.get("content") or ""
        try:
            decoded = base64.b64decode(content_b64).decode("utf-8", errors="ignore")
            readme_has_code_blocks = "```" in decoded
        except Exception:
            readme_has_code_blocks = False

    contributors = client.get_contributors(full_name)
    raw_store.put(
        f"github/{today}/{run_id}/repositories/{safe_name}_contributors.json",
        json.dumps(contributors).encode("utf-8"),
    )

    releases = client.get_releases(full_name)
    raw_store.put(
        f"github/{today}/{run_id}/repositories/{safe_name}_releases.json",
        json.dumps(releases).encode("utf-8"),
    )

    has_ci = client.path_exists(full_name, ".github/workflows")
    has_tests = any(
        client.path_exists(full_name, p) for p in ("tests", "test", "spec")
    )

    return {
        "readme_has_code_blocks": readme_has_code_blocks,
        "contributor_count": len(contributors),
        "release_count": len(releases),
        "has_ci": has_ci,
        "has_tests": has_tests,
    }


def run(months_back: int, output_path: str) -> None:
    token = _require_github_token()
    run_id = make_run_id()
    today = date.today().isoformat()
    raw_store = FilesystemRawPayloadStore()

    print(f"[stage0] run_id={run_id} months_back={months_back}")

    with GitHubClient(token) as client:
        print("[stage0] probing bucket sizes and building query grid...")
        grid = build_query_grid(months_back, probe=client.probe_count)
        print(f"[stage0] query grid has {len(grid)} (language, star_band, date_range) buckets")

        print("[stage0] running search queries (paced, this dominates runtime)...")
        repos = _fetch_search_results(client, raw_store, run_id, today, grid)
        print(f"[stage0] fetched {len(repos)} unique repositories before filtering")

        non_junk = {
            full_name: item
            for full_name, item in repos.items()
            if not is_junk(item.get("name", full_name.split("/")[-1]))
        }
        print(f"[stage0] {len(non_junk)} repositories survived junk filtering")

        today_date = date.today()
        candidates = sorted(
            non_junk.values(),
            key=lambda item: _metadata_only_score(item, today_date),
            reverse=True,
        )[:SECONDARY_FETCH_CAP]
        print(f"[stage0] fetching secondary data for top {len(candidates)} candidates (capped at {SECONDARY_FETCH_CAP})...")

        scored: list[dict] = []
        for i, item in enumerate(candidates, start=1):
            full_name = item["full_name"]
            secondary = _secondary_fetch(client, raw_store, run_id, today, full_name)
            repo = {
                "full_name": full_name,
                "description": item.get("description"),
                "html_url": item.get("html_url"),
                "stargazers_count": item.get("stargazers_count"),
                "pushed_at": item.get("pushed_at"),
                "has_license": bool(item.get("license")),
                **secondary,
            }
            repo["quality_score"] = quality_score(repo, now=today_date)
            repo["freshness_score"] = freshness_score(repo, now=today_date)
            repo["base_score"] = base_score(repo, now=today_date)
            scored.append(repo)
            if i % 100 == 0:
                print(f"[stage0]   ...{i}/{len(candidates)} secondary-fetched")

    ranked = sorted(scored, key=lambda r: r["base_score"], reverse=True)[:TOP_N]
    print(f"[stage0] rendering top {len(ranked)} to {output_path}")

    html = render_html(ranked)
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    print(f"[stage0] done. {len(ranked)} repos written to {out_path}")


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    run(months_back=args.months_back, output_path=args.output)


if __name__ == "__main__":
    main()
