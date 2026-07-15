"""Independent software-only QA campaign for the MiOS closed-loop simulator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .simulation import ClosedLoopSimulator


@dataclass(frozen=True)
class QAFinding:
    scenario: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class QACampaignReport:
    findings: tuple[QAFinding, ...]
    passed: bool
    physical: bool = False


def run_software_qa(root: str | Path) -> QACampaignReport:
    report = ClosedLoopSimulator(root).run()
    findings = (
        QAFinding(
            "teach-and-recall",
            report.taught and report.recalled_after_restart,
            "memory survives restart",
        ),
        QAFinding(
            "safe-action",
            report.action_status == "EXECUTED",
            "allowed action reaches fake gateway",
        ),
        QAFinding(
            "protective-stop", report.failure_contained, "stopped action is contained"
        ),
        QAFinding(
            "reset-isolation", report.reset_empty, "reset removes disposable memory"
        ),
    )
    return QACampaignReport(findings, all(finding.passed for finding in findings))
