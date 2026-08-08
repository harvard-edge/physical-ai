# Physical AI Chapter Outlines

**Status:** canonical drafting scaffold
**Book:** *Physical AI: Machine Learning Systems That Sense and Act*
**Backward-design source:** `BOOK-GOAL.md`

## How to Use This Scaffold

This document states what every chapter must teach before prose or lab design
begins. A chapter steward may improve a heading, example, or explanatory route,
but may not silently change the objective, concept ownership, engineering
decision, dossier artifact, or dependency graph.

The section titles are working titles. They should become natural manuscript
headings rather than a repeated template. The instructional sequence is binding
because later chapters assume it.

Every numbered chapter contains:

1. one chapter-opening question;
2. an observable objective;
3. an entering learner and dossier state;
4. one misconception to overturn;
5. one load-bearing claim;
6. concepts taught to the depth required by the decision;
7. a quantitative or representational tool;
8. a chapter-specific engineering decision;
9. one update to the cumulative design dossier;
10. a transfer task using an unfamiliar case;
11. an end-of-chapter lab contract that realizes already-complete teaching.

These are editorial controls, not a visible chapter template. A finished
chapter normally exposes a natural opening, one compact learning-objective
callout, chapter-specific sections, a decision callout that records the dossier
update, a transfer check woven into the argument, and the lab as the final
element. Opening question, entering state, misconception, crux, artifact delta,
and chapter dependency remain in the authoring packet. Their labels must not
leak into the manuscript. A question callout is optional rather than mandatory.

## The Dependency

> **Frame → specify → measure → architect → observe → estimate → propose →
> enforce → place → qualify → authorize → change → deploy**

| **Chapter** | **Capability Added** | **Dossier Artifact** |
|---:|---|---|
| 1 | Frame | Loop charter |
| 2 | Specify | Requirements and assumptions ledger |
| 3 | Measure | Measurement plan and evidence record |
| 4 | Architect | Continuous runtime skeleton |
| 5 | Observe | Observation contract |
| 6 | Estimate | State, frames, and timing model |
| 7 | Propose | Policy interface and intent contract |
| 8 | Enforce | Action limits and independent checking design |
| 9 | Place | Placement map and resource ledger |
| 10 | Qualify | Assurance plan and promotion record |
| 11 | Authorize | Human-authority map |
| 12 | Change | Governed data and update record |
| 13 | Deploy | Integrated deployment case |

The unnumbered final design review integrates these artifacts. It introduces no
new concept.

## Part I — From ML Systems to Physical AI

### Chapter 1 — From ML Systems to Physical AI

**Opening question.** When does a machine learning system become a physical-AI
system?

**Objective.** Given an unfamiliar system description, the reader can tell when
a learned system is doing more than producing information, trace how its output
may become a physical action, and decide what belongs inside the system being
engineered.

**Entering state.** The reader understands ordinary inference pipelines,
deployed software services, sensors, and actuators. No robotics or control theory
is assumed.

**Misconception.** Physical AI means placing a capable model on a robot or other
physical device.

**Crux.** Begin with a learned-component premise. The component must materially
influence the action path. The system then enters this book's scope when an
allowed action changes task-relevant physical state and can alter a later
observation or choice, and the system exercises delegated physical authority
over that action.

#### Required Sections

1. **The Endpoint Has Moved**
   Begin with the familiar ML systems pipeline. Show why prediction is no longer
   the endpoint after an output produces physical action.

2. **When an Output Becomes an Action**
   Establish the learned-component premise, consequential-physical-feedback
   test, and delegated-physical-authority test. Distinguish proposal from
   allowed action without relying on the presence of a robot, sensor, or
   actuator.

3. **Action Changes What Comes Next**
   Introduce endogeneity. The policy influences the states it visits and the
   observations from which it will later decide.

4. **The Model Inside the System**
   Place the model among sensing, state, runtime, enforcement, evidence, human
   authority, and the world.

5. **Feedback Is Not Authority**
   Introduce the two constraints that organize the book. Feedback governs how
   the system remains coupled to a changing world. Delegation governs the
   authority granted to it.

6. **What This Book Borrows**
   Position the book honestly relative to ML systems, robotics, control,
   embedded systems, cyber-physical systems, safety engineering, and HCI.

7. **Draw the Boundary**
   Preview the requirements, evidence, interfaces, limits, authority, and release
   decision the remaining chapters will construct.

#### Required Teaching Artifacts

- **Primary figure:** open-loop digital output beside a two-world-state physical
  loop, \(W_t\) to \(W_{t+1}\).
- **Table:** neighboring disciplines, what each contributes, and what this book
  assumes rather than reteaches.
- **Representation:** causal loop and authority boundary.
- **Algorithm:** none. Classification and boundary judgment are the work.

**Engineering decision.** Decide whether the problem belongs inside the book's
scope and choose the causal and authority boundary that must be engineered.

**Dossier artifact.** A loop charter containing the task, world states, learned
component, observation, proposal, accepting person or permission check, allowed action,
affected people, feedback path, assumptions, and chosen boundary.

**Transfer task.** Classify several systems that use identical models in
different contexts, including one open-loop advisory system and one system whose
accepted output changes later observations.

**End-of-chapter lab handoff.** Use the same learned component in advisory and
closed-loop modes. Make divergence visible, perturb the action path, record how
later observations change, and defend the classification. The lab must not
introduce causal closure for the first time.

