# Chapter 1 Authoring Packet

**Packet:** `CTX-CH01-001`  
**Version:** 1.0.1  
**Status:** architecture, core source locations, and representation compositions
accepted; opening-cluster drafting and provisional asset production authorized  
**Red-team state:** packet coherence passed; the resulting prose and figures
must be checked again before full-chapter acceptance  
**Chapter:** From ML Systems to Physical AI  
**Consumes:** `CTX-FND-001`  
**Produces:** `LOOP-001`

## Chapter Contract

### Reader-Facing Objective

After this chapter, you will be able to tell when a learned system is doing more
than producing information, trace how its output may become a physical action,
and decide what belongs inside the system being engineered.

### Entering State

The reader can follow an ordinary input-to-inference-to-output pipeline,
understands that deployed models run inside software services, recognizes common
sensors and actuators, and can read a simple system diagram.

The chapter assumes no control theory, robotics notation, causal inference,
state estimation, runtime assurance, or safety-engineering background.

### Misconception

The primary misconception is that Physical AI means a capable model running on
a robot, board, or other physical device.

Supporting misconceptions include:

- any feedback system is Physical AI;
- a model output is already an action;
- a system boundary is a box around deployed code;
- all machine learning systems are open loop;
- a responsive system necessarily has legitimate authority; and
- an affected person may be treated as external context.

### Crux

A learned system enters this book's scope when a learned proposal materially
affects the action path, an allowed action changes task-relevant physical state
and can alter a later observation or choice, and the engineered system exercises
delegated physical authority over that action.

This is the book's working classification, not a universal definition of the
field.

### Engineering Decision

Decide whether the learned system belongs inside the book's scope and choose the
smallest defensible boundary containing the causal path, authority path,
physical consequence, affected people, and next observation.

### Dossier Delta

Create `LOOP-001`, the first version of the system's loop charter.

## Concept Ownership

### Owned Here

- the learned-component premise;
- consequential physical feedback;
- delegated physical authority at a classification level;
- learned proposal versus allowed action;
- the two-world-state loop, \(W_t\) to \(W_{t+1}\);
- endogeneity at an intuitive causal level;
- causal boundary versus deployed-code boundary;
- authority boundary at an identification level;
- feedback and authority as independent constraints;
- identification of affected people; and
- the loop-charter representation.

### Borrowed Briefly

- the familiar ML inference pipeline;
- feedback and closed-loop language from control and cybernetics;
- system-boundary reasoning;
- policies and sequential decisions;
- causal paths;
- sociotechnical context and human-automation allocation; and
- policy-induced state visitation.

The chapter credits these lineages without surveying them.

### Deferred

- timescales, deadlines, freshness thresholds, and physical requirements;
- measurement validity, distributions, uncertainty, and evidence strength;
- services, queues, scheduling, and physical recovery;
- observation-contract details and belief-state construction;
- VLM and VLA interfaces;
- action limits, safe sets, and enforcement design;
- compute placement;
- evidence tiers and promotion;
- detailed approval, intervention, revocation, and forgetting mechanisms;
- interaction-data governance; and
- release assurance.

The symbol \(b_t\) and a labeled permission check may appear as placeholders.
Their implementation remains later material.

## Opening Design

Open with `CASE-SWH-001` using the same learned model in two deployments.

The model observes a tabletop and identifies which object belongs in a declared
destination zone.

- In advisory mode, it marks a suggestion. A person independently decides
  whether and how to move the object.
- In delegated mode, its result becomes proposal \(p_t\), an authority path
  permits an action, and the system moves or diverts the object. The next
  observation describes a changed workspace.

The model, observation, and prediction are the same. The causal and authority
path after inference differs.

Do not define Physical AI before showing the contrast. Let the reader notice
that the endpoint moved.

## Section Briefs

### `SEC-CH01-01` — The Endpoint Has Moved

**Reader before.** An ML system is input, model, and digital output. Model and
service quality dominate the system story.

**Instructional job.** Follow the output beyond the API response. Distinguish a
digital output, learned proposal, allowed action, and physical consequence.

**Canonical-case move.** Show the same object-selection result in advisory and
delegated deployments without classifying them yet.

**Reader after.** The reader asks what happens after inference and recognizes
that digital output may be the midpoint.

**Check.** Identify the last digital event and first physical effect in each
deployment.

### `SEC-CH01-02` — When an Output Becomes an Action

**Reader before.** The reader may classify from hardware, a robot, or the
presence of feedback.

**Instructional job.** Introduce the learned-component premise, consequential-
physical-feedback test, and delegated-physical-authority test. Separate
proposal \(p_t\), permission check, and allowed action \(u_t\).

**Canonical-case move.** The person retains physical action selection in
advisory mode. In delegated mode, the system may move the selected object only
within a defined class of tasks.

