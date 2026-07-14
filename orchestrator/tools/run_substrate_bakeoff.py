"""Generate normalized Phase 1A workflow-substrate evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

try:
    from tools.evidence_common import source_reference
except ModuleNotFoundError:
    from evidence_common import source_reference


RUNNER_VERSION = "1.0.0"
SCENARIO_VERSION = "phase1a-durable-cycle-v1"
EFFECTS = [
    "local_issue_manifest",
    "local_preregistration",
    "local_design",
    "local_candidate_commit",
    "local_fixture_evaluation",
    "local_review_attestations",
    "local_pull_request_manifest",
]


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def command(argv: list[str], *, env: dict[str, str] | None = None, check=True):
    return subprocess.run(
        argv,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=90,
        check=check,
    )


def normalized(effects: list[str], terminal: str) -> dict[str, object]:
    return {
        "scenario_version": SCENARIO_VERSION,
        "effects": effects,
        "effect_count": len(effects),
        "duplicates": len(effects) - len(set(effects)),
        "terminal_state": terminal,
    }


def dbos_case(repository: Path, cli: Path) -> dict[str, object]:
    started = time.monotonic_ns()
    with tempfile.TemporaryDirectory(prefix="mios-bakeoff-dbos-") as temporary:
        root = Path(temporary) / "controller"
        common = ["--root", str(root), "--repository", str(repository)]
        observation = repository / "evolution/fixtures/synthetic-observation.json"
        command([str(cli), "init", *common])
        command([str(cli), "ingest", *common, str(observation)])
        command([str(cli), "resume", *common])
        crash_env = os.environ.copy()
        crash_env.update(
            MIOS_ENABLE_CRASH_INJECTION="1",
            MIOS_TEST_CRASH_TRANSITION="DESIGNED",
            MIOS_TEST_CRASH_POINT="after_registry_before_ledger",
        )
        crash_at = time.monotonic_ns()
        crashed = command([str(cli), "run", *common], env=crash_env, check=False)
        if crashed.returncode != 77:
            raise RuntimeError(
                f"DBOS crash injection returned {crashed.returncode}: {crashed.stderr}"
            )
        command([str(cli), "run", *common])
        recovered_at = time.monotonic_ns()
        verification = command([str(cli), "verify", *common], check=False)
        if verification.returncode != 0:
            raise RuntimeError(
                f"DBOS verification returned {verification.returncode}: {verification.stderr}"
            )
        verified = json.loads(verification.stdout)
        summary = json.loads((root / "evidence/semantic-summary.json").read_text())
        effects = [item["kind"] for item in summary["effects"]]

        cancel_root = Path(temporary) / "cancel-controller"
        cancel_common = ["--root", str(cancel_root), "--repository", str(repository)]
        command([str(cli), "init", *cancel_common])
        command([str(cli), "ingest", *cancel_common, str(observation)])
        command([str(cli), "resume", *cancel_common])
        command([str(cli), "pause", *cancel_common])
        denied = command([str(cli), "run", *cancel_common], check=False)
        stop_preserved = (cancel_root / "STOP").is_file()
        semantic = normalized(effects, summary["terminal_state"])
        return {
            "substrate": "dbos",
            "substrate_version": importlib.metadata.version("dbos"),
            "runner_version": RUNNER_VERSION,
            "status": "passed",
            "tool_versions": {
                "python": sys.version.split()[0],
                "dbos": importlib.metadata.version("dbos"),
                "mios_controller": importlib.metadata.version("mios-controller"),
            },
            "criterion": "same seven-effect cycle; crash after registry commit before ledger; persistent pause before next effect",
            "timings_ms": {
                "total": (time.monotonic_ns() - started) // 1_000_000,
                "crash_to_recovery": (recovered_at - crash_at) // 1_000_000,
            },
            "effects": effects,
            "duplicates": semantic["duplicates"],
            "terminal_state": summary["terminal_state"],
            "semantic_digest": canonical_digest(semantic),
            "raw": {
                "crash_returncode": crashed.returncode,
                "artifact_count": verified["artifact_count"],
                "ledger_records": verified["ledger_records"],
                "pause_run_returncode": denied.returncode,
                "stop_preserved": stop_preserved,
            },
            "limitations": [
                "Cancellation case is persistent pause before the next effect, not an active-work latency measurement."
            ],
        }


def custom_worker(database: Path, crash_marker: Path, allow_run: bool) -> int:
    with sqlite3.connect(database) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS effects(seq INTEGER PRIMARY KEY, kind TEXT UNIQUE)"
        )
        db.execute("CREATE TABLE IF NOT EXISTS state(key TEXT PRIMARY KEY,value TEXT)")
        db.execute("INSERT OR IGNORE INTO state VALUES('controller','RUNNING')")
        if (
            not allow_run
            or db.execute("SELECT value FROM state WHERE key='controller'").fetchone()[
                0
            ]
            != "RUNNING"
        ):
            return 73
        existing = {row[0] for row in db.execute("SELECT kind FROM effects")}
        for sequence, effect in enumerate(EFFECTS, 1):
            if effect in existing:
                continue
            db.execute("INSERT INTO effects VALUES(?,?)", (sequence, effect))
            db.commit()
            if effect == "local_candidate_commit" and not crash_marker.exists():
                crash_marker.write_text("crashed\n")
                os._exit(77)
        db.execute(
            "UPDATE state SET value='LOCAL_CANDIDATE_READY' WHERE key='controller'"
        )
        db.commit()
    return 0


def custom_case(script: Path) -> dict[str, object]:
    started = time.monotonic_ns()
    with tempfile.TemporaryDirectory(prefix="mios-bakeoff-custom-") as temporary:
        root = Path(temporary)
        database, marker = root / "control.sqlite3", root / "crash.marker"
        crash_at = time.monotonic_ns()
        crashed = command(
            [
                sys.executable,
                str(script),
                "--custom-worker",
                str(database),
                str(marker),
            ],
            check=False,
        )
        if crashed.returncode != 77:
            raise RuntimeError(f"custom crash injection returned {crashed.returncode}")
        recovered = command(
            [
                sys.executable,
                str(script),
                "--custom-worker",
                str(database),
                str(marker),
            ],
            check=False,
        )
        recovered_at = time.monotonic_ns()
        if recovered.returncode != 0:
            raise RuntimeError(f"custom recovery returned {recovered.returncode}")
        with sqlite3.connect(database) as db:
            effects = [
                row[0] for row in db.execute("SELECT kind FROM effects ORDER BY seq")
            ]
            terminal = db.execute(
                "SELECT value FROM state WHERE key='controller'"
            ).fetchone()[0]
            db.execute("UPDATE state SET value='PAUSED' WHERE key='controller'")
            db.commit()
        denied = command(
            [
                sys.executable,
                str(script),
                "--custom-worker",
                str(database),
                str(marker),
            ],
            check=False,
        )
        semantic = normalized(effects, terminal)
        return {
            "substrate": "custom_durable_control",
            "substrate_version": "sqlite-" + sqlite3.sqlite_version,
            "runner_version": RUNNER_VERSION,
            "status": "passed",
            "tool_versions": {
                "python": sys.version.split()[0],
                "sqlite": sqlite3.sqlite_version,
            },
            "criterion": "same seven-effect cycle; crash after durable candidate effect; persistent pause before next effect",
            "timings_ms": {
                "total": (time.monotonic_ns() - started) // 1_000_000,
                "crash_to_recovery": (recovered_at - crash_at) // 1_000_000,
            },
            "effects": effects,
            "duplicates": semantic["duplicates"],
            "terminal_state": terminal,
            "semantic_digest": canonical_digest(semantic),
            "raw": {
                "crash_returncode": crashed.returncode,
                "recovery_returncode": recovered.returncode,
                "pause_run_returncode": denied.returncode,
                "effect_rows": len(effects),
            },
            "limitations": [
                "Custom control is a minimal SQLite comparison fixture, not the MiOS controller implementation.",
                "Cancellation case is persistent pause before the next effect, not an active-work latency measurement.",
            ],
        }


def temporal_case() -> dict[str, object]:
    executable = shutil.which("temporal")
    criterion = "Temporal is runnable only with a local Temporal CLI and an explicitly provisioned local development service; remote/cloud service use is forbidden in Phase 1A."
    error = (
        "temporal CLI not found"
        if executable is None
        else "local Temporal development service was not explicitly provisioned for this bakeoff"
    )
    return {
        "substrate": "temporal",
        "substrate_version": None,
        "runner_version": RUNNER_VERSION,
        "status": "not_runnable",
        "tool_versions": {
            "python": sys.version.split()[0],
            "temporal_cli": "unavailable"
            if executable is None
            else "present-version-not-queried",
        },
        "criterion": criterion,
        "timings_ms": {},
        "effects": [],
        "duplicates": 0,
        "terminal_state": None,
        "semantic_digest": None,
        "raw": {"cli_path": executable, "captured_error": error},
        "limitations": [
            "No Temporal performance, recovery, or cancellation claim is made."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--cli", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--custom-worker", nargs=2, metavar=("DATABASE", "MARKER"))
    args = parser.parse_args()
    if args.custom_worker:
        return custom_worker(
            Path(args.custom_worker[0]), Path(args.custom_worker[1]), True
        )
    if not args.repository or not args.cli or not args.output:
        parser.error("--repository, --cli, and --output are required")
    report = {
        "schema_version": "1.0.0",
        "source": source_reference(args.repository.resolve()),
        "scenario_version": SCENARIO_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": [
            dbos_case(args.repository.resolve(), args.cli.resolve()),
            custom_case(Path(__file__).resolve()),
            temporal_case(),
        ],
    }
    schema = json.loads(
        (Path(__file__).with_name("substrate-bakeoff.schema.json")).read_text()
    )
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
