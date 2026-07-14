"""Fail-closed Phase 1A policy loading and authorization."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .canonical import digest_json, sha256_bytes
from .domain import PolicyViolation


POLICY_FILES = (
    "authority-policy.yml",
    "budgets.yml",
    "dependency-policy.yml",
    "privacy-policy.yml",
    "protected-paths.yml",
    "release-policy.yml",
)


class PolicyEngine:
    def __init__(self, repository_root: Path):
        self.repository_root = repository_root.resolve()
        self.governance_root = self.repository_root / "governance"
        self.documents: dict[str, dict[str, Any]] = {}
        raw_digests: dict[str, str] = {}
        for name in POLICY_FILES:
            path = self.governance_root / name
            raw = path.read_bytes()
            parsed = yaml.safe_load(raw)
            if not isinstance(parsed, dict):
                raise PolicyViolation(f"policy must be a mapping: {name}")
            self.documents[name] = parsed
            raw_digests[name] = sha256_bytes(raw)
        self.digest = digest_json(raw_digests)
        self._validate_phase_1a()
        active_period = self.documents["budgets.yml"]["active_period"]
        self.authorized_at = self._parse_time(active_period["authorized_at"])
        self.expires_at = self.authorized_at + timedelta(
            days=int(active_period["expires_after_days"])
        )

    @staticmethod
    def _parse_time(value: str) -> datetime:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise PolicyViolation("policy timestamp must include a timezone")
        return parsed.astimezone(timezone.utc)

    def assert_campaign_active(self, now: datetime | None = None) -> None:
        current = now or datetime.now(timezone.utc)
        if current < self.authorized_at or current >= self.expires_at:
            raise PolicyViolation("Phase 1A campaign authority is not active")

    def _validate_phase_1a(self) -> None:
        expected_status = {
            "authority-policy.yml": "active_phase_1a_local_only",
            "budgets.yml": "phase_1a_active",
            "dependency-policy.yml": "active_phase_1a_local_research",
            "privacy-policy.yml": "active_phase_1a_synthetic_data_only",
            "protected-paths.yml": "active_phase_1a_local_only",
            "release-policy.yml": "active_phase_1a_local_only",
        }
        for name, status in expected_status.items():
            if self.documents[name].get("status") != status:
                raise PolicyViolation(f"Phase 1A policy is not active: {name}")
        budgets = self.documents["budgets.yml"]["active_limits"]
        required_zero = (
            "money_usd",
            "model_tokens",
            "model_input_tokens",
            "model_output_tokens",
            "paid_provider_calls",
            "protected_evaluation_queries",
            "physical_canaries",
        )
        if any(int(budgets.get(name, -1)) != 0 for name in required_zero):
            raise PolicyViolation("Phase 1A external-effect budgets must remain zero")
        if int(budgets.get("wip_experiments", 0)) != 1:
            raise PolicyViolation(
                "Phase 1A requires exactly one experiment in progress"
            )
        release = self.documents["release-policy.yml"]["current_authority"]
        if release != {
            "build": "local_only",
            "publish": "disabled",
            "merge": "disabled",
            "deploy_simulation": "disabled_not_authorized_phase_1a",
            "deploy_physical": "disabled",
        }:
            raise PolicyViolation("release authority exceeds Phase 1A")
        registry_schema = self.documents["release-policy.yml"].get("registry_schema")
        if registry_schema != {
            "monotonic_only": True,
            "current": 3,
            "minimum_controller_compatible": 3,
            "rollback_to_older_schema": "forbidden",
            "forward_migration_requires": "empty_drained_registry",
        }:
            raise PolicyViolation("registry schema policy is not fail-closed")

    def budget_caps(self) -> dict[str, int]:
        active = self.documents["budgets.yml"]["active_limits"]
        wall_cap = int(active["wall_clock_hours"]) * 60 * 60 * 1000
        return {
            "wall_ms": wall_cap,
            "controller_runtime_ms": wall_cap,
            "storage_bytes": int(active["storage_mb"]) * 1024 * 1024,
            "attempts": 64,
            "model_tokens": int(active["model_tokens"]),
            "provider_calls": int(active["paid_provider_calls"]),
            "wip_experiments": int(active["wip_experiments"]),
        }

    def storage_cap_bytes(self) -> int:
        return (
            int(self.documents["budgets.yml"]["active_limits"]["storage_mb"])
            * 1024
            * 1024
        )

    def assert_synthetic_observation(self, value: dict[str, Any]) -> None:
        if (
            value.get("source") != "synthetic_fixture"
            or value.get("privacy_class") != "synthetic"
        ):
            raise PolicyViolation("Phase 1A accepts synthetic observations only")

    def assert_effect(self, effect: str) -> None:
        allowed = {
            "local_issue_manifest",
            "local_preregistration",
            "local_design",
            "local_candidate_commit",
            "local_fixture_evaluation",
            "local_review_attestations",
            "local_pull_request_manifest",
        }
        if effect not in allowed:
            raise PolicyViolation(f"effect is not authorized in Phase 1A: {effect}")

    def assert_fixture_changes(self, paths: list[str]) -> None:
        if not paths:
            raise PolicyViolation("candidate produced no change")
        allowed = {"src/behavior.py"}
        normalized: set[str] = set()
        for raw in paths:
            path = PurePosixPath(raw)
            if path.is_absolute() or ".." in path.parts or ".git" in path.parts:
                raise PolicyViolation(f"unsafe candidate path: {raw}")
            normalized.add(path.as_posix())
        if normalized != allowed:
            raise PolicyViolation(
                f"candidate changed paths outside the frozen scope: {sorted(normalized)}"
            )

    def candidate_environment(self, temporary_directory: Path) -> dict[str, str]:
        return {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": str(temporary_directory / "home"),
            "TMPDIR": str(temporary_directory / "tmp"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_ALLOW_PROTOCOL": "",
        }

    def assert_reviews(self, reviews: list[dict[str, Any]]) -> None:
        if len(reviews) < 2:
            raise PolicyViolation("two separated review identities are required")
        identities = {review.get("reviewer_identity") for review in reviews}
        if None in identities or len(identities) != len(reviews):
            raise PolicyViolation("review identities must be present and distinct")
        verdicts = {review.get("verdict") for review in reviews}
        if verdicts != {"approve"}:
            raise PolicyViolation("review disagreement or rejection requires a pause")
        decisive = [review for review in reviews if review.get("decisive") is True]
        if len(decisive) != 1 or decisive[0].get("role") != "verification_engineer":
            raise PolicyViolation("exactly one verification review must be decisive")
