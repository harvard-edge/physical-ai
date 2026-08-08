# Chapter 2 Authoring Packet

**Packet:** `CTX-CH02-001`  
**Version:** 1.0.0  
**Status:** contract accepted; architecture candidate; manuscript drafting
blocked pending sources, representation review, and red team  
**Chapter:** What the Physical World Costs  
**Consumes:** `CTX-FND-001`, `LOOP-001`  
**Produces:** `REQ-001`  
**Canonical case:** `CASE-SWH-001@0.2`

## Chapter Contract

### Reader-Facing Objective

After this chapter, you will be able to determine how quickly the system must
observe and act, how old its information may be, what task performance is
acceptable, and which conditions it can handle.

### Entering State

The learner can identify proposal \(p_t\), the permission check, allowed action
\(u_t\), world states \(W_t\) and \(W_{t+1}\), physical consequence, affected
people, and the boundary recorded in `LOOP-001`.

The learner does not yet know how to derive a physical deadline, distinguish the
timing quantities in the loop, state a freshness threshold, define an efficacy
floor, validate a requirement, design runtime cadences, or choose placement.

No numeric requirement or measured value is accepted at entry.

### Misconception

The primary misconception is that model accuracy or additional computation is
the principal requirement and can compensate indefinitely for uncertainty or
delay.

Supporting misconceptions include:

- the world imposes one universal deadline;
- inference latency and information age are the same;
- every older observation loses value in the same way;
- waiting always improves a decision;
- prediction removes the cost of delay;
- every physical action is irreversible;
- platform constraints and world-derived requirements are interchangeable; and
- a requirement needs no operating regime or assumptions.

### Crux

The world determines when information ceases to support a useful or acceptable
action. A defensible requirement therefore names the physical variable,
consequence, operating regime, efficacy floor, and assumptions from which its
timing and resource limits were derived.

### Engineering Decision

State the conditions in which the system is expected to work and the
requirements and assumptions that must hold there. If those conditions cannot
be defended, narrow the task or allowed action rather than inventing a
threshold.

### Dossier Delta

Create `REQ-001`, the requirements and assumptions ledger for
`CASE-SWH-001@0.2`.

### Accepted Exit State

Chapter 3 may assume a named physical variable and regime, world timescale,
candidate freshness limit, response deadline, consequence horizon, efficacy
measure and floor, separated world and platform constraints, assumptions,
sensitivity questions, and explicit claims that require evidence.

## Concept Ownership

### Owned Here

| Concept | Instructional depth |
| --- | --- |
| Operating regime | Conditions under which a requirement claim is intended to hold |
| Relevant world variable | The state variable whose change makes age or response consequential |
| World timescale | Task- and regime-specific interval associated with meaningful physical change |
| Information age | Time from a declared information-generation event to a declared use point |
| Update period | Time between updates, distinct from age and latency |
| Response deadline | Latest acceptable response relative to a declared event |
| Freshness limit | Maximum accepted information age for a stated decision and regime |
| Partial-information decision | Wait-versus-act tradeoff without estimator construction |
| Consequence horizon | Interval before an undesirable consequence or material loss of recovery margin |
| Recovery margin | Remaining opportunity to avoid or limit a consequence |
| Prediction under delay | Recovery of only the component that remains predictable |
| World requirement versus platform constraint | Task necessity separated from implementation limitation |
| Efficacy floor | Minimum useful task behavior an optimization must preserve |
| Consequence-to-requirement procedure | Repeatable derivation from regime and consequence to requirement |
| Claim strength | Established, analytical, empirical, heuristic, or explanatory status |

### Borrowed

- consequential physical loop, endogeneity, affected people, and authority
  boundary from Chapter 1;
- partial observability and value-of-information ideas at introductory depth;
- delayed and sampled physical-system lineage;
- prediction under uncertainty;
- hazard and time-to-consequence reasoning; and
- energy, bandwidth, memory, and data movement as systems constraints.

### Deferred

