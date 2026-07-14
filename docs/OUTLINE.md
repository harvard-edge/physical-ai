# Physical AI Engineering: The Discipline of Closed-Loop AI

> ⚠️ **SUPERSEDED for structure.** After the Round-4 review, the canonical chapter
> list and per-chapter content live in **CHAPTER-OUTLINES.md** (13 chapters, the two
> axes, Memory cut, Meaning+Cognition merged, measurement before the runtime). This
> file is kept for its design-commitment and appendix detail; where the two disagree,
> CHAPTER-OUTLINES.md wins.

**Status:** working draft, rewritten through the closed-loop lens. Supersedes the
prior outline. Built on OUTCOMES.md (six graduate outcomes), pressure-tested in
PANEL-REVIEW.md (8 experts + 3 incumbents). Scope and pedagogy in CURRICULUM.md.

## The Thesis, and Where It Lives

The book has one idea, stated as a dichotomy:

> **Open-loop AI** perceives. It classifies, predicts, generates, and hands the
> result to a human or a rule. Everything today is this, including TinyML.
> **Closed-loop AI** acts on the world it just sensed, and lives with what its
> action changed.

And one fundamental, which is why closed-loop AI is a discipline and not a demo:

> **Closing the loop with the world prices time.** Information becomes perishable,
> action becomes irreversible, and decision quality is bounded by the freshness of
> what you know. That bound is measurable, model-agnostic, and durable. It is the
> Carnot limit of the field.

Two places carry this, at two altitudes:

- **`index.qmd` (landing / manifesto):** plants the flag. The dichotomy, the
  fundamental, the lineage from TinyML, who it is for, why it exists. States the
  thesis, does not prove it. Short and sharp.
- **Chapter 1:** teaches the frame rigorously. What closed-loop AI is, the two
  broken assumptions, the fundamental, the positioning against the neighbors.

## Design Commitments (What Is Baked In)

