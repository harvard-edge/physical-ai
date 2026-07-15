"""MiOS domain engine used by the durable workflow adapter."""

from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .artifacts import ArtifactStore
from .canonical import atomic_write, canonical_bytes, digest_json, sha256_bytes
from .domain import (
    BudgetViolation,
    ExperimentState,
    IntegrityViolation,
    NEXT_STATE,
    ObservationInput,
    ReviewAttestation,
)
from .experiment import ExperimentRecord
from .forge import LocalForge
from .ledger import Ledger
from .policy import PolicyEngine
from .registry import SCHEMA_VERSION, Lease, Registry
from .sandbox import PINNED_IMAGE, SandboxRunner


CONTROLLER_RELEASE_VERSION = "0.1.0"
# This version changes only when an evolution workflow can no longer replay the
# history produced by the previous compatibility line. Ordinary package
# releases stay on the same value and use DBOS.patch sites for safe additions.
WORKFLOW_COMPATIBILITY_VERSION = "1"
# Retain the old name for callers that report the package version.
CONTROLLER_VERSION = CONTROLLER_RELEASE_VERSION


@dataclass(frozen=True)
class ControllerPaths:
    root: Path
    registry: Path
    artifacts: Path
    ledger: Path
    trusted_head: Path
    forge: Path
    workspaces: Path
    evidence: Path
    metadata: Path
    stop_file: Path
    dbos_database: Path

    @classmethod
    def create(cls, root: Path) -> "ControllerPaths":
        root = root.resolve()
        return cls(
            root=root,
            registry=root / "registry" / "mios.sqlite3",
            artifacts=root / "artifacts" / "sha256",
            ledger=root / "ledger" / "evolution.jsonl",
            trusted_head=root / "assurance" / "ledger-head.json",
            forge=root / "forge",
            workspaces=root / "workspaces",
            evidence=root / "evidence",
            metadata=root / "metadata",
            stop_file=root / "STOP",
            dbos_database=root / "checkpoints" / "dbos.sqlite3",
        )


def tree_digest(root: Path) -> str:
    entries: list[dict[str, Any]] = []
    if not root.exists():
        return digest_json(entries)
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if any(
            part in {"__pycache__", ".pytest_cache", "assets/cache"}
            for part in path.parts
        ):
            continue
        if path.is_symlink():
            entries.append(
                {"path": relative, "type": "symlink", "target": os.readlink(path)}
            )
        elif path.is_file() and path.suffix != ".pyc":
            entries.append(
                {
                    "path": relative,
                    "type": "file",
                    "sha256": sha256_bytes(path.read_bytes()),
                }
            )
    return digest_json(entries)


def directory_bytes(root: Path) -> int:
    total = 0
    if root.exists():
        for path in root.rglob("*"):
            try:
                if path.is_file() and not path.is_symlink():
                    total += path.stat().st_size
            except FileNotFoundError:
                continue
    return total


def path_digest(path: Path) -> str:
    if not path.exists() or not path.is_file() or path.is_symlink():
        return digest_json({"missing": path.name})
    return sha256_bytes(path.read_bytes())


