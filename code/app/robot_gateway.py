"""Bounded robot gateway used by the native Reachy app and its simulator."""

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Protocol


@dataclass(frozen=True)
class GatewayResult:
    operation: str
    status: str
    reason: str


class RobotGateway(Protocol):
    def speak(self, audio_path: str) -> GatewayResult: ...

    def gesture(self, mood: str, duration_seconds: float) -> GatewayResult: ...

    def protective_stop(self) -> GatewayResult: ...


class SafeRobotGateway:
    """Adapter seam; the SDK-specific implementation remains behind this API."""

    ALLOWED_MOODS = frozenset({"friendly", "excited", "curious", "neutral"})

    def __init__(self) -> None:
        self.stopped = False

    def speak(self, audio_path: str) -> GatewayResult:
        if self.stopped:
            return GatewayResult("speak", "STOPPED", "protective stop is active")
        if not audio_path:
            return GatewayResult("speak", "REJECTED", "audio path is empty")
        return GatewayResult("speak", "AUTHORIZED", "SDK adapter may play approved audio")

    def gesture(self, mood: str, duration_seconds: float) -> GatewayResult:
        if self.stopped:
            return GatewayResult("gesture", "STOPPED", "protective stop is active")
        if mood not in self.ALLOWED_MOODS:
            return GatewayResult("gesture", "REJECTED", "mood is outside the gateway contract")
        if not 0.0 < duration_seconds <= 30.0:
            return GatewayResult("gesture", "REJECTED", "gesture duration exceeds the contract")
        return GatewayResult("gesture", "AUTHORIZED", "SDK adapter may execute bounded gesture")

    def protective_stop(self) -> GatewayResult:
        self.stopped = True
        return GatewayResult("protective_stop", "STOPPED", "future operations are rejected")


class ControlWatchdog:
    """Monotonic heartbeat watchdog for the native control loop."""

    def __init__(self, timeout_seconds: float = 0.25) -> None:
        if timeout_seconds <= 0:
            raise ValueError("watchdog timeout must be positive")
        self.timeout_seconds = timeout_seconds
        self._last_heartbeat = time.monotonic()

    def heartbeat(self) -> None:
        self._last_heartbeat = time.monotonic()

    def expired(self, now: float | None = None) -> bool:
        current = time.monotonic() if now is None else now
        return current - self._last_heartbeat > self.timeout_seconds