---

### Chapter 2 — What the Physical World Costs

**Opening question.** What requirements does the world impose before the
hardware or model has been chosen?

**Objective.** Given a task and environment, the reader can determine how
quickly the system must observe and act, how old its information may be, what
task performance is acceptable, and which conditions it can handle.

**Entering state.** The loop charter from Chapter 1.

**Misconception.** Model quality is the principal requirement, and additional
computation can compensate indefinitely for uncertainty or delay.

**Crux.** The world determines how long information remains useful and how much
margin an action can safely consume.

#### Required Sections

1. **The World Sets the Clock**
   Derive deadlines from motion, process dynamics, human response, and time to
   consequence rather than from processor speed.

2. **Information Ages**
   Introduce observation age, freshness, and task-dependent value decay.

3. **Partial State, Not Complete Knowledge**
   Explain why the system often must act before perfect information is
   available.

4. **Action Changes What Comes Next**
   Deepen endogeneity through path-dependent data, changing visibility, and
   policy-induced state visitation.

5. **Consequences Accumulate**
   Replace careless claims of universal irreversibility with lost options,
   increasing recovery cost, and shrinking safety margin.

6. **Prediction Buys Back the Predictable Part**
   Show what prediction can and cannot recover from delay. Reserve estimator
   construction for Chapter 6.

7. **Physical Budgets Interact**
   Connect time, energy, bandwidth, uncertainty, action authority, and
   consequence without prematurely solving placement.

8. **From Consequence to Requirement**
   Convert the task into a freshness limit, efficacy floor, energy and data
   budgets, consequence threshold, and operating assumptions.

9. **State the Claim at the Strength You Have**
   Separate theorem-backed results, empirical relationships, engineering
   heuristics, and explanatory metaphors.

#### Required Teaching Artifacts

- **Primary figure:** task efficacy versus information age with a measured or
  analytical knee and named operating regimes.
- **Table:** physical cost, operational measure, consequence, and assumption.
- **Equation:**

  \[
  \eta_{\mathrm{loop}} =
  \frac{\text{specified loop-latency percentile}}
       {\text{task-specific world timescale}}
  \]

  Present the ratio as a diagnostic for one loop and regime, not a universal
  score.
- **Representation:** requirements and assumptions ledger.
- **Algorithm:** consequence-to-requirement derivation checklist.

**Engineering decision.** State the conditions in which the system is expected
to work and the requirements it must meet there.

**Dossier artifact.** Requirements ledger containing world timescale, freshness
limit, efficacy floor, energy and data budgets, consequence horizon, allowed
action class, and assumptions.

**Transfer task.** Derive different requirements for the same learned capability
used in a slow inspection process and a fast physical interception task.

**End-of-chapter lab handoff.** Increase information age under controlled
conditions, measure task success, find when the information becomes too old,
and choose among a faster path, prediction, less action authority, slower
motion, or refusal of the task.

## Part II — Measure and Run

### Chapter 3 — Measuring a Moving System

**Opening question.** What evidence would make a claim about the running loop
believable?

**Objective.** Given a proposed system property, the reader can turn it into
something measurable, instrument the complete path, describe typical and
worst-case behavior with uncertainty, and accept, reject, or narrow the claim.

**Entering state.** Requirements, thresholds, and assumptions from Chapter 2.
Basic descriptive statistics are helpful but not required.

**Misconception.** A mean latency from an internal timer and a successful
demonstration provide sufficient systems evidence.

**Crux.** A measurement is useful only when its boundary, regime, uncertainty,
and decision consequence match the claim.

#### Required Sections

1. **Turn a Property Into a Claim**
   Define the phenomenon, quantity, unit, regime, threshold, and decision before
   collecting data.

2. **Instrument the Boundary**
   Identify where the complete sense-to-consequence path begins and ends. Explain
   why convenient component timing can miss transport, buffering, and actuation.

3. **Measure a Distribution**
   Teach tails, jitter, correlation, warm-up behavior, and regime changes.

4. **Keep the Task Honest**
   Pair resource or latency measurements with task efficacy so an inert or
   degraded system cannot appear optimal.

5. **Account for the Instrument**
   Cover calibration, timebase, synchronization, observer effects, negative
   controls, and independent references.

6. **Express Uncertainty**
   Distinguish run-to-run variation, instrument uncertainty, environmental
   variation, and uncertainty caused by limited coverage.

7. **Replay and Live Operation Are Different Evidence**
   Separate repeatable benchmark evidence from fixed-rig and live closed-loop
   characterization.

8. **Diagnose Before Explaining**
   Introduce hypothesis, bisect, and confirm as the book's reusable failure
   diagnosis method.

9. **The Evidence Record**
   Define the common record containing claim, operational definition, setup,
   versions, regime, result, uncertainty, counterevidence, and verdict.

#### Required Teaching Artifacts

- **Primary figure:** measurement points around the complete loop boundary.
- **Measured figure:** distribution whose tail changes the engineering decision.
- **Table:** claim, metric, unit, boundary, regime, uncertainty, efficacy, and
  decision threshold.
- **Algorithm:** hypothesis → bisect → confirm.
- **Representation:** evidence record schema.

**Engineering decision.** Accept, reject, or narrow the claim supported by the
measurement.

**Dossier artifact.** Instrumentation plan, measurement schema, and first
evidence record.