- measurement design, calibration, distributions, and uncertainty to Chapter 3;
- services, queues, cancellation, and recovery to Chapter 4;
- sensor operating points to Chapter 5;
- belief construction and correction to Chapter 6;
- VLM and VLA context, chunks, and validity to Chapter 7;
- stopping envelopes and runtime assurance to Chapter 8;
- placement to Chapter 9;
- scenario coverage and promotion to Chapter 10; and
- release evidence to Chapter 13.

Chapter 2 may create requirements these chapters later satisfy. It may not solve
their owned design problems.

## Claim Spine

1. Requirements begin with a task-relevant physical variable and consequence,
   not a processor.
2. A world rarely presents one universal timescale. The relevant interval
   depends on the variable, event, regime, action, and consequence.
3. Sampling time, information age, update period, inference latency, response
   deadline, and consequence horizon describe different intervals.
4. Information usefulness is task-dependent. Age is often informative, but it
   is not a universal value function.
5. Waiting can reduce some uncertainty while increasing age and consuming
   response margin.
6. An allowed action changes later state and may reduce options or increase
   recovery cost.
7. Prediction compensates only for the component that remains predictable.
8. World requirements and platform constraints interact but answer different
   questions.
9. A requirement records assumptions, efficacy floor, sensitivity, and evidence
   need.
10. The result is a candidate claim. Chapter 3 decides whether evidence supports
    it.

## Section Briefs

### `SEC-CH02-01` — The World Sets the Clock

**Reader before.** Requirements begin from model runtime or processor capacity.

**Job.** Name the task-relevant physical variable, important event, consequence,
and operating regime. Introduce world timescale as a property of the declared
situation rather than a universal constant.

**Case move.** Compare routine sorting in a clear workspace with a regime in
which a person or object can enter the action corridor after observation.

**Reader after.** The learner can state which variable creates time pressure,
under which regime, and because of which consequence.

### `SEC-CH02-02` — Information Ages

**Reader before.** Every duration is called latency.

**Job.** Separate event, observation generation, arrival, decision, action issue,
physical effect, update period, information age, response deadline, and
consequence horizon.

**Case move.** Follow one workspace observation from acquisition to physical
use while the workspace can change during transport, inference, authorization,
and actuation.

**Reader after.** The learner can label each timing quantity and explain why it
cannot substitute for another without an explicit relationship.

### `SEC-CH02-03` — Partial State, Not Complete Knowledge

**Reader before.** Waiting for newer or more complete information always appears
preferable.

**Job.** Establish the wait-versus-act tradeoff. Waiting may reduce one
uncertainty while increasing age, consuming margin, or allowing a regime change.

**Case move.** Another observation may resolve object identity but arrive after
the person or object has moved again.

**Reader after.** “Wait for certainty” and “act immediately” are both recognized
as incomplete policies.

### `SEC-CH02-04` — Action Changes What Comes Next

**Reader before.** Endogeneity is understood but not connected to requirement
derivation.

**Job.** Apply Chapter 1 once. Show that action changes visibility, state
visitation, later data, and response opportunities.

**Case move.** Moving one object can reveal another, occlude a hand, block a
zone, or create a different pickup configuration.

**Reader after.** The learner can identify which assumptions depend on the
planned action class.

### `SEC-CH02-05` — Consequences Accumulate

**Reader before.** Every action is described as irreversible or immediately
hazardous.

**Job.** Replace universal irreversibility with lost options, increasing
recovery cost, consumed margin, and consequence horizon.

**Case move.** A misplaced object may remain reversible while becoming harder to
recover after it blocks another object, enters shared space, or leaves view.

**Reader after.** The learner can state a consequence and remaining recovery
interval precisely.

### `SEC-CH02-06` — Prediction Buys Back the Predictable Part

**Reader before.** Prediction either eliminates staleness or is useless because
it is imperfect.

**Job.** Separate predictable evolution from residual uncertainty, disturbance,
other-agent behavior, and regime change.

**Case move.** Predict regular object motion, then contrast it with a person
entering or moving the object unexpectedly.

**Reader after.** The learner can state when prediction may relax a requirement
and what prevents that relaxation.

### `SEC-CH02-07` — Physical Budgets Interact

**Reader before.** Time, energy, bandwidth, uncertainty, and authority appear
independent or equally world-derived.

