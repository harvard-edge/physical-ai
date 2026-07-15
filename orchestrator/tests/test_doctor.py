from mios_controller.doctor import DoctorCheck, DoctorLifecycle, DoctorPhase


def test_doctor_persists_ready_report_and_reloads(tmp_path):
    lifecycle = DoctorLifecycle(
        tmp_path / "doctor.json",
        checks=(lambda root: DoctorCheck("local", True, detail=str(root)),),
    )
    report = lifecycle.run()
    assert report.phase is DoctorPhase.READY
    assert report.passed
    restored = lifecycle.load()
    assert restored is not None
    assert restored.run_id == 1
    assert restored.phase is DoctorPhase.READY


def test_required_failure_blocks_ready_but_optional_failure_degrades(tmp_path):
    checks = (
        lambda root: DoctorCheck("required", False, detail="bad"),
        lambda root: DoctorCheck("optional", False, severity="advisory"),
    )
    report = DoctorLifecycle(tmp_path / "doctor.json", checks=checks).run()
    assert report.phase is DoctorPhase.FAILED
    assert not report.passed

    report = DoctorLifecycle(
        tmp_path / "doctor.json",
        checks=(lambda root: DoctorCheck("optional", False, severity="advisory"),),
    ).run()
    assert report.phase is DoctorPhase.DEGRADED
    assert report.passed


def test_doctor_recovery_reruns_checks_with_monotonic_run_id(tmp_path):
    lifecycle = DoctorLifecycle(
        tmp_path / "doctor.json", checks=(lambda root: DoctorCheck("ok", True),)
    )
    lifecycle.run()
    report = lifecycle.recover()
    assert report.phase is DoctorPhase.READY
    assert report.run_id == 3


def test_doctor_captures_check_exception_as_failure(tmp_path):
    def broken(root):
        raise RuntimeError("fixture failure")

    report = DoctorLifecycle(tmp_path / "doctor.json", checks=(broken,)).run()
    assert report.phase is DoctorPhase.FAILED
    assert report.checks[0].name == "doctor_execution"
