"""Static HTML rendering of the ranked feed. See DEVFEED.md section 28 (item 5:
"A static HTML page rendering the top ~100 results with repository,
description, stars, and score."). Plain HTML/CSS, no framework, no JS.

Visual design: Instagram-style social feed, per explicit, repeated project-
owner direction (not a compromise/adaptation -- the owner wants this look and
DEVFEED.md's product direction now embraces it, see section 1's revision
note). Palette and fonts from the "Social Media Feed" Figma Make export
(purple/cyan, Fraunces + Inter). Stories bar, post-card layout, and heart/
comment/bookmark icon row are all real data, not fabricated social state:
- The "stories" strip is the top-ranked repos, not fake user stories.
- The heart icon shows real star count, the comment icon shows real open
  issue count, the bookmark icon shows the real computed base_score.
- The verified badge shows only when a repo actually clears every quality
  signal (license+tests+CI+docs), not decoratively.
- "Open on GitHub" is the one real, working action (the repo name link and
  the pill button both go there) -- there is no working Like/Save/Follow
  button because Stage 0 has no backend to persist a click; adding one that
  looks clickable but does nothing would be exactly the "misleading
  popularity signal" DEVFEED.md section 2 still rules out even post-pivot.

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,700;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --background: #0a0a0f;
    --foreground: #f0f0f5;
    --card: #13131a;
    --primary: #7c3aed;
    --secondary: #1e1e2a;
    --secondary-foreground: #a0a0b8;
    --muted-foreground: #6b6b88;
    --accent: #06b6d4;
    --border: rgba(255,255,255,0.08);
    --radius: 0.75rem;
    color-scheme: dark;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    background: var(--background); color: var(--foreground);
    font-family: 'Inter', -apple-system, sans-serif; margin: 0;
    -webkit-font-smoothing: antialiased;
  }}
  a {{ color: var(--primary); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  header {{
    position: sticky; top: 0; z-index: 50;
    background: rgba(10,10,15,0.9); backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border); padding: 0 16px;
  }}
  .header-inner {{ max-width: 560px; margin: 0 auto; height: 56px; display: flex; align-items: center; justify-content: space-between; }}
  .brand {{ font-family: 'Fraunces', serif; font-size: 22px; font-weight: 700; letter-spacing: -0.5px; }}
  .brand .dot {{ color: var(--primary); }}
  .count {{ font-size: 12px; color: var(--muted-foreground); }}
  main {{ max-width: 560px; margin: 0 auto; padding: 0 0 60px; }}

  .stories {{
    display: flex; gap: 14px; padding: 16px; overflow-x: auto;
    border-bottom: 1px solid var(--border);
  }}
  .story {{ display: flex; flex-direction: column; align-items: center; gap: 6px; flex-shrink: 0; }}
  .story-ring {{
    width: 60px; height: 60px; border-radius: 50%; padding: 2px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
  }}
  .story-ring img, .story-ring .fallback {{
    width: 100%; height: 100%; border-radius: 50%; object-fit: cover;
    border: 2px solid var(--background); display: block;
  }}
  .story-ring .fallback {{ background: var(--secondary); display: flex; align-items: center; justify-content: center; color: var(--muted-foreground); font-size: 18px; font-weight: 600; }}
  .story-label {{ font-size: 10px; color: var(--muted-foreground); max-width: 62px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

  .feed {{ display: flex; flex-direction: column; gap: 12px; padding: 16px; }}
  .post {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
  .post-head {{ display: flex; align-items: center; gap: 12px; padding: 14px 16px; }}
  .avatar {{ width: 42px; height: 42px; border-radius: 50%; object-fit: cover; border: 2px solid var(--primary); flex-shrink: 0; }}
  .avatar-fallback {{ width: 42px; height: 42px; border-radius: 50%; border: 2px solid var(--primary); flex-shrink: 0; background: var(--secondary); display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 600; color: var(--muted-foreground); }}
  .post-id {{ flex: 1; min-width: 0; }}
  .post-name {{ display: flex; align-items: center; gap: 4px; font-weight: 600; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .post-owner {{ font-size: 12px; color: var(--muted-foreground); }}
  .open-pill {{
    background: none; border: 1px solid var(--border); border-radius: 20px;
    color: var(--muted-foreground); font-size: 12px; font-weight: 500;
    padding: 5px 14px; white-space: nowrap;
  }}
  .open-pill:hover {{ border-color: var(--primary); color: var(--primary); text-decoration: none; }}

  .post-body {{ padding: 4px 16px 0; }}
  .icon-row {{ display: flex; align-items: center; gap: 4px; }}
  .icon-btn {{ display: flex; align-items: center; gap: 5px; padding: 6px 4px; color: var(--muted-foreground); font-size: 13px; }}
  .icon-btn svg {{ flex-shrink: 0; }}
  .icon-spacer {{ flex: 1; }}

  .caption {{ font-size: 14px; color: var(--foreground); line-height: 1.55; padding: 6px 4px 12px; margin: 0; }}
  .caption .who {{ font-weight: 600; }}

  .topics {{ padding: 0 4px 12px; display: flex; gap: 6px; flex-wrap: wrap; }}
  .topic {{
    font-size: 11px; font-weight: 500; color: #a78bfa;
    background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.2);
    border-radius: 20px; padding: 3px 9px;
  }}

  .badges {{ padding: 0 4px 14px; display: flex; gap: 6px; flex-wrap: wrap; }}
  .badge {{ font-size: 11px; border-radius: 4px; padding: 3px 8px; border: 1px solid var(--border); color: var(--muted-foreground); background: rgba(255,255,255,0.03); }}
  .badge.on {{ color: #4ade80; background: #22c55e1a; border-color: #22c55e4d; }}

  .empty {{ text-align: center; padding: 60px 0; color: var(--muted-foreground); font-size: 14px; }}
</style>
</head>
<body>
<header>
  <div class="header-inner">
    <div class="brand">devfeed<span class="dot">.</span></div>
    <div class="count">{count} repos</div>
  </div>
</header>
<main>
  <div class="stories">
{stories}
  </div>
  <div class="feed">
{cards}
  </div>
</main>
</body>
</html>
"""

