import io
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import urllib.error

from morgen_api import (
    MorgenAPIClient,
    MorgenAPIError,
    MorgenAuthError,
    MorgenNetworkError,
    MorgenRateLimitError,
    MorgenValidationError,
)


class _FakeHTTPResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeHTTPResponseBytes:
    def __init__(self, raw: bytes):
        self._raw = raw

    def read(self):
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _http_error(code: int, body: str = "") -> urllib.error.HTTPError:
    fp = io.BytesIO(body.encode("utf-8"))
    return urllib.error.HTTPError(
        url="https://api.morgen.so/v3/tasks/list?limit=100",
        code=code,
        msg="error",
        hdrs=None,
        fp=fp,
    )


def test_make_request_success_parses_json():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", return_value=_FakeHTTPResponse({"ok": True})) as _:
        resp = client._make_request("/tasks/list?limit=1")
    assert resp == {"ok": True}


def test_make_request_empty_body_returns_empty_dict():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", return_value=_FakeHTTPResponseBytes(b"")) as _:
        resp = client._make_request("/tasks/close", method="POST", data={"id": "t"})
    assert resp == {}


def test_make_request_401_raises_auth_error():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", side_effect=_http_error(401, "nope")):
        with pytest.raises(MorgenAuthError) as e:
            client._make_request("/tasks/list?limit=1")
    assert e.value.status_code == 401
    assert e.value.response_body == "nope"


def test_make_request_429_raises_rate_limit_error():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", side_effect=_http_error(429, "slow down")):
        with pytest.raises(MorgenRateLimitError) as e:
            client._make_request("/tasks/list?limit=1")
    assert e.value.status_code == 429


def test_make_request_400_raises_validation_error():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", side_effect=_http_error(400, "bad")):
        with pytest.raises(MorgenValidationError) as e:
            client._make_request("/tasks/create", method="POST", data={"title": ""})
    assert e.value.status_code == 400
    assert "bad" in e.value.message


def test_make_request_other_http_error_raises_generic_api_error():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", side_effect=_http_error(500, "boom")):
        with pytest.raises(MorgenAPIError) as e:
            client._make_request("/tasks/list?limit=1")
    assert e.value.status_code == 500
    assert "boom" in e.value.message


def test_make_request_url_error_raises_network_error():
    client = MorgenAPIClient("k")
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("dns fail")):
        with pytest.raises(MorgenNetworkError) as e:
            client._make_request("/tasks/list?limit=1")
    assert "dns fail" in e.value.message


def test_make_request_invalid_json_raises_api_error():
    client = MorgenAPIClient("k")

    class _BadJSONResponse(_FakeHTTPResponse):
        def read(self):
            return b"not json"

    with patch("urllib.request.urlopen", return_value=_BadJSONResponse({"x": 1})):
        with pytest.raises(MorgenAPIError) as e:
            client._make_request("/tasks/list?limit=1")
    assert "Invalid JSON response" in e.value.message


def test_list_tasks_caps_limit_to_100():
    client = MorgenAPIClient("k")
    captured = {}

    def _capture(endpoint, method="GET", data=None):
        captured["endpoint"] = endpoint
        return {"data": {"tasks": []}}

    client._make_request = _capture  # type: ignore[method-assign]
    client.list_tasks(limit=999)
    assert captured["endpoint"].startswith("/tasks/list?limit=100")


def test_create_task_validates_priority_and_due_format():
    client = MorgenAPIClient("k")

    with pytest.raises(ValueError):
        client.create_task("x", priority=-1)
    with pytest.raises(ValueError):
        client.create_task("x", priority=10)

    with pytest.raises(ValueError):
        client.create_task("x", due="2026-02-10T09:00")  # wrong length
    with pytest.raises(ValueError):
        client.create_task("x", due="2026/02/10T09:00:00")  # wrong separators


def test_close_task_calls_close_endpoint():
    client = MorgenAPIClient("k")
    captured = {}

    def _capture(endpoint, method="GET", data=None):
        captured["endpoint"] = endpoint
        captured["method"] = method
        captured["data"] = data
        return {}

    client._make_request = _capture  # type: ignore[method-assign]
    assert client.close_task("task-123") == {}
    assert captured["endpoint"] == "/tasks/close"
    assert captured["method"] == "POST"
    assert captured["data"] == {"id": "task-123"}
