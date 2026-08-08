# Foundation-Wave Chapter Briefs

**Status:** first accepted sketch for Chapters 1 through 4  
**Execution source:** `PRODUCTION-PLAN.md`  
**Content source:** `CHAPTER-OUTLINES.md`

## Purpose

These briefs turn the first four chapter contracts into authoring work. They are
not compressed chapter drafts. They identify the indispensable argument,
representation jobs, source families, shallow treatments to reject, deliberate
deferrals, and the artifact each chapter must leave behind.

The foundation wave has one continuous argument.

> **A consequential physical loop creates requirements. Requirements create
> measurable claims. Measured claims determine the runtime.**

## Shared Context for the Wave

### Scope

A system belongs in the book only when a learned component materially influences
the action path, an allowed action changes task-relevant physical state and can
alter a later observation or choice, and the system exercises delegated
physical authority over that action. Hardware
presence, feedback alone, a fixed controller, or a capable model alone is
insufficient.

### Notation

Use \(W_t\), \(o_t\), \(b_t\), \(p_t\), \(u_t\), \(d_t\), and
\(W_{t+1}\) as defined in `PRODUCTION-PLAN.md`. Show the permission check in
words. Learned proposal \(p_t\) and allowed action \(u_t\) must remain
distinct in prose and figures.

### Canonical Case

The shared-workspace handling system observes a defined tabletop area,
interprets a requested handling or sorting task, proposes an action, checks it
against physical and authority constraints, acts, and observes the result.

The same case evolves across the wave.

| Version | State of the case |
| --- | --- |
| 0.1 | Task, world, affected people, action path, and system boundary are declared |
| 0.2 | World timescale, freshness limit, efficacy floor, consequences, and assumptions are attached |
| 0.3 | Requirements have operational definitions, instruments, thresholds, and evidence records |
| 0.4 | Continuous services, cadences, ownership, queue rules, failure states, and recovery behavior are specified |

### Traceability Thread

The first wave should produce at least one complete chain:

```text
LOOP-001 consequential action
    ↓
REQ-001 freshness requirement
    ↓
MEAS-001 complete-path age measurement
    ↓
RUN-001 stale-event rejection invariant
    ↓
later ENF-, EVID-, and REL- records
```

### Reader-Facing Form

Each chapter opens naturally, uses one objective callout, teaches through
chapter-specific headings, culminates in a decision callout with a dossier
sentence, and ends with the lab. Editorial fields remain in the context packet.

## Chapter 1 — From ML Systems to Physical AI

### Objective Callout

After this chapter, you will be able to tell when a learned system is doing more
than producing information, trace how its output may become a physical action,
and decide what belongs inside the system being engineered.

### Decision and Artifact

**Decision.** Decide whether the system belongs in scope and choose the boundary
that must be engineered.

**Artifact.** A loop charter containing the task, \(W_t\), observations, learned
proposal, authority path, allowed action, physical consequence, \(W_{t+1}\),
affected people, feedback path, assumptions, and chosen boundary.

### Claim Spine

1. A deployed model is not yet a physical-AI system.
2. The important transition occurs when a learned output crosses an authority
   boundary and can produce a physical consequence.
3. Feedback alone is insufficient because many digital and fixed-control systems
   alter their future inputs.
4. After establishing that a learned component materially influences the action
   path, ask whether the allowed action changes task-relevant physical state and
   can alter a later observation or choice, and whether the system exercises
   delegated physical authority over that action.
5. Action creates endogeneity. The system helps determine which states and data
   it encounters next.
6. The model remains one component among observation, state, runtime,
   enforcement, evidence, authority, and the world.
7. A system boundary is a defensible causal claim, not a box around deployed
   code.
8. Feedback and delegation impose different obligations. Either can fail while
   the other succeeds.

### Section Jobs

