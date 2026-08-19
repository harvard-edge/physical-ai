# Physical AI Systems — Course Syllabus

**ETH Zurich · Project-Based Course · 6 ECTS**  
**Online / Partner Offering:** [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai)

| Parameter | Specification |
| :--- | :--- |
| **Course** | Physical AI Systems (*Physical AI: Machine Learning Systems That Sense and Act*) |
| **Credits** | 6 ECTS (≈ 150–180 total workload hours) |
| **Format** | Project seminar + hardware studio / group project · **No written final exam** |
| **Language** | English |
| **Level** | Advanced Bachelor (3rd/4th year) & Master (D-ITET, D-INFK, Robotics/CPS) |
| **Contact** | Weekly Seminar (2 h / week) + Hands-On Studio / Lab Time |
| **Reference Book** | *Physical AI: Machine Learning Systems That Sense and Act* (Vijay Janapa Reddi) |
| **Hardware Kit** | **Physical AI Kit** (Arduino UNO Q Dual-Brain: Linux MPU + Real-Time MCU) |

: Course Logistics and Parameters. {#tbl-course-logistics}

---

## 1. Teaching Team

### Prof. Vijay Janapa Reddi — Lecturer
* Gordon McKay Professor of Electrical Engineering, Harvard University
* Visiting Professor, ETH Zurich (Integrated Systems Laboratory, IIS, D-ITET)
* **Office:** ETZ F 83 · **Email:** [vjanapa@ethz.ch](mailto:vjanapa@ethz.ch) · **Web:** [Homepage](https://profvjreddi.github.io/homepage)

### Dr. Andrea Mattia Garavagno — Co-Teacher & Studio Lead
* Postdoctoral Researcher, ETH Zurich (Integrated Systems Laboratory, IIS, D-ITET)
* Runs day-to-day Physical AI Kit bring-up, studio hours, and hardware milestone checkpoints.

**Office Hours:** By appointment (email instructors with subject `[Physical AI]`).

---

## 2. Course Overview & Three Defining Properties

Standard machine learning ends at digital output. A classifier emits a label; a language model emits text. **Physical AI Systems** begin when that output moves matter, consumes kinetic energy, affects humans, and alters all future sensory observations ($W_t \to W_{t+1}$). **You cannot `ctrl+z` kinetic energy.**

An engineered system is defined as **Physical AI** if and only if it satisfies three criteria:
1. **Learned Foundation Component:** High-capacity learned models (VLMs, World Models, Diffusion Policies) capable of open-world generalization.
2. **Operations Across the Analog $\longleftrightarrow$ Digital Boundary:** Digital tensors and tokens directly governing continuous analog energy fluxes (inverters, motor coils, valves).
3. **Governed by Irreversible Physical Laws:** Conservation of energy, momentum ($p=mv$), Joule heating ($I^2R$), and friction.

### The Three Canonical Archetypes & The Desk Bench Twin
* **Archetype 1: Locomotion & Mobility:** Autonomous vehicles (Waymo), delivery drones (Skydio), quadrupeds ($P_{99}$ latency tails & dynamic stopping $d_{\text{stop}}$).
* **Archetype 2: Contact Manipulation:** Humanoid hands, robot arms, surgical tools (Torque rates $\dot{\boldsymbol{\tau}}$, harmonic drive flexspline shear).
* **Archetype 3: Cybernetic Process & Energy:** Smart grid inverters, EV battery thermal management ($I^2R$ Joule heating & AC phase synchronization).
* **The Desk Bench Twin:** Arduino UNO Q Dual-Brain Kit (Linux Application MPU + Real-Time Cortex-M4 MCU).

### What This Course Is (and Is Not)

| What This Course Is NOT | What This Course IS |
| :--- | :--- |
| ✗ A compressed classical robotics kinematics / ROS course | ✓ A **systems engineering discipline** for learned, acting machines |
| ✗ TinyML “quantize and deploy” alone | ✓ Bridging **high-level foundation models to real-time safety** |
| ✗ A cloud LLM prompt-chaining / chatbot lab | ✓ **Multi-rate runtimes, zero-copy DMA, IPC, and watchdogs** |
| ✗ A purely theoretical or simulation-only seminar | ✓ Real hardware with **mass, inertia, bus contention, and tails** |

: Course Boundary and Scope. {#tbl-course-scope}

---

## 3. The 14-Week Schedule

The curriculum follows the **Physical AI Co-Design Matrix**, moving from physical and cognitive foundations to internal spatial belief, deliberative reasoning, real-time safety vetoes, heterogeneous placement, and defensible release:

| Week | Seminar & Chapter Topic | Project & Kit Milestone | Due Artifact Checkpoint |
| :---: | :--- | :--- | :---: |
| **W01** | **Kickoff & The Dual-Brain Architecture** | Team formation & UNO Q kit bring-up | **M0: Roster + Kit Setup** |
| **W02** | **Ch 1: The Causal Boundary & Co-Design Matrix** | Matter, momentum & power isolation sandbox | **M1: `LOOP-01` (Loop Charter)** |
| **W03** | **Ch 2: The Physical Constraints (The Columns)** | Sense-to-actuation $P_{99}$ tail metrology & stopping bounds | **M2: `REQ-01` (Requirements Ledger)** |
| **W04** | **Ch 3: The Cognitive Dimensions (The Rows & Matrix)** | Multi-rate 3-cadence runtime & watchdog crash survival | **M3: `FLOW-01` (Workflow Charter)** |
| **W05** | **Ch 4: Stage 1 — Perceive (Spatial Tokens & Ingestion)**| Zero-copy DMA ring buffers & DINOv2 spatial tokens | **M4: `OBS-01` (Observation Contract)** |
| **W06** | **Ch 5: Stage 2 — Remember (World Models & SE(3))** | $SE(3)$ frame graph trees & uncertainty decay leases | **M5: `STATE-01` (State & Timing Model)** |
| **W07** | **MIDTERM DESIGN REVIEWS & LIVE DEMOS** | **Team Talks:** Proposal–Permission closed-loop bench demo | **M6: Midterm System Review** |
| **W08** | **Ch 6: Stage 3 — Reason (VLMs & Intent Leases)** | Multimodal VLM grounding & expiring intent leases | **M7: `INTENT-01` (Intent Schema)** |
| **W09** | **Ch 7: Stage 4 — Plan (Diffusion Action Chunking)** | Receding-horizon ACT rollouts & $\mathcal{C}^2$ jerk splines | **M8: `PLAN-01` (Planning Schema)** |
| **W10** | **Ch 8: Stage 5 — Execute (1 kHz MCU Safety Reflex)**| 1 kHz Control Barrier Functions & dynamic stop halts | **M9: `ENF-01` (Signature Lab)** |
| **W11** | **Ch 9: Heterogeneous Silicon Placement & UMA QoS** | Compute, SRAM, and bus arbitration resource ledger | **M10: `PLACE-01` (Placement Map)** |
| **W12** | **Ch 10: Human Governance & Governed Data Flywheels**| $\mathcal{C}^2$ bumpless transfer & truncated episode slicing | **M11: `AUTH-01` (Governance Record)** |
| **W13** | **Ch 11: Defensible Assurance & Seeded Fault Trials** | Cross-layer fault injection rig & CAE safety case | **M12: `REL-01` (Release Case)** |
| **W14** | **FINAL CAPSTONE DEFENSE & DOSSIER SUBMISSION** | **Oral defense under unannounced seeded bench faults** | **M13: Capstone Release Verdict** |

: 14-Week Master Schedule and Milestones. {#tbl-master-schedule}

---

## 4. Assessment & The Cumulative Design Dossier

There is **no written final exam**. Graded semester performance is evaluated based on continuous engineering progress, oral defense, and the written engineering record:

| Component | Weight | Description |
| :--- | :---: | :--- |
| **Process & Studio Checkpoints** | **20%** | Weekly milestone progress, active studio debugging, and team collaboration. |
| **Midterm Presentation (W07)** | **15%** | 10-minute talk + live demo of the working observe $\to$ propose $\to$ permit loop. |
| **Final Design Defense (W14)** | **25%** | Oral capstone defense and live diagnosis of an instructor-seeded bench fault. |
| **Cumulative Design Dossier (W14)** | **40%** | The complete versioned engineering dossier (`LOOP-01` through `REL-01`). |

: Grade Weighting Breakdown. {#tbl-grade-breakdown}

### The 11 Cumulative Design Dossier Milestones
1. `LOOP-01`: **Loop Charter** (Scope, boundary, and authority)
2. `REQ-01`: **Requirements Ledger** (World deadlines and $P_{99}$ latency budgets)
3. `FLOW-01`: **Workflow Charter** (Three-cadence timing model, IPC mailboxes, and watchdog protocol)
4. `OBS-01`: **Observation Contract** (Sensor rates, DMA channels, and timestamps)
5. `STATE-01`: **State & Timing Model** ($SE(3)$ frame tree and TTL validity leases)
6. `INTENT-01`: **Policy & Intent Schema** (VLM 3D bounding boxes and expiration leases)
7. `PLAN-01`: **Planning Schema** (Action chunk horizons $H$ and temporal ensembling)
8. `ENF-01`: **Enforcement Design** (MCU 1 kHz safety filters and physical fallback states)
9. `PLACE-01`: **Placement Map & Resource Ledger** (Whole-system compute/memory/power budgets)
10. `AUTH-01`: **Human-Authority & Governance Record** (Bumpless overrides and truncated logs)
11. `REL-01`: **Integrated Deployment Case** (Claim-Argument-Evidence case and **Deploy / Condition / Refuse** release verdict)

---

## 5. Prerequisites & The Two On-Ramps

We pair students with complementary backgrounds into **2–3 person teams**:

* **On-Ramp 1 (ML & Software / D-INFK):** Strong Python/PyTorch background; learns real-time MCU enforcers, DMA bus contention, and hardware watchdogs.
* **On-Ramp 2 (Embedded & CPS / D-ITET):** Strong C/C++, FreeRTOS, and electronics background; learns VLM spatial grounding, action chunk unrolling, and governed data flywheels.

---

## 6. Course Policies & Safety Invariants

* **Safety Invariant:** All autonomous machines must run with an active MCU safety enforcer. Intentionally bypassing the hardware enforcer for a demo is an immediate failure.
* **Collaboration:** High-level architectural discussion between teams is encouraged; firmware and dossier schemas must be the team's own original work.
* **Materials & Kit Loan:** Kits are provided on loan for the duration of the semester. Open follow-along materials are available at [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai).

