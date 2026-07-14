"""Exercise DBOS recovery around every Phase 1A transition/effect boundary."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from tools.evidence_common import source_reference
except ModuleNotFoundError:
    from evidence_common import source_reference


TRANSITIONS = (
    "OBSERVED",
    "TRIAGED",
    "PREREGISTERED",
    "DESIGNED",
    "IMPLEMENTING",
    "EVALUATING",
    "REVIEWING",
)
POINTS = (
    "after_claim_before_effect",
    "after_intent_before_action",
    "after_effect_before_artifact",
    "after_artifact_before_registry",
    "after_registry_before_ledger",
    "after_ledger_before_checkpoint",
)


def run(
    command: list[str], environment: dict[str, str] | None = None, check: bool = True
):
    return subprocess.run(
        command,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
        check=check,
    )


def scenario(
    cli: Path, repository: Path, transition: str, point: str
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="mios-crash-") as temporary:
        root = Path(temporary) / "controller"
        common = ["--root", str(root), "--repository", str(repository)]
        run([str(cli), "init", *common])
        run(
            [
                str(cli),
                "ingest",
                *common,
                str(
                    repository / "evolution" / "fixtures" / "synthetic-observation.json"
                ),
            ]
        )
        run([str(cli), "resume", *common])
        environment = os.environ.copy()
        environment.update(
            {
                "MIOS_ENABLE_CRASH_INJECTION": "1",
                "MIOS_TEST_CRASH_TRANSITION": transition,
                "MIOS_TEST_CRASH_POINT": point,
            }
        )
        crashed = run([str(cli), "run", *common], environment=environment, check=False)
        if crashed.returncode != 77:
            raise RuntimeError(
                f"{transition}/{point} did not reach injected crash: {crashed.returncode}\n{crashed.stderr}"
            )
        recovered = run([str(cli), "run", *common], check=False)
        if recovered.returncode != 0:
            raise RuntimeError(
                f"{transition}/{point} recovery returned {recovered.returncode}\n"
                f"{recovered.stderr}"
            )
        verified = json.loads(run([str(cli), "verify", *common]).stdout)
        summary = json.loads((root / "evidence" / "semantic-summary.json").read_text())
        effect_kinds = [effect["kind"] for effect in summary["effects"]]
        if len(effect_kinds) != 7 or len(set(effect_kinds)) != 7:
            raise RuntimeError(
                f"duplicate or missing effects after {transition}/{point}"
            )
        if verified["artifact_count"] != 9:
            raise RuntimeError(
                f"orphan or missing artifacts after {transition}/{point}"
            )
        return {
            "scenario_id": f"{transition}:{point}",
            "outcome": "passed",
            "terminal_state": summary["terminal_state"],
            "effect_count": len(effect_kinds),
            "ledger_records": verified["ledger_records"],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--cli", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    cases = (
        [("DESIGNED", "after_registry_before_ledger")]
        if arguments.quick
        else [(transition, point) for transition in TRANSITIONS for point in POINTS]
    )
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=arguments.workers) as pool:
        futures = {
            pool.submit(
                scenario,
                arguments.cli.resolve(),
                arguments.repository.resolve(),
                transition,
                point,
            ): (transition, point)
            for transition, point in cases
        }
        for future in as_completed(futures):
            results.append(future.result())
    report = {
        "schema_version": "1.0.0",
        "source": source_reference(arguments.repository.resolve()),
        "scenario_count": len(results),
        "passed": len(results),
        "failed": 0,
        "results": sorted(results, key=lambda item: item["scenario_id"]),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
