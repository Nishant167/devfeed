from datetime import date

from stage0.query_grid import month_ranges, split_band_if_needed


# --- month_ranges ---


def test_month_ranges_fixed_today_matches_acceptance_criteria():
    # DEVFEED.md acceptance criteria #5: month_ranges(3, today=date(2026, 8, 27))
    # must be deterministic and hardcoded-assertable -- no wall-clock dependency.
    result = month_ranges(3, today=date(2026, 8, 27))
    assert result == [
        "2026-08-01..2026-08-31",
        "2026-07-01..2026-07-31",
        "2026-06-01..2026-06-30",
    ]


def test_month_ranges_single_month():
    result = month_ranges(1, today=date(2026, 2, 15))
    assert result == ["2026-02-01..2026-02-28"]


def test_month_ranges_year_rollover():
    result = month_ranges(2, today=date(2026, 1, 15))
    assert result == [
        "2026-01-01..2026-01-31",
        "2025-12-01..2025-12-31",
    ]


def test_month_ranges_leap_year_february():
    # 2028 is a leap year -> February has 29 days.
    result = month_ranges(2, today=date(2028, 3, 1))
    assert result == [
        "2028-03-01..2028-03-31",
        "2028-02-01..2028-02-29",
    ]


# --- split_band_if_needed ---


def test_split_band_if_needed_under_threshold_returns_unchanged():
    def probe(lang, star_band, date_range):
        return 500

    result = split_band_if_needed(
        "python", "100..250", "2026-08-01..2026-08-31", probe=probe
    )
    assert result == ["100..250"]


def test_split_band_if_needed_over_threshold_splits_in_two():
    def probe(lang, star_band, date_range):
        if star_band == "100..250":
            return 1500
        return 400  # both halves are under threshold -- recursion stops there

    result = split_band_if_needed(
        "python", "100..250", "2026-08-01..2026-08-31", probe=probe
    )
    assert result == ["100..175", "176..250"]


def test_split_band_if_needed_exact_boundary_does_not_split():
    def probe(lang, star_band, date_range):
        return 800  # exactly at threshold -- DEVFEED.md says "exceeds", i.e. strictly >

    result = split_band_if_needed(
        "python", "100..250", "2026-08-01..2026-08-31", threshold=800, probe=probe
    )
    assert result == ["100..250"]
