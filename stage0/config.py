"""Stage 0 constants: query grid, rate limits, thresholds, junk patterns.

See DEVFEED.md section 9 (GitHub ingestion) and section 11 (junk patterns).
"""

from __future__ import annotations

# --- Query grid (DEVFEED.md section 9) ---

LANGUAGES = ["python", "typescript", "rust", "go"]

STAR_BANDS = ["50..100", "100..250", "250..1000", "1000..5000", ">5000"]

MONTHS_BACK_DEFAULT = 3

# --- GitHub Search API pacing (DEVFEED.md section 9, "GitHub API usage") ---
# The Search API's authenticated rate limit is 30 requests/minute -- stricter than,
# and separate from, the general core-REST limit of 5,000/hour used for secondary
# fetches (repository detail, README, contributors, releases).
SEARCH_RATE_LIMIT_PER_MIN = 30

# Fixed delay between Search API requests, paced against SEARCH_RATE_LIMIT_PER_MIN
# with a small margin so ingestion sleeps proactively before exhaustion rather than
# reacting to a 403. 60s / 30 requests = 2.0s; padded to ~2.2s per request.
SEARCH_REQUEST_INTERVAL_SECONDS = 2.2

# --- Secondary-fetch pacing (discovered live: GitHub's secondary/abuse rate
# limiter can return 403 on core-REST endpoints well before the primary
# 5,000/hour budget is exhausted, if requests fire back-to-back with no
# delay. This is separate from -- and not documented anywhere near as
# clearly as -- the primary rate limit. A modest fixed delay between
# secondary-fetch requests (readme/contributors/releases/path_exists) avoids
# triggering it, which in practice is *faster* end-to-end than hitting 403s
# and paying exponential retry-backoff on nearly every other repo.) ---
SECONDARY_REQUEST_INTERVAL_SECONDS = 0.5

# --- Bucket-size probe (DEVFEED.md section 9, "Query strategy") ---
# A bucket whose probed total_count exceeds this threshold gets its star band split
# further before the real, paginated query runs -- leaves headroom under GitHub's
# 1,000-result Search API cap.
BUCKET_PROBE_THRESHOLD = 800

# --- Secondary-fetch cap (DEVFEED.md section 9, "Defensive parsing") ---
# Survivors of the metadata-only filter are capped at this ceiling, sorted by a
# metadata-only score (stars + recency), before the secondary-fetch step (README,
# contributors, releases) runs -- keeps ingestion inside an unattended overnight run.
SECONDARY_FETCH_CAP = 2000

# --- Junk patterns (DEVFEED.md section 11, "Junk patterns") ---
# Maintained as configuration, not hard-coded into application logic. Matching is
# whole-token, not substring -- see stage0/filter.py:is_junk.
JUNK_PATTERNS = [
    "awesome-",
    "-awesome",
    "tutorial",
    "course",
    "bootcamp",
    "interview-",
    "-questions",
    "roadmap",
    "cheatsheet",
    "dotfiles",
    "my-portfolio",
    "learning-",
    "100-days",
    "leetcode",
    "hackerrank",
    "curriculum",
    "resources",
    "-notes",
    "study-",
    "practice-",
    "assignment",
]

# --- Scoring weights (DEVFEED.md section 12, Stage 0 simplification: quality + freshness only) ---

QUALITY_WEIGHTS = {
    "has_license": 0.15,
    "readme_has_code_blocks": 0.20,
    "has_tests": 0.15,
    "has_ci": 0.15,
    "contributor_count": 0.15,
    "release_count": 0.10,
    "maintenance_recency": 0.10,
}

BASE_SCORE_WEIGHTS = {
    "quality": 0.6,
    "freshness": 0.4,
}
