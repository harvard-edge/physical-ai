# MiOS Agent Work Protocol

**Version:** 1.1.0
**Status:** Active for Phase 1A

MiOS coordinates workers through versioned task and result envelopes. The
protocol is independent of Claude, Codex, Gemini, or any other provider. A
provider adapter translates a validated task into a private invocation and
returns only the common result envelope.

Repository policy describes roles, capabilities, evidence, and stopping rules.
Private assistant prompts, account details, authentication, home-directory
configuration, and provider session identifiers never enter repository
artifacts. This keeps the experiment reproducible without publishing personal
AI configuration.

## Authority

The supervisor creates all identifiers, the task nonce, budget, policy digest,
artifact digests, and capability set. A worker cannot grant itself new tools,
paths, time, network access, external services, or release authority. Unknown
fields and mismatched identifiers fail validation.

Phase 1A accepts only the deterministic fixture provider. It has no model,
network, GitHub, robot, or main-repository authority. Future provider adapters
must satisfy the same envelopes and receive separate approval.

## Work Lifecycle

1. The supervisor freezes a task packet against an approved policy snapshot.
2. It atomically reserves budget and claims work with a fenced lease.
3. A sandbox runner materializes verified input artifacts in a disposable
   workspace.
4. The worker runs with the declared capabilities and produces a result file.
5. The supervisor independently measures resource use, validates identifiers
   and schema, scans outputs, and recomputes every digest.
6. Accepted artifacts enter the content-addressed store. The transition and
   ledger record then commit.

Worker prose never advances controller state without the required structured
evidence.

## Isolation Profiles

`container` is the required profile for untrusted code. It uses no network,
read-only root filesystems, a writable disposable workspace, an empty temporary
home, dropped Linux capabilities, no privilege escalation, process and memory
limits, and an allowlisted command.

`cooperative_fixture` exists for development when a container is unavailable.
It uses argument arrays, an empty environment, a new process group, timeouts,
and a disposable fixture. It is not a security boundary and cannot run
adversarial or model-generated code.

## Persistent Stop Rule

Stopping is a durable state transition. SIGINT, SIGTERM, or the local kill file
sets `accept_new_work` false before active process groups are terminated. A
restart remains paused until an operator supplies an explicit resume command
whose campaign and policy digests match the stored approval.

The machine-readable contracts are
[`agent-task.schema.json`](../protocol/agent-task.schema.json) and
[`agent-result.schema.json`](../protocol/agent-result.schema.json).
