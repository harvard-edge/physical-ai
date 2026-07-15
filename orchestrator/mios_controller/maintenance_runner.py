"""Deterministic supervisor tick runner for bounded maintenance simulations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from .maintenance_scheduler import MaintenanceScheduler, SchedulerResult


@dataclass(frozen=True)
class MaintenanceRunReport:
    ticks: int
    completed_cycles: int
    skipped_ticks: int
    failures: int
    results: tuple[SchedulerResult, ...]


def run_supervisor_ticks(
    scheduler: MaintenanceScheduler,
    tick_times: Sequence[float],
    cycle: Callable[[], object],
) -> MaintenanceRunReport:
    """Run finite supervisor ticks; exceptions stop the run and remain visible."""
    results: list[SchedulerResult] = []
    failures = 0
    for now in tick_times:
        try:
            result = scheduler.run_if_due(now, cycle)
        except Exception:
            failures += 1
            raise
        results.append(result)
    return MaintenanceRunReport(
        ticks=len(tick_times),
        completed_cycles=sum(result.ran for result in results),
        skipped_ticks=sum(not result.ran for result in results),
        failures=failures,
        results=tuple(results),
    )