**Transfer task.** Diagnose why two teams measuring “loop latency” report
incompatible numbers despite using the same model and hardware.

**End-of-chapter lab handoff.** Produce a complete evidence record with a
predeclared prediction, external reference where needed, negative control,
uncertainty, minimum acceptable task performance, diagnosed discrepancy, and
written verdict.

---

### Chapter 4 — A Runtime That Must Keep Running

**Opening question.** What must continue to operate when the learned component
does not?

**Objective.** Given measured requirements, the reader can organize a
continuously running system so that sensing, state, action checks, and recovery
continue to meet their requirements when the learned component is late, stale,
restarted, or unavailable.

**Entering state.** The requirements ledger and measurement discipline.

**Misconception.** A physical-AI runtime is an inference call repeated inside a
request-response application.

**Crux.** A physical system is a living process whose responsibilities continue
across late inference, missing data, restart, partial availability, and recovery.

#### Required Sections

1. **Beyond Request and Response**
   Establish continuity, lifecycle, unattended operation, and state across
   interactions.

2. **Derive Services From Responsibilities**
   Decompose by cadence, state ownership, privilege, failure containment, and
   recovery rather than by arbitrary software modules.

3. **Many Loops, Many Cadences**
   Distinguish acquisition, estimation, policy, enforcement, actuation, logging,
   health monitoring, and learning timescales.

4. **State, Events, and Backpressure**
   Cover event age, finite queues, latest-value semantics, overload, and stale
   work cancellation.

5. **The Proposal Boundary**
   Establish that learned reasoning proposes while another component decides
   whether the proposal may produce physical action.

6. **Failure as an Operating Mode**
   Treat timeout, stale input, service restart, loss of connectivity, and
   partial availability as runtime states.

7. **Recovery and Safe Continuity**
   Distinguish restarting software from recovering physical state and authority.

8. **Observability That Survives Failure**
   Embed the Chapter 3 evidence path without making instrumentation the cause of
   failure or losing the last useful state.

#### Required Teaching Artifacts

- **Primary figure:** multi-rate runtime with services, state, event paths, and
  the proposal boundary.
- **Supporting figure:** lifecycle state machine with degraded and recovery
  modes.
- **Table:** service, owner, cadence, deadline, state, input-age rule, failure,
  and fallback.
- **Algorithm:** runtime supervisor with freshness checks, timeouts, watchdogs,
  and recovery transitions.

**Engineering decision.** Choose service boundaries, state ownership, cadences,
queue policies, failure behavior, and the initial propose/dispose boundary.

**Dossier artifact.** Runtime skeleton, service contracts, lifecycle states, and
instrumentation points.

**Transfer task.** Redesign a synchronous model-serving application so that a
sensor, safety monitor, and actuator continue to meet their stated timing and
action requirements when the policy service hangs.

**End-of-chapter lab handoff.** Make a learned service late, hung, and then
unavailable. Measure event age and recovery, verify which responsibilities
continue to be met, and use the evidence record to diagnose the observed
failure.

## Part III — Sense, Estimate, Decide, Act

### Chapter 5 — Perception Under a Deadline

**Opening question.** Which observations are worth acquiring before they become
too expensive or too old to use?

**Objective.** Given sensors and task requirements, the reader can choose what
the system should sense and how often, balancing information age and quality
against energy, data movement, and what the sensors cannot observe.

**Entering state.** Runtime services, deadlines, operating assumptions, and a
valid measurement method.

**Misconception.** Sensors provide complete, neutral, and free inputs, and more
resolution or more modalities necessarily improve the physical system.

**Crux.** Perception is a timed acquisition decision whose costs begin before
inference and whose output is evidence, not world state.

#### Required Sections

1. **Observation Is a Design Choice**
   Separate the world from what the system elects and is able to observe.

2. **What Each Sensor Can and Cannot See**
   Teach complementarity, blind spots, contradiction, dropout, and visibility.

3. **Sampling the World**
   Connect sampling rate, exposure, field of view, resolution, and quantization
   to task dynamics.

4. **Active Perception**
   Show that aiming, moving, illuminating, or querying a sensor changes later
   observations and can spend action authority.

5. **The Cost Before Inference**
   Account for acquisition, conversion, transport, copying, buffering, and
   preprocessing.

6. **When a Model Interprets the Scene**
   Introduce detectors and VLM-assisted perception as black-box components with
   temporal context, latency, data-egress, uncertainty, and failure behavior.

7. **Freshness, Quality, Energy, and Bandwidth**
   Construct the measured operating frontier and identify dominated choices.

8. **The Observation Contract**
   Specify payload, source, timestamp, frame, age, quality or uncertainty,
   validity conditions, and missing-data behavior.

#### Required Teaching Artifacts

- **Primary figure:** measured operating frontier showing feasible and dominated
  sensing regimes.
- **Supporting figure:** acquisition-to-observation path with costs before model
  inference.
- **Table:** modality, field, cadence, data rate, blind spot, placement
  constraint, and failure behavior.
- **Equation:** sensor data-rate and observation-age calculations.
- **Representation:** observation contract.

**Engineering decision.** Choose the sensing strategy and operating point.
Whole-system compute placement remains provisional until Chapter 9.

**Dossier artifact.** Observation contract and sensing-service specification.

