from mios_controller.assurance import (
    AssuranceVerdict,
    decide_release,
    evaluate_flawed_candidate,
)


def test_release_requires_independent_evidence_for_every_auditor():
    reports = [
        AssuranceVerdict(
            "qa-auditor", "a" * 64, "approve", evidence=("artifact://qa",)
        ),
        AssuranceVerdict(
            "safety-auditor", "a" * 64, "approve", evidence=("artifact://safety",)
        ),
    ]
    decision = decide_release(
        "a" * 64, reports, required_auditors=frozenset({"qa-auditor", "safety-auditor"})
    )
    assert decision.verdict == "approved"


def test_rejection_blocks_release_even_when_other_audits_pass():
    reports = [
        AssuranceVerdict(
            "qa-auditor", "b" * 64, "approve", evidence=("artifact://qa",)
        ),
        AssuranceVerdict(
            "safety-auditor",
            "b" * 64,
            "reject",
            ("unsafe authority",),
            ("artifact://safety",),
        ),
    ]
    decision = decide_release(
        "b" * 64, reports, required_auditors=frozenset({"qa-auditor", "safety-auditor"})
    )
    assert decision.verdict == "blocked"
    assert "safety-auditor rejected candidate" in decision.reasons


def test_flawed_candidate_campaign_is_blocked():
    decision = evaluate_flawed_candidate("c" * 64)
    assert decision.verdict == "blocked"
    assert "safety-auditor rejected candidate" in decision.reasons
