from mios_controller.qa import run_software_qa


def test_independent_software_qa_reports_all_scenarios(tmp_path):
    report = run_software_qa(tmp_path)
    assert report.passed
    assert {finding.scenario for finding in report.findings} == {
        "teach-and-recall",
        "safe-action",
        "protective-stop",
        "reset-isolation",
    }
    assert not report.physical
