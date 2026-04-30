from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from src.task import Task


def get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def create_task_from_env() -> Task:
    return Task(
        id=get_env_int("TASK_ID", 1),
        description=os.getenv("TASK_DESCRIPTION", "Demo task for Kubernetes"),
        priority=get_env_int("TASK_PRIORITY", 3),
        status=os.getenv("TASK_STATUS", "new"),
    )


def task_to_dict(task: Task) -> dict[str, Any]:
    return {
        "id": task.id,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "status_label": task.status_label,
        "is_completed": task.is_completed,
        "created_at": task.created_at.isoformat(),
    }


def build_response(path: str) -> tuple[int, dict[str, Any]]:
    if path == "/health":
        return 200, {"status": "ok", "service": "task-model"}

    if path == "/task":
        return 200, task_to_dict(create_task_from_env())

    if path == "/":
        return 200, {
            "service": "task-model",
            "endpoints": {
                "/health": "health check",
                "/task": "task data",
            },
        }

    return 404, {"error": "not found"}


class TaskRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        status_code, body = build_response(self.path)
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def run_server() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = get_env_int("PORT", 8000)

    server = HTTPServer((host, port), TaskRequestHandler)
    print(f"Task model server started on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