**Reader after.** The reader can classify straightforward cases without relying
on model family, embodiment, or hardware presence.

**Check.** Explain why a recommender, fixed thermostat, learned HVAC controller,
and learned handler receive different verdicts.

### `SEC-CH01-03` — Action Changes What Comes Next

**Reader before.** Each inference appears independent, and action occurs after
the “real” AI work.

**Instructional job.** Introduce \(W_t\), \(u_t\), \(W_{t+1}\), and
\(o_{t+1}\). Show how allowed action changes position, visibility, risk,
remaining options, and later data. Introduce endogeneity without formal
learning-theory results.

**Canonical-case move.** Moving an object changes the next image, can reveal or
occlude another object, and can move the system into a sparsely represented
state.

**Reader after.** The reader can trace how one allowed action changes later
state and observation.

**Check.** Compare the next observation after two allowed actions from the same
initial state.

### `SEC-CH01-04` — The Model Inside the System

**Reader before.** The model remains the organizing center; the surrounding
parts appear to be implementation detail.

**Instructional job.** Introduce the minimal recurring plate.

\[
W_t \rightarrow o_t \rightarrow b_t \rightarrow p_t
\rightarrow \operatorname{permit} \rightarrow u_t \rightarrow W_{t+1}
\]

Add disturbance \(d_t\) and affected people. Treat belief and permission-check internals as
placeholders.

**Canonical-case move.** Label observation, task state, proposal, authority
path, issued command, physical consequence, disturbance, person, and next
observation.

**Reader after.** The reader can locate the learned component without confusing
it with the system.

**Check.** Remove the model from the diagram and identify which engineering
responsibilities still exist.

### `SEC-CH01-05` — Feedback Is Not Authority

**Reader before.** A responsive loop appears authorized, or human approval
appears to compensate for poor physical coupling.

**Instructional job.** Compare feedback quality and authority allocation as
separate dimensions.

| Feedback relationship | Authority relationship | Result |
| --- | --- | --- |
| Current and responsive | Authority is explicit and limited | Target design condition |
| Current and responsive | Excessive or unapproved | Responsive but improperly delegated |
| Stale or poorly coupled | Legitimately approved | Authorized but physically unreliable |
| Stale or poorly coupled | Excessive or absent | Neither constraint is satisfied |

**Canonical-case move.** Contrast prompt action outside the permitted zone with
approved action based on an obsolete workspace view.

**Reader after.** The reader evaluates coupling and authority independently.

**Check.** Diagnose which constraint fails in two short variants.

### `SEC-CH01-06` — What This Book Borrows

**Reader before.** The book may appear to be robotics with a model or a claim to
an entirely new field.

**Instructional job.** Credit the contributions of ML systems, control,
robotics, embedded and real-time systems, cyber-physical systems, systems
engineering, human factors, safety, and security in one compact comparison.

**Canonical-case move.** Route each obligation in the handler to its
intellectual lineage while showing that the loop charter must hold them
together.

**Reader after.** The reader can explain the book's integration claim without
claiming the invention of feedback, physical coupling, or authority analysis.

**Check.** Assign five canonical-case questions to their source disciplines and
identify the cross-field systems decision.

### `SEC-CH01-07` — Draw the Boundary

**Reader before.** The reader understands the classification but has not
produced an auditable artifact.

**Instructional job.** Present and complete the loop-charter schema. Compare a
boundary that is too narrow, a boundary that is needlessly broad, and a
defensible boundary. Preserve ambiguity and assumptions.

**Canonical-case move.** Complete the task, world state, observation, proposal,
authority path, action, disturbance, consequence, next observation, affected
people, and chosen boundary.

**Reader after.** The reader can turn a scope judgment into an engineering
record that later chapters can refine.

**Check.** Complete `LOOP-001` and defend one included and one excluded element.

## Representation Briefs

### `REP-CH01-FIG-001` — Matched Deployments

Show the same learned component in advisory and delegated deployments. Only the
second contains an allowed action that changes \(W_{t+1}\).

**Inference.** Model identity and hardware presence do not determine the scope
verdict. The causal and authority path does.

### `REP-CH01-TBL-001` — Scope Test

Compare an image-description model, recommender, fixed thermostat, learned HVAC
controller, advisory inspection system, automated rejector, teleoperated robot,
and learned shared-workspace handler.

**Inference.** Learned influence, consequential physical feedback, and delegated
physical authority are separate classification checks.

### `REP-CH01-SCHEMA-001` — Loop Charter

Provide the exact schema and one completed canonical-case entry.

**Inference.** Classification and boundary judgment produce an auditable
artifact.

### `REP-CH01-TBL-002` — Intellectual Lineage

Compare what neighboring disciplines contribute, what the book consumes, and
what it deliberately does not reteach.

**Inference.** The book's contribution is the systems integration and pedagogy,
not ownership of the component ideas.

## `LOOP-001` Schema

