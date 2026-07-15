from mios_controller.benchmark import benchmark_provider
from mios_controller.providers import DeterministicProvider, ModelRequest


def test_benchmark_records_latency_and_provenance():
    result = benchmark_provider(
        DeterministicProvider(),
        ModelRequest("MIOS-BENCH-001", "monitor", "summarize", 16, "synthetic"),
    )
    assert result.succeeded is True
    assert result.provider == "local-replay"
    assert result.elapsed_ms >= 0
