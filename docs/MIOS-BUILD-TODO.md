# MiOS Build TODO

**Status:** Active
**Owner:** MiOS coordinator
**Operating mode:** bounded iterative loops with durable checkpoints
**Last updated:** 2026-07-15

This is the executable build map for the MiOS prototype. The coordinator should
work one small item at a time, record evidence, run the relevant checks, commit
completed work, and update this file. An unchecked item is not complete merely
because code exists; it needs a verification record.

## Loop contract

Every iteration follows this sequence:

1. Select the highest-priority unblocked item.
2. State the intended change and acceptance checks.
3. Assign the work to the appropriate specialist role.
4. Produce an artifact in an isolated workspace.
5. Run tests and independent assurance checks.
6. Record evidence, risks, and unresolved questions.
7. Commit only the accepted change.
8. Check off the item and select the next item.

The loop pauses on a safety or privacy violation, missing authority, corrupted
evidence, repeated failure, budget exhaustion, or any request to publish or
access the robot without explicit approval.

## Current foundation

- [x] Durable MiOS evolution controller.
- [x] Crash-safe effects, leases, budgets, STOP, and resume controls.
- [x] Sandboxed deterministic worker and reviewer boundary.
- [x] Durable agent council task queue and handoff records.
- [x] Specialist architecture role contracts.
- [x] Independent assurance role contracts and release gate.
- [x] Deterministic workers for council replay.
- [x] Source-bound Phase 1A evidence and exit attestation.
- [x] Bootstrap charter audit with explicit missing-evidence matrix.
- [x] Typed cognitive runtime contracts and schema baseline.
- [x] Dependency-aware council routing and replayable campaign.
- [x] Evidence-gated episodic/semantic/procedural memory foundation.
- [x] Explicit maintenance-mode transition state machine.
- [x] Runtime event boundary with privacy-classified digests.
- [x] Cognitive checkpoint persistence and restart recovery.
- [x] Provider-neutral model adapter with deterministic fallback.
- [x] Protected candidate evaluation runner bound to an immutable suite digest.
- [x] Local staged release manifest, inactive slot, health check, and rollback.
- [x] Deterministic action envelope, fake hardware gateway, and protective stop.
- [x] Native Reachy app gateway contract with bounded gestures and protective stop.
- [x] Wire native Reachy response path through the gateway authorization check.
- [x] Add control-loop watchdog with protective-stop escalation.
- [x] Add bounded trace and metric observability store.
- [x] Define portable-core contracts and UNO Q-style conformance checker.
- [x] Bind replay campaign outcomes to the append-only ledger and report.
- [x] Expose the deterministic replay campaign through the controller CLI.
- [x] Add offline-testable local Ollama provider adapter with bounded fallback seam.
- [x] Add provider benchmark harness for latency, token use, failure, and provenance.
- [x] Connect maintenance mode to evidence-gated memory consolidation and runtime events.

## Flagship milestone — MiOS autonomous build demonstration

This is the near-term north-star demonstration: MiOS receives a bounded software
goal, coordinates specialized agents, tests and audits their work, records what
was learned, and starts another measured iteration. It is inspired by ambitious
autonomous engineering demonstrations, but remains local, replayable, and
evidence-bound until external authority is approved.

- [ ] Accept a natural-language build goal and create a durable campaign.
- [ ] Decompose the goal into a dependency-aware task graph.
- [ ] Route architect → researcher → implementer → verifier automatically.
- [ ] Run QA, security, safety, reliability, and release assurance in parallel.
- [ ] Produce a candidate artifact and an evidence-backed release decision.
- [ ] Store episodic events, semantic facts, and procedural lessons.
- [ ] Generate the next improvement task from failures or open questions.
- [ ] Run at least three bounded iterations without duplicate effects.
- [ ] Demonstrate pause, crash recovery, resume, and rollback.
- [ ] Produce a human-readable campaign report showing every handoff and result.

**Acceptance test:** Given a fixed local repository goal, a fresh MiOS instance
can execute the complete campaign offline using deterministic workers, reject an
injected unsafe candidate, accept a verified candidate, persist the lessons, and
schedule the next iteration with a complete provenance trail.

## Runtime-mode architecture

MiOS has one stable architecture with explicit operating modes. The system does
not rewrite its core during maintenance; maintenance changes memories,
procedures, and verified release candidates under the same authority boundary.

- [ ] **Interaction mode:** serve users, execute approved procedures, and record
      observations without mutating policy or installing code.
- [ ] **Maintenance mode:** drain active work, snapshot state, replay failures,
      consolidate memory, and generate bounded improvement tasks.
- [ ] **Build mode:** let the cloud or local agent council create isolated
      candidates and run evaluation and assurance.
