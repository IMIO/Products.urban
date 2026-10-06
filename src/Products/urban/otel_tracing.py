# -*- coding: utf-8 -*-
"""Hand-rolled OTLP/HTTP-JSON span export (Zope2/ZServer, Python 2.7 — no
OpenTelemetry SDK available on this runtime). Hooks ZPublisher's publication
events instead of WSGI middleware, since ZServer predates WSGI.

Sends to the local Puppet-managed otelcol agent (plaintext, no auth needed —
same-host loopback traffic). Payload shape (hex trace/span IDs, NOT base64 —
contrary to the usual protojson bytes-as-base64 convention, trace/span IDs use
a custom hex encoder; startTimeUnixNano/endTimeUnixNano as JSON strings, not
numbers) verified against the real gateway before this was written.

Tracing must never break a real request: every failure here is swallowed.
"""
import os
import random
import time
import json

try:
    from urllib2 import Request, urlopen
except ImportError:  # pragma: no cover - this module only ever runs under py2
    from urllib.request import Request, urlopen

OTLP_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
SERVICE_NAME = os.environ.get("OTEL_SERVICE_NAME", "urban-unknown")
SERVICE_NAMESPACE = "urban"


def _random_hex(n_bytes):
    return "".join("%02x" % random.randint(0, 255) for _ in range(n_bytes))


def _parse_traceparent(value):
    # Format: 00-<32 hex trace id>-<16 hex parent span id>-<2 hex flags>
    try:
        version, trace_id, parent_span_id, _flags = value.split("-")
        if version == "00" and len(trace_id) == 32 and len(parent_span_id) == 16:
            return trace_id, parent_span_id
    except Exception:
        pass
    return None, None


def _send_span(trace_id, span_id, parent_span_id, name, start_ns, end_ns, status_code, http_method, http_status):
    span = {
        "traceId": trace_id,
        "spanId": span_id,
        "name": name,
        "kind": "SPAN_KIND_SERVER",
        "startTimeUnixNano": str(start_ns),
        "endTimeUnixNano": str(end_ns),
        "attributes": [
            {"key": "http.method", "value": {"stringValue": http_method}},
            {"key": "http.status_code", "value": {"intValue": str(http_status)}},
        ],
        "status": {"code": status_code},
    }
    if parent_span_id:
        span["parentSpanId"] = parent_span_id

    payload = {
        "resourceSpans": [{
            "resource": {
                "attributes": [
                    {"key": "service.name", "value": {"stringValue": SERVICE_NAME}},
                    {"key": "service.namespace", "value": {"stringValue": SERVICE_NAMESPACE}},
                ]
            },
            "scopeSpans": [{"spans": [span]}],
        }]
    }

    try:
        body = json.dumps(payload).encode("utf-8")
        req = Request(OTLP_ENDPOINT, data=body, headers={"Content-Type": "application/json"})
        urlopen(req, timeout=2).read()
    except Exception:
        # Never let a broken/unreachable collector take down a real request.
        pass


def handle_pub_start(event):
    request = event.request
    traceparent = request.getHeader("traceparent")
    trace_id, parent_span_id = _parse_traceparent(traceparent) if traceparent else (None, None)
    request._otel = {
        "trace_id": trace_id or _random_hex(16),
        "parent_span_id": parent_span_id,
        "span_id": _random_hex(8),
        "start_ns": int(time.time() * 1e9),
        "path": request.get("PATH_INFO", "unknown"),
        "method": request.get("REQUEST_METHOD", "GET"),
    }


def _finish(event, status_code):
    request = event.request
    ctx = getattr(request, "_otel", None)
    if ctx is None:
        return
    end_ns = int(time.time() * 1e9)
    try:
        http_status = request.response.getStatus()
    except Exception:
        http_status = 0
    _send_span(
        ctx["trace_id"], ctx["span_id"], ctx["parent_span_id"],
        "%s %s" % (ctx["method"], ctx["path"]),
        ctx["start_ns"], end_ns,
        status_code, ctx["method"], http_status,
    )


def handle_pub_success(event):
    _finish(event, "STATUS_CODE_OK")


def handle_pub_failure(event):
    _finish(event, "STATUS_CODE_ERROR")