| Working section | Instructional job |
| --- | --- |
| The Endpoint Has Moved | Begin with the familiar inference pipeline and show why digital output is no longer the endpoint |
| When an Output Becomes an Action | Introduce the learned-component premise and two scope tests while distinguishing accepted action from model output |
| Action Changes What Comes Next | Make endogeneity concrete through policy-shaped state visitation and observations |
| The Model Inside the System | Place the learned component inside the full causal and authority path |
| Feedback Is Not Authority | Separate responsiveness to the world from permission to affect it |
| What This Book Borrows | Establish intellectual lineage and honest scope in one compact comparison |
| Draw the Boundary | Turn the unresolved obligations into the loop charter and the rest of the book's agenda |

### Required Representations

#### Matched-Deployment Figure

Show the same learned component in two deployments. In the first, its output is
advisory. In the second, an accepted proposal crosses an authority boundary,
produces \(u_t\), changes \(W_{t+1}\), and alters the next observation.

**Inference supported.** A model or device does not define physical AI. The
causal and authority path does.

#### Scope-Test Table

Compare an advisory classifier, recommender, trading system, thermostat,
industrial inspection system, and shared-workspace handler across future-input
change, physical consequence, delegated authority, affected people, and scope
verdict.

**Inference supported.** Consequential physical feedback and delegated physical authority are
separate classification dimensions.

#### Loop-Charter Schema

Provide exact fields and one completed entry for the canonical case.

**Inference supported.** The chapter's boundary decision produces an auditable
engineering artifact.

The neighboring-disciplines table is secondary. It should establish lineage and
exclusions without becoming the chapter's main argument.

### Source Families

- feedback, cybernetics, control, and cyber-physical systems;
- causal inference and sequential decision-making;
- imitation learning and policy-induced distribution shift;
- sociotechnical system boundaries and human-automation authority; and
- machine learning systems deployment and lifecycle work.

The source packet must distinguish established concepts from the book's
integrating synthesis.

### Shallow Treatments to Reject

- “Robot plus model equals physical AI.”
- “Any feedback loop equals physical AI.”
- “Machine learning systems are all open loop.”
- A generic circular diagram that returns to the same unchanged world.
- A manifesto about field names without an operational scope test.
- A long neighboring-fields survey that delays the chapter's decision.

### Deliberate Deferrals

- timescales, deadlines, and freshness thresholds to Chapter 2;
- measurement and statistical evidence to Chapter 3;
- services, queues, and lifecycle to Chapter 4;
- observation and belief semantics to Chapters 5 and 6;
- VLM and VLA interfaces to Chapter 7;
- enforcement and safe sets to Chapter 8; and
- detailed human authority and revocation to Chapter 11.

### Acceptance Test

Give the reader several systems that use the same model. The reader must classify
them, identify ambiguous cases, draw the complete causal and authority path, and
defend the chosen boundary without relying on the presence of a robot.

## Chapter 2 — What the Physical World Costs

### Objective Callout

After this chapter, you will be able to determine how quickly the system must
observe and act, how old its information may be, what task performance is
acceptable, and which conditions it can handle.

### Decision and Artifact

**Decision.** State the conditions in which the system is expected to work and
the requirements and assumptions that apply there.

**Artifact.** A requirements ledger containing the relevant world variable,
regime, timescale, freshness limit, response deadline, efficacy floor,
consequence horizon, resource constraints, and assumptions.

### Claim Spine

1. Requirements begin with task dynamics and consequences.
2. The world rarely has one universal timescale. The engineer must name the
   state variable, event, regime, and consequence that make a timescale relevant.
3. Sampling period, inference latency, information age, jitter, response
   deadline, and consequence horizon are different quantities.
4. The value of information is task-dependent. Age is a useful surrogate, not a
   universal measure, and value need not always decay monotonically.
5. Waiting can reduce observation uncertainty while increasing staleness.
6. Prediction recovers only the predictable component of delayed state.
7. Path dependence and shrinking recovery margin make delay consequential, but
   action is not universally irreversible.
8. Requirements must include assumptions, thresholds, and an efficacy floor.
9. World-derived requirements and platform-imposed resource constraints must
   remain distinguishable.

### Section Jobs

