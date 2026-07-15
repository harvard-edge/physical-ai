"""Typed, provider-neutral cognitive runtime primitives."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from .domain import StrictModel


PrivacyClass = Literal["synthetic", "derived-redacted", "internal", "restricted"]


class Provenance(StrictModel):
    source: str = Field(min_length=1, max_length=256)
    created_at: datetime
    privacy_class: PrivacyClass
    evidence_digest: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")


class GoalRecord(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    record_id: str = Field(pattern=r"^MIOS-GOAL-[A-Z0-9-]{4,}$")
    objective: str = Field(min_length=1, max_length=4096)
    success_criteria: tuple[str, ...] = Field(min_length=1, max_length=32)
    budget_tokens: int = Field(ge=1)
    deadline: datetime
    authority_scope: tuple[str, ...] = Field(max_length=32)
    provenance: Provenance


class ObservationRecord(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    record_id: str = Field(pattern=r"^MIOS-OBS-[A-Z0-9-]{4,}$")
    summary: str = Field(min_length=1, max_length=4096)
    payload_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    provenance: Provenance


class BeliefRecord(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    record_id: str = Field(pattern=r"^MIOS-BELIEF-[A-Z0-9-]{4,}$")
    claim: str = Field(min_length=1, max_length=4096)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_ids: tuple[str, ...] = Field(min_length=1, max_length=64)
    status: Literal["proposed", "accepted", "retracted"] = "proposed"
    provenance: Provenance


class CapabilityLease(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    lease_id: str = Field(pattern=r"^MIOS-LEASE-[A-Z0-9-]{4,}$")
    capability: str = Field(min_length=1, max_length=128)
    holder: str = Field(min_length=1, max_length=128)
    expires_at: datetime
    revocable: bool = True
    provenance: Provenance


class ActionProposal(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    record_id: str = Field(pattern=r"^MIOS-ACTION-[A-Z0-9-]{4,}$")
    capability: str = Field(min_length=1, max_length=128)
    intent: str = Field(min_length=1, max_length=2048)
    reversible: bool
    risk_class: Literal["informational", "interaction", "physical"]
    status: Literal["proposed", "authorized", "rejected", "executed"] = "proposed"
    provenance: Provenance
