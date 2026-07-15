"""Independent assurance verdicts and release gating."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

Verdict = Literal["approve", "reject", "escalate"]


@dataclass(frozen=True)
class AssuranceVerdict:
    auditor: str
    candidate_digest: str
    verdict: Verdict
    findings: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    decisive: bool = True


@dataclass(frozen=True)
class ReleaseDecision:
    candidate_digest: str
    verdict: Literal["approved", "blocked", "escalated"]
    reasons: tuple[str, ...]
    reviewed_by: tuple[str, ...]


def decide_release(
    candidate_digest: str,
    verdicts: Iterable[AssuranceVerdict],
    *,
    required_auditors: frozenset[str],
) -> ReleaseDecision:
    """Apply the hard release gate without allowing self-approval or omission."""
    reports = tuple(verdicts)
    reasons: list[str] = []
    reviewed_by = tuple(sorted({report.auditor for report in reports}))

    wrong_digest = [
        report.auditor
        for report in reports
        if report.candidate_digest != candidate_digest
    ]
    if wrong_digest:
        reasons.append(
            f"audits reference another candidate: {', '.join(sorted(wrong_digest))}"
        )

    missing = required_auditors - set(reviewed_by)
    if missing:
        reasons.append(f"missing required audits: {', '.join(sorted(missing))}")

    for report in reports:
        if report.decisive and report.verdict == "reject":
            reasons.append(f"{report.auditor} rejected candidate")
        elif report.decisive and report.verdict == "escalate":
            reasons.append(f"{report.auditor} escalated candidate")
        if report.decisive and not report.evidence:
            reasons.append(f"{report.auditor} supplied no evidence")

    if any(
        "rejected" in reason or "missing" in reason or "no evidence" in reason
        for reason in reasons
    ):
        result: Literal["approved", "blocked", "escalated"] = "blocked"
    elif any("escalated" in reason for reason in reasons):
        result = "escalated"
    else:
        result = "approved"
    return ReleaseDecision(candidate_digest, result, tuple(reasons), reviewed_by)