| Working section | Instructional job |
| --- | --- |
| The World Sets the Clock | Derive time pressure from a named physical variable and consequence |
| Information Ages | Distinguish event time, arrival, decision, actuation, age, and useful lifetime |
| Partial State, Not Complete Knowledge | Expose the wait-versus-act tradeoff without teaching the estimator |
| Action Changes What Comes Next | Apply Chapter 1 endogeneity briefly to requirement derivation |
| Consequences Accumulate | Replace universal irreversibility with lost options and increasing recovery cost |
| Prediction Buys Back the Predictable Part | Bound what prediction can recover from delay |
| Physical Budgets Interact | Record coupled constraints without solving placement |
| From Consequence to Requirement | Produce the ledger through a repeatable procedure |
| State the Claim at the Strength You Have | Qualify the resulting relationships without preempting Chapter 3 |

### Required Representations

#### Timing Plate

Show sample time, arrival time, decision time, actuation time, information age,
update period, response deadline, and consequence horizon on one physical
timeline.

**Inference supported.** These quantities describe different aspects of the
loop and cannot be exchanged casually.

#### Task Success as Information Ages

Plot task efficacy against information age for slow and fast regimes. Include an
efficacy floor and a prediction-assisted curve with residual uncertainty.

**Inference supported.** The maximum useful information age depends on the task
and operating conditions, not on physical AI in general.

#### Definition Table

Compare world timescale, freshness limit, response deadline, update period,
consequence horizon, and efficacy floor.

**Inference supported.** Each field in the requirements ledger has a distinct
decision role.

#### Consequence-to-Requirement Procedure

Start with an undesirable consequence, identify the relevant world variable and
dynamics, declare the regime, derive thresholds, set an efficacy floor, and test
sensitivity to changed assumptions.

**Inference supported.** Requirements are derived arguments rather than guessed
numbers.

### Source Families

- Age of Information, Age of Incorrect Information, and value of information;
- sampled-data, delayed, and networked control systems;
- stochastic prediction under delay;
- real-time systems and deadline semantics;
- hazard analysis and time-to-consequence measures; and
- partial observability at the depth required for requirement derivation.

### Shallow Treatments to Reject

- “The world prices time” without a derivation.
- A universal freshness curve or physical-AI score.
- Conflating inference latency with information age.
- Claiming that intelligence can always or never compensate for delay.
- Repeating Chapter 1's endogeneity lesson.
- Optimizing hardware placement before Chapter 9.

### Deliberate Deferrals

- measurement, calibration, and evidence strength to Chapter 3;
- queue and cadence design to Chapter 4;
- sensing operating points to Chapter 5;
- estimator construction to Chapter 6;
- policy chunks and asynchronous execution to Chapter 7;
- stopping envelopes and runtime assurance to Chapter 8; and
- resource optimization and placement to Chapter 9.

### Acceptance Test

Give the reader one learned capability in a slow inspection regime and a fast
interception regime. The reader must produce different requirements, explain
which assumptions caused the difference, and state what evidence would be
needed before either number could be trusted.

## Chapter 3 — Measuring a Moving System

### Objective Callout

After this chapter, you will be able to turn a system claim into something
measurable, instrument the complete path, describe both typical and worst-case
behavior with uncertainty, and decide whether the evidence supports the claim.

### Decision and Artifact

**Decision.** Accept, reject, or narrow the measured claim.

**Artifact.** A measurement plan and evidence record containing the property,
boundary, regime, operational definition, instrument, statistic, threshold,
uncertainty, efficacy floor, exclusions, and decision.

### Claim Spine

1. An engineering claim is a structured object rather than a slogan or number.
2. Instrumentation must surround the claimed phenomenon. A model timer cannot
   establish sensor-to-effect latency.
3. Physical events, software events, and clock domains must be connected.
4. A distribution is part of the behavior. Warm-up, tails, jitter, dependence,
   timeouts, and regime changes cannot be collapsed into a mean.
5. Failed and censored runs must remain visible.
6. Systems efficiency must stay paired with task efficacy.
7. Replay can establish repeatable benchmark claims. Live closed-loop evidence
   supports a different class of claim.
8. Diagnosis requires an intervention that can confirm or falsify the
   hypothesis.
9. The evidence record ends with accept, reject, or narrow. Missing evidence
   must be named.

### Section Jobs

