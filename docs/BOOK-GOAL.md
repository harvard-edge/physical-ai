# Physical AI Book Goal

**Working title:** *Physical AI: Machine Learning Systems That Sense and Act*
**Status:** canonical source of truth for backward design and authoring
**Audience:** serious learners, early-career engineers, and practicing ML systems engineers entering physical AI

---

## The Goal

This book should teach a reader how to turn a learned capability into a physical
system that can be trusted to keep operating while the world changes around it.
The model is important, but it is never the whole system. The engineering work
begins when an observation becomes a belief, a belief becomes a proposal, a
proposal is checked against physical limits, and an allowed action changes the
world that will produce the next observation.

The finished book should enable a reader to take an unfamiliar task, model,
embodiment, and computing platform and produce a defensible physical-AI system.
The reader should be able to:

1. define the system boundary and show how action closes the causal loop;
2. derive deadlines and operating requirements from the dynamics and
   consequences of the world;
3. measure the running loop with valid operational definitions, distributions,
   uncertainty, and task-efficacy floors;
4. design a continuous, multi-rate runtime that continues to meet its timing,
   state, action, and authority requirements when a learned component is late,
   wrong, or unavailable;
5. turn sensor observations into a time-indexed, uncertainty-aware belief about
   the world and the system itself;
6. treat VLMs, VLAs, and future learned policies as measurable proposal
   interfaces rather than unquestioned sources of physical authority;
7. translate intent into skills with explicit limits and check proposed actions
   through a path that does not depend on the learned component;
8. place sensing, estimation, policy, enforcement, logging, and learning across
   heterogeneous compute under shared latency, energy, memory, bandwidth,
   privacy, and failure-domain constraints;
9. construct an evidence ladder and decide when a candidate may advance from
   offline evaluation toward consequential operation;
10. allocate meaningful human authority to teach, approve, inspect, interrupt,
    revoke, retain, and forget;
11. govern interaction data and system updates through consent, lineage,
    coverage analysis, evaluation, versioning, and rollback; and
12. make and defend a decision to deploy, deploy under explicit conditions, or
    refuse deployment, with every claim supported by evidence.

The final test is transfer. A graduate should be able to apply this method to an
embodiment and model family that never appears in the book. Successful assembly
of the reference lab is not sufficient.

---

## Target Audience & Ecosystem Audit: Broad Physical AI vs. Physical AI Systems

### 1. Distinguishing Broad Physical AI from Physical AI Systems

A crucial positioning principle of this book is distinguishing **Broad Physical AI** (the general concept) from **Physical AI Systems** (our explicit engineering specialization):

*   **Broad Physical AI (The Conceptual Field):** Encompasses generative AI on robots, text-to-video manipulation, synthetic data generation in simulation, general humanoid demonstrations, and end-to-end foundation model research. While valuable context, broad physical AI often treats physical execution as a black box or downstream simulation detail.
*   **Physical AI Systems (Our Core Specialization):** Focuses specifically on the **systems engineering discipline** required to build, measure, constrain, place, govern, and qualify learned components acting back into the physical world. It answers how multi-rate runtimes, proposal-permission dual-brain architectures, $P_{99}$ latency tail distributions, microsecond PTP clock synchronization, zero-copy DMA memory paths, STPA hazard controls, and Claim-Argument-Evidence (CAE) release cases guarantee physical safety and operational dependability.

---

### 2. The 3 Primary Target Reader & Reviewer Personas

This textbook is engineered to serve, be reviewed by, and be adopted across three distinct technical communities:

```text
                        THE 3 CORE TARGET AUDIENCES
 ┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐
 │ PERSONA 1: EMBEDDED ML │ │ PERSONA 2: ROBOTICS/CPS│ │ PERSONA 3: EMBODIED AI │
 │ & EDGE SYSTEMS (TINYML)│ │ & CONTROL ENGINEERS    │ │ & VLM/VLA RESEARCHERS  │
 ├────────────────────────┤ ├────────────────────────┤ ├────────────────────────┤
 │ • Transitioning from   │ │ • Integrating non-     │ │ • Moving from open-    │
 │   passive edge model   │   deterministic learned│   loop benchmark accuracy│
 │   inference (TinyML) to│   models into real-    │   to closed-loop spatial  │
 │   active dual-brain    │   time safety-critical │   belief, hardware buses,│
 │   physical runtimes.   │   control loops safely.│   and data flywheels.    │
 └────────────────────────┘ └────────────────────────┘ └────────────────────────┘
```