**Job.** Separate world requirements from implementation constraints and show
their interactions without choosing placement.

**Case move.** Increasing acquisition rate may improve freshness while spending
energy and bandwidth. Hosted semantic reasoning may consume response margin and
move sensitive data.

**Reader after.** The learner can label the source and decision role of each
limit.

### `SEC-CH02-08` — From Consequence to Requirement

**Reader before.** The ingredients are understood but no repeatable artifact
exists.

**Job.** Apply `REP-CH02-ALG-001` to derive `REQ-001`.

1. Name the task and allowed action class from `LOOP-001`.
2. Name the physical variable whose change can invalidate the action.
3. Declare the operating regime.
4. State the undesirable consequence and affected role.
5. Identify the world timescale and consequence horizon.
6. Define the efficacy property and floor.
7. Derive candidate freshness and response requirements.
8. Record resource and authority constraints separately.
9. State prediction and disturbance assumptions.
10. Vary assumptions and identify the binding requirement.
11. Record what Chapter 3 must measure.

**Case move.** Produce the first `REQ-001` using symbolic values or explicitly
labeled analytical examples. No value is called measured.

**Reader after.** The learner can produce an auditable ledger instead of a list
of guessed targets.

### `SEC-CH02-09` — State the Claim at the Strength You Have

**Reader before.** An analytical derivation or heuristic may be mistaken for an
empirically established limit.

**Job.** Classify each requirement as definition-backed, analytical under
assumptions, empirically observed, engineering heuristic, or explanatory model.

**Case move.** Mark every `REQ-001` entry with its current claim class and
verification state.

**Reader after.** The learner can state what the ledger claims, what remains
hypothetical, and which evidence would change the decision.

## `REQ-001` Schema

### Identity and Traceability

- artifact, case, version, chapter, owner, and status;
- upstream `LOOP-001`;
- downstream `MEAS-001` and `RUN-001`; and
- claim and representation references.

### Task and Regime

- task and allowed action class;
- affected roles and authority assumptions;
- regime name, included and excluded conditions;
- relevant variables and triggering events;
- considered and excluded disturbances; and
- transition out of regime.

### Timing Model

- physical event, observation generation, use, action issue, and physical effect
  definitions;
- world timescale `REQ-001-R01`;
- update period `REQ-001-R02`;
- freshness limit `REQ-001-R03`;
- response deadline `REQ-001-R04`; and
- consequence horizon `REQ-001-R05`.

Every field records value, unit, regime, derivation, assumptions, and evidence
status.

### Efficacy and Resources

- task-efficacy property and operationalization question;
- efficacy floor `REQ-001-R06`;
- null or do-nothing baseline;
- energy, data movement, compute, and memory constraints;
- source of each constraint; and
- unacceptable tradeoffs.

### Prediction and Sensitivity

- predictable component, residual uncertainty, and valid regime;
- disturbance assumptions;
- any proposed requirement relaxation;
- assumptions varied and resulting requirement changes; and
- binding requirement.

### Requirement Record

Each record contains:

- identifier and statement;
- source type, physical variable, quantity, threshold, and unit;
- regime, consequence, efficacy reference, and derivation;
- assumptions and sensitivity;
- claim class and evidence needed;
- verification status; and
- downstream consumers.

### Decision

- selected regime;
- accepted, provisional, and rejected requirements;
- narrowed task or authority if necessary;
- rationale; and
- condition that would reverse the choice.

## Representation Briefs

### `REP-CH02-FIG-001` — Physical Timing Plate

Show the physical event, observation generation, arrival, decision, action
issue, physical effect, next observation, information-age interval, update
period, response deadline, consequence horizon, and shrinking recovery margin.

**Inference.** Low model latency can coexist with stale information or a missed
physical deadline.

### `REP-CH02-PLOT-001` — Task Success as Information Ages

Show at least two regimes, an efficacy floor, candidate freshness crossing,
prediction-assisted case, and residual uncertainty. Label it analytical or
schematic until Chapter 3.

**Inference.** The maximum useful information age depends on the task and
operating conditions.