### Record Identity

- loop identifier, version, and status;
- system or deployment name;
- task;
- record owner; and
- date.

### Scope Verdict

- learned component and its role;
- learned-component premise, yes, no, or ambiguous;
- consequential-physical-feedback test, yes, no, or ambiguous;
- delegated-physical-authority test, yes, no, or ambiguous;
- scope verdict; and
- rationale.

### Causal Path

- relevant physical state \(W_t\);
- observation \(o_t\);
- maintained decision state \(b_t\), if present;
- learned proposal \(p_t\);
- accepting person or permission check;
- allowed action \(u_t\);
- disturbance \(d_t\);
- immediate physical consequence;
- resulting state \(W_{t+1}\);
- next observation \(o_{t+1}\); and
- explanation of how action changed later state or observation.

### Authority and People

- authority granted to the system;
- authority retained by a person or another system;
- requester, nearby collaborator, bystander, operator, maintainer, and other
  affected roles;
- physical space, resource, body, access, or data affected; and
- initial permission assumptions.

### Boundary and Assumptions

- components, roles, and world processes included;
- excluded entities and rationale;
- an alternative plausible boundary;
- assumptions on which the verdict depends;
- known ambiguity; and
- unresolved engineering obligations.

Do not add latency thresholds, measurements, runtime services, safety envelopes,
or release evidence yet.

## Transfer Check

Use a learned occupancy estimator in four building-system deployments.

1. It displays occupancy estimates on a facilities dashboard.
2. It automatically opens and closes a ventilation damper.
3. It changes room recommendations and influences later bookings.
4. A fixed non-learned thermostat directly controls heating.

Ask the reader to apply the learned-component premise and both scope tests,
classify each deployment, draw the causal and authority path for the ventilation
case, identify affected people, and name an assumption that would reverse a
verdict.

The task passes only when the reader reasons from causality and authority rather
than matching the tabletop example.

## Decision Callout Contract

Decide whether the learned system closes a consequential physical loop and has
delegated physical authority. Draw the smallest defensible boundary containing
the proposal, authority path, allowed action, affected people, physical
consequence, and next observation. Record the result as `LOOP-001`.

## Lab Boundary

### Phenomenon

The same learned component has different system meaning when its output remains
advisory and when an allowed action changes the next physical state and
observation.

### Prediction

Before enabling either path, predict whether a proposal becomes an allowed
action, whether \(W_{t+1}\) differs, whether the next observation changes, and
whether the deployment satisfies the scope test.

### Perturbation and Alternative

Enable, disable, approve, or reject the action path while keeping the learned
component and initial scene fixed. Advisory and rejected-proposal paths are the
negative controls.

### Evidence

Record proposal, acceptance or rejection, issued or absent action, initial world
state, resulting world state, next observation, and authority path. A repeated-
trial count may be recorded but must not be presented as statistically validated
evidence before Chapter 3.

### Native Failure and Diagnosis

The initial boundary omits the permission check, person retaining authority, or
physical process that produces the next observation.

- **Hypothesis.** The allowed action caused the changed next observation.
- **Bisect.** Disable or reject the action while preserving the proposal.
- **Confirm.** The physical and observational change disappears or changes as
  predicted.

### Decision and Dossier

Classify the deployment, defend its causal and authority boundary, and complete
or revise `LOOP-001`.

The lab may not introduce deadlines, measurement uncertainty, runtime
scheduling, state estimation, model architecture, action limits, placement,
detailed authority mechanisms, or release assurance.

## Acceptance Checklist

- The objective tests one integrated classification and boundary skill.
- Proposal \(p_t\) and allowed action \(u_t\) are never interchangeable.
- Every primary loop representation distinguishes \(W_t\) from \(W_{t+1}\).
- The learned-component premise precedes the two scope tests.
- Counterexamples prevent classification from superficial features.
- Authority and affected people appear in the boundary.
- The reader may state an assumption-dependent verdict without forced certainty.
- Endogeneity is explained without implying that action is the only cause.
- Intellectual lineage is credited without turning into a survey.
- Later chapters retain their concept ownership.
- The transfer check cannot be passed through imitation.
- The chapter stands without hardware.
- The visible chapter uses one objective callout, natural headings, one decision
  callout with the `LOOP-001` update, and the lab last.

## Draft Authorization State

The architecture, objective, source locations, case progression, transfer task,
and lab boundary are accepted. The opening cluster may now be drafted one
connected section group at a time while provisional representation assets are
built from the accepted briefs.

The full chapter is not accepted until:

1. the representation assets pass HTML, PDF, manuscript-width, grayscale, and
   alt-text review;
2. the remaining bibliography cleanup is complete;
3. the resolved source-and-scope red-team findings are verified against the
   prose and figures; and
4. context packet `CTX-CH01-001` records any accepted deltas from the pilot.
