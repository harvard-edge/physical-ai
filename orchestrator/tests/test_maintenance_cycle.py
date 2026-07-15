from mios_controller.maintenance import MaintenanceController, RuntimeMode
from mios_controller.maintenance_cycle import run_maintenance_cycle
from mios_controller.maintenance_scheduler import MaintenanceScheduler
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


def test_bounded_scheduler_runs_repeated_maintenance_cycles(tmp_path):
    memory = MemoryStore(tmp_path / "memory.sqlite")
    memory.append(
        MemoryRecord("MIOS-MEM-002", "episodic", "maya", "likes music", 0.9, ("obs-2",))
    )
    controller = MaintenanceController()
    runtime = RuntimeBoundary(tmp_path / "runtime.sqlite")
    scheduler = MaintenanceScheduler(60, max_cycles=2)
    results = []

    def cycle():
        results.append(
            run_maintenance_cycle(
                controller,
                memory,
                runtime,
                (("MIOS-MEM-002", ("review-2",)),) if not results else (),
            )
        )

    assert scheduler.run_if_due(0, cycle).ran
    assert scheduler.run_if_due(30, cycle).ran is False
    assert scheduler.run_if_due(60, cycle).ran
    assert len(results) == 2
    assert all(result.mode == RuntimeMode.INTERACTION for result in results)
