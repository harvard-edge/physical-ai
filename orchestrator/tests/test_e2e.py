from __future__ import annotations

import json
import hashlib
import os
import signal
import shutil
import sqlite3
import subprocess
import time
from pathlib import Path

from mios_controller.engine import EvolutionEngine
from mios_controller.supervisor import Supervisor


REPOSITORY = Path(__file__).resolve().parents[2]
CLI = Path(__file__).resolve().parents[1] / ".venv" / "bin" / "mios-controller"
OBSERVATION = REPOSITORY / "evolution" / "fixtures" / "synthetic-observation.json"


def run_cli(*arguments: str, environment=None, check=True):
    command = [str(CLI), *arguments, "--repository", str(REPOSITORY)]
    return subprocess.run(
        command,
        cwd=REPOSITORY,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=check,
        timeout=45,
    )


def initialized(root: Path) -> None:
    run_cli("init", "--root", str(root))
    run_cli("ingest", "--root", str(root), str(OBSERVATION))
    run_cli("resume", "--root", str(root))


def file_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_signal_handler_defers_durable_work_to_normal_control_flow(
    tmp_path, monkeypatch
) -> None:
    supervisor = Supervisor(EvolutionEngine(tmp_path / "controller", REPOSITORY))
    stop_requests: list[str] = []
    monkeypatch.setattr(supervisor, "request_stop", stop_requests.append)

    supervisor._handle_signal(signal.SIGTERM, None)

    assert stop_requests == []
    assert supervisor._pending_signal == signal.SIGTERM
    assert supervisor._persist_pending_signal() is True
    assert stop_requests == ["received signal SIGTERM"]


