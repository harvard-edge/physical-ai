from mios_controller.maintenance import MaintenanceController, RuntimeMode
from mios_controller.maintenance_cycle import run_maintenance_cycle
from mios_controller.memory import MemoryRecord, MemoryStore
from mios_controller.runtime import RuntimeBoundary


def test_maintenance_cycle_promotes_memory_and_returns_to_interaction(tmp_path):
    memory = MemoryStore(tmp_path / "memory.sqlite")
    memory.append(
        MemoryRecord(
            "MIOS-MEM-001", "episodic", "maya", "likes robots", 0.9, ("obs-1",)
        )
    )
    controller = MaintenanceController()
    result = run_maintenance_cycle(
        controller,
        memory,
        RuntimeBoundary(tmp_path / "runtime.sqlite"),
        (("MIOS-MEM-001", ("review-1",)),),
    )
    assert result.promoted_memory_ids == ("MIOS-MEM-001",)
    assert result.mode == RuntimeMode.INTERACTION
