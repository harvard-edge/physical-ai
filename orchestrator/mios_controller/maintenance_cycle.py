"""Bounded maintenance cycle connecting runtime mode and memory promotion."""

from __future__ import annotations

from dataclasses import dataclass

from .maintenance import MaintenanceController, RuntimeMode
from .memory import MemoryStore
from .runtime import RuntimeBoundary, RuntimeEvent, digest_payload


@dataclass(frozen=True)
class MaintenanceResult:
    promoted_memory_ids: tuple[str, ...]
    mode: RuntimeMode
    event_id: str


def run_maintenance_cycle(
    controller: MaintenanceController,
    memory: MemoryStore,
    runtime: RuntimeBoundary,
    promotions: tuple[tuple[str, tuple[str, ...]], ...],
) -> MaintenanceResult:
    """Run one bounded, evidence-backed consolidation cycle."""
    controller.enter_maintenance()
    promoted: list[str] = []
    try:
        for memory_id, evidence_ids in promotions:
            memory.promote(memory_id, "semantic", evidence_ids)
            promoted.append(memory_id)
        event_id = f"MIOS-MAINT-{len(controller.history):04d}"
        runtime.record_event(
            RuntimeEvent(
                event_id,
                "maintenance",
                f"promoted {len(promoted)} memories",
                "derived-redacted",
                digest_payload("|".join(promoted).encode()),
            ),
        )
        controller.complete_maintenance()
        return MaintenanceResult(tuple(promoted), controller.mode, event_id)
    except Exception:
        controller.recover("maintenance consolidation failed")
        raise