- [ ] **Staging mode:** install a signed candidate in an inactive slot and run
      startup, health, and behavioral checks.
- [ ] **Recovery mode:** preserve evidence, stop unsafe effects, restore the last
      known-good version, and create an incident task.
- [ ] **Human-authority mode:** accept approvals for policy, external services,
      GitHub publication, model-provider access, and physical deployment.

Mode transitions must be durable, observable, resumable, and denied when the
required drain, evidence, approval, or rollback conditions are not satisfied.

## Two-level intelligence architecture

MiOS should use a small local model as an optional runtime copilot and a larger
cloud model for heavy design work. The local model is never the safety boundary
and never directly controls actuators; deterministic policy code remains in
charge.

- [ ] Define a local-model interface for summarization, intent classification,
      memory tagging, uncertainty reporting, and maintenance triage.
- [ ] Benchmark Ollama ARM64 and llama.cpp-style runtimes on the target hardware.
- [ ] Compare a small quantized model against a deterministic no-model fallback.
- [ ] Keep local inference bounded by CPU, memory, latency, and thermal budgets.
- [ ] Define cloud escalation for complex planning, code generation, and research.
- [ ] Record local/cloud provenance, model version, confidence, and fallback path.
- [ ] Ensure the robot remains safe and useful when both model tiers are offline.
- [ ] Evaluate ExecuTorch or another embedded runtime if the hardware benefits
      from ahead-of-time edge deployment rather than a general LLM server.

## Open MiOS platform architecture

The public system should be a packageable platform rather than a single robot
application. Reuse existing infrastructure wherever it gives us a tested
primitive; MiOS owns the contracts, authority, memory lifecycle, and evidence.

- [ ] Define the public package boundaries and minimal installation profile.
- [ ] Use ExecuTorch as the north-star edge inference runtime; keep Ollama or
      llama.cpp as development and fallback adapters.
- [ ] Define isolated nodes for perception, speech, cognition, memory, behavior,
      safety, and hardware adapters.
- [ ] Evaluate ROS 2 lifecycle nodes for robot-facing integration, without making
      ROS 2 a requirement for the core cloud or desktop runtime.
- [ ] Define typed event, task, artifact, memory, capability, and release schemas.
- [ ] Build a curated skills library with versioned metadata, tests, permissions,
      provenance, examples, and deprecation policy.
- [ ] Separate raw episodic storage, curated semantic knowledge, procedural
      skills, and derived embeddings.
- [ ] Start with SQLite for local single-device operation and PostgreSQL for
      multi-user/cloud operation; evaluate Kùzu or Apache AGE only when graph
      workload tests justify a dedicated graph layer.
- [ ] Make every memory and skill promotion traceable to source evidence and an
      assurance verdict.
- [ ] Publish an open-source contributor guide, extension API, compatibility
      policy, and security reporting process.

## LLM-first design principle

MiOS is not merely a conventional robot stack with an LLM added on top. Its
first-class abstractions are goals, context, memory, skills, uncertainty,
delegation, evidence, and reflection. Conventional operating-system and
robotics components remain implementation choices, not architectural laws.

- [ ] Define the MiOS cognitive object model: goal, belief, memory, skill,
      capability, obligation, observation, action proposal, and evidence.
- [ ] Define model-native context assembly and attention budgets as explicit
      runtime resources rather than hidden prompt construction.
- [ ] Define structured reflection and self-critique protocols that produce
      inspectable artifacts rather than unbounded internal conversations.
- [ ] Define a capability negotiation protocol so agents discover tools and
      constraints through schemas.
- [ ] Define graceful degradation from cloud model → local model → deterministic
      procedure → safe idle state.
- [ ] Evaluate every reused framework against MiOS criteria: model-native state,
      durable recovery, inspectability, edge suitability, safety boundaries,
      extensibility, and operational cost.
- [ ] Replace a conventional component when a simpler MiOS-native design is
      measurably better, while retaining standard adapters for interoperability.
- [ ] Keep the deterministic safety kernel below the LLM layer; no model may
      directly own irreversible authority.
- [ ] Implement the cognitive runtime primitive contracts in
      `docs/MIOS-CONTEXTVM.md`.
- [ ] Define schemas for goals, contexts, beliefs, skills, capabilities,
      observations, proposals, checkpoints, and evidence.
- [ ] Build context assembly with explicit budgets, leases, provenance, and
      reproducible retrieval.
- [ ] Build deterministic promotion gates from episodic to semantic and
      procedural memory.
- [ ] Add checkpoint and resume semantics for cognitive execution.

## Build-time track — bootstrap MiOS itself

These items are completed while the system is being created. They produce the
first installable and inspectable MiOS release.

