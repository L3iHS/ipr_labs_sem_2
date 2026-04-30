from __future__ import annotations

import os

from prometheus_client import Counter, Histogram

HTTP_REQUESTS_TOTAL = Counter(
    "task_model_http_requests_total",
    "Total HTTP requests handled by task-model",
    ["method", "route", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "task_model_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"],
)

TASK_RESPONSES_TOTAL = Counter(
    "task_model_task_responses_total",
    "Business metric: total task responses returned by the service",
    ["status"],
)


def setup_tracing() -> object:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    service_name = os.getenv("OTEL_SERVICE_NAME", "task-model-lab7")

    if not endpoint:
        return _NoopTracer()

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        print("OpenTelemetry packages are not installed, tracing is disabled")
        return _NoopTracer()

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)


class _NoopSpan:
    def __enter__(self) -> _NoopSpan:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None

    def set_attribute(self, key: str, value: object) -> None:
        return None


class _NoopTracer:
    def start_as_current_span(self, name: str) -> _NoopSpan:
        return _NoopSpan()
