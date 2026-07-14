from __future__ import annotations

from pathlib import Path

import pytest

from mios_controller.domain import ExperimentState
from mios_controller.engine import EvolutionEngine


REPOSITORY = Path(__file__).resolve().parents[2]
OBSERVATION = REPOSITORY / "evolution" / "fixtures" / "synthetic-observation.json"


def test_failing_frozen_check_pauses_experiment_and_controller(tmp_path) -> None:
    engine = EvolutionEngine(tmp_path / "controller", REPOSITORY)
    engine.initialize()
    experiment_id, _ = engine.ingest_file(OBSERVATION)
    engine.registry.resume(engine.policy.digest)
    for state in (
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        ExperimentState.PREREGISTERED,
        ExperimentState.DESIGNED,
    ):
        engine.run_transition(experiment_id, state)

    behavior = (
        engine.paths.workspaces / experiment_id / "repository" / "src" / "behavior.py"
    )
    behavior.write_text(
        'def current_value() -> str:\n    return "old"\n', encoding="utf-8"
    )
    with pytest.raises(RuntimeError, match="acceptance test failed"):
        engine.run_transition(experiment_id, ExperimentState.IMPLEMENTING)

    assert engine.registry.get_experiment(experiment_id)["state"] == "PAUSED"
    assert engine.registry.status()["controller_state"] == "PAUSED"
    assert engine.registry.status()["accept_new_work"] is False