_STORY_TEMPLATE = """    <a class="story" href="{url}" target="_blank" rel="noopener noreferrer">
      <div class="story-ring">{story_avatar}</div>
      <span class="story-label">{name}</span>
    </a>"""

_HEART_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
_COMMENT_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
_BOOKMARK_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>'
_VERIFIED_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" style="display:inline;vertical-align:middle;margin-left:2px;"><circle cx="12" cy="12" r="12" fill="#7c3aed"/><path d="M9 12l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'

_POST_TEMPLATE = """    <article class="post">
      <div class="post-head">
        {avatar}
        <div class="post-id">
          <div class="post-name">#{rank} {owner}/{name}{verified}</div>
          <div class="post-owner">{language_or_pushed}</div>
        </div>
        <a class="open-pill" href="{url}" target="_blank" rel="noopener noreferrer">Open</a>
      </div>
      <div class="post-body">
        <div class="icon-row">
          <span class="icon-btn">{heart_svg} {stars}</span>
          <span class="icon-btn">{comment_svg} {issues}</span>
          <span class="icon-spacer"></span>
          <span class="icon-btn">{bookmark_svg} {score}</span>
        </div>
        <p class="caption"><span class="who">{owner}/{name}</span> {description}</p>
        {topics_html}
        <div class="badges">{badges_html}</div>
      </div>
    </article>"""

_EMPTY_STATE = '<p class="empty">No repositories survived filtering and scoring.</p>'


def _fmt_count(n: object) -> str:
    if not isinstance(n, (int, float)):
        return "0"
    n = int(n)
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(n)


def _fmt_date(value: object) -> str:
    s = str(value or "")
    return _html.escape(s[:10]) if s else "unknown"


