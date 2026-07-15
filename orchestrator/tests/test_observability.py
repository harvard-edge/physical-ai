import pytest

from mios_controller.observability import MetricSample, ObservabilityStore


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