**Transfer task.** Choose observations for the same task under abundant local
power and under a strict energy and egress budget.

**End-of-chapter lab handoff.** Vary acquisition rate, resolution, preprocessing,
or semantic path. Measure task efficacy, observation age, energy, and data
movement, then defend an operating point rather than the highest-quality input.

---

### Chapter 6 — State, Time, and World Models

**Opening question.** What must the system believe now when every observation
describes a different place and time?

**Objective.** Given timestamped observations and actions, the reader can decide
what the system must keep track of, align measurements across space and time,
represent uncertainty, detect when the system's estimate is wrong, and correct
it.

**Entering state.** Observation contracts, runtime state ownership, and basic
probabilistic intuition.

**Misconception.** The latest observation is the current state, or a model's
context window is the system's world model.

**Crux.** The system acts from a time-indexed belief, not directly from raw
observations.

#### Required Sections

1. **Observation Is Not State**
   Separate a sample from a maintained belief about the world and the body.

2. **Frames Give Geometry Meaning**
   Introduce world, body, sensor, actuator, and task frames to the depth required
   for interface correctness.

3. **Clocks Give State Meaning**
   Cover timestamps, synchronization, age, delay, and out-of-order observations.

4. **Predict, Observe, Correct**
   Teach the estimator cycle using prior belief, action, new evidence, and
   correction.

5. **Belief Includes Uncertainty**
   Make uncertainty an explicit output consumed by policy, enforcement, and
   confidence decisions.

6. **Prediction and World Models**
   Define an operational world model as maintained belief and optional dynamics
   used for prediction. Distinguish it from a generative scenario model.

7. **The System Must Know Itself**
   Include embodiment, actuator state, resource state, health, and available
   skills when they constrain action.

8. **Detect When the Estimate Is Wrong**
   Use residuals to expose model-observation disagreement and trigger correction
   or degraded operation.

9. **What Must Persist Now**
   Bound the operational history needed for estimation. Reserve retained human
   data and training trajectories for Chapters 11 and 12.

#### Required Teaching Artifacts

- **Primary figure:** observation → transform and time alignment → belief →
  prediction → residual → correction.
- **Supporting figure:** frame graph with clock ownership.
- **Table:** observation, operational state, model context, retained memory, and
  training trajectory.
- **Equation:**

  \[
  x_{t+1}=f(x_t,u_t)+w_t,
  \qquad
  o_t=h(x_t)+v_t
  \]

- **Algorithm:** predict → observe → correct with innovation and stale-input
  handling.

**Engineering decision.** Choose state variables, frame conventions, update
cadence, uncertainty representation, drift threshold, and correction trigger.

**Dossier artifact.** Frames-and-timing model, state schema, estimator contract,
and uncertainty path.

**Transfer task.** Explain and correct failures caused by the same observation
arriving with a wrong frame, wrong timestamp, and underestimated uncertainty.

**End-of-chapter lab handoff.** Introduce one frame, clock, or belief error. Make
the resulting physical or simulated discrepancy visible, detect it through the
innovation, bisect the source, and choose a correction.

---

### Chapter 7 — From Meaning to Intent

**Opening question.** What must be true before a model's semantic output can
become a proposal for physical action?

**Objective.** Given a task, maintained belief, and candidate VLM or VLA, the
reader can define what the model receives and may propose, connect its proposal
to a particular body, choose how often it updates, and decide when the model
should decline or ask for help.

**Entering state.** Runtime services, observation and state contracts,
uncertainty, deadlines, and basic familiarity with vision and language models.

**Misconception.** A fluent VLM answer or plausible VLA output is grounded,
current, compatible with the body, and ready to execute.

**Crux.** A model produces a proposal that is valid only for a stated time and
context; it does not possess physical authority.

#### Required Sections

1. **From State to Task Meaning**
   Separate physical state from the entities, relationships, affordances, and
   goals relevant to a task.

2. **VLMs as Semantic Components**
   Teach inputs, temporal context, outputs, grounding limits, latency, egress,
   calibration, and failure without teaching transformer internals.

3. **VLAs as Policy Interfaces**
   Explain observation-to-action policies, temporal conditioning, and how their
   interface differs from descriptive models.

4. **Grounding the Goal**
   Bind language and task semantics to current entities, frames, capabilities,
   authority, and belief validity.

5. **Representing Action**
   Compare discrete tokens, continuous actions, joint-space and task-space
   commands, trajectories, action chunks, and named skills.

6. **What the Model Assumes About the Body**
   Make morphology, coordinate conventions, action normalization, available
   skills, and adapters explicit.

7. **Fast Policies and Slow Reasoning**
   Derive multi-rate semantic and policy paths from the deadlines established
   earlier.

8. **Action Chunks and Freshness**
   Treat chunk horizon, asynchronous inference, buffering, interruption,
   overlap, and stale-action risk as systems decisions.

9. **When the Model Should Decline or Ask for Help**
   Define behavior outside validated coverage, under stale belief, or when fast
   and slow paths disagree.

10. **Intent as a Proposal**
    Specify task, target, frame, skill, parameters, preconditions, validity
    horizon, confidence or support, and requested authority.

#### Required Teaching Artifacts

- **Primary figure:** maintained belief feeding contrasting VLM and VLA policy
  interfaces and producing expiring intent.
- **Timing figure:** observation age, inference overlap, action chunks,
  interruption, and replanning.
