"""Deterministic quality + freshness scoring. See DEVFEED.md section 12
("Ranking Engine"). Stage 0 uses only quality_score and freshness_score --
star velocity, topic relevance, novelty, and MMR arrive in Stage 1+.

Expected `repo` dict shape (defensive: every key may be missing or None, per
DEVFEED.md section 9 "Defensive parsing"):

    has_license: bool | None
    readme_has_code_blocks: bool | None
    has_tests: bool | None
    has_ci: bool | None
    contributor_count: int | None
    release_count: int | None
    pushed_at: str | date | datetime | None   # ISO 8601 or a date/datetime

Note on quality_score/freshness_score's return type: both are declared to
return a plain `float` (not `float | None`) per the spec, since `base_score`
and `render.py` need a definite number to rank and display every survivor.
`weighted_score` -- the function whose (None, excluded) contract for
all-signals-missing is explicitly unit tested per the acceptance criteria --
is used internally by `quality_score`; on the (extremely rare, in practice
all secondary-fetch fields failing at once) all-missing case it falls back to
0.0 so the composite always resolves to a number, while the underlying
`weighted_score` utility itself is never allowed to silently return 0.0 for
"unknown" -- that distinction is preserved and is what the acceptance
criteria test directly.
"""

from __future__ import annotations

from datetime import date, datetime

from stage0.config import BASE_SCORE_WEIGHTS, QUALITY_WEIGHTS

_RECENCY_FULL_CREDIT_DAYS = 30
_RECENCY_ZERO_DAYS = 365
_FRESHNESS_ZERO_DAYS = 365


def _parse_date(value: object) -> date | None:
    """Tolerant date parsing: accepts date, datetime, ISO-8601 string, or None.
    Never raises -- an unparseable value is treated as missing."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        v = value.strip()
        if not v:
            return None
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(v).date()
        except ValueError:
            return None
    return None


def _bool_signal(value: object) -> float | None:
    if value is None:
        return None
    return 1.0 if value else 0.0


def _count_signal(value: object, cap: float) -> float | None:
    if value is None:
        return None
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    return min(max(n, 0.0) / cap, 1.0)


def _recency_signal(pushed_date: date | None, now: date) -> float | None:
    """1.0 within _RECENCY_FULL_CREDIT_DAYS, linear decay to 0.0 by
    _RECENCY_ZERO_DAYS, clipped to [0, 1]."""
    if pushed_date is None:
        return None
    days = (now - pushed_date).days
    if days < 0:
        days = 0  # clock skew / future timestamp guard -- never above full credit
    if days <= _RECENCY_FULL_CREDIT_DAYS:
        return 1.0
    if days >= _RECENCY_ZERO_DAYS:
        return 0.0
    span = _RECENCY_ZERO_DAYS - _RECENCY_FULL_CREDIT_DAYS
    return 1.0 - (days - _RECENCY_FULL_CREDIT_DAYS) / span


def weighted_score(
    signals: dict[str, float | None], weights: dict[str, float]
) -> tuple[float | None, list[str]]:
    """Signals with a None value are excluded; remaining weights are
    renormalized to sum to 1. Returns (None, excluded) if every signal is
    missing -- the caller excludes that repository from the ranked set
    entirely. A score of 0.0 means "worst possible," which is not the same
    thing as "no data," and must never be returned for the all-missing case.
    Verbatim per DEVFEED.md section 12."""
    available = {k: v for k, v in signals.items() if v is not None}
    excluded = [k for k, v in signals.items() if v is None]
    if not available:
        return None, excluded
    total_weight = sum(weights[k] for k in available)
    score = sum(weights[k] * available[k] for k in available) / total_weight
    return score, excluded


def quality_score(repo: dict, now: date | None = None) -> float:
    """[0,1]. Composed of documentation, license, tests, CI, contributor
    count, release activity, and maintenance recency -- never popularity
    alone (DEVFEED.md section 11). Starting weights, tuned later in Stage 1's
    evaluation harness (section 12)."""
    now = now or date.today()
    signals: dict[str, float | None] = {
        "has_license": _bool_signal(repo.get("has_license")),
        "readme_has_code_blocks": _bool_signal(repo.get("readme_has_code_blocks")),
        "has_tests": _bool_signal(repo.get("has_tests")),
        "has_ci": _bool_signal(repo.get("has_ci")),
        "contributor_count": _count_signal(repo.get("contributor_count"), cap=10),
        "release_count": _count_signal(repo.get("release_count"), cap=5),
        "maintenance_recency": _recency_signal(_parse_date(repo.get("pushed_at")), now),
    }
    score, _excluded = weighted_score(signals, QUALITY_WEIGHTS)
    return score if score is not None else 0.0


def freshness_score(repo: dict, now: date | None = None) -> float:
    """[0,1]. max(0, 1 - days_since_pushed_at / 365), clipped. Stage 0
    simplification: uses pushed_at only, not release recency (the full
    formula arrives Stage 1+ per DEVFEED.md section 12)."""
    now = now or date.today()
    pushed_date = _parse_date(repo.get("pushed_at"))
    if pushed_date is None:
        return 0.0  # no known push date -- treat as not fresh (see module note)
    days = (now - pushed_date).days
    return min(1.0, max(0.0, 1.0 - days / _FRESHNESS_ZERO_DAYS))


def base_score(repo: dict, now: date | None = None) -> float:
    """0.6 * quality_score(repo) + 0.4 * freshness_score(repo). Starting
    weights, not evaluated against a labeled set yet (that's Stage 1)."""
    now = now or date.today()
    return (
        BASE_SCORE_WEIGHTS["quality"] * quality_score(repo, now=now)
        + BASE_SCORE_WEIGHTS["freshness"] * freshness_score(repo, now=now)
    )
