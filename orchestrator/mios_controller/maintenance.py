"""Explicit runtime maintenance-mode state machine."""

from __future__ import annotations

from enum import StrEnum


class RuntimeMode(StrEnum):
    INTERACTION = "INTERACTION"
    DRAINING = "DRAINING"
    MAINTENANCE = "MAINTENANCE"
    STAGING = "STAGING"
    RECOVERY = "RECOVERY"


class InvalidModeTransition(RuntimeError):
    pass


TRANSITIONS: dict[RuntimeMode, frozenset[RuntimeMode]] = {
    RuntimeMode.INTERACTION: frozenset({RuntimeMode.DRAINING, RuntimeMode.RECOVERY}),
    RuntimeMode.DRAINING: frozenset({RuntimeMode.MAINTENANCE, RuntimeMode.RECOVERY}),
    RuntimeMode.MAINTENANCE: frozenset(
        {RuntimeMode.STAGING, RuntimeMode.INTERACTION, RuntimeMode.RECOVERY}
    ),
    RuntimeMode.STAGING: frozenset({RuntimeMode.INTERACTION, RuntimeMode.RECOVERY}),
    RuntimeMode.RECOVERY: frozenset({RuntimeMode.INTERACTION}),
}


class MaintenanceController:
    def __init__(self, initial: RuntimeMode = RuntimeMode.INTERACTION) -> None:
        self.mode = initial
        self.history: list[tuple[RuntimeMode, RuntimeMode, str]] = []

    def transition(self, target: RuntimeMode, reason: str) -> RuntimeMode:
        if not reason.strip():
            raise ValueError("mode transitions require a reason")
        if target not in TRANSITIONS[self.mode]:
            raise InvalidModeTransition(f"cannot transition {self.mode} → {target}")
        previous = self.mode
        self.mode = target
        self.history.append((previous, target, reason))
        return self.mode

    def enter_maintenance(self) -> None:
        self.transition(RuntimeMode.DRAINING, "maintenance requested")
        self.transition(RuntimeMode.MAINTENANCE, "active work drained")

    def complete_maintenance(self) -> None:
        if self.mode != RuntimeMode.MAINTENANCE:
            raise InvalidModeTransition("maintenance is not active")
        self.transition(RuntimeMode.INTERACTION, "maintenance completed")

    def recover(self, reason: str) -> None:
        if self.mode != RuntimeMode.RECOVERY:
            self.transition(RuntimeMode.RECOVERY, reason)