- **Table:** action representations and their consequences for embodiment,
  cadence, interruption, enforcement, and transfer.
- **Representation:** policy-interface card and intent contract.
- **Algorithm:** uncertainty, abstention, and escalation policy.

**Engineering decision.** Choose the semantic path, policy interface, action
abstraction, replanning cadence, validity horizon, and escalation behavior.

**Dossier artifact.** Policy-interface card and enforceable intent schema.

**Transfer task.** Compare two unfamiliar policies that solve the same task but
use different temporal context, action representations, and embodiment adapters.

**End-of-chapter lab handoff.** Run two meaning-to-intent paths against the same
belief and task. Measure grounding, latency, action validity, abstention, and
failure behavior. Choose an interface and escalation rule while keeping every
wrong output on the proposal side of the boundary.

---

### Chapter 8 — Keeping Action Within Limits

**Opening question.** What separates a capable proposal from permission to move
the physical system?

**Objective.** Given an intent contract and physical limits, the reader can give
each skill explicit limits, calculate whether an action can stop before causing
harm, decide where actions are checked, and specify what the system should do
when action cannot continue.

**Entering state.** Proposed intent, belief and uncertainty, deadlines, runtime
failure behavior, and embodiment state.

**Misconception.** A valid model output may be forwarded to an actuator, or
simple command clipping constitutes a complete safety mechanism.

**Crux.** Physical authority belongs to an enforceable action contract and a
trusted boundary, not to the component that generated the proposal.

#### Required Sections

1. **Intent Is Not Motion**
   Establish the semantic-to-physical boundary and the responsibilities on each
   side.

2. **Skills Need Clear Limits**
   Define preconditions, parameters, coordinate frame, termination, timeout,
   progress, interruption, and failure outcomes.

3. **The Inner Loop**
   Introduce tracking, feedback, cadence, error, and disturbance rejection only
   to the depth needed for systems decisions.

4. **Motion Uses Up Safety Margin**
   Connect delay, velocity, acceleration, braking capability, uncertainty, and
   action horizon.

5. **Limits Change With the Situation**
   Define allowed state-action regions, explicit limits, and invalid states.

6. **Check Actions While the System Runs**
   Introduce advanced proposal, trusted monitor, reversionary behavior, and safe
   set with honest lineage.

7. **Separate the Check From the Model**
   Determine what must not share a failure domain, privilege boundary, clock, or
   resource bottleneck with semantic reasoning.

8. **Stop, Hold, Retreat, or Continue**
   Distinguish stop, hold, retreat, release, and degraded continuation. Connect
   software recovery to physical recovery.

9. **Write Down What Each Skill May Do**
   Complete the proposal boundary introduced in Chapter 4 and make every command
   checkable.

#### Required Teaching Artifacts

- **Primary figure:** dashed learned proposal entering an independent action
  check and becoming either an allowed command or a visible refusal.
- **Supporting figure:** current action limits and stopping margin.
- **Table:** skill, precondition, limit, timeout, completion, fallback, and the
  component responsible for checking it.
- **Equation:**

  \[
  d_{\mathrm{required}}=
  v\,t_{\mathrm{delay}}+
  \frac{v^2}{2a_{\mathrm{brake}}}+
  d_{\mathrm{uncertainty}}
  \]

  Present it as an engineering bound, not a complete safety proof.
- **Algorithm:** validate, accept or veto, execute, monitor, interrupt, and
  recover.

**Engineering decision.** Choose the skill set, the limits that apply, the
component responsible for checking them, the safe response, and the recovery
policy.

**Dossier artifact.** Skill contracts, action limits, checking logic, and
recovery policy.

**Transfer task.** Determine how the same semantic intent requires different
skills, limits, and fallback behavior on two embodiments.

**End-of-chapter lab handoff.** Submit valid, invalid, and stale proposals,
including proposals outside the allowed limits. Measure refusal and stopping
behavior, diagnose one failure, and defend where the action check belongs.

## Part IV — The Whole System

### Chapter 9 — Where Intelligence Runs

**Opening question.** Where should each capability run when every placement
spends resources and changes a failure boundary?

**Objective.** Given the complete system and fixed resources, the reader can
decide where each part runs, identify the resources it consumes and the parts
that must not fail together, and predict what changes when one part moves.

**Entering state.** Measured contracts and cadences for sensing, estimation,
policy, enforcement, action, logging, and recovery.

**Misconception.** Components can be optimized independently, and “on device”
describes one homogeneous compute location.

**Crux.** Placement is a whole-system decision because capabilities share
resources, move data, fail together, and carry different authority.

#### Required Sections

1. **See the Whole Loop at Once**
   Assemble every prior contract into one causal and dataflow architecture.

2. **Compute Domains Have Different Jobs**
   Distinguish microcontroller, application processor, accelerator, local server,
   edge service, and hosted compute by behavior rather than brand.

3. **Measure Before Choosing Where It Runs**
   Record cadence, latency distribution, memory, energy, bandwidth, criticality,
   data sensitivity, and update requirements.

4. **Data Movement Is Work**
   Make acquisition, serialization, copying, synchronization, transport, and
   egress visible.

5. **Resources Are Shared**
   Introduce contention, interference, priority inversion, thermal limits, and
   coupled budgets.

6. **What Must Not Fail Together**
   Treat isolation, privilege, clocking, connectivity, and trusted execution as
   placement constraints.

