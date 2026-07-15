from mios_controller.embodiment import (
    ActionEnvelope,
    FakeHardwareGateway,
    SafetySupervisor,
)


def envelope(command="nod"):
    return ActionEnvelope(
        "MIOS-ACTION-001", "robot.motion", command, (("angle", 1.0),), 1000, "physical"
    )


def test_fake_hardware_requires_deterministic_authorization():
    gateway = FakeHardwareGateway(SafetySupervisor(frozenset({"nod"})))
    result = gateway.execute(envelope())
    assert result.status == "EXECUTED"
    assert len(gateway.executed) == 1


def test_protective_stop_and_unknown_commands_cannot_execute():
    supervisor = SafetySupervisor(frozenset({"nod"}))
    gateway = FakeHardwareGateway(supervisor)
    assert gateway.execute(envelope("wave")).status == "REJECTED"
    supervisor.protective_stop()
    assert gateway.execute(envelope()).status == "STOPPED"
    assert gateway.executed == []
