"""Runtime event boundary and resumable cognitive checkpoints."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


EventKind = Literal["observation", "outcome", "failure", "maintenance", "mode_change"]


@dataclass(frozen=True)
class RuntimeEvent:
    event_id: str
    kind: EventKind
    summary: str
    privacy_class: Literal["synthetic", "derived-redacted", "internal", "restricted"]
    payload_digest: str


@dataclass(frozen=True)
class CognitiveCheckpoint:
    checkpoint_id: str
    goal_id: str
    context_digest: str
    memory_ids: tuple[str, ...]
    pending_action_ids: tuple[str, ...]
    model_provenance: str


class RuntimeBoundary:
    """Stores privacy-classified runtime records separately from the ledger."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS runtime_events (
                    event_id TEXT PRIMARY KEY, kind TEXT NOT NULL, summary TEXT NOT NULL,
                    privacy_class TEXT NOT NULL, payload_digest TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS cognitive_checkpoints (
                    checkpoint_id TEXT PRIMARY KEY, goal_id TEXT NOT NULL,
                    context_digest TEXT NOT NULL, memory_ids TEXT NOT NULL,
                    pending_action_ids TEXT NOT NULL, model_provenance TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def record_event(self, event: RuntimeEvent) -> None:
        if not event.summary.strip() or len(event.summary) > 2048:
            raise ValueError("runtime event summary must be bounded and non-empty")
        if len(event.payload_digest) != 64 or any(
            c not in "0123456789abcdef" for c in event.payload_digest
        ):
            raise ValueError("runtime payload must be represented by a SHA-256 digest")
        with self._connect() as db:
            db.execute(
                "INSERT INTO runtime_events VALUES (?, ?, ?, ?, ?, ?)",
                (
                    event.event_id,
                    event.kind,
                    event.summary,
                    event.privacy_class,
                    event.payload_digest,
                    _now(),
                ),
            )

    def checkpoint(self, state: CognitiveCheckpoint) -> None:
        for digest in (state.context_digest,):
            if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise ValueError("checkpoint context must be content addressed")
        if not state.model_provenance.strip():
            raise ValueError(
                "checkpoint requires model provenance or explicit fallback"
            )
        with self._connect() as db:
            db.execute(
                "INSERT INTO cognitive_checkpoints VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    state.checkpoint_id,
                    state.goal_id,
                    state.context_digest,
                    json.dumps(state.memory_ids),
                    json.dumps(state.pending_action_ids),
                    state.model_provenance,
                    _now(),
                ),
            )

    def latest_checkpoint(self, goal_id: str) -> CognitiveCheckpoint | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT * FROM cognitive_checkpoints WHERE goal_id=? ORDER BY created_at DESC LIMIT 1",
                (goal_id,),
            ).fetchone()
        if row is None:
            return None
        return CognitiveCheckpoint(
            row["checkpoint_id"],
            row["goal_id"],
            row["context_digest"],
            tuple(json.loads(row["memory_ids"])),
            tuple(json.loads(row["pending_action_ids"])),
            row["model_provenance"],
        )


def digest_payload(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