#### Persona 1: Embedded ML & Edge Systems Engineers (The TinyML & Silicon Community)
*   **Background:** Embedded systems developers, TinyML practitioners, computer architects, and mobile edge engineers.
*   **Core Pain Points:** Transitioning from passive edge inference (keyword spotting, anomaly detection, image classification) to active physical actuation without overwhelming SRAM/DRAM, DMA memory channels, or thermal TDP.
*   **Why This Book Spans Their Needs:** Demonstrates that the microcontroller (MCU) is not obsolete, but rather serves as the **System 1 Spinal Reflex Arc**—the zero-allocation, deterministic guardian holding physical permission while application processors (SoCs) run heavy AI workloads.

#### Persona 2: Robotics & Cyber-Physical Systems (CPS) Engineers (The Controls & Safety Community)
*   **Background:** Classical roboticists, mechatronics leads, autonomous vehicle engineers, ROS2 developers, and functional safety engineers.
*   **Core Pain Points:** Deep skepticism of un-shielded, non-deterministic neural network proposals driving physical actuators without real-time safety guarantees or dynamic stopping bounds.
*   **Why This Book Spans Their Needs:** Establishes rigorous system controls: independent MCU safety enforcers, dynamic stopping distance bounds ($d_{\text{stop}}$), Category 0/1/2 physical fallbacks, STPA hazard analysis (ISO 21448 / SOTIF), and Claim-Argument-Evidence (CAE/GSN) release cases.

#### Persona 3: Embodied AI & ML Systems Researchers (The VLM / VLA / Foundation Model Community)
*   **Background:** Deep learning researchers, PyTorch developers, Vision-Language-Action (VLA) architects, and multimodal foundation model deployment leads.
*   **Core Pain Points:** Understanding how open-ended VLM/VLA models execute on physical hardware beyond static simulation benchmarks, managing multi-step action chunking ($H$), and addressing policy endogeneity/selection bias.
*   **Why This Book Spans Their Needs:** Delivers the complete physical wrapper: 3D spatial affordance tokenization, expiring intent proposals ($t_{\text{expire}}$), $\mathcal{C}^2$ temporal ensembling, microsecond PTP trajectory logging, and governed data flywheels.

---

### 3. Reviewer & Educator Buy-In Strategy

By explicitly structuring the manuscript around these three personas, the textbook achieves strong peer-review validation and university adoption:
1.  **Robotics/CPS Peer Reviewers** validate the real-time safety rigor (Chapters 4, 7, 10).
2.  **Embedded/Silicon Peer Reviewers** validate the microarchitecture and interconnect bus budgets (Chapters 2, 3, 8).
3.  **Embodied AI Peer Reviewers** validate the generative AI proposal interfaces and dataset governance (Chapters 5, 6, 9).

---

## Why the Book Exists

Machine learning systems usually end at a digital output. Physical-AI systems do
not. Their outputs consume time, move matter, spend energy, affect people, remove
future options, and alter the distribution of observations that follows. A
system can therefore contain an excellent model and still fail because its
belief is stale, its runtime misses a deadline, its action representation does
not match the body, its fallback shares the same failure domain, or nobody has
meaningful authority to stop or revise it.

Robotics, control, embedded systems, human-computer interaction, safety
engineering, and machine learning already contain much of the necessary
knowledge. The contribution of this book is not to rename those fields or claim
their results. It is to assemble the parts into a teachable machine learning
systems discipline for learned components that sense and act in the real world.

The durable question is not which model is currently strongest. The book asks:

> What must the surrounding system know, measure, enforce, preserve, and prove
> before a learned proposal may produce a physical consequence?

---

## What the Book Is

The book combines the rigor of a textbook with the immediacy of an engineering
field guide. It teaches concepts, quantitative tools, and design judgment before
asking the reader to build. Its labs are an executable companion to the
pedagogy, not a substitute for it.

The manuscript has four simultaneous identities:

- **A continuation of machine learning systems.** The reader begins with models,
  data, runtimes, deployment, and evaluation, then follows what changes when the
  output acts back into the world.
- **A systems curriculum.** Every chapter ends with a decision that changes one
  accumulating system design.
- **An evidence discipline.** Claims about latency, confidence, safety, privacy,
  or readiness are tied to an operational definition and an explicit regime.
- **A laboratory-backed book.** Every concept can later be manifested through an
  analytical exercise, a hosted artifact, and a reproducible physical build.

It should remain useful when the named model families, boards, accelerators, and
software stacks have changed.

---

## What the Book Is Not

The book is not a compressed robotics curriculum. It borrows frames, estimation,
dynamics, and control only to the depth required for a physical-AI engineering
decision.

It is not a VLM or VLA catalog. Contemporary models appear as contrasting case
studies of policy interfaces, action representations, temporal context,
embodiment assumptions, latency, uncertainty, and failure behavior.

It is not a hardware manual. A board or robot realizes the mechanisms, but the
chapter remains complete for a reader who never owns the hardware.

It is not a sequence of successful demonstrations. Every substantive exercise
contains a prediction, perturbation, measurement, diagnosed failure, and written
decision.

It is not a claim that physical AI, feedback, runtime assurance, state
estimation, limits on action, or human oversight were invented here. Originality
comes from the integration, pedagogy, and cumulative evidence structure.

---

## The Backward-Designed Spine

The chapters add one capability at a time to the same system:

> **Frame → specify → measure → architect → observe → estimate → propose →
> enforce → place → qualify → authorize → change → deploy**

| **Chapter** | **Capability** | **Decision** | **Artifact Added** |
|---:|---|---|---|
| 1 | Frame | Choose the causal boundary | Loop charter |
| 2 | Specify | Choose a defensible operating regime | Requirements and assumptions ledger |
| 3 | Measure | Accept, reject, or narrow a claim | Measurement plan and evidence record |
| 4 | Architect | Choose services, cadences, ownership, and failure behavior | Continuous runtime skeleton |
| 5 | Observe | Choose the sensing strategy and operating point | Observation contract |
| 6 | Estimate | Choose state, frames, clocks, uncertainty, and correction | State and timing model |
| 7 | Propose | Choose the policy interface, action representation, and escalation behavior | Intent contract |
| 8 | Enforce | Choose skill limits, action checks, and trusted enforcement | Enforcement design |
| 9 | Place | Choose the whole-system placement under shared budgets | Placement map and resource ledger |
| 10 | Qualify | Promote, hold, or reject the candidate | Assurance plan and promotion record |
| 11 | Authorize | Allocate and limit human authority | Authority map |
| 12 | Change | Admit or reject experience and updates | Governed data and update record |
| 13 | Deploy | Deploy, deploy under explicit conditions, or refuse | Integrated deployment case |

The unnumbered final design review introduces no new subject matter. It asks the
reader to defend the complete system, diagnose a deliberately introduced
failure, and adapt the method to an unfamiliar embodiment.

---

## The Cumulative Design Dossier

The learner should not complete thirteen unrelated chapter assignments. Each
chapter modifies a versioned dossier for one evolving system. At any point, the
dossier records:

- the task, world, affected people, causal boundary, and feedback path;
- world timescales, freshness limits, efficacy floors, physical consequences,
  budgets, and operating assumptions;
- operational definitions, instrumentation, distributions, uncertainty, and
  rejected claims;
- runtime services, state ownership, event contracts, cadences, deadlines,
  overload behavior, and recovery paths;
- observation, state, policy, intent, skill, and action contracts;
- frames, clocks, belief uncertainty, validity horizons, and drift triggers;
- placement, resource consumption, failure domains, trust boundaries, and data
  movement;
- scenario coverage, evidence tiers, promotion thresholds, and evidence gaps;
- human authority, consent scope, override paths, retention, revocation, and
  exit rights;
- trajectory provenance, data admissibility, update evaluation, versions, and
  rollback; and
- the deployment claim, explicit limits, residual risk, conditions, owners,
  monitoring, and release decision.

This dossier is the book's final integration artifact. The physical build
supplies evidence for it.

---

## Pedagogical Commitments

### Concepts Precede Their Manifestation

The chapter must teach the complete mental model, engineering representation,
and decision before the lab begins. A lab may make an invisible property visible
or expose a misconception through experience. It may not rescue an incomplete
explanation.

### Every Chapter Lands

A chapter is complete only when the reader can explain its central systems
problem, use its quantitative or representational tool, diagnose a relevant
failure, compare alternatives, make the chapter's engineering decision, update
the design dossier, and enter the next chapter without a hidden prerequisite.

### The Authoring Machinery Stays Off the Page

Backward design controls the chapter without becoming its visible template.
The reader normally sees a natural opening, one compact learning-objective
callout, chapter-specific sections, a decision callout that records the dossier
update, a transfer check embedded in the argument, and the lab as the final
element. Entering state, misconception, crux, concept ownership, dependencies,
and acceptance criteria remain in the authoring packet. Repeated curriculum
labels must not become manuscript headings.

### Name the Actual Decision

Reader-facing prose should name the action, limit, measurement, and responsible
component directly. Say what is checked, who decides, how old information may
be, or where the system may operate. Do not make a framework metaphor carry the
technical meaning. Introduce specialized terminology only after the plain idea
is clear and only when the term will be used again.

### Progressive Disclosure Follows Causal Need