7. **Local, Edge, and Hosted Tradeoffs**
   Evaluate capability, freshness, energy, privacy, cost, availability,
   maintainability, and updateability.

8. **Move One Thing and Follow the Ripple**
   Perform sensitivity analysis rather than comparing local component scores.

9. **Record Where Each Part Runs**
   Preserve alternatives, assumptions, evidence, binding constraints, and the
   condition that would force re-placement.

#### Required Teaching Artifacts

- **Primary figure:** complete loop mapped across compute, trust, and enforcement
  domains.
- **Supporting figure:** one re-placement and its ripple through latency, energy,
  data movement, failure, and authority.
- **Table:** capability, cadence, resource signature, sensitivity, criticality,
  trust requirement, candidate domain, and evidence.
- **Equation:** shared resource constraints such as

  \[
  \sum_i r_{i,k} \leq R_k
  \]

  supplemented by deadline, privacy, connectivity, and failure-domain
  constraints.
- **Algorithm:** placement and ripple audit.

**Engineering decision.** Choose and defend the whole-system placement map.

**Dossier artifact.** Placement map, shared-budget ledger, failure-domain map,
and sensitivity analysis.

**Transfer task.** Re-place a capability after connectivity, privacy, or energy
conditions change and explain every downstream consequence.

**End-of-chapter lab handoff.** Move one capability across available compute
domains. Measure the ripple through at least three system properties and one
failure behavior, then accept or reject the placement.

---

### Chapter 10 — Building Confidence Before Deployment

**Opening question.** What can each form of evidence actually justify before the
system encounters greater consequence?

**Objective.** Given a candidate system and its stated operating limits, the
reader can choose the right test for a claim, cover the situations that matter,
recognize when earlier evidence no longer applies, inject failures, and decide
whether the system is ready for more realistic use.

**Entering state.** Valid measurement, complete placement, operating limits,
enforcement, and recovery behavior.

**Misconception.** Offline, replay, simulation, or benchmark success proves
closed-loop readiness.

**Crux.** Evidence supports a specific claim, not the system in general. A
candidate may advance only when the current tier supports the declared claim
and the next exposure is controlled.

#### Required Sections

1. **A Candidate Needs a Specific Claim**
   State expected behavior, task, environment, users, operating limits, and
   exclusions before selecting tools.

2. **Metrics Do Not Prove System Behavior**
   Explain why component accuracy and fixed datasets do not establish system
   behavior.

3. **List the Situations That Matter**
   Define environment, people, task variation, dynamics, disturbances, failures,
   and boundary conditions.

4. **Test in Increasingly Realistic Conditions**
   Organize offline tests, simulation, replay, software-in-the-loop,
   hardware-in-the-loop, shadow operation, limited trials, and monitored use by
   the claims each can support.

5. **Know When Earlier Evidence No Longer Applies**
   Show how policy divergence and endogeneity limit counterfactual replay and
   simulation conclusions.

6. **Find Where Test Coverage Is Thin**
   Identify weakly supported regions, scenario gaps, and changes that invalidate
   prior evidence.

7. **Use World Models to Generate Test Scenarios**
   Treat generative world models and synthetic environments as tools for
   producing candidate scenarios, not as evidence by themselves.

8. **Inject Failures Deliberately**
   Test stale observation, service loss, contention, wrong belief, malformed
   proposal, enforcement delay, and connectivity failure.

9. **Decide Before You See the Results**
   Prevent post hoc acceptance and define what triggers hold, rejection, or
   rollback.

10. **Advance, Hold, or Reject**
    Make the exposure decision explicit, limited, and reversible.

#### Required Teaching Artifacts

- **Primary figure:** increasingly realistic test conditions with the claims
  each condition can and cannot support.
- **Supporting figure:** replay paths diverging after the candidate changes an
  action.
- **Table:** evidence tier, supported claim, unsupported claim, cost, realism,
  failure coverage, and promotion condition.
- **Representation:** scenario coverage table and test-advancement record.
- **Algorithm:** predeclared rules for advancing, holding, or rejecting a
  candidate.

**Engineering decision.** Advance the candidate to a more realistic test, keep
it at the current stage, or reject it.

**Dossier artifact.** Evaluation plan, scenario coverage, collected evidence,
failure-test record, and decision.

**Transfer task.** Decide whether apparently strong simulation and replay results
justify a limited live trial when the candidate policy changes state visitation.

**End-of-chapter lab handoff.** Create disagreement between offline and
closed-loop results. Explain why replay no longer supports the claim, inject a
relevant failure, and decide what test should come next.

## Part V — Authority, Learning, and Deployment

### Chapter 11 — Human Authority

**Opening question.** Who may teach, approve, interrupt, inspect, revoke, and
forget what this system does?

**Objective.** Given a use case and its stakeholders, the reader can decide who
may request, teach, approve, run, inspect, interrupt, revoke, retain, and forget,
and verify that stopping or revoking permission works quickly enough when it
matters.

**Entering state.** Complete system behavior, failure modes, assurance limits,
and the distinction between learned proposal and trusted enforcement.

**Misconception.** A human somewhere “in the loop” guarantees meaningful
oversight or control.

**Crux.** Human authority is an explicit system interface with scope, timing,
state, evidence, and revocation behavior.

#### Required Sections

