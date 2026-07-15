from mios_controller.experiment import ExperimentRecord
from mios_controller.ledger import Ledger


def test_validated_experiment_record_is_idempotently_ledgered(tmp_path) -> None:
    from test_experiment import record

    ledger = Ledger(tmp_path / "evolution.jsonl", tmp_path / "head.json")
    experiment: ExperimentRecord = record()
    first = ledger.append_experiment_record(experiment)
    second = ledger.append_experiment_record(experiment)
    assert first == second
    assert ledger.verify()[0]["kind"] == "EXPERIMENT_RECORD_RECORDED"
