"""DBOS compatible workflow-upgrade fixture used by the Phase 1A test suite."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dbos import DBOS, SetWorkflowID


ROOT = Path(os.environ["MIOS_UPGRADE_FIXTURE_ROOT"]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
VERSION = os.environ["MIOS_UPGRADE_FIXTURE_VERSION"]
EFFECTS = ROOT / "effects.jsonl"

DBOS(
    config={
        "name": "mios-upgrade-fixture",
        "system_database_url": f"sqlite:///{ROOT / 'dbos.sqlite3'}",
        "application_version": "phase1a-upgrade-contract",
        "executor_id": "upgrade-fixture",
        "enable_patching": True,
        "run_admin_server": False,
    }
)


def append_effect(workflow_id: str, effect: str) -> None:
    with EFFECTS.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps({"workflow_id": workflow_id, "effect": effect}, sort_keys=True)
        )
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


@DBOS.step()
def step_a(workflow_id: str) -> None:
    append_effect(workflow_id, "A")


@DBOS.step()
def step_new(workflow_id: str) -> None:
    append_effect(workflow_id, "NEW")


@DBOS.step()
def step_b(workflow_id: str) -> None:
    append_effect(workflow_id, "B")


@DBOS.step()
def step_c(workflow_id: str) -> None:
    if VERSION == "v1":
        os._exit(77)
    append_effect(workflow_id, "C")


@DBOS.workflow()
def upgrade_workflow(workflow_id: str) -> str:
    step_a(workflow_id)
    if VERSION == "v2" and DBOS.patch("phase1a-add-middle-step"):
        step_new(workflow_id)
    step_b(workflow_id)
    step_c(workflow_id)
    return "complete"


def main() -> int:
    DBOS.launch()
    try:
        command = sys.argv[1]
        workflow_id = sys.argv[2]
        if command == "start":
            with SetWorkflowID(workflow_id):
                result = upgrade_workflow(workflow_id)
        elif command == "retrieve":
            result = DBOS.retrieve_workflow(workflow_id).get_result()
        else:
            raise ValueError(command)
        print(result)
        return 0
    finally:
        DBOS.destroy(workflow_completion_timeout_sec=2)


if __name__ == "__main__":
    raise SystemExit(main())
