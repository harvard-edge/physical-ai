"""Validation helpers for the provider-neutral MiOS agent protocol."""

from __future__ import annotations

import json
import os
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from .canonical import canonical_bytes, digest_json, sha256_bytes
from .domain import PolicyViolation


class AgentProtocol:
    def __init__(self, repository_root: Path):
        protocol_root = repository_root / "protocol"
        self.task_schema = json.loads(
            (protocol_root / "agent-task.schema.json").read_text(encoding="utf-8")
        )
        self.result_schema = json.loads(
            (protocol_root / "agent-result.schema.json").read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator.check_schema(self.task_schema)
        jsonschema.Draft202012Validator.check_schema(self.result_schema)
        self.task_validator = jsonschema.Draft202012Validator(
            self.task_schema, format_checker=jsonschema.FormatChecker()
        )
        self.result_validator = jsonschema.Draft202012Validator(
            self.result_schema, format_checker=jsonschema.FormatChecker()
        )
        budget_policy = yaml.safe_load(
            (repository_root / "governance" / "budgets.yml").read_text(encoding="utf-8")
        )
        active_period = budget_policy["active_period"]
        authorized_at = self._parse_time(active_period["authorized_at"])
        self.not_before = authorized_at
        self.deadline = authorized_at + timedelta(
            days=int(active_period["expires_after_days"])
        )

    @staticmethod
    def _validate(validator, value: dict[str, Any], kind: str) -> None:
        errors = sorted(
            validator.iter_errors(value), key=lambda error: list(error.path)
        )
        if errors:
            first = errors[0]
            location = ".".join(str(part) for part in first.path) or "<root>"
            raise PolicyViolation(
                f"invalid agent {kind} at {location}: {first.message}"
            )

    def validate_task(self, value: dict[str, Any]) -> None:
        self._validate(self.task_validator, value, "task")

    def validate_result(self, value: dict[str, Any]) -> None:
        self._validate(self.result_validator, value, "result")

    @staticmethod
    def _parse_time(value: str) -> datetime:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise PolicyViolation("agent timestamp must include a timezone")
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _format_time(value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _read_regular_file(path: Path, maximum_bytes: int) -> bytes:
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags)
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise PolicyViolation(
                    "agent output is not a single-linked regular file"
                )
            if metadata.st_size > maximum_bytes:
                raise PolicyViolation("agent output exceeded its byte budget")
            data = b""
            while len(data) <= maximum_bytes:
                chunk = os.read(descriptor, min(65536, maximum_bytes + 1 - len(data)))
                if not chunk:
                    break
                data += chunk
            if len(data) > maximum_bytes:
                raise PolicyViolation("agent output exceeded its byte budget")
            return data
        finally:
            os.close(descriptor)

    @classmethod
    def read_result_file(
        cls, path: Path, maximum_bytes: int = 65_536
    ) -> dict[str, Any]:
        try:
            value = json.loads(cls._read_regular_file(path, maximum_bytes))
        except (FileNotFoundError, OSError, json.JSONDecodeError) as error:
            raise PolicyViolation(
                "agent result is missing, unsafe, or invalid"
            ) from error
        if not isinstance(value, dict):
            raise PolicyViolation("agent result must be a JSON object")
        return value

    def fixture_task(
        self,
        *,
        experiment_id: str,
        attempt_id: str,
        policy_digest: str,
        source: Path,
    ) -> dict[str, Any]:
        source_bytes = source.read_bytes()
        task_id = f"MIOS-TASK-{experiment_id}-IMPLEMENT"
        nonce = digest_json(
            {
                "task_id": task_id,
                "attempt_id": attempt_id,
                "policy_digest": policy_digest,
                "source_sha256": sha256_bytes(source_bytes),
            }
        )[:32]
        task = {
            "protocol_version": "1.1.0",
            "task_id": task_id,
            "experiment_id": experiment_id,
            "attempt_id": attempt_id,
            "role": "implementation_engineer",
            "objective": "Change the synthetic behavior fixture from the observed value to the preregistered expected value.",
            "input_artifacts": [
                {
                    "logical_name": "behavior_source",
                    "uri": "workspace:///src/behavior.py",
                    "sha256": sha256_bytes(source_bytes),
                    "media_type": "text/x-python",
                    "privacy_class": "synthetic",
                }
            ],
            "capabilities": {
                "read_scopes": ["src/behavior.py"],
                "write_scopes": ["src/behavior.py"],
                "commands": ["fixture_replace_value_v1"],
                "network": False,
                "external_services": [],
            },
            "prohibited_effects": [
                "change_tests",
                "change_git_metadata",
                "read_controller_state",
                "network",
                "model_call",
                "github",
                "robot",
            ],
            "acceptance_checks": [
                {
                    "id": "frozen_acceptance_test",
                    "command_id": "fixture_unittest_v1",
                    "expected": "exit_code_equals_zero",
                }
            ],
            "budgets": {
                "wall_ms": 30000,
                "cpu_ms": 30000,
                "memory_bytes": 134217728,
                "output_bytes": 65536,
                "file_count": 1,
                "processes": 4,
            },
            "not_before": self._format_time(self.not_before),
            "deadline": self._format_time(self.deadline),
            "output_contract": "protocol/agent-result.schema.json",
            "escalation_conditions": [
                "source_digest_mismatch",
                "unexpected_source_content",
                "write_scope_insufficient",
            ],
            "policy_digest": policy_digest,
            "nonce": nonce,
        }
        self.validate_task(task)
        now = datetime.now(timezone.utc)
        if now < self.not_before or now >= self.deadline:
            raise PolicyViolation("Phase 1A task authority is not currently active")
        return task

    def review_task(
        self,
        *,
        experiment_id: str,
        attempt_id: str,
        role: str,
        policy_digest: str,
        source: Path,
        acceptance_test: Path,
        evidence_bundle: bytes,
    ) -> dict[str, Any]:
        command_by_role = {
            "verification_engineer": "fixture_verify_candidate_v1",
            "research_skeptic": "fixture_challenge_candidate_v1",
        }
        if role not in command_by_role:
            raise PolicyViolation(f"unsupported deterministic reviewer role: {role}")
        command_id = command_by_role[role]
        task_id = f"MIOS-TASK-{experiment_id}-REVIEW-{role.upper()}"
        input_artifacts = [
            {
                "logical_name": "behavior_source",
                "uri": "workspace:///src/behavior.py",
                "sha256": sha256_bytes(source.read_bytes()),
                "media_type": "text/x-python",
                "privacy_class": "synthetic",
            },
            {
                "logical_name": "frozen_acceptance_test",
                "uri": "workspace:///tests/test_acceptance.py",
                "sha256": sha256_bytes(acceptance_test.read_bytes()),
                "media_type": "text/x-python",
                "privacy_class": "synthetic",
            },
            {
                "logical_name": "candidate_evidence_bundle",
                "uri": "exchange:///evidence.json",
                "sha256": sha256_bytes(evidence_bundle),
                "media_type": "application/json",
                "privacy_class": "synthetic",
            },
        ]
        nonce = digest_json(
            {
                "task_id": task_id,
                "attempt_id": attempt_id,
                "policy_digest": policy_digest,
                "inputs": input_artifacts,
            }
        )[:32]
        task = {
            "protocol_version": "1.1.0",
            "task_id": task_id,
            "experiment_id": experiment_id,
            "attempt_id": attempt_id,
            "role": role,
            "objective": (
                "Independently recompute the deterministic candidate evidence "
                "for the assigned review role."
            ),
            "input_artifacts": input_artifacts,
            "capabilities": {
                "read_scopes": [
                    "src/behavior.py",
                    "tests/test_acceptance.py",
                    "evidence.json",
                ],
                "write_scopes": [],
                "commands": [command_id],
                "network": False,
                "external_services": [],
            },
            "prohibited_effects": [
                "change_candidate",
                "change_tests",
                "change_git_metadata",
                "network",
                "model_call",
                "github",
                "robot",
            ],
            "acceptance_checks": [
                {
                    "id": "independent_evidence_recomputation",
                    "command_id": command_id,
                    "expected": "all_role_invariants_hold",
                }
            ],
            "budgets": {
                "wall_ms": 30000,
                "cpu_ms": 30000,
                "memory_bytes": 134217728,
                "output_bytes": 65536,
                "file_count": 1,
                "processes": 4,
            },
            "not_before": self._format_time(self.not_before),
            "deadline": self._format_time(self.deadline),
            "output_contract": "protocol/agent-result.schema.json",
            "escalation_conditions": [
                "input_digest_mismatch",
                "candidate_evidence_mismatch",
                "role_invariant_failed",
            ],
            "policy_digest": policy_digest,
            "nonce": nonce,
        }
        self.validate_task(task)
        now = datetime.now(timezone.utc)
        if now < self.not_before or now >= self.deadline:
            raise PolicyViolation("Phase 1A review authority is not currently active")
        return task

    def _validate_result_authority(
        self, task: dict[str, Any], result: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        self.validate_result(result)
        rendered = canonical_bytes(result)
        if any(
            marker in rendered
            for marker in (
                b"SECRET_CANARY",
                b"TOKEN_CANARY",
                b"KEY_CANARY",
                b"PASSWORD_CANARY",
            )
        ):
            raise PolicyViolation("agent result contained a secret canary")
        for field in ("task_id", "experiment_id", "attempt_id", "nonce"):
            if result[field] != task[field]:
                raise PolicyViolation(f"agent result forged or mismatched {field}")
        if result["status"] != "succeeded":
            raise PolicyViolation(f"agent worker did not succeed: {result['status']}")
        not_before = self._parse_time(task["not_before"])
        deadline = self._parse_time(task["deadline"])
        started = self._parse_time(result["started_at"])
        finished = self._parse_time(result["finished_at"])
        if not (not_before <= started <= finished <= deadline):
            raise PolicyViolation("agent result timestamps are outside task authority")
        if datetime.now(timezone.utc) >= deadline:
            raise PolicyViolation("agent result arrived after its deadline")
        commands = result["commands_executed"]
        if len(commands) != 1:
            raise PolicyViolation("agent worker must execute exactly one command")
        command = commands[0]
        if command["command_id"] not in task["capabilities"]["commands"]:
            raise PolicyViolation("agent worker executed an unauthorized command")
        if command["argv_digest"] != digest_json([command["command_id"]]):
            raise PolicyViolation("agent worker command argv digest is invalid")
        if command["exit_code"] != 0:
            raise PolicyViolation("agent worker command did not succeed")
        actuals = result["resource_actuals"]
        budget_mapping = {
            "wall_ms": "wall_ms",
            "cpu_ms": "cpu_ms",
            "peak_memory_bytes": "memory_bytes",
            "output_bytes": "output_bytes",
            "files": "file_count",
            "processes": "processes",
        }
        for actual_name, budget_name in budget_mapping.items():
            if int(actuals[actual_name]) > int(task["budgets"][budget_name]):
                raise PolicyViolation(f"agent worker exceeded {budget_name} budget")
        if command["duration_ms"] > actuals["wall_ms"]:
            raise PolicyViolation("command duration exceeds reported wall time")
        available_evidence = {
            artifact["sha256"] for artifact in task["input_artifacts"]
        } | {output["sha256"] for output in result["outputs"]}
        if any(
            evidence_id not in available_evidence
            for claim in result["claims"]
            for evidence_id in claim["evidence_artifact_ids"]
        ):
            raise PolicyViolation("agent claim cites unavailable evidence")
        return command, actuals

    def validate_fixture_result(
        self,
        task: dict[str, Any],
        result: dict[str, Any],
        workspace: Path,
    ) -> dict[str, Any]:
        if not result.get("outputs"):
            raise PolicyViolation("fixture worker returned no output")
        output = result["outputs"][0]
        path = workspace / output["relative_path"]
        try:
            resolved = path.resolve(strict=True)
        except (FileNotFoundError, RuntimeError) as error:
            raise PolicyViolation("fixture worker output is unavailable") from error
        if workspace.resolve() not in resolved.parents:
            raise PolicyViolation("fixture worker output escaped its workspace")
        data = self._read_regular_file(path, int(task["budgets"]["output_bytes"]))
        return self.validate_fixture_record(task, result, data)

    def validate_fixture_record(
        self,
        task: dict[str, Any],
        result: dict[str, Any],
        output_bytes: bytes,
    ) -> dict[str, Any]:
        _, actuals = self._validate_result_authority(task, result)
        if len(result["outputs"]) != 1:
            raise PolicyViolation("fixture worker must return exactly one output")
        output = result["outputs"][0]
        if output["relative_path"] != "src/behavior.py":
            raise PolicyViolation("fixture worker returned an unauthorized output path")
        if len(output_bytes) > int(task["budgets"]["output_bytes"]):
            raise PolicyViolation("fixture worker output exceeded its byte budget")
        if output["sha256"] != sha256_bytes(output_bytes) or output["size"] != len(
            output_bytes
        ):
            raise PolicyViolation("fixture worker output digest or size is invalid")
        if actuals["output_bytes"] != len(output_bytes):
            raise PolicyViolation("fixture worker resource report is inconsistent")
        return {
            "task_digest": digest_json(task),
            "result_digest": digest_json(result),
            "worker": result["worker"],
        }

    def validate_review_result(
        self, task: dict[str, Any], result: dict[str, Any]
    ) -> dict[str, Any]:
        self._validate_result_authority(task, result)
        if task["role"] not in {"verification_engineer", "research_skeptic"}:
            raise PolicyViolation("review result has an unauthorized role")
        if result["outputs"]:
            raise PolicyViolation("reviewer must not produce candidate outputs")
        if not result["claims"]:
            raise PolicyViolation("reviewer returned no independently checked claims")
        if result["errors"] or result["unresolved"]:
            raise PolicyViolation("reviewer returned unresolved evidence")
        return {
            "task_digest": digest_json(task),
            "result_digest": digest_json(result),
            "reviewer_identity": (f"{task['role']}:{digest_json(result)[:24]}"),
            "worker": result["worker"],
        }
