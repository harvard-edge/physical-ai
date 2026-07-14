"""Bounded restartable supervisor with persistent stopping semantics."""

from __future__ import annotations

import os
import random
import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path
from typing import Any

import fcntl

from .canonical import atomic_write, canonical_bytes, utc_now
from .dbos_workflow import DurableWorkflowRuntime
from .domain import BudgetViolation
from .engine import EvolutionEngine
from .sandbox import clear_sandbox_stop, request_sandbox_stop


class SupervisorLock:
    def __init__(self, path: Path):
        self.path = path
        self.handle = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+b")
        try:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            self.handle.close()
            raise RuntimeError(
                "another MiOS supervisor owns the controller root"
            ) from error
        self.handle.seek(0)
        self.handle.truncate()
        self.handle.write(
            canonical_bytes(
                {
                    "pid": os.getpid(),
                    "started_at": utc_now(),
                    "boot_id": os.urandom(16).hex(),
                }
            )
            + b"\n"
        )
        self.handle.flush()
        os.fsync(self.handle.fileno())
        return self

    def __exit__(self, exc_type, exc, traceback):
        if self.handle:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()


class Supervisor:
    def __init__(
        self,
        engine: EvolutionEngine,
        *,
        allow_cooperative: bool = False,
        base_backoff_seconds: float = 0.25,
        max_backoff_seconds: float = 5.0,
    ):
        self.engine = engine
        self.allow_cooperative = allow_cooperative
        self.base_backoff_seconds = base_backoff_seconds
        self.max_backoff_seconds = max_backoff_seconds
        self.stop_event = threading.Event()
        self.active_experiment: str | None = None
        self._previous_handlers: dict[int, Any] = {}
        self._runtime_checkpoint_ns: int | None = None
        self._pending_signal: int | None = None

    def request_stop(self, reason: str) -> None:
        if not self.stop_event.is_set():
            self.stop_event.set()
            request_sandbox_stop()
            atomic_write(self.engine.paths.stop_file, f"{reason}\n".encode())
            self.engine.registry.begin_pausing(reason)

    def _account_runtime(self) -> bool:
        now = time.monotonic_ns()
        if self._runtime_checkpoint_ns is None:
            self._runtime_checkpoint_ns = now
            return True
        elapsed_ms = (now - self._runtime_checkpoint_ns) // 1_000_000
        if elapsed_ms < 1:
            return True
        try:
            self.engine.registry.consume_budget(
                "controller_runtime_ms", int(elapsed_ms)
            )
        except BudgetViolation:
            self.request_stop("controller runtime budget exhausted")
            return False
        self._runtime_checkpoint_ns += int(elapsed_ms) * 1_000_000
        return True

    def _handle_signal(self, signum, frame) -> None:
        # A Python signal can interrupt the main thread while it owns a SQLite
        # transaction. Record only the signal here. Normal control flow persists
        # the stop at the next polling boundary.
        self._pending_signal = signum

    def _persist_pending_signal(self) -> bool:
        signum = self._pending_signal
        if signum is None:
            return False
        self._pending_signal = None
        self.request_stop(f"received signal {signal.Signals(signum).name}")
        return True

    def _install_signals(self) -> None:
        for signum in (signal.SIGINT, signal.SIGTERM):
            self._previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, self._handle_signal)

    def _restore_signals(self) -> None:
        for signum, handler in self._previous_handlers.items():
            signal.signal(signum, handler)

    def _wait_or_observe_stop(self, delay: float) -> None:
        """Wait in short slices so an external pause file is promptly observed."""
        deadline = time.monotonic() + delay
        while not self.stop_event.is_set():
            if self._persist_pending_signal():
                return
            if self.engine.paths.stop_file.exists():
                self.request_stop("persistent kill switch was activated")
                return
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            self.stop_event.wait(min(0.1, remaining))

    def run(self, max_cycles: int | None, explicit_resume: bool) -> dict[str, Any]:
        if max_cycles is not None and max_cycles < 1:
            raise ValueError("max_cycles must be positive")
        with SupervisorLock(self.engine.paths.metadata / "supervisor.lock"):
            self.engine.policy.assert_campaign_active()
            if self.engine.paths.stop_file.exists():
                self.engine.registry.pause("persistent kill switch is present")
                raise RuntimeError(
                    "persistent kill switch is present; use the dedicated resume command"
                )
            if not explicit_resume:
                raise RuntimeError("supervisor requires explicit resume authority")
            if self.engine.registry.setting("controller_state") != "RUNNING":
                raise RuntimeError(
                    "controller is not authorized; use the dedicated resume command"
                )
            self.engine.registry.abandon_running_leases(
                "previous process no longer owns the exclusive supervisor lock"
            )
            clear_sandbox_stop()
            if self.engine.registry.budget_remaining("controller_runtime_ms") <= 0:
                atomic_write(
                    self.engine.paths.stop_file,
                    b"controller runtime budget exhausted\n",
                )
                self.engine.registry.pause("controller runtime budget exhausted")
                raise BudgetViolation("budget exhausted: controller_runtime_ms")
            self._runtime_checkpoint_ns = time.monotonic_ns()
            self._install_signals()
            runtime = DurableWorkflowRuntime(self.engine.paths.root)
            cycles = 0
            completed: list[str] = []
            idle_streak = 0
            try:
                while not self.stop_event.is_set() and (
                    max_cycles is None or cycles < max_cycles
                ):
                    if self._persist_pending_signal():
                        break
                    if not self._account_runtime():
                        break
                    if self.engine.paths.stop_file.exists():
                        self.request_stop("persistent kill switch was activated")
                        break
                    cycles += 1
                    experiment = self.engine.registry.next_experiment()
                    if not experiment:
                        idle_streak += 1
                        delay = min(
                            self.max_backoff_seconds,
                            self.base_backoff_seconds * (2 ** min(idle_streak - 1, 8)),
                        )
                        delay *= 0.9 + random.Random(cycles).random() * 0.2
                        remaining_seconds = (
                            self.engine.registry.budget_remaining(
                                "controller_runtime_ms"
                            )
                            / 1000
                        )
                        delay = min(delay, max(0.001, remaining_seconds))
                        self._wait_or_observe_stop(delay)
                        self._account_runtime()
                        continue
                    idle_streak = 0
                    self.active_experiment = experiment["id"]
                    handle = runtime.start(
                        self.engine.repository_root,
                        self.active_experiment,
                        allow_cooperative=self.allow_cooperative,
                    )
                    with ThreadPoolExecutor(
                        max_workers=1, thread_name_prefix="mios-workflow-wait"
                    ) as pool:
                        future = pool.submit(handle.get_result)
                        while not future.done():
                            try:
                                future.result(timeout=0.1)
                            except FutureTimeout:
                                self._persist_pending_signal()
                                if not self._account_runtime():
                                    runtime.cancel(self.active_experiment)
                                    break
                                if self.stop_event.is_set():
                                    runtime.cancel(self.active_experiment)
                                    break
                        if not self.stop_event.is_set():
                            result = future.result()
                            if result != "LOCAL_CANDIDATE_READY":
                                raise RuntimeError(
                                    f"unexpected workflow result: {result}"
                                )
                            completed.append(self.active_experiment)
                    self.active_experiment = None
                self._account_runtime()
                reason = (
                    "bounded supervisor run completed"
                    if not self.stop_event.is_set()
                    else "operator stop completed"
                )
                self.engine.registry.pause(reason)
                return {
                    "cycles": cycles,
                    "completed": completed,
                    "state": "PAUSED",
                    "reason": reason,
                }
            except BaseException as error:
                self._persist_pending_signal()
                self._account_runtime()
                if self.stop_event.is_set() or self.engine.paths.stop_file.exists():
                    self.engine.registry.pause("operator stop completed")
                    return {
                        "cycles": cycles,
                        "completed": completed,
                        "state": "PAUSED",
                        "reason": "operator stop completed",
                    }
                self.engine.registry.pause(
                    f"supervisor failed: {type(error).__name__}: {error}", incident=True
                )
                raise
            finally:
                if self.stop_event.is_set() and self.active_experiment:
                    try:
                        runtime.cancel(self.active_experiment)
                    except BaseException:
                        pass
                runtime.close()
                self._restore_signals()