| Working section | Instructional job |
| --- | --- |
| Claims Before Counters | Define the claim and decision before choosing instrumentation |
| Name the Property | Build a complete operational definition with units and regime |
| Draw the Measurement Boundary | Connect physical endpoints, software events, and clocks |
| Measure Distributions, Not Anecdotes | Preserve warm-up, tails, jitter, dependence, and failures |
| Keep Task Efficacy Beside Systems Cost | Prevent an inert or degraded system from winning |
| Know What Uncertainty Means | Separate repeatability, calibration, clock, environmental, and model effects |
| Replay Is Not the World | Scope claims to the apparatus and evidence class |
| Diagnose by Intervention | Turn hypothesis, bisect, and confirm into an executable method |
| Write the Evidence Record | Produce a verdict and expose the remaining uncertainty |

### Required Representations

#### Complete-Loop Measurement Figure

Show physical start and end events, internal timestamps, clocks, transport,
buffering, inference, command, actuator response, and an external reference.

**Inference supported.** The claimed boundary determines which measurements can
support the claim.

#### Decision-Changing Distribution

Use an ECDF or tail plot in which the mean passes but the required percentile
fails. Keep timeouts and efficacy visible.

**Inference supported.** Summary choice and omitted runs can reverse the
engineering verdict.

#### Evidence-Record Schema

Link each claim field to `REQ-`, `MEAS-`, and later records.

**Inference supported.** Evidence remains scoped, comparable, and traceable.

#### Diagnosis Algorithm

Specify symptom, hypothesis, causal partition, perturbation, expected response,
observation, and verdict.

**Inference supported.** Diagnosis changes a claim or design rather than ending
with a plausible story.

### Source Families

- metrology vocabulary and uncertainty guidance;
- experimental design and computer-systems performance evaluation;
- tail latency, coordinated omission, censoring, and dependent time series;
- timing instrumentation and clock synchronization;
- distributed tracing; and
- benchmark design and reproducibility.

### Shallow Treatments to Reject

- “Use p95 instead of the mean.”
- Tiny-sample percentile claims.
- Silent removal of timeouts and failed runs.
- Unsynchronized timestamps treated as ground truth.
- Instrumentation effects ignored on the critical path.
- Hypothesis, bisect, and confirm presented without a confirming intervention.
- Consuming Chapter 10 by treating one measurement as deployment assurance.

### Deliberate Deferrals

- runtime implementation of instrumentation to Chapter 4;
- sensor calibration and observation validity to Chapter 5;
- belief uncertainty to Chapter 6;
- scenario coverage and promotion to Chapter 10; and
- the release evidence case to Chapter 13.

### Acceptance Test

Provide two plausible measurements of the same system that disagree because
their boundaries, clocks, censoring, or regimes differ. The reader must diagnose
the disagreement and decide which claim, if either, remains supportable.

## Chapter 4 — A Runtime That Must Keep Running

### Objective Callout

After this chapter, you will be able to organize a continuously running system
so that sensing, state, action checks, and recovery continue to meet their
requirements when the learned component is late, stale, restarted, or
unavailable.

### Decision and Artifact

**Decision.** Choose service boundaries, cadences, state ownership, temporal
contracts, queue rules, degraded behavior, and recovery conditions.

**Artifact.** A continuous runtime skeleton containing services, lifecycle
states, owned state, event schemas, invariants, cadences, deadlines, queue and
ordering rules, observability, degraded behavior, and recovery conditions.

### Claim Spine

1. A physical-AI runtime is a continuing supervisory process rather than an
   inference endpoint.
2. Required responsibilities persist when the learned service does not.
3. Service boundaries follow cadence, state ownership, authority, failure
   containment, and recovery responsibility rather than fashion.
4. Multi-rate operation requires temporal contracts for event time, arrival,
   version, validity, deadline, and cancellation.
5. Backpressure cannot slow the physical world. Queues must be finite and stale
   work must be discarded.
6. Command delivery needs explicit duplicate, ordering, lease, and idempotency
   behavior.
7. Failure is an operating mode represented in runtime state.
8. Process restart and physical recovery are different operations.
9. The proposal boundary is an architectural seam here, not yet a safety
   guarantee.
