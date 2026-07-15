"""Replayable synthetic council campaign used before model or robot authority."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .assurance import AssuranceVerdict, ReleaseDecision, decide_release
from .council import (
    CouncilCoordinator,
    CouncilStore,
    CouncilTask,
    Handoff,
)
from .council_workers import deterministic_workers


@dataclass(frozen=True)
class ReplayCampaignResult:
    campaign_id: str
    handoffs: tuple[Handoff, ...]
    release: ReleaseDecision


def run_replay_campaign(
    path: str | Path, *, campaign_id: str = "MIOS-CAMPAIGN-REPLAY-001"
) -> ReplayCampaignResult:
    """Run a fixed design/build/verify campaign entirely offline."""
    store = CouncilStore(path)
    coordinator = CouncilCoordinator(store)
    for role, worker in deterministic_workers().items():
        coordinator.register(role, worker)

    architect = f"{campaign_id}-ARCH"
    implementer = f"{campaign_id}-IMPL"
    verifier = f"{campaign_id}-VERIFY"
    store.enqueue(
        CouncilTask(architect, "architect", "Design a bounded memory improvement")
    )
    store.enqueue(
        CouncilTask(
            implementer,
            "implementer",
            "Implement the accepted design",
            depends_on=(architect,),
        )
    )
    store.enqueue(
        CouncilTask(
            verifier, "verifier", "Verify the candidate", depends_on=(implementer,)
        )
    )
    handoffs = tuple(
        coordinator.run_until_idle(
            ("architect", "implementer", "verifier"), max_steps=8
        )
    )
    candidate_digest = "a" * 64
    reports = (
        AssuranceVerdict(
            "qa-auditor", candidate_digest, "approve", evidence=("artifact://qa",)
        ),
        AssuranceVerdict(
            "safety-auditor",
            candidate_digest,
            "approve",
            evidence=("artifact://safety",),
        ),
    )
    release = decide_release(
        candidate_digest,
        reports,
        required_auditors=frozenset({"qa-auditor", "safety-auditor"}),
    )
    if release.verdict != "approved":
        raise RuntimeError(f"replay campaign failed release gate: {release.reasons}")
    return ReplayCampaignResult(campaign_id, handoffs, release)
