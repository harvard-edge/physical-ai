from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from mios_controller.cognitive import ActionProposal, GoalRecord, Provenance


def provenance():
    return Provenance(
        source="test", created_at=datetime.now(timezone.utc), privacy_class="synthetic"
    )


def test_goal_requires_bounded_success_criteria_and_budget():
    goal = GoalRecord(
        record_id="MIOS-GOAL-TEST-001",
        objective="Learn a name",
        success_criteria=("recall after restart",),
        budget_tokens=100,
        deadline=datetime.now(timezone.utc) + timedelta(minutes=5),
        authority_scope=("memory.write",),
        provenance=provenance(),
    )
    assert goal.schema_version == "1.0.0"


def test_physical_action_is_only_a_proposal():
    proposal = ActionProposal(
        record_id="MIOS-ACTION-TEST-001",
        capability="robot.motion",
        intent="raise arm",
        reversible=True,
        risk_class="physical",
        provenance=provenance(),
    )
    assert proposal.status == "proposed"


def test_invalid_digest_is_rejected():
    with pytest.raises(ValidationError):
        ActionProposal(
            record_id="MIOS-ACTION-TEST-002",
            capability="robot.motion",
            intent="raise arm",
            reversible=True,
            risk_class="physical",
            provenance=Provenance(
                source="test",
                created_at=datetime.now(timezone.utc),
                privacy_class="synthetic",
                evidence_digest="not-a-digest",
            ),
        )
