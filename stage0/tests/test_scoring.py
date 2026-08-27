from datetime import date, timedelta

import pytest

from stage0.scoring import base_score, freshness_score, quality_score, weighted_score

TODAY = date(2026, 8, 27)


# --- quality_score ---


def test_quality_score_happy_path_all_signals_present_and_maxed():
    repo = {
        "has_license": True,
        "readme_has_code_blocks": True,
        "has_tests": True,
        "has_ci": True,
        "contributor_count": 20,  # >= 10 -> capped signal of 1.0
        "release_count": 10,  # >= 5 -> capped signal of 1.0
        "pushed_at": TODAY,  # 0 days since push -> full recency credit
    }
    assert quality_score(repo, now=TODAY) == pytest.approx(1.0)


def test_quality_score_missing_fields_excludes_and_renormalizes():
    repo = {
        "has_license": True,  # 1.0, w=0.15
        "readme_has_code_blocks": True,  # 1.0, w=0.20
        "has_tests": False,  # 0.0, w=0.15
        "has_ci": None,  # missing -> excluded
        "contributor_count": 5,  # 0.5, w=0.15
        "release_count": None,  # missing -> excluded
        "pushed_at": TODAY,  # 1.0, w=0.10
    }
    # available weight = 0.15+0.20+0.15+0.15+0.10 = 0.75
    # weighted sum = 0.15*1 + 0.20*1 + 0.15*0 + 0.15*0.5 + 0.10*1 = 0.525
    # score = 0.525 / 0.75 = 0.7
    assert quality_score(repo, now=TODAY) == pytest.approx(0.7)


def test_quality_score_all_signals_missing_returns_zero_not_exception():
    # quality_score's declared return type is a plain float (not Optional), so
    # the all-missing case falls back to 0.0 -- see the module docstring for
    # why this is distinct from weighted_score's own None contract, which is
    # tested directly below.
    assert quality_score({}, now=TODAY) == 0.0


# --- freshness_score ---


def test_freshness_score_happy_path_pushed_today():
    assert freshness_score({"pushed_at": TODAY}, now=TODAY) == pytest.approx(1.0)


def test_freshness_score_boundary_365_days_is_zero():
    pushed = TODAY - timedelta(days=365)
    assert freshness_score({"pushed_at": pushed}, now=TODAY) == pytest.approx(0.0)


def test_freshness_score_missing_pushed_at_returns_zero():
    assert freshness_score({}, now=TODAY) == 0.0


def test_freshness_score_partial_decay():
    pushed = TODAY - timedelta(days=182)
    expected = 1 - 182 / 365
    assert freshness_score({"pushed_at": pushed}, now=TODAY) == pytest.approx(expected)


# --- weighted_score ---


def test_weighted_score_all_signals_present():
    signals = {"a": 1.0, "b": 0.5}
    weights = {"a": 0.5, "b": 0.5}
    score, excluded = weighted_score(signals, weights)
    assert score == pytest.approx(0.75)
    assert excluded == []


def test_weighted_score_some_excluded_and_renormalized():
    signals = {"a": 1.0, "b": None, "c": 0.4}
    weights = {"a": 0.5, "b": 0.3, "c": 0.2}
    score, excluded = weighted_score(signals, weights)
    # available weight = 0.5 + 0.2 = 0.7; weighted sum = 0.5*1.0 + 0.2*0.4 = 0.58
    assert score == pytest.approx(0.58 / 0.7)
    assert excluded == ["b"]


def test_weighted_score_empty_dict_returns_none_never_zero():
    # DEVFEED.md acceptance criteria #4, verbatim: weighted_score({}, weights)
    # returns (None, [...]), never (0.0, [...]).
    weights = {"a": 0.5, "b": 0.5}
    score, excluded = weighted_score({}, weights)
    assert score is None
    assert excluded == []


def test_weighted_score_all_signals_present_but_none_returns_none():
    signals = {"a": None, "b": None}
    weights = {"a": 0.5, "b": 0.5}
    score, excluded = weighted_score(signals, weights)
    assert score is None
    assert excluded == ["a", "b"]


# --- base_score ---


def test_base_score_combines_quality_and_freshness_with_stage0_weights():
    repo = {
        "has_license": True,
        "readme_has_code_blocks": True,
        "has_tests": True,
        "has_ci": True,
        "contributor_count": 20,
        "release_count": 10,
        "pushed_at": TODAY,
    }
    # quality_score == 1.0, freshness_score == 1.0 -> base_score == 0.6*1 + 0.4*1 == 1.0
    assert base_score(repo, now=TODAY) == pytest.approx(1.0)