1. **Authority Must Be Designed**
   Treat decision rights as a system property rather than as policy language
   added after implementation.

2. **Who Is Affected and Who Is Responsible**
   Identify operator, owner, developer, maintainer, bystander, data subject,
   dependent user, and accountable organization.

3. **Requesting, Teaching, and Approving Differ**
   Separate the ability to ask, demonstrate, label, authorize, and deploy a
   behavior.

4. **People Must Understand Before They Agree**
   Make system state, recording state, uncertainty, intent, authority, and
   consequence understandable to the relevant person.

5. **Intervene, Override, and Stop**
   Specify reachability, latency, priority, physical effect, and behavior when
   the human path fails.

6. **Revoke What Was Granted**
   Cover skill revocation, credential removal, model rollback, device removal,
   authority expiry, and incomplete revocation.

7. **Inspect, Correct, and Forget**
   Place retained preferences, interaction records, and personal data under
   inspectable and testable control.

8. **Permission Has Scope and Duration**
   Bind consent to purpose, person, place, data, action, recipient, and time.

9. **When Services Disappear**
   Address offline continuity, portability, ownership, dependency exit, and the
   loss of a hosted capability.

10. **The Authority Map**
    Record who may perform each operation, under which conditions, with which
    evidence, override, expiry, and audit trail.

#### Required Teaching Artifacts

- **Primary figure:** authority sequence from request through approval,
  execution, inspection, intervention, revocation, and forgetting.
- **Supporting figure:** authority lane attached to the components and data paths
  it governs.
- **Table:** actor, operation, notice, approval, override, expiry, revocation,
  audit, and failure behavior.
- **Representation:** authority map and consent boundary.
- **Algorithm:** approval, override, revoke, and forget state machine.

**Engineering decision.** Allocate authority and determine which operations
require notice, approval, timely override, prohibition, expiry, or revocation.

**Dossier artifact.** Authority map, consent boundaries, intervention path,
retention rights, revocation behavior, and exit policy.

**Transfer task.** Compare authority for the same capability used privately by
an owner, in a shared workplace, and around bystanders who did not configure the
system.

**End-of-chapter lab handoff.** Exercise approval, override, revocation,
inspection, and forgetting as system operations. Measure intervention or
revocation completion where timing matters and diagnose one failed authority
path.

---

### Chapter 12 — Learning From Interaction

**Opening question.** When may physical experience become data that changes the
system?

**Objective.** Given interaction records and an authority policy, the reader can
decide which records may be used, check whether the data covers the situations
that matter, trace where the data came from and who allowed its use, test an
updated model, and decide whether it may replace the current one.

**Entering state.** Complete trajectories from the running loop, evidence and
promotion criteria, authority, and consent.

**Misconception.** Logged interaction is automatically useful training data, and
more data necessarily produces a better physical policy.

**Crux.** Interaction creates governed trajectories shaped by the current
policy, embodiment, people, and environment; training produces a new candidate,
not an automatic update.

#### Required Sections

1. **Every Action Creates an Interaction Record**
   Define the physical interaction record across observation, belief, proposal,
   enforcement, action, consequence, and outcome.

2. **The Policy Shapes Its Own Data**
   Revisit endogeneity as selection bias, coverage distortion, missing failures,
   and changing state visitation.

3. **Ways a System Learns From People**
   Distinguish demonstrations, teleoperation, corrections, preferences,
   interventions, approvals, and autonomous experience.

4. **What Each Interaction Record Must Contain**
   Specify observations, state, action, timing, frames, policy version,
   embodiment, outcome, environment, authority, and provenance.

5. **Coverage Before Quantity**
   Examine state-action coverage, rare conditions, interventions, failures,
   operator bias, and missing regions.

6. **The Same Command Can Mean Different Things on Different Bodies**
   Explain why similar-looking trajectories may differ in morphology, frames,
   action normalization, dynamics, and available skills.

7. **Where the Data Came From and Who Allowed Its Use**
   Apply Chapter 11 to collection, retention, reuse, export, sharing, and
   deletion.

8. **Choose the Data Before Training**
   Treat selection, filtering, labeling, failure inclusion, and dataset versions
   as governed engineering choices.

9. **Training Produces a Candidate**
   Keep training mostly outside scope while making the resulting model version,
   interface, claimed improvement, and compatibility explicit.

10. **Evaluate the Updated System**
    Reuse Chapter 10 to evaluate the candidate against prior behavior, new
    coverage, regression, enforcement, and authority requirements.

11. **Version, Roll Back, and Learn Again**
    Close the lifecycle without uncontrolled online change.

#### Required Teaching Artifacts

- **Primary figure:** interaction → admission → curation → candidate →
  evaluation → approval → deployment or rollback.
- **Supporting figure:** provenance graph connecting person, environment,
  embodiment, trajectory, dataset, candidate, and deployed version.
- **Table:** trajectory field, meaning, provenance, consent, coverage role, and
  failure if missing.
- **Representation:** coverage map, data-admission record, and change record.
- **Algorithm:** admit or reject experience, evaluate candidate, approve or hold,
  deploy, monitor, and roll back.

**Engineering decision.** Admit or reject experience, then promote, hold, or
reject the candidate produced from it.

**Dossier artifact.** Trajectory schema, governed dataset lineage, coverage
report, change-control process, candidate record, and rollback path.

