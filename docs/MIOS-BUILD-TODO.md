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
