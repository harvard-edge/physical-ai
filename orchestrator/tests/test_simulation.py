from mios_controller.simulation import ClosedLoopSimulator


def test_closed_loop_simulation_exercises_logic_and_reset(tmp_path):
    report = ClosedLoopSimulator(tmp_path).run()
    assert report.taught
    assert report.recalled_after_restart
    assert report.action_status == "EXECUTED"
    assert report.failure_contained
    assert report.reset_empty
