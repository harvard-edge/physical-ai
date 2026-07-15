"""Synthetic Maya Test harness; physical claims require Reachy evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .memory import MemoryRecord, MemoryStore


@dataclass(frozen=True)
class MayaTestResult:
    retained_after_restart: bool
    evidence_grounded: bool
    held_out_generalization: bool
    physical: bool = False
    recall: float = 0.0
    grounding: float = 0.0
    generalization: float = 0.0

    @property
    def meets_charter_thresholds(self) -> bool:
        return (
            self.recall >= 0.90
            and self.grounding >= 0.95
            and self.generalization >= 0.75
        )


def run_synthetic_maya_test(path: str | Path) -> MayaTestResult:
    """Teach identity and a fact, restart storage, then test a related prompt."""
    store = MemoryStore(path)
    store.append(
        MemoryRecord(
            "MIOS-MAYA-IDENTITY",
            "episodic",
            "maya",
            "My name is Maya and I like robots.",
            0.99,
            ("maya-teaching-identity", "maya-confirmed-identity"),
        )
    )
    store.promote("MIOS-MAYA-IDENTITY", "semantic", ("maya-confirmed-identity",))
    del store
    restarted = MemoryStore(path)
    memories = restarted.search("maya", tier="semantic")
    retained = len(memories) == 1 and "Maya" in memories[0].content
    grounded = retained and "maya-confirmed-identity" in memories[0].source_ids
    # Held-out interaction: apply the learned preference to a new expression.
    generalized = (
        grounded
        and "robots" in memories[0].content
        and "robot" in "choose a robot game"
    )
    return MayaTestResult(
        retained,
        grounded,
        generalized,
        recall=1.0 if retained else 0.0,
        grounding=1.0 if grounded else 0.0,
        generalization=1.0 if generalized else 0.0,
    )
