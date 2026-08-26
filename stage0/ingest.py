"""GitHub API client (paced Search calls, core-REST secondary fetches, 403/5xx
backoff+jitter) and the raw payload store. See DEVFEED.md section 9.

This module is the untested I/O shell (per the spec's Testing Plan: "The GitHub
API calls, backoff/retry logic, and HTML rendering stay untested -- this is the
I/O shell, not the pure logic"). `RawPayloadStore.put/get/exists` on the real
filesystem IS covered by an integration test (test_ingest.py), since that's a
plain round-trip with no network involved.
"""

from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Protocol

import httpx

from stage0.config import SEARCH_REQUEST_INTERVAL_SECONDS

GITHUB_API_BASE = "https://api.github.com"


def make_run_id(now: float | None = None) -> str:
    """Fresh run_id per invocation -- 'run-{timestamp}'. No resume/checkpoint
    logic (deliberately dropped from the spec): each invocation starts over
    cleanly, and a distinct run_id per invocation is what keeps raw payloads
    from different runs from ever overwriting each other."""
    ts = int(now if now is not None else time.time())
    return f"run-{ts}"


class RawPayloadStore(Protocol):
    """Key convention: 'github/{YYYY-MM-DD}/{run_id}/{search|repositories}/
    {identifier}.json'. run_id (not just date) so a same-day re-run never
    overwrites a prior run's snapshot."""

    def put(self, key: str, payload: bytes) -> None: ...
    def get(self, key: str) -> bytes: ...
    def exists(self, key: str) -> bool: ...


class FilesystemRawPayloadStore:
    """Stage 0 implementation of RawPayloadStore: local disk. Adequate because
    nothing is deployed yet and nothing is expected to survive between runs
    (DEVFEED.md section 9). Default root lands payloads at
    data/raw/github/{date}/{run_id}/... to match the repo's file layout."""

    def __init__(self, root: Path | str = "data/raw") -> None:
        self.root = Path(root)

    def _path(self, key: str) -> Path:
        return self.root / key

    def put(self, key: str, payload: bytes) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)

    def get(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    def exists(self, key: str) -> bool:
        return self._path(key).exists()


class GitHubTransientError(RuntimeError):
    """Raised when a request exhausts its retry budget against 403/5xx."""


class GitHubClient:
    """Authenticated GitHub API client.

    - `search()` / `probe_count()` hit the Search API, paced at a fixed
      interval so ingestion sleeps proactively before hitting the Search
      API's stricter 30 requests/minute limit, rather than reacting to a 403
      (DEVFEED.md section 9, "GitHub API usage").
    - The `get_*` secondary-fetch methods hit the general core-REST endpoints
      (5,000/hour, not paced the same way -- monitored via
      X-RateLimit-Remaining instead).
    - All requests back off with jitter on 403 and 5xx responses.
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str = GITHUB_API_BASE,
        transport: httpx.BaseTransport | None = None,
        search_interval_seconds: float = SEARCH_REQUEST_INTERVAL_SECONDS,
    ) -> None:
        self._token = token
        self._search_interval_seconds = search_interval_seconds
        self._last_search_request_at: float = 0.0
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=30.0,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # --- Search API ---

    def _pace_search(self) -> None:
        elapsed = time.monotonic() - self._last_search_request_at
        wait = self._search_interval_seconds - elapsed
        if wait > 0:
            time.sleep(wait)
        self._last_search_request_at = time.monotonic()

    def search(self, query: str, page: int = 1, per_page: int = 100) -> dict:
        """One Search API page, paced against the Search rate limit."""
        return self._request_json(
            "GET",
            "/search/repositories",
            params={"q": query, "page": page, "per_page": per_page},
            pace_fn=self._pace_search,
        )

    def probe_count(self, lang: str, star_band: str, date_range: str) -> int:
        """Single count-only Search request (per_page=1) -- returns
        total_count for one (language, star_band, date_range) bucket. This is
        the `probe` callable passed to stage0.query_grid.build_query_grid."""
        query = f"language:{lang} stars:{star_band} pushed:{date_range}"
        data = self._request_json(
            "GET",
            "/search/repositories",
            params={"q": query, "page": 1, "per_page": 1},
            pace_fn=self._pace_search,
        )
        return int(data.get("total_count", 0) or 0)

    # --- Core REST secondary fetches ---

    def get_repo(self, full_name: str) -> dict:
        return self._request_json("GET", f"/repos/{full_name}")

    def get_readme(self, full_name: str) -> dict | None:
        try:
            return self._request_json("GET", f"/repos/{full_name}/readme")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    def get_contributors(self, full_name: str, per_page: int = 100) -> list[dict]:
        try:
            data = self._request_json(
                "GET",
                f"/repos/{full_name}/contributors",
                params={"per_page": per_page, "anon": "0"},
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (404, 403):
                return []
            raise
        return data if isinstance(data, list) else []

    def get_releases(self, full_name: str, per_page: int = 100) -> list[dict]:
        try:
            data = self._request_json(
                "GET", f"/repos/{full_name}/releases", params={"per_page": per_page}
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (404, 403):
                return []
            raise
        return data if isinstance(data, list) else []

    def path_exists(self, full_name: str, path: str) -> bool:
        """True if `path` exists in the repo's default branch (used to
        approximate has_ci by checking for .github/workflows, and has_tests
        by checking common test directory names)."""
        try:
            self._request_json("GET", f"/repos/{full_name}/contents/{path}")
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return False
            raise

    # --- Shared request/backoff plumbing ---

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        headers: dict | None = None,
        pace_fn=None,
        max_retries: int = 5,
    ) -> dict | list:
        attempt = 0
        while True:
            if pace_fn is not None:
                pace_fn()
            response = self._client.request(method, path, params=params, headers=headers)
            if response.status_code == 403 or response.status_code >= 500:
                attempt += 1
                if attempt > max_retries:
                    response.raise_for_status()
                self._backoff(response, attempt)
                continue
            response.raise_for_status()
            return response.json()

    def _backoff(self, response: httpx.Response, attempt: int) -> None:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                delay = float(retry_after)
            except ValueError:
                delay = min(2**attempt, 60)
        else:
            delay = min(2**attempt, 60)
        delay += random.uniform(0, 1)  # jitter
        time.sleep(delay)
