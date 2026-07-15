"""Embedded episodic and semantic memory backed by SQLite."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any

ALLOWED_PREDICATES = {
    "is_a",
    "part_of",
    "has_property",
    "likes",
    "dislikes",
    "knows",
    "named",
    "located_in",
    "created_by",
    "related_to",
    "can_do",
    "interested_in",
}


class _ManagedConnection(sqlite3.Connection):
    """Close SQLite connections when used as context managers."""

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def default_memory_path() -> Path:
    """Choose persistent app data outside the installed Python package."""
    override = os.environ.get("MAYAS_REACHY_MEMORY_FILE")
    if override:
        return Path(override).expanduser()
    data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return data_home / "mayas-reachy" / "memory.sqlite3"


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _canonical(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())[:80]


class MemoryStore:
    """Thread-safe event, entity, claim, and evidence store for one robot."""

    def __init__(self, path: Path | None = None) -> None:
        requested = path or default_memory_path()
        # Older callers and installations may still point at memory.json.
        self.legacy_path = requested if requested.suffix == ".json" else requested.with_name("memory.json")
        self.path = requested.with_suffix(".sqlite3") if requested.suffix == ".json" else requested
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._initialize()
        self._migrate_legacy_json()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=5, factory=_ManagedConnection)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._lock, self._connect() as db:
            db.execute("PRAGMA journal_mode = WAL")
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS episodes (
                    id TEXT PRIMARY KEY, occurred_at TEXT NOT NULL, session_id TEXT NOT NULL,
                    speaker TEXT NOT NULL, text TEXT NOT NULL, source TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS entities (
                    id TEXT PRIMARY KEY, kind TEXT NOT NULL, canonical_name TEXT NOT NULL,
                    normalized_name TEXT NOT NULL, created_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active',
                    UNIQUE(kind, normalized_name)
                );
                CREATE TABLE IF NOT EXISTS aliases (
                    entity_id TEXT NOT NULL REFERENCES entities(id), alias TEXT NOT NULL,
                    normalized_alias TEXT NOT NULL, UNIQUE(entity_id, normalized_alias)
                );
                CREATE TABLE IF NOT EXISTS claims (
                    id TEXT PRIMARY KEY, subject_id TEXT NOT NULL REFERENCES entities(id),
                    predicate TEXT NOT NULL, object_id TEXT REFERENCES entities(id), literal_value TEXT,
                    confidence REAL NOT NULL, origin TEXT NOT NULL, valid_from TEXT NOT NULL,
                    valid_until TEXT, status TEXT NOT NULL DEFAULT 'active',
                    CHECK (object_id IS NOT NULL OR literal_value IS NOT NULL)
                );
                CREATE TABLE IF NOT EXISTS evidence (
                    claim_id TEXT NOT NULL REFERENCES claims(id), episode_id TEXT NOT NULL REFERENCES episodes(id),
                    PRIMARY KEY(claim_id, episode_id)
                );
                CREATE TABLE IF NOT EXISTS skills (
                    name TEXT PRIMARY KEY, description TEXT NOT NULL, implementation TEXT NOT NULL,
                    safety_class TEXT NOT NULL, enabled INTEGER NOT NULL DEFAULT 1
                );
                CREATE TABLE IF NOT EXISTS memory_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS claims_subject ON claims(subject_id, status);
                CREATE INDEX IF NOT EXISTS claims_object ON claims(object_id, status);
                """
            )
            db.executemany(
                "INSERT OR IGNORE INTO skills(name, description, implementation, safety_class) VALUES(?,?,?,?)",
                [
                    ("listen", "Capture one bounded microphone turn", "MayasReachyApp.capture_microphone", "sensory"),
                    ("speak", "Synthesize and play a short reply", "PiperVoiceSynthesizer", "conversational"),
                    ("look", "Move the head within approved limits", "MayasReachyApp.perform_response", "physical"),
                    ("gesture", "Perform an approved expressive motion", "MayasReachyApp.perform_response", "physical"),
                ],
            )
            try:
                db.execute(
                    "CREATE VIRTUAL TABLE IF NOT EXISTS episodes_fts USING fts5(episode_id UNINDEXED, text)"
                )
            except sqlite3.OperationalError:
                pass

    def _migrate_legacy_json(self) -> None:
        if not self.legacy_path.exists():
            return
        with self._lock, self._connect() as db:
            if db.execute("SELECT 1 FROM memory_meta WHERE key='legacy_migrated'").fetchone():
                return
        try:
            data = json.loads(self.legacy_path.read_text(encoding="utf-8"))
            name = data.get("robot", {}).get("name")
        except (OSError, json.JSONDecodeError, AttributeError):
            name = None
        if isinstance(name, str) and name.strip() and not self.robot_name():
            self.remember_robot_name(name.strip(), origin="imported")
        with self._lock, self._connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO memory_meta(key, value) VALUES('legacy_migrated', ?)",
                (_now(),),
            )

    def record_episode(
        self,
        speaker: str,
        text: str,
        *,
        source: str = "web_chat",
        session_id: str = "family",
    ) -> str:
        episode_id = str(uuid.uuid4())
        cleaned = text.strip()[:2000]
        with self._lock, self._connect() as db:
            db.execute(
                "INSERT INTO episodes VALUES(?, ?, ?, ?, ?, ?)",
                (episode_id, _now(), session_id, speaker[:80], cleaned, source),
            )
            try:
                db.execute(
                    "INSERT INTO episodes_fts(episode_id, text) VALUES(?, ?)",
                    (episode_id, cleaned),
                )
            except sqlite3.OperationalError:
                pass
        return episode_id

    def resolve_entity(self, name: str, kind: str = "concept") -> str:
        canonical = _canonical(name)
        normalized = canonical.casefold()
        if not canonical:
            raise ValueError("Entity name cannot be empty")
        with self._lock, self._connect() as db:
            row = db.execute(
                "SELECT id FROM entities WHERE kind=? AND normalized_name=? AND status='active'",
                (kind[:32], normalized),
            ).fetchone()
            if row:
                return str(row["id"])
            entity_id = str(uuid.uuid4())
            db.execute(
                "INSERT INTO entities(id, kind, canonical_name, normalized_name, created_at) VALUES(?,?,?,?,?)",
                (entity_id, kind[:32], canonical, normalized, _now()),
            )
            return entity_id

    def remember_claim(
        self,
        subject: str,
        predicate: str,
        *,
        object_name: str | None = None,
        literal_value: str | None = None,
        subject_kind: str = "concept",
        object_kind: str = "concept",
        confidence: float = 1.0,
        origin: str = "asserted",
        episode_id: str | None = None,
    ) -> dict[str, Any]:
        if predicate not in ALLOWED_PREDICATES:
            raise ValueError(f"Unsupported relationship: {predicate}")
        subject_id = self.resolve_entity(subject, subject_kind)
        object_id = self.resolve_entity(object_name, object_kind) if object_name else None
        literal = _canonical(literal_value) if literal_value else None
        if object_id is None and literal is None:
            raise ValueError("A claim needs an object or literal value")
        with self._lock, self._connect() as db:
            existing = db.execute(
                """SELECT id FROM claims WHERE subject_id=? AND predicate=?
                   AND COALESCE(object_id,'')=COALESCE(?, '') AND COALESCE(literal_value,'')=COALESCE(?, '')
                   AND status='active'""",
                (subject_id, predicate, object_id, literal),
            ).fetchone()
            claim_id = str(existing["id"]) if existing else str(uuid.uuid4())
            if existing:
                db.execute(
                    "UPDATE claims SET confidence=MAX(confidence, ?) WHERE id=?",
                    (max(0.0, min(1.0, confidence)), claim_id),
                )
            else:
                db.execute(
                    "INSERT INTO claims VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (
                        claim_id, subject_id, predicate, object_id, literal,
                        max(0.0, min(1.0, confidence)), origin, _now(), None, "active",
                    ),
                )
            if episode_id:
                db.execute(
                    "INSERT OR IGNORE INTO evidence(claim_id, episode_id) VALUES(?,?)",
                    (claim_id, episode_id),
                )
        return {"id": claim_id, "subject": subject, "predicate": predicate, "object": object_name or literal}

    def robot_name(self) -> str | None:
        with self._lock, self._connect() as db:
            row = db.execute(
                """SELECT COALESCE(o.canonical_name, c.literal_value) AS value
                   FROM claims c JOIN entities s ON s.id=c.subject_id
                   LEFT JOIN entities o ON o.id=c.object_id
                   WHERE s.kind='robot' AND s.normalized_name='self' AND c.predicate='named'
                     AND c.status='active' ORDER BY c.valid_from DESC LIMIT 1"""
            ).fetchone()
        return str(row["value"]) if row and row["value"] else None

    def remember_robot_name(
        self, name: str, *, episode_id: str | None = None, origin: str = "asserted"
    ) -> dict[str, Any]:
        with self._lock, self._connect() as db:
            self_id = self.resolve_entity("self", "robot")
            db.execute(
                "UPDATE claims SET status='superseded', valid_until=? WHERE subject_id=? AND predicate='named' AND status='active'",
                (_now(), self_id),
            )
        claim = self.remember_claim(
            "self", "named", literal_value=_canonical(name), subject_kind="robot",
            confidence=1.0, origin=origin, episode_id=episode_id,
        )
        return {"robot": {"name": name, "claim_id": claim["id"]}}

    def relevant_context(self, query: str, limit: int = 8) -> list[dict[str, Any]]:
        tokens = [t.casefold() for t in re.findall(r"[A-Za-z0-9'-]+", query) if len(t) > 1]
        with self._lock, self._connect() as db:
            params: list[Any] = []
            where = "c.status='active'"
            if tokens:
                where += " AND (" + " OR ".join(
                    ["s.normalized_name LIKE ? OR COALESCE(o.normalized_name,'') LIKE ? OR c.predicate LIKE ?"] * len(tokens)
                ) + ")"
                for token in tokens:
                    params.extend((f"%{token}%", f"%{token}%", f"%{token}%"))
            rows = db.execute(
                f"""SELECT c.id, s.canonical_name subject, c.predicate,
                    COALESCE(o.canonical_name, c.literal_value) object, c.confidence, c.origin,
                    'claim' AS memory_type
                    FROM claims c JOIN entities s ON s.id=c.subject_id
                    LEFT JOIN entities o ON o.id=c.object_id WHERE {where}
                    ORDER BY c.valid_from DESC LIMIT ?""",
                (*params, limit),
            ).fetchall()
            if not rows and tokens:
                rows = db.execute(
                    """SELECT c.id, s.canonical_name subject, c.predicate,
                       COALESCE(o.canonical_name,c.literal_value) object, c.confidence, c.origin,
                       'claim' AS memory_type
                       FROM claims c JOIN entities s ON s.id=c.subject_id LEFT JOIN entities o ON o.id=c.object_id
                       WHERE c.status='active' ORDER BY c.valid_from DESC LIMIT ?""",
                    (limit,),
                ).fetchall()
            results = [dict(row) for row in rows]
            if tokens and len(results) < limit:
                try:
                    match = " OR ".join(f'"{token}"' for token in tokens[:8])
                    episodes = db.execute(
                        """SELECT e.id, e.speaker, e.text, e.occurred_at, 'episode' memory_type
                           FROM episodes_fts f JOIN episodes e ON e.id=f.episode_id
                           WHERE episodes_fts MATCH ? ORDER BY rank LIMIT ?""",
                        (match, limit - len(results)),
                    ).fetchall()
                    results.extend(dict(row) for row in episodes)
                except sqlite3.OperationalError:
                    pass
        return results

    def snapshot(self) -> dict[str, Any]:
        with self._lock, self._connect() as db:
            counts = {
                table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in ("episodes", "entities", "claims", "skills")
            }
        return {"version": 2, "robot": {"name": self.robot_name()}, "counts": counts, "facts": self.relevant_context("")}

    def forget_claim(self, claim_id: str) -> bool:
        with self._lock, self._connect() as db:
            result = db.execute(
                "UPDATE claims SET status='forgotten', valid_until=? WHERE id=? AND status='active'",
                (_now(), claim_id),
            )
        return result.rowcount > 0

    def reset(self, *, hard: bool = False) -> Path | None:
        """Archive current beliefs, or back up and recreate the complete database."""
        with self._lock:
            if not hard:
                with self._connect() as db:
                    db.execute(
                        "UPDATE claims SET status='forgotten', valid_until=? WHERE status='active'",
                        (_now(),),
                    )
                return None
            backup = self.path.with_name(f"memory-backup-{int(time.time())}.sqlite3")
            if self.path.exists():
                with self._connect() as source, sqlite3.connect(backup, factory=_ManagedConnection) as target:
                    source.backup(target)
                self.path.unlink()
            for suffix in ("-wal", "-shm"):
                Path(str(self.path) + suffix).unlink(missing_ok=True)
            self._initialize()
            return backup
