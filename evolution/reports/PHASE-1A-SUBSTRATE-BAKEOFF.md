# MiOS Phase 1A Workflow Substrate Bakeoff

**Date:** July 14, 2026
**Decision:** DBOS 2.26.0 with SQLite for the single-host local proof

## Result

The normalized bakeoff executes the same seven-effect semantic sequence for
DBOS and a minimum custom SQLite control. DBOS owns the actual MiOS workflow.
The custom runner is only a comparison fixture and does not implement the MiOS
registry, policy, artifact, review, or ledger planes. Temporal is recorded as
not runnable because Phase 1A did not provision its required local service and
forbids substituting a remote service.

| **Criterion** | **Custom Control** | **DBOS 2.26.0** | **Temporal** |
| --- | --- | --- | --- |
| Seven-effect normalized cycle | Passed | Passed | Not run |
| Injected process exit | Passed | Passed | Not run |
| Recovery to terminal state | Passed | Passed | Not run |
| Duplicate semantic effects | Zero | Zero | Not measured |
| Persistent pause before another effect | Passed | Passed | Not measured |
| Equivalent semantic digest | Matched DBOS | Matched custom | Not available |
| Separate service | No | No for SQLite proof | Required |
| Role in MiOS | Comparison fixture only | Selected checkpoint substrate | Scale candidate |

Raw timing is observational and excluded from the semantic digest. The current
measurements and exact tool versions live in
[`phase1a-substrate-bakeoff.json`](../../evaluation/results/phase1a-substrate-bakeoff.json).
The checked-in schema prevents a failed or unavailable candidate from being
silently represented as a pass.

## Selection Boundary

DBOS supplies workflow identity, durable step checkpoints, restart recovery,
cancellation requests, queues, and inspection. It does not own hypotheses,
budgets, effect identities, review attestations, release authority, or the
engineering ledger. Those remain in MiOS-owned stores so a future substrate can
be compared or replaced without redefining the research record.

The production workflow separates package release version from replay
compatibility. Compatible changes use named `DBOS.patch` sites. Incompatible
history must fully drain. A declarative migration record cannot substitute for
an executable history migration, which Phase 1A does not implement. A real
interrupted MiOS workflow test proves that pre-patch history resumes under the
current workflow without duplicating domain effects.
The drain gate checks both MiOS registry state and DBOS workflow status while
the controller is paused and new work is disabled.

Temporal should be reconsidered when MiOS requires multiple hosts, long waits,
or availability that justifies operating another service. A custom substrate
should be reconsidered only if DBOS fails a measured requirement that cannot be
corrected within the approved resource and assurance boundary.

## Platform, Resource, and License Evidence

The frozen dependency lock resolves with hashes and binary artifacts for Linux
ARM64 with CPython 3.12. Native Linux ARM64 controller execution has not yet
been run because no target host was available. The earlier Python 3.10 claim was
incorrect. The package requires Python 3.11 or newer.

The pinned sandbox image is Linux ARM64 and runs as UID and GID 65532. Its
candidate processes have no network, inherited credentials, Git metadata, or
write access to frozen tests. Cached vulnerability results apply only to the
scanner data available at collection time. They are not a permanent safety
claim.

The dependency SBOM and license inventory are evaluated against the Phase 1A
allowlist. Unknown metadata and licenses outside the list fail closed. The
policy also surfaces LGPL distribution obligations. This is a local research
admission decision, not project-license selection or public-distribution legal
clearance.

Measured controller time and storage for the synthetic cycle remain well below
the Phase 1A limits. No RSS threshold exists in governance, so memory is
reported without a compliance claim. The evidence is stored in:

- [`phase1a-supply-chain.json`](../../evaluation/results/phase1a-supply-chain.json)
- [`phase1a-sandbox-image.json`](../../evaluation/results/phase1a-sandbox-image.json)
- [`phase1a-resource-profile.json`](../../evaluation/results/phase1a-resource-profile.json)

## Authority Scope

Candidate and reviewer containers are network denied and narrowly mounted. The
trusted controller has no model, GitHub, robot, or deployment adapter in Phase
1A. Its host process is not confined by an operating-system network sandbox.
The evidence therefore proves candidate-worker isolation and adapter absence,
not independently measured zero host egress.

Active child and grandchild process cancellation is tested separately from the
substrate comparison. Those tests prove bounded controller process-group
termination. The normalized bakeoff currently proves persistent pause before
another effect and does not label that result as an active DBOS cancellation
latency measurement.

## Reproduction

Run the normalized candidate comparison with:

```text
cd orchestrator
.venv/bin/python tools/run_substrate_bakeoff.py \
  --repository .. \
  --cli .venv/bin/mios-controller \
  --output ../evaluation/results/phase1a-substrate-bakeoff.json
```

Run the complete DBOS boundary matrix with:

```text
cd orchestrator
.venv/bin/python tools/run_crash_matrix.py \
  --repository .. \
  --cli .venv/bin/mios-controller \
  --workers 2 \
  --output ../evaluation/results/phase1a-crash-matrix.json
```

Collect platform, supply-chain, image, and resource evidence with:

```text
cd orchestrator
.venv/bin/python tools/collect_phase1a_evidence.py \
  --output-dir ../evaluation/results
```
