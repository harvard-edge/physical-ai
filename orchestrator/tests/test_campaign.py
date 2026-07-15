from mios_controller.campaign import run_replay_campaign
from mios_controller.ledger import Ledger


def test_replay_campaign_completes_dependency_order(tmp_path):
    result = run_replay_campaign(
        tmp_path / "campaign.sqlite",
        ledger=Ledger(tmp_path / "ledger.jsonl", tmp_path / "head.json"),
        report_path=tmp_path / "report.json",
    )

    assert [handoff.role for handoff in result.handoffs] == [
        "architect",
        "implementer",
        "verifier",
    ]
    assert result.release.verdict == "approved"
    assert (
        '"kind":"REPLAY_CAMPAIGN_COMPLETED"' in (tmp_path / "ledger.jsonl").read_text()
    )
    assert (
        '"kind":"EXPERIMENT_RECORD_RECORDED"' in (tmp_path / "ledger.jsonl").read_text()
    )
    assert (
        '"campaign_id": "MIOS-CAMPAIGN-REPLAY-001"'
        in (tmp_path / "report.json").read_text()
    )
