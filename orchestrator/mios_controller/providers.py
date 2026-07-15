"""Provider-neutral model adapter contract with deterministic fallback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ModelRequest:
    request_id: str
    role: str
    prompt: str
    max_tokens: int
    privacy_class: str


@dataclass(frozen=True)
class ModelResponse:
    request_id: str
    provider: str
    model: str
    text: str
    input_tokens: int
    output_tokens: int
    fallback: bool


class ModelProvider(Protocol):
    provider: str
    model: str

    def complete(self, request: ModelRequest) -> ModelResponse: ...


class DeterministicProvider:
    provider = "local-replay"
    model = "deterministic-v1"

    def complete(self, request: ModelRequest) -> ModelResponse:
        if request.max_tokens < 1 or not request.prompt.strip():
            raise ValueError("model requests require a bounded prompt and token budget")
        return ModelResponse(
            request.request_id,
            self.provider,
            self.model,
            f"replay:{request.role}:{request.prompt[:128]}",
            len(request.prompt.split()),
            1,
            True,
        )


def complete_with_fallback(
    request: ModelRequest, primary: ModelProvider, fallback: ModelProvider
) -> ModelResponse:
    try:
        response = primary.complete(request)
    except (TimeoutError, ConnectionError, RuntimeError):
        response = fallback.complete(request)
    if response.request_id != request.request_id:
        raise ValueError("provider returned a mismatched request ID")
    return response
