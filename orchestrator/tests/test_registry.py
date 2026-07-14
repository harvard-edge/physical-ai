from __future__ import annotations

import sqlite3
import time

import pytest

from mios_controller.domain import (
    BudgetViolation,
    ExperimentState,
    IntegrityViolation,
    ObservationInput,
    StaleLease,
)
from mios_controller.registry import Registry


CAPS = {
    "wall_ms": 1000,
    "storage_bytes": 1000,
    "attempts": 4,
    "model_tokens": 0,
    "provider_calls": 0,
    "wip_experiments": 1,
    "controller_runtime_ms": 100,
}


def observation() -> ObservationInput:
    return ObservationInput(
        observation_id="MIOS-OBS-0001",
        source="synthetic_fixture",
        privacy_class="synthetic",
        summary="Synthetic observation",
        payload={"observed": "old", "expected": "new"},
    )


def registry(tmp_path) -> Registry:
    value = Registry(tmp_path / "registry.sqlite3")
    value.initialize("CAMPAIGN", "a" * 64, CAPS)
    value.resume("a" * 64)
    return value


def test_registry_rejects_a_newer_schema_without_rewriting_it(tmp_path) -> None:
    path = tmp_path / "registry.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        connection.execute(
            "INSERT INTO settings(key, value) VALUES ('schema_version', '4')"
        )

    value = Registry(path)
    with pytest.raises(IntegrityViolation, match="newer than this controller"):
        value.initialize("CAMPAIGN", "a" * 64, CAPS)

    with sqlite3.connect(path) as connection:
        assert (
            connection.execute(
                "SELECT value FROM settings WHERE key='schema_version'"
            ).fetchone()[0]
            == "4"
        )


def test_registry_records_an_approved_monotonic_migration(tmp_path) -> None:
    path = tmp_path / "registry.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        connection.execute(
            "INSERT INTO settings(key, value) VALUES ('schema_version', '2')"
        )

    value = Registry(path)
    value.initialize("CAMPAIGN", "a" * 64, CAPS)

    assert value.setting("schema_version") == "3"
    assert value.export()["schema_migrations"] == [
        {
            "target_version": 3,
            "source_version": 2,
            "migrated_at": value.export()["schema_migrations"][0]["migrated_at"],
        }
    ]


def test_registry_refuses_to_migrate_nonempty_legacy_state(tmp_path) -> None:
    value = registry(tmp_path)
    value.ingest(observation())
    with sqlite3.connect(value.path) as connection:
        connection.execute("UPDATE settings SET value='2' WHERE key='schema_version'")

    with pytest.raises(IntegrityViolation, match="empty drained registry"):
        value.initialize("CAMPAIGN", "a" * 64, CAPS)


def prepare_effect(value: Registry, lease, *, action_digest: str = "d" * 64):
    return value.prepare_effect_intent(
        lease,
        "effect",
        action_digest,
        "b" * 64,
    )


def test_duplicate_observation_produces_one_experiment(tmp_path) -> None:
    value = registry(tmp_path)
    first = value.ingest(observation())
    second = value.ingest(observation())
    assert first == ("MIOS-EXP-0001", True)
    assert second == ("MIOS-EXP-0001", False)
    assert len(value.export()["experiments"]) == 1


def test_wip_limit_rejects_a_second_active_experiment(tmp_path) -> None:
    value = registry(tmp_path)
    value.ingest(observation())
    second = observation().model_copy(
        update={
            "observation_id": "MIOS-OBS-0002",
            "summary": "A different synthetic observation",
        }
    )

    with pytest.raises(BudgetViolation, match="work-in-progress limit"):
        value.ingest(second)

    assert len(value.export()["experiments"]) == 1


def test_atomic_budget_reservation_rejects_over_cap(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    with pytest.raises(BudgetViolation, match="wall_ms"):
        value.claim_transition(
            experiment_id,
            ExperimentState.OBSERVED,
            ExperimentState.TRIAGED,
            "worker",
            "a" * 64,
            10,
            {"wall_ms": 1001},
        )
    assert value.export()["attempts"] == []


def test_controller_runtime_budget_is_durable_and_atomic(tmp_path) -> None:
    value = registry(tmp_path)
    assert value.consume_budget("controller_runtime_ms", 40) == 60
    assert value.budget_remaining("controller_runtime_ms") == 60
    with pytest.raises(BudgetViolation, match="controller_runtime_ms"):
        value.consume_budget("controller_runtime_ms", 61)
    assert value.budget_remaining("controller_runtime_ms") == 60


def test_expired_lease_is_fenced_and_attempt_is_retained(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    first = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker-a",
        "a" * 64,
        0.03,
        {"wall_ms": 10, "attempts": 1},
    )
    time.sleep(0.04)
    second = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker-b",
        "a" * 64,
        1,
        {"wall_ms": 10, "attempts": 1},
    )
    adopted = prepare_effect(value, second)
    assert second.fencing_token > first.fencing_token
    assert adopted["fencing_token"] == second.fencing_token
    with pytest.raises(StaleLease):
        value.complete_transition(
            first, "effect", "b" * 64, "c" * 64, {"wall_ms": 1, "attempts": 1}
        )
    attempts = value.export()["attempts"]
    assert [attempt["status"] for attempt in attempts] == ["abandoned", "running"]


