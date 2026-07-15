from mios_controller.providers import (
    DeterministicProvider,
    ModelRequest,
    OllamaProvider,
    HostedCompatibleProvider,
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


def test_hosted_adapter_requires_allowlisted_https_and_is_offline_testable():
    provider = HostedCompatibleProvider(
        "cloud-model",
        endpoint="https://llm.example.test/v1/chat/completions",
        allowed_hosts=frozenset({"llm.example.test"}),
        transport=lambda endpoint, payload, timeout: (
            b'{"choices":[{"message":{"content":"hello Maya"}}]}'
        ),
    )
    response = provider.complete(
        ModelRequest("MIOS-REQ-004", "memory", "recall", 16, "synthetic")
    )
    assert response.provider == "hosted-compatible"
    assert response.fallback is False


def test_hosted_adapter_rejects_unapproved_endpoint():
    import pytest

    with pytest.raises(ValueError):
        HostedCompatibleProvider(
            "cloud-model",
            endpoint="http://127.0.0.1:11434/api",
            allowed_hosts=frozenset({"127.0.0.1"}),
        )


def test_hosted_adapter_rejects_restricted_data():
    import pytest

    provider = HostedCompatibleProvider(
        "cloud-model",
        endpoint="https://llm.example.test/v1/chat/completions",
        allowed_hosts=frozenset({"llm.example.test"}),
        transport=lambda endpoint, payload, timeout: (
            b'{"choices":[{"message":{"content":"no"}}]}'
        ),
    )
    with pytest.raises(ValueError):
        provider.complete(
            ModelRequest("MIOS-REQ-005", "memory", "secret", 16, "restricted")
        )
