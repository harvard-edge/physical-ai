import pytest

from mios_controller.maintenance import (
    InvalidModeTransition,
    MaintenanceController,
    RuntimeMode,
)


def test_maintenance_drains_and_returns_to_interaction():
    controller = MaintenanceController()
    controller.enter_maintenance()
    assert controller.mode == RuntimeMode.MAINTENANCE
    controller.complete_maintenance()
    assert controller.mode == RuntimeMode.INTERACTION


def test_staging_cannot_start_from_interaction():
    controller = MaintenanceController()
    with pytest.raises(InvalidModeTransition):
        controller.transition(RuntimeMode.STAGING, "unsafe shortcut")
