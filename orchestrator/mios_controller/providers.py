"""Provider-neutral model adapter contract with deterministic fallback."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Protocol


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


class OllamaProvider:
    """Small local-model adapter using Ollama's HTTP API."""

    provider = "ollama"

    def __init__(
        self,
        model: str,
        *,
        endpoint: str = "http://127.0.0.1:11434/api/generate",
        transport: Callable[[str, bytes, float], bytes] | None = None,
    ) -> None:
        if not model.strip() or not endpoint.startswith("http://127.0.0.1"):
            raise ValueError(
                "local Ollama provider requires a loopback endpoint and model"
            )
        self.model = model
        self.endpoint = endpoint
        self._transport = transport or _http_transport

    def complete(self, request: ModelRequest) -> ModelResponse:
        if request.max_tokens < 1 or not request.prompt.strip():
            raise ValueError("model requests require a bounded prompt and token budget")
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": request.prompt,
                "stream": False,
                "options": {"num_predict": request.max_tokens},
            }
        ).encode()
        raw = self._transport(self.endpoint, payload, 5.0)
        decoded = json.loads(raw)
        text = decoded.get("response")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Ollama returned a malformed response")
        return ModelResponse(
            request.request_id,
            self.provider,
            self.model,
            text,
            len(request.prompt.split()),
            len(text.split()),
            False,
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


def _http_transport(endpoint: str, payload: bytes, timeout: float) -> bytes:
    from urllib.request import Request, urlopen

    request = Request(
        endpoint, data=payload, headers={"Content-Type": "application/json"}
    )
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - loopback endpoint enforced above
        return response.read(1_000_000)
