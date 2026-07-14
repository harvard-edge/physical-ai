"""Provider-neutral policy contracts for language and future learned actions."""
from __future__ import annotations

from typing import Any, Protocol

from pydantic import BaseModel, Field


class ReasoningPolicy(Protocol):
    """Structural interface implemented by cloud or local reasoning providers."""

    configured: bool

    def analyze_turn(
        self,
        user_text: str,
        *,
        robot_name: str | None,
        history: list[dict[str, str]],
        memory_context: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]: ...


class ActionProposal(BaseModel):
    """Bounded policy output; a safety supervisor must authorize execution."""

    capability: str = Field(max_length=64)
    parameters: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)
    policy: str = Field(max_length=80)


class ActionPolicy(Protocol):
    """Adapter seam for deterministic planners, LeRobot, OpenVLA, or GR00T."""

    def propose(self, observation: dict[str, Any]) -> ActionProposal: ...
