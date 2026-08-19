# Physical AI Systems — Course & Studio Guide

**Course Portal:** [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai)  
**Academic Offering:** ETH Zurich (D-ITET / D-INFK) · 6 ECTS Project Seminar & Hardware Studio  
**Author & Lecturer:** **Prof. Vijay Janapa Reddi** (Harvard University / Visiting Professor, ETH Zurich)  
**Kit & Studio Lead:** **Dr. Andrea Mattia Garavagno** (Integrated Systems Laboratory, IIS, D-ITET, ETH Zurich)

---

## 1. Course Vision & Pedagogical Philosophy

Standard machine learning ends at digital output: a language model emits text; a classifier emits a token. In the digital realm, software bugs are safely isolated behind glass—transactions roll back, dropped packets retry, and exceptions are caught.

**Physical AI Systems begin at the exact moment digital software commands physical actuators—accelerating mass, consuming energy, interacting with humans, and permanently altering the physical world ($W_t \to W_{t+1}$).**

Because physical actions cannot be rewound (**you cannot `ctrl+z` kinetic momentum or Joule heat**), this course trains engineers to answer one central question:

> **"What must the surrounding system know, measure, enforce, preserve, and prove before an unverified learned proposal may produce a physical consequence?"**

---

## 2. The Core Conceptual Framework

### The Three Universal Defining Properties
1. **Learned Foundation Component:** High-capacity learned models (VLMs, World Models, Diffusion Policies) capable of open-world generalization, replacing brittle hardcoded if-then state machines.
2. **Operations Across the Analog $\longleftrightarrow$ Digital Boundary:** Digital tensors and tokens directly command continuous physical energy fluxes (inverters, motor coils, momentum).
3. **Governed by Irreversible Physical Laws:** Conservation of energy, momentum $p=mv$, Joule heating $I^2R$, and static/dynamic friction. Zero undo button.

### The Three Canonical Archetypes
* **Archetype 1: Locomotion & Mobility (Free-Space Navigation):** Autonomous Vehicles (Waymo), High-Speed Delivery Drones (Skydio), Quadrupeds (Spot). Focus: $P_{99}$ latency tails and dynamic stopping envelopes ($d_{\text{stop}}$).
* **Archetype 2: Contact Manipulation (Touching & Shaping Matter):** Humanoid Hands (Optimus, Figure), 6-DoF Manipulator Arms, Surgical Robotics. Focus: Discontinuous contact, torque rates ($\dot{\boldsymbol{\tau}}$), and harmonic drive flexspline shear.
* **Archetype 3: Cybernetic Process & Energy (Continuous State Flows):** Smart Grid Power Inverters, EV Battery Management Systems (BMS). Focus: Microsecond AC phase tracking, $I^2R$ thermal accumulation, and runaway prevention.
* **The Desk Bench Twin:** The **Arduino UNO Q Dual-Brain Kit** (Linux Application MPU + Real-Time Cortex-M4 MCU + Camera + Motion Stage) grounding every concept on real bench silicon.

### The Grand Systems Conflict & The Three Cadences
* **Physics Demands *Less Time* ($t \to 0$):** Kinetic momentum carries mass forward; coils accumulate heat; sensor data ages instantly; transport delays erode phase margin.
* **Cognition Demands *More Time* ($t \to \infty$):** Foundation models, spatial transformers, and diffusion decoders need time and compute to deliberate over open-world ambiguity.
* **The Resolution (The Three Cadences):**
  * **System 2 (0.5–2 Hz · Linux MPU):** Semantic Deliberation (Untrusted proposal service emitting Expiring Intent Leases $\mathcal{L}_{\text{intent}}$).
  * **System 1.5 (20–50 Hz · Edge NPU):** Trajectory Action Chunking (Candidate generator emitting $H=16$ waypoint chunks with $\mathcal{C}^2$ jerk splines).
  * **System 1 (1000 Hz · Bare-Metal MCU):** Deterministic Safety Reflex (Sole hardware permission authority running Control Barrier Functions and PWM locks with **`malloc = 0`**).

---

## 3. The 14-Week Master Schedule

| Week | Lecture / Seminar Topic (Book Chapter) | Hardware Lab / Studio Activity (Arduino UNO Q) | Due Milestone / Dossier Checkpoint |
| :---: | :--- | :--- | :---: |
| **W01** | **Course Kickoff & The Dual-Brain Architecture** | Kit unboxing, Linux/FreeRTOS bring-up, IPC ping-pong | **M0: Roster & Kit Bring-up** |
| **W02** | **Ch 1: The Causal Boundary & Co-Design Challenge** | Lab 1 (`labs/01-close-the-loop`): Advisory vs. closed-loop mutation | **M1: `LOOP-01` (Loop Charter)** |
| **W03** | **Ch 2: The Physical Constraints (The Columns)** | Lab 2 (`labs/02-metrology-wall`): $P_{99}$ latency tail metrology & $d_{\text{stop}}$ | **M2: `REQ-01` (Requirements Ledger)** |
| **W04** | **Ch 3: The Cognitive Dimensions (The Rows & Matrix)** | Lab 3 (`labs/03-agent-workflow`): 3-cadence runtime & watchdog crash survival | **M3: `FLOW-01` (Workflow Charter)** |
| **W05** | **Ch 4: Stage 1 — Perceive (Spatial Tokens & Ingestion)** | Lab 4 (`labs/04-dma-tokens`): MIPI DMA bus contention & DINOv2 3D tokens | **M4: `OBS-01` (Observation Contract)** |
| **W06** | **Ch 5: Stage 2 — Remember (World Models & SE(3))** | Lab 5 (`labs/05-latent-state`): $SE(3)$ frame trees & occlusion TTL leases | **M5: `STATE-01` (State & Timing Model)** |
| **W07** | **MIDTERM DESIGN REVIEWS & LIVE SYSTEM DEMOS** | **Live Team Demos:** End-to-end propose $\to$ permit loop on bench hardware | **M6: Midterm System Review** |
| **W08** | **Ch 6: Stage 3 — Reason (VLMs & Intent Leases)** | Lab 6 (`labs/06-vlm-intent`): Open-world VLM prompt grounding & intent leases | **M7: `INTENT-01` (Intent Schema)** |
| **W09** | **Ch 7: Stage 4 — Plan (Diffusion Action Chunking)** | Lab 7 (`labs/07-action-chunking`): ACT trajectory decoding & $\mathcal{C}^2$ jerk splines | **M8: `PLAN-01` (Planning Schema)** |
| **W10** | **Ch 8: Stage 5 — Execute (1 kHz MCU Safety Reflex)** | Lab 8 (`labs/08-cbf-enforcer`): 1 kHz Control Barrier Functions & dynamic stop | **M9: `ENF-01` (Signature Lab)** |
| **W11** | **Ch 9: Heterogeneous Silicon Placement & Bus QoS** | Lab 9 (`labs/09-heterogeneous-placement`): UMA memory QoS & thermal derating | **M10: `PLACE-01` (Placement Map)** |
| **W12** | **Ch 10: Human Governance & Data Flywheels** | Lab 10 (`labs/10-bumpless-governance`): Bumpless takeover & truncated flight logs | **M11: `AUTH-01` (Governance Record)** |
| **W13** | **Ch 11: Defensible Assurance & Fault Trials** | Lab 11 (`labs/11-fault-injection-rig`): Cross-layer fault injection & CAE case | **M12: `REL-01` (Release Case)** |
| **W14** | **FINAL CAPSTONE JURY DEFENSE & DOSSIER SIGN-OFF** | **Whole-System Defense Trial under unannounced seeded faults** | **M13: Capstone Release Verdict** |

