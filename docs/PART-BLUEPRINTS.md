# Physical AI Part Openers & Role Declarations

**Status:** Locked Canonical Blueprint  
**Book:** *Physical AI: Machine Learning Systems That Sense and Act*  
**Course:** *Physical AI Systems*  
**Related Docs:** `CHAPTER-OUTLINES.md` · `MANIFESTO.md` · `COURSE.md`

---

## The Part Opener Architecture

Every Part opens with a dedicated **1-Page Part Manifesto & Role Declaration** containing:
1. **Part Role Statement:** Explicitly declaring *"The role of this Part in the physical AI system is..."*
2. **System Job & Scope:** The specific architectural transformation performed across the Part's chapters.
3. **Pipeline Stage Location:** Where the Part sits within the canonical 7-stage pipeline (*Sensing $\rightarrow$ Perception $\rightarrow$ Memory $\rightarrow$ Reasoning $\rightarrow$ Planning $\rightarrow$ Enforcement $\rightarrow$ Learn/Deploy*).
4. **Entering vs. Exiting Reader State:** What the reader understands entering the Part and what design capability they gain upon exiting.
5. **Dossier Artifact Evolution:** How the reader's Cumulative Design Dossier evolves across the Part.

---

## PART I: Foundations & Metrology (Chapters 1–2)

> **Role Declaration:**  
> *"The role of Part I is to establish the physical boundaries of the system, define what Physical AI is and is not, introduce the System 1 / System 2 proposal-permission architecture, unravel the complete 7-stage pipeline map, and quantify the non-negotiable costs imposed by the physical world."*

### System Job
- Ground the system in physical reality—matter, momentum, energy, and irreversible state mutation ($W_t \rightarrow W_{t+1}$).
- Establish the Proposal-Permission Split (System 2 untrusted MPU proposal brain vs. System 1 trusted MCU permission brain).
- Provide the complete 7-stage pipeline architectural map.
- Measure sense-to-actuation metrology ($P_{99}$ tail latencies, information freshness decay $\Delta t$, world dynamic deadlines $\tau_{\text{world}}$).

### Pipeline Stage Location
- Scope Definition & Pipeline Architecture Overview (Stages 1 through 7 Map).

### Reader Journey
- **Entering State:** Believes Physical AI is simply putting an ML model or VLM onto a robot or microcontroller.
- **Exiting State:** Can define causal system boundaries, separate proposal from permission compute domains, trace the 7-stage dataflow, and measure real-time tail latency budgets.

### Dossier Artifacts Built
- `Loop Charter` (Ch 1) $\longrightarrow$ `Requirements & Assumptions Ledger` (Ch 2).

---

## PART II: Sense, Perceive & Believe (Chapters 3–4)

> **Role Declaration:**  
> *"The role of Part II is to construct the machine's internal world model and proprioceptive state—converting noisy, high-dimensional physical observations into a time-indexed, spatially registered temporal belief."*

### System Job
- Ingest physical sensor modalities (vision, LiDAR, IMU, tactile) and manage pre-inference DMA and memory copy overheads (Stage 1 & Stage 2).
- Compress observations into spatial latent tokens under strict edge NPU/memory Pareto frontiers.
- Transform spatial frame trees ($SE(3)$), synchronize hardware clocks via PTP (IEEE 1588), and maintain time-indexed temporal belief (Stage 3).
- Monitor proprioceptive state (joint positions, forces) and interoceptive health (thermal derating, bus voltage sag).

### Pipeline Stage Location
- **Stage 1 (Sensing)** $\rightarrow$ **Stage 2 (Perception)** $\rightarrow$ **Stage 3 (Memory & Temporal Belief)**.

### Reader Journey
- **Entering State:** Assumes sensors provide free inputs and that the latest camera sample represents current reality.
- **Exiting State:** Can design Pareto-optimal perception pipelines, synchronize multi-sensor clocks, build $SE(3)$ frame graphs, and maintain uncertainty-aware temporal belief.

### Dossier Artifacts Built
- `Observation Contract` (Ch 3) $\longrightarrow$ `State, Frames & Timing Model` (Ch 4).

---

## PART III: Deliberate, Plan & Enforce (Chapters 5–7)

> **Role Declaration:**  
> *"The role of Part III is to close the sense-to-actuation loop—structuring slow System 2 semantic reasoning into expiring intent proposals, unrolling VLA trajectory action chunks, and shielding the machine with fast System 1 MCU safety vetoes."*

### System Job
- Anchor open-vocabulary natural language to 3D spatial affordances and structure VLM reasoning into expiring intent leases (Stage 4 - System 2 Cortex).
- Unroll Vision-Language-Action (VLA) multi-step trajectory action chunks ($H$) with continuous replanning and temporal ensembling (Stage 5 - Planning).
- Decouple physical authority from neural policies, placing independent real-time safety enforcers on MCU hardware to check dynamic stopping bounds ($d_{\text{stop}}$) and execute physical fallbacks (Stage 6 - System 1 Reflex Arc).

### Pipeline Stage Location
- **Stage 4 (Reasoning)** $\rightarrow$ **Stage 5 (Planning)** $\rightarrow$ **Stage 6 (Action & Safety Enforcement)**.

### Reader Journey
- **Entering State:** Believes neural policy outputs can be forwarded directly to motors or clipped with simple software boundaries.
- **Exiting State:** Can architect asynchronous proposal-permission interfaces, select action chunk horizons, calculate dynamic stopping bounds, and write checkable MCU safety veto logic.

### Dossier Artifacts Built
- `Policy Interface & Intent Schema` (Ch 5) $\longrightarrow$ `Planning Schema` (Ch 6) $\longrightarrow$ `Action Limits & Enforcement Design` (Ch 7).

---

## PART IV: Place, Govern & Assure (Chapters 8–10)

> **Role Declaration:**  
> *"The role of Part IV is to transform the physical AI system into an engineered, production-ready product—mapping execution across heterogeneous hardware, governing data flywheels and human authority, and assembling the evidence case for release."*

### System Job
- Partition the 7-stage pipeline across heterogeneous MCU, MPU, NPU, and Cloud hardware under shared memory, power, and thermal ledgers (Ch 8).
- Structure hardware-synchronized PTP trajectory logs, handle policy endogeneity and intervention selection bias, and build bumpless human override controls (Stage 7 - Governance & Learn).
- Define Target Deployment Envelopes (ISO 22736 ODD), execute multi-rung SIM/HIL qualification ladders, inject cross-layer faults, and assemble Claim-Argument-Evidence (CAE/GSN) safety cases to issue an evidence-backed **Deploy / Condition / Refuse** release verdict.

### Pipeline Stage Location
- **Stage 7 (Learn & Governance)** $\rightarrow$ **Hardware System Placement** $\rightarrow$ **System Qualification & Release Verdict**.

### Reader Journey
- **Entering State:** Believes a high benchmark score or impressive demo video constitutes deployment proof.
- **Exiting State:** Can construct whole-system resource ledgers, engineer human override handoffs, execute HIL fault injection, build CAE safety cases, and render defensible release verdicts.

### Dossier Artifacts Built
- `Placement Map & Ledger` (Ch 8) $\longrightarrow$ `Human-Authority & Governed Data Record` (Ch 9) $\longrightarrow$ `Integrated Deployment Case` (Ch 10).
