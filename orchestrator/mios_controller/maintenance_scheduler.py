"""Bounded, supervisor-friendly scheduling for maintenance cycles."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class SchedulerResult:
    ran: bool
    cycle_number: int
    reason: str


class MaintenanceScheduler:
    """Run maintenance only when explicitly due; never owns a background thread."""

    def __init__(
        self,
        interval_seconds: float,
        max_cycles: int = 1,
        state_path: str | Path | None = None,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("maintenance interval must be positive")
        if max_cycles < 1:
            raise ValueError("max_cycles must be positive")
        self.interval_seconds = interval_seconds
        self.max_cycles = max_cycles
        self.state_path = Path(state_path) if state_path is not None else None
        self.last_started_at: float | None = None
        self.cycles_completed = 0
        self._load()

    def _load(self) -> None:
        if self.state_path is None or not self.state_path.exists():
            return
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        if (
            state.get("interval_seconds") != self.interval_seconds
            or state.get("max_cycles") != self.max_cycles
        ):
            raise ValueError("maintenance scheduler configuration changed")
        self.last_started_at = state.get("last_started_at")
        self.cycles_completed = int(state.get("cycles_completed", 0))
        if self.cycles_completed < 0 or self.cycles_completed > self.max_cycles:
            raise ValueError("maintenance scheduler state is invalid")

    def _save(self) -> None:
        if self.state_path is None:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                {
                    "interval_seconds": self.interval_seconds,
                    "max_cycles": self.max_cycles,
                    "last_started_at": self.last_started_at,
                    "cycles_completed": self.cycles_completed,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.state_path)

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
        self._save()
        return SchedulerResult(True, self.cycles_completed, "maintenance completed")

    def reset_budget(self) -> None:
        """Reset only the scheduler's bounded window after an operator decision."""
        self.cycles_completed = 0
        self._save()
