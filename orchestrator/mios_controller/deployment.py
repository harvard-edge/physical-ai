"""Local staged release and rollback boundary for MiOS candidates."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Callable, Literal


@dataclass(frozen=True)
class ReleaseManifest:
    release_id: str
    artifact_digest: str
    source_experiment: str
    rollback_release: str
    signature: str


@dataclass(frozen=True)
class DeploymentResult:
    release_id: str
    slot: Literal["A", "B"]
    status: Literal["STAGED", "PROMOTED", "ROLLED_BACK"]
    active_release: str
    reason: str


HealthCheck = Callable[[ReleaseManifest], bool]


class LocalDeploymentController:
    """Two-slot release controller; physical installation is deliberately absent."""

    def __init__(self, initial_release: str) -> None:
        if not initial_release:
            raise ValueError("an initial known-good release is required")
        self.active_release = initial_release
        self.slots: dict[str, str] = {"A": initial_release, "B": ""}
        self.history: list[DeploymentResult] = []

    def stage(
        self, manifest: ReleaseManifest, health_check: HealthCheck
    ) -> DeploymentResult:
        _validate_manifest(manifest)
        inactive = "B" if self.slots["A"] == self.active_release else "A"
        self.slots[inactive] = manifest.release_id
        result = DeploymentResult(
            manifest.release_id,
            inactive,
            "STAGED",
            self.active_release,
            "artifact staged",
        )
        self.history.append(result)
        if health_check(manifest):
            self.active_release = manifest.release_id
            promoted = DeploymentResult(
                manifest.release_id,
                inactive,
                "PROMOTED",
                self.active_release,
                "health checks passed",
            )
            self.history.append(promoted)
            return promoted
        self.slots[inactive] = manifest.rollback_release
        rolled_back = DeploymentResult(
            manifest.release_id,
            inactive,
            "ROLLED_BACK",
            self.active_release,
            "health checks failed",
        )
        self.history.append(rolled_back)
        return rolled_back


def sign_manifest(
    release_id: str,
    artifact_digest: str,
    source_experiment: str,
    rollback_release: str,
    signing_material: str,
) -> ReleaseManifest:
    payload = "|".join(
        (
            release_id,
            artifact_digest,
            source_experiment,
            rollback_release,
            signing_material,
        )
    )
    return ReleaseManifest(
        release_id,
        artifact_digest,
        source_experiment,
        rollback_release,
        hashlib.sha256(payload.encode()).hexdigest(),
    )


def _validate_manifest(manifest: ReleaseManifest) -> None:
    for value in (manifest.artifact_digest, manifest.signature):
        if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise ValueError("release manifest contains an invalid digest")
    if not manifest.rollback_release:
        raise ValueError("release manifest requires a rollback target")
