"""Deterministic embodied action envelope and fake hardware gateway."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ActionEnvelope:
    action_id: str
    capability: str
    command: str
    parameters: tuple[tuple[str, float], ...]
    timeout_ms: int
    risk_class: Literal["interaction", "physical"]


@dataclass(frozen=True)
class ActionResult:
    action_id: str
    status: Literal["EXECUTED", "REJECTED", "STOPPED"]
    reason: str


class SafetySupervisor:
    """The model cannot bypass these deterministic checks."""

    def __init__(
        self, allowed_commands: frozenset[str], max_timeout_ms: int = 5000
    ) -> None:
        self.allowed_commands = allowed_commands
        self.max_timeout_ms = max_timeout_ms
        self.stopped = False

    def protective_stop(self) -> None:
        self.stopped = True

    def authorize(self, envelope: ActionEnvelope) -> ActionResult | None:
        if self.stopped:
            return ActionResult(
                envelope.action_id, "STOPPED", "protective stop is active"
            )
        if envelope.command not in self.allowed_commands:
            return ActionResult(
                envelope.action_id,
                "REJECTED",
                "command is outside the allowed envelope",
            )
        if envelope.timeout_ms < 1 or envelope.timeout_ms > self.max_timeout_ms:
            return ActionResult(
                envelope.action_id, "REJECTED", "timeout exceeds safety budget"
            )
        if envelope.risk_class != "physical":
            return ActionResult(
                envelope.action_id,
                "REJECTED",
                "only physical actions reach the gateway",
            )
        return None


class FakeHardwareGateway:
    """Simulation-only gateway used by protected tests."""

    def __init__(self, supervisor: SafetySupervisor) -> None:
        self.supervisor = supervisor
        self.executed: list[ActionEnvelope] = []

    def execute(self, envelope: ActionEnvelope) -> ActionResult:
        rejection = self.supervisor.authorize(envelope)
        if rejection is not None:
            return rejection
        self.executed.append(envelope)
        return ActionResult(
            envelope.action_id, "EXECUTED", "fake hardware accepted envelope"
        )
