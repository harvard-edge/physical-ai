# Physical AI — Curriculum Plan

Status: **draft for review, uncommitted.** This is the careful plan we build the
chapters from: the scope boundary, the pedagogy model, the per-chapter
scaffolding, the ideal chapter list, and what each chapter should cover. Read it,
mark it up, and we lock the open decisions at the end before writing prose.

---

## 1. Scope: what this book is, and is not

**It is** *Physical AI: Machine Learning Systems That Sense and Act*. It extends
the systems perspective into a machine that closes a time-bounded feedback loop
with the physical world, under the limits of a body and in a space that belongs
to a person. The recurring skill is **placement**, and the deliverable is a
**defended design decision**.

**It is not** a repeat of a conventional machine learning systems course. This
is the sharp line, and we hold it:

- **Out of scope** (lives in the companion *Introduction to Machine Learning
  Systems*): how models work inside — quantization, training, architectures,
  efficiency, compilers, the accuracy/latency/energy mechanics of a network.
- **In scope**: the AI model as a **component with measurable properties**
  (latency, size, accuracy, failure modes, cost) that the engineer must *place*
  in a loop and a box, and *bound* with a safety and privacy envelope.

> The test for every paragraph is whether it teaches how the model works or what
> changes when that model participates in a physical feedback loop. The first
> belongs in the introductory ML systems book. The second belongs here. When a
> model detail appears (a precision knob, a model size), it appears **only as an
> illustrative instance of a coupling**, a decision about the component that
> spends a physical property, never as a subject in its own right.

This is what keeps the book distinct from its neighbors rather than a remix of
them: the subject is the **coupling and the placement**, not the parts.

---

## 2. The pedagogy model

Written down as you framed it, because it drives the scaffolding:

1. **The book teaches concepts.** The concept track is the primary deliverable
   and is complete on its own — a reader who never touches hardware still learns
   the discipline. Concepts are physical AI *engineering* ideas (the loop,
   timeliness, placement, the propose/dispose boundary, the safety envelope, the
   flywheel), not model internals.

2. **Labs are the manifestation of the concepts.** A lab (mid-chapter or at the
   end) is where a concept stops being an argument and becomes a concrete,
   measured thing. The lab exists to *realize* the concept, not to introduce it.

3. **Two forms of manifestation, one active now:**
   - **Hero robot (Reachy / "Robby") — active.** The reference build that
     realizes the full end functionality, and whose measurements **distill back**
     into the concepts (revise the estimate, sharpen the claim). This is where the
     concept is proven and fed back.
   - **Kit (Arduino UNO Q) — deferred.** The reproducible learner build. We are
     **not building this now.** It slots under each concept later; for now it is a
     placeholder rung.

4. **We are getting the pedagogy right first** — the concepts and the learning
   scaffolding — before any kit implementation.

The per-chapter flow, then: **teach the concept → manifest it (hero build) →
distill back what the build revised.**

---

## 3. The chapter scaffolding (the per-chapter learning architecture)

Every chapter follows this section order. The two load-bearing layers are **(B)
the concept, taught** and **(F) the manifestation** — everything else serves
them. New layers relative to the current draft chapters are marked `+`.

| # | Section | What it does |
|---|---|---|
| A | **The question** (styled box) | the one question the chapter answers |
| + | **Learning objectives** | what the reader will be able to *decide or do* after this chapter — concept-level, testable |
| C | **The scene** | the robot moment that makes the concept matter; the stakes you can see (the WHY) |
| **B** | **The concept, taught** | **the physical AI systems idea developed properly**: the core idea, the mental model, the recurring diagram, the reasoning, the **iron law** (a napkin formula that makes it quantitative), the **properties in tension**. This is the body the current chapters skip. |
| D | **The decision: placement** | apply the concept to a placement and defend it — the climax |
| E | **Why it is physical AI** | tie the concept back to the coupling: the consequence that only exists because the loop is closed around a body. Keeps the chapter from reading as generic systems. |
| **F** | **Manifestation (the lab)** | predict → build → measure → reconcile. **Hero robot now** (realize it on Reachy); **kit later** (deferred UNO Q rung); analytical/thought-experiment fallback where hardware is out of reach |
| + | **Distill back** | what the build revised about the concept or the placement — the reconcile, generalized |
| G | **Read** | literature anchors, honest about what is borrowed |
| H | **Teaching note** (collapsible) | for the instructor: hook, open question, what to watch |
| + | **Carry forward / check yourself** | the one idea that carries to the next chapter, and 2–3 questions that test the concept |

Principle for depth (so the book teaches fundamentals without becoming a survey):
**teach each concept to the depth the placement decision demands — no less, or it
is hand-waving; no more, or it is a survey. The decision sets the depth.**

---

## 4. The chapters: what we have, and what we should ideally have

The current draft has 12 short chapters. Under the scope correction and the
runtime work, here is the proposed ideal list. **Bold = new or substantially
reframed; these are the open decisions in §7.**

### Part I — Foundations (the discipline)

- **F1. The Discipline** — coupling as the dividing line; why it is a field of its
  own (add the Cyber-Physical Systems positioning); placement as the recurring
  move.
- **F2. The Elements** — the nine properties as engineering budgets; the budget
  identity; **observability built first** (measurement as a taught skill, not
  logging for its own sake).

### Part II — The loop, one concept per chapter

- **C1. The Loop** — open loop vs closed loop; timeliness as a correctness
  property; the loop is the subject, the model is a part. *(was Ch 0)*
- **C2. Perception in the Loop** — sensing as a coupled, budgeted, **active**
  process (where to look is itself an action); partial and noisy sensing; the
  sensing budget. **Reframed away from edge-perception/quantization** (that is ML
  systems). *(was Ch 1)*
- **C3. Meaning and Intent** — VLMs and **VLAs as components**: pixels to meaning
  to intent; the grounding gap; a decision sets a *target*, never a motor command.
  The deep home of the VLA thread. *(was Ch 2)*
- **C4. World and Self State** — fusing partial, noisy sensing into a belief over
  time; grounding, drift, what the system thinks is true. **Elevated** from a
  sub-point of memory; it is its own physical AI concept. *(new — open decision)*
- **C5. Cognition and Agency** — the two-speed brain; the escalation budget; the
  propose side of propose/dispose; tool use as the interface to the world. *(was
  Ch 3)*
- **C6. Action and Control** — the dispose side; the safety envelope; **an AI
  choice is a control choice** (the signature coupling), taught as coupling, not
  as control theory. *(was Ch 4)*
- **C7. Memory** — persistence as a component and a privacy liability;
  structured/inspectable/forgettable vs opaque; what to keep and forget. *(was Ch
  5)*
- **C8. The Data Flywheel** — the loop generates its own training data; engagement
  is collection; curate on the edge; adaptivity and privacy are the same decision.
  *(was Ch 6)*

### Part III — The system

- **S1. Architecture and the Runtime** — how the components compose into one
  continuous system: the supervisor loop, the event bus, the state store, the
  propose/dispose privilege boundary, the lifecycle (wake/sleep/maintenance). The
  "how it all hooks up" that the component chapters imply. **New — this is the
  runtime we designed, and it is the through-line of the whole build.** *(new —
  open decision)*
- **S2. Placement and Systems** — where each capability runs; capabilities share
  one budget; the placement map as the whole-system worksheet. *(was Ch 7)*
- **S3. Safety, Privacy, and Deployment** — putting it in a human space; the
  fail-safe and the egress audit; ship / no-ship as a gate. *(was Ch 8)*
- **S4. The Human in the Loop** — the human is part of the loop: turn-taking,
  legibility, trust, and the human as teacher and labeler. A genuine gap for a
  *companion*, but the most optional. *(new — open decision, lowest priority)*

- **Capstone** — the whole runtime, defended: a filled placement map, the binding
  constraint for each placement, one re-placement and its ripple.

Net: **12 → ~15** if we take all three additions. The three additions are the
open decisions; the reframe of C2 is not optional under the scope correction.

---

## 5. Per-chapter coverage

Compact spec per chapter. "Sections" lists the actual topics it teaches, all
inside the physical-AI-engineering scope.

### F1. The Discipline
- **Concept:** physical AI is defined by world-coupling in a closed loop; it is
  its own discipline because its neighbors' bracketing assumptions break at once.
- **Scene:** the robot that must look at the child before she finishes speaking.
- **Sections:** coupling is the dividing line · a discipline of its own (ML
  systems / control / robotics each bracket one thing) · **positioning vs
  Cyber-Physical Systems** (CPS verifies known dynamics; here the plant includes
  an unverifiable learned model) · the governing reality (four facts) · properties
  before parts · placement as the recurring decision.
- **Manifestation:** thought experiment — list what is hard about the task before
  any model is named. Hero robot: none yet.
- **Models appear as:** not yet; the point is that the model is *not* the hard
  part.
- **Carry forward:** the properties, and the placement question.

### F2. The Elements
- **Concept:** a system is judged by its properties, not its parts; a design fits
  only if every budget closes at once; you cannot budget what you cannot see.
- **Sections:** the nine properties, each *defined and how to measure it* · the
  budget identity and the binding constraint · the three that bind first ·
  **observability built first** (instrument the loop; percentiles and the tail).
- **Iron law:** the budget identity (fits ⇔ every used/limit ≤ 1).
- **Manifestation:** hero robot — stand up the telemetry that every later chapter
  reads (the observability harness). Kit later: same harness across two brains.
- **Carry forward:** name the binding constraint every chapter.

### C1. The Loop
- **Concept:** closing the loop makes timeliness a correctness property; late is
  wrong, and the worst case binds.
- **Sections:** from a pipeline to a loop · why timeliness inverts once the loop
  closes · latency vs period · the iron law of the loop · predicting the loop
  before building.
- **Iron law:** t_loop = t_sense + t_infer + t_act + t_actuate; period < dynamics
  timescale.
- **Manifestation:** hero robot — close a tracking loop, time it, read the tail.
- **Models appear as:** a black-box inference stage with a latency; we time it, we
  do not open it.
- **Carry forward:** the loop is the unit; timeliness first.

### C2. Perception in the Loop  *(reframed)*
- **Concept:** sensing is a coupled, budgeted, **active** process — the system
  acts on a sliver of the world, and *where it senses is itself an action*.
- **Sections:** partial and noisy sensing (the map is not the territory) · sensing
  as a loop stage under a timeliness/energy/bandwidth budget · **active
  perception** (aiming the sensor is an action that changes the next input) ·
  sensor data rate as a cost paid before any model runs · perception latency in
  the loop.
- **Iron law:** sensor data rate = pixels/frame × framerate × bytes/pixel (the
  cost before the model), used to show *sense less* can beat *shrink the model*.
- **Properties in tension:** timeliness and energy against completeness of the
  read.
- **Manifestation:** hero robot — aim the camera/mic actively; measure how the
  read changes with the sensing budget.
- **Models appear as:** a detector with a latency and a field of view; **no
  quantization, no efficient-net internals** — those are the ML systems book.
- **Carry forward:** perception is an action inside the loop, not a free input.

### C3. Meaning and Intent  *(VLA deep home)*
- **Concept:** meaning is the expensive step; who decides it (device vs cloud) is
  a placement; a decision produces *intent*, never a motor command.
- **Sections:** detection vs meaning · VLM as a component (pixels + words → an
  answer) · **VLA as a component** (a VLM whose output vocabulary includes
  actions) · the round-trip cost of asking the cloud · the grounding gap
  (fluent-but-wrong is an observability problem) · intent-not-commands (the target
  goes to the control layer).
- **Iron law:** t_cloud = t_upload + t_infer + t_download, weighed against t_local.
- **Properties in tension:** capability against latency, cost, privacy.
- **Manifestation:** hero robot — ask a small local model and a cloud model the
  same scene question; compare answer, latency, and bytes that left the room.
- **Models appear as:** VLM/VLA as black boxes with capability, latency, size, and
  a grounding-gap failure mode. We teach *placement and the safety floor*, not the
  transformer.
- **Carry forward:** capability is not trust; intent needs a floor.

### C4. World and Self State  *(new — open)*
- **Concept:** the system fuses partial, noisy sensing over time into a belief
  about the world and itself; that belief, not the raw sensor, is what it acts on.
- **Sections:** why a single frame is not enough · fusing over time into a belief
  · grounding and drift (the belief diverging from the world) · self-state (where
  the body is) · the belief as the thing the loop actually runs on.
