"""Closed-loop software-only embodiment simulation and QA scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .embodiment import ActionEnvelope, FakeHardwareGateway, SafetySupervisor
from .memory import MemoryRecord, MemoryStore
from .providers import DeterministicProvider, ModelRequest
from .runtime import RuntimeBoundary, RuntimeEvent, digest_payload


@dataclass(frozen=True)
class SimulationReport:
    taught: bool
    recalled_after_restart: bool
    model_response: str
    action_status: str
    failure_contained: bool
    reset_empty: bool


class ClosedLoopSimulator:
    def __init__(self, root: str | Path) -> None:
        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)
        self.memory = MemoryStore(root / "memory.sqlite")
        self.runtime = RuntimeBoundary(root / "runtime.sqlite")
        self.safety = SafetySupervisor(frozenset({"nod"}))
        self.gateway = FakeHardwareGateway(self.safety)
        self.provider = DeterministicProvider()

    def run(self) -> SimulationReport:
        self.memory.append(
            MemoryRecord(
                "SIM-MEM-001",
                "episodic",
                "maya",
                "Maya likes robots",
                0.99,
                ("sim-obs-1",),
            )
        )
        self.memory.promote("SIM-MEM-001", "semantic", ("sim-review-1",))
        self.runtime.record_event(
            RuntimeEvent(
                "SIM-EVENT-001",
                "observation",
                "taught a fact",
                "synthetic",
                digest_payload(b"fact"),
            )
        )
        response = self.provider.complete(
            ModelRequest("SIM-REQ-001", "conversation", "recall Maya", 16, "synthetic")
        )
        action = self.gateway.execute(
            ActionEnvelope("SIM-ACTION-001", "head", "nod", (), 100, "physical")
        )
        restarted = MemoryStore(self.memory.path)
        recalled = bool(restarted.search("maya", tier="semantic"))
        self.safety.protective_stop()
        stopped = self.gateway.execute(
            ActionEnvelope("SIM-ACTION-002", "head", "nod", (), 100, "physical")
        )
        self.memory.reset()
        reset_empty = not MemoryStore(self.memory.path).search("maya")
        return SimulationReport(
            taught=True,
            recalled_after_restart=recalled,
            model_response=response.text,
            action_status=action.status,
            failure_contained=stopped.status == "STOPPED",
            reset_empty=reset_empty,
        )