10. Observability must survive the failure it is intended to explain.

### Section Jobs

| Working section | Instructional job |
| --- | --- |
| From Request to Continuous Process | Replace the inference-call mental model with continuous supervision |
| Responsibilities Before Services | Derive boundaries from timing, state, authority, failure, and recovery |
| Many Clocks, One Physical Loop | Establish multi-rate temporal contracts |
| State and Event Ownership | Prevent ambiguous truth and uncontrolled mutation |
| Backpressure Cannot Slow the World | Design finite queues, freshness checks, cancellation, and drop policy |
| The Proposal Boundary | Separate learned proposal from the path that may later authorize action |
| Failure Is an Operating Mode | Specify degraded states, fault ownership, and evidence preservation |
| Recovery Must Reconcile With the World | Re-establish body, world, pending-work, and authority state before resuming |

### Required Representations

#### Multi-Rate Runtime Timeline

Show acquisition, state maintenance, learned proposal, provisional permission
check, actuation, health monitoring, and logging at different cadences while the
policy stalls.

**Inference supported.** The system continues through a learned-component
failure because its responsibilities and clocks are not one inference call.

#### Service-Contract Table

Record owner, cadence, deadline, state, event-age rule, queue policy, ordering
semantics, failure assumption, degraded behavior, recovery condition, and
evidence emitted.

**Inference supported.** A service boundary is justified by a contract rather
than a diagram box.

#### Runtime Supervisor Algorithm

Specify inputs, lifecycle state, invariants, freshness and version checks,
timeout handling, degraded transitions, evidence preservation, recovery
reconciliation, and conditions for restored authority.

**Inference supported.** Failure and recovery become executable system behavior.

### Source Families

- real-time and fault-tolerant systems;
- reactive and cyber-physical systems;
- multi-rate scheduling and deadline semantics;
- event-stream, actor, and dataflow systems with finite queues and explicit overload behavior;
- messaging quality-of-service semantics as examples rather than architecture;
- fault, error, and failure taxonomies; and
- supervisory health management and runtime-assurance lineage at introductory
  depth.

### Shallow Treatments to Reject

- A bus, state store, and supervisor presented as a universal architecture.
- Watchdog restart treated as physical recovery.
- Unbounded queues or execution of stale completions.
- Exactly-once actuation assumed rather than specified.
- Every service assigned the same cadence.
- A hardware boundary described as automatically safe.
- “Safe continuity” claimed before Chapter 8 defines and enforces a safe set.

The defensible Chapter 4 claim is specified behavior during degradation, not completed
safety assurance.

### Deliberate Deferrals

- observation contracts to Chapter 5;
- belief, frames, clocks, and correction to Chapter 6;
- VLM and VLA intent, chunking, and abstention to Chapter 7;
- action limits, safe sets, fallback controllers, and enforcement to Chapter
  8;
- physical placement and failure-domain independence to Chapter 9; and
- assurance and promotion to Chapter 10.

### Acceptance Test

Give the reader a synchronous inference application and measured requirements
from Chapters 2 and 3. The reader must derive a continuous runtime, inject a late
or unavailable policy, show which responsibilities remain, and explain what must
happen before physical operation resumes.

## Foundation-Wave Integration Review

The four briefs pass together only if:

1. Chapter 1 produces the exact task, action, consequence, and boundary that
   Chapter 2 uses.
2. Chapter 2 produces requirements and thresholds that Chapter 3 can
   operationalize.
3. Chapter 3 produces evidence and instrumentation that Chapter 4 consumes.
4. Chapter 4 derives its invariants, cadences, and failure behavior from those
   accepted artifacts.
5. Proposal and allowed action remain distinct throughout.
6. No chapter uses VLM, VLA, hardware, or robotics novelty as its organizing
   argument.
7. The canonical case changes cumulatively rather than resetting.
8. The transfer cases prove that the method survives a different physical
   regime.

The next authoring action is WP0. Three workers should independently prepare the
scope-and-notation audit, canonical-case and traceability schema, and fault-and-
security thread. The architect then resolves those outputs into context packet
version 1 before Chapter 1 section briefs enter prose production.