- [ ] Freeze the bootstrap specification, architecture decisions, and threat model.
- [ ] Define component interfaces and machine-readable protocol schemas.
- [ ] Implement the coordinator, queues, workers, assurance, memory, and release
      components behind tested interfaces.
- [ ] Create deterministic fixtures and replayable end-to-end campaigns.
- [ ] Build a complete local candidate and verify its provenance.
- [ ] Run static analysis, type checks, unit tests, integration tests, failure
      injection, resource checks, and security scans.
- [ ] Produce operator, developer, and architecture documentation alongside code.
- [ ] Package a signed local release with an explicit rollback target.
- [ ] Install the release into a disposable environment and exercise recovery.

## Runtime track — operate an installed MiOS

These items apply after bootstrap, when MiOS is serving users and evolving over
time. Runtime changes must not depend on the original development session.

- [ ] Start from a known-good release and verify its manifest and configuration.
- [ ] Serve interaction workloads while recording bounded observations.
- [ ] Monitor health, latency, resource use, queue depth, and uncertainty.
- [ ] Enter maintenance mode only after active work drains safely.
- [ ] Replay incidents and consolidate memory without rewriting raw history.
- [ ] Generate improvement tasks from measured failures and unanswered questions.
- [ ] Build candidates in isolated workspaces with immutable baselines.
- [ ] Run independent assurance and release gates before staging.
- [ ] Install into an inactive slot, run health checks, and roll back on failure.
- [ ] Keep a human override, persistent STOP, incident record, and recovery path.
- [ ] Periodically verify backups, provenance, rollback, and memory integrity.

## Code quality and readability gates

MiOS must remain understandable to a human engineer. Generated code is treated
as an untrusted draft until it passes the same review as hand-written code.

- [ ] Every module has a narrow responsibility and a short module docstring.
- [ ] Public interfaces have type annotations and concise documentation.
- [ ] Tests explain behavior and failure modes, not implementation trivia.
- [ ] No dead code, duplicate helpers, speculative abstractions, or unexplained
      generated boilerplate.
- [ ] No broad exception swallowing, hidden network calls, unbounded retries, or
      mutable global state in control paths.
- [ ] Every non-obvious policy decision links to an ADR or governance rule.
- [ ] Ruff, type checking, documentation checks, and test coverage run before
      commit.
- [ ] An independent readability review removes unnecessary complexity before
      release.
- [ ] Each iteration records what was simplified or deliberately left unchanged.

## Complete lifecycle team

- [ ] Bootstrap engineer completes first-release installation and recovery.
- [ ] Memory engineer owns schemas, retrieval, consolidation, and integrity.
- [ ] Evaluation scientist defines improvement metrics and comparison protocols.
- [ ] Maintenance scheduler owns drain, sleep, replay, and resume transitions.
- [ ] Observability engineer owns metrics, traces, alerts, and operator health.
- [ ] Incident commander owns containment, pause, recovery, and postmortems.
- [ ] Deployment engineer owns staging, health checks, and rollback exercises.
- [ ] Robot integration engineer owns simulation and the physical gateway boundary.
- [ ] Documentation engineer keeps code and architecture readable and traceable.
- [ ] Human authority role handles irreversible approvals and escalations.

## Loop 1 — Council execution

- [ ] Add dependency-aware task graphs and automatic handoff routing.
- [ ] Add task retry, timeout, cancellation, and dead-letter states.
- [ ] Add coordinator CLI commands to enqueue, inspect, and run council tasks.
- [ ] Add durable council event records to the MiOS ledger.
- [ ] Add a replay fixture that exercises architect → implementer → verifier →
      assurance → historian.

## Loop 2 — Memory and consolidation

- [ ] Define episodic memory schema for observations, tasks, and outcomes.
- [ ] Define semantic memory schema for entities, concepts, and relations.
- [ ] Define procedural memory schema for reusable workflows and lessons.
- [ ] Implement append-only memory records with provenance and confidence.
- [ ] Implement retrieval by exact relation and text before adding embeddings.
- [ ] Implement sleep-time consolidation and deduplication.
- [ ] Implement memory rollback and selective forgetting.
- [ ] Test that unverified proposals cannot become durable knowledge.

## Loop 3 — Model-provider workers

- [ ] Define provider-neutral worker adapter protocol.
- [ ] Add deterministic replay provider.
- [ ] Add local model provider stub with explicit capability limits.
- [ ] Add hosted-provider adapters behind budget and approval gates.
- [ ] Record model name, version, parameters, token use, latency, and cost.
- [ ] Freeze provider versions within comparison experiments.
- [ ] Test provider failure, timeout, malformed output, and rate limiting.

## Loop 4 — Build and evaluation pipeline

