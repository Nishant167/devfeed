"""Static HTML rendering of the ranked feed. See DEVFEED.md section 28 (item 5:
"A static HTML page rendering the top ~100 results with repository,
description, stars, and score."). Plain HTML/CSS, no framework.

Untested per the spec's Testing Plan ("HTML rendering stays untested -- this is
the I/O shell, not the pure logic").
"""

from __future__ import annotations

import html as _html

_PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DevFeed Stage 0 -- Scroll Test</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 760px;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.5;
  }}
  header {{ margin-bottom: 1.5rem; }}
  header p {{ opacity: 0.7; }}
  .card {{
    border: 1px solid rgba(128, 128, 128, 0.35);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.9rem;
  }}
  .card h2 {{ margin: 0 0 0.35rem; font-size: 1.05rem; }}
  .card h2 a {{ text-decoration: none; }}
  .card h2 a:hover {{ text-decoration: underline; }}
  .meta {{ font-size: 0.85rem; opacity: 0.75; margin-bottom: 0.35rem; }}
  .rank {{ opacity: 0.5; margin-right: 0.4rem; }}
  .desc {{ margin: 0; }}
  .empty {{ opacity: 0.7; }}
</style>
</head>
<body>
<header>
  <h1>DevFeed Stage 0 -- Scroll Test</h1>
  <p>{count} ranked, non-junk repositories.</p>
</header>
<main>
{cards}
</main>
</body>
</html>
"""

_CARD_TEMPLATE = """<article class="card">
  <h2><span class="rank">#{rank}</span><a href="{url}" target="_blank" rel="noopener noreferrer">{full_name}</a></h2>
  <div class="meta">&#9733; {stars} &middot; score {score}</div>
  <p class="desc">{description}</p>
</article>"""

_EMPTY_STATE = '<p class="empty">No repositories survived filtering and scoring.</p>'


def _card_html(rank: int, repo: dict) -> str:
    full_name = _html.escape(str(repo.get("full_name") or repo.get("name") or "unknown/unknown"))
    url = _html.escape(str(repo.get("html_url") or f"https://github.com/{repo.get('full_name', '')}"))
    stars = repo.get("stargazers_count", repo.get("stars", 0)) or 0
    score = repo.get("base_score", 0.0) or 0.0
    description = _html.escape(str(repo.get("description") or "").strip()) or "<em>No description.</em>"
    return _CARD_TEMPLATE.format(
        rank=rank,
        url=url,
        full_name=full_name,
        stars=f"{int(stars):,}" if isinstance(stars, (int, float)) else _html.escape(str(stars)),
        score=f"{float(score):.3f}",
        description=description,
    )


def render_html(ranked: list[dict]) -> str:
    """Renders one card per repo: full name, description, stars, base_score,
    link to GitHub. `ranked` is expected to already be junk-filtered, scored,
    sorted by base_score descending, and capped to the top ~100 by the caller
    (main.py) -- this function only renders what it's given."""
    if not ranked:
        cards_html = _EMPTY_STATE
    else:
        cards_html = "\n".join(_card_html(i, repo) for i, repo in enumerate(ranked, start=1))
    return _PAGE_TEMPLATE.format(count=len(ranked), cards=cards_html)
