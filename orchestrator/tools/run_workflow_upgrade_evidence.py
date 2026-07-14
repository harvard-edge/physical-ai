"""Record compatible DBOS upgrade evidence from fixture and production tests."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

try:
    from tools.evidence_common import canonical, source_reference
except ModuleNotFoundError:
    from evidence_common import canonical, source_reference


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository = args.repository.resolve()
    orchestrator = repository / "orchestrator"
    argv = [
        str(orchestrator / ".venv/bin/pytest"),
        "-o",
        "addopts=",
        "-q",
        "tests/test_dbos_upgrade.py",
    ]
    result = subprocess.run(
        argv,
        cwd=orchestrator,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
        check=False,
    )
    evidence = {
        "schema_version": "1.0.0",
        "evidence_kind": "phase1a_workflow_upgrade",
        "source": source_reference(repository),
        "status": "passed" if result.returncode == 0 else "failed",
        "workflow_substrate": "dbos-2.26.0",
        "compatible_upgrade_policy": "named_dbos_patch_site",
        "incompatible_upgrade_policy": "full_drain_required",
        "scenarios": [
            {
                "id": "isolated_patch_fixture",
                "claim": "A V2 worker resumes interrupted V1 history without replaying completed effects and applies the patch only to fresh V2 history.",
                "test": "test_compatible_v2_worker_resumes_v1_without_replaying_completed_effects",
            },
            {
                "id": "production_evolution_cycle",
                "claim": "The production workflow resumes interrupted pre-patch history and runs fresh patched history without duplicate domain effects.",
                "test": "test_real_evolution_cycle_recovers_v1_history_and_runs_new_v2",
            },
        ],
        "command": {
            "argv": argv,
            "exit_code": result.returncode,
            "stdout_sha256": digest(result.stdout),
            "stderr_sha256": digest(result.stderr),
            "summary": result.stdout.strip().splitlines()[-1]
            if result.stdout.strip()
            else "",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical(evidence) + b"\n")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
