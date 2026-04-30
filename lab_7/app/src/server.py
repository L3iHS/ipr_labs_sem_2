from __future__ import annotations

import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.observability import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
    TASK_RESPONSES_TOTAL,
    setup_tracing,
)
from src.task import Task

TRACER = setup_tracing()


def get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def create_task_from_env() -> Task:
    return Task(
        id=get_env_int("TASK_ID", 7),
        description=os.getenv("TASK_DESCRIPTION", "Task from lab_7"),
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


def route_for_metrics(path: str) -> str:
    if path in {"/", "/health", "/task", "/metrics"}:
        return path
    return "not_found"


def build_response(path: str) -> tuple[int, dict[str, Any]]:
    if path == "/health":
        return 200, {"status": "ok", "service": "task-model-lab7"}

    if path == "/task":
        task = create_task_from_env()
        TASK_RESPONSES_TOTAL.labels(status=task.status).inc()
        return 200, task_to_dict(task)

    if path == "/":
        return 200, {
            "service": "task-model-lab7",
            "endpoints": {
                "/health": "health check",
                "/task": "task data",
                "/metrics": "Prometheus metrics",
            },
        }

    return 404, {"error": "not found"}


class TaskRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        started_at = time.perf_counter()
        route = route_for_metrics(self.path)

        with TRACER.start_as_current_span(f"GET {route}") as span:
            span.set_attribute("http.method", "GET")
            span.set_attribute("http.route", route)

            if self.path == "/metrics":
                payload = generate_latest()
                status_code = 200
                self.send_response(status_code)
                self.send_header("Content-Type", CONTENT_TYPE_LATEST)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            else:
                status_code, body = build_response(self.path)
                payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            duration = time.perf_counter() - started_at
            HTTP_REQUESTS_TOTAL.labels("GET", route, str(status_code)).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels("GET", route).observe(duration)
            span.set_attribute("http.status_code", status_code)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def run_server() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = get_env_int("PORT", 8080)
    server = HTTPServer((host, port), TaskRequestHandler)
    print(f"Task model lab7 server started on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
