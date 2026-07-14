"""Independent deterministic review worker for the Phase 1A fixture."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


EXPECTED_SOURCE = b'def current_value() -> str:\n    return "new"\n'


def digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def read_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"unsafe review input: {path.name}")
    return path.read_bytes()


def main() -> int:
    if len(sys.argv) != 5:
        return 64
    workspace = Path(sys.argv[1]).resolve(strict=True)
    evidence_path = Path(sys.argv[2]).resolve(strict=True)
    task_path = Path(sys.argv[3]).resolve(strict=True)
    result_path = Path(sys.argv[4])
    task = json.loads(read_regular(task_path))
    if task.get("protocol_version") != "1.1.0":
        return 65
    if task.get("capabilities", {}).get("network") is not False:
        return 66
    if task.get("capabilities", {}).get("write_scopes") != []:
        return 67

    source = read_regular(workspace / "src" / "behavior.py")
    acceptance = read_regular(workspace / "tests" / "test_acceptance.py")
    evidence_bytes = read_regular(evidence_path)
    evidence = json.loads(evidence_bytes)
    inputs = {
        item["logical_name"]: item for item in task.get("input_artifacts", [])
    }
    actual_inputs = {
        "behavior_source": source,
        "frozen_acceptance_test": acceptance,
        "candidate_evidence_bundle": evidence_bytes,
    }
    checks = [
        inputs.get(name, {}).get("sha256") == hashlib.sha256(data).hexdigest()
        for name, data in actual_inputs.items()
    ]
    role = task.get("role")
    command_id = task.get("capabilities", {}).get("commands", [None])[0]
    implementation = evidence.get("implementation", {})
    evaluation = evidence.get("evaluation", {})
    candidate_commit = evidence.get("candidate_commit")

    if role == "verification_engineer":
        checks.extend(
            [
                command_id == "fixture_verify_candidate_v1",
                source == EXPECTED_SOURCE,
                b'current_value(), "new"' in acceptance,
                implementation.get("candidate_commit") == candidate_commit,
                evaluation.get("candidate_commit") == candidate_commit,
                evaluation.get("execution", {}).get("passed") is True,
                evaluation.get("checks", [{}])[0].get("test_sha256")
                == hashlib.sha256(acceptance).hexdigest(),
            ]
        )
        statement = (
            "Recomputed the candidate, frozen-test, commit, and passing-evaluation "
            "invariants from read-only evidence."
        )
    elif role == "research_skeptic":
        checks.extend(
            [
                command_id == "fixture_challenge_candidate_v1",
                source == EXPECTED_SOURCE,
                implementation.get("candidate_commit") == candidate_commit,
                implementation.get("changed_paths") == ["src/behavior.py"],
                implementation.get("real_repository_write") is False,
                evaluation.get("protected_evaluation_queries") == 0,
                evaluation.get("checks", [{}])[0].get("test_sha256")
                == hashlib.sha256(acceptance).hexdigest(),
            ]
        )
        statement = (
            "Challenged scope, protected-test integrity, repository isolation, and "
            "evaluation-query use from read-only evidence."
        )
    else:
        return 68

    if os.environ.get("MIOS_REVIEW_FORCE_FAIL") == role:
        checks.append(False)
    succeeded = all(checks)
    cited = [item["sha256"] for item in task["input_artifacts"]]
    result = {
        "protocol_version": "1.1.0",
        "task_id": task["task_id"],
        "experiment_id": task["experiment_id"],
        "attempt_id": task["attempt_id"],
        "nonce": task["nonce"],
        "status": "succeeded" if succeeded else "failed",
        "summary": statement if succeeded else "Independent review invariant failed.",
        "outputs": [],
        "claims": (
            [{"statement": statement, "evidence_artifact_ids": cited}]
            if succeeded
            else []
        ),
        "commands_executed": [
            {
                "command_id": command_id,
                "argv_digest": digest([command_id]),
                "exit_code": 0 if succeeded else 1,
                "duration_ms": 1,
            }
        ],
        "resource_actuals": {
            "wall_ms": 1,
            "cpu_ms": 1,
            "peak_memory_bytes": 1048576,
            "output_bytes": 0,
            "files": 0,
            "processes": 1,
        },
        "policy_events": [],
        "errors": (
            []
            if succeeded
            else [
                {
                    "class": "ReviewInvariantFailure",
                    "message": "one or more deterministic review invariants failed",
                    "artifact_ref": None,
                }
            ]
        ),
        "assumptions": [],
        "unresolved": [],
        "started_at": task["not_before"],
        "finished_at": task["not_before"],
        "worker": {
            "implementation": f"deterministic_{role}_fixture",
            "version": "1.0.0",
        },
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        result_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
    )
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(
            result,
            handle,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
