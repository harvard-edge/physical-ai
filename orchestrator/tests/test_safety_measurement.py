from mios_controller.embodiment import (
    ActionEnvelope,
    FakeHardwareGateway,
    SafetySupervisor,
)
from mios_controller.safety_measurement import measure_protective_stop


def test_simulated_protective_stop_meets_latency_and_safety_thresholds():
    gateway = FakeHardwareGateway(SafetySupervisor(frozenset({"nod"})))
    measurement = measure_protective_stop(
        gateway,
        ActionEnvelope("a-1", "head", "nod", (), 100, "physical"),
    )
    assert measurement.unsafe_commands == 0
    assert measurement.passes
    assert not measurement.physical
