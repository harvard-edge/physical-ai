"""Small, model-independent contracts for one MiOS cognitive turn.

These are deliberately transport-neutral.  They let the runtime record what a
model saw and proposed without making the model a privileged part of the app.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class ContextPacket(BaseModel):
    id: str = Field(default_factory=lambda: f"ctx_{uuid4().hex[:12]}")
    user_text: str = Field(min_length=1, max_length=500)
    robot_name: str | None = None
    memory_context: list[dict[str, Any]] = Field(default_factory=list)
    history_turns: int = 0
    assembled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ActionProposal(BaseModel):
    id: str = Field(default_factory=lambda: f"prop_{uuid4().hex[:12]}")
    context_id: str
    intent: str = "conversation"
    requested_capabilities: list[str] = Field(default_factory=list)
    effect: Literal["none", "speak", "speak_and_gesture"] = "none"
    approved: bool = False
    rationale: str = "awaiting deterministic validation"


class MemoryMutation(BaseModel):
    id: str = Field(default_factory=lambda: f"mem_{uuid4().hex[:12]}")
    context_id: str
    kind: Literal["robot_name", "claim"]
    evidence_episode_id: str
    accepted: bool = True
