import pytest

from mios_controller.observability import (
    MetricSample,
    ObservabilityProjection,
    ObservabilityStore,
)
from mios_controller.memory import MemoryRecord, MemoryStore
from mios_controller.runtime import RuntimeBoundary, RuntimeEvent, digest_payload


def test_observability_records_trace_metrics(tmp_path):
    store = ObservabilityStore(tmp_path / "telemetry.sqlite")
    trace = store.start_trace()
    store.record(
        MetricSample(trace, "controller.latency", 4.2, "ms", (("role", "verifier"),))
    )


def test_observability_rejects_unknown_trace(tmp_path):
    store = ObservabilityStore(tmp_path / "telemetry.sqlite")
    with pytest.raises(KeyError):
        store.record(MetricSample("MIOS-TRACE-MISSING", "errors", 1, "count"))


def test_projection_is_versioned_and_redacts_memory(tmp_path):
    runtime_path = tmp_path / "runtime.sqlite"
    memory_path = tmp_path / "memory.sqlite"
    runtime = RuntimeBoundary(runtime_path)
    runtime.record_event(
        RuntimeEvent(
            "evt-1",
            "observation",
            "learned a private fact",
            "internal",
            digest_payload(b"private"),
        )
    )
    memory = MemoryStore(memory_path)
    memory.append(
        MemoryRecord(
            "mem-1",
            "semantic",
            "Maya",
            "Maya's favorite secret",
            0.9,
            ("evt-1",),
            "accepted",
        )
    )
    snapshot = ObservabilityProjection(
        runtime_path=runtime_path,
        memory_path=memory_path,
        maintenance=type("Mode", (), {"mode": "INTERACTION"})(),
        safety={"stop_active": False},
    ).snapshot()
    payload = snapshot.to_payload()
    assert snapshot.schema_version == "mios.observability.v1"
    assert payload["runtime_event_count"] == 1
    assert payload["memory_counts"] == {"semantic": 1}
    assert payload["concepts"][0]["subject_digest"] != "Maya"
    assert payload["concepts"][0]["content_digest"] != "Maya's favorite secret"


def test_projection_is_bounded_and_handles_missing_stores(tmp_path):
    snapshot = ObservabilityProjection(
        runtime_path=tmp_path / "missing-runtime.sqlite",
        memory_path=tmp_path / "missing-memory.sqlite",
        max_items=1,
    ).snapshot()
    assert snapshot.activity == ()
    assert snapshot.concepts == ()
    assert snapshot.runtime_event_count == 0
