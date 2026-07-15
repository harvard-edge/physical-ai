from mios_controller.campaign import run_replay_campaign


def test_replay_campaign_completes_dependency_order(tmp_path):
    result = run_replay_campaign(tmp_path / "campaign.sqlite")

    assert [handoff.role for handoff in result.handoffs] == [
        "architect",
        "implementer",
        "verifier",
    ]
    assert result.release.verdict == "approved"
