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


def test_maya_test_cli_reports_thresholds(tmp_path, capsys):
    assert main(["maya-test", "--state", str(tmp_path / "memory.sqlite")]) == 0
    assert '"meets_charter_thresholds": true' in capsys.readouterr().out


def test_reconstruction_cli_compares_two_runs(tmp_path, capsys):
    assert main(["reconstruct-campaign", "--root", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert '"identical": true' in output
    assert '"reconstructions": 2' in output
