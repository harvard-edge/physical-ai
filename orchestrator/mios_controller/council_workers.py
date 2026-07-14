"""Deterministic council workers used for replay and integration tests.

These workers are intentionally boring. Real model adapters will implement the
same callable contract after the coordinator and handoff protocol are stable.
"""

from __future__ import annotations

from .council import CouncilTask, Handoff, Worker, new_handoff_id


def _worker(role: str, summary: str) -> Worker:
    def run(task: CouncilTask, context: tuple[Handoff, ...]) -> Handoff:
        context_note = f"; consumed {len(context)} prior handoffs" if context else ""
        return Handoff(
            new_handoff_id(), task.task_id, role, "COMPLETED",
            f"{summary}: {task.objective}{context_note}",
            (f"artifact://council/{task.task_id}/{role}",), (),
        )

    return run


def deterministic_workers() -> dict[str, Worker]:
    """Return replayable workers for every core council role."""
    return {
        "architect": _worker("architect", "design proposal produced"),
        "researcher": _worker("researcher", "research packet produced"),
        "implementer": _worker("implementer", "candidate patch produced"),
        "verifier": _worker("verifier", "verification report produced"),
        "safety-reviewer": _worker("safety-reviewer", "risk review produced"),
        "historian": _worker("historian", "memory update proposed"),
        "release-engineer": _worker("release-engineer", "local release candidate produced"),
    }
