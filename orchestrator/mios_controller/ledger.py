"""Append-only hash-chained evolution ledger."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import fcntl

from .canonical import atomic_write, canonical_bytes, digest_json, utc_now
from .domain import IntegrityViolation


GENESIS_HASH = "0" * 64


class Ledger:
    def __init__(self, path: Path, trusted_head_path: Path):
        self.path = path
        self.trusted_head_path = trusted_head_path
        self.lock_path = path.with_suffix(path.suffix + ".lock")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.trusted_head_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _lock(self) -> Iterator[None]:
        with self.lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def append(
        self, kind: str, payload: dict[str, Any], actor: str = "mios-controller"
    ) -> dict[str, Any]:
        with self._lock():
            verified = self.verify()
            previous_hash = verified[-1]["record_hash"] if verified else GENESIS_HASH
            record = {
                "sequence": len(verified) + 1,
                "recorded_at": utc_now(),
                "kind": kind,
                "actor": actor,
                "previous_hash": previous_hash,
                "payload_hash": digest_json(payload),
                "payload": payload,
            }
            record["record_hash"] = digest_json(record)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("ab") as handle:
                handle.write(canonical_bytes(record) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            atomic_write(
                self.trusted_head_path,
                canonical_bytes(
                    {
                        "sequence": record["sequence"],
                        "record_hash": record["record_hash"],
                    }
                )
                + b"\n",
                mode=0o600,
            )
            return record

    def append_once(
        self,
        event_id: str,
        kind: str,
        payload: dict[str, Any],
        actor: str = "mios-controller",
    ) -> dict[str, Any]:
        payload_with_id = {"event_id": event_id, **payload}
        with self._lock():
            verified = self.verify()
            matches = [
                record
                for record in verified
                if record["payload"].get("event_id") == event_id
            ]
            if matches:
                if matches[0]["kind"] != kind or matches[0][
                    "payload_hash"
                ] != digest_json(payload_with_id):
                    raise IntegrityViolation(
                        f"ledger event ID reused with different content: {event_id}"
                    )
                return matches[0]
            previous_hash = verified[-1]["record_hash"] if verified else GENESIS_HASH
            record = {
                "sequence": len(verified) + 1,
                "recorded_at": utc_now(),
                "kind": kind,
                "actor": actor,
                "previous_hash": previous_hash,
                "payload_hash": digest_json(payload_with_id),
                "payload": payload_with_id,
            }
            record["record_hash"] = digest_json(record)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("ab") as handle:
                handle.write(canonical_bytes(record) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            atomic_write(
                self.trusted_head_path,
                canonical_bytes(
                    {
                        "sequence": record["sequence"],
                        "record_hash": record["record_hash"],
                    }
                )
                + b"\n",
                mode=0o600,
            )
            return record

    def verify(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        previous_hash = GENESIS_HASH
        if self.path.exists():
            with self.path.open("rb") as handle:
                for expected_sequence, raw_line in enumerate(handle, start=1):
                    try:
                        record = json.loads(raw_line)
                    except (UnicodeDecodeError, json.JSONDecodeError) as error:
                        raise IntegrityViolation(
                            f"ledger line {expected_sequence} is invalid"
                        ) from error
                    claimed_hash = record.pop("record_hash", None)
                    if record.get("sequence") != expected_sequence:
                        raise IntegrityViolation(
                            f"ledger sequence mismatch at {expected_sequence}"
                        )
                    if record.get("previous_hash") != previous_hash:
                        raise IntegrityViolation(
                            f"ledger link mismatch at {expected_sequence}"
                        )
                    if record.get("payload_hash") != digest_json(record.get("payload")):
                        raise IntegrityViolation(
                            f"ledger payload mismatch at {expected_sequence}"
                        )
                    actual_hash = digest_json(record)
                    if claimed_hash != actual_hash:
                        raise IntegrityViolation(
                            f"ledger hash mismatch at {expected_sequence}"
                        )
                    record["record_hash"] = claimed_hash
                    records.append(record)
                    previous_hash = claimed_hash

        if self.trusted_head_path.exists():
            try:
                head = json.loads(self.trusted_head_path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise IntegrityViolation("trusted ledger head is invalid") from error
            expected = (
                {
                    "sequence": records[-1]["sequence"],
                    "record_hash": records[-1]["record_hash"],
                }
                if records
                else {"sequence": 0, "record_hash": GENESIS_HASH}
            )
            if head != expected:
                raise IntegrityViolation("ledger does not match trusted head")
        elif records:
            raise IntegrityViolation("trusted ledger head is missing")
        return records
