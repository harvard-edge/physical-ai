"""Collect reproducible Phase 1A supply-chain, platform, and resource evidence.

The collector never upgrades dependencies or pulls images. It uses the frozen
uv lock, the already-pinned local sandbox image, and temporary controller roots.
Target resolution and target execution are deliberately reported separately.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import yaml

from mios_controller.supply_chain import evaluate_dependency_licenses

try:
    from tools.evidence_common import source_reference
except ModuleNotFoundError:
    from evidence_common import source_reference


IMAGE = (
    "cgr.dev/chainguard/python@sha256:"
    "ce9aaca1f826f7f963cd031e98f8c19f993b1843096d395ea919b646e72cb8de"
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(
    argv: list[str], *, cwd: Path, timeout: float = 120, check: bool = False
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=check,
    )


def command_record(argv: list[str], result: subprocess.CompletedProcess[str]) -> dict:
    return {
        "argv": argv,
        "exit_code": result.returncode,
        "stdout_sha256": sha256(result.stdout.encode()),
        "stderr_sha256": sha256(result.stderr.encode()),
    }


def tree_bytes(path: Path) -> int:
    return sum(
        item.stat().st_size
        for item in path.rglob("*")
        if item.is_file() and not item.is_symlink()
    )


def measured_process(argv: list[str], cwd: Path) -> dict[str, Any]:
    started = time.monotonic_ns()
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    peak_rss_bytes = 0
    samples = 0
    while process.poll() is None:
        measured = run(["ps", "-o", "rss=", "-p", str(process.pid)], cwd=cwd)
        try:
            peak_rss_bytes = max(peak_rss_bytes, int(measured.stdout.strip()) * 1024)
            samples += 1
        except ValueError:
            pass
        time.sleep(0.005)
    stdout, stderr = process.communicate()
    return {
        "argv": argv,
        "exit_code": process.returncode,
        "wall_ns": time.monotonic_ns() - started,
        "peak_rss_bytes": peak_rss_bytes,
        "rss_samples": samples,
        "stdout_sha256": sha256(stdout.encode()),
        "stderr_sha256": sha256(stderr.encode()),
    }


def collect_dependencies(root: Path, output: Path) -> None:
    lock = root / "uv.lock"
    with tempfile.TemporaryDirectory(prefix="mios-dependencies-") as temporary_name:
        temporary = Path(temporary_name)
        requirements = temporary / "requirements.txt"
        sbom_path = temporary / "dependencies.cdx.json"
        export_requirements_argv = [
            "uv",
            "export",
            "--frozen",
            "--format",
            "requirements.txt",
            "--no-emit-project",
            "--no-annotate",
            "--output-file",
            str(requirements),
        ]
        exported = run(export_requirements_argv, cwd=root)
        export_sbom_argv = [
            "uv",
            "export",
            "--frozen",
            "--format",
            "cyclonedx1.5",
            "--no-emit-project",
            "--output-file",
            str(sbom_path),
        ]
        sbom_export = run(export_sbom_argv, cwd=root)
        resolution: dict[str, Any]
        if exported.returncode == 0:
            resolve_argv = [
                "uv",
                "pip",
                "install",
                "--dry-run",
                "--python-platform",
                "aarch64-unknown-linux-gnu",
                "--python-version",
                "3.12",
                "--only-binary",
                ":all:",
                "--require-hashes",
                "--requirements",
                str(requirements),
            ]
            resolved = run(resolve_argv, cwd=root)
            minimum_argv = [
                "uv",
                "pip",
                "install",
                "--dry-run",
                "--python-platform",
                "aarch64-unknown-linux-gnu",
                "--python-version",
                "3.11",
                "--only-binary",
                ":all:",
                "--require-hashes",
                "--requirements",
                str(requirements),
            ]
            minimum = run(minimum_argv, cwd=root)
            resolution = {
                "status": "passed" if resolved.returncode == 0 else "failed",
                "target": {
                    "os": "linux",
                    "architecture": "arm64",
                    "python": "3.12",
                },
                "command": command_record(resolve_argv, resolved),
                "declared_minimum_python": {
                    "python": "3.11",
                    "status": "passed" if minimum.returncode == 0 else "failed",
                    "reason": (
                        None
                        if minimum.returncode == 0
                        else "The frozen dependencies do not resolve for the declared Python 3.11 minimum."
                    ),
                    "command": command_record(minimum_argv, minimum),
                },
                "runtime_execution": {
                    "status": "not_runnable",
                    "reason": "No native Linux ARM64 host was available to this collector.",
                },
            }
        else:
            resolution = {
                "status": "failed",
                "reason": "Frozen requirements export failed.",
                "command": command_record(export_requirements_argv, exported),
                "runtime_execution": {"status": "not_runnable"},
            }

        sbom = json.loads(sbom_path.read_text()) if sbom_export.returncode == 0 else {}
        components = [
            {
                "name": item["name"],
                "version": item.get("version"),
                "purl": item.get("purl"),
            }
            for item in sbom.get("components", [])
        ]
        locked_names = {
            item["name"].casefold().replace("_", "-") for item in components
        }
        installed = []
        for distribution in importlib.metadata.distributions():
            name = distribution.metadata.get("Name")
            if not name or name.casefold().replace("_", "-") not in locked_names:
                continue
            expression = distribution.metadata.get("License-Expression")
            declared = distribution.metadata.get("License")
            classifiers = sorted(
                value.removeprefix("License :: ")
                for value in distribution.metadata.get_all("Classifier", [])
                if value.startswith("License :: ")
            )
            installed.append(
                {
                    "name": name,
                    "version": distribution.version,
                    "license_expression": expression,
                    "license_declared": declared,
                    "license_classifiers": classifiers,
                }
            )
        installed.sort(key=lambda item: item["name"].casefold())
        license_complete = all(
            item["license_expression"]
            or item["license_declared"]
            or item["license_classifiers"]
            for item in installed
        )
        policy_path = root.parent / "governance" / "dependency-policy.yml"
        policy_raw = policy_path.read_bytes()
        dependency_policy = yaml.safe_load(policy_raw)
        policy_result = evaluate_dependency_licenses(installed, dependency_policy)
        policy_result.update(
            {
                "policy_path": "governance/dependency-policy.yml",
                "policy_sha256": sha256(policy_raw),
                "policy_version": str(dependency_policy["version"]),
            }
        )
        uv_version = run(["uv", "--version"], cwd=root)
        evidence = {
            "schema_version": "1.0.0",
            "evidence_kind": "phase1a_dependency_supply_chain",
            "source": source_reference(root.parent),
            "status": (
                "passed"
                if exported.returncode == 0
                and sbom_export.returncode == 0
                and resolution["status"] == "passed"
                and policy_result["status"] == "passed"
                else "failed"
            ),
            "deployment_readiness": {
                "status": "blocked",
                "reason": "Native Linux ARM64 controller execution has not run.",
            },
            "lock": {
                "path": "orchestrator/uv.lock",
                "sha256": sha256(lock.read_bytes()),
            },
            "tools": {"uv": uv_version.stdout.strip()},
            "exports": {
                "requirements": command_record(export_requirements_argv, exported),
                "cyclonedx": command_record(export_sbom_argv, sbom_export),
            },
            "linux_arm64_resolution": resolution,
            "sbom": {
                "format": "CycloneDX 1.5",
                "component_count": len(components),
                "components": sorted(components, key=lambda item: item["name"]),
            },
            "licenses": {
                "installed_distribution_count": len(installed),
                "inventory": installed,
                "metadata_complete": license_complete,
                "policy_result": policy_result,
            },
        }
    output.write_bytes(canonical(evidence) + b"\n")


def collect_image(root: Path, output: Path) -> None:
    inspect_argv = ["docker", "image", "inspect", IMAGE]
    inspected = run(inspect_argv, cwd=root)
    docker_version = run(["docker", "version", "--format", "{{json .}}"], cwd=root)
    scout_version = run(["docker", "scout", "version"], cwd=root)
    if inspected.returncode != 0:
        evidence = {
            "schema_version": "1.0.0",
            "evidence_kind": "phase1a_pinned_sandbox_image",
            "source": source_reference(root.parent),
            "status": "not_runnable",
            "reason": "Pinned image was not present in the local image store.",
            "command": command_record(inspect_argv, inspected),
        }
        output.write_bytes(canonical(evidence) + b"\n")
        return

    image = json.loads(inspected.stdout)[0]
    runtime_argv = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        IMAGE,
        "-c",
        (
            "import json,os,platform;"
            "print(json.dumps({'uid':os.getuid(),'gid':os.getgid(),"
            "'machine':platform.machine(),'system':platform.system(),"
            "'python':platform.python_version()},sort_keys=True))"
        ),
    ]
    runtime = run(runtime_argv, cwd=root)
    scout_cves_argv = [
        "docker",
        "scout",
        "cves",
        "--format",
        "sarif",
        f"local://{IMAGE}",
    ]
    cves = run(scout_cves_argv, cwd=root)
    scout_sbom_argv = [
        "docker",
        "scout",
        "sbom",
        "--format",
        "spdx",
        f"local://{IMAGE}",
    ]
    image_sbom = run(scout_sbom_argv, cwd=root)
    sarif = json.loads(cves.stdout) if cves.returncode == 0 else {}
    spdx = json.loads(image_sbom.stdout) if image_sbom.returncode == 0 else {}
    vulnerabilities = sum(
        len(item.get("results", [])) for item in sarif.get("runs", [])
    )
    packages = sorted(
        {
            (item.get("name"), item.get("versionInfo"))
            for item in spdx.get("packages", [])
            if item.get("name")
        }
    )
    evidence = {
        "schema_version": "1.0.0",
        "evidence_kind": "phase1a_pinned_sandbox_image",
        "source": source_reference(root.parent),
        "status": "passed",
        "reference": IMAGE,
        "inspect": {
            "id": image["Id"],
            "repo_digests": sorted(image.get("RepoDigests", [])),
            "os": image["Os"],
            "architecture": image["Architecture"],
            "configured_user": image["Config"].get("User"),
            "compressed_size_bytes": image.get("Size"),
            "layer_digests": image.get("RootFS", {}).get("Layers", []),
        },
        "runtime": {
            "status": "passed" if runtime.returncode == 0 else "failed",
            "observed": json.loads(runtime.stdout) if runtime.returncode == 0 else None,
            "command": command_record(runtime_argv, runtime),
        },
        "vulnerabilities": {
            "status": "passed" if cves.returncode == 0 else "not_runnable",
            "finding_count": vulnerabilities if cves.returncode == 0 else None,
            "scanner_note": "A zero count is scoped to the cached Scout advisory data at collection time.",
            "command": command_record(scout_cves_argv, cves),
        },
        "sbom": {
            "status": "passed" if image_sbom.returncode == 0 else "not_runnable",
            "format": "SPDX",
            "package_count": len(packages),
            "packages": [
                {"name": name, "version": version} for name, version in packages
            ],
            "raw_sha256": sha256(image_sbom.stdout.encode()),
            "command": command_record(scout_sbom_argv, image_sbom),
        },
        "tools": {
            "docker": json.loads(docker_version.stdout)
            if docker_version.returncode == 0
            else None,
            "scout": scout_version.stdout.strip(),
        },
    }
    output.write_bytes(canonical(evidence) + b"\n")


def collect_resources(root: Path, output: Path) -> None:
    cli = root / ".venv" / "bin" / "mios-controller"
    repository = root.parent
    observation = repository / "evolution" / "fixtures" / "synthetic-observation.json"
    with tempfile.TemporaryDirectory(prefix="mios-resources-") as temporary_name:
        temporary = Path(temporary_name)
        cold_root = temporary / "cold"
        cold = measured_process(
            [
                str(cli),
                "init",
                "--root",
                str(cold_root),
                "--repository",
                str(repository),
            ],
            root,
        )

        cycle_root = temporary / "cycle"

        def invoke(command: str, *args: str) -> subprocess.CompletedProcess[str]:
            return run(
                [
                    str(cli),
                    command,
                    "--root",
                    str(cycle_root),
                    "--repository",
                    str(repository),
                    *args,
                ],
                cwd=root,
            )

        init = invoke("init")
        ingest = invoke("ingest", str(observation))
        resume = invoke("resume")
        cycle_argv = [
            str(cli),
            "run",
            "--root",
            str(cycle_root),
            "--repository",
            str(repository),
        ]
        cycle = measured_process(cycle_argv, root)

        idle_root = temporary / "idle"
        run(
            [
                str(cli),
                "init",
                "--root",
                str(idle_root),
                "--repository",
                str(repository),
            ],
            cwd=root,
        )
        idle_resume = run(
            [
                str(cli),
                "resume",
                "--root",
                str(idle_root),
                "--repository",
                str(repository),
            ],
            cwd=root,
        )
        idle_argv = [
            str(cli),
            "supervise",
            "--root",
            str(idle_root),
            "--repository",
            str(repository),
            "--continuous",
            "--resume",
        ]
        idle_process = subprocess.Popen(
            idle_argv,
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        time.sleep(1.0)
        idle_running_at_sample = idle_process.poll() is None
        idle_ps = run(["ps", "-o", "rss=", "-p", str(idle_process.pid)], cwd=root)
        idle_rss = (
            int(idle_ps.stdout.strip()) * 1024 if idle_ps.stdout.strip() else None
        )
        idle_process.terminate()
        idle_process.communicate(timeout=15)

        controller_root_bytes = tree_bytes(cycle_root)
        artifact_bytes = tree_bytes(cycle_root / "artifacts")
        database_bytes = sum(
            path.stat().st_size
            for path in cycle_root.rglob("*.sqlite3")
            if path.is_file()
        )
        package_source_bytes = tree_bytes(root / "mios_controller")
        environment_bytes = tree_bytes(root / ".venv")
        storage_limit = 2048 * 1024 * 1024
        wall_limit_ns = 40 * 60 * 60 * 1_000_000_000
        evidence = {
            "schema_version": "1.0.0",
            "evidence_kind": "phase1a_resource_profile",
            "source": source_reference(root.parent),
            "status": (
                "passed"
                if cold["exit_code"] == 0
                and init.returncode == 0
                and ingest.returncode == 0
                and resume.returncode == 0
                and cycle["exit_code"] == 0
                and idle_resume.returncode == 0
                and idle_running_at_sample
                and idle_process.returncode == 0
                else "failed"
            ),
            "tools": {
                "mios_controller": importlib.metadata.version("mios-controller"),
                "python": platform.python_version(),
                "rss_sampler": "POSIX ps",
            },
            "host": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python": platform.python_version(),
            },
            "sampling": {
                "rss_source": "ps -o rss= sampled every 5 ms; values normalized from KiB to bytes",
                "scope": "controller CLI process only, not Docker daemon or container cgroup",
            },
            "cold_init": cold,
            "idle": {
                "argv": idle_argv,
                "resume_exit_code": idle_resume.returncode,
                "sample_after_ms": 1000,
                "running_at_sample": idle_running_at_sample,
                "rss_bytes": idle_rss,
                "exit_code_after_sigterm": idle_process.returncode,
            },
            "synthetic_cycle": {
                "preconditions": {
                    "init": init.returncode,
                    "ingest": ingest.returncode,
                    "resume": resume.returncode,
                },
                "process": cycle,
                "controller_root_bytes": controller_root_bytes,
                "artifact_store_bytes": artifact_bytes,
                "sqlite_bytes": database_bytes,
            },
            "installed_sizes": {
                "controller_source_bytes": package_source_bytes,
                "locked_environment_bytes": environment_bytes,
            },
            "thresholds": {
                "phase1a_storage_bytes": storage_limit,
                "phase1a_wall_ns": wall_limit_ns,
                "controller_root_within_storage_budget": controller_root_bytes
                <= storage_limit
                and cycle["exit_code"] == 0,
                "single_cycle_within_wall_budget": cycle["wall_ns"] <= wall_limit_ns
                and cycle["exit_code"] == 0,
                "rss_threshold": {
                    "status": "not_evaluable",
                    "reason": "Governance defines no Phase 1A RSS limit.",
                },
            },
        }
    output.write_bytes(canonical(evidence) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    collect_resources(root, args.output_dir / "phase1a-resource-profile.json")
    collect_dependencies(root, args.output_dir / "phase1a-supply-chain.json")
    collect_image(root, args.output_dir / "phase1a-sandbox-image.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
