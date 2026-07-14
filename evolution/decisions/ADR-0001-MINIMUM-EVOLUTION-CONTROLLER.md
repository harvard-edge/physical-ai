# ADR-0001: Select the Minimum Durable Evolution Substrate

**Status:** Revised proposal, supersedes the custom-first assumption
**Decision owner:** MiOS Systems Architect
**Approval required:** Professor Vijay Janapa Reddi

## Context

MiOS needs durable, restartable orchestration before agents receive repository,
GitHub, model-budget, or robot authority. Writing leases, queues, recovery,
workflow versioning, scheduling, cancellation, and inspection from scratch would
recreate mature infrastructure and weaken the reuse-first principle. The first
proof must remain local, deterministic, and incapable of publication or
physical deployment.

## Decision

Run a time-bounded substrate bakeoff, then build the controller as a separate
Python package. DBOS is the leading local candidate because it checkpoints
Python workflows and steps in SQLite without a separate service. Temporal is
the scale candidate for multi-host workflows and long human waits. A minimum
custom implementation is the control condition, not the automatic choice.
Prefect is retained as an operations-oriented alternative. The bakeoff records
version, license, transitive dependencies, ARM support, offline behavior,
recovery semantics, cancellation, workflow upgrades, inspection, and measured
resource cost.

The selected workflow substrate owns execution checkpoints. A MiOS experiment
registry owns hypotheses, preregistration, budgets, artifact references,
approvals, outcomes, and autonomy evidence. This separation prevents an
orchestrator's internal status from becoming the scientific record.

The first state machine is:

```text
OBSERVED → TRIAGED → PREREGISTERED → DESIGNED → IMPLEMENTING
                                                    │
                                                    ▼
LOCAL_CANDIDATE_READY ← REVIEWING ← EVALUATING

Any state → PAUSED | REJECTED
```

`LOCAL_CANDIDATE_READY` is a local terminal state. The proof cannot create an
external issue or pull request, merge a branch, call a paid model, or contact a
robot.

## Local Forge

Git has no issue or pull-request objects. A `Forge` interface will separate
workflow intent from publication. `LocalForge` writes validated issue, check,
review, and pull-request manifests and operates an isolated disposable Git
fixture. A future `GitHubForge` implements the same contract only after remote
configuration and explicit publication approval.

## Durable State

The experiment registry uses SQLite initially. Core records cover experiments,
observations, preregistrations, attempts, transitions, artifacts, idempotent
effects, reviews, budgets, ledger entries, and approvals. State advances only
when required artifact hashes and attestations exist. The selected durable
workflow substrate owns its own checkpoint store and correlates every run to a
registry experiment identifier.

External effects remain idempotent even when a workflow system retries work.
Stable keys, deterministic branch and worktree names, reconciliation before
retry, and content-addressed artifacts protect Git and forge operations.
Attempts and failures are appended rather than deleted.

## Seed Interfaces

```text
StateStore       claim, heartbeat, complete, advance, recover
Forge            create issue/candidate/check/PR and attach review
AgentProvider    discover capabilities and run a bounded task packet
EvaluationRunner run Inspect AI and conventional checks, then attest results
ArtifactStore    store and verify content-addressed bytes
PolicyEngine     authorize transitions and enforce protected paths
Ledger           append records and verify the hash chain
```

Inspect AI is the preferred agent-evaluation layer because it already provides
datasets, scorers, limits, sandboxed tools, logs, and bridges to external coding
agents. Conventional test runners continue to own deterministic functional and
safety checks. The fixture provider costs no model tokens. Candidate workers
inherit no credentials and have no network or robot access. Implementer and
decisive reviewers use different task identities and writable scopes.

## Bakeoff Decision Rule

The bakeoff uses the same crash-injected fixture with each candidate. DBOS is
selected if it passes recovery, cancellation, inspection, upgrade, and offline
tests within the resource budget. Temporal is selected if DBOS cannot safely
represent human waits or distributed workers and the service cost is justified.
The custom control is selected only when both fail a documented mandatory
requirement. LangGraph may later run inside a model worker, but it does not own
budgets, release authority, or the engineering ledger.

Every candidate must meet these mandatory criteria:

| **Criterion** | **Pass Condition** |
| --- | --- |
| Crash recovery | Resume after every transition and effect boundary |
| Duplicate effects | Zero duplicate branches, commits, reviews, charges, or manifests |
| Cancellation | Stop claiming work and terminate subprocess groups within the declared timeout |
| Offline operation | Complete the fixture with outbound network denied |
| Inspection | Query state, attempts, errors, and pending work without modifying them |
| Workflow upgrade | Resume an in-flight version-one fixture under a compatible version-two worker |
| Platform | Support Python 3.10+ and macOS and Linux ARM64 development targets |
| Resource use | Stay within the approved Phase 1A storage and controller-time budget |
| Licensing | Use a license compatible with an open research implementation |
| Policy boundary | Keep candidate credentials, filesystem, and network authority denied |

When several candidates pass, prefer the one with fewer continuously operated
services, less MiOS-specific recovery code, lower measured idle resources, and
the clearest export path for the experiment ledger. Popularity or agent
familiarity is not a selection criterion.

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
10. the substrate can be upgraded without replaying completed external effects;
11. workflow checkpoints and the research registry reconcile after injected
    partial failure; and
12. equivalent normalized evidence is produced by the bakeoff candidates so the
    selection is based on measured behavior rather than familiarity.

## Consequences

This decision adds a short bakeoff but avoids committing the research program to
homegrown workflow machinery. It keeps model, forge, evaluation, observability,
and robot adapters replaceable while assigning each durable fact to one owner.
