"""Trusted deterministic Phase 1A worker executed inside the sandbox."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path


EXPECTED = 'def current_value() -> str:\n    return "old"\n'
REPLACEMENT = 'def current_value() -> str:\n    return "new"\n'


def digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    if len(sys.argv) != 4:
        return 64
    root = Path(sys.argv[1]).resolve(strict=True)
    task_path = Path(sys.argv[2]).resolve(strict=True)
    result_path = Path(sys.argv[3])
    task = json.loads(task_path.read_text(encoding="utf-8"))
    if task.get("protocol_version") != "1.1.0":
        return 67
    capabilities = task.get("capabilities", {})
    if capabilities.get("network") is not False:
        return 68
    if capabilities.get("write_scopes") != ["src/behavior.py"]:
        return 69
    candidate = root / "src" / "behavior.py"
    if (
        candidate.is_symlink()
        or not candidate.is_file()
        or root not in candidate.resolve().parents
    ):
        return 65
    if candidate.read_text(encoding="utf-8") != EXPECTED:
        return 66
    before = candidate.read_bytes()
    expected_input = task["input_artifacts"][0]
    if expected_input["sha256"] != hashlib.sha256(before).hexdigest():
        return 70
    delay = os.environ.get("MIOS_WORKER_DELAY_SECONDS")
    if delay is not None:
        time.sleep(float(delay))
    descriptor = os.open(candidate, os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(REPLACEMENT)
        handle.flush()
        os.fsync(handle.fileno())
    output = candidate.read_bytes()
    output_digest = hashlib.sha256(output).hexdigest()
    result = {
        "protocol_version": "1.1.0",
        "task_id": task["task_id"],
        "experiment_id": task["experiment_id"],
        "attempt_id": task["attempt_id"],
        "nonce": task["nonce"],
        "status": "succeeded",
        "summary": "Updated the single authorized synthetic behavior source.",
        "outputs": [
            {
                "logical_name": "behavior_source",
                "relative_path": "src/behavior.py",
                "sha256": output_digest,
                "size": len(output),
                "media_type": "text/x-python",
            }
        ],
        "claims": [
            {
                "statement": "The authorized behavior source now returns the preregistered expected value.",
                "evidence_artifact_ids": [output_digest],
            }
        ],
        "commands_executed": [
            {
                "command_id": "fixture_replace_value_v1",
                "argv_digest": digest(["fixture_replace_value_v1"]),
                "exit_code": 0,
                "duration_ms": 0,
            }
        ],
        "resource_actuals": {
            "wall_ms": 0,
            "cpu_ms": 0,
            "peak_memory_bytes": 0,
            "output_bytes": len(output),
            "files": 1,
            "processes": 1,
        },
        "policy_events": [],
        "errors": [],
        "assumptions": [],
        "unresolved": [],
        "started_at": task["not_before"],
        "finished_at": task["not_before"],
        "worker": {"implementation": "deterministic_fixture", "version": "1.0.0"},
    }
    result_mode = os.environ.get("MIOS_WORKER_RESULT_MODE")
    if result_mode == "secret":
        result["summary"] = "SECRET_CANARY"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_descriptor = os.open(
        result_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
    )
    with os.fdopen(result_descriptor, "w", encoding="utf-8") as handle:
        if result_mode == "malformed":
            handle.write('{"protocol_version"')
        elif result_mode == "oversized":
            handle.write("x" * 70_000)
        else:
            json.dump(
                result,
                handle,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
