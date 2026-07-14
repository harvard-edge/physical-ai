"""MiOS-owned domain states and validated records."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ControllerState(StrEnum):
    RUNNING = "RUNNING"
    PAUSING = "PAUSING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    INCIDENT = "INCIDENT"


class ExperimentState(StrEnum):
    OBSERVED = "OBSERVED"
    TRIAGED = "TRIAGED"
    PREREGISTERED = "PREREGISTERED"
    DESIGNED = "DESIGNED"
    IMPLEMENTING = "IMPLEMENTING"
    EVALUATING = "EVALUATING"
    REVIEWING = "REVIEWING"
    LOCAL_CANDIDATE_READY = "LOCAL_CANDIDATE_READY"
    PAUSED = "PAUSED"
    REJECTED = "REJECTED"
    INCIDENT = "INCIDENT"


NEXT_STATE: dict[ExperimentState, ExperimentState] = {
    ExperimentState.OBSERVED: ExperimentState.TRIAGED,
    ExperimentState.TRIAGED: ExperimentState.PREREGISTERED,
    ExperimentState.PREREGISTERED: ExperimentState.DESIGNED,
    ExperimentState.DESIGNED: ExperimentState.IMPLEMENTING,
    ExperimentState.IMPLEMENTING: ExperimentState.EVALUATING,
    ExperimentState.EVALUATING: ExperimentState.REVIEWING,
    ExperimentState.REVIEWING: ExperimentState.LOCAL_CANDIDATE_READY,
}

TERMINAL_STATES = {
    ExperimentState.LOCAL_CANDIDATE_READY,
    ExperimentState.PAUSED,
    ExperimentState.REJECTED,
    ExperimentState.INCIDENT,
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ObservationInput(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    observation_id: str = Field(pattern=r"^MIOS-OBS-[0-9]{4,}$")
    source: Literal["synthetic_fixture"]
    privacy_class: Literal["synthetic"]
    summary: str = Field(min_length=1, max_length=2048)
    payload: dict[str, Any]


class ArtifactReference(StrictModel):
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    size: int = Field(ge=0)
    media_type: str
    logical_name: str


class ReviewAttestation(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    experiment_id: str
    role: Literal["verification_engineer", "research_skeptic"]
    reviewer_identity: str
    candidate_commit: str
    evidence_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    verdict: Literal["approve", "reject"]
    decisive: bool


class PolicyViolation(RuntimeError):
    """A task attempted an effect outside its authority."""


class IntegrityViolation(RuntimeError):
    """Stored evidence no longer matches its recorded digest."""


class BudgetViolation(RuntimeError):
    """A budget cannot be reserved or has been exhausted."""


class StaleLease(RuntimeError):
    """A worker tried to commit with an expired fencing token."""
