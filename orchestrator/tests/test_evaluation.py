import pytest

from mios_controller.evaluation import EvaluationManifest, ProtectedEvaluationRunner


def test_protected_evaluation_binds_checks_to_candidate():
    suite = "a" * 64
    runner = ProtectedEvaluationRunner(
        suite, {"safe": lambda digest: digest == "b" * 64}
    )
    result = runner.run(EvaluationManifest("MIOS-EVAL-001", "b" * 64, suite, ("safe",)))
    assert result.passed is True
    assert result.completed_checks == ("safe",)
    assert len(result.evidence_digest) == 64


def test_wrong_suite_or_unknown_check_is_rejected():
    runner = ProtectedEvaluationRunner("a" * 64, {"safe": lambda digest: True})
    with pytest.raises(ValueError):
        runner.run(EvaluationManifest("MIOS-EVAL-002", "b" * 64, "c" * 64, ("safe",)))
    with pytest.raises(ValueError):
        runner.run(
            EvaluationManifest("MIOS-EVAL-003", "b" * 64, "a" * 64, ("missing",))
        )
