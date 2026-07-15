from pathlib import Path

from mios_controller.cli import main


def test_replay_campaign_cli_writes_report(tmp_path, capsys):
    assert (
        main(
            [
                "replay-campaign",
                "--state",
                str(tmp_path / "state.sqlite"),
                "--ledger",
                str(tmp_path / "ledger.jsonl"),
                "--head",
                str(tmp_path / "head.json"),
                "--report",
                str(tmp_path / "report.json"),
            ]
        )
        == 0
    )
    assert '"release_verdict": "approved"' in capsys.readouterr().out
    assert Path(tmp_path / "report.json").exists()