def test_expired_lease_cannot_complete_without_reclaim(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    lease = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker",
        "a" * 64,
        0.03,
        {"wall_ms": 10, "attempts": 1},
    )
    prepare_effect(value, lease)
    time.sleep(0.04)

    with pytest.raises(StaleLease, match="expired"):
        value.complete_transition(
            lease, "effect", "b" * 64, "c" * 64, {"wall_ms": 1, "attempts": 1}
        )

    assert value.get_experiment(experiment_id)["state"] == "OBSERVED"


def test_expired_lease_cannot_register_an_effect(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    lease = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker",
        "a" * 64,
        0.001,
        {"wall_ms": 10, "attempts": 1},
    )
    time.sleep(0.01)

    with pytest.raises(StaleLease, match="expired"):
        prepare_effect(value, lease)

    exported = value.export()
    assert exported["effect_intents"] == []
    assert exported["effects"] == []
    assert exported["transitions"] == []


def test_live_lease_can_heartbeat_and_complete(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    lease = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker",
        "a" * 64,
        0.03,
        {"wall_ms": 10, "attempts": 1},
        max_lease_seconds=0.2,
    )
    time.sleep(0.015)
    renewed = value.heartbeat(lease, 0.08)
    assert renewed.expires_at > lease.expires_at
    assert renewed.deadline_at == lease.deadline_at
    time.sleep(0.04)

    prepare_effect(value, renewed)
    value.complete_transition(
        renewed, "effect", "b" * 64, "c" * 64, {"wall_ms": 1, "attempts": 1}
    )
    assert value.get_experiment(experiment_id)["state"] == "TRIAGED"


def test_heartbeat_is_capped_at_claim_time_deadline(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    lease = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker",
        "a" * 64,
        0.02,
        {"wall_ms": 10, "attempts": 1},
        max_lease_seconds=0.05,
    )

    renewed = value.heartbeat(lease, 10)
    assert renewed.expires_at == renewed.deadline_at
    assert renewed.deadline_at == lease.deadline_at
    time.sleep(0.06)
    with pytest.raises(StaleLease, match="expired"):
        value.heartbeat(renewed, 10)


def test_completion_requires_a_prepared_effect_intent(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    lease = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker",
        "a" * 64,
        1,
        {"wall_ms": 10, "attempts": 1},
    )

    with pytest.raises(IntegrityViolation, match="prepared durable intent"):
        value.complete_transition(
            lease, "effect", "b" * 64, "c" * 64, {"wall_ms": 1, "attempts": 1}
        )

    assert value.export()["effects"] == []


def test_identical_effect_intent_retry_is_adopted_but_mismatch_fails(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    first = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker-a",
        "a" * 64,
        0.03,
        {"wall_ms": 10, "attempts": 1},
    )
    original = prepare_effect(value, first)
    time.sleep(0.04)
    second = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker-b",
        "a" * 64,
        1,
        {"wall_ms": 10, "attempts": 1},
    )

    adopted = prepare_effect(value, second)
    assert adopted["idempotency_key"] == original["idempotency_key"]
    assert adopted["fencing_token"] == second.fencing_token
    with pytest.raises(IntegrityViolation, match="different identity"):
        prepare_effect(value, second, action_digest="e" * 64)


def test_transition_atomically_completes_matching_effect_intent(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    lease = value.claim_transition(
        experiment_id,
        ExperimentState.OBSERVED,
        ExperimentState.TRIAGED,
        "worker",
        "a" * 64,
        1,
        {"wall_ms": 10, "attempts": 1},
    )
    prepared = prepare_effect(value, lease)

    value.complete_transition(
        lease, "effect", "b" * 64, "c" * 64, {"wall_ms": 1, "attempts": 1}
    )

    exported = value.export()
    intent = exported["effect_intents"][0]
    assert intent["idempotency_key"] == prepared["idempotency_key"]
    assert intent["status"] == "completed"
    assert intent["output_digest"] == "c" * 64
    assert intent["completed_at"] is not None
    assert len(exported["effects"]) == 1
    assert len(exported["transitions"]) == 1


def test_review_retry_must_match_the_original_attestation(tmp_path) -> None:
    value = registry(tmp_path)
    experiment_id, _ = value.ingest(observation())
    review = {
        "experiment_id": experiment_id,
        "role": "verification_engineer",
        "reviewer_identity": "reviewer-a",
        "candidate_commit": "a" * 40,
        "evidence_digest": "b" * 64,
        "verdict": "approve",
        "decisive": True,
    }
    value.add_reviews([review])
    value.add_reviews([review])

    changed = {**review, "verdict": "reject"}
    with pytest.raises(IntegrityViolation, match="idempotency key"):
        value.add_reviews([changed])

    assert value.reviews_for(experiment_id)[0]["verdict"] == "approve"