The reader first experiences the consequence, then receives the minimum model
needed to explain it, then gains the tool needed to measure it or state its
limits, and only
then encounters a richer implementation. Later chapters reuse earlier tools
without reteaching them.

VLMs and VLAs arrive only after the reader understands deadlines, measurement,
runtime continuity, observation, and state. This order prevents model capability
from dictating the architecture.

### Models Remain Components

Model architecture and training appear only when they change a systems decision.
The book foregrounds model inputs, temporal context, action representation,
cadence, latency distribution, resource use, calibration, abstention, placement,
coverage, and failure behavior.

### Failure Is a Teaching Instrument

Every chapter includes a failure native to its concept. Diagnosis follows the
same reusable method:

> **Hypothesis → bisect → confirm**

A defended failure can demonstrate understanding. An unexplained success cannot.

### Depth Follows the Decision

Borrowed material is taught only as deeply as the chapter's engineering decision
requires. This prevents the manuscript from becoming a shallow survey at one
extreme or several compressed textbooks at the other.

---

## Laboratory Contract

Every end-of-chapter lab must include:

1. a visible phenomenon whose importance the learner already understands;
2. a prediction recorded before the outcome is known;
3. an operational definition with units and operating regime;
4. a controlled perturbation;
5. a negative control or meaningful alternative;
6. a defensible number with uncertainty and an efficacy floor where relevant;
7. a failure that exercises hypothesis, bisect, and confirm;
8. a chapter-specific engineering decision; and
9. an update to the cumulative design dossier.

Each lab objective should support three manifestations:

- **Analytical.** A trace, replay, dataset, calculation, simulation, or thought
  experiment preserves the complete reasoning without prescribed hardware.
- **Hosted.** An interactive application or reproducible artifact makes the
  evidence inspectable and shareable.
- **Physical.** A reproducible device makes timing, energy, sensing, enforcement,
  or consequence tangible.

The manifestations may use different machinery. They must assess the same
concept, evidence, and decision.

---

## The Visual Thesis

The figures should make the book recognizable without borrowing the visual
identity of another project. The transferable lesson from strong technical
figure systems is discipline. Each figure makes one claim, supports one decision,
uses a small repeated grammar, and is inspected in the rendered book. The shapes,
colors, figure families, and recurring visual argument must arise from physical
AI itself.

### The Canonical Physical-AI Plate

The book's recurring system figure should show two world states rather than a
generic circular arrow:

```text
World W(t) → Observe → Estimate → Propose ⇢ Enforce → Act → World W(t+1)
                 ↑          runtime state          ↑
                 └──── evidence and timing ────────┘

Human authority governs observation, proposal, enforcement, retention, and change.
```

The left and right world states make endogeneity explicit. Action does not return
to the same world. It produces the world from which the next observation will be
drawn. Each chapter reveals, measures, or constrains one portion of this plate.
Previously taught portions remain visible but visually subordinate.

### PhysicalAI Visual Grammar

- **World states are contextual fields.** They sit outside the system boundary
  and show time, consequence, and affected people or objects.
- **Observations and estimates are different shapes.** A measured observation is
  not visually interchangeable with a belief or prediction.
- **Learned outputs are proposals.** Proposal paths are dashed until the
  independent action check accepts them.
- **Allowed physical commands are solid.** A reader can distinguish model intent
  from actuator authority without reading the caption.
- **Refusals terminate visibly.** Rejected actions stop at the action check and
  enter the evidence record rather than disappearing.
- **Time has a direction.** Timing figures use explicit clocks, age, horizons,
  deadlines, and state versions.
- **Uncertainty occupies space.** Beliefs and operating limits use intervals,
  distributions, regions with explicit edges, or dashed containment rather than
  vague labels.
- **Human authority is a real path.** Approval, override, revocation, inspection,
  and forgetting connect to the components they govern.
- **Measurement changes decisions.** Quantitative figures visually emphasize the
  knee, tail, crossing, invalidation point, or binding limit that changes the
  engineering verdict.

### Semantic Color Roles

Color should communicate behavior, not decorate categories:

| **Role** | **Meaning** |
|---|---|
| Structural navy | Ordinary system structure, runtime, boundaries, and labels |
| Teal | Observed, measured, allowed, or locally enforced behavior |
| Amber | Learned proposal, prediction, deliberation, or unresolved uncertainty |
| Coral | Veto, violated limit, exposure, consequence, or rejected evidence |
| Violet | Human authority, approval, consent, revocation, or accountability |
| Neutral gray | World context, inactive paths, deferred work, and supporting detail |

An ordinary figure should use only the roles needed for its argument. Color is
always paired with shape, line style, label, or position.