**Transfer task.** Evaluate whether a dataset collected on one embodiment and by
one operator can support a changed policy on another embodiment and user group.

**End-of-chapter lab handoff.** Supply trajectories with missing lineage, biased
coverage, ambiguous action semantics, or invalid consent. Detect the defect,
decide whether the experience is admissible, and evaluate any resulting update
before deployment or rollback.

---

### Chapter 13 — Ready to Deploy?

**Opening question.** What evidence is sufficient to accept responsibility for
this system in this deployment?

**Objective.** Given the complete system and its evidence, the reader can state
exactly where and how it may be used, expose unsupported assumptions, connect
hazards to evidence and recovery, and decide whether it is ready to deploy.

**Entering state.** Every previous dossier artifact.

**Misconception.** A successful demonstration, safe stop, security checklist, or
privacy statement is sufficient evidence of readiness.

**Crux.** Deployment is an accountable claim about a specific system,
population, environment, operating limits, authority structure, and change
process.

#### Required Sections

1. **State What You Plan to Deploy**
   State task, system version, users, affected people, environment, operating
   limits, dependencies, monitoring, and exclusions.

2. **Match Each Hazard With Evidence**
   Link physical consequence to prevention, detection, mitigation, recovery,
   ownership, and residual risk.

3. **Safety Is More Than Action Limits**
   Integrate action limits, independent checking, runtime failure,
   confidence tiers, human intervention, and recovery.

4. **Security Controls Who Can Act**
   Cover command authentication, trust boundaries, update integrity, credentials,
   dependency provenance, supply chain, and compromise recovery.

5. **Privacy Follows the Data**
   Audit capture, inference, egress, retention, reuse, deletion, consent, and
   bystander exposure.

6. **When Parts Fail or Recover**
   Include lost connectivity, resource exhaustion, partial service, sensor loss,
   stale state, bad update, rollback, and service exit.

7. **Show What the Evidence Supports**
   Connect each release claim to its operational evidence, owner, validity
   period, and counterevidence.

8. **Name the Missing Evidence**
   Make unsupported regions, unresolved hazards, weak coverage, and assumptions
   visible rather than hiding them in prose.

9. **Know When Formal Assurance Is Required**
   Explain the limits of a teaching system and the handoff to domain standards,
   certification, legal review, safety specialists, and accountable institutions.

10. **Write the Decision**
    Record deploy, deploy under conditions, or do not deploy; residual risk;
    owners; monitoring; rollback; expiry; and the evidence that would change the
    verdict.

#### Required Teaching Artifacts

- **Primary figure:** claim-argument-evidence case with visible gaps and owners.
- **Supporting figure:** deployment dataflow and authority boundaries across
  normal, degraded, and update states.
- **Table:** claim or hazard, prevention, detection, threshold, evidence,
  recovery, owner, residual risk, and verdict.
- **Quantitative comparison:** time to safe state versus time to harm where the
  deployment makes the comparison meaningful.
- **Algorithm:** release decision with explicit conditions and an expiry date.

**Engineering decision.** Deploy, deploy under explicit conditions, or do not
deploy.

**Dossier artifact.** Integrated deployment case and accountable decision
record.

**Transfer task.** Audit an unfamiliar system whose model performs well but whose
authority, update, recovery, or coverage evidence is incomplete.

**End-of-chapter lab handoff.** Present conflicting evidence across safety,
security, privacy, recovery, coverage, updates, and authority. Require a written
release verdict and the exact evidence that would reverse it.

## Unnumbered Final Design Review

The design review is the summative transfer assessment. It does not teach a new
topic or become a fourteenth chapter.

The reader must:

- assemble the complete loop and show how \(W_t\) becomes \(W_{t+1}\);
- defend the boundary, requirements, interfaces, runtime, and placement;
- show valid evidence for ordinary behavior, tails, failures, and recovery;
- demonstrate proposal, independent enforcement, and safe-state behavior;
- present authority, consent, data-admission, update, and rollback paths;
- defend the deployment decision and name missing evidence;
- diagnose one deliberately introduced physical-system failure through
  hypothesis, bisect, and confirm; and
- adapt the method to a model, embodiment, or environment not used in the
  reference system.

A defended failure can pass. An unexplained success cannot.

## End-of-Chapter Lab Boundary

Labs are designed after the relevant chapter passes its teaching review. Every
lab must provide the same instructional outcome through analytical, hosted, and
physical manifestations where feasible.

The lab may make a property visible, expose a misconception, provide evidence,
or deepen diagnosis. It may not introduce the chapter's central concept, repair
a missing explanation, or make successful assembly the final outcome.

Every lab ends with:

1. a predeclared prediction;
2. a controlled perturbation and meaningful alternative;
3. a measurement with regime, units, uncertainty, and efficacy;
4. a diagnosed chapter-native failure;
5. a chapter-specific engineering decision; and
6. an update to the cumulative design dossier.

## Drafting Order

The final prose should be integrated in dependency order even when research and
review happen in parallel:

1. Chapters 1 through 4 establish the language, requirements, evidence, and
   runtime.
2. Chapters 5 through 8 populate the loop through observation, belief, proposal,
   and enforcement.
3. Chapters 9 and 10 integrate placement and assurance.
4. Chapters 11 and 12 establish authority before governed learning.
5. Chapter 13 integrates the deployment case.
6. The final design review is written after every chapter artifact is stable.