class EvolutionEngine:
    def __init__(
        self,
        controller_root: Path,
        repository_root: Path,
        allow_cooperative: bool = False,
    ):
        self.repository_root = repository_root.resolve()
        self.paths = ControllerPaths.create(controller_root)
        self.policy = PolicyEngine(self.repository_root)
        self.registry = Registry(self.paths.registry)
        self.artifacts = ArtifactStore(self.paths.artifacts)
        self.ledger = Ledger(self.paths.ledger, self.paths.trusted_head)
        self.forge = LocalForge(self.paths.forge)
        self.sandbox = SandboxRunner(
            self.repository_root,
            self.policy,
            allow_cooperative=allow_cooperative,
            stop_path=self.paths.stop_file,
        )

    def _execution_critical_digests(self) -> dict[str, str]:
        return {
            "reachy_code_tree": tree_digest(self.repository_root / "code"),
            "controller_tree": tree_digest(
                self.repository_root / "orchestrator" / "mios_controller"
            ),
            "fixture_tree": tree_digest(
                self.repository_root / "evolution" / "fixtures"
            ),
            "protocol_tree": tree_digest(self.repository_root / "protocol"),
            "dependency_lock": path_digest(
                self.repository_root / "orchestrator" / "uv.lock"
            ),
            "phase_approval": path_digest(
                self.repository_root / "evolution" / "approvals" / "PHASE-1A.yml"
            ),
        }

    def _assert_storage_budget(self, reserved_headroom: int = 0) -> int:
        used = directory_bytes(self.paths.root)
        cap = self.policy.storage_cap_bytes()
        if used + reserved_headroom > cap:
            raise BudgetViolation(
                f"controller storage budget exhausted: {used}+{reserved_headroom}>{cap}"
            )
        return used

    def _assert_execution_integrity(self) -> dict[str, Any]:
        path = self.paths.metadata / "run-manifest.json"
        if not path.is_file() or path.is_symlink():
            raise IntegrityViolation("current release manifest is missing or unsafe")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        history_path = (
            self.paths.metadata / "releases" / f"{digest_json(manifest)}.json"
        )
        if not history_path.is_file() or history_path.is_symlink():
            raise IntegrityViolation(
                "current release manifest has no immutable history"
            )
        if json.loads(history_path.read_text(encoding="utf-8")) != manifest:
            raise IntegrityViolation("current release manifest history diverged")
        expected = self._execution_critical_digests()
        if manifest.get("execution_critical_digests") != expected:
            raise IntegrityViolation("execution-critical controller inputs changed")
        if manifest.get("policy_digest") != self.policy.digest:
            raise IntegrityViolation("policy changed since controller initialization")
        if manifest.get("sandbox_image") != PINNED_IMAGE:
            raise IntegrityViolation("sandbox image authority changed")
        if manifest.get("registry_schema") != {
            "current": SCHEMA_VERSION,
            "minimum": SCHEMA_VERSION,
            "maximum": SCHEMA_VERSION,
        }:
            raise IntegrityViolation("registry schema compatibility changed")
        return manifest

    def initialize(self) -> dict[str, Any]:
        self.policy.assert_campaign_active()
        self.paths.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._assert_storage_budget()
        for path in (
            self.paths.artifacts,
            self.paths.forge,
            self.paths.workspaces,
            self.paths.evidence,
            self.paths.metadata,
            self.paths.dbos_database.parent,
        ):
            path.mkdir(parents=True, exist_ok=True)
        approval_digest = path_digest(
            self.repository_root / "evolution" / "approvals" / "PHASE-1A.yml"
        )
        self.registry.initialize(
            "MIOS-CAMPAIGN-001",
            self.policy.digest,
            self.policy.budget_caps(),
            approval_digest=approval_digest,
        )
        run_manifest = {
            "schema_version": "1.0.0",
            "campaign_id": "MIOS-CAMPAIGN-001",
            "controller_release_version": CONTROLLER_RELEASE_VERSION,
            "workflow_compatibility_version": WORKFLOW_COMPATIBILITY_VERSION,
            "registry_schema": {
                "current": SCHEMA_VERSION,
                "minimum": SCHEMA_VERSION,
                "maximum": SCHEMA_VERSION,
            },
            "policy_digest": self.policy.digest,
            "execution_critical_digests": self._execution_critical_digests(),
            "workflow_substrate": {"name": "dbos", "version": "2.26.0"},
            "sandbox_image": PINNED_IMAGE,
            "authority": {
                "models": False,
                "network_workers": False,
                "github": False,
                "robot": False,
                "physical_deployment": False,
            },
        }
        path = self.paths.metadata / "run-manifest.json"
        existing = (
            json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        )
        if existing is not None:
            previous_compatibility = existing.get(
                "workflow_compatibility_version", "legacy-controller-version"
            )
            if previous_compatibility != WORKFLOW_COMPATIBILITY_VERSION:
                self._assert_workflow_upgrade_allowed(
                    str(previous_compatibility), WORKFLOW_COMPATIBILITY_VERSION
                )
            if existing != run_manifest:
                self._assert_release_activation_allowed(existing, run_manifest)

        # Manifests are immutable, content-addressed release records. The
        # current pointer may advance, but an older release description is
        # never overwritten or discarded.
        manifest_digest = digest_json(run_manifest)
        history_path = self.paths.metadata / "releases" / f"{manifest_digest}.json"
        if history_path.exists():
            recorded = json.loads(history_path.read_text(encoding="utf-8"))
            if recorded != run_manifest:
                raise IntegrityViolation("release manifest digest collision")
        else:
            atomic_write(history_path, canonical_bytes(run_manifest) + b"\n")
        if existing != run_manifest:
            atomic_write(path, canonical_bytes(run_manifest) + b"\n")
        campaign_event_id = "campaign:MIOS-CAMPAIGN-001:initialized"
        if not any(
            record["payload"].get("event_id") == campaign_event_id
            for record in self.ledger.verify()
        ):
            self.ledger.append_once(
                campaign_event_id,
                "campaign_initialized",
                {
                    "run_manifest_digest": digest_json(run_manifest),
                    "policy_digest": self.policy.digest,
                },
            )
        self._assert_storage_budget()
        return run_manifest

    def _assert_release_activation_allowed(
        self, previous: dict[str, Any], candidate: dict[str, Any]
    ) -> None:
        """Prevent restart from silently blessing changed execution inputs."""

        experiments = self.registry.export()["experiments"]
        if not experiments:
            return
        changed_fields = {
            key
            for key in set(previous) | set(candidate)
            if previous.get(key) != candidate.get(key)
        }
        if changed_fields == {"workflow_compatibility_version"}:
            # The workflow-specific migration record is validated separately.
            return
        activation_path = self.paths.metadata / "release-activation.json"
        if activation_path.is_file() and not activation_path.is_symlink():
            activation = json.loads(activation_path.read_text(encoding="utf-8"))
            expected = {
                "schema_version": "1.0.0",
                "mode": "release_activation",
                "status": "completed",
                "from_manifest_digest": digest_json(previous),
                "to_manifest_digest": digest_json(candidate),
                "policy_digest": self.policy.digest,
                "approval_digest": path_digest(
                    self.repository_root / "evolution" / "approvals" / "PHASE-1A.yml"
                ),
            }
            if activation == expected:
                return
        raise IntegrityViolation(
            "execution release changed after experiment creation without an exact "
            "policy-bound release activation"
        )

    def _assert_workflow_upgrade_allowed(
        self, previous_version: str, next_version: str
    ) -> None:
        """Fail closed until every old-version workflow and intent is drained."""
        registry = self.registry.export()
        settings = {item["key"]: item["value"] for item in registry["settings"]}
        active = [
            item["id"]
            for item in registry["experiments"]
            if item["state"]
            not in {
                ExperimentState.LOCAL_CANDIDATE_READY.value,
                ExperimentState.REJECTED.value,
            }
        ]
        prepared_intents = [
            item["idempotency_key"]
            for item in registry["effect_intents"]
            if item["status"] != "completed"
        ]
        active_workflows = self._active_dbos_workflows()
        controller_drained = (
            settings.get("controller_state") == "PAUSED"
            and settings.get("accept_new_work") == "false"
        )
        if (
            controller_drained
            and not active
            and not prepared_intents
            and not active_workflows
        ):
            return
        raise IntegrityViolation(
            "workflow compatibility changed before the old line was drained; "
            f"active experiments: {active}; prepared intents: {prepared_intents}; "
            f"active DBOS workflows: {active_workflows}; "
            f"controller drained: {controller_drained}; "
            f"requested change: {previous_version}->{next_version}"
        )

    def _active_dbos_workflows(self) -> list[dict[str, str]]:
        database = self.paths.dbos_database
        if not database.exists():
            return []
        with sqlite3.connect(
            f"file:{database}?mode=ro", uri=True, timeout=5
        ) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA busy_timeout = 5000")
            table = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='workflow_status'"
            ).fetchone()
            if table is None:
                raise IntegrityViolation("DBOS checkpoint database has no status table")
            terminal = {
                "SUCCESS",
                "ERROR",
                "CANCELLED",
                "MAX_RECOVERY_ATTEMPTS_EXCEEDED",
            }
            return [
                {
                    "workflow_uuid": str(row["workflow_uuid"]),
                    "status": str(row["status"]),
                    "application_version": str(row["application_version"]),
                }
                for row in connection.execute(
                    """
                    SELECT workflow_uuid, status, application_version
                    FROM workflow_status ORDER BY workflow_uuid
                    """
                )
                if row["status"] not in terminal
            ]

    def ingest_file(self, path: Path) -> tuple[str, bool]:
        self.policy.assert_campaign_active()
        self._assert_storage_budget(reserved_headroom=1024 * 1024)
        value = json.loads(path.read_text(encoding="utf-8"))
        self.policy.assert_synthetic_observation(value)
        observation = ObservationInput.model_validate(value)
        reference = self.artifacts.put_json(
            observation.observation_id, observation.model_dump(mode="json")
        )
        experiment_id, created = self.registry.ingest(observation)
        if created:
            self.ledger.append_once(
                f"observation:{observation.observation_id}:ingested",
                "observation_ingested",
                {
                    "experiment_id": experiment_id,
                    "observation_id": observation.observation_id,
                    "artifact_digest": reference.sha256,
                    "privacy_class": observation.privacy_class,
                },
            )
        self._assert_storage_budget()
        return experiment_id, created

    def run_transition(
        self, experiment_id: str, expected_from: ExperimentState
    ) -> dict[str, Any]:
        self.policy.assert_campaign_active()
        self._assert_execution_integrity()
        self._assert_storage_budget(reserved_headroom=16 * 1024 * 1024)
        if self.paths.stop_file.exists():
            self.registry.pause("persistent kill switch is present")
            raise RuntimeError("persistent kill switch is present")
        to_state = NEXT_STATE[expected_from]
        experiment = self.registry.get_experiment(experiment_id)
        if experiment["state"] != expected_from.value:
            completed = self.registry.transition_to(experiment_id, to_state)
            if completed:
                return self._reconcile_completed(completed)
            raise RuntimeError(
                f"workflow and registry disagree: expected {expected_from.value}, found {experiment['state']}"
            )
        lease = self.registry.claim_transition(
            experiment_id=experiment_id,
            from_state=expected_from,
            to_state=to_state,
            worker_id="dbos-local-worker",
            config_digest=self.policy.digest,
            lease_seconds=120,
            budget_request={
                "wall_ms": 60_000,
                "storage_bytes": 16 * 1024 * 1024,
                "attempts": 1,
            },
        )
        self._maybe_inject_crash(expected_from, "after_claim_before_effect")
        started = time.monotonic_ns()
        bytes_before = directory_bytes(self.paths.root)
        effect_kind = self._effect_kind(to_state)
        self.policy.assert_effect(effect_kind)
        observation = self.registry.observation_for(experiment_id)
        action_implementation_digest = digest_json(
            {
                "schema_version": "1.0.0",
                "effect_kind": effect_kind,
                "controller_tree": tree_digest(
                    self.repository_root / "orchestrator" / "mios_controller"
                ),
                "fixture_tree": tree_digest(
                    self.repository_root / "evolution" / "fixtures"
                ),
                "protocol_tree": tree_digest(self.repository_root / "protocol"),
            }
        )
        input_digest = digest_json(
            {
                "experiment_id": experiment_id,
                "from_state": expected_from.value,
                "to_state": to_state.value,
                "observation_digest": observation["payload_digest"],
                "policy_digest": self.policy.digest,
                "action_implementation_digest": action_implementation_digest,
            }
        )
        try:
            self.registry.prepare_effect_intent(
                lease,
                effect_kind,
                action_implementation_digest,
                input_digest,
            )
            self._maybe_inject_crash(expected_from, "after_intent_before_action")
            action = self._action_for(to_state)
            evidence = action(experiment_id, observation, lease)
            self._maybe_inject_crash(expected_from, "after_effect_before_artifact")
            evidence_envelope = {
                "schema_version": "1.0.0",
                "experiment_id": experiment_id,
                "from_state": expected_from.value,
                "to_state": to_state.value,
                "effect": effect_kind,
                "input_digest": input_digest,
                "action_implementation_digest": action_implementation_digest,
                "evidence": evidence,
            }
            reference = self.artifacts.put_json(
                f"{experiment_id}-{to_state.value.lower()}", evidence_envelope
            )
            self._maybe_inject_crash(expected_from, "after_artifact_before_registry")
            self._assert_storage_budget()
            wall_ms = max(1, (time.monotonic_ns() - started) // 1_000_000)
            storage_growth = max(0, directory_bytes(self.paths.root) - bytes_before)
            self.registry.complete_transition(
                lease,
                effect_kind=effect_kind,
                effect_input_digest=input_digest,
                evidence_digest=reference.sha256,
                actual_budget={
                    "wall_ms": wall_ms,
                    "storage_bytes": storage_growth,
                    "attempts": 1,
                },
            )
            self._maybe_inject_crash(expected_from, "after_registry_before_ledger")
            self._append_transition_ledger(
                experiment_id,
                expected_from.value,
                to_state.value,
                reference.sha256,
                lease.fencing_token,
            )
            self._maybe_inject_crash(expected_from, "after_ledger_before_checkpoint")
            if to_state == ExperimentState.LOCAL_CANDIDATE_READY:
                self.write_semantic_summary(experiment_id)
            return evidence_envelope
        except BaseException as error:
            try:
                self.registry.fail_attempt(lease, error, retryable=False)
                self.registry.pause(f"{type(error).__name__}: {error}")
            except BaseException:
                self.registry.pause(
                    f"cleanup failure after {type(error).__name__}: {error}",
                    incident=True,
                )
            raise

    def _maybe_inject_crash(self, state: ExperimentState, point: str) -> None:
        if os.environ.get("MIOS_ENABLE_CRASH_INJECTION") != "1":
            return
        if os.environ.get("MIOS_TEST_CRASH_TRANSITION") != state.value:
            return
        if os.environ.get("MIOS_TEST_CRASH_POINT") != point:
            return
        marker = self.paths.metadata / f"crashed-{state.value}-{point}"
        if marker.exists():
            return
        atomic_write(marker, b"injected crash\n")
        os._exit(77)

    def _reconcile_completed(self, transition: dict[str, Any]) -> dict[str, Any]:
        self.artifacts.read_verified(transition["evidence_digest"])
        self._append_transition_ledger(
            transition["experiment_id"],
            transition["from_state"],
            transition["to_state"],
            transition["evidence_digest"],
            transition["fencing_token"],
        )
        if transition["to_state"] == ExperimentState.LOCAL_CANDIDATE_READY.value:
            self.write_semantic_summary(transition["experiment_id"])
        return json.loads(self.artifacts.read_verified(transition["evidence_digest"]))

    def _append_transition_ledger(
        self,
        experiment_id: str,
        from_state: str,
        to_state: str,
        evidence_digest: str,
        fencing_token: int,
    ) -> None:
        self.ledger.append_once(
            f"transition:{experiment_id}:{to_state}",
            "experiment_transition",
            {
                "experiment_id": experiment_id,
                "from_state": from_state,
                "to_state": to_state,
                "evidence_digest": evidence_digest,
                "fencing_token": fencing_token,
            },
        )
        if to_state == ExperimentState.LOCAL_CANDIDATE_READY.value:
            settings = {
                row["key"]: row["value"] for row in self.registry.export()["settings"]
            }
            observation = self.registry.observation_for(experiment_id)
            experiment = ExperimentRecord(
                experiment_id=experiment_id,
                campaign_id=settings["campaign_id"],
                autonomy_level_claimed="A1",
                trigger={
                    "observation_ids": [observation["id"]],
                    "detected_by": "runtime-monitor",
                    "privacy_class": "synthetic",
                },
                hypothesis={
                    "statement": "The bounded candidate passes the frozen fixture evaluation",
                    "expected_mechanism": "The authorized candidate changes only the observed behavior",
                },
                baseline={
                    "release": "phase-1a-baseline",
                    "comparison_condition": "fixed_single_agent",
                },
                preregistration={
                    "artifact_hash": evidence_digest,
                    "frozen_at": observation["created_at"],
                    "primary_metric": "frozen_acceptance_test_pass",
                    "minimum_effect": 0.0,
                    "sample_size": 1,
                },
                selected_design="deterministic fixture transition workflow",
                evaluation={
                    "public_suite": "behavior-value",
                    "simulation_result": "pass",
                    "evaluator_version": "phase-1a",
                },
                change={"commits": []},
                review={
                    "architecture": "approve",
                    "safety": "approve",
                    "verification": "approve",
                },
                deployment={},
                outcome={
                    "decision": "accepted",
                    "measured_delta": {"final_state": to_state},
                    "autonomy_level_supported": "A1",
                },
                lesson={
                    "supported_claims": ["the local transition is replayable"],
                    "rejected_claims": [
                        "the synthetic fixture proves embodied capability"
                    ],
                    "next_questions": ["Can this evidence be reproduced on Reachy?"],
                },
            )
            self.ledger.append_experiment_record(experiment)

    @staticmethod
    def _effect_kind(to_state: ExperimentState) -> str:
        return {
            ExperimentState.TRIAGED: "local_issue_manifest",
            ExperimentState.PREREGISTERED: "local_preregistration",
            ExperimentState.DESIGNED: "local_design",
            ExperimentState.IMPLEMENTING: "local_candidate_commit",
            ExperimentState.EVALUATING: "local_fixture_evaluation",
            ExperimentState.REVIEWING: "local_review_attestations",
            ExperimentState.LOCAL_CANDIDATE_READY: "local_pull_request_manifest",
        }[to_state]

    def _action_for(
        self, to_state: ExperimentState
    ) -> Callable[[str, dict[str, Any], Lease], dict[str, Any]]:
        return {
            ExperimentState.TRIAGED: self._triage,
            ExperimentState.PREREGISTERED: self._preregister,
            ExperimentState.DESIGNED: self._design,
            ExperimentState.IMPLEMENTING: self._implement,
            ExperimentState.EVALUATING: self._evaluate,
            ExperimentState.REVIEWING: self._review,
            ExperimentState.LOCAL_CANDIDATE_READY: self._ready,
        }[to_state]

    def _triage(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        manifest = {
            "schema_version": "1.0.0",
            "issue_id": f"LOCAL-{experiment_id}",
            "experiment_id": experiment_id,
            "observation_id": observation["id"],
            "observation_digest": observation["payload_digest"],
            "classification": "deterministic_fixture_defect",
            "summary": observation["payload"]["summary"],
            "publication": "local_only",
        }
        self.forge.write(experiment_id, "issue", manifest)
        return manifest

    def _preregister(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        acceptance = (
            self.repository_root
            / "evolution"
            / "fixtures"
            / "behavior-value"
            / "base"
            / "tests"
            / "test_acceptance.py"
        )
        return {
            "schema_version": "1.0.0",
            "experiment_id": experiment_id,
            "hypothesis": "Changing only src/behavior.py from the observed value to the expected value will pass the frozen acceptance test.",
            "expected_mechanism": "current_value returns the preregistered expected literal",
            "primary_metric": "frozen_acceptance_test_pass",
            "acceptance_rule": "exit_code_equals_zero",
            "acceptance_test_sha256": sha256_bytes(acceptance.read_bytes()),
            "allowed_change": ["src/behavior.py"],
            "alternatives": ["do_nothing", "change_acceptance_test"],
            "rejected_alternatives": ["change_acceptance_test"],
        }

    def _design(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "experiment_id": experiment_id,
            "selected_design": "replace the obsolete return value in the single authorized source file",
            "write_scope": ["src/behavior.py"],
            "protected_scope": [
                "tests/**",
                ".git/**",
                "governance/**",
                "controller_state/**",
            ],
            "worker": "deterministic_fixture_v1",
            "sandbox_required": "container",
            "network": False,
            "external_services": [],
            "rollback": "reset the disposable fixture to its deterministic base commit",
        }

    def _implement(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        workspace = self.paths.workspaces / experiment_id / "repository"
        base_commit = self.sandbox.prepare_workspace(workspace)
        behavior = workspace / "src" / "behavior.py"
        protocol_evidence_path = workspace.parent / "protocol-evidence.json"
        if 'return "new"' in behavior.read_text(encoding="utf-8"):
            changed = self.sandbox.changed_paths(workspace)
            candidate_commit = (
                self.sandbox.commit_candidate(workspace, experiment_id)
                if changed
                else self.sandbox.git_commit(workspace)
            )
            if not protocol_evidence_path.is_file():
                raise IntegrityViolation(
                    "candidate effect exists without agent protocol evidence"
                )
            sandbox_evidence = json.loads(
                protocol_evidence_path.read_text(encoding="utf-8")
            )
        else:
            sandbox_evidence = self.sandbox.apply_candidate(
                workspace, experiment_id, lease.attempt_id
            )
            atomic_write(
                protocol_evidence_path,
                canonical_bytes(sandbox_evidence) + b"\n",
            )
            candidate_commit = self.sandbox.commit_candidate(workspace, experiment_id)
        candidate_source = self.artifacts.put_file(
            f"{experiment_id}-candidate-source",
            workspace / "src" / "behavior.py",
            "text/x-python",
        )
        return {
            "schema_version": "1.0.0",
            "experiment_id": experiment_id,
            "workspace_class": "disposable_synthetic_fixture",
            "base_commit": base_commit,
            "candidate_commit": candidate_commit,
            "candidate_source_artifact": candidate_source.model_dump(mode="json"),
            "changed_paths": ["src/behavior.py"],
            "sandbox": sandbox_evidence,
            "real_repository_write": False,
        }

    def _evaluate(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        workspace = self.paths.workspaces / experiment_id / "repository"
        result = self.sandbox.evaluate(workspace)
        if not result["passed"]:
            raise RuntimeError("frozen fixture acceptance test failed")
        return {
            "schema_version": "1.0.0",
            "experiment_id": experiment_id,
            "candidate_commit": self.sandbox.git_commit(workspace),
            "checks": [
                {
                    "id": "frozen_acceptance_test",
                    "status": "passed",
                    "test_sha256": sha256_bytes(
                        (workspace / "tests" / "test_acceptance.py").read_bytes()
                    ),
                }
            ],
            "execution": result,
            "protected_evaluation_queries": 0,
        }

    def _review(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        workspace = self.paths.workspaces / experiment_id / "repository"
        candidate_commit = self.sandbox.git_commit(workspace)
        review_view_path = self.paths.forge / experiment_id / "reviews.json"
        if review_view_path.is_file() and not review_view_path.is_symlink():
            review_evidence = json.loads(review_view_path.read_text(encoding="utf-8"))
            if (
                review_evidence.get("experiment_id") != experiment_id
                or review_evidence.get("candidate_commit") != candidate_commit
                or review_evidence.get("review_set_digest")
                != digest_json(review_evidence.get("reviews", []))
                or review_evidence.get("review_execution_digest")
                != digest_json(review_evidence.get("review_executions", []))
            ):
                raise IntegrityViolation(
                    "durable review reconciliation view is invalid"
                )
            self.policy.assert_reviews(review_evidence["reviews"])
            for execution in review_evidence["review_executions"]:
                validated = self.sandbox.protocol.validate_review_result(
                    execution["task"], execution["result"]
                )
                if (
                    execution.get("task_digest") != validated["task_digest"]
                    or execution.get("result_digest") != validated["result_digest"]
                    or execution.get("reviewer_identity")
                    != validated["reviewer_identity"]
                ):
                    raise IntegrityViolation(
                        "durable reviewer execution failed reconciliation"
                    )
            self.registry.add_reviews(review_evidence["reviews"])
            return review_evidence
        implementation = self.registry.transition_to(
            experiment_id, ExperimentState.IMPLEMENTING
        )
        evaluation = self.registry.transition_to(
            experiment_id, ExperimentState.EVALUATING
        )
        if not implementation or not evaluation:
            raise RuntimeError("candidate or evaluation evidence is missing")
        implementation_envelope = json.loads(
            self.artifacts.read_verified(implementation["evidence_digest"])
        )
        evaluation_envelope = json.loads(
            self.artifacts.read_verified(evaluation["evidence_digest"])
        )
        review_executions = self.sandbox.run_reviews(
            workspace,
            experiment_id,
            lease.attempt_id,
            {
                "schema_version": "1.0.0",
                "candidate_commit": candidate_commit,
                "implementation_digest": implementation["evidence_digest"],
                "implementation": implementation_envelope["evidence"],
                "evaluation_digest": evaluation["evidence_digest"],
                "evaluation": evaluation_envelope["evidence"],
            },
        )
        reviews = []
        for execution in review_executions:
            role = str(execution["role"])
            reviews.append(
                ReviewAttestation(
                    experiment_id=experiment_id,
                    role=role,
                    reviewer_identity=str(execution["reviewer_identity"]),
                    candidate_commit=candidate_commit,
                    evidence_digest=str(execution["result_digest"]),
                    verdict="approve",
                    decisive=role == "verification_engineer",
                )
            )
        values = sorted(
            (review.model_dump(mode="json") for review in reviews),
            key=lambda review: review["role"],
        )
        self.policy.assert_reviews(values)
        review_evidence = {
            "schema_version": "1.0.0",
            "experiment_id": experiment_id,
            "candidate_commit": candidate_commit,
            "reviews": values,
            "review_set_digest": digest_json(values),
            "review_executions": review_executions,
            "review_execution_digest": digest_json(review_executions),
            "identity_separation": "separately sandboxed deterministic task identities",
            "model_independence": "not_applicable_no_models_phase_1a",
        }
        # The complete packet is written atomically before registry insertion.
        # A crash on either side can therefore reconcile the exact reviewer
        # identities and result digests instead of launching a divergent retry.
        self.forge.write(experiment_id, "reviews", review_evidence)
        self.registry.add_reviews(values)
        return review_evidence

    def _ready(
        self, experiment_id: str, observation: dict[str, Any], lease: Lease
    ) -> dict[str, Any]:
        workspace = self.paths.workspaces / experiment_id / "repository"
        transitions = {
            state.value: self.registry.transition_to(experiment_id, state)[
                "evidence_digest"
            ]
            for state in (
                ExperimentState.TRIAGED,
                ExperimentState.PREREGISTERED,
                ExperimentState.DESIGNED,
                ExperimentState.IMPLEMENTING,
                ExperimentState.EVALUATING,
                ExperimentState.REVIEWING,
            )
        }
        manifest = {
            "schema_version": "1.0.0",
            "pull_request_id": f"LOCAL-PR-{experiment_id}",
            "experiment_id": experiment_id,
            "candidate_commit": self.sandbox.git_commit(workspace),
            "evidence": transitions,
            "reviews": self.registry.reviews_for(experiment_id),
            "publication": "disabled",
            "merge": "disabled",
            "deployment": "disabled",
            "terminal_state": ExperimentState.LOCAL_CANDIDATE_READY.value,
        }
        self.forge.write(experiment_id, "pull-request", manifest)
        return manifest

    def write_semantic_summary(self, experiment_id: str) -> dict[str, Any]:
        registry = self.registry.export()
        experiment = self.registry.get_experiment(experiment_id)
        transitions = [
            {
                "from_state": row["from_state"],
                "to_state": row["to_state"],
            }
            for row in registry["transitions"]
            if row["experiment_id"] == experiment_id
        ]
        effects = [
            {
                "kind": row["kind"],
                "input_digest": row["input_digest"],
            }
            for row in registry["effects"]
            if row["experiment_id"] == experiment_id
        ]
        summary = {
            "schema_version": "1.0.0",
            "campaign_id": "MIOS-CAMPAIGN-001",
            "experiment_id": experiment_id,
            "terminal_state": experiment["state"],
            "workflow_substrate": "dbos-2.26.0",
            "transitions": transitions,
            "effects": effects,
            "review_roles": sorted(
                review["role"] for review in self.registry.reviews_for(experiment_id)
            ),
            "external_effect_counts": {
                "model_calls": 0,
                "network_worker_calls": 0,
                "github_publications": 0,
                "robot_calls": 0,
                "physical_deployments": 0,
            },
            "external_effect_counts_scope": (
                "configured MiOS adapters only; trusted controller OS egress is not confined"
            ),
            "authority_boundary": {
                "candidate_worker_network": "enforced_none",
                "candidate_worker_credentials": "enforced_stripped",
                "candidate_worker_repository_scope": "enforced_fixture_only",
                "trusted_controller_external_adapters": "absent_phase_1a",
                "trusted_controller_os_network_confinement": False,
            },
        }
        self.paths.evidence.mkdir(parents=True, exist_ok=True)
        atomic_write(
            self.paths.evidence / "semantic-summary.json",
            canonical_bytes(summary) + b"\n",
        )
        return summary

    def verify(self) -> dict[str, Any]:
        self.registry.integrity_check()
        artifacts = self.artifacts.verify_all()
        ledger = self.ledger.verify()
        exported = self.registry.export()
        artifact_set = set(artifacts)
        missing = [
            row["evidence_digest"]
            for row in exported["transitions"]
            if row["evidence_digest"] not in artifact_set
        ]
        if missing:
            raise IntegrityViolation(f"transition artifacts missing: {missing}")
        self._assert_execution_integrity()
        final_experiments = [
            experiment
            for experiment in exported["experiments"]
            if experiment["state"] == ExperimentState.LOCAL_CANDIDATE_READY.value
        ]
        for experiment in final_experiments:
            experiment_id = experiment["id"]
            transitions = [
                row
                for row in exported["transitions"]
                if row["experiment_id"] == experiment_id
            ]
            effects = [
                row
                for row in exported["effects"]
                if row["experiment_id"] == experiment_id
            ]
            intents = [
                row
                for row in exported["effect_intents"]
                if row["experiment_id"] == experiment_id
            ]
            reviews = self.registry.reviews_for(experiment_id)
            if (
                len(transitions) != 7
                or len(effects) != 7
                or len(intents) != 7
                or len(reviews) != 2
            ):
                raise IntegrityViolation(
                    f"incomplete final evidence for {experiment_id}"
                )
            if any(intent["status"] != "completed" for intent in intents):
                raise IntegrityViolation(
                    "final experiment has unresolved effect intents"
                )
            if len({review["reviewer_identity"] for review in reviews}) != 2:
                raise IntegrityViolation("review identities are not separated")
            if sum(int(review["decisive"]) for review in reviews) != 1:
                raise IntegrityViolation(
                    "exactly one synthetic review must be decisive"
                )
            evidence_by_state = {
                row["to_state"]: json.loads(
                    self.artifacts.read_verified(row["evidence_digest"])
                )
                for row in transitions
            }
            preregistered_test = evidence_by_state[ExperimentState.PREREGISTERED.value][
                "evidence"
            ]["acceptance_test_sha256"]
            evaluated_test = evidence_by_state[ExperimentState.EVALUATING.value][
                "evidence"
            ]["checks"][0]["test_sha256"]
            if preregistered_test != evaluated_test:
                raise IntegrityViolation("candidate changed the frozen acceptance test")
            if evidence_by_state[ExperimentState.IMPLEMENTING.value]["evidence"][
                "changed_paths"
            ] != ["src/behavior.py"]:
                raise IntegrityViolation("candidate changed paths outside its scope")
            implementation_evidence = evidence_by_state[
                ExperimentState.IMPLEMENTING.value
            ]["evidence"]
            candidate_source_reference = implementation_evidence.get(
                "candidate_source_artifact", {}
            )
            candidate_source_digest = candidate_source_reference.get("sha256")
            if candidate_source_digest not in artifact_set:
                raise IntegrityViolation("candidate source artifact is missing")
            candidate_source = self.artifacts.read_verified(candidate_source_digest)
            if candidate_source_reference != {
                "sha256": candidate_source_digest,
                "size": len(candidate_source),
                "media_type": "text/x-python",
                "logical_name": f"{experiment_id}-candidate-source",
            }:
                raise IntegrityViolation("candidate source artifact metadata diverged")
            protocol_evidence = implementation_evidence.get("sandbox", {}).get(
                "protocol", {}
            )
            validated_fixture = self.sandbox.protocol.validate_fixture_record(
                protocol_evidence.get("task", {}),
                protocol_evidence.get("result", {}),
                candidate_source,
            )
            if (
                protocol_evidence.get("task_digest") != validated_fixture["task_digest"]
                or protocol_evidence.get("result_digest")
                != validated_fixture["result_digest"]
            ):
                raise IntegrityViolation("candidate protocol evidence diverged")
            review_evidence = evidence_by_state[ExperimentState.REVIEWING.value][
                "evidence"
            ]
            review_executions = review_evidence.get("review_executions", [])
            if len(review_executions) != 2 or review_evidence.get(
                "review_execution_digest"
            ) != digest_json(review_executions):
                raise IntegrityViolation("independent review execution set is invalid")
            validated_review_results: dict[str, dict[str, Any]] = {}
            for execution in review_executions:
                task = execution.get("task")
                result = execution.get("result")
                if not isinstance(task, dict) or not isinstance(result, dict):
                    raise IntegrityViolation("independent review envelope is missing")
                validated = self.sandbox.protocol.validate_review_result(task, result)
                if (
                    execution.get("task_digest") != validated["task_digest"]
                    or execution.get("result_digest") != validated["result_digest"]
                    or execution.get("reviewer_identity")
                    != validated["reviewer_identity"]
                    or execution.get("role") != task.get("role")
                ):
                    raise IntegrityViolation(
                        "independent review execution metadata diverged"
                    )
                enforcement = execution.get("supervisor_enforcement", {})
                if (
                    execution.get("profile") != "container"
                    or execution.get("image") != PINNED_IMAGE
                    or execution.get("reviewer_sha256")
                    != path_digest(
                        self.repository_root
                        / "evolution"
                        / "fixtures"
                        / "behavior-value"
                        / "fixture_reviewer.py"
                    )
                    or enforcement.get("container_limits_enforced") is not True
                    or enforcement.get("wall_limit_ms") != task["budgets"]["wall_ms"]
                    or enforcement.get("memory_limit_bytes")
                    != task["budgets"]["memory_bytes"]
                    or enforcement.get("process_limit") != task["budgets"]["processes"]
                ):
                    raise IntegrityViolation(
                        "independent reviewer isolation evidence is invalid"
                    )
                validated_review_results[str(execution["role"])] = validated
            if set(validated_review_results) != {
                "verification_engineer",
                "research_skeptic",
            }:
                raise IntegrityViolation(
                    "required independent reviewer roles are missing"
                )
            registry_reviews = [
                {
                    **review,
                    "decisive": bool(review["decisive"]),
                }
                for review in reviews
            ]
            if review_evidence.get("review_set_digest") != digest_json(
                review_evidence.get("reviews", [])
            ):
                raise IntegrityViolation("review evidence set digest is invalid")
            evidence_reviews_for_registry = [
                {key: value for key, value in review.items() if key != "schema_version"}
                for review in review_evidence.get("reviews", [])
            ]
            if evidence_reviews_for_registry != registry_reviews:
                raise IntegrityViolation(
                    "registry reviews diverge from review evidence"
                )
            if any(
                review["evidence_digest"]
                != validated_review_results[review["role"]]["result_digest"]
                for review in registry_reviews
            ):
                raise IntegrityViolation(
                    "review attestation is not bound to its worker result"
                )
            reviews_path = self.paths.forge / experiment_id / "reviews.json"
            if not reviews_path.is_file() or reviews_path.is_symlink():
                raise IntegrityViolation("local review reconciliation view is missing")
            if json.loads(reviews_path.read_text(encoding="utf-8")) != review_evidence:
                raise IntegrityViolation(
                    "local review view does not match immutable evidence"
                )
            issue_path = self.paths.forge / experiment_id / "issue.json"
            if not issue_path.is_file():
                raise IntegrityViolation("local issue manifest is missing")
            if (
                json.loads(issue_path.read_text(encoding="utf-8"))
                != evidence_by_state[ExperimentState.TRIAGED.value]["evidence"]
            ):
                raise IntegrityViolation(
                    "local issue view does not match immutable evidence"
                )
            pull_request_path = self.paths.forge / experiment_id / "pull-request.json"
            if not pull_request_path.is_file():
                raise IntegrityViolation("local pull-request manifest is missing")
            if (
                json.loads(pull_request_path.read_text(encoding="utf-8"))
                != evidence_by_state[ExperimentState.LOCAL_CANDIDATE_READY.value][
                    "evidence"
                ]
            ):
                raise IntegrityViolation(
                    "local pull-request view does not match immutable evidence"
                )
        return {
            "registry": "ok",
            "artifact_count": len(artifacts),
            "ledger_records": len(ledger),
            "final_experiments": [item["id"] for item in final_experiments],
            "policy_digest": self.policy.digest,
            "reachy_code_unchanged": True,
        }
