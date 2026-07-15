import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_task_packet_protocol_schema_is_valid() -> None:
    schema = json.loads(
        (Path(__file__).parents[2] / "protocol" / "task-packet.schema.json").read_text()
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(
        {
            "schema_version": "1.0.0",
            "task_id": "task-1",
            "experiment_id": "MIOS-EXP-0001",
            "role": "verifier",
            "objective": "Verify",
            "acceptance_tests": ["pytest"],
            "budgets": {"wall_clock_minutes": 1, "tokens": 1, "money_usd": 0},
            "required_outputs": ["report"],
        }
    )
