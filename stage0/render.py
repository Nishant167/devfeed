"""Static HTML rendering of the ranked feed. See DEVFEED.md section 28 (item 5:
"A static HTML page rendering the top ~100 results with repository,
description, stars, and score."). Plain HTML/CSS, no framework, no JS.

Visual design ported from a Figma Make React/Tailwind mockup the project owner
supplied (colors, typography, card layout) -- but scoped to what Stage 0
actually has. Deliberately does NOT include: a working search box, tabs
(trending/starred), a bottom nav, star/watch buttons, or "starred by people
you follow" -- all of that implies interactivity, accounts, or a social layer
that don't exist yet (Stage 2+ / Stage 10, DEVFEED.md sections 20/21/18). The
one real, working action is "Open on GitHub". Quality badges (License/Tests/
CI/Docs) are driven by the actual computed signals, not fabricated
CI-passing/coverage numbers like the mockup had.

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
    --primary-foreground: #ffffff;
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
    background: var(--background);
    color: var(--foreground);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: 0;
    -webkit-font-smoothing: antialiased;
  }}
  header {{
    position: sticky; top: 0; z-index: 10;
    background: rgba(10,10,15,0.9);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 14px 16px;
  }}
  .header-inner {{ max-width: 640px; margin: 0 auto; }}
  .brand {{
    display: flex; align-items: baseline; gap: 8px;
    font-family: 'Fraunces', serif; font-size: 20px; font-weight: 700;
    letter-spacing: -0.4px;
  }}
  .brand .dot {{ color: var(--primary); }}
  .subtitle {{ margin: 4px 0 0; font-size: 12.5px; color: var(--muted-foreground); }}
  main {{ max-width: 640px; margin: 0 auto; padding: 16px 16px 60px; display: flex; flex-direction: column; gap: 10px; }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
  }}
  .card-head {{ padding: 14px 16px 10px; display: flex; gap: 12px; align-items: flex-start; }}
  .avatar {{
    width: 34px; height: 34px; border-radius: 8px; flex-shrink: 0;
    border: 1px solid var(--border); object-fit: cover; background: var(--secondary);
  }}
  .avatar-fallback {{
    width: 34px; height: 34px; border-radius: 8px; flex-shrink: 0;
    border: 1px solid var(--border); background: var(--secondary);
    display: flex; align-items: center; justify-content: center;
    color: var(--muted-foreground); font-size: 13px; font-weight: 600;
  }}
  .title-row {{ display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap; }}
  .rank {{ color: var(--muted-foreground); font-size: 12px; margin-right: 2px; }}
  .owner {{ font-size: 13px; color: var(--muted-foreground); }}
  .slash {{ color: var(--border); font-size: 13px; }}
  .name {{ font-size: 15px; font-weight: 700; color: var(--foreground); letter-spacing: -0.2px; }}
  .name a {{ color: inherit; text-decoration: none; }}
  .name a:hover {{ text-decoration: underline; }}
  .desc {{ margin: 6px 0 0; font-size: 13px; color: var(--secondary-foreground); line-height: 1.5; }}
  .topics {{ padding: 0 16px 12px; display: flex; gap: 6px; flex-wrap: wrap; }}
  .topic {{
    font-size: 11px; font-weight: 500; color: #a78bfa;
    background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.2);
    border-radius: 20px; padding: 3px 9px; letter-spacing: 0.02em;
  }}
  .stats {{
    padding: 10px 16px; border-top: 1px solid var(--border);
    display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
    font-size: 12px; color: var(--muted-foreground);
  }}
  .stat {{ display: flex; align-items: center; gap: 5px; }}
  .lang-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; flex-shrink: 0; }}
  .score {{ margin-left: auto; font-size: 12px; color: var(--accent); font-weight: 600; }}
  .badges {{ padding: 0 16px 12px; display: flex; gap: 6px; flex-wrap: wrap; }}
  .badge {{
    font-size: 11px; border-radius: 4px; padding: 3px 8px; border: 1px solid var(--border);
    color: var(--muted-foreground); background: rgba(255,255,255,0.03);
  }}
  .badge.on {{ color: #4ade80; background: #22c55e1a; border-color: #22c55e4d; }}
  .actions {{ padding: 12px 16px; border-top: 1px solid var(--border); display: flex; align-items: center; gap: 8px; }}
  .open-btn {{
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--secondary); color: var(--foreground);
    border: 1px solid var(--border); border-radius: 8px;
    padding: 7px 14px; font-size: 13px; font-weight: 600;
    text-decoration: none; transition: border-color 0.15s;
  }}
  .open-btn:hover {{ border-color: rgba(124,58,237,0.4); }}
  .updated {{ margin-left: auto; font-size: 11px; color: var(--muted-foreground); }}
  .empty {{ text-align: center; padding: 60px 0; color: var(--muted-foreground); font-size: 14px; }}
</style>
</head>
<body>
<header>
  <div class="header-inner">
    <div class="brand">devfeed<span class="dot">.</span></div>
  </div>
</header>
<main>
{cards}
</main>
</body>
</html>
"""

