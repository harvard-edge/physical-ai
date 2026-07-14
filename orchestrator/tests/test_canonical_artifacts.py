from __future__ import annotations

import os

import pytest

from mios_controller.artifacts import ArtifactStore
from mios_controller.canonical import canonical_bytes, digest_json
from mios_controller.domain import IntegrityViolation
from mios_controller.ledger import Ledger


def test_canonical_json_is_order_independent() -> None:
    assert canonical_bytes({"b": 2, "a": 1}) == canonical_bytes({"a": 1, "b": 2})
    assert digest_json({"b": 2, "a": 1}) == digest_json({"a": 1, "b": 2})


def test_artifact_tampering_is_detected(tmp_path) -> None:
    store = ArtifactStore(tmp_path / "artifacts")
    reference = store.put_json("fixture", {"value": "expected"})
    path = store.path_for(reference.sha256)
    path.chmod(0o600)
    path.write_bytes(b"tampered")
    with pytest.raises(IntegrityViolation, match="digest mismatch"):
        store.read_verified(reference.sha256)


def test_artifact_links_are_rejected(tmp_path) -> None:
    store = ArtifactStore(tmp_path / "artifacts")
    reference = store.put_json("fixture", {"value": "expected"})
    path = store.path_for(reference.sha256)
    path.chmod(0o600)
    linked = tmp_path / "linked-artifact"
    os.link(path, linked)
    with pytest.raises(IntegrityViolation, match="single-linked"):
        store.read_verified(reference.sha256)
    linked.unlink()
    data = path.read_bytes()
    path.unlink()
    target = tmp_path / "outside"
    target.write_bytes(data)
    path.symlink_to(target)
    with pytest.raises(IntegrityViolation, match="missing or unsafe"):
        store.read_verified(reference.sha256)


def test_ledger_tampering_and_truncation_are_detected(tmp_path) -> None:
    ledger = Ledger(tmp_path / "ledger.jsonl", tmp_path / "trusted" / "head.json")
    ledger.append_once("event-1", "test", {"value": 1})
    ledger.append_once("event-2", "test", {"value": 2})
    assert len(ledger.verify()) == 2

    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    ledger.path.write_text(lines[0] + "\n", encoding="utf-8")
    with pytest.raises(IntegrityViolation, match="trusted head"):
        ledger.verify()


def test_ledger_event_id_is_idempotent(tmp_path) -> None:
    ledger = Ledger(tmp_path / "ledger.jsonl", tmp_path / "head.json")
    first = ledger.append_once("stable", "test", {"value": 1})
    second = ledger.append_once("stable", "test", {"value": 1})
    assert first == second
    with pytest.raises(IntegrityViolation, match="reused"):
        ledger.append_once("stable", "test", {"value": 2})
