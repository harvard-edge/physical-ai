# ADR-0001: Minimum Evolution Controller

**Status:** Proposed
**Decision owner:** MiOS Systems Architect
**Approval required:** Professor Vijay Janapa Reddi

## Context

MiOS needs durable, restartable orchestration before agents receive repository,
GitHub, model-budget, or robot authority. The repository currently has no GitHub
remote and the robot is unreachable. The first proof must therefore be local,
deterministic, and incapable of publication or physical deployment.

## Decision

Build the controller as a separate Python package using Pydantic contracts,
SQLite transactions, the Git CLI, subprocess isolation, and SHA-256 addressed
artifacts. Do not place it inside the robot application process.

The first state machine is:

```text
OBSERVE → TRIAGE → HYPOTHESIZE → RESEARCH → DESIGN → IMPLEMENT
                                                     │
                                                     ▼
READY_FOR_PUBLICATION ← REVIEW ← EVALUATE
```

`READY_FOR_PUBLICATION` is a local terminal state. The proof cannot create an
external issue or pull request, merge a branch, call a paid model, or contact a
robot.

## Local Forge

Git has no issue or pull-request objects. A `Forge` interface will separate
workflow intent from publication. `LocalForge` writes validated issue, check,
review, and pull-request manifests and operates an isolated disposable Git
fixture. A future `GitHubForge` implements the same contract only after remote
configuration and explicit publication approval.

## Durable State

SQLite is the workflow source of truth. Core tables record experiments,
observations, work items and leases, attempts, transitions, artifacts,
idempotent side effects, reviews, budgets, ledger entries, and approvals.
State advances only when required artifact hashes and attestations exist.

Execution is at least once. Effects become effectively once through stable
idempotency keys, a transactional outbox, deterministic branch and worktree
names, reconciliation before retries, bounded leases, and content-addressed
artifacts. Attempts and failures are appended rather than deleted.

## Seed Interfaces

```text
StateStore       claim, heartbeat, complete, advance, recover
Forge            create issue/candidate/check/PR and attach review
AgentProvider    discover capabilities and run a bounded task packet
EvaluationRunner run public/protected checks and attest results
ArtifactStore    store and verify content-addressed bytes
PolicyEngine     authorize transitions and enforce protected paths
Ledger           append records and verify the hash chain
```

The fixture provider is deterministic and costs no model tokens. Candidate
workers inherit no credentials and have no network or robot access. Implementer
and decisive reviewers use different task identities and writable scopes.

## Framework Decision

LangGraph, Prefect, and Temporal are deferred. LangGraph is useful for branching
model reasoning but does not provide idempotent Git, budget, or deployment
effects. Prefect becomes useful when scheduled portfolios and operational
dashboards are justified. Temporal becomes useful for multi-host, long-waiting
workflows. The first proof needs fewer moving parts and one durable authority.

## Acceptance Evidence

The synthetic cycle must prove:

1. one observation produces one experiment, candidate commit, check set, two
   independent review attestations, local pull-request manifest, and ledger;
2. termination after every transition resumes without duplicate effects;
3. duplicate ingestion, expired leases, malformed output, budget exhaustion,
   reviewer disagreement, and failing checks stop safely;
4. changes to protected paths or acceptance tests are rejected;
5. ledger or artifact tampering is detected;
6. commands avoid shell interpolation and strip secrets;
7. network, GitHub, paid providers, and robot access are absent;
8. a clean directory reconstructs and verifies the cycle; and
9. the existing 19 Reachy tests continue to pass with `code/` unchanged.

## Consequences

This design delays impressive multi-agent activity until durability, authority,
and evidence are testable. It also prevents an early dependency on one model,
workflow framework, forge, or robot. Phase 1 may replace individual adapters
without replacing the controller's state and policy contracts.
