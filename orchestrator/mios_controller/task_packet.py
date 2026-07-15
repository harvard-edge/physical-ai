"""Bounded task packets supplied to MiOS specialist workers."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .domain import StrictModel


class TaskBudgets(StrictModel):
    wall_clock_minutes: int = Field(ge=1, le=24 * 60)
    tokens: int = Field(ge=1, le=10_000_000)
    money_usd: float = Field(ge=0, le=10_000)


class AgentTaskPacket(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    task_id: str = Field(min_length=1, max_length=128)
    experiment_id: str = Field(pattern=r"^MIOS-EXP-[0-9]{4,}$")
    role: str = Field(min_length=1, max_length=64)
    objective: str = Field(min_length=1, max_length=4096)
    context_files: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    write_scope: list[str] = Field(default_factory=list)
    prohibited_actions: list[str] = Field(default_factory=list)
    acceptance_tests: list[str] = Field(min_length=1)
    budgets: TaskBudgets
    required_outputs: list[str] = Field(min_length=1)
    escalation_conditions: list[str] = Field(default_factory=list)
