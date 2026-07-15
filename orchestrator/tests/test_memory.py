import pytest

from mios_controller.memory import MemoryRecord, MemoryStore


def test_memory_promotion_requires_evidence_and_preserves_history(tmp_path):
    store = MemoryStore(tmp_path / "memory.sqlite")
    store.append(
        MemoryRecord(
            "MIOS-MEM-001", "episodic", "maya", "name is Maya", 0.9, ("obs-1",)
        )
    )

    with pytest.raises(ValueError):
        store.promote("MIOS-MEM-001", "semantic", ())
    store.promote("MIOS-MEM-001", "semantic", ("review-1",))

    record = store.search("maya")[0]
    assert record.tier == "semantic"
    assert record.status == "accepted"
