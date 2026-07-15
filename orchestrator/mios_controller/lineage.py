"""Machine-checkable observation-to-deployment lineage reports."""

from __future__ import annotations

from dataclasses import dataclass

from .ledger import Ledger


@dataclass(frozen=True)
class LineageReport:
    experiment_id: str
    event_kinds: tuple[str, ...]
    observation_ids: tuple[str, ...]
    deployment_releases: tuple[str, ...]
    complete_local_lineage: bool


def inspect_lineage(ledger: Ledger, experiment_id: str) -> LineageReport:
    records = ledger.verify()
    kinds: list[str] = []
    observations: list[str] = []
    releases: list[str] = []
    for record in records:
        payload = record.get("payload", {})
        nested = payload.get("experiment", {})
        if nested.get("experiment_id") == experiment_id:
            kinds.append(record["kind"])
            observations.extend(nested.get("trigger", {}).get("observation_ids", []))
        if payload.get("experiment_id") == experiment_id:
            kinds.append(record["kind"])
        if payload.get("source_experiment") == experiment_id:
            kinds.append(record["kind"])
            releases.append(payload.get("release_id", ""))
    required = {
        "EXPERIMENT_RECORD_RECORDED",
        "experiment_transition",
        "DEPLOYMENT_DECISION",
    }
    return LineageReport(
        experiment_id,
        tuple(kinds),
        tuple(dict.fromkeys(observations)),
        tuple(releases),
        required.issubset(kinds) and bool(observations) and bool(releases),
    )
