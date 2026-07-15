import pytest

from mios_controller.runtime import (
    CognitiveCheckpoint,
    RuntimeBoundary,
    RuntimeEvent,
    digest_payload,
)


def test_runtime_event_and_checkpoint_survive_restart(tmp_path):
    path = tmp_path / "runtime.sqlite"
    boundary = RuntimeBoundary(path)
    boundary.record_event(
        RuntimeEvent(
            "MIOS-EVENT-001", "observation", "name taught", "synthetic", "a" * 64
        )
    )
    boundary.checkpoint(
        CognitiveCheckpoint(
            "MIOS-CKPT-001",
            "MIOS-GOAL-001",
            "b" * 64,
            ("mem-1",),
            (),
            "deterministic-fallback",
        )
    )

    restarted = RuntimeBoundary(path)
    checkpoint = restarted.latest_checkpoint("MIOS-GOAL-001")
    assert checkpoint is not None
    assert checkpoint.model_provenance == "deterministic-fallback"


def test_runtime_boundary_rejects_raw_payloads():
    boundary = RuntimeBoundary(":memory:")
    with pytest.raises(ValueError):
        boundary.record_event(
            RuntimeEvent("MIOS-EVENT-002", "failure", "oops", "synthetic", "raw text")
        )
    assert (
        digest_payload(b"hello")
        == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )
