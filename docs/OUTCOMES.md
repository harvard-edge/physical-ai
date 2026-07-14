# Learning Outcomes: The Backward-Design Spine

**Status:** working draft for review. This document comes *before* the chapter
list. Outcomes decide chapters, not the other way around.

## Purpose

We design this course backwards. The standard is constructive alignment: first
name what a graduate can *do*, then decide what evidence proves they can do it,
then and only then choose chapters and labs to build that capability. A course is
good when every chapter traces to an outcome and every outcome has an assessment.
Where a chapter floats free of any outcome, or an outcome has no chapter, that is
exactly where the curriculum is weak, and this page is built to make those gaps
visible.

The scope boundary still holds: these are physical-AI-engineering outcomes, not
machine-learning-systems outcomes. Every outcome below is about coupling a system
to the world, not about how a model is trained or compressed.

## The Graduate Profile

One sentence, the whole course compressed:

> A graduate can take a physical-AI problem they have never seen, architect a
> continuous system for it, ground it in real time and space, place every
> capability against a fixed budget and defend each choice with a measured number,
> prove it fails safe and keeps private data on the device, set up the human
> teaching-and-approval loop it lives inside, and diagnose it when the world makes
> it misbehave.

That sentence names seven verbs: frame, design, ground, place, assure, supervise,
diagnose. The six outcomes below carry the first six. Diagnosis is carried as a
thread, for reasons given after.

## The Six Outcomes

**O1. Frame the problem.**
Given a task, a graduate can decide whether it is even a physical-AI problem,
identify the closed loop and the world-coupling, and name which of the nine
properties bind and stand in tension.

- **Muscle:** judgment.
- **Physical-AI, not ML:** the question is whether the system acts back into the
  world its next input comes from, not whether a model is accurate.
- **Evidence:** a written verdict on a given system, is it physical AI, what loop
  closes, what binds, plus the one property you would defend first.

**O2. Design the runtime.**
Given a novel embodied task, a graduate can architect the continuous system that
runs the loop: the supervisor, the services, the state store, the event flow, and
the propose/dispose boundary that separates what the reasoner may propose from
what deterministic control disposes.

- **Muscle:** synthesis. This is the design verb the current book under-teaches.
- **Physical-AI, not ML:** the artifact is a live process bolted to a body and
  meant to outlive any single interaction, not a training pipeline or a model.
- **Evidence:** an architecture diagram, the action contract that maps an intent
  vocabulary to bounded primitives, and a defense of where the propose/dispose
  line sits and why.

**O3. Ground it in time and space.**
Given sensors and a body, a graduate can establish coordinate frames and the
transforms between them, timestamp and synchronize signals, maintain a live
world-and-self model under uncertainty, and hold an end-to-end latency budget from
sense to act.

- **Muscle:** a core build skill.
- **Physical-AI, not ML:** a detection is a pixel until it becomes a point in the
  body frame at a known time. This is the coupling made literal.
- **Evidence:** a frames-and-timing diagram, a measured latency budget, and a
  world model that reports its own uncertainty and flags drift.

**O4. Place every capability and defend it with a number.**
Given a fixed compute, power, and bandwidth budget, a graduate can place each
capability by loop (reflex, deliberation, learning) and by box (device, server,
cloud), defend each placement with a measured number, and re-place one capability
and predict the ripple through the rest of the system.

- **Muscle:** analysis and optimization. The crown jewel, and already the book's
  strongest thread.
- **Physical-AI, not ML:** the budgets belong to a body, not a datacenter, and the
  placements draw from one shared pool, so they collide.
- **Evidence:** a filled placement map with measured latency, energy, and bytes,
  and one defended re-placement. This is the capstone's core.

**O5. Assure it before it ships.**
Given a system about to enter a home, a graduate can build confidence without
running the world (simulate, replay, shadow), prove the fail-safe reaches a safe
state inside the harm budget, and audit what leaves the device, then refuse to
ship until every number passes.

- **Muscle:** verification. This carries the test verb the current book promises
  ("everything testable without hardware") but never teaches.
- **Physical-AI, not ML:** you cannot replay reality, a failure moves a body, and
  the data was gathered in someone's home.
- **Evidence:** a ship or no-ship gate with a recovery-time measurement, an egress
  audit, and a simulation-or-replay result standing in for the world.

**O6. Set up the human loop it lives inside.**
Given a robot that a person teaches and lives with, a graduate can build the
teaching-and-approval path where new skills and memories are gated by an adult,
make memory inspectable and forgettable on request, hold the consent boundary, and
close the loop so the human's corrections become the data that improves the system.

- **Muscle:** the deployment relationship.
- **Physical-AI, not ML:** the system shares a space with a specific person and is
  taught by that person, and its improvement loop runs on that person's labels.
- **Evidence:** an approval-and-teaching flow, an inspect-and-forget memory demo,
  and the flywheel turn a single correction feeds, with its consent gate shown.

## The Seventh Verb: Diagnose (Threaded, Not Homed)

Diagnosis is a real capability we want, so backward design says name it or lose
it. But it is deliberately not given its own chapter, because a physical failure
is best learned where it happens. You learn to diagnose a wrong frame while
teaching frames, a missed deadline while budgeting time, one placement starving
another while filling the map. A single debugging chapter would teach the topic in
the abstract and never build the reflex.

- **How it is carried:** every lab ends with a "break it and find why" step, a
  frame is off, a deadline slips, a placement contends, a fail-safe is too slow.
  The capstone requires one diagnosed failure, defended.
- **Physical-AI, not ML:** the failures are physical, timing, frames, contention,
  the body, not loss curves.

## The Chapter-to-Outcome Map

Every current and proposed chapter, mapped to the outcome it primarily builds.
This is where the gaps show.

| **Chapter** | **Primary outcome** | **Also serves** | **Status** |
| --- | --- | --- | --- |
| The Discipline | O1 | | have |
| The Elements | O1 | O4 | have |
| From TinyML to Physical AI (the loop) | O1 | | have |
| Perception (reframed: perception in the loop) | O3 | | have, reframe |
| Pixels to Meaning (VLM/VLA) | O4 | O3 | have |
| Cognition and Agency | O4 | O2 | have |
| Action and Control | O2 | O4 | have |
| Memory and State | O3 + O6 (split) | | have |
| The Data Flywheel | O6 | O4 | have |
| Placement and Systems | O4 | | have, crown |
| Safety, Privacy, Deployment | O5 | | have |
| **Runtime and Architecture** | **O2** | | **new** |
| **The World Model** | **O3** | | **new** |
| **Confidence Without the World** | **O5** | | **new** |
| **The Human Loop** | **O6** | O4 | **new** |
| Capstone | all, integrative | Diagnose | have |

## What the Map Reveals

The point of building the map was to let it decide things for us. It does.

1. **Two outcomes have no adequate home in today's book.** O2 (design the runtime)
   rests on the action chapter alone, and the test half of O5 (assure without the
   world) rests on nothing. That is the decisive result: the Runtime chapter and
   the Confidence-Without-the-World chapter are *required*, not optional, because
   without them two graduate outcomes cannot be assessed. Backward design just
   settled two of the four new chapters on evidence, not taste.

2. **O4 is over-served.** Five to six chapters funnel into "this is a placement,
   defend it with a number." That depth is the book's strength, but it is also the
   monotony risk: a course should not say the same thing six times. Implication,
   the loop-stage chapters can be tightened, and some may become sections of a
   larger chapter rather than full chapters of their own.

3. **O1 is front-loaded.** Three chapters argue the discipline exists before the
   student builds anything. That is right for a monograph, which must prove its
   claim. For a course it can compress, so learners start doing O2 and O3 sooner.
   The monograph proves the field is real; the course should assume it and build
   capability.

4. **Diagnose is deliberately homeless,** carried as a thread with per-lab and
   capstone assessment, for the reason given above.

5. **The order falls out on its own.** O2 (design the skeleton) is a prerequisite
   for O3, O4, and O5 to have something to attach to. So the course wants a
   spine-first spiral, not a data-flow march: frame (O1, compressed), then design
   the runtime skeleton (O2) early, then ground it, place into it, assure it, and
   supervise it, each chapter thickening the same growing artifact, ending at the
   capstone. This resolves the build-order critique. The runtime is built first,
   and every later chapter fills it in.

## Assessment Ladder (Constructive Alignment, Complete)

Each outcome has its own formative evidence (the "Evidence" line above), produced
in that outcome's chapter or lab. The capstone is the summative assessment: it
integrates all six and requires the diagnosis thread. Because the capstone is
"defend every placement with a number," it aligns most tightly to O4, so the other
five outcomes need their formative checks to carry real weight and not be
swallowed by the placement finale.

## What This Resolves, and What Is Still Yours to Decide

**Resolved by the map (no taste required):**

- All four proposed new chapters are validated by outcomes, Runtime (O2), World
  Model (O3), Confidence Without the World (O5), Human Loop (O6). Each is the only
  adequate home for its outcome.
- Diagnosis is a thread, not a chapter.
- The course order is a spine-first spiral, not a stage-by-stage march.

**Still open (your calls, a matrix cannot make them):**

- **Audience and level.** Grad seminar, practicing-engineer course, or maker
  curriculum. "Good" is relative to a learner, and this is the one decision
  backward design cannot make for us. Everything else can be tuned once it is set.
- **How hard to compress O1,** the discipline argument, from three chapters toward
  two, trading monograph completeness for a faster start to doing.
- **Whether the O4 loop-stage chapters stay full chapters** or collapse into fewer,
  to defeat the monotony risk without losing the depth.
- **Whether the World Model and Perception are two chapters or one** "Grounding"
  chapter covering frames, time, belief, and drift together.
