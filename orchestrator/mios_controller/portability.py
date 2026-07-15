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
