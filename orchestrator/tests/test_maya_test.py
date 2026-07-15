from mios_controller.maya_test import run_synthetic_maya_test


def test_synthetic_maya_test_retains_grounded_fact_across_restart(tmp_path):
    result = run_synthetic_maya_test(tmp_path / "memory.sqlite")
    assert result.retained_after_restart
    assert result.evidence_grounded
    assert result.held_out_generalization
    assert not result.physical
    assert result.meets_charter_thresholds
