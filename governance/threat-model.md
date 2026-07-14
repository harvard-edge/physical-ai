# MiOS Phase 1A Threat Model

**Status:** Active for the local synthetic controller
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

The Phase 1A controller enforces the candidate boundary for its synthetic
fixture. The browser, memory, cloud-provider, release-signing, and physical
runtime boundaries remain target requirements.

## Principal Threats

| **Threat** | **Current exposure** | **Required control** |
| --- | --- | --- |
| LAN caller records, reads, or resets memory | Routes have no demonstrated authentication | Adult and child roles, origin protection, CSRF defense, rate limits, audit |
| Child or bystander data leaves the home unexpectedly | The product prototype can send conversational context to a configured provider | Guardian consent, visible activation, provider allowlist, minimization, retention review |
| Model emits unsafe or stale action | App directly invokes SDK methods | Typed proposal, local authorization envelope, deadline, watchdog, neutral recovery |
| Candidate steals credentials or contacts robot | The synthetic worker has no credentials, external adapters, or network, but the trusted controller host is not OS-network-confined | Keep the container network denied, use an external secret store for future adapters, and confine controller egress before model access |
| Candidate reads credentials from user configuration | The pinned nonroot container receives an empty temporary home and one fixture mount | Retain the read-only root, stripped environment, narrow mount, and hostile-output tests |
| Candidate changes its evaluator | The worker can return only a validated source artifact; the supervisor rejects other paths and verifies the frozen test digest | Move protected suites to a separately administered evaluator before real-repository authority |
| Agent inflates improvement claims | No preregistration or metric service | Fixed denominators, missing-as-failure, raw attestations, paired/repeated evaluation |
| Ledger is rewritten after failure | The hash chain and trusted head detect partial corruption, but one host identity can rewrite both | Separate or sign the head before consequential autonomy |
| Dependency or workflow expands authority | A frozen lock, SBOM, license policy, release manifests, and upgrade tests exist; artifact signing does not | Require reviewed lock changes and signed releases before distribution |
| Rollback restores deleted child data | Backup lifecycle is unspecified | Consent-aware snapshots, deletion tombstones, recovery point and retention policy |
| Autonomous loop consumes unbounded resources | Durable controller-time, attempt, storage, and WIP budgets stop the local loop | Retain atomic reservations and add provider-specific budgets before Phase 1B |
| Candidate compromises a persistent hardware runner | Phase 1A has no hardware adapter or robot credentials | Use a clean ephemeral candidate runner and separate pull-based hardware evaluator |
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

## Residual Phase 1A Risk

The synthetic candidate sandbox, durable workflow, budgets, stop switch,
artifact checks, review identities, and release-manifest checks are implemented.
LAN authentication, child-data consent, external protected-evaluation custody,
trusted-controller egress confinement, artifact signing, rollback, and physical
action authorization are not. The controller therefore retains zero authority
for model providers, GitHub writes, child data, robot networking, signing, and
deployment.
