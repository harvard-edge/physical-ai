"""Disposable fixture creation and container-isolated worker execution."""

from __future__ import annotations

import os
import signal
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from .canonical import atomic_write, canonical_bytes, digest_json, sha256_bytes
from .domain import PolicyViolation
from .policy import PolicyEngine
from .protocol import AgentProtocol


PINNED_IMAGE = "cgr.dev/chainguard/python@sha256:ce9aaca1f826f7f963cd031e98f8c19f993b1843096d395ea919b646e72cb8de"

_CANCEL_EVENT = threading.Event()


def request_sandbox_stop() -> None:
    """Ask active Phase 1A host subprocess groups to stop promptly."""
    _CANCEL_EVENT.set()


def clear_sandbox_stop() -> None:
    """Clear cancellation when an authorized supervisor starts."""
    _CANCEL_EVENT.clear()


@dataclass(frozen=True)
class CommandResult:
    argv_digest: str
    exit_code: int
    duration_ms: int
    stdout: str
    stderr: str


class SandboxRunner:
    def __init__(
        self,
        repository_root: Path,
        policy: PolicyEngine,
        allow_cooperative: bool = False,
        stop_path: Path | None = None,
    ):
        self.repository_root = repository_root.resolve()
        self.policy = policy
        self.protocol = AgentProtocol(self.repository_root)
        self.allow_cooperative = allow_cooperative
        self.stop_path = stop_path
        self.fixture_root = (
            self.repository_root / "evolution" / "fixtures" / "behavior-value"
        )
        self.worker = self.fixture_root / "fixture_worker.py"
        self.reviewer = self.fixture_root / "fixture_reviewer.py"

    def _run(
        self,
        argv: list[str],
        *,
        cwd: Path,
        environment: dict[str, str],
        timeout: float = 30,
        stop_event: threading.Event | None = None,
        termination_grace: float = 1.0,
    ) -> CommandResult:
        started = time.monotonic_ns()
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        cancel = stop_event or _CANCEL_EVENT
        deadline = time.monotonic() + timeout
        try:
            while True:
                if cancel.is_set() or (
                    self.stop_path is not None and self.stop_path.exists()
                ):
                    raise InterruptedError(f"command cancelled: {argv[0]}")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"command exceeded {timeout} seconds: {argv[0]}")
                try:
                    stdout, stderr = process.communicate(timeout=min(0.1, remaining))
                    break
                except subprocess.TimeoutExpired:
                    continue
        except (InterruptedError, TimeoutError):
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.communicate(timeout=termination_grace)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate(timeout=termination_grace)
            raise
        duration_ms = (time.monotonic_ns() - started) // 1_000_000
        if len(stdout.encode()) + len(stderr.encode()) > 1_000_000:
            raise PolicyViolation("worker output exceeded one MiB")
        secret_markers = (
            "SECRET_CANARY",
            "TOKEN_CANARY",
            "KEY_CANARY",
            "PASSWORD_CANARY",
        )
        if any(marker in stdout or marker in stderr for marker in secret_markers):
            raise PolicyViolation("worker output contained a secret canary")
        return CommandResult(
            argv_digest=digest_json(argv),
            exit_code=process.returncode,
            duration_ms=int(duration_ms),
            stdout=stdout,
            stderr=stderr,
        )

    def prepare_workspace(self, workspace: Path) -> str:
        if workspace.exists():
            self.audit_fixture_workspace(workspace)
            return self.git_root_commit(workspace)
        workspace.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(self.fixture_root / "base", workspace, symlinks=False)
        with tempfile.TemporaryDirectory(prefix="mios-git-") as temporary:
            env = self.policy.candidate_environment(Path(temporary))
            env["GIT_AUTHOR_DATE"] = "2026-07-14T00:00:00Z"
            env["GIT_COMMITTER_DATE"] = "2026-07-14T00:00:00Z"
            Path(env["HOME"]).mkdir()
            Path(env["TMPDIR"]).mkdir()
            commands = [
                ["git", "init", "-b", "main"],
                ["git", "config", "user.name", "MiOS Fixture"],
                ["git", "config", "user.email", "fixture@mios.invalid"],
                ["git", "add", "--", "src", "tests"],
                [
                    "git",
                    "-c",
                    "commit.gpgsign=false",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "commit",
                    "-m",
                    "Create deterministic fixture",
                ],
            ]
            for argv in commands:
                result = self._run(argv, cwd=workspace, environment=env)
                if result.exit_code != 0:
                    raise RuntimeError(result.stderr)
        self.audit_fixture_workspace(workspace)
        return self.git_root_commit(workspace)

    def apply_candidate(
        self,
        workspace: Path,
        experiment_id: str,
        attempt_id: str,
    ) -> dict[str, object]:
        if not workspace.is_dir() or workspace.is_symlink():
            raise PolicyViolation("fixture workspace is not a regular directory")
        self.audit_fixture_workspace(workspace)
        task = self.protocol.fixture_task(
            experiment_id=experiment_id,
            attempt_id=attempt_id,
            policy_digest=self.policy.digest,
            source=workspace / "src" / "behavior.py",
        )
        with tempfile.TemporaryDirectory(prefix="mios-exchange-") as exchange_name:
            exchange = Path(exchange_name)
            task_path = exchange / "task.json"
            result_path = exchange / "result.json"
            atomic_write(task_path, canonical_bytes(task) + b"\n")
            result_mode = os.environ.get("MIOS_TEST_WORKER_RESULT_MODE")
            if result_mode not in {None, "malformed", "oversized", "secret"}:
                raise PolicyViolation("unknown fixture result test mode")
            delay_value = os.environ.get("MIOS_TEST_WORKER_DELAY_SECONDS")
            if delay_value is not None:
                try:
                    delay_seconds = float(delay_value)
                except ValueError as error:
                    raise PolicyViolation("invalid fixture worker delay") from error
                if delay_seconds <= 0 or delay_seconds > 60:
                    raise PolicyViolation("fixture worker delay is outside test bounds")
            if shutil.which("docker") and self._image_available():
                profile = "container"
                controller_identity = digest_json(
                    {"stop_path": str(self.stop_path), "workspace": str(workspace)}
                )[:12]
                container_name = f"mios-{controller_identity}-{attempt_id.lower()}"
                argv = [
                    "docker",
                    "run",
                    "--rm",
                    "--name",
                    container_name,
                    "--network",
                    "none",
                    "--read-only",
                    "--cap-drop",
                    "ALL",
                    "--security-opt",
                    "no-new-privileges",
                    "--pids-limit",
                    "4",
                    "--memory",
                    "128m",
                    "--cpus",
                    "1",
                    "--user",
                    "65532:65532",
                    "--tmpfs",
                    "/tmp:rw,noexec,nosuid,size=16m",
                    "--env",
                    "HOME=/tmp/home",
                    "--env",
                    "PYTHONDONTWRITEBYTECODE=1",
                    "--volume",
                    f"{(workspace / 'src').resolve()}:/workspace/src:rw",
                    "--volume",
                    f"{exchange.resolve()}:/exchange:rw",
                    "--volume",
                    f"{self.worker.resolve()}:/fixture_worker.py:ro",
                    PINNED_IMAGE,
                    "/fixture_worker.py",
                    "/workspace",
                    "/exchange/task.json",
                    "/exchange/result.json",
                ]
                if result_mode is not None:
                    insertion = argv.index("--volume")
                    argv[insertion:insertion] = [
                        "--env",
                        f"MIOS_WORKER_RESULT_MODE={result_mode}",
                    ]
                if delay_value is not None:
                    insertion = argv.index("--volume")
                    argv[insertion:insertion] = [
                        "--env",
                        f"MIOS_WORKER_DELAY_SECONDS={delay_value}",
                    ]
                try:
                    result = self._run(
                        argv,
                        cwd=workspace.parent,
                        environment={"PATH": os.environ.get("PATH", "")},
                    )
                except (InterruptedError, TimeoutError):
                    subprocess.run(
                        ["docker", "rm", "-f", container_name],
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=5,
                        check=False,
                    )
                    raise
            elif self.allow_cooperative:
                profile = "cooperative_fixture"
                environment_root = exchange / "environment"
                environment_root.mkdir()
                env = self.policy.candidate_environment(environment_root)
                if result_mode is not None:
                    env["MIOS_WORKER_RESULT_MODE"] = result_mode
                if delay_value is not None:
                    env["MIOS_WORKER_DELAY_SECONDS"] = delay_value
                Path(env["HOME"]).mkdir()
                Path(env["TMPDIR"]).mkdir()
                result = self._run(
                    [
                        sys.executable,
                        str(self.worker),
                        str(workspace),
                        str(task_path),
                        str(result_path),
                    ],
                    cwd=workspace,
                    environment=env,
                )
            else:
                raise PolicyViolation(
                    "pinned sandbox image is unavailable; cooperative fallback was not authorized"
                )
            if result.exit_code != 0:
                raise RuntimeError(f"fixture worker failed: {result.stderr}")
            exchange_size = sum(
                path.stat().st_size
                for path in exchange.rglob("*")
                if path.is_file() and not path.is_symlink()
            )
            if exchange_size > 131_072:
                raise PolicyViolation("fixture worker exchange exceeded 128 KiB")
            result_value = self.protocol.read_result_file(result_path)
            protocol_evidence = self.protocol.validate_fixture_result(
                task, result_value, workspace
            )
            if result.duration_ms > int(task["budgets"]["wall_ms"]):
                raise PolicyViolation(
                    "supervisor measured fixture wall budget exceeded"
                )
            protocol_evidence["supervisor_enforcement"] = {
                "wall_ms": result.duration_ms,
                "wall_limit_ms": task["budgets"]["wall_ms"],
                "memory_limit_bytes": task["budgets"]["memory_bytes"],
                "process_limit": task["budgets"]["processes"],
                "result_limit_bytes": 65_536,
                "exchange_limit_bytes": 131_072,
                "container_limits_enforced": profile == "container",
            }
            protocol_evidence["task"] = task
            protocol_evidence["result"] = result_value
        changed = self.changed_paths(workspace)
        self.policy.assert_fixture_changes(changed)
        self.audit_fixture_workspace(workspace)
        return {
            "profile": profile,
            "image": PINNED_IMAGE if profile == "container" else None,
            "worker_sha256": sha256_bytes(self.worker.read_bytes()),
            "argv_digest": digest_json(
                [
                    "fixture_worker",
                    profile,
                    PINNED_IMAGE if profile == "container" else "host",
                ]
            ),
            "changed_paths": changed,
            "protocol": protocol_evidence,
        }

    def run_reviews(
        self,
        workspace: Path,
        experiment_id: str,
        attempt_id: str,
        evidence_bundle: dict[str, object],
    ) -> list[dict[str, object]]:
        if not workspace.is_dir() or workspace.is_symlink():
            raise PolicyViolation("fixture workspace is not a regular directory")
        bundle_bytes = canonical_bytes(evidence_bundle) + b"\n"
        reviews: list[dict[str, object]] = []
        for role in ("verification_engineer", "research_skeptic"):
            with tempfile.TemporaryDirectory(
                prefix=f"mios-review-{role}-"
            ) as exchange_name:
                exchange = Path(exchange_name)
                evidence_path = exchange / "evidence.json"
                task_path = exchange / "task.json"
                result_path = exchange / "result.json"
                atomic_write(evidence_path, bundle_bytes)
                task = self.protocol.review_task(
                    experiment_id=experiment_id,
                    attempt_id=attempt_id,
                    role=role,
                    policy_digest=self.policy.digest,
                    source=workspace / "src" / "behavior.py",
                    acceptance_test=workspace / "tests" / "test_acceptance.py",
                    evidence_bundle=bundle_bytes,
                )
                atomic_write(task_path, canonical_bytes(task) + b"\n")
                force_failure = os.environ.get("MIOS_TEST_REVIEW_FAILURE_ROLE")
                if shutil.which("docker") and self._image_available():
                    profile = "container"
                    argv = [
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
                        "--pids-limit",
                        "4",
                        "--memory",
                        "128m",
                        "--cpus",
                        "1",
                        "--user",
                        "65532:65532",
                        "--tmpfs",
                        "/tmp:rw,noexec,nosuid,size=16m",
                        "--env",
                        "HOME=/tmp/home",
                        "--env",
                        "PYTHONDONTWRITEBYTECODE=1",
                    ]
                    if force_failure == role:
                        argv.extend(["--env", f"MIOS_REVIEW_FORCE_FAIL={role}"])
                    argv.extend(
                        [
                            "--volume",
                            f"{(workspace / 'src').resolve()}:/workspace/src:ro",
                            "--volume",
                            f"{(workspace / 'tests').resolve()}:/workspace/tests:ro",
                            "--volume",
                            f"{exchange.resolve()}:/exchange:rw",
                            "--volume",
                            f"{self.reviewer.resolve()}:/fixture_reviewer.py:ro",
                            PINNED_IMAGE,
                            "/fixture_reviewer.py",
                            "/workspace",
                            "/exchange/evidence.json",
                            "/exchange/task.json",
                            "/exchange/result.json",
                        ]
                    )
                    command = self._run(
                        argv,
                        cwd=workspace.parent,
                        environment={"PATH": os.environ.get("PATH", "")},
                    )
                elif self.allow_cooperative:
                    profile = "cooperative_fixture"
                    environment_root = exchange / "environment"
                    environment_root.mkdir()
                    environment = self.policy.candidate_environment(environment_root)
                    Path(environment["HOME"]).mkdir()
                    Path(environment["TMPDIR"]).mkdir()
                    if force_failure == role:
                        environment["MIOS_REVIEW_FORCE_FAIL"] = role
                    command = self._run(
                        [
                            sys.executable,
                            str(self.reviewer),
                            str(workspace),
                            str(evidence_path),
                            str(task_path),
                            str(result_path),
                        ],
                        cwd=workspace,
                        environment=environment,
                    )
                else:
                    raise PolicyViolation("sandbox unavailable for independent review")
                if command.exit_code != 0:
                    raise RuntimeError(
                        f"independent {role} worker failed: {command.stderr}"
                    )
                exchange_size = sum(
                    path.stat().st_size
                    for path in exchange.rglob("*")
                    if path.is_file() and not path.is_symlink()
                )
                if exchange_size > 131_072:
                    raise PolicyViolation("review exchange exceeded 128 KiB")
                result_value = self.protocol.read_result_file(result_path)
                validated = self.protocol.validate_review_result(task, result_value)
                if command.duration_ms > int(task["budgets"]["wall_ms"]):
                    raise PolicyViolation(
                        f"supervisor measured {role} wall budget exceeded"
                    )
                reviews.append(
                    {
                        "role": role,
                        "profile": profile,
                        "image": PINNED_IMAGE if profile == "container" else None,
                        "reviewer_sha256": sha256_bytes(self.reviewer.read_bytes()),
                        "task": task,
                        "result": result_value,
                        "supervisor_enforcement": {
                            "wall_ms": command.duration_ms,
                            "wall_limit_ms": task["budgets"]["wall_ms"],
                            "memory_limit_bytes": task["budgets"]["memory_bytes"],
                            "process_limit": task["budgets"]["processes"],
                            "result_limit_bytes": 65_536,
                            "exchange_limit_bytes": 131_072,
                            "container_limits_enforced": profile == "container",
                        },
                        **validated,
                    }
                )
        if self.changed_paths(workspace):
            raise PolicyViolation("independent reviewer modified the candidate")
        return sorted(reviews, key=lambda review: str(review["role"]))

    def evaluate(self, workspace: Path) -> dict[str, object]:
        self.audit_fixture_workspace(workspace)
        if shutil.which("docker") and self._image_available():
            argv = [
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
                "--pids-limit",
                "4",
                "--memory",
                "128m",
                "--cpus",
                "1",
                "--user",
                "65532:65532",
                "--tmpfs",
                "/tmp:rw,noexec,nosuid,size=16m",
                "--env",
                "HOME=/tmp/home",
                "--env",
                "PYTHONDONTWRITEBYTECODE=1",
                "--workdir",
                "/workspace",
                "--volume",
                f"{(workspace / 'src').resolve()}:/workspace/src:ro",
                "--volume",
                f"{(workspace / 'tests').resolve()}:/workspace/tests:ro",
                PINNED_IMAGE,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
            ]
            result = self._run(
                argv,
                cwd=workspace.parent,
                environment={"PATH": os.environ.get("PATH", "")},
            )
            profile = "container"
        elif self.allow_cooperative:
            with tempfile.TemporaryDirectory(prefix="mios-eval-") as temporary:
                env = self.policy.candidate_environment(Path(temporary))
                Path(env["HOME"]).mkdir()
                Path(env["TMPDIR"]).mkdir()
                result = self._run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                    cwd=workspace,
                    environment=env,
                )
            profile = "cooperative_fixture"
        else:
            raise PolicyViolation("sandbox unavailable")
        return {
            "profile": profile,
            "passed": result.exit_code == 0,
            "exit_code": result.exit_code,
            "argv_digest": digest_json(
                [
                    "fixture_evaluation",
                    profile,
                    PINNED_IMAGE if profile == "container" else "host",
                ]
            ),
        }

    def commit_candidate(self, workspace: Path, experiment_id: str) -> str:
        with tempfile.TemporaryDirectory(prefix="mios-git-") as temporary:
            env = self.policy.candidate_environment(Path(temporary))
            env["GIT_AUTHOR_DATE"] = "2026-07-14T00:01:00Z"
            env["GIT_COMMITTER_DATE"] = "2026-07-14T00:01:00Z"
            Path(env["HOME"]).mkdir()
            Path(env["TMPDIR"]).mkdir()
            result = self._run(
                [
                    "git",
                    "-c",
                    "commit.gpgsign=false",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "commit",
                    "-am",
                    f"Implement {experiment_id} fixture candidate",
                ],
                cwd=workspace,
                environment=env,
            )
            if (
                result.exit_code != 0
                and "nothing to commit" not in result.stdout + result.stderr
            ):
                raise RuntimeError(result.stderr)
        return self.git_commit(workspace)

    def changed_paths(self, workspace: Path) -> list[str]:
        environment = {
            "PATH": os.environ.get("PATH", ""),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
        }
        result = self._run(
            [
                "git",
                "-c",
                "status.renames=false",
                "status",
                "--porcelain=v1",
                "-z",
                "--untracked-files=all",
                "--",
            ],
            cwd=workspace,
            environment=environment,
        )
        if result.exit_code != 0:
            raise RuntimeError(result.stderr)
        paths = []
        for record in result.stdout.split("\0"):
            if not record:
                continue
            if len(record) < 4 or record[2] != " ":
                raise PolicyViolation("unexpected git status record")
            paths.append(record[3:])
        return sorted(paths)

    def audit_fixture_workspace(self, workspace: Path) -> None:
        """Reject links, extra files, and non-regular Git index entries."""

        if workspace.is_symlink() or not workspace.is_dir():
            raise PolicyViolation("fixture workspace is not a regular directory")
        expected_files = {
            "src/__init__.py",
            "src/behavior.py",
            "tests/test_acceptance.py",
        }
        observed_files: set[str] = set()
        for directory_name in ("src", "tests"):
            directory = workspace / directory_name
            if directory.is_symlink() or not directory.is_dir():
                raise PolicyViolation(f"unsafe fixture directory: {directory_name}")
            for path in directory.rglob("*"):
                relative = path.relative_to(workspace).as_posix()
                metadata = path.lstat()
                if stat.S_ISLNK(metadata.st_mode):
                    raise PolicyViolation(f"fixture symlink is forbidden: {relative}")
                if stat.S_ISDIR(metadata.st_mode):
                    continue
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                    raise PolicyViolation(
                        f"fixture entry must be a single-linked file: {relative}"
                    )
                observed_files.add(relative)
        if observed_files != expected_files:
            raise PolicyViolation(f"fixture file set changed: {sorted(observed_files)}")
        result = self._run(
            ["git", "ls-files", "--stage", "--", "src", "tests"],
            cwd=workspace,
            environment={
                "PATH": os.environ.get("PATH", ""),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_ALLOW_PROTOCOL": "",
            },
        )
        if result.exit_code != 0:
            raise RuntimeError(result.stderr)
        indexed: dict[str, str] = {}
        for line in result.stdout.splitlines():
            metadata, path = line.split("\t", 1)
            mode = metadata.split(" ", 1)[0]
            indexed[path] = mode
        if set(indexed) != expected_files or set(indexed.values()) != {"100644"}:
            raise PolicyViolation(f"fixture index contains unsafe entries: {indexed}")

    def git_commit(self, workspace: Path) -> str:
        result = self._run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            environment={
                "PATH": os.environ.get("PATH", ""),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
            },
        )
        if result.exit_code != 0:
            raise RuntimeError(result.stderr)
        return result.stdout.strip()

    def git_root_commit(self, workspace: Path) -> str:
        result = self._run(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            cwd=workspace,
            environment={
                "PATH": os.environ.get("PATH", ""),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
            },
        )
        if result.exit_code != 0:
            raise RuntimeError(result.stderr)
        commits = result.stdout.splitlines()
        if len(commits) != 1:
            raise RuntimeError("fixture repository must have exactly one root commit")
        return commits[0]

    def _image_available(self) -> bool:
        result = subprocess.run(
            ["docker", "image", "inspect", PINNED_IMAGE],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=False,
        )
        return result.returncode == 0
