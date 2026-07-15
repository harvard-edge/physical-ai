from mios_controller.experiment import ExperimentRecord
from mios_controller.ledger import Ledger
from mios_controller.lineage import inspect_lineage


def test_lineage_report_distinguishes_complete_local_chain(tmp_path):
    ledger = Ledger(tmp_path / "ledger.jsonl", tmp_path / "head.json")
    experiment = ExperimentRecord(
        experiment_id="MIOS-EXP-0001",
        campaign_id="MIOS-CAMPAIGN-001",
        autonomy_level_claimed="A1",
        trigger={
            "observation_ids": ["MIOS-OBS-0001"],
            "detected_by": "test",
            "privacy_class": "synthetic",
        },
        hypothesis={"statement": "test", "expected_mechanism": "test"},
        baseline={"release": "r0", "comparison_condition": "fixed_single_agent"},
        preregistration={
            "artifact_hash": "a" * 64,
            "frozen_at": "now",
            "primary_metric": "x",
            "minimum_effect": 0,
            "sample_size": 1,
        },
        selected_design="test",
        evaluation={
            "public_suite": "test",
            "simulation_result": "pass",
            "evaluator_version": "1",
        },
        change={},
        review={
            "architecture": "approve",
            "safety": "approve",
            "verification": "approve",
        },
        deployment={},
        outcome={"decision": "accepted", "autonomy_level_supported": "A1"},
        lesson={},
    )
    ledger.append_experiment_record(experiment)
    ledger.append_once(
        "transition-1",
        "experiment_transition",
        {"experiment_id": experiment.experiment_id},
    )
    ledger.append_once(
        "deploy-1",
        "DEPLOYMENT_DECISION",
        {"source_experiment": experiment.experiment_id, "release_id": "r1"},
    )
    report = inspect_lineage(ledger, experiment.experiment_id)
    assert report.complete_local_lineage
    assert report.observation_ids == ("MIOS-OBS-0001",)
    assert report.deployment_releases == ("r1",)