1. **Defined by constraint, not capability.** The subject is the loop and its
   limit, the way Carnot defined a heat engine by its bound, not "physical AI" the
   capability noun (that is Nvidia's, HF's, the embodied-AI field's).
2. **The fundamental is the spine.** Every chapter ties back to "the loop prices
   time." The properties, the two-speed brain, safety, placement, all descend from
   it.
3. **Measurement is the discipline.** Defend every placement with a number. The
   measurement protocol (Appendix A) is the moat, vendor-neutral, two-tier (a
   deterministic replay-slice *benchmark* and an honest closed-loop
   *characterization*).
4. **Spine-first spiral.** The runtime is built early (Ch3) and thickened after,
   not a data-flow march that only assembles at the end.
5. **Cite the lineage honestly.** Propose/dispose is Simplex and runtime assurance
   (Sha). The open world is SOTIF. The properties are the "-ilities." The loop is
   control theory. Name what is borrowed; claim only the integration and the
   loop-measurement axis.
6. **Concede what others own.** The safety *case* belongs to certification (ISO
   13482, functional-safety standards). Propose/dispose is a *teaching instrument*,
   not a safety guarantee. Latency-by-placement and model internals belong to
   others too.
7. **Every lab makes one invisible property physically visible.** A light that
   reddens on a missed deadline, the MCU refusing a command, a byte counter on
   egress.
8. **Recruit, then discipline.** Lead with the wow (close your first loop, the
   robot sees and acts), then puncture it with the measurement twist. Do not make a
   beginner earn the wow.
9. **Kit manifests, hero realizes, Maya grounds.** Every outcome is assessable on
   the bare $59-79 UNO Q. Reachy is the aspirational hero *and* the honest
   "no-enforcer" case study. Maya is the ground-floor context that makes safety,
   privacy, and consent concrete, never a lab dependency, never a gimmick.
10. **Diagnosis is threaded.** Every lab ends with "break it and find why."
11. **Scope discipline.** Models are black-box components with measured properties.
    No training, quantization, or architecture internals.

## The Shape at a Glance

| **Part** | **Ch** | **Title** | **Outcome** | **How it descends from "the loop prices time"** |
| --- | --- | --- | --- | --- |
| — | — | Landing (index.qmd) | — | states it |
| I. The Discipline | 1 | Closed-Loop AI | O1 | names the regime the price applies to |
| | 2 | The Loop Prices Time | O1, O4 | *is* the fundamental, and the nine properties as its children |
| II. The System | 3 | The Runtime | O2 | the machine that pays the price on time, every time |
| III. Closing the Loop | 4 | Perception in the Loop | O3 | a late perception is a wrong perception |
| | 5 | The World Model | O3 | belief is always stale; how stale, and how you know |
| | 6 | Meaning and Intent | O4, O3 | meaning is slow; is it worth the freshness it costs |
| | 7 | Cognition and the Deliberation Policy | O4, O2 | the two-speed brain exists *because* thinking spends time |
| | 8 | Action and Control | O4, O2 | the irreversible half of the price |
| | 9 | Memory and Persistence | O3, O6 | what survives across loops, and what must be forgettable |
| IV. The Whole System | 10 | Placement: Filling the Map | O4 | where each capability sits on the freshness/cost frontier |
| V. Into the World | 11 | Confidence Without the World | O5 | you cannot replay a world that moved |
| | 12 | Safety, Privacy, and the Ship Gate | O5 | the price of being wrong, in a home |
| | 13 | The Human Loop | O6, O4 | the slowest loop, and the one that owns the robot |
| VI. Capstone | 14 | Defend the Whole System | all | pay every price, defend every number |
| Appendices | A | The Closed-Loop Measurement Protocol | spine | the instrument that makes the price measurable |
| | B | The UNO Q Kit | platform | the two chips that make the price physical |
| | C | The Hero and the Home | pedagogy | Reachy as honest case study, Maya as ground floor |

Fourteen chapters, three appendices, a landing page.

---

## Landing Page (`index.qmd`)

Not a chapter. The manifesto. Roughly these beats, kept short:

- **The dichotomy**, stated cold: open-loop AI perceives, closed-loop AI acts.
- **The turn**: the moment a system acts on the world it sensed, time stops being
  free, and everything hard follows from that one fact.
- **The lineage**: this is TinyML with the loop closed. You learned to make a
  device perceive; now you make it act, and account for the consequence.
- **The claim, humbly**: "physical AI" is the capability, and it is crowded.
  This book is the *engineering* of it, the discipline of closed-loop AI, defined
  by its limit and taught by measurement.
- **Who it is for and how to read it**: the embedded and TinyML community stepping
  up; the kit, the hero, and the through-line artifact.

---

## Part I. The Discipline

### Chapter 1. Closed-Loop AI

- **Premise:** what changes the instant a system acts on the world it just sensed.
- **Outcome:** O1. **Property:** all, previewed.
- **Sections:**
  - Open-Loop AI Perceives, Closed-Loop AI Acts
  - The Two Broken Assumptions: A Learned Controller and an Open World
  - Why It Is Not Embodied AI, Control Theory, or Cyber-Physical Systems (position honestly, cite the lineage; the new part is the *learned* controller in the *open* world)
  - Why It Is Not "Physical AI" the Capability: the Engineering Layer Underneath
  - The Nine Properties, Previewed
  - The Recurring Move: Placement, Defended by a Number

::: {.callout-lab title="Lab 1: Close Your First Loop"}
**Does:** the recruit hook, not the discipline yet. Get the robot to see you and
react, one closed loop, in the first hour, no measurement.
**Makes visible:** the loop itself, the moment perception becomes action.
**Kit / Hero:** UNO Q with a camera and a servo; Reachy tracks your face.
**Break it:** slow the loop down by hand until the reaction feels wrong, and let
that plant the question Chapter 2 answers.
**Links out to:** lab repo (TBD).
:::

### Chapter 2. The Loop Prices Time

- **Premise:** the one fundamental the whole field rests on, and why it is a limit,
  not a slogan.
- **Outcome:** O1, O4. **Property:** all, as children of the fundamental.
- **Sections:**
  - Information Is Perishable: Its Shelf Life Is Set by the World
  - Action Is Irreversible: You Cannot Take It Back
  - The Freshness Bound: Decision Quality Is Capped by the Age of What You Know
  - You Cannot Be Both Fully Informed and Fully Current
  - The Nine Properties Are How the Price Shows Up (timeliness, reliability, safety, memory, energy, privacy, robustness, adaptivity, observability)
  - The Budget Identity, and the Measurement Stance: You Do Not Own a Property Until You Can Put a Number on It

::: {.callout-lab title="Lab 2: Measure the Wall"}
**Does:** make the freshness bound bite. Have the robot act on perception of a
chosen age; plot decision quality against information age; find the wall where more
intelligence buys nothing because the world already moved.
**Makes visible:** the price of time, a target the robot chases and cannot catch
once the loop is too slow.
**Kit / Hero:** UNO Q chasing a moving marker; the seed of the measurement protocol.
**Break it:** add compute to the decision and watch currency, not quality, decide.
**Links out to:** lab repo + Appendix A (TBD).
:::

---

## Part II. The System

### Chapter 3. The Runtime

- **Premise:** the loop has to pay the price on time, for the four-hundredth hour.
  What holds it together?
- **Outcome:** O2. **Property:** reliability, observability, safety.
- **Sections:**
  - From a Loop to a Living Process
  - The Services: Perception, Reasoner, Safety Gate, Body, Memory, Scheduler, Logger
  - Three Invariants: State in the Store, Comms on the Bus, Reasoner Proposes and Safety Disposes
  - The Action Contract: Intents In, Bounded Primitives Out
  - Propose/Dispose Is Old: the Simplex and Runtime-Assurance Lineage (cite it, state the delta: we make the boundary observable and measurable)
  - The Coupling Made Silicon: the UNO Q's MPU and MCU
  - Restart, Recovery, and Observability

::: {.callout-lab title="Lab 3: The Chip That Says No"}
**Does:** build the runtime skeleton and wire the propose/dispose boundary so the
real-time MCU can physically refuse a command the MPU proposed.
**Makes visible:** the MCU vetoing the AI, propose/dispose you can watch. This is
the kit's signature demo, buildable for under $100.
**Kit / Hero:** UNO Q across both chips (honest); Reachy runs the runtime on one
brain (and Appendix C explains why it *cannot* show this).
**Break it:** crash a service and confirm the supervisor recovers and the body
stays safe.
**Links out to:** lab repo (TBD).
:::

---

## Part III. Closing the Loop

### Chapter 4. Perception in the Loop

- **Premise:** sensing is not free and not instant. It is a timed, budgeted choice.
- **Outcome:** O3, O4. **Property:** timeliness, energy.
- **Sections:**
  - Sensing Is an Action, Not a Given
  - Perceive at the Knee, Not the Peak
  - The Sensor Firehose and What You Keep
  - A Late Perception Is a Wrong Perception (the freshness bound, applied)
  - Placement of Perception: Which Chip, Which Box

::: {.callout-lab title="Lab 4: The Deadline Light"}
**Does:** measure the accuracy, latency, and energy knee of a detector; pick the
operating point; wire an LED that reddens when perception misses its deadline.
**Makes visible:** the perception deadline, the moment fast-enough fails.
**Kit / Hero:** UNO Q detector; Reachy's gaze latency.
**Break it:** push resolution up until the light stays red, and read the knee.
**Links out to:** lab repo (TBD).
:::

### Chapter 5. The World Model

- **Premise:** a detection is a pixel until it is a point in the body's frame at a
  known time. Where, what, and *when*.
- **Outcome:** O3. **Property:** timeliness, robustness, reliability.
- **Sections:**
  - Where Am I: Coordinate Frames and the Transforms Between Them
  - When Did It Happen: Clocks, Timestamps, and Synchronization
  - The End-to-End Latency Budget, From Photon to Motion
  - What Is Around Me: Fusion Into a Belief
  - What Is My Body Doing: Proprioception
  - Belief Under Uncertainty, and Detecting Drift (belief is always stale; how stale, and how you know)

::: {.callout-lab title="Lab 5: Two Frames Disagree"}
**Does:** transform a detection from image space into the body frame and act on it;
measure timestamp skew; show the same object in two frames and the moment they
diverge.
**Makes visible:** drift, belief coming apart from the world.
**Kit / Hero:** UNO Q transform + skew measurement; Reachy tracks in its own frame.
**Break it:** delay one sensor stream and watch the belief lie.
**Links out to:** lab repo (TBD).
:::

### Chapter 6. Meaning and Intent

- **Premise:** the model can name what it sees. That is not the same as knowing
  what to do, or being allowed to decide it, and meaning is slow.
- **Outcome:** O4, O3. **Property:** latency, privacy, robustness.
- **Sections:**
  - From Pixels to Meaning: the VLM as a Black-Box Component
  - The Grounding Gap: Words Are Not Coordinates
  - Intent, Not Commands: What the Model May and May Not Decide
  - Vision-Language-Action: When Perception, Language, and Action Share a Model
  - Placement of Meaning: Is It Worth the Freshness a Round Trip Costs

::: {.callout-lab title="Lab 6: The Cost of a Round Trip"}
**Does:** turn a spoken request into a grounded, bounded intent; measure the cost
of answering locally versus in the cloud.
**Makes visible:** the bytes and latency of a cloud round trip beside a local answer.
**Kit / Hero:** UNO Q local-vs-cloud bench; Reachy responds to a request.
**Break it:** cut the network mid-request and watch the intent degrade or stall.
**Links out to:** lab repo (TBD).
:::

### Chapter 7. Cognition and the Deliberation Policy

- **Premise:** thinking hard spends time you may not have. When is a situation
  worth it?
- **Outcome:** O4, O2. **Property:** timeliness, reliability, energy.
- **Sections:**
  - Two Speeds Because Time Is Priced: Reflex Stays Current, Deliberation Decides Well
  - When Is a Situation Worth Thinking Hard About? Uncertainty as the Trigger
  - The Escalation Ladder and Its Rungs
  - The Cost of Thinking: Latency and Energy of Deliberation
  - Falling Back: Graceful Degradation When the Slow Path Is Gone

::: {.callout-lab title="Lab 7: The Escalation Meter"}
**Does:** build the uncertainty-triggered escalation from reflex to deliberation;
meter how often it fires and what each rung costs.
**Makes visible:** the reflex-versus-deliberation rate and its latency, live.
**Kit / Hero:** UNO Q two-speed loop; Reachy escalates on a hard case.
**Break it:** force constant escalation and watch the loop miss its deadline.
**Links out to:** lab repo (TBD).
:::

### Chapter 8. Action and Control

- **Premise:** a learned proposer will eventually propose something wrong, and the
  action cannot be taken back.
- **Outcome:** O4, O2. **Property:** safety, timeliness.
- **Sections:**
  - The Dispose Side: Turning an Intent Into Safe Motion
  - The Safety Envelope: Bounds the Model Cannot Cross
  - An AI Choice Is a Control Choice
  - Irreversibility and Margin: Time and Distance Are the Same Constraint
  - The MCU as Enforcer, and the Honest Limit: a Teaching Instrument, Not a Safety Case (cite where certification takes over)

::: {.callout-lab title="Lab 8: Watch the Envelope Hold"}
**Does:** implement the safety envelope on the kit, then try to make the model
violate it and watch the bound clamp the command in real time.
**Makes visible:** the envelope clamping an out-of-bounds action as it happens.
**Kit / Hero:** UNO Q envelope on a servo; Reachy's motion bounds.
**Break it:** feed the proposer garbage and confirm the body still cannot exceed
the bound.
**Links out to:** lab repo (TBD).
:::

### Chapter 9. Memory and Persistence

- **Premise:** the robot cannot keep everything, and some things it must be able to
  drop on request. What survives across loops.
- **Outcome:** O3, O6. **Property:** memory and state, privacy.
- **Sections:**
  - What Persists: the State Store Across Time
  - Retention Under a Budget: You Cannot Keep Everything
  - Recall: Finding the Right Memory Fast Enough
  - Forgetting as a First-Class Operation
  - Episodic and Semantic: What Kind of Memory for What Job

::: {.callout-lab title="Lab 9: Recall, Then Truly Forget"}
**Does:** build a bounded memory with fast recall and a working forget.
**Makes visible:** a memory recalled, then genuinely gone after a forget.
**Kit / Hero:** UNO Q memory store; Reachy remembers a name, then forgets on request.
**Break it:** overflow the budget and watch what recall drops first.
**Links out to:** lab repo (TBD).
:::

---

## Part IV. The Whole System

### Chapter 10. Placement: Filling the Map

- **Premise:** every isolated placement was right. Together they do not fit.
- **Outcome:** O4, the crown. **Property:** all, in tension.
- **Sections:**
  - The Placement Map: Every Capability by Loop and by Box
  - The Third Axis: Placement by Chip, MCU or MPU
  - Placements Share a Budget: the Sum That Must Fit
  - Criticality First: Place the Tightest Constraint, Then Fit the Rest
  - Re-placing Ripples: Move One Thing, Measure the System Effect
  - The Map Is the Design, and the Frontier Is the Freshness/Cost Trade

::: {.callout-lab title="Lab 10: Fill the Map, Move One Thing"}
**Does:** instrument the whole robot, fill the placement map with measured numbers,
then move one placement and report the ripple.
**Makes visible:** the whole map lit with real numbers, and a re-placement that
frees one budget and breaks another.
**Kit / Hero:** UNO Q full instrumentation; the hero analyzed with the same budgets.
**Break it:** move the capability whose constraint binds hardest and watch the loop
fail.
**Links out to:** lab repo + Appendix A (TBD).
:::

---

## Part V. Into the World

### Chapter 11. Confidence Without the World

- **Premise:** you cannot replay a world that moved. How do you trust the loop
  before it acts?
- **Outcome:** O5. **Property:** reliability, robustness, observability.
- **Sections:**
  - You Cannot Replay Reality: Why Closed-Loop Testing Is Different
  - Simulation: a World Cheap Enough to Run a Thousand Times, and Where It Lies
  - Replay: Yesterday's Sensor Log as Today's Test, and When It Goes Invalid
  - Shadow Mode: Running the New Policy Without Letting It Act
  - Staged Rollout: Earning Trust One Rung at a Time
  - Two Tiers: the Deterministic Replay Benchmark vs the Honest Closed-Loop Characterization

::: {.callout-lab title="Lab 11: Run It in Shadow"}
**Does:** build a replay test for the kit and run a new policy in shadow beside the
live one.
**Makes visible:** the shadow policy's decisions next to the live one's, with
neither acting.
**Kit / Hero:** UNO Q replay + shadow; the hero's policy vetted before it moves.
**Break it:** find the input where the shadow would have diverged, and see the
replay go invalid.
**Links out to:** lab repo (TBD).
:::

### Chapter 12. Safety, Privacy, and the Ship Gate

- **Premise:** shipping does not make the robot smarter. It makes it, and the
  family, more exposed.
- **Outcome:** O5. **Property:** safety, privacy, reliability.
- **Sections:**
  - Deployment Is a Gate, Not a Launch
  - The Fail-Safe: a Number for What Happens When It Fails (process safety time)
  - The Privacy Gate: a Number for What Leaves the Device (egress audit)
  - A Child in the Room: Egress, Consent, and the COPPA-Shaped Line
  - The Ship or No-Ship Decision, Written Down
  - Where Certification Takes Over: the Honest Edge of a Teaching Kit

::: {.callout-lab title="Lab 12: The Ship / No-Ship Gate"}
**Does:** run the two-number gate, recovery time to a safe state, and an egress
audit of everything that crossed the device boundary in an hour.
**Makes visible:** a byte counter on what actually leaves the board.
**Kit / Hero:** UNO Q gate; the hero's egress measured with a child's words as the
worked example.
**Break it:** inject a mid-loop failure and measure the true time to safe state.
**Links out to:** lab repo (TBD).
:::

### Chapter 13. The Human Loop

- **Premise:** the slowest loop, and the one that owns the robot. It is taught by,
  and lives with, a specific person.
- **Outcome:** O6, O4. **Property:** adaptivity, privacy, safety.
- **Sections:**
  - The Robot Lives With Someone: the Supervisory Relationship
  - Teaching: How a Person Adds a Skill or a Memory
  - The Approval Gate: Nothing New Without an Adult's Yes
  - Consent and the Boundary: What the Family Agreed To
  - Inspect, Edit, Forget: the Human's Control Over Memory
  - The Engagement Loop Is the Data Loop: Corrections as Labels
  - Does the Turn Pay? Weighing Improvement Against Its Cost
  - When the Servers Go Dark: Graceful Degradation, Portability, and the Robot's Mortality

::: {.callout-lab title="Lab 13: Teach, Approve, Forget"}
**Does:** build the approval-and-teaching flow, then feed one correction into the
improvement loop.
**Makes visible:** a pending skill waiting for approval, and the correction becoming
a training example.
**Kit / Hero:** UNO Q approval flow; Maya teaches Reachy a gated, forgettable skill.
**Break it:** pull the cloud and confirm the robot still does something safe and
useful offline.
**Links out to:** lab repo (TBD).
:::

---

## Part VI. Capstone

### Chapter 14. Defend the Whole System

- **Premise:** not "did it work," but "can you say why every part of it lives where
  it lives, and what it cost."
- **Outcome:** all six, as first-class deliverables (fixing the placement-swallows-
  everything risk), plus the diagnosis thread.
- **Sections:**
  - The Deliverable: a Working Loop, a Filled Map, a Binding Constraint per Placement, One Re-placement
  - Plus Three Gated Artifacts: the Runtime Design Defense (O2), the Ship/No-Ship Gate (O5), the Teach/Approve/Forget Flow (O6)
  - The Diagnosis: One Failure Found and Explained
  - The Bar: a Defended Failure Beats an Undefended Success
  - The Discipline, In Your Hands

::: {.callout-lab title="Capstone: Defend Your Loop"}
**Does:** the integrative build and defense, on the kit and/or the hero.
**Makes visible:** the whole discipline, in one system the student can account for.
**Break it:** the diagnosis is required, not optional.
**Links out to:** capstone brief (TBD).
:::

---

## Appendices

### Appendix A. The Closed-Loop Measurement Protocol

The instrument, and the moat. The measured loop properties (tail latency, joules per
decision, egress bytes per hour, time-to-safe-state, drift), the two-tier method
(deterministic replay *benchmark* + honest closed-loop *characterization*), the
per-property measurement recipes, and the reporting format the capstone defends.
Vendor-neutral by design so it spans a $59 board to a datacenter. This is what
turns "the loop prices time" from a sentence into a science, and it deserves to
ship as runnable, versioned software, not stay prose.

### Appendix B. The UNO Q Kit

The platform. The MPU and the MCU, the bridge between them, how placement-by-chip
works, the propose/dispose demo, and lab bring-up. The board is where the price of
time becomes physical.

### Appendix C. The Hero and the Home

Reachy's role, and its honesty. It realizes the full experience *and* serves as the
"no-enforcer" case study: a single-brain robot with no independent dispose channel,
shipping into a child's room, which teaches the cost of *not* having the boundary
the kit makes explicit. And Maya, the ground-floor context that makes safety,
privacy, and consent concrete, never a lab dependency.

---

## Other Ideas and Thoughts (Yours to React To)

- **A "Chapter 0 / Quickstart" is worth considering,** separate from Ch1, that is
  pure recruit-hook: close your first loop in an hour, no theory. The panel was
  emphatic that the wow must come before the discipline. Lab 1 half does this; a
  named quickstart would do it fully and protect the on-ramp that made TinyML a
  movement.
- **Appendix A may not want to be an appendix.** It is the moat and the field-
  founding artifact (the "MLPerf Tiny" of this book). Consider promoting the
  *concept* into the body (it is already seeded in Ch2 and consolidated in Ch10)
  and keeping the appendix as the reference spec.
- **The freshness bound should recur as a visible motif,** one short callback per
  chapter ("here is the price this chapter pays"). It is what keeps fourteen
  chapters feeling like one argument instead of a tour.
- **Every lab is filmable on purpose.** A reddening light, a byte counter ticking,
  an arm clamped mid-swing, the MCU saying no. That is "show your build" fuel, and
  it is how a kit spreads. Keep the visible-property law strict.
- **Positioning line for Ch1:** name the neighbors explicitly and place yourself
  *below* the capability layer. "After you have trained a policy (LeRobot) or bought
  the brain (Nvidia), this is how you engineer, measure, and trust the loop it runs
  in." Complementary, not competing.

## Open Decisions

1. **Chapter 0 quickstart**: separate recruit-hook chapter, or leave it as Lab 1?
2. **Promote Appendix A into the body** as a full chapter, given it is the moat?
3. **Ch2 load**: is "the fundamental + the nine properties + the measurement stance"
   one chapter or two? It is the densest chapter in the book.
4. **World Model and Perception** as two chapters (Ch4, Ch5) or one "Grounding"
   chapter?
5. **Name on the cover**: "Physical AI Engineering: The Discipline of Closed-Loop
   AI," or lead with "Closed-Loop AI" and let "physical AI engineering" be the
   descriptor?
