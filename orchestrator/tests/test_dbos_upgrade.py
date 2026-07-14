from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from mios_controller.sandbox import PINNED_IMAGE


FIXTURE = Path(__file__).resolve().parents[1] / "tools" / "workflow_upgrade_fixture.py"
PYTHON = Path(__file__).resolve().parents[1] / ".venv" / "bin" / "python"
CLI = Path(__file__).resolve().parents[1] / ".venv" / "bin" / "mios-controller"
REPOSITORY = Path(__file__).resolve().parents[2]
OBSERVATION = REPOSITORY / "evolution" / "fixtures" / "synthetic-observation.json"


def invoke(
    root: Path, version: str, command: str, workflow_id: str, check: bool = True
):
    environment = os.environ.copy()
    environment["MIOS_UPGRADE_FIXTURE_ROOT"] = str(root)
    environment["MIOS_UPGRADE_FIXTURE_VERSION"] = version
    return subprocess.run(
        [str(PYTHON), str(FIXTURE), command, workflow_id],
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
        check=check,
    )


def test_compatible_v2_worker_resumes_v1_without_replaying_completed_effects(
    tmp_path,
) -> None:
    root = tmp_path / "upgrade"
    crashed = invoke(root, "v1", "start", "old-workflow", check=False)
    assert crashed.returncode == 77

    recovered = invoke(root, "v2", "retrieve", "old-workflow")
    assert recovered.stdout.strip().endswith("complete")
    fresh = invoke(root, "v2", "start", "new-workflow")
    assert fresh.stdout.strip().endswith("complete")

    effects = [
        json.loads(line) for line in (root / "effects.jsonl").read_text().splitlines()
    ]
    old_effects = [
        item["effect"] for item in effects if item["workflow_id"] == "old-workflow"
    ]
    new_effects = [
        item["effect"] for item in effects if item["workflow_id"] == "new-workflow"
    ]
    assert old_effects == ["A", "B", "C"]
    assert new_effects == ["A", "NEW", "B", "C"]


def sandbox_available() -> bool:
    return (
        bool(shutil.which("docker"))
        and subprocess.run(
            ["docker", "image", "inspect", PINNED_IMAGE],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def production_cli(root: Path, command: str, *arguments: str, environment=None):
    return subprocess.run(
        [
            str(CLI),
            command,
            "--root",
            str(root),
            "--repository",
            str(REPOSITORY),
            *arguments,
        ],
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=45,
        check=False,
    )


@pytest.mark.skipif(not sandbox_available(), reason="pinned sandbox unavailable")
def test_real_evolution_cycle_recovers_v1_history_and_runs_new_v2(tmp_path) -> None:
    interrupted = tmp_path / "interrupted"
    assert production_cli(interrupted, "init").returncode == 0
    assert production_cli(interrupted, "ingest", str(OBSERVATION)).returncode == 0
    assert production_cli(interrupted, "resume").returncode == 0

    old_environment = os.environ.copy()
    old_environment.update(
        {
            "MIOS_ENABLE_WORKFLOW_TEST_MODE": "1",
            "MIOS_TEST_WORKFLOW_REVISION": "1",
            "MIOS_ENABLE_CRASH_INJECTION": "1",
            "MIOS_TEST_CRASH_TRANSITION": "DESIGNED",
            "MIOS_TEST_CRASH_POINT": "after_registry_before_ledger",
        }
    )
    crashed = production_cli(interrupted, "run", environment=old_environment)
    assert crashed.returncode == 77, crashed.stderr

    current_environment = os.environ.copy()
    current_environment.update(
        {
            "MIOS_ENABLE_WORKFLOW_TEST_MODE": "1",
            "MIOS_TEST_WORKFLOW_REVISION": "2",
        }
    )
    recovered = production_cli(interrupted, "run", environment=current_environment)
    assert recovered.returncode == 0, recovered.stderr
    recovered_summary = json.loads(
        (interrupted / "evidence" / "semantic-summary.json").read_text()
    )
    assert recovered_summary["terminal_state"] == "LOCAL_CANDIDATE_READY"
    assert len(recovered_summary["effects"]) == 7
    assert len({item["kind"] for item in recovered_summary["effects"]}) == 7

    fresh = tmp_path / "fresh-v2"
    assert production_cli(fresh, "init").returncode == 0
    assert production_cli(fresh, "ingest", str(OBSERVATION)).returncode == 0
    assert production_cli(fresh, "resume").returncode == 0
    executed = production_cli(fresh, "run", environment=current_environment)
    assert executed.returncode == 0, executed.stderr
    fresh_summary = json.loads(
        (fresh / "evidence" / "semantic-summary.json").read_text()
    )
    assert fresh_summary["terminal_state"] == "LOCAL_CANDIDATE_READY"
    assert len(fresh_summary["effects"]) == 7