- [ ] Create isolated candidate workspace manager.
- [ ] Add patch and changed-file artifacts.
- [ ] Add baseline-versus-candidate evaluation manifests.
- [ ] Add regression, resource, and reliability benchmark runners.
- [ ] Add adversarial review fixtures.
- [ ] Add improvement decision records with measurable thresholds.
- [ ] Ensure rejected candidates cannot enter shared memory or release storage.

## Loop 5 — Maintenance and self-improvement

- [ ] Add maintenance-mode state machine.
- [ ] Add scheduled observation, replay, and consolidation jobs.
- [ ] Add task generation from failures, uncertainty, and unanswered questions.
- [ ] Add controller health and queue-depth monitoring.
- [ ] Add nightly maintenance report.
- [ ] Add safe rollback to the last known-good controller configuration.
- [ ] Prove that maintenance pauses cleanly and resumes without duplicate effects.

## Loop 6 — Release and deployment boundary

- [ ] Define signed local release manifest.
- [ ] Add artifact registry and provenance index.
- [ ] Add inactive-slot installation model.
- [ ] Add startup health checks and automatic rollback.
- [ ] Add simulated robot gateway with no physical authority.
- [ ] Add explicit human approval for physical deployment.
- [ ] Add robot-side update agent only after simulation passes.
- [ ] Document cloud, local, and robot data-flow boundaries.

## Loop 7 — Operational readiness

- [ ] Add structured logs, metrics, and trace IDs.
- [ ] Add incident and escalation records.
- [ ] Add operator status and pause/resume interface.
- [ ] Add backup and restore verification.
- [ ] Add resource and cost dashboards.
- [ ] Run an end-to-end overnight simulation with bounded budgets.
- [ ] Complete an independent architecture and threat-model review.

## Definition of done

The prototype is complete when every required item above is checked, the full
test suite passes, the end-to-end maintenance simulation can run through
multiple cycles, every accepted artifact has provenance and assurance evidence,
rollback has been demonstrated, and physical deployment remains explicitly
gated behind human authority.

## Iteration log

| Date | Loop/item | Result | Evidence or commit |
|---|---|---|---|
| 2026-07-15 | Foundation and council | Completed | `e4776d6` |
| 2026-07-15 | Charter audit and cognitive contracts | Completed | `b1eb3dd` |
| 2026-07-15 | Dependency routing and replay campaign | Completed | `38cce3c` |
| 2026-07-15 | Memory and maintenance foundation | Completed | `5cd3bcc` |
| 2026-07-15 | Runtime boundary and provider fallback | Completed | `6cf2e58` |
| 2026-07-15 | Protected evaluation runner | Completed | `f9e6854` |
| 2026-07-15 | Staged release and rollback boundary | Completed | `a0ad2d9` |
| 2026-07-15 | Embodied safety gateway | Completed | `0926965` |
| 2026-07-15 | Native Reachy app gateway contract | Completed | `fa43b61` |
| 2026-07-15 | Reachy response-path gateway integration | Completed | `7743976` |
| 2026-07-15 | Native memory connection cleanup | Completed | `a7b5ee3` |
| 2026-07-15 | Reachy control watchdog | Completed | `d4faddb` |
| 2026-07-15 | Observability store | Completed | `37b96f4` |
| 2026-07-15 | Portable-core conformance | Completed | `5183344` |
| 2026-07-15 | Campaign ledger and report binding | Completed | `3488ad5` |
| 2026-07-15 | Replay campaign CLI | Completed | `e7492f8` |
| 2026-07-15 | Live replay CLI execution evidence | Completed | `evaluation/results/replay-campaign-cli.json` |
| 2026-07-15 | Local Ollama provider adapter | Completed | `2a1ee4e` |
| 2026-07-15 | Provider benchmark harness | Completed | `ae60344` |
| 2026-07-15 | Maintenance/memory integration | Completed | `b393b9d` |
| 2026-07-15 | Machine-readable experiment record contract | Completed | `ExperimentRecord` in `orchestrator/mios_controller/experiment.py`; unit and full-suite verification |
| 2026-07-15 | Idempotent experiment-record ledger append | Completed | `Ledger.append_experiment_record`; ledger idempotency test |
| 2026-07-15 | Bind replay campaign to structured research record | Completed | Campaign emits `EXPERIMENT_RECORD_RECORDED` before completion event |
| 2026-07-15 | Bind controller candidate state to experiment record | Completed | `LOCAL_CANDIDATE_READY` transition persists validated record with observation and evidence digest |
| 2026-07-15 | Record staged deployment and rollback decisions | Completed | Two-slot controller appends idempotent `DEPLOYMENT_DECISION` events |
