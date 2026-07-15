"""Durable, provider-neutral agent council coordination.

The council passes immutable handoff records through a SQLite-backed queue. Model
providers are workers behind this interface; the coordinator owns state changes.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .task_packet import AgentTaskPacket


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CouncilTask:
    task_id: str
    role: str
    objective: str
    input_artifacts: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    parent_task_id: str | None = None
    budget: int = 1


@dataclass(frozen=True)
class Handoff:
    handoff_id: str
    task_id: str
    role: str
    status: str
    summary: str
    artifacts: tuple[str, ...]
    risks: tuple[str, ...]


class CouncilStore:
    """Small durable queue; SQLite is replaceable without changing worker APIs."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS council_tasks (
                    task_id TEXT PRIMARY KEY, role TEXT NOT NULL, objective TEXT NOT NULL,
                    input_artifacts TEXT NOT NULL, depends_on TEXT NOT NULL DEFAULT '[]',
                    parent_task_id TEXT, budget INTEGER NOT NULL,
                    status TEXT NOT NULL, created_at TEXT NOT NULL, claimed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS council_handoffs (
                    handoff_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, role TEXT NOT NULL,
                    status TEXT NOT NULL, summary TEXT NOT NULL, artifacts TEXT NOT NULL,
                    risks TEXT NOT NULL, created_at TEXT NOT NULL
                );
                """
            )
            columns = {
                row["name"] for row in db.execute("PRAGMA table_info(council_tasks)")
            }
            if "depends_on" not in columns:
                db.execute(
                    "ALTER TABLE council_tasks ADD COLUMN depends_on TEXT NOT NULL DEFAULT '[]'"
                )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def enqueue(self, task: CouncilTask) -> None:
        if not task.objective.strip():
            raise ValueError("task objective cannot be empty")
        if task.budget < 1:
            raise ValueError("task budget must be positive")
        with self._connect() as db:
            db.execute(
                "INSERT INTO council_tasks "
                "(task_id, role, objective, input_artifacts, depends_on, parent_task_id, "
                "budget, status, created_at, claimed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)",
                (
                    task.task_id,
                    task.role,
                    task.objective,
                    json.dumps(task.input_artifacts),
                    json.dumps(task.depends_on),
                    task.parent_task_id,
                    task.budget,
                    "QUEUED",
                    _now(),
                ),
            )

    def enqueue_packet(self, packet: AgentTaskPacket) -> None:
        """Validate and enqueue a worker task from the shared packet contract."""
        self.enqueue(
            CouncilTask(
                task_id=packet.task_id,
                role=packet.role,
                objective=packet.objective,
                budget=packet.budgets.tokens,
            )
        )

    def claim(self, role: str) -> CouncilTask | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT task.* FROM council_tasks task WHERE task.role=? AND task.status='QUEUED' "
                "AND NOT EXISTS (SELECT 1 FROM json_each(task.depends_on) dep "
                "LEFT JOIN council_tasks prerequisite ON prerequisite.task_id=dep.value "
                "WHERE prerequisite.task_id IS NULL OR prerequisite.status != 'COMPLETED') "
                "ORDER BY task.created_at LIMIT 1",
                (role,),
            ).fetchone()
            if row is None:
                return None
            db.execute(
                "UPDATE council_tasks SET status='RUNNING', claimed_at=? WHERE task_id=?",
                (_now(), row["task_id"]),
            )
            return CouncilTask(
                row["task_id"],
                row["role"],
                row["objective"],
                tuple(json.loads(row["input_artifacts"])),
                tuple(json.loads(row["depends_on"])),
                row["parent_task_id"],
                row["budget"],
            )

    def record(self, handoff: Handoff) -> None:
        if handoff.status not in {"COMPLETED", "BLOCKED", "REJECTED"}:
            raise ValueError("handoff has an invalid terminal status")
        with self._connect() as db:
            db.execute(
                "INSERT INTO council_handoffs VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    handoff.handoff_id,
                    handoff.task_id,
                    handoff.role,
                    handoff.status,
                    handoff.summary,
                    json.dumps(handoff.artifacts),
                    json.dumps(handoff.risks),
                    _now(),
                ),
            )
            db.execute(
                "UPDATE council_tasks SET status=? WHERE task_id=?",
                (handoff.status, handoff.task_id),
            )

    def recent_handoffs(self, limit: int = 50) -> list[Handoff]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT * FROM council_handoffs ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            Handoff(
                r["handoff_id"],
                r["task_id"],
                r["role"],
                r["status"],
                r["summary"],
                tuple(json.loads(r["artifacts"])),
                tuple(json.loads(r["risks"])),
            )
            for r in rows
        ]


Worker = Callable[[CouncilTask, tuple[Handoff, ...]], Handoff]


class CouncilCoordinator:
    """Routes work to registered roles; it never edits files or grants authority."""

    def __init__(self, store: CouncilStore) -> None:
        self.store = store
        self.workers: dict[str, Worker] = {}

    def register(self, role: str, worker: Worker) -> None:
        if role in self.workers:
            raise ValueError(f"worker already registered: {role}")
        self.workers[role] = worker

    def run_once(self, role: str) -> Handoff | None:
        worker = self.workers.get(role)
        if worker is None:
            raise KeyError(f"no worker registered for role: {role}")
        task = self.store.claim(role)
        if task is None:
            return None
        context = tuple(self.store.recent_handoffs())
        handoff = worker(task, context)
        if handoff.task_id != task.task_id or handoff.role != role:
            raise ValueError("worker handoff does not match claimed task")
        self.store.record(handoff)
        return handoff

    def run_until_idle(
        self, roles: tuple[str, ...], max_steps: int = 32
    ) -> list[Handoff]:
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        completed: list[Handoff] = []
        for _ in range(max_steps):
            progressed = False
            for role in roles:
                result = self.run_once(role)
                if result is not None:
                    completed.append(result)
                    progressed = True
            if not progressed:
                break
        return completed


def new_task_id() -> str:
    return f"MIOS-TASK-{uuid.uuid4().hex[:12].upper()}"


def new_handoff_id() -> str:
    return f"MIOS-HANDOFF-{uuid.uuid4().hex[:12].upper()}"
