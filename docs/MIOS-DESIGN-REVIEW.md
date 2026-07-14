# MiOS Design Review

**Review date:** July 14, 2026
**Reviewed baseline:** `3826c6d`
**Disposition:** Revise before Phase 1 authorization

## Overall Judgment

The MiOS North Star remains technically credible as an experiment. The original
plan had a strong safety instinct and a useful separation between runtime,
evolution, and assurance. It was not yet a sufficiently controlled research
protocol or a reuse-first implementation plan. Revision 0.2 corrects the most
material gaps without reducing the ambition.

## Material Findings

| **Finding** | **Why It Matters** | **Revision** |
| --- | --- | --- |
| Activity and improvement were too easy to conflate | Many PRs can coexist with no behavioral gain | Compare adaptive MiOS with fixed-agent controls at matched budgets |
| Autonomy was binary and underspecified | “Out of the loop” hides intervention and task-selection differences | Report autonomy levels A0 through A5 and every intervention |
| The controller state machine omitted rejection and incident paths | A durable loop must represent failure as first-class state | Add paused, rejected, incident, and rolled-back terminal paths |
| Preregistration could be silently revised | Iteration can become post hoc metric selection | Revisions create linked child experiments |
| The 70% improvement target was gameable | Selective deployment and weak metrics could inflate success | Use cumulative preregistered utility and keep every outcome in the denominator |
| Custom orchestration was selected too early | It would recreate recovery and scheduling machinery | Require a DBOS, Temporal, and minimum-custom bakeoff |
| Evaluation infrastructure was mostly custom | Cross-model sandboxes, limits, and logs already exist | Prefer Inspect AI for agent evaluation and conventional tests for deterministic evidence |
| Software Stop was described too much like an emergency stop | Interaction cancellation is not a safety-rated control | Separate cancellation, protective stop, watchdog, and hardware stop terminology |
| Candidate isolation inherited `HOME` | Credentials can live in user configuration files, not only environment variables | Give workers an empty ephemeral home and deny filesystem escape |
| GitHub runners could become a bridge to the robot | Untrusted PR code can compromise persistent self-hosted machines | Use hosted or clean ephemeral workers and a separate pull-based hardware evaluator |
| Hidden evaluation and reproducibility conflicted | Secret cases cannot be both candidate-hidden and always repository-visible | Keep sealed cases with a custodian and publish or escrow them after the campaign |
| Phase 0 required Phase 2 evidence | Hardware rollback cannot be rehearsed before its controller and assurance path exist | Move hardware and rollback evidence to Phase 2 |
| The first budget bundled architecture and spending | It requested model money before deterministic orchestration worked | Split zero-dollar Phase 1A from the separately approved Phase 1B model pilot |
| The experiment had no bounded end | “Continuous” could prevent a defensible completion claim | Define a finite Campaign 1 completion boundary |

## Reuse-First Stack

The revised plan assigns one clear job to each adopted component.

| **Concern** | **Preferred component** | **Boundary** |
| --- | --- | --- |
| Durable local workflow | DBOS, subject to the bakeoff | Execution checkpoints and recovery only |
| Distributed scale-up | Temporal, only when justified | Multi-host work and long waits |
| Agent evaluation | Inspect AI | Datasets, solvers, scorers, limits, sandboxes, and logs |
| Research truth | MiOS experiment registry | Hypotheses, budgets, approvals, outcomes, and autonomy evidence |
| Operational telemetry | OpenTelemetry | Correlated traces, metrics, and privacy-filtered events |
| Engineering lineage | Hash-chained MiOS ledger | Immutable references to evidence and decisions |
| Source collaboration | Git and GitHub | Branches, reviews, checks, and releases |
| Build provenance | GitHub artifact attestations and SBOM | Verifiable release origin after a remote exists |
| Robot authority | Local deterministic supervisor | Capability validation and final actuator authorization |

DBOS documents SQLite-backed checkpoint recovery for Python workflows without a
separate service. Temporal supplies mature workflow, activity, cancellation,
timeout, and versioning primitives when distributed operation warrants its
service. Inspect AI already supports agent tasks, external coding agents,
sandboxing, limits, scoring, and evaluation logs. OpenTelemetry supplies common
semantics for traces, metrics, logs, and events. GitHub recommends ephemeral
self-hosted runners for autoscaling and supports signed artifact provenance and
SBOM attestations.

## Scientific Controls

Campaign 1 evaluates MiOS as a systems intervention, not only as a robot demo.
Fixed single-agent, fixed-team, and adaptive-team conditions receive matched
models, tools, tokens, calls, and time. Model upgrades create new blocks.
Protected cases are sealed from candidates. Primary metrics and minimum effects
are frozen before execution. Negative and inconclusive experiments remain in the
dataset.

The strongest publishable result would show that MiOS reaches a higher embodied
task utility under the same resource budget and safety constraints, while using
fewer unplanned human interventions. If it does not, the complete lineage still
supports a useful negative result about autonomous systems engineering.

## Residual Decisions for the Principal Investigator

Revision 0.2 does not resolve value judgments that belong to the study owner.
Phase 0 still needs an evaluation custodian, approved child-data retention and
research-admission rules, and authorization of the zero-dollar Phase 1A
operational budget. The release trust root is a Phase 2 gate before target
deployment. Phase 1B model access and spending are deliberately separate.

## Primary Infrastructure References

- [DBOS Python workflows](https://docs.dbos.dev/python/programming-guide)
- [Temporal Python SDK](https://docs.temporal.io/develop/python)
- [Inspect AI](https://inspect.aisi.org.uk/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
- [GitHub self-hosted runner guidance](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
