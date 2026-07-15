from mios_controller.maintenance_runner import run_supervisor_ticks
from mios_controller.maintenance_scheduler import MaintenanceScheduler


def test_supervisor_tick_runner_completes_bounded_overnight_simulation(tmp_path):
    calls: list[float] = []
    scheduler = MaintenanceScheduler(
        60, max_cycles=2, state_path=tmp_path / "state.json"
    )
    report = run_supervisor_ticks(
        scheduler,
        (0, 30, 60, 90, 120),
        lambda: calls.append(1),
    )
    assert report.ticks == 5
    assert report.completed_cycles == 2
    assert report.skipped_ticks == 3
    assert report.failures == 0
    assert len(calls) == 2
