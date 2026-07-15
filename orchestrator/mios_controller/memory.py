"""Provenance-backed runtime memory tiers for the MiOS prototype."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

MemoryTier = Literal["episodic", "semantic", "procedural"]


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    tier: MemoryTier
    subject: str
    content: str
    confidence: float
    source_ids: tuple[str, ...]
    status: Literal["proposed", "accepted", "retracted"] = "proposed"


class MemoryStore:
    """Append-only memory records with explicit promotion and retraction."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS memory_records (
                    memory_id TEXT PRIMARY KEY,
                    tier TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                    source_ids TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS memory_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id TEXT NOT NULL,
                    event TEXT NOT NULL,
                    source_ids TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def append(self, record: MemoryRecord) -> None:
        if not record.source_ids:
            raise ValueError("memory records require provenance source IDs")
        if record.tier not in {"episodic", "semantic", "procedural"}:
            raise ValueError("unsupported memory tier")
        with self._connect() as db:
            db.execute(
                "INSERT INTO memory_records VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    record.memory_id,
                    record.tier,
                    record.subject,
                    record.content,
                    record.confidence,
                    json.dumps(record.source_ids),
                    record.status,
                    _now(),
                ),
            )
            db.execute(
                "INSERT INTO memory_events(memory_id, event, source_ids, created_at) VALUES (?, ?, ?, ?)",
                (record.memory_id, "APPENDED", json.dumps(record.source_ids), _now()),
            )

    def promote(
        self, memory_id: str, target_tier: MemoryTier, evidence_ids: tuple[str, ...]
    ) -> None:
        if target_tier == "episodic" or not evidence_ids:
            raise ValueError("promotion requires a durable target tier and evidence")
        with self._connect() as db:
            row = db.execute(
                "SELECT * FROM memory_records WHERE memory_id=?", (memory_id,)
            ).fetchone()
            if row is None:
                raise KeyError(memory_id)
            if row["status"] != "proposed":
                raise ValueError("only proposed memories may be promoted")
            db.execute(
                "UPDATE memory_records SET tier=?, status='accepted' WHERE memory_id=?",
                (target_tier, memory_id),
            )
            db.execute(
                "INSERT INTO memory_events(memory_id, event, source_ids, created_at) VALUES (?, ?, ?, ?)",
                (
                    memory_id,
                    f"PROMOTED:{target_tier}",
                    json.dumps(evidence_ids),
                    _now(),
                ),
            )

    def retract(self, memory_id: str, evidence_ids: tuple[str, ...]) -> None:
        if not evidence_ids:
            raise ValueError("retraction requires evidence")
        with self._connect() as db:
            if (
                db.execute(
                    "SELECT 1 FROM memory_records WHERE memory_id=?", (memory_id,)
                ).fetchone()
                is None
            ):
                raise KeyError(memory_id)
            db.execute(
                "UPDATE memory_records SET status='retracted' WHERE memory_id=?",
                (memory_id,),
            )
            db.execute(
                "INSERT INTO memory_events(memory_id, event, source_ids, created_at) VALUES (?, ?, ?, ?)",
                (memory_id, "RETRACTED", json.dumps(evidence_ids), _now()),
            )

    def search(
        self, subject: str, tier: MemoryTier | None = None
    ) -> list[MemoryRecord]:
        with self._connect() as db:
            if tier is None:
                rows = db.execute(
                    "SELECT * FROM memory_records WHERE subject=? ORDER BY created_at",
                    (subject,),
                ).fetchall()
            else:
                rows = db.execute(
                    "SELECT * FROM memory_records WHERE subject=? AND tier=? ORDER BY created_at",
                    (subject, tier),
                ).fetchall()
        return [
            MemoryRecord(
                r["memory_id"],
                r["tier"],
                r["subject"],
                r["content"],
                r["confidence"],
                tuple(json.loads(r["source_ids"])),
                r["status"],
            )
            for r in rows
        ]

    def reset(self, backup_path: str | Path | None = None) -> None:
        """Reset disposable memory, optionally preserving a SQLite backup."""
        target = Path(self.path)
        if backup_path is not None and target.exists():
            backup = sqlite3.connect(backup_path)
            source = sqlite3.connect(self.path)
            try:
                source.backup(backup)
            finally:
                backup.close()
                source.close()
        with self._connect() as db:
            db.execute("DELETE FROM memory_events")
            db.execute("DELETE FROM memory_records")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
