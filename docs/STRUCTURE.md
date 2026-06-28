# Physical AI Engineering: how the book and labs are structured

This is the meta-design: how the material is organized so it reads as a
*discipline*, not a kit walkthrough. It refines the chapter content in
`COURSE.md` (which stays the per-chapter source). Pressure-tested with two
adversarial review passes (Gemini 3.1 Pro, 2026-06-27); the provenance note at
the end records what was adopted and what was deliberately rejected, and why.

---

## 1. The discipline, in one paragraph

A physical AI system runs a closed loop: it senses, decides, acts, and the act
changes what it senses next. From that follow nine cross-cutting **properties**
every such system must satisfy (timeliness, reliability, safety, memory/state,
energy, privacy, robustness, adaptivity, observability). The recurring
engineering skill is **placement**: for each capability, decide which *loop* it
belongs in (reflex ~ms / deliberation ~1s / learning ~days) and which *box* it
runs in (device / edge / cloud), then defend the choice with measured numbers.
The properties are the vocabulary; placement is the verb; "constraints drive
architecture" is the law. That is the whole subject, and everything below exists
to make it teachable and felt.

The two things that make this a discipline rather than a tour are both
structural: **placement is taught first and applied in every chapter** (not
deferred), and **every claim is a prediction the reader then measures and
reconciles** (not a fact they are told).

---

## 2. The narrative spine: one robot grows up

The book has a protagonist. One robot gains exactly **one capability per
chapter** (it looks, then routes fast vs. slow, then understands, then moves
safely, then remembers, then improves). The reader watches it become more
capable as their own understanding deepens. The robot is "just a robot" to the
reader: the story does not depend on which hardware it runs on.

Division of labor, kept strict, because conflating them is what makes a lab feel
like a chore:

- **The robot is the WHY.** It carries the narrative and the stakes through
  short scenes and photos: a head that turns a half-second too late, a glass it
  almost knocks over, the moment it finally recognizes a child. Physical AI's
  implications are physical and visible, and *none of them fit in a log file*.
  This is what a lab cannot do, and it is the engagement engine.
- **The kit is the HOW.** The reader reproduces a slice on the Arduino UNO Q and
  earns the number behind the scene. The lab is always **downstream of a scene
  the reader already cares about**, so it never arrives as a cold exercise.

Three reader tiers, so the book serves everyone:

1. **Read-only** gets the complete narrative through the robot scenes. Nothing
   is missing.
