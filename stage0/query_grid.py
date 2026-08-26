"""Build the language x star-band x date-range query grid for GitHub Search.

See DEVFEED.md section 9 ("Query strategy -- language, star, and date slicing").

Design note (deviation from the spec's literal signatures, documented here and in
the final implementation report): `split_band_if_needed` and `build_query_grid`
need to probe GitHub's Search API for `total_count` per bucket, but this module
otherwise contains only pure, unit-testable logic. Rather than hard-coding a
network call inside these functions (making them untestable without mocking HTTP),
both accept an injected `probe` callable -- `(lang, star_band, date_range) -> int`.
In production, `main.py` passes `GitHubClient.probe_count` (see ingest.py). In
tests, a fake probe function drives the splitting logic deterministically. This
keeps the splitting *logic* pure and testable while the actual network I/O lives
where the rest of the untested I/O shell lives (ingest.py), consistent with
DEVFEED.md's `rank()` precedent of "pure function, no I/O" (section 12) and the
Testing Plan's expectation that `split_band_if_needed` itself is unit-testable
across "under threshold, over threshold, exact boundary" without a live API call.
"""

from __future__ import annotations

from calendar import monthrange
from datetime import date
from typing import Callable

from stage0.config import BUCKET_PROBE_THRESHOLD, LANGUAGES, MONTHS_BACK_DEFAULT, STAR_BANDS

# (lang, star_band, date_range) -> total_count
ProbeFn = Callable[[str, str, str], int]

# Recursion guard: a band that still exceeds the threshold after this many splits
# is accepted as-is rather than split forever (protects against pathological probe
# functions in tests and against genuinely unsplittable single-star bands).
_MAX_SPLIT_DEPTH = 8


def month_ranges(months_back: int = MONTHS_BACK_DEFAULT, today: date | None = None) -> list[str]:
    """Concrete 'YYYY-MM-DD..YYYY-MM-DD' month ranges for the trailing `months_back`
    months, most recent first. `today` is injectable so this is unit-testable without
    patching the clock (per DEVFEED.md section 9)."""
    today = today or date.today()
    ranges = []
    for i in range(months_back):
        y, m = today.year, today.month - i
        while m <= 0:
            m += 12
            y -= 1
        last_day = monthrange(y, m)[1]
        ranges.append(f"{y:04d}-{m:02d}-01..{y:04d}-{m:02d}-{last_day:02d}")
    return ranges


def _split_star_band(star_band: str) -> tuple[str, str] | None:
    """Split one star-band string into two adjacent, non-overlapping sub-bands.

    Returns None if the band cannot be usefully split further (width < 2, or a
    malformed band string).
    """
    if star_band.startswith(">"):
        lo = int(star_band[1:])
        hi = lo * 2
        return f"{lo}..{hi}", f">{hi}"

    lo_str, hi_str = star_band.split("..")
    lo, hi = int(lo_str), int(hi_str)
    if hi - lo < 2:
        return None
    mid = lo + (hi - lo) // 2
    return f"{lo}..{mid}", f"{mid + 1}..{hi}"


def split_band_if_needed(
    lang: str,
    star_band: str,
    date_range: str,
    threshold: int = BUCKET_PROBE_THRESHOLD,
    *,
    probe: ProbeFn,
    _depth: int = 0,
) -> list[str]:
    """Probes total_count for one (lang, star_band, date_range) bucket via `probe`
    (a single count-only Search request in production, no pagination) and splits
    the star band further if the count exceeds `threshold`. Returns one or more
    star-band strings to actually query.

    Recurses on each half until every resulting sub-band is at or under the
    threshold, or the band can no longer be split (or _MAX_SPLIT_DEPTH is hit).
    """
    total_count = probe(lang, star_band, date_range)

    if total_count <= threshold or _depth >= _MAX_SPLIT_DEPTH:
        return [star_band]

    halves = _split_star_band(star_band)
    if halves is None:
        return [star_band]

    left, right = halves
    return split_band_if_needed(
        lang, left, date_range, threshold, probe=probe, _depth=_depth + 1
    ) + split_band_if_needed(
        lang, right, date_range, threshold, probe=probe, _depth=_depth + 1
    )


def build_query_grid(
    months_back: int, *, probe: ProbeFn
) -> list[tuple[str, str, str]]:
    """Returns (language, star_band, date_range) tuples, pre-split via
    split_band_if_needed. Starting grid: LANGUAGES x STAR_BANDS x month_ranges."""
    grid: list[tuple[str, str, str]] = []
    for lang in LANGUAGES:
        for star_band in STAR_BANDS:
            for date_range in month_ranges(months_back):
                for actual_band in split_band_if_needed(
                    lang, star_band, date_range, probe=probe
                ):
                    grid.append((lang, actual_band, date_range))
    return grid
