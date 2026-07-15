from mios_controller.deployment import LocalDeploymentController, sign_manifest
from mios_controller.ledger import Ledger


def manifest():
    return sign_manifest(
        "release-2", "a" * 64, "MIOS-EXP-0001", "release-1", "test-key"
    )


def test_failed_health_check_rolls_back_to_known_good_release():
    controller = LocalDeploymentController("release-1")
    result = controller.stage(manifest(), lambda candidate: False)
    assert result.status == "ROLLED_BACK"
    assert controller.active_release == "release-1"


def test_healthy_candidate_promotes_from_inactive_slot():
    controller = LocalDeploymentController("release-1")
    result = controller.stage(manifest(), lambda candidate: True)
    assert result.status == "PROMOTED"
    assert controller.active_release == "release-2"


def test_deployment_decisions_are_recorded(tmp_path):
    ledger = Ledger(tmp_path / "ledger.jsonl", tmp_path / "head.json")
    controller = LocalDeploymentController("release-1", ledger=ledger)
    result = controller.stage(manifest(), lambda candidate: False)
    assert result.status == "ROLLED_BACK"
    records = ledger.verify()
    assert [record["kind"] for record in records] == [
        "DEPLOYMENT_DECISION",
        "DEPLOYMENT_DECISION",
    ]
