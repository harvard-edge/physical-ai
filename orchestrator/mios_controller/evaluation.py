"""Protected evaluation runner with candidate-bound manifests."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class EvaluationManifest:
    evaluation_id: str
    candidate_digest: str
    protected_suite_digest: str
    checks: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationResult:
    evaluation_id: str
    candidate_digest: str
    passed: bool
    completed_checks: tuple[str, ...]
    failed_checks: tuple[str, ...]
    evidence_digest: str


Check = Callable[[str], bool]


class ProtectedEvaluationRunner:
    """Runs custodian-defined checks without exposing their implementation."""

    def __init__(self, protected_suite_digest: str, checks: dict[str, Check]) -> None:
        if not _sha256(protected_suite_digest):
            raise ValueError("protected suite must be content addressed")
        if not checks:
            raise ValueError("protected evaluation requires at least one check")
        self.protected_suite_digest = protected_suite_digest
        self._checks = dict(checks)

    def run(self, manifest: EvaluationManifest) -> EvaluationResult:
        if manifest.protected_suite_digest != self.protected_suite_digest:
            raise ValueError(
                "evaluation manifest references a different protected suite"
            )
        if not manifest.checks or any(
            check not in self._checks for check in manifest.checks
        ):
            raise ValueError("manifest contains unknown or empty checks")
        completed: list[str] = []
        failed: list[str] = []
        for name in manifest.checks:
            if self._checks[name](manifest.candidate_digest):
                completed.append(name)
            else:
                failed.append(name)
        evidence = _evidence_digest(manifest, completed, failed)
        return EvaluationResult(
            manifest.evaluation_id,
            manifest.candidate_digest,
            not failed,
            tuple(completed),
            tuple(failed),
            evidence,
        )


def _sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def _evidence_digest(
    manifest: EvaluationManifest, completed: Iterable[str], failed: Iterable[str]
) -> str:
    payload = "|".join(
        (manifest.evaluation_id, manifest.candidate_digest, *completed, "FAIL", *failed)
    )
    return hashlib.sha256(payload.encode()).hexdigest()