_CARD_TEMPLATE = """<article class="card">
  <div class="card-head">
    {avatar}
    <div style="flex:1;min-width:0;">
      <div class="title-row">
        <span class="rank">#{rank}</span>
        <span class="owner">{owner}</span>
        <span class="slash">/</span>
        <span class="name"><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></span>
      </div>
      <p class="desc">{description}</p>
    </div>
  </div>
  {topics_html}
  <div class="stats">
    {lang_html}
    <div class="stat">&#9733; {stars}</div>
    {forks_html}
    {issues_html}
    <div class="stat">{contributors} contributors</div>
    <div class="score">score {score}</div>
  </div>
  <div class="badges">{badges_html}</div>
  <div class="actions">
    <a class="open-btn" href="{url}" target="_blank" rel="noopener noreferrer">Open on GitHub</a>
    <span class="updated">Pushed {pushed_at}</span>
  </div>
</article>"""

_EMPTY_STATE = '<p class="empty">No repositories survived filtering and scoring.</p>'

_LANG_COLORS: dict[str, str] = {
    "Python": "#3572a5",
    "TypeScript": "#3178c6",
    "JavaScript": "#f7df1e",
    "Rust": "#dea584",
    "Go": "#00add8",
}


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


def _card_html(rank: int, repo: dict) -> str:
    full_name = str(repo.get("full_name") or "unknown/unknown")
    owner, _, name = full_name.partition("/")
    owner = _html.escape(owner or "unknown")
    name = _html.escape(name or full_name)
    url = _html.escape(str(repo.get("html_url") or f"https://github.com/{full_name}"))
    stars = _fmt_count(repo.get("stargazers_count"))
    score = repo.get("base_score", 0.0) or 0.0
    description = _html.escape(str(repo.get("description") or "").strip()) or "No description."

    avatar_url = repo.get("owner_avatar_url")
    if avatar_url:
        avatar = f'<img class="avatar" src="{_html.escape(str(avatar_url))}" alt="{owner}" loading="lazy">'
    else:
        initial = _html.escape((owner[:1] or "?").upper())
        avatar = f'<div class="avatar-fallback">{initial}</div>'

    topics = [str(t) for t in (repo.get("topics") or [])][:6]
    if topics:
        chips = "".join(f'<span class="topic">{_html.escape(t)}</span>' for t in topics)
        topics_html = f'<div class="topics">{chips}</div>'
    else:
        topics_html = ""

    language = repo.get("language")
    if language:
        color = _LANG_COLORS.get(str(language), "#888")
        lang_html = (
            f'<div class="stat"><span class="lang-dot" style="background:{color}"></span>'
            f"{_html.escape(str(language))}</div>"
        )
    else:
        lang_html = ""

    forks = repo.get("forks_count")
    forks_html = f'<div class="stat">{_fmt_count(forks)} forks</div>' if forks is not None else ""

    issues = repo.get("open_issues_count")
    issues_html = f'<div class="stat">{_fmt_count(issues)} open issues</div>' if issues is not None else ""

    badges = []
    if repo.get("has_license"):
        badges.append('<span class="badge on">License</span>')
    if repo.get("has_tests"):
        badges.append('<span class="badge on">Tests</span>')
    if repo.get("has_ci"):
        badges.append('<span class="badge on">CI</span>')
    if repo.get("readme_has_code_blocks"):
        badges.append('<span class="badge on">Docs</span>')
    badges_html = "".join(badges) if badges else '<span class="badge">No quality signals detected</span>'

    return _CARD_TEMPLATE.format(
        rank=rank,
        avatar=avatar,
        owner=owner,
        name=name,
        url=url,
        description=description,
        topics_html=topics_html,
        lang_html=lang_html,
        stars=stars,
        forks_html=forks_html,
        issues_html=issues_html,
        contributors=repo.get("contributor_count", 0) or 0,
        score=f"{float(score):.3f}",
        badges_html=badges_html,
        pushed_at=_fmt_date(repo.get("pushed_at")),
    )


def render_html(ranked: list[dict]) -> str:
    """Renders one card per repo. `ranked` is expected to already be
    junk-filtered, scored, sorted by base_score descending, and capped to the
    top ~100 by the caller (main.py) -- this function only renders what it's
    given."""
    if not ranked:
        cards_html = _EMPTY_STATE
    else:
        cards_html = "\n".join(_card_html(i, repo) for i, repo in enumerate(ranked, start=1))
    return _PAGE_TEMPLATE.format(count=len(ranked), cards=cards_html)
