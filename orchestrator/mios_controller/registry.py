"""MiOS experiment registry and fenced work leases."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .canonical import canonical_bytes, digest_json, utc_now
from .domain import (
    BudgetViolation,
    ControllerState,
    ExperimentState,
    IntegrityViolation,
    ObservationInput,
    StaleLease,
)


SCHEMA_VERSION = 3


@dataclass(frozen=True)
class Lease:
    work_id: str
    attempt_id: str
    experiment_id: str
    from_state: ExperimentState
    to_state: ExperimentState
    worker_id: str
    fencing_token: int
    expires_at: float
    deadline_at: float
    reservation_id: str


class Registry:
    def __init__(self, path: Path, create_parent: bool = True):
        self.path = path
        if create_parent:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self, readonly: bool = False) -> sqlite3.Connection:
        if readonly:
            connection = sqlite3.connect(
                f"file:{self.path}?mode=ro&immutable=1", uri=True, timeout=5
            )
        else:
            connection = sqlite3.connect(self.path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        if not readonly:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = FULL")
        return connection

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(
        self,
        campaign_id: str,
        policy_digest: str,
        budget_caps: dict[str, int],
        approval_digest: str | None = None,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            stored_schema_row = connection.execute(
                "SELECT value FROM settings WHERE key='schema_version'"
            ).fetchone()
            stored_schema_version: int | None = None
            if stored_schema_row is not None:
                try:
                    stored_schema_version = int(stored_schema_row["value"])
                except (TypeError, ValueError) as error:
                    raise IntegrityViolation(
                        "registry schema version is malformed"
                    ) from error
                if stored_schema_version > SCHEMA_VERSION:
                    raise IntegrityViolation(
                        "registry schema is newer than this controller supports: "
                        f"{stored_schema_version}>{SCHEMA_VERSION}"
                    )
                if (
                    stored_schema_version < SCHEMA_VERSION
                    and stored_schema_version
                    not in {
                        1,
                        2,
                    }
                ):
                    raise IntegrityViolation(
                        "registry schema has no approved forward migration: "
                        f"{stored_schema_version}->{SCHEMA_VERSION}"
                    )
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS observations (
                    id TEXT PRIMARY KEY,
                    fingerprint TEXT NOT NULL UNIQUE,
                    payload_digest TEXT NOT NULL,
                    payload_json BLOB NOT NULL,
                    privacy_class TEXT NOT NULL CHECK (privacy_class = 'synthetic'),
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    observation_id TEXT NOT NULL UNIQUE REFERENCES observations(id),
                    state TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    terminal_reason TEXT
                );
                CREATE TABLE IF NOT EXISTS work_items (
                    id TEXT PRIMARY KEY,
                    experiment_id TEXT NOT NULL REFERENCES experiments(id),
                    from_state TEXT NOT NULL,
                    to_state TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL DEFAULT 0,
                    lease_owner TEXT,
                    lease_expires REAL,
                    lease_deadline REAL,
                    fencing_token INTEGER NOT NULL DEFAULT 0,
                    config_digest TEXT NOT NULL,
                    UNIQUE(experiment_id, from_state, to_state)
                );
                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY,
                    work_id TEXT NOT NULL REFERENCES work_items(id),
                    fencing_token INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    error_class TEXT,
                    error_message TEXT
                );
                CREATE TABLE IF NOT EXISTS effects (
                    idempotency_key TEXT PRIMARY KEY,
                    experiment_id TEXT NOT NULL REFERENCES experiments(id),
                    kind TEXT NOT NULL,
                    input_digest TEXT NOT NULL,
                    output_digest TEXT NOT NULL,
                    fencing_token INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS effect_intents (
                    idempotency_key TEXT PRIMARY KEY,
                    experiment_id TEXT NOT NULL REFERENCES experiments(id),
                    work_id TEXT NOT NULL REFERENCES work_items(id),
                    effect_kind TEXT NOT NULL,
                    action_implementation_digest TEXT NOT NULL,
                    input_digest TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('prepared', 'completed')),
                    fencing_token INTEGER NOT NULL,
                    output_digest TEXT,
                    prepared_at TEXT NOT NULL,
                    completed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS transitions (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT NOT NULL REFERENCES experiments(id),
                    from_state TEXT NOT NULL,
                    to_state TEXT NOT NULL,
                    evidence_digest TEXT NOT NULL,
                    fencing_token INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(experiment_id, to_state)
                );
                CREATE TABLE IF NOT EXISTS reviews (
                    experiment_id TEXT NOT NULL REFERENCES experiments(id),
                    role TEXT NOT NULL,
                    reviewer_identity TEXT NOT NULL,
                    candidate_commit TEXT NOT NULL,
                    evidence_digest TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    decisive INTEGER NOT NULL,
                    PRIMARY KEY(experiment_id, role, candidate_commit)
                );
                CREATE TABLE IF NOT EXISTS budget_counters (
                    resource TEXT PRIMARY KEY,
                    cap INTEGER NOT NULL,
                    used INTEGER NOT NULL DEFAULT 0,
                    reserved INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS budget_reservations (
                    reservation_id TEXT NOT NULL,
                    resource TEXT NOT NULL REFERENCES budget_counters(resource),
                    amount INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    PRIMARY KEY(reservation_id, resource)
                );
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    target_version INTEGER PRIMARY KEY,
                    source_version INTEGER NOT NULL,
                    migrated_at TEXT NOT NULL
                );
                """
            )
            work_item_columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(work_items)")
            }
            if "lease_deadline" not in work_item_columns:
                connection.execute(
                    "ALTER TABLE work_items ADD COLUMN lease_deadline REAL"
                )
                connection.execute(
                    """
                    UPDATE work_items SET lease_deadline=lease_expires
                    WHERE lease_expires IS NOT NULL
                    """
                )
            defaults = {
                "schema_version": str(SCHEMA_VERSION),
                "campaign_id": campaign_id,
                "policy_digest": policy_digest,
                "approval_digest": approval_digest or "",
                "controller_state": ControllerState.PAUSED.value,
                "accept_new_work": "false",
                "last_error": "",
            }
            for key, value in defaults.items():
                connection.execute(
                    "INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)",
                    (key, value),
                )
            for key in ("campaign_id", "policy_digest", "approval_digest"):
                stored_value = connection.execute(
                    "SELECT value FROM settings WHERE key=?", (key,)
                ).fetchone()["value"]
                if stored_value != defaults[key]:
                    raise IntegrityViolation(
                        f"immutable campaign setting changed: {key}"
                    )
            if (
                stored_schema_version is not None
                and stored_schema_version < SCHEMA_VERSION
            ):
                existing_domain_rows = sum(
                    int(
                        connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[
                            0
                        ]
                    )
                    for table in ("experiments", "effects", "transitions")
                )
                if existing_domain_rows:
                    raise IntegrityViolation(
                        "registry schema migration requires an empty drained registry"
                    )
                connection.execute(
                    "UPDATE settings SET value=? WHERE key='schema_version'",
                    (str(SCHEMA_VERSION),),
                )
                connection.execute(
                    """
                    INSERT OR IGNORE INTO schema_migrations(
                        target_version, source_version, migrated_at
                    ) VALUES (?, ?, ?)
                    """,
                    (SCHEMA_VERSION, stored_schema_version, utc_now()),
                )
            for resource, cap in budget_caps.items():
                connection.execute(
                    "INSERT OR IGNORE INTO budget_counters(resource, cap) VALUES (?, ?)",
                    (resource, cap),
                )
                stored = connection.execute(
                    "SELECT cap FROM budget_counters WHERE resource = ?", (resource,)
                ).fetchone()["cap"]
                if stored != cap:
                    raise BudgetViolation(
                        f"budget cap changed for {resource}: {stored} != {cap}"
                    )
            connection.commit()
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")

    def integrity_check(self) -> None:
        with self.connect(readonly=True) as connection:
            result = connection.execute("PRAGMA quick_check").fetchone()[0]
            if result != "ok":
                raise RuntimeError(f"registry integrity check failed: {result}")

    def setting(self, key: str) -> str:
        with self.connect(readonly=True) as connection:
            row = connection.execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            ).fetchone()
            if row is None:
                raise KeyError(key)
            return str(row["value"])

    def _set_setting(
        self, connection: sqlite3.Connection, key: str, value: str
    ) -> None:
        connection.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))

    def pause(self, reason: str, incident: bool = False) -> None:
        with self.transaction() as connection:
            self._set_setting(connection, "accept_new_work", "false")
            self._set_setting(
                connection,
                "controller_state",
                ControllerState.INCIDENT.value
                if incident
                else ControllerState.PAUSED.value,
            )
            self._set_setting(connection, "last_error", reason)

    def begin_pausing(self, reason: str) -> None:
        with self.transaction() as connection:
            self._set_setting(connection, "accept_new_work", "false")
            self._set_setting(
                connection, "controller_state", ControllerState.PAUSING.value
            )
            self._set_setting(connection, "last_error", reason)

    def resume(
        self,
        policy_digest: str,
        campaign_id: str | None = None,
        approval_digest: str | None = None,
    ) -> None:
        with self.transaction() as connection:
            settings = {
                row["key"]: row["value"]
                for row in connection.execute("SELECT key, value FROM settings")
            }
            if settings["controller_state"] == ControllerState.INCIDENT.value:
                raise RuntimeError("incident state requires repair and a new approval")
            if settings["policy_digest"] != policy_digest:
                raise RuntimeError(
                    "policy digest changed; stored approval cannot authorize resume"
                )
            if campaign_id is not None and settings["campaign_id"] != campaign_id:
                raise RuntimeError("campaign identity does not match stored approval")
            if (
                approval_digest is not None
                and settings.get("approval_digest") != approval_digest
            ):
                raise RuntimeError("approval artifact digest does not match")
            self._set_setting(
                connection, "controller_state", ControllerState.RUNNING.value
            )
            self._set_setting(connection, "accept_new_work", "true")
            self._set_setting(connection, "last_error", "")

    def abandon_running_leases(self, reason: str) -> int:
        """Fence leases left by a process that no longer owns the supervisor lock."""

        with self.transaction() as connection:
            rows = connection.execute(
                "SELECT id FROM work_items WHERE status='running' ORDER BY id"
            ).fetchall()
            for row in rows:
                connection.execute(
                    """
                    UPDATE attempts SET status='abandoned', finished_at=?, error_class='ProcessBoundary',
                        error_message=? WHERE work_id=? AND status='running'
                    """,
                    (utc_now(), reason[:2048], row["id"]),
                )
                self._consume_abandoned_reservations(connection, row["id"])
                connection.execute(
                    """
                    UPDATE work_items SET status='pending', lease_owner=NULL, lease_expires=NULL
                    WHERE id=?
                    """,
                    (row["id"],),
                )
            return len(rows)

    def ingest(self, observation: ObservationInput) -> tuple[str, bool]:
        payload = observation.model_dump(mode="json")
        fingerprint = digest_json(
            {
                "source": observation.source,
                "privacy_class": observation.privacy_class,
                "summary": observation.summary,
                "payload": observation.payload,
            }
        )
        payload_digest = digest_json(payload)
        now = utc_now()
        with self.transaction() as connection:
            existing = connection.execute(
                "SELECT id FROM observations WHERE fingerprint = ?", (fingerprint,)
            ).fetchone()
            if existing:
                experiment = connection.execute(
                    "SELECT id FROM experiments WHERE observation_id = ?",
                    (existing["id"],),
                ).fetchone()
                return str(experiment["id"]), False
            wip_counter = connection.execute(
                "SELECT cap FROM budget_counters WHERE resource='wip_experiments'"
            ).fetchone()
            wip_limit = int(wip_counter["cap"]) if wip_counter is not None else 1
            active_experiments = int(
                connection.execute(
                    """
                    SELECT COUNT(*) FROM experiments
                    WHERE state NOT IN ('LOCAL_CANDIDATE_READY', 'REJECTED')
                    """
                ).fetchone()[0]
            )
            if active_experiments >= wip_limit:
                raise BudgetViolation(
                    f"work-in-progress limit reached: {active_experiments}/{wip_limit}"
                )
            sequence = connection.execute(
                "SELECT COUNT(*) + 1 AS value FROM experiments"
            ).fetchone()["value"]
            experiment_id = f"MIOS-EXP-{sequence:04d}"
            connection.execute(
                "INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?)",
                (
                    observation.observation_id,
                    fingerprint,
                    payload_digest,
                    canonical_bytes(payload),
                    observation.privacy_class,
                    now,
                ),
            )
            connection.execute(
                "INSERT INTO experiments(id, observation_id, state, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (
                    experiment_id,
                    observation.observation_id,
                    ExperimentState.OBSERVED.value,
                    now,
                    now,
                ),
            )
            return experiment_id, True

    def next_experiment(self) -> dict[str, Any] | None:
        with self.connect(readonly=True) as connection:
            row = connection.execute(
                """
                SELECT * FROM experiments
                WHERE state NOT IN ('LOCAL_CANDIDATE_READY', 'PAUSED', 'REJECTED', 'INCIDENT')
                ORDER BY created_at, id LIMIT 1
                """
            ).fetchone()
            return dict(row) if row else None

    def get_experiment(self, experiment_id: str) -> dict[str, Any]:
        with self.connect(readonly=True) as connection:
            row = connection.execute(
                "SELECT * FROM experiments WHERE id = ?", (experiment_id,)
            ).fetchone()
            if row is None:
                raise KeyError(experiment_id)
            return dict(row)

    def transition_to(
        self, experiment_id: str, to_state: ExperimentState
    ) -> dict[str, Any] | None:
        with self.connect(readonly=True) as connection:
            row = connection.execute(
                "SELECT * FROM transitions WHERE experiment_id=? AND to_state=?",
                (experiment_id, to_state.value),
            ).fetchone()
            return dict(row) if row else None

    def reviews_for(self, experiment_id: str) -> list[dict[str, Any]]:
        with self.connect(readonly=True) as connection:
            return [
                dict(row)
                for row in connection.execute(
                    "SELECT * FROM reviews WHERE experiment_id=? ORDER BY role",
                    (experiment_id,),
                )
            ]

    def observation_for(self, experiment_id: str) -> dict[str, Any]:
        with self.connect(readonly=True) as connection:
            row = connection.execute(
                """
                SELECT o.* FROM observations o
                JOIN experiments e ON e.observation_id = o.id
                WHERE e.id = ?
                """,
                (experiment_id,),
            ).fetchone()
            if row is None:
                raise KeyError(experiment_id)
            result = dict(row)
            result["payload"] = json.loads(result.pop("payload_json"))
            return result

    def _reserve(
        self,
        connection: sqlite3.Connection,
        reservation_id: str,
        requests: dict[str, int],
    ) -> None:
        for resource, amount in requests.items():
            counter = connection.execute(
                "SELECT cap, used, reserved FROM budget_counters WHERE resource = ?",
                (resource,),
            ).fetchone()
            if counter is None:
                raise BudgetViolation(f"unknown budget resource: {resource}")
            if (
                amount < 0
                or counter["used"] + counter["reserved"] + amount > counter["cap"]
            ):
                raise BudgetViolation(f"budget exhausted: {resource}")
        for resource, amount in requests.items():
            connection.execute(
                "INSERT INTO budget_reservations VALUES (?, ?, ?, 'reserved')",
                (reservation_id, resource, amount),
            )
            connection.execute(
                "UPDATE budget_counters SET reserved = reserved + ? WHERE resource = ?",
                (amount, resource),
            )

    @staticmethod
    def _database_now(connection: sqlite3.Connection) -> float:
        """Read one transaction-local wall-clock value from SQLite."""

        return float(
            connection.execute(
                "SELECT (julianday('now') - 2440587.5) * 86400.0"
            ).fetchone()[0]
        )

    def claim_transition(
        self,
        experiment_id: str,
        from_state: ExperimentState,
        to_state: ExperimentState,
        worker_id: str,
        config_digest: str,
        lease_seconds: float,
        budget_request: dict[str, int],
        max_attempts: int = 3,
        max_lease_seconds: float | None = None,
    ) -> Lease:
        with self.transaction() as connection:
            now = self._database_now(connection)
            if lease_seconds <= 0:
                raise ValueError("lease_seconds must be positive")
            maximum = lease_seconds if max_lease_seconds is None else max_lease_seconds
            if maximum < lease_seconds or maximum <= 0:
                raise ValueError(
                    "max_lease_seconds must be positive and at least lease_seconds"
                )
            if (
                connection.execute(
                    "SELECT value FROM settings WHERE key='accept_new_work'"
                ).fetchone()[0]
                != "true"
            ):
                raise RuntimeError("controller is paused")
            experiment = connection.execute(
                "SELECT state FROM experiments WHERE id = ?", (experiment_id,)
            ).fetchone()
            if experiment is None or experiment["state"] != from_state.value:
                raise StaleLease("experiment state changed before claim")
            work_id = f"{experiment_id}:{from_state.value}:{to_state.value}:v1"
            connection.execute(
                """
                INSERT OR IGNORE INTO work_items(
                    id, experiment_id, from_state, to_state, status, config_digest
                ) VALUES (?, ?, ?, ?, 'pending', ?)
                """,
                (
                    work_id,
                    experiment_id,
                    from_state.value,
                    to_state.value,
                    config_digest,
                ),
            )
            work = connection.execute(
                "SELECT * FROM work_items WHERE id = ?", (work_id,)
            ).fetchone()
            if work["config_digest"] != config_digest:
                raise RuntimeError("work item policy digest changed")
            if work["status"] == "succeeded":
                raise StaleLease("transition already completed")
            if work["status"] == "running" and work["lease_expires"] > now:
                raise RuntimeError("transition already leased")
            if work["status"] == "running":
                connection.execute(
                    "UPDATE attempts SET status='abandoned', finished_at=? WHERE work_id=? AND status='running'",
                    (utc_now(), work_id),
                )
                self._consume_abandoned_reservations(connection, work_id)
            attempt_count = int(work["attempt_count"]) + 1
            if attempt_count > max_attempts:
                raise BudgetViolation(f"attempt limit reached for {work_id}")
            attempt_sequence = connection.execute(
                "SELECT COUNT(*) + 1 FROM attempts"
            ).fetchone()[0]
            attempt_id = f"MIOS-ATT-{attempt_sequence:04d}"
            reservation_id = f"{work_id}:attempt:{attempt_count}"
            self._reserve(connection, reservation_id, budget_request)
            fencing_token = int(work["fencing_token"]) + 1
            expires_at = now + lease_seconds
            deadline_at = now + maximum
            connection.execute(
                """
                UPDATE work_items SET status='running', attempt_count=?, lease_owner=?,
                    lease_expires=?, lease_deadline=?, fencing_token=? WHERE id=?
                """,
                (
                    attempt_count,
                    worker_id,
                    expires_at,
                    deadline_at,
                    fencing_token,
                    work_id,
                ),
            )
            connection.execute(
                "INSERT INTO attempts VALUES (?, ?, ?, 'running', ?, NULL, NULL, NULL)",
                (attempt_id, work_id, fencing_token, utc_now()),
            )
            return Lease(
                work_id=work_id,
                attempt_id=attempt_id,
                experiment_id=experiment_id,
                from_state=from_state,
                to_state=to_state,
                worker_id=worker_id,
                fencing_token=fencing_token,
                expires_at=expires_at,
                deadline_at=deadline_at,
                reservation_id=reservation_id,
            )

    def _consume_abandoned_reservations(
        self, connection: sqlite3.Connection, work_id: str
    ) -> None:
        rows = connection.execute(
            """
            SELECT br.* FROM budget_reservations br
            WHERE br.reservation_id LIKE ? AND br.status='reserved'
            """,
            (f"{work_id}:attempt:%",),
        ).fetchall()
        for row in rows:
            connection.execute(
                "UPDATE budget_counters SET reserved=reserved-?, used=used+? WHERE resource=?",
                (row["amount"], row["amount"], row["resource"]),
            )
            connection.execute(
                "UPDATE budget_reservations SET status='consumed' WHERE reservation_id=? AND resource=?",
                (row["reservation_id"], row["resource"]),
            )

    def _validate_lease(
        self, connection: sqlite3.Connection, lease: Lease, now: float
    ) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM work_items WHERE id = ?", (lease.work_id,)
        ).fetchone()
        if (
            row is None
            or row["status"] != "running"
            or row["lease_owner"] != lease.worker_id
            or int(row["fencing_token"]) != lease.fencing_token
        ):
            raise StaleLease(f"stale fencing token for {lease.work_id}")
        if row["lease_expires"] is None or float(row["lease_expires"]) <= now:
            raise StaleLease(f"lease expired for {lease.work_id}")
        if row["lease_deadline"] is None or float(row["lease_deadline"]) < float(
            row["lease_expires"]
        ):
            raise StaleLease(f"invalid lease deadline for {lease.work_id}")
        return row

    def heartbeat(self, lease: Lease, extension_seconds: float) -> Lease:
        """Renew a live lease without exceeding its claim-time deadline."""

        if extension_seconds <= 0:
            raise ValueError("extension_seconds must be positive")
        with self.transaction() as connection:
            now = self._database_now(connection)
            row = self._validate_lease(connection, lease, now)
            deadline = float(row["lease_deadline"])
            expires_at = min(now + extension_seconds, deadline)
            if expires_at <= now:
                raise StaleLease(f"lease deadline reached for {lease.work_id}")
            connection.execute(
                "UPDATE work_items SET lease_expires=? WHERE id=?",
                (expires_at, lease.work_id),
            )
            return Lease(
                work_id=lease.work_id,
                attempt_id=lease.attempt_id,
                experiment_id=lease.experiment_id,
                from_state=lease.from_state,
                to_state=lease.to_state,
                worker_id=lease.worker_id,
                fencing_token=lease.fencing_token,
                expires_at=expires_at,
                deadline_at=deadline,
                reservation_id=lease.reservation_id,
            )

    @staticmethod
    def _validate_digest(value: str, name: str) -> None:
        if len(value) != 64 or any(
            character not in "0123456789abcdef" for character in value
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")

    def prepare_effect_intent(
        self,
        lease: Lease,
        effect_kind: str,
        action_implementation_digest: str,
        input_digest: str,
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Durably authorize one effect before its implementation executes."""

        if not effect_kind:
            raise ValueError("effect_kind must not be empty")
        self._validate_digest(
            action_implementation_digest, "action_implementation_digest"
        )
        self._validate_digest(input_digest, "input_digest")
        key = idempotency_key or f"{lease.work_id}:{effect_kind}"
        if not key or len(key) > 512:
            raise ValueError("idempotency_key must contain at most 512 characters")
        identity = {
            "experiment_id": lease.experiment_id,
            "work_id": lease.work_id,
            "effect_kind": effect_kind,
            "action_implementation_digest": action_implementation_digest,
            "input_digest": input_digest,
        }
        with self.transaction() as connection:
            now = self._database_now(connection)
            self._validate_lease(connection, lease, now)
            existing = connection.execute(
                "SELECT * FROM effect_intents WHERE idempotency_key=?", (key,)
            ).fetchone()
            if existing is not None:
                mismatches = [
                    name
                    for name, expected in identity.items()
                    if existing[name] != expected
                ]
                if mismatches:
                    raise IntegrityViolation(
                        "effect intent idempotency key reused with different identity: "
                        + ", ".join(mismatches)
                    )
                if existing["status"] == "prepared":
                    connection.execute(
                        "UPDATE effect_intents SET fencing_token=? WHERE idempotency_key=?",
                        (lease.fencing_token, key),
                    )
                elif existing["status"] != "completed":
                    raise IntegrityViolation(
                        f"unknown effect intent status: {existing['status']}"
                    )
            else:
                connection.execute(
                    """
                    INSERT INTO effect_intents(
                        idempotency_key, experiment_id, work_id, effect_kind,
                        action_implementation_digest, input_digest, status,
                        fencing_token, output_digest, prepared_at, completed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 'prepared', ?, NULL, ?, NULL)
                    """,
                    (
                        key,
                        lease.experiment_id,
                        lease.work_id,
                        effect_kind,
                        action_implementation_digest,
                        input_digest,
                        lease.fencing_token,
                        utc_now(),
                    ),
                )
            row = connection.execute(
                "SELECT * FROM effect_intents WHERE idempotency_key=?", (key,)
            ).fetchone()
            return dict(row)

    def complete_transition(
        self,
        lease: Lease,
        effect_kind: str,
        effect_input_digest: str,
        evidence_digest: str,
        actual_budget: dict[str, int],
        *,
        effect_idempotency_key: str | None = None,
    ) -> None:
        idempotency_key = effect_idempotency_key or f"{lease.work_id}:{effect_kind}"
        self._validate_digest(effect_input_digest, "effect_input_digest")
        self._validate_digest(evidence_digest, "evidence_digest")
        with self.transaction() as connection:
            now = self._database_now(connection)
            self._validate_lease(connection, lease, now)
            intent = connection.execute(
                "SELECT * FROM effect_intents WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if intent is None:
                raise IntegrityViolation(
                    "effect completion requires a prepared durable intent"
                )
            if (
                intent["experiment_id"] != lease.experiment_id
                or intent["work_id"] != lease.work_id
                or intent["effect_kind"] != effect_kind
                or intent["input_digest"] != effect_input_digest
            ):
                raise IntegrityViolation(
                    "effect completion does not match its prepared intent"
                )
            if intent["status"] == "prepared":
                if int(intent["fencing_token"]) != lease.fencing_token:
                    raise StaleLease(
                        f"effect intent has stale fencing token for {lease.work_id}"
                    )
                connection.execute(
                    """
                    UPDATE effect_intents
                    SET status='completed', output_digest=?, completed_at=?
                    WHERE idempotency_key=? AND status='prepared' AND fencing_token=?
                    """,
                    (
                        evidence_digest,
                        utc_now(),
                        idempotency_key,
                        lease.fencing_token,
                    ),
                )
            elif (
                intent["status"] != "completed"
                or intent["output_digest"] != evidence_digest
            ):
                raise IntegrityViolation(
                    "completed effect intent has a different output"
                )
            existing = connection.execute(
                "SELECT * FROM effects WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if existing:
                if (
                    existing["input_digest"] != effect_input_digest
                    or existing["output_digest"] != evidence_digest
                ):
                    raise RuntimeError("idempotency key reused with different content")
            else:
                connection.execute(
                    "INSERT INTO effects VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        idempotency_key,
                        lease.experiment_id,
                        effect_kind,
                        effect_input_digest,
                        evidence_digest,
                        lease.fencing_token,
                        utc_now(),
                    ),
                )
            connection.execute(
                """
                INSERT OR IGNORE INTO transitions(
                    experiment_id, from_state, to_state, evidence_digest, fencing_token, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    lease.experiment_id,
                    lease.from_state.value,
                    lease.to_state.value,
                    evidence_digest,
                    lease.fencing_token,
                    utc_now(),
                ),
            )
            cursor = connection.execute(
                "UPDATE experiments SET state=?, version=version+1, updated_at=? WHERE id=? AND state=?",
                (
                    lease.to_state.value,
                    utc_now(),
                    lease.experiment_id,
                    lease.from_state.value,
                ),
            )
            if cursor.rowcount != 1:
                raise StaleLease("experiment state changed before commit")
            connection.execute(
                "UPDATE work_items SET status='succeeded', lease_owner=NULL, lease_expires=NULL WHERE id=?",
                (lease.work_id,),
            )
            connection.execute(
                "UPDATE attempts SET status='succeeded', finished_at=? WHERE id=?",
                (utc_now(), lease.attempt_id),
            )
            self._finalize_reservation(connection, lease.reservation_id, actual_budget)

    def _finalize_reservation(
        self,
        connection: sqlite3.Connection,
        reservation_id: str,
        actuals: dict[str, int],
    ) -> None:
        rows = connection.execute(
            "SELECT * FROM budget_reservations WHERE reservation_id=? AND status='reserved'",
            (reservation_id,),
        ).fetchall()
        for row in rows:
            actual = int(actuals.get(row["resource"], 0))
            if actual < 0 or actual > row["amount"]:
                raise BudgetViolation(f"actual {row['resource']} exceeds reservation")
            connection.execute(
                "UPDATE budget_counters SET reserved=reserved-?, used=used+? WHERE resource=?",
                (row["amount"], actual, row["resource"]),
            )
            connection.execute(
                "UPDATE budget_reservations SET status='consumed' WHERE reservation_id=? AND resource=?",
                (reservation_id, row["resource"]),
            )

    def fail_attempt(
        self, lease: Lease, error: BaseException, retryable: bool = False
    ) -> None:
        with self.transaction() as connection:
            now = self._database_now(connection)
            self._validate_lease(connection, lease, now)
            status = "pending" if retryable else "failed"
            connection.execute(
                "UPDATE work_items SET status=?, lease_owner=NULL, lease_expires=NULL WHERE id=?",
                (status, lease.work_id),
            )
            connection.execute(
                """
                UPDATE attempts SET status='failed', finished_at=?, error_class=?, error_message=?
                WHERE id=?
                """,
                (utc_now(), type(error).__name__, str(error)[:2048], lease.attempt_id),
            )
            self._consume_abandoned_reservations(connection, lease.work_id)
            if not retryable:
                connection.execute(
                    "UPDATE experiments SET state='PAUSED', terminal_reason=?, updated_at=? WHERE id=?",
                    (
                        f"{type(error).__name__}: {str(error)[:1024]}",
                        utc_now(),
                        lease.experiment_id,
                    ),
                )

    def add_reviews(self, reviews: list[dict[str, Any]]) -> None:
        with self.transaction() as connection:
            for review in reviews:
                row = (
                    review["experiment_id"],
                    review["role"],
                    review["reviewer_identity"],
                    review["candidate_commit"],
                    review["evidence_digest"],
                    review["verdict"],
                    int(review["decisive"]),
                )
                existing = connection.execute(
                    """
                    SELECT experiment_id, role, reviewer_identity, candidate_commit,
                        evidence_digest, verdict, decisive
                    FROM reviews
                    WHERE experiment_id=? AND role=? AND candidate_commit=?
                    """,
                    (row[0], row[1], row[3]),
                ).fetchone()
                if existing is not None:
                    if tuple(existing) != row:
                        raise IntegrityViolation(
                            "review idempotency key was reused with different content"
                        )
                    continue
                connection.execute(
                    "INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?)", row
                )

    def export(self) -> dict[str, Any]:
        table_order = [
            "settings",
            "observations",
            "experiments",
            "work_items",
            "attempts",
            "effect_intents",
            "effects",
            "transitions",
            "reviews",
            "budget_counters",
            "budget_reservations",
            "schema_migrations",
        ]
        with self.connect(readonly=True) as connection:
            result: dict[str, Any] = {}
            for table in table_order:
                rows = [
                    dict(row)
                    for row in connection.execute(
                        f"SELECT * FROM {table} ORDER BY rowid"
                    )
                ]
                for row in rows:
                    for key, value in list(row.items()):
                        if isinstance(value, bytes):
                            row[key] = json.loads(value)
                result[table] = rows
            return result

    def status(self) -> dict[str, Any]:
        exported = self.export()
        settings = {row["key"]: row["value"] for row in exported["settings"]}
        return {
            "controller_state": settings["controller_state"],
            "accept_new_work": settings["accept_new_work"] == "true",
            "last_error": settings["last_error"],
            "experiments": exported["experiments"],
            "budgets": exported["budget_counters"],
        }

    def consume_budget(self, resource: str, amount: int) -> int:
        """Atomically consume a measured controller-level resource."""

        if amount < 0:
            raise ValueError("budget consumption must be nonnegative")
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT cap, used, reserved FROM budget_counters WHERE resource=?",
                (resource,),
            ).fetchone()
            if row is None:
                raise BudgetViolation(f"unknown budget resource: {resource}")
            if int(row["used"]) + int(row["reserved"]) + amount > int(row["cap"]):
                raise BudgetViolation(f"budget exhausted: {resource}")
            connection.execute(
                "UPDATE budget_counters SET used=used+? WHERE resource=?",
                (amount, resource),
            )
            return int(row["cap"]) - int(row["used"]) - int(row["reserved"]) - amount

    def budget_remaining(self, resource: str) -> int:
        with self.connect(readonly=True) as connection:
            row = connection.execute(
                "SELECT cap, used, reserved FROM budget_counters WHERE resource=?",
                (resource,),
            ).fetchone()
            if row is None:
                raise BudgetViolation(f"unknown budget resource: {resource}")
            return int(row["cap"]) - int(row["used"]) - int(row["reserved"])
