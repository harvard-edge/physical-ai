from mios_controller.portability import EmbodimentManifest, check_conformance


def test_uno_q_like_manifest_passes_portable_core():
    operations = frozenset(
        {
            "append",
            "promote",
            "retract",
            "search",
            "authorize",
            "protective_stop",
            "checkpoint",
            "resume",
        }
    )
    report = check_conformance(EmbodimentManifest("uno-q", "1.0.0", operations, 128))
    assert report.passed is True


def test_missing_safety_operation_fails_conformance():
    report = check_conformance(
        EmbodimentManifest("reachy", "1.0.0", frozenset({"append"}), 128)
    )
    assert report.passed is False
    assert "protective_stop" in report.missing_operations
