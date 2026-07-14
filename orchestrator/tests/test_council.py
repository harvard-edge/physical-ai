from mios_controller.council import (
    CouncilCoordinator,
    CouncilStore,
    Handoff,
    CouncilTask,
    new_handoff_id,
)
from mios_controller.council_workers import deterministic_workers


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


def test_deterministic_council_runs_multiple_specialists(tmp_path):
    store = CouncilStore(tmp_path / "council.sqlite")
    coordinator = CouncilCoordinator(store)
    for role, worker in deterministic_workers().items():
        coordinator.register(role, worker)
        store.enqueue(CouncilTask(f"MIOS-TASK-{role.upper()}-001", role, "Design the memory lifecycle"))

    results = coordinator.run_until_idle(tuple(deterministic_workers()), max_steps=2)

    assert len(results) == 7
    assert {result.role for result in results} == set(deterministic_workers())
    assert all(result.status == "COMPLETED" for result in results)
