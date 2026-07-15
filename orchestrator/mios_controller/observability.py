"""Small privacy-filtered observability store for MiOS runtime and controller."""

from __future__ import annotations

import sqlite3
import uuid
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MetricSample:
    trace_id: str
    name: str
    value: float
    unit: str
    labels: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ActivityItem:
    """Privacy-safe activity projection; never contains raw payload text."""

    event_id: str
    kind: str
    privacy_class: str
    summary: str
    payload_digest: str
    created_at: str


@dataclass(frozen=True)
class BrainConcept:
    """Redacted semantic-memory projection with provenance identifiers only."""

    memory_id: str
    tier: str
    subject_digest: str
    content_digest: str
    confidence: float
    source_ids: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class ObservabilitySnapshot:
    schema_version: str
    generated_at: str
    mode: str
    activity: tuple[ActivityItem, ...]
    concepts: tuple[BrainConcept, ...]
    memory_counts: tuple[tuple[str, int], ...]
    runtime_event_count: int
    ledger_record_count: int
    safety: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "mode": self.mode,
            "activity": [item.__dict__ for item in self.activity],
            "concepts": [
                {**concept.__dict__, "source_ids": list(concept.source_ids)}
                for concept in self.concepts
            ],
            "memory_counts": {key: value for key, value in self.memory_counts},
            "runtime_event_count": self.runtime_event_count,
            "ledger_record_count": self.ledger_record_count,
            "safety": self.safety,
        }


class ObservabilityProjection:
    """Read-only, bounded projection for the operator dashboard.

    It reads existing stores without granting the dashboard write access. Raw
    memory content is deliberately never returned; concepts expose stable
    digests and provenance IDs so an authorized operator can correlate records
    without leaking child conversations.
    """

    SCHEMA_VERSION = "mios.observability.v1"

    def __init__(
        self,
        *,
        runtime_path: str | Path,
        memory_path: str | Path,
        ledger: Any | None = None,
        maintenance: Any | None = None,
        safety: dict[str, Any] | None = None,
        max_items: int = 100,
    ) -> None:
        if max_items < 1 or max_items > 1000:
            raise ValueError("max_items must be between 1 and 1000")
        self.runtime_path = str(runtime_path)
        self.memory_path = str(memory_path)
        self.ledger = ledger
        self.maintenance = maintenance
        self.safety = dict(safety or {})
        self.max_items = max_items

    def snapshot(self) -> ObservabilitySnapshot:
        activity = self._activity()
        concepts, counts = self._memory()
        ledger_count = 0
        if self.ledger is not None:
            ledger_count = len(self.ledger.verify())
        mode = getattr(self.maintenance, "mode", "UNKNOWN")
        return ObservabilitySnapshot(
            schema_version=self.SCHEMA_VERSION,
            generated_at=_now(),
            mode=str(mode),
            activity=tuple(activity),
            concepts=tuple(concepts),
            memory_counts=tuple(sorted(counts.items())),
            runtime_event_count=self._runtime_count(),
            ledger_record_count=ledger_count,
            safety={"state": "unknown", **self.safety},
        )

    def _activity(self) -> list[ActivityItem]:
        path = Path(self.runtime_path)
        if not path.exists():
            return []
        with sqlite3.connect(path) as db:
            rows = db.execute(
                "SELECT event_id, kind, summary, privacy_class, payload_digest, created_at "
                "FROM runtime_events ORDER BY created_at DESC LIMIT ?",
                (self.max_items,),
            ).fetchall()
        return [ActivityItem(*row) for row in rows]

    def _runtime_count(self) -> int:
        path = Path(self.runtime_path)
        if not path.exists():
            return 0
        with sqlite3.connect(path) as db:
            return int(db.execute("SELECT count(*) FROM runtime_events").fetchone()[0])

    def _memory(self) -> tuple[list[BrainConcept], dict[str, int]]:
        path = Path(self.memory_path)
        if not path.exists():
            return [], {}
        with sqlite3.connect(path) as db:
            rows = db.execute(
                "SELECT memory_id, tier, subject, content, confidence, source_ids, status "
                "FROM memory_records ORDER BY created_at DESC LIMIT ?",
                (self.max_items,),
            ).fetchall()
            count_rows = db.execute(
                "SELECT tier, count(*) FROM memory_records GROUP BY tier"
            ).fetchall()
        concepts = [
            BrainConcept(
                memory_id=row[0],
                tier=row[1],
                subject_digest=_digest_text(row[2]),
                content_digest=_digest_text(row[3]),
                confidence=float(row[4]),
                source_ids=tuple(json.loads(row[5])),
                status=row[6],
            )
            for row in rows
        ]
        return concepts, {str(tier): int(count) for tier, count in count_rows}


class ObservabilityStore:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS traces (
                    trace_id TEXT PRIMARY KEY, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS metrics (
                    sample_id INTEGER PRIMARY KEY AUTOINCREMENT, trace_id TEXT NOT NULL,
                    name TEXT NOT NULL, value REAL NOT NULL, unit TEXT NOT NULL,
                    labels TEXT NOT NULL, created_at TEXT NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def start_trace(self) -> str:
        trace_id = f"MIOS-TRACE-{uuid.uuid4().hex[:16].upper()}"
        with self._connect() as db:
            db.execute("INSERT INTO traces VALUES (?, ?)", (trace_id, _now()))
        return trace_id

    def record(self, sample: MetricSample) -> None:
        if not sample.trace_id.startswith("MIOS-TRACE-"):
            raise ValueError("metric must reference a MiOS trace")
        if len(sample.name) > 128 or len(sample.unit) > 32:
            raise ValueError("metric names and units must be bounded")
        if len(sample.labels) > 16 or any(
            len(k) > 64 or len(v) > 128 for k, v in sample.labels
        ):
            raise ValueError("metric labels exceed the telemetry budget")
        with self._connect() as db:
            if (
                db.execute(
                    "SELECT 1 FROM traces WHERE trace_id=?", (sample.trace_id,)
                ).fetchone()
                is None
            ):
                raise KeyError(sample.trace_id)
            db.execute(
                "INSERT INTO metrics(trace_id, name, value, unit, labels, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    sample.trace_id,
                    sample.name,
                    sample.value,
                    sample.unit,
                    repr(sample.labels),
                    _now(),
                ),
            )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
