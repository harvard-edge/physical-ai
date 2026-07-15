"""Command-line interface for the local MiOS controller."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .canonical import atomic_write
from .campaign import run_replay_campaign
from .engine import ControllerPaths, EvolutionEngine, directory_bytes, path_digest
from .registry import Registry
from .sandbox import PINNED_IMAGE
from .supervisor import Supervisor


def repository_default() -> Path:
    return Path(__file__).resolve().parents[2]


def add_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root", type=Path, default=Path(".mios"), help="controller state root"
    )
    parser.add_argument(
        "--repository",
        type=Path,
        default=repository_default(),
        help="PhysicalAI checkout",
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="mios-controller")
    subcommands = result.add_subparsers(dest="command", required=True)
    for name in ("init", "status", "verify", "doctor", "pause", "resume"):
        child = subcommands.add_parser(name)
        add_paths(child)
    ingest = subcommands.add_parser("ingest")
    add_paths(ingest)
    ingest.add_argument("observation", type=Path)
    run = subcommands.add_parser("run")
    add_paths(run)
    run.add_argument("--allow-cooperative-fixture", action="store_true")
    supervise = subcommands.add_parser("supervise")
    add_paths(supervise)
    supervise.add_argument("--max-cycles", type=int, default=20)
    supervise.add_argument("--continuous", action="store_true")
    supervise.add_argument(
        "--resume",
        action="store_true",
        help="explicitly authorize this process to resume",
    )
    supervise.add_argument("--allow-cooperative-fixture", action="store_true")
    replay = subcommands.add_parser("replay-campaign")
    replay.add_argument("--state", type=Path, default=Path(".mios/replay.sqlite"))
    replay.add_argument(
        "--ledger", type=Path, default=Path(".mios/replay-ledger.jsonl")
    )
    replay.add_argument("--head", type=Path, default=Path(".mios/replay-head.json"))
    replay.add_argument("--report", type=Path, default=Path(".mios/replay-report.json"))
    return result


def print_json(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.command == "replay-campaign":
        from .ledger import Ledger

        result = run_replay_campaign(
            arguments.state,
            ledger=Ledger(arguments.ledger, arguments.head),
            report_path=arguments.report,
        )
        print_json(
            {
                "campaign_id": result.campaign_id,
                "handoffs": len(result.handoffs),
                "release_verdict": result.release.verdict,
                "report": str(arguments.report),
            }
        )
        return 0
    if arguments.command == "status":
        paths = ControllerPaths.create(arguments.root)
        status = Registry(paths.registry, create_parent=False).status()
        status["controller_storage_bytes_current"] = directory_bytes(paths.root)
        print_json(status)
        return 0
    if arguments.command == "pause":
        paths = ControllerPaths.create(arguments.root)
        atomic_write(paths.stop_file, b"operator pause\n")
        registry = Registry(paths.registry, create_parent=False)
        registry.pause("operator created persistent kill switch")
        print_json(registry.status())
        return 0
    engine = EvolutionEngine(
        arguments.root,
        arguments.repository,
        allow_cooperative=getattr(arguments, "allow_cooperative_fixture", False),
    )
    if arguments.command == "init":
        print_json(engine.initialize())
        return 0
    if arguments.command == "verify":
        print_json(engine.verify())
        return 0
    engine.initialize()
    if arguments.command == "ingest":
        experiment_id, created = engine.ingest_file(arguments.observation)
        print_json({"experiment_id": experiment_id, "created": created})
    elif arguments.command == "run":
        supervisor = Supervisor(
            engine, allow_cooperative=arguments.allow_cooperative_fixture
        )
        if engine.paths.stop_file.exists():
            raise RuntimeError(
                "persistent kill switch is present; use the dedicated resume command"
            )
        if engine.registry.setting("controller_state") != "RUNNING":
            raise RuntimeError(
                "controller is not authorized; use the dedicated resume command"
            )
        print_json(supervisor.run(max_cycles=1, explicit_resume=True))
    elif arguments.command == "supervise":
        if arguments.continuous and arguments.max_cycles != 20:
            raise SystemExit(
                "--continuous and an explicit --max-cycles are mutually exclusive"
            )
        maximum = None if arguments.continuous else arguments.max_cycles
        supervisor = Supervisor(
            engine, allow_cooperative=arguments.allow_cooperative_fixture
        )
        print_json(supervisor.run(max_cycles=maximum, explicit_resume=arguments.resume))
    elif arguments.command == "resume":
        approval_digest = path_digest(
            engine.repository_root / "evolution" / "approvals" / "PHASE-1A.yml"
        )
        engine.registry.resume(
            engine.policy.digest,
            campaign_id="MIOS-CAMPAIGN-001",
            approval_digest=approval_digest,
        )
        engine.paths.stop_file.unlink(missing_ok=True)
        print_json(engine.registry.status())
    elif arguments.command == "doctor":
        docker = shutil.which("docker")
        image_available = False
        if docker:
            import subprocess

            image_available = (
                subprocess.run(
                    [docker, "image", "inspect", PINNED_IMAGE],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                ).returncode
                == 0
            )
        print_json(
            {
                "policy_digest": engine.policy.digest,
                "registry": "ok",
                "docker": docker,
                "pinned_sandbox_image": PINNED_IMAGE,
                "pinned_sandbox_image_available": image_available,
                "external_authority": {
                    "candidate_worker": {
                        "network": "enforced_none",
                        "credentials": "enforced_stripped",
                        "repository_scope": "enforced_fixture_only",
                    },
                    "trusted_controller": {
                        "model_adapter": "absent",
                        "github_adapter": "absent",
                        "robot_adapter": "absent",
                        "physical_deployment_adapter": "absent",
                        "os_network_confinement": False,
                    },
                },
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
