"""Clean reconstruction checks for deterministic MiOS campaigns."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .campaign import run_replay_campaign
from .canonical import digest_json


@dataclass(frozen=True)
class ReconstructionReport:
    campaign_id: str
    reconstructions: int
    evidence_digest: str
    identical: bool


def reconstruct_campaign_twice(root: str | Path) -> ReconstructionReport:
    root = Path(root)
    summaries: list[dict[str, object]] = []
    for index in (1, 2):
        result = run_replay_campaign(root / f"run-{index}" / "state.sqlite")
        summaries.append(
            {
                "roles": [handoff.role for handoff in result.handoffs],
                "statuses": [handoff.status for handoff in result.handoffs],
                "release": result.release.verdict,
            }
        )
    digest = digest_json(summaries[0])
    return ReconstructionReport(
        "MIOS-CAMPAIGN-REPLAY-001",
        2,
        digest,
        summaries[0] == summaries[1],
    )
