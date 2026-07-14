# Chapter Outlines: The Canonical Drafting Scaffold

**Status:** the single source of truth for structure and per-chapter content.
Reconciles and supersedes the chapter list in OUTLINE.md. Round-5 north-star
decisions applied: graduate promise made explicit, labs end in an engineering
decision rather than placement alone, the growing runtime restored as the course
artifact, measurement embedded in every lab rather than spun out as a separate
product, audience locked to the serious learner and practicing engineer, and the
Reachy/UNO Q boundary made honest.
13 chapters.

## How to Use This

Each chapter has: **Crux** (the one load-bearing claim), **Objective** (what a
reader can do after), **Sections** (each with the beats to write), **Running scene**
(the Maya-and-Reachy moment that grounds it), **Figure**, and **Lab**. Every lab
climbs the mandatory rung: *visible signal → defensible number → engineering
decision*. Under the feedback constraint that decision is usually a placement.
Under the delegation constraint it may be a ship gate, authority boundary,
retention rule, consent decision, or fallback.

**Bullet voice (house style).** When we list, we list like the fundamental below: a
**bold declarative claim**, then a plain, concrete gloss with a specific physical
image, never an abstract restatement. "Action is irreversible. You cannot
un-knock-over the cup or un-startle the child." Claim, then a thing you can see.

## The North Star and Graduate Promise

This book teaches the missing engineering layer between a learned policy and its
deployment in the world. It does not claim the loop, placement, runtime assurance,
or the system properties as inventions. It owns their integration into a
measurable discipline for learned systems that act back into the world and receive
authority in human spaces.

> A graduate can take a physical-AI problem they have never seen, architect a
> continuous system for it, ground it in real time and space, measure the running
> loop, place every capability against a fixed budget and defend each choice,
> prove it reaches a safe state and keeps private data on the device, set up the
> human teaching-and-approval loop it lives inside, and diagnose it when the world
> makes it misbehave.

Seven verbs carry that promise: **frame, design, ground, measure and place,
assure, supervise, diagnose**. Each chapter must build one of those capabilities,
and the capstone must require evidence for all seven.

Two artifacts divide the work cleanly. **Reachy makes the consequence felt.**
The hero supplies the real scene, real stakes, and honest system limits. **The
UNO Q makes the mechanism reproducible.** Its MPU/MCU boundary lets a learner
measure and defend the architecture on one board. The measurement method lives
inside the labs and the growing runtime. Each lab emits an evidence record with
the operational definition, setup, uncertainty, result, and decision, without
creating a third product that must be maintained and validated independently.

The primary reader is a serious learner or practicing engineer. Makers can ride
along through the visible demonstrations, but rigor is not removed to make the
material look easier. Maya is the human context that keeps the engineering honest,
not a learner tier or a lab dependency.

## The Fundamental: What Closing the Loop Costs

Closing the loop with the world exacts a price that decoupled AI never pays. Stated
as it feels:

1. **Information is perishable.** The world moves while you compute. Its shelf life is set by the world, not by you.
2. **Knowledge is always partial and always stale.** You act on an estimate of a state that has already changed.
3. **Action is irreversible.** You cannot un-knock-over the cup or un-startle the child. The world keeps the consequence.

And the one that makes closed-loop *closed-loop*, the cost open-loop AI never faces:

4. **Your action changes what you will see next.** The robot's own move becomes its next input, so a small error compounds and it drifts into states it was never ready for.

Those four are the *experiential* framing, how it feels. Chapter 2 puts the rigor
underneath them as a **claims hierarchy** (theorem / heuristic / metaphor), because a
sharp reviewer will collapse #1 and #2 into one freshness claim and note that #3 is
really path-dependence, not literal irreversibility. The fourth, **endogeneity**, is
the uniquely-closed-loop cost. We black-box *how* to fix a policy, but we measure its
*effects* here (distribution shift, recovery frequency, departure from the validated
envelope). Bringing it back was the strongest external note: the book was hiding the
one property that makes closed-loop closed-loop.

**Energy is a first-class property, not a fourth price.** Joules bound how fast you
can compute against the freshness wall, so energy rides every measurement and every
placement as part of the constraint vector. But open-loop TinyML is energy-bound too,
so energy is a *physical-AI property*, prominent but not a *closed-loop* price.

**Two axes, not one spine.** The book runs on two constraints. The **feedback
constraint** (freshness, estimation, delay, stability, placement, recovery) carries
Parts I-IV. The **delegation constraint** (authority, safety, privacy, consent,
inspectability) carries Part V. Governance does not descend from "the loop prices
time"; it descends from handing an autonomous system authority in someone's home.
Naming both honestly beats forcing one to explain the other.