### `REP-CH02-TBL-001` — Timing and Requirement Definitions

Compare what each quantity begins and ends at, the question it answers, what it
depends on, its common confusion, and its `REQ-001` field.

**Inference.** Each timing and efficacy field has a distinct decision role.

### `REP-CH02-ALG-001` — Consequence-to-Requirement Procedure

Consume `LOOP-001` and produce `REQ-001`, the selected regime, candidate
thresholds, narrowed task or authority if needed, and Chapter 3 questions.

**Invariant.** Every threshold traces to a consequence, efficacy property,
regime, and assumption.

### `REP-CH02-EQN-001` — Loop Fit Diagnostic

\[
\eta_{\mathrm{loop}} = \frac{L_q}{T_{\mathrm{world}}}
\]

The ratio is a regime-specific sensitivity diagnostic. It has no universal pass
threshold and does not replace efficacy, uncertainty, consequence, or authority
analysis. \(L_q\) remains unestablished until Chapter 3.

## Transfer Check

Use the same learned localization capability in a slow stationary-inspection
task and a fast package-interception task. For each, name the physical variable,
regime, consequence, world timescale, freshness limit, response deadline,
efficacy floor, prediction and disturbance assumptions, binding requirement,
provisional values, and Chapter 3 measurements.

The response passes only if the deployments receive materially different
requirements because their physical regimes differ. No threshold may be copied
from the canonical case or presented as measured.

## Decision Callout Contract

State the conditions in which age, response, task performance, and consequence
requirements can be stated honestly. If the assumptions cannot be defended,
narrow the task or allowed action instead of inventing a threshold. Record the
decision, assumptions, and unresolved evidence needs in `REQ-001`.

## Lab Boundary

### Phenomenon

The same proposal succeeds when the world changes slowly and fails when the
observation becomes old relative to the chosen regime.

### Perturbation and Alternative

Increase observation age under a fixed regime. As alternatives, change the
physical regime with the software path fixed or add prediction under declared
disturbance assumptions. Use a refreshed observation with similar computation
time as a negative control.

### Evidence Boundary

The lab uses supplied timestamps and an explicit measurement boundary. Chapter
3 owns the design and audit of that instrumentation. Record age, efficacy,
regime, assumptions, and visible failures without making a universal claim.

### Native Failures

- configured delay is confused with actual information age;
- prediction fails after an unmodeled workspace change; or
- the selected freshness limit does not preserve the efficacy floor.

### Decision and Dossier

Choose a faster path, prediction for a stated time horizon, reduced action authority, slower
physical regime, or refusal of the task. Update `REQ-001` with the candidate
requirement, regime, efficacy floor, assumptions, evidence limits, and decision.

The analytical, hosted, and physical forms must test this same reasoning. The
lab may not introduce calibration, statistical uncertainty methods, queues,
estimator construction, action limits, or deployment assurance.

## Unresolved Source Queue

| Claim | Question to resolve |
| --- | --- |
| Physical requirements depend on a named variable, consequence, and regime | Which real-time, control, CPS, or systems sources best support the components? |
| Information age differs from latency, period, and deadline | Which formal age definition fits sensed physical observations and exposure intervals? |
| Waiting can reduce uncertainty while consuming freshness | What source establishes the tradeoff without requiring a full POMDP treatment? |
| Recovery cost can rise while physical reversal remains possible | Which resilience, hazard, or planning lineage supports the distinction? |
| Prediction recovers only the predictable component | Which formulation remains accurate across predictor classes and disturbances? |
| World requirements and platform constraints have different origins | Which authoritative terminology distinguishes requirement, constraint, assumption, and choice? |
| The loop ratio is useful only as a regime-specific diagnostic | Is there precedent, or must it remain explicit book synthesis? |
| Requirement claims need strength labels | Which measurement or engineering taxonomy should anchor the distinction? |

## Draft Authorization State

The objective, decision, dossier schema, section sequence, transfer task, and lab
boundary are accepted as an architecture candidate. Drafting remains blocked
until sources are verified, representations pass review, an independent red
team closes blocking findings, and an accepted context delta produces packet
version 1.1.0.
