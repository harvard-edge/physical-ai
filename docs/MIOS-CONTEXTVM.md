# MiOS Cognitive Runtime Primitives

The MiOS cognitive runtime manages context, memory,
goals, skills, capabilities, uncertainty, attention, and evidence. Models are
schedulable workers inside this machine, not the machine itself.

“ContextVM” is one useful design metaphor, not a constraint on the whole OS. MiOS
should combine several native abstractions where each is strongest.

## Broader LLM-first primitives

- **Cognition scheduler:** decides which reasoning process runs, with what
  context, model, budget, urgency, and interruption policy.
- **Memory fabric:** routes episodic, semantic, procedural, and working memory
  while preserving provenance and promotion rules.
- **Skill runtime:** loads, composes, tests, versions, and retires executable
  procedures with explicit contracts.
- **Capability mesh:** exposes tools, sensors, services, and actuators through
  typed, leased, revocable capabilities.
- **World model:** maintains entities, state, time, uncertainty, and relations
  about the robot and its environment.
- **Attention manager:** decides what deserves context and computation under
  token, latency, energy, and thermal budgets.
- **Self-model:** tracks the system's capabilities, limits, identity, current
  mode, health, and unresolved uncertainty.
- **Event fabric:** carries observations, intentions, outcomes, failures, and
  maintenance signals as durable typed events.
- **Reflection engine:** turns experience into bounded lessons and candidate
  improvements without directly changing authority.
- **Evidence ledger:** makes claims, memories, actions, and releases auditable.
- **Safety kernel:** validates proposed effects deterministically and remains
  independent of model interpretation.

## First-class primitives

- **Goal:** bounded objective with success criteria, priority, authority scope,
  budget, deadline, and parent campaign.
- **Context:** leased, size-bounded working set whose items have provenance,
  relevance, sensitivity, and expiry policy.
- **Memory:** episodic events, semantic concepts and relations, procedural
  skills, and temporary working state.
- **Belief:** a claim with confidence, evidence, scope, timestamp, and possible
  contradictions.
- **Skill:** versioned procedure with schemas, required capabilities, tests,
  risk class, owner, and rollback behavior.
- **Capability:** typed, leased permission to read, compute, communicate, or act.
- **Observation:** immutable, privacy-classified input from a user, sensor,
  service, or monitor.
- **Action proposal:** intended effect with expected outcome, risk,
  reversibility, and required capabilities; it is not yet an action.
- **Reflection:** bounded analysis that produces lessons, uncertainty, or tasks.
- **Checkpoint:** durable state needed to resume without hidden model state.
- **Evidence:** provenance binding claims, actions, tests, and releases to
  immutable artifacts.

## Execution cycle

```text
observe → retrieve → assemble context → reason
   → propose belief/skill/action → verify authority
   → execute or reject → record evidence → checkpoint
```

Every step has explicit token, latency, memory, tool, and effect budgets. Context
is summarized or retrieved by policy when it is too large; it is never silently
truncated.

## Context and virtual-memory analogy

| Conventional OS | Cognitive runtime analogy |
|---|---|
| process | goal/campaign |
| address space | assembled context |
| page | memory artifact or fact bundle |
| page fault | retrieval request |
| scheduler | coordinator |
| capability | leased tool/action authority |
| checkpoint | durable cognitive state |
| syscall boundary | deterministic safety boundary |
| filesystem | provenance-backed memory and artifacts |

The analogy is a design tool for making cognition explicit, bounded,
inspectable, and recoverable; it is not a claim that cognition literally pages
like virtual memory.

## Invariants

1. Models never receive unbounded hidden state.
2. Models never directly promote durable memory.
3. Models never directly invoke irreversible effects.
4. Every durable claim and action has provenance.
5. Every worker can resume from a checkpoint.
6. Context assembly is reproducible from references and policy.
7. A deterministic fallback exists when no model is available.
