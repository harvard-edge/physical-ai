"""Simulation-only safety measurements for the embodied gateway."""

from __future__ import annotations

import time
from dataclasses import dataclass

from .embodiment import ActionEnvelope, FakeHardwareGateway


@dataclass(frozen=True)
class SafetyMeasurement:
    stop_latency_ms: float
    unsafe_commands: int
    physical: bool = False

    @property
    def passes(self) -> bool:
        return self.unsafe_commands == 0 and self.stop_latency_ms < 100.0


def measure_protective_stop(
    gateway: FakeHardwareGateway, envelope: ActionEnvelope
) -> SafetyMeasurement:
    """Measure the deterministic supervisor path without actuating hardware."""
    gateway.execute(envelope)
    started = time.perf_counter_ns()
    gateway.supervisor.protective_stop()
    result = gateway.execute(envelope)
    elapsed = (time.perf_counter_ns() - started) / 1_000_000
    unsafe = int(result.status == "EXECUTED")
    return SafetyMeasurement(elapsed, unsafe)
