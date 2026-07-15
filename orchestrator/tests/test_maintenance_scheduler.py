import pytest

from mios_controller.maintenance_scheduler import MaintenanceScheduler


def test_scheduler_runs_when_due_and_then_waits() -> None:
    calls: list[int] = []
    scheduler = MaintenanceScheduler(60, max_cycles=2)
    assert scheduler.run_if_due(100, lambda: calls.append(1)).ran
    assert not scheduler.run_if_due(120, lambda: calls.append(1)).ran
    assert scheduler.run_if_due(160, lambda: calls.append(1)).ran
    assert calls == [1, 1]
    assert not scheduler.run_if_due(220, lambda: calls.append(1)).ran


def test_scheduler_force_and_budget_are_explicit() -> None:
    calls: list[int] = []
    scheduler = MaintenanceScheduler(60, max_cycles=1)
    assert scheduler.run_if_due(0, lambda: calls.append(1), force=True).ran
    assert not scheduler.run_if_due(1, lambda: calls.append(1), force=True).ran
    scheduler.reset_budget()
    assert scheduler.run_if_due(1, lambda: calls.append(1), force=True).ran
    assert calls == [1, 1]


@pytest.mark.parametrize("interval", [0, -1])
def test_scheduler_rejects_unbounded_interval(interval: float) -> None:
    with pytest.raises(ValueError):
        MaintenanceScheduler(interval)
