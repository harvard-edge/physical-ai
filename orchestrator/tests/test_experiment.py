import pytest
from pydantic import ValidationError

from mios_controller.experiment import ExperimentRecord


def record() -> ExperimentRecord:
    return ExperimentRecord(
        experiment_id="MIOS-EXP-0001",
        campaign_id="MIOS-CAMPAIGN-001",
        autonomy_level_claimed="A1",
        trigger={"detected_by": "runtime-monitor", "privacy_class": "synthetic"},
        hypothesis={
            "statement": "bounded change improves recall",
            "expected_mechanism": "better retrieval",
        },
        baseline={"release": "r0", "comparison_condition": "fixed_single_agent"},
        preregistration={
            "artifact_hash": "a" * 64,
            "frozen_at": "2026-07-15T00:00:00Z",
            "primary_metric": "recall",
            "minimum_effect": 0.1,
            "sample_size": 10,
        },
        selected_design="replay",
        evaluation={
            "public_suite": "suite-1",
            "simulation_result": "pass",
            "evaluator_version": "1",
        },
        change={},
        review={
            "architecture": "pending",
            "safety": "pending",
            "verification": "pending",
        },
        deployment={},
        outcome={"decision": "inconclusive", "autonomy_level_supported": "A0"},
        lesson={},
    )


def test_experiment_record_is_canonicalizable() -> None:
    value = record()
    assert value.to_payload()["schema_version"] == "1.0.0"
    assert value.to_payload()["trigger"]["observation_ids"] == []


def test_experiment_record_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ExperimentRecord(**{**record().to_payload(), "unexpected": True})
