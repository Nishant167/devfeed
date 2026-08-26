from stage0.ingest import FilesystemRawPayloadStore, make_run_id


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