- **Properties in tension:** robustness and timeliness against the richness of the
  belief.
- **Manifestation:** hero robot — maintain "the child is here, holding a drawing"
  across frames; measure drift.
- **Models appear as:** a state estimator / fuser as a component; we teach *what
  the belief is for and how it drifts*, not the filter's math.
- **Carry forward:** the system acts on a belief, and the belief can be wrong.
- **Open decision:** own chapter, or a strong section inside C2 or C7?

### C5. Cognition and Agency
- **Concept:** a two-speed brain escalates only when needed; the escalation policy
  is the design.
- **Sections:** two speeds, one decision · the escalation budget · where the
  confidence line sits · observability of escalations · the propose side (the
  brain proposes; it does not actuate) · tool use as the interface.
- **Iron law:** t̄ = t_reflex + f · t_deliberate ≤ response deadline.
- **Properties in tension:** timeliness and cost against capability.
- **Manifestation:** hero robot — reflex + escalate-on-uncertainty; count f,
  measure latency per path.
- **Models appear as:** the reflex and the deliberator are two components at two
  costs; the LLM/agent is the deliberator, reached through tools.
- **Carry forward:** thinking is a budgeted resource; the brain proposes.

### C6. Action and Control
- **Concept:** decisions become safe motion under a real-time and safety budget;
  **an AI choice is a control choice** — the signature coupling.
- **Sections:** the dual brain made physical (real-time control vs cognition) ·
  the safety envelope as a budget · why an AI choice is a control choice (a
  decision about the model spends a physical margin) · the dispose side (the
  control layer clips even a well-formed command).
- **Iron law:** margin ≥ e_sense + e_overshoot + stopping distance.
- **Properties in tension:** timeliness and safety, bounded by reliability.
- **Manifestation:** hero robot — smooth vs naive gesture + a safe-stop; then move
  the model's accuracy/latency knob and measure the envelope shrink.
- **Models appear as:** a component with an accuracy↔latency knob; **the knob is
  illustrative (resolution, model size), the concept is the cross-property
  coupling** — not the knob's mechanics.
- **Carry forward:** a statistical choice arrives as a physical consequence.

### C7. Memory
- **Concept:** persistence is a component and a privacy liability; the form you can
  audit and prune is the one a private space demands.
- **Sections:** memory as a budget and a liability · the state grows unless you
  forget · what to keep and in what form (structured/inspectable/forgettable vs
  opaque similarity) · the privacy cost of moving memory off-device.
- **Iron law:** state = memories × bytes ≤ storage; recall latency and privacy
  surface bind before disk does.
- **Properties in tension:** memory/state against privacy.
- **Manifestation:** hero robot — teach it facts, recall next session, forget one
  fact exactly.
- **Models appear as:** the recall mechanism (structured store vs vector index) as
  a component with an *enumerability/auditability* property — not embedding
  internals.
- **Carry forward:** keep less, keep it legible.

### C8. The Data Flywheel
- **Concept:** the system improves from its own curated experience; the engagement
  loop and the data loop are the same loop.
- **Sections:** the four-stage flywheel · quality not quantity (the curator) · the
  cost of a turn (does the round pay?) · adaptivity and privacy as one decision.
- **Iron law:** data yield = kept/collected; kept × bytes ≤ egress budget.
- **Properties in tension:** adaptivity against privacy.
- **Manifestation:** hero robot — log + curate on-device; measure yield.
  Off-device retrain is provided/analytical (slow, out of session).
- **Models appear as:** training is off-device and treated as a black-box round
  with a cost and a delay; **we do not teach training** — we teach the *loop that
  feeds it and what a round costs*.
- **Carry forward:** engagement is data collection.

### S1. Architecture and the Runtime  *(new — open)*
- **Concept:** the components compose into one continuous, always-on system; the
  runtime is a supervisor loop + an event bus + a persistent state store, with the
  reasoner as the least-privileged actor.
- **Sections:** app vs runtime (why continuity, not one-off) · the three
  invariants (state in the store, comms on the bus, propose/dispose) · the
  supervisor loop and the lifecycle (wake/sleep/nightly maintenance) · the
  privilege boundary (LLM proposes, the gate disposes) · the skill library
  (capabilities added over time).
