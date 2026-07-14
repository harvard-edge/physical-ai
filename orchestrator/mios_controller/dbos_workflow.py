"""DBOS durability adapter for the MiOS-owned experiment state machine."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dbos import DBOS, SetWorkflowID

from .domain import ExperimentState
from .engine import EvolutionEngine, WORKFLOW_COMPATIBILITY_VERSION


WORKFLOW_STATES = (
    ExperimentState.OBSERVED,
    ExperimentState.TRIAGED,
    ExperimentState.PREREGISTERED,
    ExperimentState.DESIGNED,
    ExperimentState.IMPLEMENTING,
    ExperimentState.EVALUATING,
    ExperimentState.REVIEWING,
)


@DBOS.step()
def execute_transition(
    controller_root: str,
    repository_root: str,
    experiment_id: str,
    from_state: str,
    allow_cooperative: bool,
) -> dict[str, Any]:
    engine = EvolutionEngine(
        Path(controller_root),
        Path(repository_root),
        allow_cooperative=allow_cooperative,
    )
    return engine.run_transition(experiment_id, ExperimentState(from_state))


@DBOS.workflow()
def evolution_cycle(
    controller_root: str,
    repository_root: str,
    experiment_id: str,
    allow_cooperative: bool = False,
) -> str:
    # DBOS uses this marker to distinguish histories created before the first
    # production compatibility site. New replay-sensitive operations must be
    # introduced inside a uniquely named patch branch rather than by changing
    # the stable operation sequence in place.
    revision = 2
    if os.environ.get("MIOS_ENABLE_WORKFLOW_TEST_MODE") == "1":
        revision = int(os.environ.get("MIOS_TEST_WORKFLOW_REVISION", "2"))
    if revision >= 2 and DBOS.patch("mios-evolution-cycle-v2-compatibility-site"):
        # The first site intentionally has no domain effect. It establishes a
        # safe insertion point for subsequent compatible releases.
        pass
    for state in WORKFLOW_STATES:
        execute_transition(
            controller_root,
            repository_root,
            experiment_id,
            state.value,
            allow_cooperative,
        )
    return ExperimentState.LOCAL_CANDIDATE_READY.value


class DurableWorkflowRuntime:
    def __init__(self, controller_root: Path):
        self.controller_root = controller_root.resolve()
        database = self.controller_root / "checkpoints" / "dbos.sqlite3"
        database.parent.mkdir(parents=True, exist_ok=True)
        DBOS(
            config={
                "name": "mios-evolution-controller",
                "system_database_url": f"sqlite:///{database}",
                # Package releases are deliberately decoupled from replay
                # compatibility. Patch-compatible releases keep this stable.
                "application_version": (
                    f"mios-evolution-{WORKFLOW_COMPATIBILITY_VERSION}"
                ),
                "executor_id": "mios-local",
                "enable_patching": True,
                "run_admin_server": False,
            }
        )
        DBOS.launch()

    def start(
        self,
        repository_root: Path,
        experiment_id: str,
        allow_cooperative: bool = False,
    ):
        with SetWorkflowID(experiment_id):
            return DBOS.start_workflow(
                evolution_cycle,
                str(self.controller_root),
                str(repository_root.resolve()),
                experiment_id,
                allow_cooperative,
            )

    def cancel(self, experiment_id: str) -> None:
        DBOS.cancel_workflow(experiment_id, cancel_children=True)

    def close(self) -> None:
        DBOS.destroy(workflow_completion_timeout_sec=2)
