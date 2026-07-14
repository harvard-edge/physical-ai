from mios_controller.council import (
    CouncilCoordinator,
    CouncilStore,
    Handoff,
    CouncilTask,
    new_handoff_id,
)


def test_council_persists_handoffs_and_routes_context(tmp_path):
    store = CouncilStore(tmp_path / "council.sqlite")
    coordinator = CouncilCoordinator(store)
    seen = []

    def architect(task, context):
        seen.append((task.objective, len(context)))
        return Handoff(
            new_handoff_id(),
            task.task_id,
            task.role,
            "COMPLETED",
            "design ready",
            ("artifact://design",),
            (),
        )

    coordinator.register("architect", architect)
    task = CouncilTask("MIOS-TASK-TEST-001", "architect", "Define memory lifecycle")
    store.enqueue(task)

    result = coordinator.run_once("architect")

    assert result is not None
    assert seen == [("Define memory lifecycle", 0)]
    assert store.recent_handoffs()[0].summary == "design ready"


def test_coordinator_requires_matching_terminal_handoff(tmp_path):
    store = CouncilStore(tmp_path / "council.sqlite")
    coordinator = CouncilCoordinator(store)

    def bad_worker(task, context):
        return Handoff(
            new_handoff_id(), "MIOS-TASK-WRONG", task.role, "COMPLETED", "bad", (), ()
        )

    coordinator.register("verifier", bad_worker)
    store.enqueue(CouncilTask("MIOS-TASK-TEST-002", "verifier", "Verify candidate"))

    try:
        coordinator.run_once("verifier")
    except ValueError as error:
        assert "does not match" in str(error)
    else:
        raise AssertionError("mismatched handoff was accepted")
