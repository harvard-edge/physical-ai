"""Model-provider benchmark records with bounded, reproducible inputs."""

from __future__ import annotations

import time
from dataclasses import dataclass

from .providers import ModelProvider, ModelRequest


@dataclass(frozen=True)
class ProviderBenchmark:
    provider: str
    model: str
    request_id: str
    succeeded: bool
    elapsed_ms: float
    input_tokens: int
    output_tokens: int
    fallback: bool
    error: str | None = None


def benchmark_provider(
    provider: ModelProvider, request: ModelRequest
) -> ProviderBenchmark:
    started = time.perf_counter()
    try:
        response = provider.complete(request)
    except (TimeoutError, ConnectionError, RuntimeError, ValueError) as error:
        return ProviderBenchmark(
            provider.provider,
            provider.model,
            request.request_id,
            False,
            (time.perf_counter() - started) * 1000,
            0,
            0,
            False,
            str(error),
        )
    return ProviderBenchmark(
        response.provider,
        response.model,
        response.request_id,
        True,
        (time.perf_counter() - started) * 1000,
        response.input_tokens,
        response.output_tokens,
        response.fallback,
    )
