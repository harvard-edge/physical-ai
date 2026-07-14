from __future__ import annotations

import json
import shutil
from datetime import timedelta
from pathlib import Path

import jsonschema
import pytest

from mios_controller.domain import PolicyViolation
from mios_controller.canonical import digest_json, sha256_bytes
from mios_controller.policy import PolicyEngine
from mios_controller.protocol import AgentProtocol


REPOSITORY = Path(__file__).resolve().parents[2]


def valid_task_and_result(tmp_path):
    workspace = tmp_path / "workspace"
    source = workspace / "src" / "behavior.py"
    source.parent.mkdir(parents=True)
    shutil.copyfile(
        REPOSITORY
        / "evolution"
        / "fixtures"
        / "behavior-value"
        / "base"
        / "src"
        / "behavior.py",
        source,
    )
    protocol = AgentProtocol(REPOSITORY)
    task = protocol.fixture_task(
        experiment_id="MIOS-EXP-0001",
        attempt_id="MIOS-ATT-0001",
        policy_digest="a" * 64,
        source=source,
    )
    source.write_text('def current_value() -> str:\n    return "new"\n')
    output = source.read_bytes()
    output_digest = sha256_bytes(output)
    result = {
        "protocol_version": "1.1.0",
        "task_id": task["task_id"],
        "experiment_id": task["experiment_id"],
        "attempt_id": task["attempt_id"],
        "nonce": task["nonce"],
        "status": "succeeded",
        "summary": "Changed the one authorized file.",
        "outputs": [
            {
                "logical_name": "behavior_source",
                "relative_path": "src/behavior.py",
                "sha256": output_digest,
                "size": len(output),
                "media_type": "text/x-python",
            }
        ],
        "claims": [
            {
                "statement": "The output was produced.",
                "evidence_artifact_ids": [output_digest],
            }
        ],
        "commands_executed": [
            {
                "command_id": "fixture_replace_value_v1",
                "argv_digest": digest_json(["fixture_replace_value_v1"]),
                "exit_code": 0,
                "duration_ms": 1,
            }
        ],
        "resource_actuals": {
            "wall_ms": 1,
            "cpu_ms": 1,
            "peak_memory_bytes": 1024,
            "output_bytes": len(output),
            "files": 1,
            "processes": 1,
        },
        "policy_events": [],
        "errors": [],
        "assumptions": [],
        "unresolved": [],
        "started_at": task["not_before"],
        "finished_at": task["not_before"],
        "worker": {"implementation": "test_fixture", "version": "1"},
    }
    return protocol, task, result, workspace


def test_agent_protocol_schemas_are_strict() -> None:
    task_schema = json.loads(
        (REPOSITORY / "protocol" / "agent-task.schema.json").read_text()
    )
    result_schema = json.loads(
        (REPOSITORY / "protocol" / "agent-result.schema.json").read_text()
    )
    jsonschema.Draft202012Validator.check_schema(task_schema)
    jsonschema.Draft202012Validator.check_schema(result_schema)
    assert task_schema["additionalProperties"] is False
    assert result_schema["additionalProperties"] is False


@pytest.mark.parametrize(
    "paths",
    [
        ["tests/test_acceptance.py"],
        ["../governance/budgets.yml"],
        ["/tmp/escape"],
        ["src/behavior.py", "tests/test_acceptance.py"],
        [".git/config"],
    ],
)
def test_protected_fixture_changes_fail_closed(paths) -> None:
    policy = PolicyEngine(REPOSITORY)
    with pytest.raises(PolicyViolation):
        policy.assert_fixture_changes(paths)


def test_only_frozen_fixture_source_is_writable() -> None:
    PolicyEngine(REPOSITORY).assert_fixture_changes(["src/behavior.py"])


def test_campaign_authority_has_hard_time_bound() -> None:
    policy = PolicyEngine(REPOSITORY)
    policy.assert_campaign_active(policy.authorized_at)
    with pytest.raises(PolicyViolation, match="authority is not active"):
        policy.assert_campaign_active(policy.expires_at)
    with pytest.raises(PolicyViolation, match="authority is not active"):
        policy.assert_campaign_active(policy.authorized_at - timedelta(seconds=1))


def test_candidate_environment_does_not_inherit_secrets(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EXAMPLE_TOKEN", "TOKEN_CANARY")
    monkeypatch.setenv("SSH_AUTH_SOCK", "/private/agent.sock")
    environment = PolicyEngine(REPOSITORY).candidate_environment(tmp_path)
    assert "EXAMPLE_TOKEN" not in environment
    assert "SSH_AUTH_SOCK" not in environment
    assert set(environment) == {
        "PATH",
        "HOME",
        "TMPDIR",
        "LANG",
        "LC_ALL",
        "GIT_CONFIG_NOSYSTEM",
        "GIT_CONFIG_GLOBAL",
        "GIT_TERMINAL_PROMPT",
        "GIT_ALLOW_PROTOCOL",
    }


def test_malformed_agent_result_is_rejected() -> None:
    protocol = AgentProtocol(REPOSITORY)
    with pytest.raises(PolicyViolation, match="invalid agent result"):
        protocol.validate_result({"protocol_version": "1.1.0", "unexpected": True})


def test_agent_result_enforces_commands_budgets_and_claim_evidence(tmp_path) -> None:
    protocol, task, result, workspace = valid_task_and_result(tmp_path)
    evidence = protocol.validate_fixture_result(task, result, workspace)
    assert evidence["worker"]["implementation"] == "test_fixture"

    result["commands_executed"][0]["command_id"] = "arbitrary_shell"
    with pytest.raises(PolicyViolation, match="unauthorized command"):
        protocol.validate_fixture_result(task, result, workspace)
    result["commands_executed"][0]["command_id"] = "fixture_replace_value_v1"

    result["resource_actuals"]["processes"] = 5
    with pytest.raises(PolicyViolation, match="processes budget"):
        protocol.validate_fixture_result(task, result, workspace)
    result["resource_actuals"]["processes"] = 1

    result["claims"][0]["evidence_artifact_ids"] = ["b" * 64]
    with pytest.raises(PolicyViolation, match="unavailable evidence"):
        protocol.validate_fixture_result(task, result, workspace)


def test_agent_result_rejects_timestamps_outside_task_authority(tmp_path) -> None:
    protocol, task, result, workspace = valid_task_and_result(tmp_path)
    result["finished_at"] = "2099-01-01T00:00:00Z"
    with pytest.raises(PolicyViolation, match="outside task authority"):
        protocol.validate_fixture_result(task, result, workspace)


def test_review_disagreement_fails_closed() -> None:
    policy = PolicyEngine(REPOSITORY)
    with pytest.raises(PolicyViolation, match="disagreement"):
        policy.assert_reviews(
            [
                {
                    "role": "verification_engineer",
                    "reviewer_identity": "review-a",
                    "verdict": "approve",
                    "decisive": True,
                },
                {
                    "role": "research_skeptic",
                    "reviewer_identity": "review-b",
                    "verdict": "reject",
                    "decisive": False,
                },
            ]
        )
