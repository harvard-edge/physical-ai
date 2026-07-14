# MiOS Phase 0 Review and Approval Gate

**Date:** July 14, 2026
**Decision:** Pause before continuous operation

## Review Process

Three clean-context specialist roles independently inspected the charter and
repository. A Verification Engineer measured the implementation and identified
test and deployment gaps. A Governor and Safety Reviewer derived protected
invariants and threat controls. A Systems Architect and Framework Scout compared
controller designs and local tooling.

All three roles were executed within the current Codex environment. Claude Code
is installed, but the active model-call budget is zero. Gemini CLI is not
installed. No Claude, Gemini, or other paid external model call was made. The
cross-family critique required by the charter remains pending budget approval
and Gemini installation or another approved Gemini access method.

## Reconciled Decisions

The reviews agree that continuous autonomy should not run inside the robot or a
long-lived model session. A separate local controller will own durable state and
invoke replaceable workers. SQLite, Pydantic, Git, subprocess isolation, and
content-addressed artifacts are sufficient for the first synthetic proof.
LangGraph, Prefect, and Temporal are deferred until measured workflow complexity
justifies them.

The first forge is local. It creates issue and pull-request manifests but cannot
publish them. A GitHub adapter remains disabled until the repository has a
remote, protected controls exist, and external publication is explicitly
authorized.

The reviewers rejected the assumption that the current app already has a
deterministic physical-safety boundary. Direct Reachy SDK calls remain in the
application process. Physical authority therefore stays disabled until a
separate capability supervisor, emergency stop, watchdog, and target-hardware
tests exist.

The reviewers also rejected treating the current event journal as an evolution
ledger. It is in memory, bounded, and may contain verbatim interactions. The
controller needs a privacy-filtered, append-only, hash-chained record with
explicit provenance.

## Evidence That Would Reverse These Decisions

- Measured coordination failures in the local controller could justify Prefect
  or Temporal.
- A real branching, resumable reasoning workload could justify LangGraph inside
  a worker without replacing controller authority.
- A verified Git remote and protected-environment configuration could justify a
  disabled-by-default GitHub adapter.
- Hardware evidence from an independently enforced action envelope could permit
  a supervised physical canary request.

## Approval Requests

The principal investigator is asked to decide the following items before Phase
1 begins:

1. Approve the proposed constitution, authority policy, protected paths, threat
   model, privacy direction, and local-only controller decision.
2. Approve or revise the 30-day pilot limits of $200, 10 million model tokens,
   200 provider calls, 100 controller hours, 10 GiB storage, two concurrent
   experiments, and three protected-evaluation queries per experiment.
3. Approve Claude and Codex subscription-backed tools as engineering providers
   and authorize installation and authentication of Gemini CLI. Exact model
   identifiers will be discovered and recorded at runtime.
4. Assign an independent custodian for the protected Maya Test cases. Candidate
   agents must not have access to the source cases.
5. Decide retention periods for verbatim interactions and personal semantic
   memory, and approve each cloud provider's child-data purpose and terms before
   real child interactions are used as experimental evidence.

Physical canaries, public GitHub publication, automatic merge, and ordinary
child-data egress are not requested at this gate.

## Authorized Next Work After Approval

Phase 1 will implement only the deterministic offline controller and synthetic
issue-to-local-PR cycle described in ADR-0001. It will begin with fixture workers
that consume no model budget. Claude, Gemini, and Codex critique will follow once
provider access and budgets are active. The milestone ends at
`READY_FOR_PUBLICATION` and cannot deploy to Reachy.
