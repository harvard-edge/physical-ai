"""Bounded, persisted installation and runtime doctor lifecycle.

The doctor is deliberately read-only with respect to hardware and networks.  It
records setup decisions and check results so operators can inspect why a node
is ready (or degraded) without depending on transient process state.
"""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable, Iterable

from .canonical import atomic_write, utc_now


class DoctorPhase(StrEnum):
    DISCOVER = "DISCOVER"
    PREPARE = "PREPARE"
    VERIFY = "VERIFY"
    SELF_TEST = "SELF_TEST"
    READY = "READY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    RECOVERY = "RECOVERY"


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    passed: bool
    severity: str = "required"
    detail: str = ""
    remediation: str | None = None


@dataclass(frozen=True)
class DoctorReport:
    phase: DoctorPhase
    started_at: str
    completed_at: str
    checks: tuple[DoctorCheck, ...]
    run_id: int
    physical: bool = False

    @property
    def passed(self) -> bool:
        return all(
            check.passed for check in self.checks if check.severity == "required"
        )

    def as_dict(self) -> dict:
        result = asdict(self)
        result["phase"] = self.phase.value
        result["checks"] = [asdict(check) for check in self.checks]
        result["passed"] = self.passed
        return result


CheckFactory = Callable[[Path], DoctorCheck]


def default_checks(root: Path) -> tuple[CheckFactory, ...]:
    """Return local, deterministic checks suitable for first boot."""

    def writable(path: Path) -> DoctorCheck:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".doctor-write-probe"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return DoctorCheck("state_directory", True, detail=str(path))
        except OSError as error:
            return DoctorCheck(
                "state_directory",
                False,
                detail=str(error),
                remediation="repair permissions",
            )

    def disk(path: Path) -> DoctorCheck:
        try:
            free = shutil.disk_usage(path).free
        except OSError as error:
            return DoctorCheck("disk_space", False, detail=str(error))
        return DoctorCheck("disk_space", free > 1_048_576, detail=f"free_bytes={free}")

    def python_runtime(_: Path) -> DoctorCheck:
        return DoctorCheck(
            "python_runtime", True, detail=f"version={os.sys.version.split()[0]}"
        )

    return (writable, disk, python_runtime)


class DoctorLifecycle:
    """Run bounded setup checks and persist the latest report atomically."""

    def __init__(
        self, state_path: Path, *, checks: Iterable[CheckFactory] | None = None
    ):
        self.state_path = state_path
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.checks = tuple(checks or default_checks(state_path.parent))

    def _persist(self, report: DoctorReport) -> None:
        atomic_write(
            self.state_path,
            (json.dumps(report.as_dict(), sort_keys=True, indent=2) + "\n").encode(),
        )

    def load(self) -> DoctorReport | None:
        if not self.state_path.exists():
            return None
        payload = json.loads(self.state_path.read_text(encoding="utf-8"))
        checks = tuple(DoctorCheck(**item) for item in payload["checks"])
        return DoctorReport(
            phase=DoctorPhase(payload["phase"]),
            started_at=payload["started_at"],
            completed_at=payload["completed_at"],
            checks=checks,
            run_id=int(payload["run_id"]),
            physical=bool(payload.get("physical", False)),
        )

    def run(self) -> DoctorReport:
        previous = self.load()
        run_id = 1 if previous is None else previous.run_id + 1
        started = utc_now()
        checks: list[DoctorCheck] = []
        # Phase transitions are persisted only through the final atomic report;
        # a failed run cannot leave a misleading READY marker behind.
        try:
            for check in self.checks:
                checks.append(check(self.state_path.parent))
        except Exception as error:  # doctor must report failure, never crash boot
            checks.append(DoctorCheck("doctor_execution", False, detail=repr(error)))
        required_failed = any(
            not item.passed and item.severity == "required" for item in checks
        )
        optional_failed = any(
            not item.passed and item.severity != "required" for item in checks
        )
        phase = (
            DoctorPhase.FAILED
            if required_failed
            else DoctorPhase.DEGRADED
            if optional_failed
            else DoctorPhase.READY
        )
        report = DoctorReport(phase, started, utc_now(), tuple(checks), run_id)
        self._persist(report)
        return report

    def recover(self) -> DoctorReport:
        """Record a recovery attempt, then rerun the bounded checks."""
        previous = self.load()
        run_id = 1 if previous is None else previous.run_id + 1
        now = utc_now()
        recovery = DoctorReport(DoctorPhase.RECOVERY, now, now, tuple(), run_id)
        self._persist(recovery)
        return self.run()
