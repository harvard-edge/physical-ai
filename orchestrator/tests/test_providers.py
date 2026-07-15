from mios_controller.providers import (
    DeterministicProvider,
    ModelRequest,
    OllamaProvider,
    complete_with_fallback,
)


def test_deterministic_provider_records_fallback_provenance():
    response = DeterministicProvider().complete(
        ModelRequest("MIOS-REQ-001", "architect", "design", 32, "synthetic")
    )
    assert response.provider == "local-replay"
    assert response.fallback is True


def test_provider_failure_uses_fallback():
    class Failing:
        provider = "cloud"
        model = "test"

        def complete(self, request):
            raise TimeoutError("offline")

    response = complete_with_fallback(
        ModelRequest("MIOS-REQ-002", "researcher", "research", 32, "synthetic"),
        Failing(),
        DeterministicProvider(),
    )
    assert response.request_id == "MIOS-REQ-002"
    assert response.fallback is True


def test_ollama_adapter_is_offline_testable():
    provider = OllamaProvider(
        "small-model",
        transport=lambda endpoint, payload, timeout: b'{"response":"hello Maya"}',
    )
    response = provider.complete(
        ModelRequest("MIOS-REQ-003", "memory", "recall", 16, "synthetic")
    )
    assert response.provider == "ollama"
    assert response.fallback is False