2. **Kit builder** reproduces a slice on the UNO Q and earns the measurements.
3. **Full-robot builder** (the author's own path) is the aspiration at the top.

---

## 3. The placement method (the discipline's core tool)

Placement is a repeatable method with a concrete artifact, not a category label.
For each capability the reader fills a **Placement Map**: a double-column budget
table that forces an honest comparison between the kit they own and the hero
robot they are reading about.

| Property budget | My Kit (UNO Q) | The Hero (Reachy / production robot) |
|---|---|---|
| Latency vs. deadline | estimate, then measured | scaled-up estimate |
| Memory vs. limit | … | … |
| Energy vs. budget | … | … |
| Bandwidth vs. link | … | … |
| Accuracy vs. target | … | … |
| **Binding constraint** | name the one that decides it | name it |
| **Placement (loop × box)** | reflex/delib/learn × device/edge/cloud | … |

Two things make this rigorous rather than hand-wavy:

- **The reader names the *binding* constraint** for each capability (the one
  property that actually decides the placement) and justifies the choice against
  it. A defended placement is one where you can say which number forced your
  hand.
- **The double column anchors the narrative robot in math.** The reader does the
  same budget analysis for the hero they cannot run as for the kit they can. The
  hero is present as a quantitative reference design, not flavor text, and the
  "you can't reproduce the hero" objection dissolves because the hero was never
  a lab target, only an analysis target.

Each chapter supplies a small **"iron law"**, a napkin-math formula the reader
predicts with, so *Predict* is calculation and not a guess (see the chapter
table). This is the same quantitative-reasoning move as the Iron Law in the
author's ML Systems book.

---

## 4. Two brains on one board

The reproducible "two machines, one decision" comparison runs on the UNO Q's
*own* two brains, so the reader needs only the one board they own:

- **Dragonwing Linux SoC** = the deliberation box (heavier models via
  ExecuTorch, ~1s reasoning).
- **STM32 MCU** = the reflex box (hard real-time, ~ms).
- They talk over a **shared-memory ring buffer / IPC pattern built once in
  Foundations** and reused in every later lab, so the reader treats the two
  processors as one coordinated system from day one rather than two boards
  stuck together late in the book.

The CM4 Reachy stays the **narrative hero only**: it appears in scenes and as the
"hero" column of the Placement Map. The reader never runs lab code on it.

---

## 5. The signature tension: AI choices change physical outcomes

The thing that separates this from "embedded programming with a model bolted on"
is that **model decisions are control decisions.** Quantizing a perception model
from FP32 to INT8 to fit the bandwidth budget can degrade its accuracy enough to
violate a safety envelope; inference jitter can destabilize a control loop. The
book teaches this coupling on purpose: the reader makes an AI optimization, then
*measures the physical consequence*. This runs explicitly through the
action/control chapter and the capstone, and it is what makes the discipline
physical.

A failure-analysis thread (watchdogs, a defined fallback when the model returns
garbage, graceful degradation) runs through control and deployment, because in a
body a wrong prediction moves something.

---

## 6. The per-chapter rhythm

A rhythm, not a rigid checklist. Beats compress; the Crux merges the property in
tension with the placement decision.

1. **Question** (the styled box that opens the chapter).
2. **Scene** (the robot, a photo, the stakes you can see).
3. **Crux** (the property in tension + the placement decision it forces).
4. **Predict** (estimate the placement with the chapter's iron law).
5. **Build** (reproduce the scene on the UNO Q).
6. **Measure** (the real number).
7. **Reconcile** (why reality differed from the estimate; revise the map).
8. **Read** (literature anchors for engineers).

`Predict -> Build -> Measure -> Reconcile` is the engineering loop that makes the
lab rigorous and keeps it from being a cold exercise: the lab tests *the reader's
own prediction*.

---

## 7. The sequence

Placement is taught up front and applied throughout; chapter 7 becomes the
whole-system synthesis rather than the first time placement appears.

| # | Chapter | Property foregrounded | Chapter "iron law" (the Predict tool) | Lab core |
|---|---|---|---|---|
| F1 | The Discipline | the closed loop + all nine | — (framing) | time a trivial sense→act loop |
| F2 | The Elements | observability + the budgets | the budget identity (fits a box iff latency ≤ deadline AND memory ≤ limit AND energy ≤ budget AND bandwidth ≤ link) | **build the dual-brain telemetry + IPC harness** every later lab plugs into |
| 0 | From TinyML to Physical AI | timeliness | loop latency = sense + infer + act + actuate; period < dynamics timescale | close an open-loop classifier, measure loop latency |
| 1 | Perception on the edge | timeliness · energy · robustness | sensor-bus bandwidth = resolution × framerate × bitdepth | localize sound / frame a camera; halve the window, watch robustness fall |
| 2 | The two-speed brain | reflex vs. deliberation | escalation budget: fraction escalated × deliberation latency ≤ response deadline; reflex period < control period | cheap reflex + escalate-on-uncertainty; measure escalation rate + latency saved |
| 3 | Pixels to meaning (VLM/VLA) | capability · privacy · cost | T_cloud = T_upload + T_infer + T_download vs. T_local; privacy cost = bytes leaving the device | small detector on the NPU (ExecuTorch) vs. cloud VLM; predict both, defend the placement |
| 4 | Action and control | safety · reliability · timeliness | control deadline + jitter budget; **quantization → accuracy → safety-envelope coupling** | servo + safety envelope; then quantize/jitter the perception model and measure how control degrades |
| 5 | Memory and state | memory/state · privacy | state growth vs. storage; recall latency | remember a preference on-device; measure recall + privacy cost of moving it off |
| 6 | The data flywheel | adaptivity · observability | improvement-per-round vs. round-trip cost; data yield = fraction kept | log → curate → adapt off-device → redeploy; measure improvement + round-trip cost |
| 7 | Placement and systems | all, in tension | the whole-system map | synthesize and defend the full double-column Placement Map; re-place one capability, measure the system effect |
| 8 | Safety, privacy, deployment | safety · privacy · reliability · robustness | failure-recovery time; data-egress audit (bytes leaving) | deployment checklist, failure-modes pass, privacy audit, ship/no-ship |
| — | Capstone | the discipline, demonstrated | — | full loop + a defended Placement Map with measured numbers + a written defense |

The order intentionally teaches the **MCU↔SoC boundary (ch.2) before
distributing a big model across it (ch.3)**. The F2 harness makes the boundary a
day-one primitive, so the dependency holds either way.

---

## 8. First-class concerns (not afterthoughts)

- **Observability** is built first (the F2 harness) and reused, so debugging a
  closed loop is a taught skill, not an aside.
- **Data movement** is a named, measured cost (sensor bus + on/off-device
  transfer), echoing the "energy of moving a bit" thesis from the ML Systems
  book.
- **Failure analysis** runs through control and deployment.
- **Compiler/scheduler performance signatures** (what ExecuTorch quantization
  costs in memory/accuracy; how the RTOS schedules the model thread vs. the
  safety reflex) enter as *inputs to the budget*, taught at the signature level,
  not as compiler internals.

---

## 9. Cadence and ownership

- **Serial release**: one chapter + its lab per drop, cumulative (the robot and
  the Placement Map both grow). Foundations + early chapters run in sim / any
  board, so they ship before the kit is in hand; hardware-heavy chapters align
  with kit availability.
- **Two tracks**: the *concept* (properties + placement method, platform-neutral)
  is the durable asset the author owns and that courses adopt; the *lab* (UNO Q,
  ExecuTorch) is co-branded and swappable as hardware evolves. Keep it "the
  Physical AI Engineering book that uses the UNO Q for labs," never "the UNO Q
  book."

---

## 10. Open decisions for the author

1. **Primary audience.** Serious learner / early-career engineer (rigor) vs.
   maker (kit). Recommendation: design for the engineer, let makers ride along.
2. **How hard to push the math.** The iron-law-per-chapter approach is the floor;
   decide whether advanced "rigor boxes" (e.g., a formal placement optimization)
   appear as optional depth.
3. **What ships per drop.** Chapter + lab + the running Placement-Map increment,
   or chapter + lab with the map as a capstone artifact only.
4. **The land-grab.** Is owning the *framework* (the properties + the placement
   method) the explicit goal, or is the book a means to the kit? This sets how
   hard to push the concept track.

---

## Provenance: the pressure-test

Drafted, then critiqued adversarially twice by Gemini 3.1 Pro (2026-06-27),
treated as a skeptical textbook editor.

**Adopted** (the critique was right): placement taught early as the spine; a
repeatable placement *method* with a concrete artifact; the
Predict→Build→Measure→Reconcile lab loop; the two-brain comparison on the UNO Q's
own SoC+MCU; a napkin-math iron law per chapter; the double-column (kit vs. hero)
Placement Map; the AI↔control coupling as the signature tension; the dual-brain
harness built in Foundations; observability / data-movement / failure as
first-class; compiler/scheduler performance signatures as budget inputs.

**Rejected** (would have gutted the vision): cutting the narrative Scene and the
capability arc (the engagement engine; the critic's bias toward an advanced-EE
audience); eliminating the Reachy hero (kept as narrative + the hero column of
the Placement Map); reordering to a hardware-layer-first sequence and adding
control-theory math (a narrower, different book). The second review confirmed
these rejections were correct and that the result did not overcorrect into a dry
embedded-systems text.
