from src.server import build_response


def test_health_endpoint_returns_ok():
    status_code, body = build_response("/health")

    assert status_code == 200
    assert body == {"status": "ok", "service": "task-model"}


def test_task_endpoint_returns_task_data(monkeypatch):
    monkeypatch.setenv("TASK_ID", "7")
    monkeypatch.setenv("TASK_DESCRIPTION", "Task from env")
    monkeypatch.setenv("TASK_PRIORITY", "4")
    monkeypatch.setenv("TASK_STATUS", "new")

    status_code, body = build_response("/task")

    assert status_code == 200
    assert body["id"] == 7
    assert body["description"] == "Task from env"
    assert body["priority"] == 4
    assert body["status"] == "new"
    assert body["status_label"] == "Новая"


def test_unknown_endpoint_returns_404():
    status_code, body = build_response("/unknown")

    assert status_code == 404
    assert body == {"error": "not found"}