def _avatar_html(owner: str, avatar_url: object, css_class: str, fallback_class: str) -> str:
    if avatar_url:
        return f'<img class="{css_class}" src="{_html.escape(str(avatar_url))}" alt="{owner}" loading="lazy">'
    initial = _html.escape((owner[:1] or "?").upper())
    return f'<div class="{fallback_class}">{initial}</div>'


def _story_html(repo: dict) -> str:
    full_name = str(repo.get("full_name") or "unknown/unknown")
    owner, _, name = full_name.partition("/")
    owner = _html.escape(owner or "unknown")
    name = _html.escape(name or full_name)
    url = _html.escape(str(repo.get("html_url") or f"https://github.com/{full_name}"))
    avatar = _avatar_html(owner, repo.get("owner_avatar_url"), "", "fallback")
    return _STORY_TEMPLATE.format(url=url, story_avatar=avatar, name=name)


def _card_html(rank: int, repo: dict) -> str:
    full_name = str(repo.get("full_name") or "unknown/unknown")
    owner, _, name = full_name.partition("/")
    owner = _html.escape(owner or "unknown")
    name = _html.escape(name or full_name)
    url = _html.escape(str(repo.get("html_url") or f"https://github.com/{full_name}"))
    stars = _fmt_count(repo.get("stargazers_count"))
    issues = _fmt_count(repo.get("open_issues_count"))
    score = repo.get("base_score", 0.0) or 0.0
    description = _html.escape(str(repo.get("description") or "").strip()) or "No description."

    avatar = _avatar_html(owner, repo.get("owner_avatar_url"), "avatar", "avatar-fallback")

    signals = (repo.get("has_license"), repo.get("has_tests"), repo.get("has_ci"), repo.get("readme_has_code_blocks"))
    verified = _VERIFIED_SVG if all(signals) else ""

    language = repo.get("language")
    language_or_pushed = (
        _html.escape(str(language)) if language else f"pushed {_fmt_date(repo.get('pushed_at'))}"
    )

    topics = [str(t) for t in (repo.get("topics") or [])][:6]
    topics_html = ""
    if topics:
        chips = "".join(f'<span class="topic">{_html.escape(t)}</span>' for t in topics)
        topics_html = f'<div class="topics">{chips}</div>'

    badge_defs = [
        ("License", repo.get("has_license")),
        ("Tests", repo.get("has_tests")),
        ("CI", repo.get("has_ci")),
        ("Docs", repo.get("readme_has_code_blocks")),
    ]
    badges = [f'<span class="badge{" on" if on else ""}">{label}</span>' for label, on in badge_defs]
    badges_html = "".join(badges)

    return _POST_TEMPLATE.format(
        rank=rank,
        avatar=avatar,
        owner=owner,
        name=name,
        verified=verified,
        language_or_pushed=language_or_pushed,
        url=url,
        heart_svg=_HEART_SVG,
        stars=stars,
        comment_svg=_COMMENT_SVG,
        issues=issues,
        bookmark_svg=_BOOKMARK_SVG,
        score=f"{float(score):.3f}",
        description=description,
        topics_html=topics_html,
        badges_html=badges_html,
    )


def render_html(ranked: list[dict]) -> str:
    """Renders the stories strip (top 15 by rank) plus one post-card per repo.
    `ranked` is expected to already be junk-filtered, scored, sorted by
    base_score descending, and capped to the top ~100 by the caller
    (main.py) -- this function only renders what it's given."""
    if not ranked:
        return _PAGE_TEMPLATE.format(count=0, stories="", cards=_EMPTY_STATE)
    stories_html = "\n".join(_story_html(repo) for repo in ranked[:15])
    cards_html = "\n".join(_card_html(i, repo) for i, repo in enumerate(ranked, start=1))
    return _PAGE_TEMPLATE.format(count=len(ranked), stories=stories_html, cards=cards_html)