def test_containerized_end_to_end_cycle(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    run_cli("run", "--root", str(root))
    result = json.loads(run_cli("verify", "--root", str(root)).stdout)
    assert result["final_experiments"] == ["MIOS-EXP-0001"]
    assert result["reachy_code_unchanged"] is True
    summary = json.loads((root / "evidence" / "semantic-summary.json").read_text())
    assert summary["terminal_state"] == "LOCAL_CANDIDATE_READY"
    assert len(summary["transitions"]) == 7
    assert len(summary["effects"]) == 7
    assert set(summary["external_effect_counts"].values()) == {0}


def test_independent_reviewer_failure_pauses_without_downstream_effect(
    tmp_path,
) -> None:
    root = tmp_path / "controller"
    initialized(root)
    environment = os.environ.copy()
    environment["MIOS_TEST_REVIEW_FAILURE_ROLE"] = "research_skeptic"

    failed = run_cli("run", "--root", str(root), environment=environment, check=False)

    assert failed.returncode != 0
    status = json.loads(run_cli("status", "--root", str(root)).stdout)
    assert status["controller_state"] in {"PAUSED", "INCIDENT"}
    assert status["accept_new_work"] is False
    assert status["experiments"][0]["state"] == "PAUSED"
    assert not (root / "forge" / "MIOS-EXP-0001" / "pull-request.json").exists()
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        effects = [row[0] for row in connection.execute("SELECT kind FROM effects")]
        prepared = connection.execute(
            "SELECT status FROM effect_intents WHERE effect_kind='local_review_attestations'"
        ).fetchone()[0]
    assert "local_review_attestations" not in effects
    assert "local_pull_request_manifest" not in effects
    assert prepared == "prepared"


def test_malformed_worker_result_pauses_before_candidate_effect(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    environment = os.environ.copy()
    environment["MIOS_TEST_WORKER_RESULT_MODE"] = "malformed"

    failed = run_cli("run", "--root", str(root), environment=environment, check=False)

    assert failed.returncode != 0
    status = json.loads(run_cli("status", "--root", str(root)).stdout)
    assert status["accept_new_work"] is False
    assert status["experiments"][0]["state"] == "PAUSED"
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        effects = [row[0] for row in connection.execute("SELECT kind FROM effects")]
        intent = connection.execute(
            "SELECT status FROM effect_intents WHERE effect_kind='local_candidate_commit'"
        ).fetchone()[0]
    assert effects == [
        "local_issue_manifest",
        "local_preregistration",
        "local_design",
    ]
    assert intent == "prepared"


def test_duplicate_ingestion_creates_one_experiment_and_one_cycle(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    duplicate = json.loads(
        run_cli("ingest", "--root", str(root), str(OBSERVATION)).stdout
    )
    assert duplicate == {"created": False, "experiment_id": "MIOS-EXP-0001"}
    run_cli("run", "--root", str(root))
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        assert connection.execute("SELECT COUNT(*) FROM experiments").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM effects").fetchone()[0] == 7


def test_exhausted_budget_pauses_before_first_effect(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        connection.execute(
            "UPDATE budget_counters SET used=cap WHERE resource='wall_ms'"
        )
    failed = run_cli("run", "--root", str(root), check=False)
    assert failed.returncode != 0
    status = json.loads(run_cli("status", "--root", str(root)).stdout)
    assert status["accept_new_work"] is False
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        assert connection.execute("SELECT COUNT(*) FROM effects").fetchone()[0] == 0


def test_dbos_recovers_crash_without_duplicate_effects(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    environment = os.environ.copy()
    environment["MIOS_ENABLE_CRASH_INJECTION"] = "1"
    environment["MIOS_TEST_CRASH_TRANSITION"] = "DESIGNED"
    environment["MIOS_TEST_CRASH_POINT"] = "after_registry_before_ledger"
    crashed = run_cli("run", "--root", str(root), environment=environment, check=False)
    assert crashed.returncode == 77
    recovered = run_cli("run", "--root", str(root), environment=os.environ.copy())
    assert recovered.returncode == 0
    summary = json.loads((root / "evidence" / "semantic-summary.json").read_text())
    assert (
        len(summary["effects"])
        == len({item["kind"] for item in summary["effects"]})
        == 7
    )


def test_review_packet_reconciles_after_effect_before_artifact_crash(
    tmp_path,
) -> None:
    root = tmp_path / "controller"
    initialized(root)
    environment = os.environ.copy()
    environment.update(
        {
            "MIOS_ENABLE_CRASH_INJECTION": "1",
            "MIOS_TEST_CRASH_TRANSITION": "EVALUATING",
            "MIOS_TEST_CRASH_POINT": "after_effect_before_artifact",
        }
    )
    crashed = run_cli("run", "--root", str(root), environment=environment, check=False)
    assert crashed.returncode == 77

    recovered = run_cli("run", "--root", str(root), environment=os.environ.copy())
    assert recovered.returncode == 0, recovered.stderr
    result = json.loads(run_cli("verify", "--root", str(root)).stdout)
    assert result["final_experiments"] == ["MIOS-EXP-0001"]
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        assert connection.execute("SELECT COUNT(*) FROM reviews").fetchone()[0] == 2


def test_supervisor_requires_explicit_resume(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    denied = run_cli("supervise", "--root", str(root), "--max-cycles", "1", check=False)
    assert denied.returncode != 0
    assert "explicit resume" in denied.stderr


def test_status_inspection_does_not_modify_controller_state(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    before = file_snapshot(root)
    status = json.loads(run_cli("status", "--root", str(root)).stdout)
    after = file_snapshot(root)
    assert status["experiments"][0]["state"] == "OBSERVED"
    assert before == after


def test_idle_supervisor_stops_on_sigterm_and_persists_pause(tmp_path) -> None:
    root = tmp_path / "controller"
    run_cli("init", "--root", str(root))
    run_cli("resume", "--root", str(root))
    process = subprocess.Popen(
        [
            str(CLI),
            "supervise",
            "--root",
            str(root),
            "--repository",
            str(REPOSITORY),
            "--continuous",
            "--resume",
        ],
        cwd=REPOSITORY,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(1)
    process.terminate()
    stdout, stderr = process.communicate(timeout=15)
    assert process.returncode == 0, stderr
    result = json.loads(stdout)
    assert result["state"] == "PAUSED"
    status = json.loads(run_cli("status", "--root", str(root)).stdout)
    assert status["controller_state"] == "PAUSED"
    assert status["accept_new_work"] is False


def test_sigterm_cancels_active_container_work_within_bound(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    environment = os.environ.copy()
    environment["MIOS_TEST_WORKER_DELAY_SECONDS"] = "60"
    process = subprocess.Popen(
        [
            str(CLI),
            "run",
            "--root",
            str(root),
            "--repository",
            str(REPOSITORY),
        ],
        cwd=REPOSITORY,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(3)
    stopped_at = time.monotonic()
    process.terminate()
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode == 0, stderr
    assert time.monotonic() - stopped_at < 5
    assert json.loads(stdout)["state"] == "PAUSED"
    assert (root / "STOP").is_file()
    status = json.loads(run_cli("status", "--root", str(root)).stdout)
    assert status["accept_new_work"] is False
    with sqlite3.connect(root / "registry" / "mios.sqlite3") as connection:
        effects = [row[0] for row in connection.execute("SELECT kind FROM effects")]
    assert effects == [
        "local_issue_manifest",
        "local_preregistration",
        "local_design",
    ]
    containers = subprocess.run(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            "name=mios-",
            "--format",
            "{{.Names}}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert not any(name.endswith("-mios-att-0004") for name in containers)


def test_persistent_pause_blocks_ordinary_run_and_supervise_resume(tmp_path) -> None:
    root = tmp_path / "controller"
    initialized(root)
    run_cli("pause", "--root", str(root))

    ordinary = run_cli("run", "--root", str(root), check=False)
    supervised = run_cli(
        "supervise",
        "--root",
        str(root),
        "--resume",
        "--max-cycles",
        "1",
        check=False,
    )

    assert ordinary.returncode != 0
    assert supervised.returncode != 0
    assert "persistent kill switch" in ordinary.stderr
    assert "persistent kill switch" in supervised.stderr
    assert (root / "STOP").is_file()


def test_normalized_evidence_is_reproducible(tmp_path) -> None:
    summaries = []
    for name in ("first", "second"):
        root = tmp_path / name
        initialized(root)
        run_cli("run", "--root", str(root))
        summaries.append((root / "evidence" / "semantic-summary.json").read_bytes())
    assert summaries[0] == summaries[1]


def test_evidence_reconstructs_without_workspace_or_workflow_database(tmp_path) -> None:
    source = tmp_path / "source"
    reconstructed = tmp_path / "reconstructed"
    initialized(source)
    run_cli("run", "--root", str(source))
    for name in (
        "artifacts",
        "assurance",
        "evidence",
        "forge",
        "ledger",
        "metadata",
        "registry",
    ):
        shutil.copytree(source / name, reconstructed / name)
    result = json.loads(run_cli("verify", "--root", str(reconstructed)).stdout)
    assert result["final_experiments"] == ["MIOS-EXP-0001"]
    assert not (reconstructed / "workspaces").exists()
    assert not (reconstructed / "checkpoints").exists()
