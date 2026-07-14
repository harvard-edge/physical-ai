from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from mios_controller.policy import PolicyEngine
from mios_controller.domain import PolicyViolation
from mios_controller.sandbox import PINNED_IMAGE, SandboxRunner


REPOSITORY = Path(__file__).resolve().parents[2]


def docker_image_available() -> bool:
    if not shutil.which("docker"):
        return False
    return (
        subprocess.run(
            ["docker", "image", "inspect", PINNED_IMAGE],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


@pytest.mark.skipif(
    not docker_image_available(), reason="pinned sandbox image unavailable"
)
def test_fixture_worker_uses_networkless_container(tmp_path) -> None:
    runner = SandboxRunner(REPOSITORY, PolicyEngine(REPOSITORY))
    workspace = tmp_path / "fixture"
    runner.prepare_workspace(workspace)
    result = runner.apply_candidate(workspace, "MIOS-EXP-0001", "MIOS-ATT-0001")
    assert result["profile"] == "container"
    assert result["image"] == PINNED_IMAGE
    assert result["changed_paths"] == ["src/behavior.py"]
    assert runner.evaluate(workspace)["passed"] is True


@pytest.mark.skipif(
    not docker_image_available(), reason="pinned sandbox image unavailable"
)
def test_container_has_no_dns_or_external_network() -> None:
    probe = """
import socket
blocked = 0
for action in (
    lambda: socket.getaddrinfo('github.com', 443),
    lambda: socket.create_connection(('1.1.1.1', 443), timeout=0.5),
):
    try:
        action()
    except OSError:
        blocked += 1
raise SystemExit(0 if blocked == 2 else 1)
"""
    result = subprocess.run(
        [
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
            PINNED_IMAGE,
            "-c",
            probe,
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr


def test_argument_metacharacters_are_not_interpreted_by_a_shell(tmp_path) -> None:
    runner = SandboxRunner(REPOSITORY, PolicyEngine(REPOSITORY), allow_cooperative=True)
    marker = tmp_path / "should-not-exist"
    literal = f"$(touch {marker})"
    result = runner._run(
        [sys.executable, "-c", "import sys; print(sys.argv[1])", literal],
        cwd=tmp_path,
        environment={"PATH": os.environ.get("PATH", "")},
    )
    assert result.exit_code == 0
    assert result.stdout.strip() == literal
    assert not marker.exists()


def test_workspace_audit_rejects_symlink_and_hardlink_outputs(tmp_path) -> None:
    runner = SandboxRunner(REPOSITORY, PolicyEngine(REPOSITORY), allow_cooperative=True)
    workspace = tmp_path / "fixture"
    runner.prepare_workspace(workspace)
    behavior = workspace / "src" / "behavior.py"
    behavior.unlink()
    behavior.symlink_to(workspace / "tests" / "test_acceptance.py")
    with pytest.raises(PolicyViolation, match="symlink"):
        runner.audit_fixture_workspace(workspace)

    behavior.unlink()
    outside = tmp_path / "outside.py"
    outside.write_text('def current_value():\n    return "new"\n')
    os.link(outside, behavior)
    with pytest.raises(PolicyViolation, match="single-linked"):
        runner.audit_fixture_workspace(workspace)


def test_workspace_audit_rejects_untracked_and_gitlink_entries(tmp_path) -> None:
    runner = SandboxRunner(REPOSITORY, PolicyEngine(REPOSITORY), allow_cooperative=True)
    workspace = tmp_path / "fixture"
    runner.prepare_workspace(workspace)
    extra = workspace / "src" / "extra.py"
    extra.write_text("value = 1\n")
    assert "src/extra.py" in runner.changed_paths(workspace)
    with pytest.raises(PolicyViolation, match="file set changed"):
        runner.audit_fixture_workspace(workspace)
    extra.unlink()

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=workspace,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.strip()
    subprocess.run(
        [
            "git",
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{head},src/submodule",
        ],
        cwd=workspace,
        check=True,
    )
    with pytest.raises(PolicyViolation, match="unsafe entries"):
        runner.audit_fixture_workspace(workspace)


@pytest.mark.parametrize(
    ("mode", "message"),
    [
        ("malformed", "missing, unsafe, or invalid"),
        ("oversized", "byte budget"),
        ("secret", "secret canary"),
    ],
)
def test_worker_result_boundary_rejects_hostile_envelopes(
    tmp_path, monkeypatch, mode, message
) -> None:
    runner = SandboxRunner(REPOSITORY, PolicyEngine(REPOSITORY), allow_cooperative=True)
    workspace = tmp_path / mode
    runner.prepare_workspace(workspace)
    monkeypatch.setenv("MIOS_TEST_WORKER_RESULT_MODE", mode)
    with pytest.raises(PolicyViolation, match=message):
        runner.apply_candidate(workspace, "MIOS-EXP-0001", "MIOS-ATT-0001")


def test_cancellation_terminates_child_process_group_within_bound(tmp_path) -> None:
    runner = SandboxRunner(REPOSITORY, PolicyEngine(REPOSITORY), allow_cooperative=True)
    child_pid = tmp_path / "child.pid"
    cancel = threading.Event()
    timer = threading.Timer(0.3, cancel.set)
    program = (
        "import pathlib,subprocess,sys,time; "
        "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
        "pathlib.Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(60)"
    )
    started = time.monotonic()
    timer.start()
    try:
        with pytest.raises(InterruptedError, match="cancelled"):
            runner._run(
                [sys.executable, "-c", program, str(child_pid)],
                cwd=tmp_path,
                environment={"PATH": os.environ.get("PATH", "")},
                timeout=30,
                stop_event=cancel,
                termination_grace=0.5,
            )
    finally:
        timer.cancel()
    assert time.monotonic() - started < 2.0
    pid = int(child_pid.read_text())
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        status = subprocess.run(
            ["ps", "-o", "stat=", "-p", str(pid)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        ).stdout.strip()
        if not status or status.startswith("Z"):
            break
        time.sleep(0.05)
    assert not status or status.startswith("Z")


def test_external_stop_file_cancels_active_process_group(tmp_path) -> None:
    stop_path = tmp_path / "STOP"
    runner = SandboxRunner(
        REPOSITORY,
        PolicyEngine(REPOSITORY),
        allow_cooperative=True,
        stop_path=stop_path,
    )
    timer = threading.Timer(0.3, lambda: stop_path.write_text("pause\n"))
    started = time.monotonic()
    timer.start()
    try:
        with pytest.raises(InterruptedError, match="cancelled"):
            runner._run(
                [sys.executable, "-c", "import time; time.sleep(60)"],
                cwd=tmp_path,
                environment={"PATH": os.environ.get("PATH", "")},
                timeout=30,
                termination_grace=0.5,
            )
    finally:
        timer.cancel()
    assert time.monotonic() - started < 2.0
