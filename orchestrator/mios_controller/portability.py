"""Portable-core contract conformance for alternate embodiments."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortableContract:
    name: str
    version: str
    required_operations: tuple[str, ...]


@dataclass(frozen=True)
class EmbodimentManifest:
    embodiment: str
    runtime_version: str
    implemented_operations: frozenset[str]
    resource_budget_mb: int


@dataclass(frozen=True)
class ConformanceReport:
    embodiment: str
    passed: bool
    missing_operations: tuple[str, ...]
    budget_ok: bool


@dataclass(frozen=True)
class ResourceMeasurement:
    embodiment: str
    peak_memory_mb: int
    p95_latency_ms: float
    memory_budget_mb: int
    latency_budget_ms: float
    measured_on_hardware: bool = False

    @property
    def within_budget(self) -> bool:
        return (
            0 < self.peak_memory_mb <= self.memory_budget_mb
            and 0 < self.p95_latency_ms <= self.latency_budget_ms
        )


PORTABLE_CORE = (
    PortableContract("memory", "1.0.0", ("append", "promote", "retract", "search")),
    PortableContract("safety", "1.0.0", ("authorize", "protective_stop")),
    PortableContract("cognition", "1.0.0", ("checkpoint", "resume")),
)


def check_conformance(
    manifest: EmbodimentManifest, *, memory_budget_mb: int = 256
) -> ConformanceReport:
    required = {
        operation
        for contract in PORTABLE_CORE
        for operation in contract.required_operations
    }
    missing = tuple(sorted(required - manifest.implemented_operations))
    budget_ok = 0 < manifest.resource_budget_mb <= memory_budget_mb
    return ConformanceReport(
        manifest.embodiment, not missing and budget_ok, missing, budget_ok
    )


def check_transfer(
    manifest: EmbodimentManifest, measurement: ResourceMeasurement
) -> bool:
    """Require unchanged contracts plus explicit target-profile budgets."""
    return (
        check_conformance(
            manifest, memory_budget_mb=measurement.memory_budget_mb
        ).passed
        and measurement.within_budget
    )
