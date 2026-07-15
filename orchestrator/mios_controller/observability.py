"""Small privacy-filtered observability store for MiOS runtime and controller."""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class MetricSample:
    trace_id: str
    name: str
    value: float
    unit: str
    labels: tuple[tuple[str, str], ...] = ()


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
