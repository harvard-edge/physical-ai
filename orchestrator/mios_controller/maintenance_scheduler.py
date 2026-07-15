"""Bounded, supervisor-friendly scheduling for maintenance cycles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class SchedulerResult:
    ran: bool
    cycle_number: int
    reason: str


class MaintenanceScheduler:
    """Run maintenance only when explicitly due; never owns a background thread."""

    def __init__(self, interval_seconds: float, max_cycles: int = 1) -> None:
        if interval_seconds <= 0:
            raise ValueError("maintenance interval must be positive")
        if max_cycles < 1:
            raise ValueError("max_cycles must be positive")
        self.interval_seconds = interval_seconds
        self.max_cycles = max_cycles
        self.last_started_at: float | None = None
        self.cycles_completed = 0

    def run_if_due(
        self,
        now: float,
        cycle: Callable[[], object],
        *,
        force: bool = False,
    ) -> SchedulerResult:
        if self.cycles_completed >= self.max_cycles:
            return SchedulerResult(
                False, self.cycles_completed, "cycle budget exhausted"
            )
        if not force and self.last_started_at is not None:
            if now - self.last_started_at < self.interval_seconds:
                return SchedulerResult(False, self.cycles_completed, "not due")
        self.last_started_at = now
        cycle()
        self.cycles_completed += 1
        return SchedulerResult(True, self.cycles_completed, "maintenance completed")

    def reset_budget(self) -> None:
        """Reset only the scheduler's bounded window after an operator decision."""
        self.cycles_completed = 0
