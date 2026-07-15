import pytest
from pydantic import ValidationError

from mios_controller.task_packet import AgentTaskPacket


def test_task_packet_requires_bounded_budget_and_acceptance() -> None:
    packet = AgentTaskPacket(
        task_id="task-1",
        experiment_id="MIOS-EXP-0001",
        role="verifier",
        objective="Reproduce the candidate result",
        acceptance_tests=["uv run pytest"],
        budgets={"wall_clock_minutes": 10, "tokens": 1000, "money_usd": 1.0},
        required_outputs=["verification-report.json"],
    )
    assert packet.schema_version == "1.0.0"


def test_task_packet_rejects_missing_acceptance_tests() -> None:
    with pytest.raises(ValidationError):
        AgentTaskPacket(
            task_id="task-1",
            experiment_id="MIOS-EXP-0001",
            role="verifier",
            objective="No acceptance test",
            budgets={"wall_clock_minutes": 10, "tokens": 1000, "money_usd": 0},
            required_outputs=["report"],
        )
