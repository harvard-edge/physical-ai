from __future__ import annotations

import json
import shutil
import sqlite3

import pytest

import mios_controller.engine as engine_module
from mios_controller.domain import IntegrityViolation
from mios_controller.engine import EvolutionEngine


REPOSITORY = engine_module.Path(__file__).resolve().parents[2]


def critical_repository(tmp_path):
    repository = tmp_path / "repository"
    (repository / "code").mkdir(parents=True)
    (repository / "governance").symlink_to(
        REPOSITORY / "governance", target_is_directory=True
    )
    shutil.copytree(REPOSITORY / "protocol", repository / "protocol")
    shutil.copytree(
        REPOSITORY / "evolution" / "fixtures",
        repository / "evolution" / "fixtures",
    )
    shutil.copytree(
        REPOSITORY / "evolution" / "approvals",
        repository / "evolution" / "approvals",
    )
    shutil.copytree(
        REPOSITORY / "orchestrator" / "mios_controller",
        repository / "orchestrator" / "mios_controller",
    )
    shutil.copyfile(
        REPOSITORY / "orchestrator" / "uv.lock",
        repository / "orchestrator" / "uv.lock",
    )
    return repository


def test_package_release_advances_without_losing_manifest_history(
    tmp_path, monkeypatch
) -> None:
    root = tmp_path / "controller"
    repository = tmp_path / "repository"
    (repository / "code").mkdir(parents=True)
    (repository / "evolution" / "fixtures").mkdir(parents=True)
    for name in ("governance", "protocol"):
        source = engine_module.Path(__file__).resolve().parents[2] / name
        target = repository / name
        target.symlink_to(source, target_is_directory=True)

    first = EvolutionEngine(root, repository).initialize()
    monkeypatch.setattr(engine_module, "CONTROLLER_RELEASE_VERSION", "0.2.1")
    second = EvolutionEngine(root, repository).initialize()

    history = sorted((root / "metadata" / "releases").glob("*.json"))
    assert len(history) == 2
    assert {
        json.loads(path.read_text())["controller_release_version"] for path in history
    } == {
        first["controller_release_version"],
        second["controller_release_version"],
    }
    current = json.loads((root / "metadata" / "run-manifest.json").read_text())
    assert current == second
    assert (
        first["workflow_compatibility_version"]
        == second["workflow_compatibility_version"]
    )


def test_incompatible_workflow_change_requires_drain_and_rejects_declaration(
    tmp_path, monkeypatch
) -> None:
    repository = engine_module.Path(__file__).resolve().parents[2]
    root = tmp_path / "controller"
    first_engine = EvolutionEngine(root, repository)
    first_engine.initialize()
    first_engine.ingest_file(
        repository / "evolution" / "fixtures" / "synthetic-observation.json"
    )

    monkeypatch.setattr(engine_module, "WORKFLOW_COMPATIBILITY_VERSION", "2")
    with pytest.raises(IntegrityViolation, match="active experiments"):
        EvolutionEngine(root, repository).initialize()

    migration = {
        "schema_version": "1.0.0",
        "from_version": "1",
        "to_version": "2",
        "mode": "migration",
        "status": "completed",
        "policy_digest": first_engine.policy.digest,
    }
    (root / "metadata" / "workflow-migration.json").write_text(
        json.dumps(migration, sort_keys=True), encoding="utf-8"
    )
    with pytest.raises(IntegrityViolation, match="old line was drained"):
        EvolutionEngine(root, repository).initialize()


def test_incompatible_workflow_change_is_allowed_after_complete_drain(
    tmp_path, monkeypatch
) -> None:
    repository = engine_module.Path(__file__).resolve().parents[2]
    root = tmp_path / "controller"
    engine = EvolutionEngine(root, repository)
    engine.initialize()
    experiment_id, _ = engine.ingest_file(
        repository / "evolution" / "fixtures" / "synthetic-observation.json"
    )
    engine.registry.resume(engine.policy.digest)
    for state in engine_module.NEXT_STATE:
        engine.run_transition(experiment_id, state)

    monkeypatch.setattr(engine_module, "WORKFLOW_COMPATIBILITY_VERSION", "2")
    with pytest.raises(IntegrityViolation, match="controller drained: False"):
        EvolutionEngine(root, repository).initialize()

    engine.registry.pause("drained for incompatible upgrade")
    manifest = EvolutionEngine(root, repository).initialize()

    assert manifest["workflow_compatibility_version"] == "2"


def test_incompatible_workflow_change_requires_dbos_history_to_be_terminal(
    tmp_path, monkeypatch
) -> None:
    repository = engine_module.Path(__file__).resolve().parents[2]
    root = tmp_path / "controller"
    engine = EvolutionEngine(root, repository)
    engine.initialize()
    checkpoint = engine.paths.dbos_database
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(checkpoint) as connection:
        connection.execute(
            """
            CREATE TABLE workflow_status (
                workflow_uuid TEXT PRIMARY KEY,
                status TEXT,
                application_version TEXT
            )
            """
        )
        connection.execute(
            "INSERT INTO workflow_status VALUES ('workflow-1', 'PENDING', 'mios-evolution-1')"
        )

    monkeypatch.setattr(engine_module, "WORKFLOW_COMPATIBILITY_VERSION", "2")
    with pytest.raises(IntegrityViolation, match="active DBOS workflows"):
        EvolutionEngine(root, repository).initialize()

    with sqlite3.connect(checkpoint) as connection:
        connection.execute(
            "UPDATE workflow_status SET status='SUCCESS' WHERE workflow_uuid='workflow-1'"
        )
    manifest = EvolutionEngine(root, repository).initialize()
    assert manifest["workflow_compatibility_version"] == "2"


def test_release_manifest_binds_registry_schema(tmp_path) -> None:
    repository = engine_module.Path(__file__).resolve().parents[2]
    manifest = EvolutionEngine(tmp_path / "controller", repository).initialize()

    assert manifest["registry_schema"] == {
        "current": 3,
        "minimum": 3,
        "maximum": 3,
    }


@pytest.mark.parametrize(
    "relative_path",
    [
        "orchestrator/mios_controller/canonical.py",
        "evolution/fixtures/synthetic-observation.json",
        "protocol/agent-task.schema.json",
        "orchestrator/uv.lock",
        "evolution/approvals/PHASE-1A.yml",
    ],
)
def test_execution_critical_input_tampering_is_detected(
    tmp_path, relative_path
) -> None:
    repository = critical_repository(tmp_path)
    engine = EvolutionEngine(tmp_path / "controller", repository)
    engine.initialize()
    target = repository / relative_path
    target.write_bytes(target.read_bytes() + b"\n")

    with pytest.raises(IntegrityViolation, match="execution-critical"):
        engine._assert_execution_integrity()


def test_restart_cannot_bless_changed_controller_after_experiment_creation(
    tmp_path,
) -> None:
    repository = critical_repository(tmp_path)
    root = tmp_path / "controller"
    engine = EvolutionEngine(root, repository)
    engine.initialize()
    engine.ingest_file(repository / "evolution/fixtures/synthetic-observation.json")
    controller_source = repository / "orchestrator/mios_controller/canonical.py"
    controller_source.write_bytes(controller_source.read_bytes() + b"\n")

    with pytest.raises(IntegrityViolation, match="release activation"):
        EvolutionEngine(root, repository).initialize()
