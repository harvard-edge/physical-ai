"""Typed cognitive events shared by runtime and future transport adapters."""
from __future__ import annotations

from datetime import datetime, timezone
import threading
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field


EventKind: TypeAlias = Literal[
    "observation_recorded", "speech_transcribed", "claims_proposed",
    "memory_updated", "plan_created", "skill_requested", "action_executed",
]


class CognitiveEvent(BaseModel):
    kind: EventKind
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = Field(default_factory=dict)


class EventJournal:
    """Small in-process journal; ROS, Zenoh, or dataset adapters can consume later."""

    def __init__(self, maximum: int = 200) -> None:
        self.maximum = maximum
        self._events: list[CognitiveEvent] = []
        self._lock = threading.Lock()

    def publish(self, kind: EventKind, **payload: Any) -> None:
        with self._lock:
            self._events.append(CognitiveEvent(kind=kind, payload=payload))
            self._events = self._events[-self.maximum :]

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            return [event.model_dump(mode="json") for event in self._events[-limit:]]