: 14-Week Master Schedule and Milestone Deliverables. {#tbl-course-schedule}

---

## 4. Assessment & The 11-Artifact Cumulative Design Dossier

There is **no written final exam**. Students are graded as professional systems engineers building an accumulating, versioned **Cumulative Design Dossier**:

| Grade Weight | Component | Deliverable & Description |
| :---: | :--- | :--- |
| **20%** | **Process & Studio Checkpoints** | Weekly milestone progress, active lab bench participation, and code commits. |
| **15%** | **Midterm System Review (W07)** | 10-minute presentation + live bench demo of closed-loop proposal-permission pipeline. |
| **25%** | **Final Capstone Defense (W14)** | Oral jury defense and live recovery from an instructor-seeded hardware/software fault. |
| **40%** | **Cumulative Design Dossier** | Complete 11-artifact engineering dossier (`LOOP-01` through `REL-01`). |

### The 11 Dossier Milestones
1. `LOOP-01`: **Loop Charter** (Causal boundary, power isolation, and invariant definitions)
2. `REQ-01`: **Requirements & Latency Ledger** (World deadlines, $P_{99}$ latency budgets, stopping envelopes)
3. `FLOW-01`: **Workflow Charter** (Three-cadence timing model, IPC mailboxes, and watchdog protocol)
4. `OBS-01`: **Observation Contract** (Sensor sample rates, MIPI DMA buffers, and PTP timestamps)
5. `STATE-01`: **State & Timing Model** ($SE(3)$ coordinate frame tree, latent JEPA, and TTL leases)
6. `INTENT-01`: **Policy & Intent Schema** (VLM prompt decomposition, 3D workspace bounding $\mathcal{B}$, velocity clamps)
7. `PLAN-01`: **Planning Schema** (Action chunk horizon $H=16$, temporal ensembling, $\mathcal{C}^2$ jerk splines)
8. `ENF-01`: **Enforcement Design** (1 kHz Control Barrier Functions, dynamic stopping $d_{\text{stop}}$, STO interlocks)
9. `PLACE-01`: **Placement Map & Resource Ledger** (Heterogeneous MPU/NPU/MCU memory, compute, and thermal limits)
10. `AUTH-01`: **Governance Record** (Bumpless human handoff, intervention slicing, and cryptographic flight logs)
11. `REL-01`: **Integrated Deployment Case** (Claim-Argument-Evidence case rendering a **Deploy / Condition / Refuse** release verdict)

---

## 5. Studio & Hardware Kit Infrastructure (For Andrea & Teaching Team)

### Reference Hardware Kit: Arduino UNO Q Dual-Brain
* **Host Brain (MPU):** Qualcomm Linux Application Processor running PyTorch, TensorRT, VLMs, and ACT Action Chunk decoders.
* **Reflex Brain (MCU):** Dedicated ARM Cortex-M4 Microcontroller running bare-metal / FreeRTOS with strictly **zero dynamic heap allocation (`malloc = 0`)**.
* **Camera & Vision:** MIPI CSI-2 camera module with DMA ring buffer capture.
* **Sensors:** 6-DoF IMU, high-resolution optical shaft encoders, phase current sensing.
* **Actuation & Motion:** Multi-axis precision motion stage with current-limiting gate drivers and emergency Safe Torque Off (STO) relay.

### Studio Operations & TA Guidelines
* **Team Formation (W01):** Pair students with complementary skills (e.g., 1 D-INFK machine learning / software student + 1 D-ITET embedded systems / control student).
* **Studio Lab Hours:** Weekly hands-on lab sessions staffed by Andrea and TAs. Teams verify hardware firmware contracts using logic analyzers and oscilloscope triggers.
* **Capstone Defense Protocol (W14):**
  1. Team presents their complete 11-artifact Cumulative Design Dossier to the faculty jury.
  2. The instructor injects an unannounced fault (e.g., pulling the camera MIPI cable, freezing the Linux MPU with a memory exhaustion storm, or inducing synthetic clock jitter).
  3. The system must autonomously transition to a safe state without violating physical invariants ($h(x) \ge 0, d_{\text{stop}} \le d_{\text{clear}}$), and the team must diagnose the root cause live from telemetry logs.
