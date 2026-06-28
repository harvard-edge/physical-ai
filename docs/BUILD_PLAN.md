# Build plan and design method

How we actually build this book. The premise: physical AI is an engineering
discipline, and a discipline is taught by having the reader make and defend
decisions under constraint, not by listing facts.

## What it means to teach an engineering discipline

- A topic teaches *what* (facts about sensors, VLMs). A tool teaches *how* (use
  this SDK). A discipline teaches *judgment under constraint*: how to make a
  defensible design decision when you cannot have everything.
- Engineering produces a defensible artifact under constraints you did not
  choose. The deliverable of the discipline is the **justified decision**, not
  the working artifact.
- So the unit of every chapter is a **decision the reader makes and defends** (a
  placement), backed by a **measurement**. The reader should leave able to face a
  new physical AI problem and reason: name the properties in tension, choose a
  placement, measure it, defend it.

## Designing for "some parts might not work"

Because the deliverable is the justified decision, a build that fails but is
measured and explained still teaches the discipline. A well-instrumented failure
is a successful exercise. We are not betting the pedagogy on every build
reproducing.

Two layers per chapter:

- **Durable core** (hardware-agnostic): the property tension, the decision, the
  measurement method, and the defense. This is what the chapter teaches.
- **Fragile shell** (one instantiation): the specific kit build (this board,
  this model, this code). Swappable; it can break without taking the lesson.

Write the durable core first; instantiate the shell second.

### The fallback ladder (every exercise has a floor)

Pick the highest rung that reproduces and teaches; name the rung below as the
fallback.

1. **Live build** on the kit (best: the reader feels the constraint).
2. **Provided data + notebook** (we captured the run; the reader analyzes and decides).
3. **Worked example** (we make the decision in front of them, with numbers).
4. **Thought experiment** (reason it out, no apparatus).

Prototype every live build before writing it as an exercise. If it does not
reproduce or does not teach the trade, drop it a rung.

## The diagrams are the discipline's thinking tools

Not decoration. A small recurring set the reader learns to *draw* for a new
problem. Each chapter instantiates one or two.

| Diagram | What it makes visible | Instantiated in |
|---|---|---|
| **Loop schematic** | where a component sits in sense -> decide -> act | The Discipline, each part opener |
| **Tradeoff knee** | a property bought at the cost of another (the margin) | Perception, Pixels to Meaning |
| **Placement map** | capability x {reflex/deliberation/learning} x {device/server/cloud}, each cell's property cost | Cognition, Placement, Capstone |
| **Property budget** | how one design spends the nine elements (cannot max all) | The Elements, Placement |
| **Latency budget bar** | where the milliseconds go (sense, infer, act) | The Loop, Action |
| **Flywheel cycle** | collect -> curate -> train -> deploy | Data flywheel |

The signature is the **placement map**: the book's whole argument is one drawing
the reader fills in for their own system.

## Per-chapter design sheets

Each sheet: the one Claim, the property Tension, the Decision the reader defends,
the Diagram, the Build with its Risk and Fallback rung, and the Measure.

### The Discipline
- **Claim**: physical AI is defined by world-coupling in a closed loop; the deliverable is a justified placement.
- **Tension**: introduces all nine elements.
- **Decision**: none yet; list what is hard about a coupled task before any model is named.
- **Diagram**: loop schematic.
- **Build / risk / fallback**: thought experiment (rung 4), no apparatus, cannot fail.
- **Measure**: qualitative (the list of what is hard is the lesson).

### The Elements
- **Claim**: nine cross-cutting properties; no system maxes all.
- **Tension**: the set, against each other.
- **Decision**: name the three irreducible elements for a first build.
- **Diagram**: property budget.
- **Build / risk / fallback**: fill the empty elements table for one device (rung 3); fallback thought experiment.
- **Measure**: qualitative ranking, defended.

### Ch 0 — The Loop
- **Claim**: closing the loop creates timeliness, reliability, and safety.
- **Tension**: timeliness vs reliability vs safety.
- **Decision**: pick a control-loop rate and defend it.
- **Diagram**: loop schematic + latency budget bar.
- **Build / risk / fallback**: a reflex (turn toward a sound) on the device. Risk: mic direction over the remote link is unreliable (we hit this). Fallback: run on the robot, or provided audio analyzed offline (rung 2).
- **Measure**: end-to-end loop latency.

### Ch 1 — Perception on the edge
- **Claim**: on-device perception trades accuracy for latency and energy.
- **Tension**: timeliness, energy, robustness vs accuracy.
- **Decision**: choose a model size and quantization; defend the operating point.
- **Diagram**: tradeoff knee.
- **Build / risk / fallback**: run one detector at three operating points (cloud, laptop, device). Risk: device too slow or install friction. Fallback: provided benchmark CSV + notebook (rung 2).
- **Measure**: accuracy, inferences/sec, milliwatts at each point.

