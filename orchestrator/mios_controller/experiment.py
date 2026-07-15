"""Validated, append-only experiment records for MiOS evolution."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from .domain import StrictModel


class ExperimentTrigger(StrictModel):
    observation_ids: list[str] = Field(default_factory=list)
    detected_by: str = Field(min_length=1)
    privacy_class: Literal["synthetic", "derived-nonverbatim", "approved"]


class ExperimentHypothesis(StrictModel):
    statement: str = Field(min_length=1, max_length=4096)
    expected_mechanism: str = Field(min_length=1, max_length=4096)


class BaselineCondition(StrictModel):
    release: str = Field(min_length=1)
    comparison_condition: Literal["fixed_single_agent", "fixed_specialist_team", "adaptive_mios"]
    metrics: dict[str, float | int | str] = Field(default_factory=dict)


class Preregistration(StrictModel):
    artifact_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    frozen_at: str = Field(min_length=1)
    primary_metric: str = Field(min_length=1)
    minimum_effect: float
    sample_size: int = Field(ge=1)


class ExperimentEvaluation(StrictModel):
    public_suite: str = Field(min_length=1)
    sealed_suite_attestation: str | None = None
    simulation_result: Literal["pass", "fail", "inconclusive"]
    evaluator_version: str = Field(min_length=1)
    complete_failure_inventory: list[str] = Field(default_factory=list)


class ExperimentChange(StrictModel):
    issue: str | None = None
    branch: str | None = None
    pull_request: str | None = None
    commits: list[str] = Field(default_factory=list)


class ExperimentReview(StrictModel):
    architecture: Literal["approve", "reject", "pending"]
    safety: Literal["approve", "reject", "pending"]
    verification: Literal["approve", "reject", "pending"]


class ExperimentDeployment(StrictModel):
    release: str | None = None
    canary_window: str | None = None
    rollback_release: str | None = None


class ExperimentOutcome(StrictModel):
    decision: Literal["accepted", "rejected", "inconclusive", "rolled_back"]
    measured_delta: dict[str, float | int | str] = Field(default_factory=dict)
    human_interventions: list[str] = Field(default_factory=list)
    autonomy_level_supported: Literal["A0", "A1", "A2", "A3", "A4", "A5"]


class ExperimentLesson(StrictModel):
    supported_claims: list[str] = Field(default_factory=list)
    rejected_claims: list[str] = Field(default_factory=list)
    next_questions: list[str] = Field(default_factory=list)


class ExperimentRecord(StrictModel):
    """The research record; artifacts and ledger hashes remain separate."""

    schema_version: Literal["1.0.0"] = "1.0.0"
    experiment_id: str = Field(pattern=r"^MIOS-EXP-[0-9]{4,}$")
    parent_experiment_id: str | None = None
    campaign_id: str = Field(pattern=r"^MIOS-CAMPAIGN-[A-Za-z0-9-]+$")
    autonomy_level_claimed: Literal["A0", "A1", "A2", "A3", "A4", "A5"]
    trigger: ExperimentTrigger
    hypothesis: ExperimentHypothesis
    baseline: BaselineCondition
    preregistration: Preregistration
    alternatives: list[str] = Field(default_factory=list)
    selected_design: str = Field(min_length=1)
    risks: list[str] = Field(default_factory=list)
    budgets: dict[str, float | int] = Field(default_factory=dict)
    evaluation: ExperimentEvaluation
    change: ExperimentChange
    review: ExperimentReview
    deployment: ExperimentDeployment
    outcome: ExperimentOutcome
    lesson: ExperimentLesson
    previous_record_hash: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")

    def to_payload(self) -> dict[str, Any]:
        """Return canonicalizable data for a ledger payload."""
        return self.model_dump(mode="json", exclude_none=True)