### Figure Families

1. **World-coupling plates** show how an allowed action changes the next world
   state and observation.
2. **Timing plates** show observation age, inference latency, action horizons,
   action chunks, deadlines, jitter, and multi-rate runtime behavior.
3. **Belief plates** separate observation, state, uncertainty, prediction,
   innovation, drift, and correction.
4. **Proposal-and-enforcement plates** distinguish learned intent, validation,
   veto, fallback, safe state, and actuator command.
5. **Placement plates** locate capabilities, data movement, resource contention,
   trust boundaries, and failure domains.
6. **Evidence plates** show distributions, operating frontiers, coverage,
   invalidation boundaries, promotion decisions, and assurance cases.
7. **Authority plates** show who may observe, teach, approve, execute, interrupt,
   retain, revise, and forget.
8. **System-build plates** revisit the same canonical system after each chapter
   and make the new artifact visible.

Not every section receives a figure. A figure is warranted only when spatial
relationship, time, causality, uncertainty, ownership, or measured tradeoff is
materially clearer than it would be in prose or a table.

### Chapter-Level Visual Program

| **Chapter** | **Primary Visual Argument** |
|---:|---|
| 1 | Open-loop output versus action that produces the next world state |
| 2 | Task efficacy decays as information ages relative to the world's timescale |
| 3 | Complete-loop measurement boundary and the tail that changes the claim |
| 4 | Multi-rate runtime continues while a learned service is late or unavailable |
| 5 | Observation quality, freshness, energy, and bandwidth form an operating frontier |
| 6 | Timestamped observations update an uncertain belief across frames and clocks |
| 7 | A policy interface turns grounded state into expiring intent and action chunks |
| 8 | Independent enforcement separates a proposal from physical authority |
| 9 | One placement change ripples through shared resources and failure domains |
| 10 | Each evidence tier supports some claims and invalidates others |
| 11 | Human authority attaches to specific operations and can be revoked |
| 12 | Interaction becomes admissible data, a candidate update, or a rejected record |
| 13 | Deployment claims terminate in evidence, explicit gaps, and a release verdict |

### Visual Quality Standard

A manuscript figure is complete only when:

- its claim and supported decision can be stated after a brief inspection;
- the figure uses only concepts already introduced;
- topology, timing, units, hardware facts, and authority paths are correct;
- quantitative marks come from data or a clearly labeled analytical model;
- labels fit without crowding and remain legible at manuscript width;
- it remains meaningful in grayscale and does not rely on color alone;
- its caption states the conclusion rather than inventorying the objects;
- its alt text explains the relationship and takeaway; and
- the exact asset has been inspected in both rendered HTML and PDF.

---

## Authoring Method

One persistent steward should own each chapter's argument. Independent agents
may research concepts, audit pedagogy, design representations, challenge claims,
or map labs, but unrelated agents should not write neighboring sections from
cold prompts.

Each chapter should move through the following reviews:

1. **Chapter contract.** Lock the objective, misconception, decision, artifact
   delta, prerequisites, and deferred concepts.
2. **Fundamental material.** Identify indispensable concepts, distinctions,
   failure modes, and primary sources without drafting prose.
3. **Backward pedagogy.** Work from the transfer task to the necessary teaching
   sequence and representations.
4. **Outline challenge.** Find hidden prerequisites, false universals, vendor
   leakage, repetition, and dependence on the lab.
5. **Progressive drafting.** The chapter steward drafts one section or connected
   cluster at a time using accepted prior material and the next section's entry
   condition.
6. **Chapter integration.** Repair continuity, notation, example flow, pacing,
   and the landing into the cumulative dossier.
7. **Independent review.** Audit technical correctness, citation support, novice
   comprehension, practitioner transfer, visual sufficiency, and human voice.
8. **Lab mapping.** Instantiate the already-complete pedagogy through analytical,
   hosted, and physical forms.

Context should grow through accepted decisions, not raw transcripts. Every
section-generation call receives the book goal, chapter contract, concept
ownership, incoming dossier state, accepted preceding sections, current section
job, required representation, and what the following section may assume.

---

## Definition of Success

The project succeeds when a reader can encounter a physical-AI system the book
never discusses and ask better questions than “Which model should I run?” The
reader should be able to find the causal loop, identify the physical deadline,
measure the complete path, expose stale belief, inspect the policy interface,
separate proposal from authority, place enforcement in an independent domain,
state what the evidence actually proves, govern the system's ability to learn,
and refuse deployment when the case is not defensible.

The book should be judged by transfer, not fashion. Its models and hardware may
age. Its method for reasoning about systems that sense and act should not.
