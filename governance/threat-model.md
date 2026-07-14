# MiOS Phase 0 Threat Model

**Status:** Proposed
**Scope:** Reachy runtime, Evolution Controller, assurance plane, data providers,
Git forge, release path, and household network

## Protected Assets

MiOS must protect people from physical action, children and bystanders from
unconsented data use, credentials from candidate workers, protected evaluations
from contamination, budgets from uncontrolled consumption, the ledger from
rewriting, and the robot from unauthenticated control or unsafe releases.

## Trust Boundaries

```text
child or adult browser
        │ untrusted LAN request
        ▼
robot interaction gateway
        │ privacy-filtered events only
        ▼
runtime memory and cloud providers

candidate worktree ──deny──► assurance store, secrets, robot, deployment
        │ manifests and artifacts
        ▼
Evolution Controller ──attestations──► release authority
```

The current prototype does not yet enforce these boundaries. They are target
requirements, not descriptions of present protection.

## Principal Threats

| **Threat** | **Current exposure** | **Required control** |
| --- | --- | --- |
| LAN caller records, reads, or resets memory | Routes have no demonstrated authentication | Adult and child roles, origin protection, CSRF defense, rate limits, audit |
| Child or bystander data leaves the home unexpectedly | Groq receives audio or conversational context | Guardian consent, visible activation, provider allowlist, minimization, retention review |
| Model emits unsafe or stale action | App directly invokes SDK methods | Typed proposal, local authorization envelope, deadline, watchdog, neutral recovery |
| Candidate steals credentials or contacts robot | No candidate sandbox exists | Clean environment, network deny, external secret store, isolated disposable worker |
| Candidate reads credentials from user configuration | A scrubbed environment can still inherit a real home directory | Empty ephemeral home and denial outside the pinned worktree |
| Candidate changes its evaluator | Tests and governance are not protected | External protected suite, pinned manifest, deny candidate writes, independent custodian |
| Agent inflates improvement claims | No preregistration or metric service | Fixed denominators, missing-as-failure, raw attestations, paired/repeated evaluation |
| Ledger is rewritten after failure | No durable ledger exists | Hash chain, append API, reconciliation, external backup and verification |
| Dependency or workflow expands authority | No provenance or protected workflow | Locked dependencies, SBOM, ownership, policy classification, signed release |
| Rollback restores deleted child data | Backup lifecycle is unspecified | Consent-aware snapshots, deletion tombstones, recovery point and retention policy |
| Autonomous loop consumes unbounded resources | No active budget exists | Atomic reservations, per-task and monthly caps, fail-closed exhaustion |
| Candidate compromises a persistent hardware runner | Untrusted code can persist or steal robot access | Hosted or clean ephemeral candidate runner and separate pull-based hardware evaluator |
| Model upgrade is credited as MiOS improvement | Hosted model behavior changes outside the experiment | Freeze resolved model per comparison block and restart comparisons after change |

## Misuse and Metric Gaming

Protected cases remain outside candidate workspaces and reveal minimal failure
detail. All deployed experiments, including rollback and inconclusive outcomes,
remain in the denominator. Required-task completion is reported beside safety so
the system cannot achieve zero unsafe actions by refusing every task. Complexity,
latency, cost, and resource regressions accompany capability metrics.

Repeated protected-evaluation queries are limited. Evaluator dependencies,
workflow changes, and threshold changes receive the same protection as evaluator
source. A candidate that modifies its public acceptance test is rejected even
when all visible checks pass.

Fixed single-agent and fixed-team controls receive matched model, tool, token,
call, and time budgets. Failed and inconclusive runs remain registered. A
revision creates a child experiment so post hoc changes cannot overwrite the
original hypothesis or denominator.

## Incident Response

A suspected physical-safety or privacy incident stops recording and motion,
isolates the candidate and controller, preserves privacy-minimized evidence,
revokes affected credentials, restores the last-known-good runtime when safe,
and notifies the principal investigator. No agent may resume the experiment or
publish incident details without human authorization.

## Residual Phase 0 Risk

The policies are documents only. Authentication, sandboxing, protected
evaluation custody, action authorization, signing, and rollback are not yet
implemented. Until enforcement tests pass, the controller must have no paid
provider, GitHub-write, child-data, robot-network, signing, or deployment
credentials.