## Design Commitments (What Is Baked In)

1. **Defined by constraint, not capability** (the loop and its limit, not "physical AI" the noun).
2. **The claims hierarchy is the rigor test** (every load-bearing statement is a theorem, a heuristic, or a metaphor, labeled).
3. **Measurement is the discipline, and it must be metrology** (operational definitions, calibration, uncertainty, negative controls, reproducibility across ≥3 systems, and evidence the numbers predict outcomes, not a branded checklist).
4. **Cite the lineage honestly** (Simplex/RTA, SOTIF, the "-ilities", Age of Information, control theory); claim only the integration and the loop-measurement axis.
5. **Every lab makes one invisible property physically visible, measures it, and ends in a defensible engineering decision.**
6. **Recruit, then discipline** (the wow before the measurement).
7. **Kit manifests, hero realizes, Maya grounds** (Reachy is the active reference build and honest "no-enforcer" case study; the UNO Q becomes the reproducible release path, with every outcome assessable on the bare board; Maya is context, never a lab dependency).
8. **Diagnosis is a taught method** (hypothesis → bisect → confirm, introduced in Ch3, reinforced every "break it").
9. **Scope discipline** (models are black-box components; we measure the loop, including endogeneity's effects, we do not teach model internals).
10. **One runtime grows across the book** (Ch4 creates the measured skeleton; Ch5-Ch12 add services, placements, gates, and human authority to that same continuous system).
11. **Measurement is embedded, not separately branded** (Ch3 teaches the method, the runtime carries the reusable instrumentation, and Appendix A records the common evidence format).

## The Structure (13 Chapters)

```
index.qmd     Manifesto (states both axes)
Quickstart    Close Your First Loop            (unnumbered front matter, the recruit-hook)

FEEDBACK CONSTRAINT ─────────────────────────
Part I    The Discipline
  Ch1   Closed-Loop AI
  Ch2   The Price of the Loop
Part II   Measuring and Running the Loop
  Ch3   Measuring the Loop                     (moved: before the runtime)
  Ch4   The Runtime
Part III  Closing the Loop
  Ch5   Perception in the Loop
  Ch6   The World Model                        (the estimator)
  Ch7   The Reasoner                           (Meaning + Cognition, merged)
  Ch8   Action and Control
Part IV   The Whole System
  Ch9   Placement: Filling the Map             (crown; energy first-class)
  Ch10  Confidence Without the World

DELEGATION CONSTRAINT ───────────────────────
Part V    Into a Home
  Ch11  Safety, Privacy, and the Ship Gate
  Ch12  The Human Loop                         (absorbs forgetting)

Part VI   Capstone
  Ch13  Defend the Whole System

App A  Normative Measurement Protocol · App B  UNO Q Kit · App C  Hero and Home
(Memory dissolved: state → Ch6/Ch4, retention/egress → Ch11, forgetting → Ch12.)
```

---

## index.qmd — Manifesto

**Crux:** the loop just closed, and everything changed.
Beats: the dichotomy (open-loop perceives, closed-loop acts on the world it just
sensed and lives with what it changed); the turn (the moment it acts, the world
charges a price); the lineage (TinyML with the loop closed); the two axes named
plainly (the feedback constraint and the delegation constraint); the humble claim
("physical AI" is the crowded capability, this is the *engineering* of it). Short.
Plants the flag, proves nothing.

## Quickstart — Close Your First Loop (front matter, unnumbered)

The recruit-hook, no theory. Get the robot to see you and react in an hour, then slow
the loop by hand until the reaction feels wrong, and let that plant the question Ch2
answers. An experience, not a chapter.

---

## Part I. The Discipline

### Ch1 — Closed-Loop AI

**Crux:** learned systems acting in an open world create a demanding engineering
regime whose deployment properties must be measured and governed as a whole loop.
**Objective:** decide whether a system is closed-loop AI, identify the learned-
controller/open-world coupling, and locate the engineering layer below capability.

- **Open-Loop AI Perceives, Closed-Loop AI Acts.** The clean cut is not "perceives vs acts" but *does the action change the system's own future input distribution*. Give the honest counterexamples (a TinyML wake-word gating an actuator closes a loop; a chatbot does not). Teaching device, not a field-flag.
- **The Two Broken Assumptions.** Learned controller and open world. Neither is new; their coupling creates the deployment problem this book makes measurable. The loop itself is Maxwell, 1868.
- **Endogeneity, the Closed-Loop Signature.** Your action changes what you see next. Name it as the first-class cost that makes this regime unique. We *measure* its effects here (distribution shift, recovery frequency, envelope departure); we do not teach how to fix the policy, that is the policy-learning course. Measure the symptom, black-box the cure.
- **The Two Axes.** The feedback constraint (this book's engine) and the delegation constraint (Part V). Preview both so Part V does not read as a different book.
- **An Engineering Layer Across Embodied AI, Control, and CPS.** Position, cite the lineage, and own the substrate-independence (high-frequency trading is closed-loop AI with no robot); physical AI is where the constraints bite hardest and where consequences become literal.
- **The Engineering Layer Beneath "Physical AI."** Software Engineering : software :: this : physical AI.

**Scene:** Robby follows Maya before she finishes turning; the same Robby drifts wrong
after acting on its own last move. Freshness and endogeneity, felt.
**Figure:** the open-loop → closed-loop diagram (the arrow that closes, and feeds back).
**Experience (Quickstart tie-in):** notice the reaction lag; it plants Ch2.

### Ch2 — The Price of the Loop

**Crux:** you cannot be both fully informed and fully current; the gap is measurable,
and the world sets it.
**Objective:** state the price as a claims hierarchy, name the world's timescale as a
measurable quantity, compute η_loop.

- **The Four Costs, as Felt.** The house-voice bullets (perishable, partial-and-stale, irreversible, endogeneity). The intuition pump.
- **The Claims Hierarchy** (the rigor, Codex's #1 ask). Separate what is a **theorem**, a **heuristic**, and a **metaphor**. "You cannot be both fully informed and fully current" is the demonstrable claim; "the Carnot limit" is dropped (or labeled explicitly as aspiration).
- **The Freshness Price, as Three Theorems** (cite all three, honestly scoped):
  - *Estimation.* Error in the current state grows with the age of your last sample; for a mean-reverting source it has a closed form whose knee names the world's decorrelation time. Value-of-information is non-monotone in age (a stale-but-correct belief costs nothing), so age is a *surrogate*, not the bound.
  - *Information.* The data-processing inequality: delay can only lose information, not create it. But it does *not* prove intelligence cannot help, the predictor below is the counterexample. State it scoped.
  - *Control.* Loop delay eats phase margin; past a delay the loop cannot track, dependent on plant, controller, and task.
  - Anchor on **Age of Information** (Kaul-Yates-Gruteser, 2012).
- **Intelligence Buys Back the Predictable Part.** A world model acts on a *prediction*; the irreducible floor is the *innovation*, not the age. Sets up the World Model and the two-speed brain.
- **η_loop, the Diagnostic (Not a Universal Merit).** η_loop = loop-latency / world-timescale, reported **per loop and per regime**, with a stated latency percentile and a precisely defined task timescale. A single scalar hides the binding failure mode; use it as a normalized diagnostic, not a figure of merit.

**Scene:** how late can Robby see Maya and still catch her turn? That age is her
motion's timescale.
**Figure:** the value-decay curve, quality vs information age, knee marked.
**Lab (Measure the Wall):** drive the loop on perception of controlled age Δ; plot
quality vs Δ; extract the knee and compute η_loop. Add a predictor and show the wall
*moves* → decide whether prediction, a faster path, or a slower operating regime is
the defensible response. Number: η_loop, before and after.

---

## Part II. Measuring and Running the Loop

### Ch3 — Measuring the Loop (moved: before the runtime)

**Crux:** you do not own a property until you can put a number on it, and the number
has to be metrology, not a checklist.
**Objective:** measure a loop's properties rigorously, defend them, and know what
makes a measurement valid.

- **What to Measure.** Tail latency (not mean), joules per decision (energy, first-class here), egress bytes per hour, time-to-safe-state, drift, recovery frequency (endogeneity's fingerprint), and η_loop as the summary ratio.
- **Metrology, Not a Branded Checklist** (Codex's bar). Operational definitions, calibration, uncertainty intervals, repeatability, reference tasks, comparison rules, negative controls. A measurement earns its place only if it *predicts an engineering outcome*.
- **Measure Externally, Never on the Hot Path.** GPIO to a logic analyzer, an external power rail; self-timing on a shared-Linux MPU perturbs what it measures. Borrow MLPerf Tiny's discipline.
- **Two Tiers, Enforced in the Evidence Record.** Deterministic *replay* = BENCHMARK (frozen log, error bars, a task-efficacy floor scored against ground truth so a do-nothing system cannot win). Live closed loop = CHARACTERIZATION, relative A-vs-B on a fixed rig, never absolute cross-lab numbers. Every lab report names the tier explicitly.
- **The Diagnostic Method.** Hypothesis → bisect → confirm; the reusable procedure every later "break it" reinforces.

**Scene:** the first honest numbers for Robby's face-tracking loop.
**Figure:** the loop's measured properties, replay tier, with η_loop and its error bars.
**Lab (Your First Measurement):** replay-tier measurements for one capability with the
task-efficacy floor → accept or reject the measurement and the engineering claim it
supports. This establishes the evidence format reused by every later lab. (Because
this chapter precedes the runtime, the reader measures requirements *before* being
handed an architecture.)

### Ch4 — The Runtime

**Crux:** the loop becomes a discipline only when it is a process that pays its price
on time, survives its own failures, and is *derived from the measurements*, not
prescribed.
**Objective:** architect a runtime and defend where the propose/dispose line sits.

- **From a Loop to a Living Process.** What runs at 3pm on a Tuesday, hour 400.
- **The Services.** Perception, reasoner, safety gate, body, memory/state, scheduler, logger. (Persistent state lives here, absorbing part of the old Memory chapter.)
- **Three Invariants.** State in the store, comms on the bus, reasoner proposes and safety disposes.
- **The Action Contract.** Intents in, bounded primitives out.
- **The Simplex and Runtime-Assurance Lineage.** Cite Sha honestly; the delta is observability and measurability at kit scale; the honest limit is that a box-clamp is a *saturation*, not a certified forward-invariant safe-set switch.
- **The Coupling Made Silicon.** The UNO Q's MPU proposes, MCU disposes.
- **Restart, Recovery, and Observability.**

**Scene:** the UNO Q's MCU holds the test rig still when its reasoner hangs;
Reachy exposes the contrasting cost of having no independent enforcer.
**Figure:** the runtime, services on the bus, propose/dispose across two chips.
**Lab (The Chip That Says No):** the MCU physically refuses a bad MPU command → measure
the veto latency → argue why it is the placement's binding constraint.

---

## Part III. Closing the Loop

### Ch5 — Perception in the Loop

**Crux:** sensing is a timed, budgeted action, not a free given.
**Objective:** choose a sensing operating point from measured efficacy, latency,
energy, and bandwidth, then defend where perception runs.
- **Sensing Is an Action, Not a Given.**
- **Perceive at the Knee, Not the Peak** (accuracy vs latency vs energy).
- **The Sensor Firehose and What You Keep.**
- **A Late Perception Is a Wrong Perception** (freshness, applied).
- **Placement of Perception** (which chip, which box).
**Scene:** at full res Robby misses Maya's turn; at the knee it catches it.
**Figure:** the sensing trade curve, with the knee and missed-deadline region marked.
**Lab (The Deadline Light):** LED reddens on a missed deadline → measure the knee →
defend the operating point.

### Ch6 — The World Model (the estimator)

**Crux:** the world model is a *state estimator*; belief is always stale, and the art
is knowing how stale and buying back the predictable part.
**Objective:** build a frames-and-timing diagram, maintain a timestamped belief
with uncertainty, measure drift, and place the correction that binds.
- **Coordinate Frames and Transforms.**
- **Clocks, Timestamps, and Synchronization.**
- **The End-to-End Latency Budget** (photon to motion).
- **The Estimator and the Innovation Floor** (Bayes/Kalman; the buy-back machine from Ch2).
- **Sensor Fusion Into a Belief.**
- **Belief, Uncertainty, and Drift** (and the endogeneity check: has the robot's own action pushed belief off the world?).
**Scene:** Robby predicts where Maya's face will be, and beats its own latency.
**Figure:** raw observations flowing through transforms and timestamps into a
belief with uncertainty and an innovation residual.
**Lab (Two Frames Disagree):** transform + measure timestamp skew → the drift number →
place the fix.

### Ch7 — The Reasoner (Meaning + Deliberation, merged)

**Crux:** the slow, semantic path, deciding what the world means and whether it is
worth the time to think; and the two-speed brain is the *resolution* of the freshness
price, not a contradiction of it.
**Objective:** turn a request into a grounded bounded intent, and build the policy that
decides when to invoke the slow path.
- **From Pixels to Meaning** (the VLM as a black-box component).
- **The Grounding Gap** (words are not coordinates).
- **Intent, Not Commands** (the propose side; what the model may and may not decide).
- **Vision-Language-Action Models.**
- **Two Speeds, Because Time Is Priced** (reflex stays current, deliberation decides well; multi-rate; cite the async-inference frontier so it reads as the answer to Ch2).
- **When to Think Hard** (uncertainty as the escalation trigger).
- **The Escalation Ladder, and Falling Back** (rungs; graceful degradation when the slow path fails).
- **Placement of Meaning** (worth the freshness a round trip costs?).
**Scene:** Robby's reflex holds his gaze on Maya while the slow brain grounds "look at
the red one."
**Figure:** the two-speed path, with a bounded reflex continuing beneath a slower
semantic escalation and the intent boundary marked.
**Lab (Meaning and the Round Trip):** request → bounded intent; meter reflex vs
deliberation and measure how a fast rate tolerates more staleness → place it.

### Ch8 — Action and Control

**Crux:** a learned proposer will eventually be wrong, the consequence is
path-dependent, and delay itself can destabilize the loop.
**Objective:** turn bounded intent into safe motion, measure the available margin,
and defend the enforcement boundary without mistaking it for a safety case.
- **From Intent to Safe Motion** (the dispose side).
- **The Safety Envelope** (bounds the model cannot cross).
- **An AI Choice Is a Control Choice.**
- **Path-Dependence and Margin** (the rigorous form of "irreversible", the action changes future state, options, and risk; time and distance are the same constraint).
- **Delay Destabilizes** (the dead-time limit made physical, add too much loop delay and the envelope oscillates no matter how good the model).
- **The MCU as Enforcer, and Its Honest Limit** (teaching instrument, not a certified safety case).
**Scene:** Robby's head begins an over-eager turn toward Maya; the envelope clamps
the motion before speed and delay consume the available margin.
**Figure:** intent passing through the safety envelope, with stopping distance and
delay margin made visible.
**Lab (Watch the Envelope Hold):** force a violation, watch the clamp → measure stopping
time/distance → add delay until it rings → choose the safe operating region and
defend where enforcement must run.

---

## Part IV. The Whole System

### Ch9 — Placement: Filling the Map (crown)

**Crux:** every isolated placement was right; together they do not fit, and the map is
where you see the trade whole.
**Objective:** fill the system placement map from measured constraints, name the
binding resource for each capability, and predict the ripple from one re-placement.
- **The Placement Map** (every capability by loop and by box).
- **The Placement Address.** Name the loop, box, and enforcement domain for each capability; MCU or MPU is an enforcement and timing choice, not a resource metric.
- **The Constraint Vector.** Evaluate latency, task efficacy, energy, bandwidth, memory, privacy, recovery, and drift; latency × efficacy × energy is one useful projection, not the whole map.
- **Placements Share a Budget** (the budget identity lands here, where it is real).
- **Place the Tightest Constraint First** (criticality ordering).
- **Move One Thing, Measure the Ripple** (including the endogeneity ripple, does the re-placement change what the loop drives itself into?).
- **The Map Is the Design.**
**Scene:** meaning, tracking, safety, and power all want the device, and cannot all have it.
**Figure:** the complete placement map, with shared budgets and the binding
constraint for each placement.
**Lab (Fill the Map, Move One Thing):** measured map → one re-placement → the ripple.

### Ch10 — Confidence Without the World

**Crux:** you cannot replay a world that moved, so you earn trust in tiers.
**Objective:** choose the appropriate confidence tier, identify where its evidence
becomes invalid, and make a staged-rollout decision from measured divergence.
- **You Cannot Replay Reality.**
- **Simulation, and Where It Lies** (contact, sensor timing, actuator delay).
- **Replay, and When It Goes Invalid** (the instant the policy would diverge, endogeneity again).
- **Shadow Mode.**
- **Earning Trust One Rung at a Time** (staged rollout).
- **Two Tiers, Benchmark and Characterization** (the replay/live split from Ch3, plus relative ranking for the live tier).
**Scene:** the new gaze policy vetted in shadow before it ever moves Robby's head.
**Figure:** the confidence ladder from replay through shadow to bounded live
operation, with each tier's invalidation boundary.
**Lab (Run It in Shadow):** shadow the new policy → measure where it would have
diverged → decide whether it advances, remains in shadow, or is rejected.

---

## Part V. Into a Home (the delegation constraint)

### Ch11 — Safety, Privacy, and the Ship Gate

**Crux:** shipping does not make the robot smarter; it makes it, and the family,
more exposed, and two non-negotiable numbers can veto readiness without pretending
to constitute a complete safety case.
**Objective:** produce a written ship/no-ship gate from confidence-tier evidence,
time-to-safe-state, egress, and the known boundary where certification takes over.
- **Deployment Is a Gate, Not a Launch.**
- **Delegation, the Second Axis** (this Part descends from handing an autonomous system authority in a home, not from "the loop prices time"; say so).
- **The Fail-Safe** (time-to-safe-state vs the harm budget).
- **The Privacy Gate** (egress bytes; retention limits, absorbing part of the old Memory chapter).
- **A Child in the Room** (Maya's *actual words* as the worked egress example; the COPPA-shaped line).
- **The Ship or No-Ship Decision, Written Down.**
- **Where Certification Takes Over** (the honest edge of a teaching kit).
**Scene:** the hour of Maya's living room that must never leave the device.
**Figure:** the ship gate, with confidence evidence, harm budget, egress boundary,
and certification handoff shown separately.
**Lab (The Ship/No-Ship Gate):** recovery time + egress audit → the two numbers → ship
or don't.

### Ch12 — The Human Loop

**Crux:** the person who teaches the robot and lives with it holds the real authority.
**Objective:** build and defend the approval, consent, inspect-and-forget, and
offline-continuity paths through which a person retains authority over the system.
- **The Robot Lives With Someone.**
- **Teaching a New Skill.**
- **The Approval Gate** (nothing new without an adult's yes).
- **Consent and the Boundary.**
- **Inspect, Edit, Forget** (memory governance, *forgetting as a first-class operation* moved intact from the dissolved Memory chapter, it belongs here with consent and human control).
- **The Engagement Loop Is the Data Loop** (corrections as labels; the flywheel).
- **The Cost of a Turn.**
- **When the Servers Go Dark** (graceful offline degradation, portability, the robot's mortality; Moxie/Jibo as the warning).
**Scene:** Maya teaches Robby a trick; Dad approves it; it can be forgotten.
**Figure:** the human authority loop, separating proposed skill, adult approval,
inspectable memory, consented learning data, and offline fallback.
**Lab (The Authority Test):** three gated checkpoints: teach and approve; inspect
and forget; pull the cloud and verify the bounded experience that remains. Each
checkpoint records a number and ends in an authority, retention, or continuity
decision.

---

## Part VI. Capstone

### Ch13 — Defend the Whole System

**Crux:** success is not merely whether it worked once. Success is whether measured
evidence explains where every part lives, what authority it holds, and why the
decision being defended is warranted.
**Objective:** defend an unfamiliar physical-AI system using evidence for all
seven graduate verbs, including one diagnosed failure.
- **The Deliverable** (a working loop plus an integrated defense containing the problem frame; runtime and action contract; frames, timing, and belief; measurement and placement map; assurance and ship gate; human authority and forgetting; one re-placement; and one diagnosed failure).
- **The Gated Artifacts** (runtime design defense, ship/no-ship gate, teach/approve/forget, distributed as earlier checkpoints, not crammed here).
- **The Greenfield Synthesis** (architect a runtime for an embodiment you have not seen, the design muscle the book must exercise).
- **The Diagnosis** (one failure, found and explained, using the taught method).
- **A Defended Failure Beats an Undefended Success.**
- **The Discipline, In Your Hands.**
**Scene:** the system succeeds once, then the defense begins; the measured failure
reveals more engineering judgment than the polished demo.
**Figure:** the final evidence dossier, with one artifact mapped to each graduate verb.
**Lab (The Defense):** demonstrate the loop, present the integrated dossier, then
architect a greenfield runtime for an unfamiliar embodiment and defend one failure.

---

## Appendices

- **A. Normative Measurement Protocol.** The common evidence format used by the labs: operational definitions, the two tiers, per-property recipes, uncertainty and negative-control protocols, and the validation study (≥3 systems with different dynamics).
- **B. The UNO Q Kit.** The two chips, the bridge, placement-by-chip, the propose/dispose demo, bring-up.
- **C. The Hero and the Home.** Reachy as hero *and* honest "no-enforcer" case study; Maya as the ground-floor context.

## Locked Decisions

- **The title is final.** *Physical AI: Machine Learning Systems That Sense and Act.*
- **Endogeneity stays threaded.** It is a property of the running loop rather than a separate chapter.
- **Energy stays first class.** It remains a measured property rather than a co-fundamental.
- **The primary reader is the engineer.** Makers receive accessible manifestations rather than reduced rigor.
