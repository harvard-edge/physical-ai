"""Run and record the complete host-side Phase 1A validation suite."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

try:
    from tools.evidence_common import canonical, source_reference
except ModuleNotFoundError:
    from evidence_common import canonical, source_reference


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def run(
    argv: list[str], cwd: Path, environment: dict[str, str] | None = None
) -> dict[str, object]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=300,
        check=False,
    )
    output = result.stdout.strip()
    summary = output.splitlines()[-1] if output else ""
    matched = re.search(r"(\d+) passed", summary)
    return {
        "argv": argv,
        "exit_code": result.returncode,
        "passed": int(matched.group(1)) if matched else None,
        "summary": summary,
        "stdout_sha256": digest(result.stdout),
        "stderr_sha256": digest(result.stderr),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository = args.repository.resolve()
    orchestrator = repository / "orchestrator"
    pytest = orchestrator / ".venv/bin/pytest"
    ruff = orchestrator / ".venv/bin/ruff"
    reachy_python = shutil.which("python3")
    if reachy_python is None:
        raise RuntimeError("python3 is required for the Reachy regression suite")

    source = source_reference(repository)
    controller = run(
        [str(pytest), "-o", "addopts=", "-q"],
        orchestrator,
    )
    reachy_environment = os.environ.copy()
    reachy_environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": "code"})
    reachy = run(
        [reachy_python, "-m", "pytest", "-q", "code/tests"],
        repository,
        reachy_environment,
    )
    static = [
        run([str(ruff), "format", "--check", "."], orchestrator),
        run([str(ruff), "check", "."], orchestrator),
        run(["uv", "lock", "--check"], orchestrator),
        run(["git", "diff", "--check"], repository),
    ]
    source_after = source_reference(repository)
    status = (
        "passed"
        if controller["exit_code"] == 0
        and reachy["exit_code"] == 0
        and all(item["exit_code"] == 0 for item in static)
        and source == source_after
        else "failed"
    )
    evidence = {
        "schema_version": "1.0.0",
        "evidence_kind": "phase1a_host_validation",
        "source": source,
        "status": status,
        "controller_tests": controller,
        "reachy_regression_tests": reachy,
        "static_checks": static,
        "scope": "macOS ARM64 host and pinned Linux ARM64 worker containers",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical(evidence) + b"\n")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
