import httpx

from stage0.ingest import FilesystemRawPayloadStore, GitHubClient, make_run_id


def test_filesystem_raw_payload_store_put_get_roundtrip(tmp_path):
    store = FilesystemRawPayloadStore(root=tmp_path)
    key = "github/2026-08-27/run-1/search/python_100..250_2026-08-01..2026-08-31_p1.json"
    payload = b'{"total_count": 42, "items": []}'

    store.put(key, payload)

    assert store.get(key) == payload


def test_filesystem_raw_payload_store_exists_reflects_put(tmp_path):
    store = FilesystemRawPayloadStore(root=tmp_path)
    key = "github/2026-08-27/run-1/repositories/foo_bar.json"

    assert store.exists(key) is False

    store.put(key, b"{}")

    assert store.exists(key) is True


def test_make_run_id_is_distinct_across_different_timestamps():
    # DEVFEED.md acceptance criteria #2: raw payloads from separate runs are
    # never overwritten -- this holds only because run_id is fresh every
    # invocation. A distinct timestamp must produce a distinct run_id.
    first = make_run_id(now=1000.0)
    second = make_run_id(now=2000.0)
    assert first != second
    assert first.startswith("run-")


def test_path_exists_true_on_200():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"name": "tests", "type": "dir"})

    with GitHubClient("fake-token", transport=httpx.MockTransport(handler)) as client:
        assert client.path_exists("owner/repo", "tests") is True


def test_path_exists_false_on_404():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "Not Found"})

    with GitHubClient("fake-token", transport=httpx.MockTransport(handler)) as client:
        assert client.path_exists("owner/repo", "tests") is False


def test_path_exists_false_on_persistent_403_not_raised(monkeypatch):
    """Regression test: a real overnight run crashed here. GitHub returns a
    persistent 403 (e.g. an access-blocked repo) that retrying never resolves.
    path_exists must degrade to False like a 404, never propagate -- one
    repo's blocked status must not be able to kill the whole secondary-fetch
    batch (DEVFEED.md section 9: "one repository's failure never takes down
    the whole ingestion run")."""
    monkeypatch.setattr("time.sleep", lambda *_args, **_kwargs: None)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"message": "Repository access blocked"})

    with GitHubClient("fake-token", transport=httpx.MockTransport(handler)) as client:
        assert client.path_exists("owner/blocked-repo", "tests") is False


def test_secondary_fetches_are_paced(monkeypatch):
    """Regression test: a live overnight run needed ~18h at the observed rate
    because secondary-fetch requests (readme/contributors/releases/
    path_exists) fired back-to-back with zero delay, tripping GitHub's
    secondary/abuse rate limiter well before the primary 5,000/hour budget
    was anywhere near exhausted. Every secondary-fetch call must go through
    the same pacing mechanism as Search."""
    sleep_calls: list[float] = []
    monkeypatch.setattr("time.sleep", lambda seconds: sleep_calls.append(seconds))

    call_count = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        call_count["n"] += 1
        return httpx.Response(200, json={"content": "", "encoding": "base64"})

    client = GitHubClient(
        "fake-token",
        transport=httpx.MockTransport(handler),
        secondary_interval_seconds=0.5,
    )
    try:
        client.get_readme("owner/repo-a")
        client.get_readme("owner/repo-b")
    finally:
        client.close()

    assert call_count["n"] == 2
    # First call has nothing to wait on (elapsed since epoch-zero exceeds the
    # interval); the second call must have paced at least once.
    assert len(sleep_calls) >= 1
    assert any(s > 0 for s in sleep_calls)