### Ch 2 — Pixels to meaning
- **Claim**: meaning is expensive; who decides (device vs cloud) is a property trade.
- **Tension**: capability vs timeliness, cost, privacy; observability via the grounding gap.
- **Decision**: place the VLM (tiny on-device vs cloud) for a task; defend.
- **Diagram**: placement map for "describe the scene" + tradeoff knee.
- **Build / risk / fallback**: same image to a tiny local VLM vs a cloud VLM. Risk: on-device VLM too heavy on the CM4 (true). Fallback: cloud-only plus provided local-VLM latency numbers (rung 2/3).
- **Measure**: latency and cost, local vs cloud.

### Ch 3 — Cognition and agency
- **Claim**: a two-speed brain escalates only when needed.
- **Tension**: timeliness, cost vs capability; observability.
- **Decision**: set the reflex/deliberation boundary; defend the escalation policy.
- **Diagram**: placement map + fast/slow loop schematic.
- **Build / risk / fallback**: MCU reflex + cloud LLM over MCP; count escalations. Risk: install + connectivity. Fallback: analyze a provided conversation log (rung 2).
- **Measure**: fraction handled locally, latency per path.

### Ch 4 — Action and control
- **Claim**: decisions become safe motion under real-time and safety budgets.
- **Tension**: timeliness, safety, reliability.
- **Decision**: pick a control rate and a safety envelope; defend.
- **Diagram**: latency budget bar + loop schematic with a safety interlock.
- **Build / risk / fallback**: smooth vs naive gesture, plus a safe-stop. Risk: needs the hardware. Fallback: simulate the trajectory and plot jitter (rung 2/3).
- **Measure**: jitter, overshoot, time to safe stop.

### Ch 5 — Memory and state
- **Claim**: persistence is a property and a component; structured memory is inspectable.
- **Tension**: memory and state vs privacy; storage, robustness.
- **Decision**: what to keep vs forget; structured graph vs vector store.
- **Diagram**: the knowledge graph growing + property budget.
- **Build / risk / fallback**: teach-it-and-remember (knowledge graph). Risk: low. Fallback: provided graph + recall test (rung 2).
- **Measure**: recall accuracy over time, state growth.

### Ch 6 — The data flywheel
- **Claim**: the system improves from its own curated experience; the engagement loop is the data loop.
- **Tension**: adaptivity vs privacy; data quality vs quantity; observability.
- **Decision**: what to log and curate (active learning); defend the privacy posture.
- **Diagram**: flywheel cycle.
- **Build / risk / fallback**: episode logger + interestingness curator. Risk: training is off-device and improvement may not show within a session. Fallback: provided logged episodes + an offline retrain delta, or a worked example (rung 2/3).
- **Measure**: data yield, fraction kept, improvement delta after a retrain.

### Ch 7 — Placement and systems
- **Claim**: placement is the discipline's core decision; it trades all the properties at once.
- **Tension**: all nine.
- **Decision**: place every capability of one real system; defend with numbers.
- **Diagram**: the full placement map (signature) + property budget.
- **Build / risk / fallback**: instrument the whole robot and fill the placement map. Risk: integration effort. Fallback: provided measurements to fill the map (rung 2).
- **Measure**: latency, energy, privacy per placement.

### Ch 8 — Safety, privacy, deployment
- **Claim**: a home deployment is a reliability, safety, and privacy problem, head-on.
- **Tension**: reliability, safety, privacy.
- **Decision**: design the privacy gate and the fail-safe; defend the data-egress posture.
- **Diagram**: data-egress diagram (what leaves the device) + loop with a safety interlock.
- **Build / risk / fallback**: privacy-gated capture + watchdog + a data-egress audit. Risk: failure is hard to test safely. Fallback: a tabletop failure-mode analysis (rung 3/4).
- **Measure**: recovery time, and a data-egress audit (what actually leaves the device).

### Capstone
- **Claim**: the whole loop, placed and defended.
- **Decision**: present a complete system with its placement map and property budget, and defend the trades.
- **Diagram**: the reader's own placement map.
- **Build / risk / fallback**: the full system, or a chosen embodiment. Risk: scope. Fallback: present the map and measurements for a partial build (rung 2).
- **Measure**: the system's property budget, defended.

## Build order

1. Lock the recurring diagrams (draw the placement map and the tradeoff knee as
   reusable templates) since every chapter reuses them.
2. Prototype the high-risk builds early (Ch 0 reflex, Ch 2 on-device VLM, Ch 6
   flywheel) to learn which rung each exercise actually lands on.
3. Write durable cores first across all chapters; instantiate shells as the
   prototypes come back.
