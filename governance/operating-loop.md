# MiOS Shared Operating Loop

**Version:** 1.0.0
**Status:** Active for Phase 1A

MiOS continuity lives in durable project state, not in one model conversation or
one provider's private configuration. Claude, Codex, Gemini, deterministic
workers, and future providers synchronize through the same repository-neutral
task envelopes, evidence records, policies, and state machine. Private prompts,
credentials, subscriptions, and home-directory settings remain outside the
repository.

## Operating Rule

Continuous operation means a restartable supervised service. It does not mean
an unbounded shell loop. The supervisor accepts one fenced work item at a time,
records every completed boundary, backs off while idle, and stops when policy,
time, storage, work-in-progress, integrity, or failure limits are reached.

The durable loop is:

```text
observe → claim → preregister → prepare effect intent → execute in sandbox
        → verify evidence → commit transition → append ledger → inspect
        → wait with bounded backoff → repeat
```

A process crash loses only in-memory execution. DBOS recovers workflow
checkpoints, while the MiOS registry remains the source of research truth.
Prepared effect intents make retries reconcile an existing effect before they
attempt another one.

## Shared Coordination Contract

Every worker receives a validated task packet from
`protocol/agent-task.schema.json` and returns
`protocol/agent-result.schema.json`. The packet fixes identity, role, inputs,
capabilities, command identifiers, budgets, deadlines, acceptance checks,
policy digest, and nonce. Unknown fields, expanded authority, forged identity,
expired work, or unsupported evidence fail closed.

Provider adapters may translate this contract into a Claude, Codex, Gemini, or
local worker invocation. They may not change its authority. A provider session
identifier is operational metadata, not durable project state. Model-specific
prompt material stays private unless a later research protocol explicitly
approves a publishable prompt artifact.

## Restart and Stop Semantics

`STOP` is the persistent operator kill switch. Ordinary `run` and `supervise`
commands cannot remove it. The dedicated `resume` command validates the stored
campaign, policy, and approval-artifact digests before it clears the file.
Signals and an external pause request stop new claims, terminate active process
groups within the declared grace period, and leave the controller paused.

Service managers may restart a crashed process, but they must never issue the
resume command. This preserves the difference between process recovery and a
new grant of authority.

## Upgrade Semantics

Package release versions and DBOS workflow compatibility versions are separate.
Compatible workflow changes use named patch sites. Incompatible histories must
fully drain. Phase 1A has no executable history-migration mechanism, so a
declarative migration record grants no authority. Once an experiment exists, a
restart cannot bless changed controller code, fixtures, protocol schemas,
dependency locks, approval artifacts, or sandbox identity. An exact
release-activation record is required for a compatible package release.
Registry schema versions are monotonic and bound into the release manifest.
This controller rejects newer schemas and permits its legacy-to-v3 migration
only for an empty, fully drained registry.

An incompatible workflow activation also requires the controller to be paused,
new work disabled, every experiment terminal, every effect intent completed,
and every DBOS workflow in a terminal status. Registry completion alone is not
treated as proof that checkpoint execution has drained.

## Current Authority Boundary

Phase 1A allows only synthetic local fixtures. Candidate and reviewer containers
have no network, inherited credentials, Git metadata, protected test writes,
model provider, GitHub, robot, or deployment authority. The trusted controller
has no external adapters, but its host process is not yet confined by an
operating-system network sandbox. Evidence must state that limitation rather
than claiming independently measured zero host egress.

Model providers, GitHub publication, child or household data, robot access, and
physical deployment remain disabled until a later phase has a new approval and
its required assurance evidence.

## Completion and Escalation

The loop pauses when it cannot prove a safe next transition. Budget exhaustion,
review disagreement, malformed output, integrity drift, repeated failure, or an
expired campaign is a normal terminal condition, not a reason to improvise.
The principal investigator decides whether to repair, migrate, expand authority,
or close the campaign.
