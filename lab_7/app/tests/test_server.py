from __future__ import annotations

from src.server import build_response, route_for_metrics


def test_health_response() -> None:
    status_code, body = build_response("/health")

    assert status_code == 200
    assert body["status"] == "ok"


def test_task_response_contains_task_data() -> None:
    status_code, body = build_response("/task")

    assert status_code == 200
    assert body["id"] == 7
    assert body["status"] == "new"


def test_unknown_path_uses_low_cardinality_route() -> None:
    assert route_for_metrics("/task/123") == "not_found"