- **Properties in tension:** observability and reliability against complexity.
- **Manifestation:** hero robot — the runtime *is* the thing every other chapter's
  build plugs into; here it is assembled and shown surviving a restart.
- **Models appear as:** the reasoner service, sandboxed behind the gate.
- **Carry forward:** the runtime is the artifact the whole book builds.
- **Open decision:** own chapter (recommended — it is the through-line), or folded
  into S2 Placement?

### S2. Placement and Systems
- **Concept:** placement is the discipline's hardest move once capabilities share
  one budget; move one and the whole map shifts.
- **Sections:** the whole placement map · placements share a budget · re-placing
  ripples · criticality-first ordering.
- **Iron law:** Σ r_c ≤ R_box per shared resource.
- **Manifestation:** hero robot — fill the map with measured numbers, move one
  placement, measure the ripple.
- **Carry forward:** the system's character is the shape of its map.

### S3. Safety, Privacy, and Deployment
- **Concept:** a home deployment is a safety, privacy, and reliability problem
  head-on; ship only if every gate closes.
- **Sections:** deployment is a gate not a launch · the fail-safe (recovery time)
  · the privacy gate (egress audit) · ship / no-ship.
- **Iron law:** t_detect + t_act + t_brake ≤ t_harm; raw egress target = 0.
- **Manifestation:** hero robot — inject a failure and time recovery; audit the
  egress for an hour.
- **Carry forward:** privacy and safety are numbers you can show a parent.

### S4. The Human in the Loop  *(new — open, lowest priority)*
- **Concept:** the human is inside the loop — turn-taking, legibility, trust, and
  as teacher and labeler; a companion's loop closes through a person.
- **Sections:** the social loop as a real loop · legibility (the robot's state is
  readable) · trust and predictability · the human as the label source (ties to
  the flywheel).
- **Manifestation:** hero robot — a teaching/turn-taking interaction, measured for
  latency and legibility.
- **Open decision:** own chapter, a thread through C5/C8, or out of scope for v1?

### Capstone
- **Concept:** the discipline, demonstrated — defend every placement with a number.
- **Deliverable:** a working loop, a filled placement map, the binding constraint
  per placement, one re-placement and its ripple. A defended failure passes; an
  undefended success does not.

---

## 6. Cross-cutting threads (run through many chapters, introduced once)

- **The VLA thread:** introduced deeply in C3 (component: actions-as-intent), then
  reused — C5 (VLA as fast policy under a slow planner), C6 (intent → control,
  grounding gap → safety floor), C8 (improved by demonstration data). One concept,
  four deepening touch points.
- **The placement map:** a cumulative artifact the reader fills from C1 onward and
  completes in S2 — the book's signature worksheet.
- **The runtime (S1):** the through-line artifact; every chapter's manifestation
  plugs a service into it, so by the capstone the reader has built one continuous
  system, not eight demos.
- **Observability:** built in F2, read by every later measurement.
- **Safety and privacy:** foreshadowed from C1, bound in C6 and S3, never bolted
  on.
- **The human as teacher:** the engagement-is-data insight (C8) and the social
  loop (S4).

---

## 7. Open decisions to lock before writing prose

1. **Chapter list additions.** Take all three new chapters, some, or none?
   - **S1 Architecture and the Runtime** — recommended (it is the through-line).
   - **C4 World and Self State** — own chapter, or a section in C2/C7?
   - **S4 The Human in the Loop** — chapter, thread, or defer to v1.5?
2. **C2 reframe.** Confirm perception is recast as "perception in the loop"
   (active, budgeted sensing), with edge-model mechanics explicitly out of scope.
3. **Depth ceiling.** Confirm the rule "teach each concept to the depth the
   placement decision demands" as the guard against survey creep.
4. **Manifestation now.** Confirm hero-robot (Reachy) is the only active build
   track; UNO Q kit is a deferred rung named but not built.
5. **Order.** Does C4 (World and Self State) sit before or after C3 (Meaning and
   Intent)? Belief-before-meaning or meaning-before-belief.

Once these are settled, the next concrete step is to **write one chapter in full
as the exemplar** (recommend C3, the VLA home, because it exercises the hardest
version of the scaffolding), and the other chapters follow the pattern.
