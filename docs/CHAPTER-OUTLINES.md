# Physical AI Chapter Outlines & Section Blueprints

**Status:** Locked Canonical Blueprint (10 Chapters · 50 Sections · Sub-Bullet Outlines)  
**Book:** *Physical AI: Machine Learning Systems That Sense and Act*  
**Author:** Vijay Janapa Reddi  
**Course:** *Physical AI Systems*  
**Backward-Design Source:** `BOOK-GOAL.md` · **Manifesto:** `MANIFESTO.md` · **Part Blueprints:** `PART-BLUEPRINTS.md` · **Agent Workflows:** `AGENT-WORKFLOWS.md`

---

## The North Star Question

> **"How do we engineer a machine learning system that turns unverified neural proposals into trusted physical actions before kinetic energy hits the real world?"**

### The Graduate Endpoint
Given an unfamiliar physical task, an unfamiliar model family (VLM/VLA/RL), an unfamiliar embodiment (arm, rover, humanoid), and an unfamiliar compute stack, the graduate can:
1. **Architect** a multi-rate, fault-contained runtime that separates learned proposals (System 2 MPU Cortex) from real-time physical permission (System 1 MCU Reflex).
2. **Quantify** sense-to-actuation tail latencies ($P_{99}$), mutual information freshness ($\Delta t$), and dynamic stopping bounds ($d_{\text{stop}}$) across heterogeneous hardware.
3. **Construct** a Claim-Argument-Evidence (CAE/GSN) safety case and issue a defensible **Deploy / Condition / Refuse** release verdict backed by empirical HIL/SIM test evidence.

---

## The Canonical 7-Stage Physical AI Pipeline

All 10 chapters map directly onto the 7 canonical stages of an agentic physical machine:

$$\text{(1) Sensing} \longrightarrow \text{(2) Perception} \longrightarrow \text{(3) Memory/State} \longrightarrow \text{(4) Reasoning} \longrightarrow \text{(5) Planning} \longrightarrow \text{(6) Action/Enforcement} \longrightarrow \text{(7) Learn/Deploy}$$

---

## PART I: Foundations & Metrology (Chapters 1–2)

> **Part Role Declaration:**  
> *"The role of Part I is to establish the physical boundaries of the system, define what Physical AI is and is not, introduce the System 1 / System 2 proposal-permission architecture, unravel the complete 7-stage pipeline map, and quantify the non-negotiable costs imposed by the physical world."*

- **Chapters:** Chapter 1 (*Physical AI Systems Scope*) & Chapter 2 (*The Physical System, Its Loop, and the 7-Stage Architecture*).
- **Dossier Deliverables:** `Loop Charter` (Ch 1) $\longrightarrow$ `Requirements & Assumptions Ledger` (Ch 2).

---

### Chapter 1 — Physical AI Systems Scope

**Opening Question:** When does a machine learning system become a physical-AI system?

**Objective:** Given a system description, the reader can tell when a learned component acts back into the physical world, trace its causal loop, and define the scope of the engineered system.

#### Section Blueprints
- **1.1 Grounding in the Physical World: Matter, Energy, and State Mutation**
  - *1.1.1 The Physical Reality vs. Digital Virtualism:* Software bits can be rolled back with `try/catch` or `ctrl+z`; physical actions ($W_t \rightarrow W_{t+1}$) governed by mass, momentum, and energy are permanent and irreversible.
  - *1.1.2 State Mutation & Causal Consequences:* Actions mutate physical world state ($W_t \rightarrow W_{t+1}$), altering all future observations ($O_{t+1}$). Kinetic energy compounds over time.
  - *1.1.3 Physical Constraints as Boundary Conditions:* Friction ($\mu$), gravity ($g$), thermal limits, and light speed set non-negotiable hard bounds on every algorithm.
- **1.2 What Physical AI Is (and What Pre-Physical AI Is)**
  - *1.2.1 Core Definition:* Learned components generate unverified proposals that act back into the physical world under delegated physical authority.
  - *1.2.2 What Pre-Physical AI IS:* Human-in-the-loop advisory software (radiology assistant, coding co-pilot) where human holds physical authority to act.
  - *1.2.3 Delegated Physical Authority:* The fundamental transition when a machine holds physical permission to energize motors and move matter autonomously.
- **1.3 The Fundamental Paradigm Shift: Digital ML vs. Physical AI**
  - *1.3.1 Substrate Shift:* Offline accuracy ($\text{F1, BLEU}$) vs. Sense-to-actuation tail latencies ($P_{99}$), freshness ($\Delta t$), and stopping bounds ($d_{\text{stop}}$).
  - *1.3.2 Cost Shift:* Extra compute cost vs. Hardware destruction and physical collision.
  - *1.3.3 The 8-Dimension System Matrix:* Systematic comparison across 8 system dimensions.
- **1.4 Dismantling the Monolithic Misconception: System 1 & System 2 Architecture**
  - *1.4.1 Biological Parallels:* System 1 (Spinal Reflex Arc & Cerebellum: fast, deterministic motor control) vs. System 2 (Cerebral Cortex: slow, deliberative reasoning).
  - *1.4.2 Proposal-Permission Split:* System 2 Untrusted MPU Proposal Brain vs. System 1 Trusted MCU Permission Brain.
  - *1.4.3 Architectural Decoupling:* Why monolithic models fail when running slow cortical reasoning directly on motor nerves.
- **1.5 System Scope, Causal Boundaries, and Loop Charters**
  - *1.5.1 Drawing Causal Boundaries:* Scoping sensor hardware, pre-processing, neural models, safety enforcers, actuators, and world feedback.
  - *1.5.2 Formalizing `Loop Charter`:* Schema defining task, world states, proposal component, permission rules, and allowed actions.
  - *1.5.3 Handoff to Metrology:* Bridging Chapter 1 scope into Chapter 2 architecture.

**Dossier Artifact:** `Loop Charter`

---

### Chapter 2 — The Physical System, Its Loop, and the 7-Stage Architecture

**Opening Question:** Here is the physical machine, here is its loop—how do all 7 stages unravel together, and how do we measure what the physical world demands of them?

**Objective:** Given a physical machine description, the reader can trace how data flows through all 7 pipeline stages, explain the role and necessity of each stage, derive deadlines from world dynamics, measure tail latency distributions ($P_{99}$), and quantify information freshness decay ($\Delta t$).

#### Section Blueprints
- **2.1 Physical Embodiment, Topology, and Human Proprioception**
  - *2.1.1 Biological Parallel:* Human Proprioception (encoders, IMUs, tactile feedback) & Interoception (winding temperature, voltage sag, phase currents).
  - *2.1.2 Mechanical Realities:* Embodiment morphology, motor payload capacity, chassis dynamics, mass.
  - *2.1.3 Compute Interconnect Topology:* Sensor buses (MIPI-CSI, USB), compute buses (AXI, PCIe), actuator buses (CAN-FD, EtherCAT). MCU + MPU split.
- **2.2 Closed-Loop Causality and World Timescales**
  - *2.2.1 World Deadlines ($\tau_{\text{world}}$):* Deriving physical deadlines from target velocity, friction limits, and momentum.
  - *2.2.2 World vs Inference Timescale:* Why a 500ms VLM reasoning loop cannot stabilize a 10ms dynamic physical system without intermediate stages.
  - *2.2.3 Closed-Loop Stability Thresholds:* Maximum allowable sense-to-actuation latency before open-loop control divergence.
- **2.3 The 7-Stage Architectural Unraveling (The System Map)**
  - *2.3.1 Walkthrough of 7 Stages:* Sensing $\rightarrow$ Perception $\rightarrow$ Memory/State $\rightarrow$ Reasoning $\rightarrow$ Planning $\rightarrow$ Action/Enforcement $\rightarrow$ Learn/Deploy.
  - *2.3.2 Why Each Stage Is Necessary:* Systemic risks of omitting any single stage.
  - *2.3.3 Multi-Rate Decoupling:* Fast control loops (100-1000 Hz) running continuously while slow reasoning loops (1-5 Hz) update asynchronously.
- **2.4 Sense-to-Actuation Metrology: Tail Latencies ($P_{99}$) and Freshness Decay ($\Delta t$)**
  - *2.4.1 End-to-End Timing Metrics:* Transduction $\rightarrow$ DMA $\rightarrow$ Preprocessing $\rightarrow$ Inference $\rightarrow$ Enforcer $\rightarrow$ Motor drive.
  - *2.4.2 Tail Latency Distributions ($P_{99}, P_{99.9}$):* Why mean latency hides physical failure and tail spikes cause crashes.
  - *2.4.3 Mutual Information Decay ($\Delta t$):* How aging sensor data erodes safety margins and expands dynamic stopping distance ($d_{\text{stop}}$).
- **2.5 Continuous Multi-Rate Runtimes**
  - *2.5.1 Multi-Rate Thread Scheduling:* MCU control (1000 Hz) + VLA policy (20 Hz) + VLM reasoning (1 Hz).
  - *2.5.2 Lock-Free Queues:* Decoupling asynchronous execution without thread contention locks.
  - *2.5.3 Fault Containment:* MPU kernel crash isolation via independent MCU execution (`Continuous Runtime Skeleton`).

**Dossier Artifact:** `Requirements & Assumptions Ledger`

---

## PART II: Sense, Perceive & Believe (Chapters 3–4)

> **Part Role Declaration:**  
> *"The role of Part II is to construct the machine's internal world model and proprioceptive state—converting noisy, high-dimensional physical observations into a time-indexed, spatially registered temporal belief."*

- **Chapters:** Chapter 3 (*Perception and Sensor Encoders*) & Chapter 4 (*State Estimation and Temporal Belief*).
- **Pipeline Stages:** **Stage 1 (Sensing)** $\rightarrow$ **Stage 2 (Perception)** $\rightarrow$ **Stage 3 (Memory & Temporal Belief)**.
- **Dossier Deliverables:** `Observation Contract` (Ch 3) $\longrightarrow$ `State, Frames & Timing Model` (Ch 4).

---

### Chapter 3 — Sensory-Motor Perception and Physical Tokenization

**Opening Question:** How do we ingest raw physical signals (photons, forces, motion) into compact spatial tokens without starving memory buses or adding tail latency to the control loop?

**Objective:** Given a physical machine and environment, the reader can balance sensory acquisition, pre-inference DMA ingestion overheads, edge NPU memory bandwidth, and spatial tokenization to formalize an observation contract.

#### Section Blueprints
- **3.1 Physical Sensor Modalities, Transduction & Failure Modes**
  - *3.1.1 Physical Transduction Physics:* Converting physical phenomena into digital signals across vision (RGB-D), kinematics (IMUs, encoders), range (LiDAR), and contact (tactile GelSight arrays).
  - *3.1.2 Physical Environment Failure Modes:* Sensor degradation under motion blur, lens mud/dust, darkness/glare, acoustic specular reflection, and thermal calibration drift.
  - *3.1.3 Complementary Sensor Suites:* Combining vision, range, and touch to eliminate single-sensor blind spots without exceeding mass or power budgets.
- **3.2 Sensor Ingestion Overheads & Bus Contention**
  - *3.2.1 The Pre-Inference Ingestion Tax:* Quantifying latency incurred *before* neural inference starts: ADC conversion, DMA transfers over MIPI-CSI/PCIe, format conversion, and memory copying.
  - *3.2.2 Shared Memory Bus & UMA L3 Cache Eviction:* How high-resolution image streams saturate AXI/PCIe buses and evict L3 cache lines on Unified Memory Architectures (UMA SoCs), starving CPU control threads and causing $P_{99}$ latency spikes.
  - *3.2.3 Zero-Copy Hardware DMA Architecture:* Structuring zero-copy DMA ring buffers directly into NPU SRAM to bypass OS page-fault jitter and memory allocations.
- **3.3 Spatial Affordance Tokenization & Encoder Selection**
  - *3.3.1 Spatial Tokenization for Physical Action:* Encoding visual streams into spatial affordance tokens (where can the robot grasp, step, or navigate?) rather than passive classification labels.
  - *3.3.2 NPU Memory Complexity Scaling:* Quadratic ViT self-attention memory footprint ($O(N^2)$) vs. CNN downsampling pyramids ($O(N)$) under tight edge SRAM constraints.
  - *3.3.3 Token Resolution vs. Action Latency:* Trading off spatial token resolution against downstream VLA memory footprint and ingestion cadence.
  - *3.3.4 Action Representation Taxonomy:* Contrasting discrete action bin tokenization (RT-1/RT-2 256-bin spatial tokens) vs continuous trajectory decoders (Diffusion Policy, ACT, Flow Matching) for memory footprint vs execution responsiveness.
- **3.4 Pareto Frontiers in Sensory-Motor Perception**
  - *3.4.1 Multi-Objective Perception Frontiers:* Formalizing trade-offs: Observation Quality ($Q$) vs. Latency ($L$), Energy ($E$), Memory ($M$), and Bus Bandwidth ($B$).
  - *3.4.2 Operating Point Selection:* Selecting perception cadences (e.g. 720p @ 60 Hz vs. 4K @ 10 Hz) tied directly to dynamic world deadlines ($\tau_{\text{world}}$).
  - *3.4.3 Graceful Degradation under Thermal/Bus Saturation:* Automatically dropping resolution or frame rates when NPU thermal throttling or bus contention occurs.
- **3.5 PTP Timestamping and Observation Contracts**
  - *3.5.1 Microsecond Hardware Timestamping (IEEE 1588 PTP):* Stamping data at the physical sensor hardware clock to align multi-modal streams.
  - *3.5.2 Missing-Frame & Dropout Fallbacks:* Deterministic software fallbacks when sensor frames drop or arrive out of order.
  - *3.5.3 Formalizing `Observation Contract`:* Binary schema specifying sensor IDs, cadences, resolution, PTP hardware timestamp offset, latency bounds, and fallback triggers.

#### Chapter 3 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** Ingestion latency vs. pixel resolution, ViT patch count vs. SRAM footprint, PTP hardware timestamping overhead.
2. **Dossier Delta:** Freeze `Observation Contract`.
3. **Systems Fallacies:** "Higher resolution is always better", "Software timestamps are fine".
4. **Downstream Handoff:** Pass `Observation Contract` to Chapter 4 (*State Estimation and Temporal Belief*).

---

### Chapter 4 — State Estimation and Temporal Belief

**Opening Question:** What must the system believe right now when every observation describes a different place and time?

**Objective:** Given timestamped observations, the reader can transform discrete sensor readings into a continuous, time-indexed spatial belief, synchronize multi-sensor clocks, track proprioception/interoception health, and manage uncertainty horizons.

#### Section Blueprints
- **4.1 Sensor Samples vs. Maintained State**
  - *4.1.1 Raw Observations vs. Continuous Temporal Belief:* Why discrete sensor readings must be transformed into continuous belief states via prediction buffers.
  - *4.1.2 Continuous State Prediction Buffers:* Integrating physical motion models to estimate state $S(t_{\text{now}})$ between discrete sensor updates.
  - *4.1.3 Transport Delay & Observation Lag:* Managing state estimation when visual frames arrive 50ms late.
- **4.2 Spatial Frame Graphs and Clock Synchronization**
  - *4.2.1 Coordinate Frame Transformations ($SE(3)$ Trees & Lie Algebra $\mathfrak{se}(3)$):* Mapping camera frame $\rightarrow$ end-effector frame $\rightarrow$ body frame $\rightarrow$ world frame ($SE(3)$ transformations). Using Lie algebra ($\mathfrak{se}(3)$) tangent space integration to avoid gimbal lock singularities cleanly.
  - *4.2.2 PTP Clock Synchronization (IEEE 1588):* Preventing timestamp skew ($\Delta t_{\text{skew}}$) from introducing artificial velocity errors ($v_{\text{err}} \approx a \cdot \Delta t_{\text{skew}}$).
  - *4.2.3 Transform Lookup Overhead:* Efficient frame graph lookup without transform interpolation error.
- **4.3 Predict-Observe-Correct Estimator Loops (Systems View)**
  - *4.3.1 Intuitive 3-Step Estimator Cycle:* Predict $\rightarrow$ Observe $\rightarrow$ Correct without dense academic matrix derivations.
  - *4.3.2 Innovation Residuals as Disagreement Detectors:* Using residuals ($y = z - h(\hat{x})$) to spot sensor glare, blockage, or failure.
  - *4.3.3 Out-of-Sequence Measurement (OOSM) Buffering:* Rewinding state history buffers for late-arriving frames without stalling control threads.
- **4.4 Proprioceptive State and Kinematic-Thermal Limits**
  - *4.4.1 Proprioceptive State Tracking:* Motor encoders, joint positions, velocities, torques, and tactile forces.
  - *4.4.2 Interoceptive Hardware Health:* Motor winding temperatures, bus voltage sag, phase currents, and mechanical strain.
  - *4.4.3 Dynamic Thermal Derating:* Dynamic torque limit derating ($\tau_{\text{max}}(T)$) before thermal runaway damages motor windings.
- **4.5 State Schemas, Validity Horizons, and Drift Triggers**
  - *4.5.1 Time-Indexed State Schemas:* Binary schema for pose, velocity, orientation, covariance, and timestamp $t_{\text{stamp}}$.
  - *4.5.2 State Validity Horizons (TTL Leases):* Invalidate state belief if no new sensor evidence arrives within $\tau_{\text{TTL}}$.
  - *4.5.3 Drift Triggers & Resynchronization Rules:* Triggering state drift alarms when spatial uncertainty exceeds physical task limits (`State, Frames & Timing Model`).

#### Chapter 4 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** Prediction buffer history depth vs. Memory overhead, PTP sync frequency vs. Network bus load, State TTL validity window vs. Re-calibration cadence.
2. **Dossier Delta:** Freeze `State, Frames & Timing Model`.
3. **Systems Fallacy & Pitfall Audit:**
   - *Fallacy 1:* "The latest sensor reading is the current physical state."
   - *Fallacy 2:* "A neural context window acts as a spatial world model."
4. **Downstream Handoff:** Pass `State Model` to Chapter 5 (*Semantic Reasoning and Intent Proposals*).

---

## PART III: Deliberate, Plan & Enforce (Chapters 5–7)

> **Part Role Declaration:**  
> *"The role of Part III is to close the sense-to-actuation loop—structuring slow System 2 semantic reasoning into expiring intent proposals, unrolling VLA trajectory action chunks, and shielding the machine with fast System 1 MCU safety vetoes."*

- **Chapters:** Chapter 5 (*Semantic Reasoning and Intent Proposals*), Chapter 6 (*Policy Interfaces and Action Chunks*), & Chapter 7 (*Real-Time Action Enforcement*).
- **Pipeline Stages:** **Stage 4 (Reasoning)** $\rightarrow$ **Stage 5 (Planning)** $\rightarrow$ **Stage 6 (Action & Safety Enforcement)**.
- **Dossier Deliverables:** `Policy Interface & Intent Schema` (Ch 5) $\longrightarrow$ `Planning Schema` (Ch 6) $\longrightarrow$ `Action Limits & Enforcement Design` (Ch 7).

---

### Chapter 5 — Semantic Reasoning and Intent Proposals (System 2 Cortex)

**Opening Question:** How does a vision-language model reason about an open-ended scene without taking unchecked, direct control of physical motors?

**Objective:** Given maintained state belief and a VLM, the reader can structure semantic reasoning into expiring intent proposals with explicit spatial 3D bounds and validity leases.

#### Section Blueprints
- **5.1 Grounding Open-Vocabulary Goals to 3D Physical Affordances**
  - *5.1.1 From Words to Coordinates:* Anchoring natural language instructions ("pick up the red mug") to explicit 3D spatial frames ($SE(3)$), physical object bounding volumes, and tool approach vectors.
  - *5.1.2 Affordance Grids & Contact Constraints:* Identifying valid grasp points and contact surfaces on physical objects before motion generation begins.
  - *5.1.3 Semantic Ambiguity Resolution:* Handling ambiguous instructions ("hand me that thing") using visual grounding and scene spatial relations.
- **5.2 Vision-Language Models as Asynchronous Proposal Services**
  - *5.2.1 The VLM Execution Profile:* Characterizing VLM inference latency ($100\text{--}2000\text{ ms}$), token generation overhead, and edge accelerator power draw (50–300W).
  - *5.2.2 Untrusted Proposal Service Model:* Why VLMs must be treated as asynchronous proposal generators rather than direct motor controllers.
  - *5.2.3 Context Window Management:* Managing multimodal context windows to prevent token growth from bloating inference latency.
  - *5.2.4 Autoregressive Memory Bandwidth Saturation:* Modeling KV-cache DRAM memory footprint and LPDDR5 memory bus saturation during multi-token VLM decoding on UMA edge SoCs.
- **5.3 Task Goal Binding to Physical Embodiment Capabilities**
  - *5.3.1 Morphological Kinematic Validation:* Validating VLM proposals against robot morphology, reachability limits, and arm Inverse Kinematics (IK) feasibility.
  - *5.3.2 Payload & Static Equilibrium Checks:* Checking whether the embodiment can physically lift or manipulate the targeted object mass.
  - *5.3.3 Binding to Primitive Motor Skills:* Resolving high-level semantic intent into sequences of named low-level skill primitives (`Grasp`, `MoveTo`, `Place`).
- **5.4 Asynchronous Reasoning vs. Real-Time Execution**
  - *5.4.1 Multi-Rate Decoupling Architecture:* Running deliberative VLM reasoning ($\le 1-5\text{ Hz}$) on MPU/Cloud asynchronously decoupled from fast motor execution ($100-1000\text{ Hz}$).
  - *5.4.2 Non-Blocking Proposal Queues & Speculative Intent Buffers:* Using lock-free IPC queues and speculative intent buffers to insulate downstream VLA planning from VLM tail latency jitter ($100-2000\text{ ms}$).
  - *5.4.3 Handling Mid-Task Scene Drift:* Updating or invalidating intent proposals when the physical scene changes during VLM token generation.
- **5.5 Expiring Intent Proposal Schemas and Abstention**
  - *5.5.1 Time-Bounded Intent Leases:* Encapsulating proposals into expiring leases specifying target 3D bounding boxes, maximum velocity limits, and expiration timestamps ($t_{\text{expire}}$).
  - *5.5.2 Intent Validity Horizon Rules:* Automatically invalidating intent proposals if execution has not commenced before lease expiration.
  - *5.5.3 Explicit Model Abstention & Fallbacks:* Structuring confidence thresholds ($p_{\text{confidence}} < \gamma$) where the model explicitly abstains and requests clarification or triggers a safe hold (`Policy Interface & Intent Schema`).
  - *5.5.4 Autoregressive Tail Latency Bounding & Token Preemption:* Decoupling Time-to-First-Token (TTFT) and Time-Per-Output-Token (TPOT) tail metrics; enforcing hard execution preemption when generation latency approaches lease expiration ($t_{\text{expire}}$).

#### Chapter 5 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** VLM reasoning depth vs. proposal cadence, spatial grounding precision vs. vocabulary flexibility, intent lease duration vs. replanning rate.
2. **Dossier Delta:** Freeze `Policy Interface & Intent Schema`.
3. **Systems Fallacies:** "VLMs are physically grounded out of the box", "VLM token generation is fast enough for direct motor control".
4. **Downstream Handoff:** Pass `Intent Schema` to Chapter 6 (*Policy Interfaces and Action Chunks*).

---

### Chapter 6 — Policy Interfaces and Action Chunks (VLA Planning)

**Opening Question:** How do vision-action models generate smooth physical trajectories instead of jerky single-step moves?

**Objective:** Given expiring intent leases and state belief, the reader can structure VLA policy interfaces, unroll multi-step action chunks ($H$-step horizons), and manage asynchronous replanning continuity.

#### Section Blueprints
- **6.1 Vision-Language-Action Policies & Trajectory Rollouts**
  - *6.1.1 VLA Model Architecture:* Mapping visual tokens and intent leases directly into multi-dimensional spatial-temporal trajectory rollouts (Diffusion Policy, ACT).
  - *6.1.2 Mid-Frequency Execution Cadence:* Operating VLA trajectory generators at mid-frequencies ($10-50\text{ Hz}$) on neural processing units (NPUs).
  - *6.1.3 Trajectory Representation:* Representing trajectories as continuous spatial curves rather than discrete step-by-step motor commands.
  - *6.1.4 NPU SRAM vs DRAM Execution for Action Diffusion Policies:* Profiling weight-loading bandwidth vs SRAM double-buffering during $H$-step diffusion/ACT trajectory unrolling.
- **6.2 Joint Space vs. Task Space vs. Skill Primitives**
  - *6.2.1 Task-Space Cartesian Control:* Outputting end-effector target vectors $(x, y, z, \text{roll}, \text{pitch}, \text{yaw}, F_{\text{grasp}})$; trade-offs in cross-robot transferability vs. singularity risk.
  - *6.2.2 Joint-Space Angle Control:* Outputting direct motor joint angles $(q_1, q_2, \dots, q_n)$; trade-offs in embodiment specificity vs. dynamic stability.
  - *6.2.3 Jacobian Singularity Handling:* Matrix condition number checks ($\kappa(J)$) to prevent joint velocity saturation near kinematic singularities.
- **6.3 Action Decoders and Multi-Step Chunk Horizons ($H$)**
  - *6.3.1 Multi-Step Action Chunking ($H$-step horizons):* Predicting a sequence of $H$ future action steps per inference pass to bridge neural inference latency.
  - *6.3.2 Chunk Horizon Length ($H$) Trade-offs:* Short chunks (high responsiveness, high inference load) vs. Long chunks (open-loop execution drift risk).
  - *6.3.3 Overlapping Receding Horizon Buffers:* Maintaining receding action buffers where new chunks overlap with executing trajectories.
  - *6.3.4 Cumulative Information Age ($\Delta t_{\text{total}}$) Formulation:* Formalizing cumulative age decay $\Delta t_{\text{total}} = \Delta t_{\text{sensing}} + \Delta t_{\text{perception}} + \Delta t_{\text{state}} + P_{99}(t_{\text{inference}})$ and quantifying its expansion of initial trajectory safety margins.
- **6.4 Asynchronous Replanning & State Re-Anchoring Handshake**
  - *6.4.1 Temporal Ensembling & Chunk Blending:* Blending overlapping action chunks ($\alpha(t) a_k(t) + (1-\alpha(t)) a_{k-1}(t)$) to eliminate acceleration/jerk discontinuities between inference passes.
  - *6.4.2 Acceleration & Jerk Continuity ($\mathcal{C}^2$ Smoothing):* Enforcing smooth position, velocity, and acceleration profiles to prevent motor gearbox mechanical shock.
  - *6.4.3 Asynchronous State Re-Anchoring Handshake:* When an MCU safety veto occurs in Ch 7, the MPU policy buffer instantly clears stale trajectory continuation steps and re-anchors its planning horizon to the MCU's active fallback position.
  - *6.4.4 Re-Anchoring State Machine & Buffer Flush:* Formalizing the state machine for clearing stale MPU action chunk buffers, re-synchronizing baseline PTP timestamps, and resetting VLA policy initial conditions to MCU active fallback states upon safety veto.
- **6.5 Policy Cards and Trajectory Contract Schemas**
  - *6.5.1 Standardized Policy Cards:* Documenting policy operational bounds, trained environmental domains, maximum action derivatives, and verified workspace envelopes.
  - *6.5.2 Trajectory Contract Schemas:* Structuring trajectory payloads with explicit derivative limits (velocity $\|\dot{x}\| \le v_{\text{limit}}$, acceleration $\|\ddot{x}\| \le a_{\text{limit}}$, jerk $\|\dddot{x}\| \le j_{\text{limit}}$).
  - *6.5.3 Policy Interface Handoff to MCU Enforcers:* Passing trajectory contracts to Chapter 7 for real-time safety veto validation (`Planning & Trajectory Schema`).

#### Chapter 6 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** Action chunk horizon $H$ vs. open-loop drift, task-space vs. joint-space output representation, temporal ensembling smoothness vs. reaction latency.
2. **Dossier Delta:** Freeze `Planning & Trajectory Schema`.
3. **Systems Fallacies:** "Policies should output single discrete motor steps", "VLA trajectory rollouts don't need joint velocity smoothing".
4. **Downstream Handoff:** Pass `Planning Contract` to Chapter 7 (*Real-Time Action Enforcement*).

---

### Chapter 7 — Real-Time Action Enforcement (System 1 MCU Reflex)

**Opening Question:** What mechanism separates a capable policy proposal from permission to move physical actuators?

**Objective:** Given proposed trajectory chunks, the reader can design independent MCU safety enforcers, calculate dynamic stopping bounds ($d_{\text{stop}}$), and define physical fallbacks.

#### Section Blueprints
- **7.1 The Proposal-Permission Split (SoC vs. MCU Boundary)**
  - *7.1.1 Decoupling Authority from Intelligence:* Establishing the fundamental safety rule: neural models (MPU/SoC) propose trajectories; independent real-time controllers (MCU) permit or veto execution.
  - *7.1.2 Hardware Memory & Bus Decoupling Invariants:* Running safety enforcers on dedicated microcontroller hardware (Cortex-M / RISC-V RTOS) isolated from Linux application processor kernel panics, GPU throttling, and shared memory bus contention via hardware MPUs/PMPs and non-blocking bus queues (isolated SPI/RPMSG).
  - *7.1.3 Heartbeat & Watchdog Protocols:* Hardened IPC heartbeat monitoring ($\tau_{\text{watchdog}} \in [10\text{ms}, 50\text{ms}]$) between host SoC and MCU enforcer.
  - *7.1.4 Zero-Copy Shared Memory IPC Substrate:* Structuring dual-port SRAM, RPMSG buffers, and PCIe Endpoint doorbell queues between host Linux MPU and RTOS MCU to transmit trajectory action chunks without CPU cache invalidation or memory copy jitter.
- **7.2 Dynamic Stopping Bounds ($d_{\text{stop}}$) and Skill Limits**
  - *7.2.1 Dynamic Stopping Distance Physics:* Continuous calculation of stopping bounds incorporating dynamic latency jitter: $d_{\text{stop}}(t) = v \cdot t_{\text{delay}}(t) + \frac{v^2}{2 a_{\text{decel\_max}}}$, where $t_{\text{delay}}(t) = t_{\text{transduce}} + \Delta t_{\text{age}}(t) + t_{\text{comm}} + t_{\text{enforce}} + t_{\text{actuator\_response}}$.
  - *7.2.2 Workspace Geofencing & Velocity Envelopes:* Dynamic workspace boundary enforcement and speed derating based on distance to physical obstacles.
  - *7.2.3 Jerk-Limited Deceleration Profiles:* Calculating maximum safe deceleration profiles without causing structural tipping or mechanical damage.
- **7.3 Independent Real-Time Safety Enforcers on MCU**
  - *7.3.1 Bare-Metal / RTOS vs Time-Triggered Architecture (TTA):* Building zero-allocation, deterministic safety check loops running at $1000\text{ Hz}$ on MCU hardware; evaluating Time-Triggered static cyclic executives vs. preemptive RTOS for ASIL-D / SIL 3 safety channels.
  - *7.3.2 Safety Filter Invariants:* Checking trajectory proposals against hard physical constraints ($\|v\| \le v_{\text{max}}$, $\|a\| \le a_{\text{max}}$, joint torque limits, workspace bounds).
  - *7.3.3 Real-Time Veto Logic:* Instantly overriding or clipping candidate action vectors that violate safety invariants and triggering the asynchronous re-anchoring handshake back to Ch 6.
- **7.4 Physical Fallbacks: Stop, Position Hold, and Retreat**
  - *7.4.1 Standardized Fallback Escalation State Machines (IEC 60204-1 / ISO 13850):* Defining safe physical fallback modes upon proposal veto or heartbeat loss: Category 0 Stop (uncontrolled power cut), Category 1 Stop (controlled dynamic braking), Category 2 Stop (position hold); enforcing deterministic thermal escalation triggers (Cat 2 position hold $\xrightarrow{T > T_{\text{limit}}}$ Cat 1 dynamic brake $\xrightarrow{\text{brake fail}}$ Cat 0 power cut).
  - *7.4.2 Active Position Hold & Impedance Control:* Holding joint positions under external disturbance forces without exceeding motor thermal limits.
  - *7.4.3 Safe Retreat Trajectories:* Executing deterministic backward retreat paths away from physical contact zones.
- **7.5 Skill Envelopes and Safety Veto Logic**
  - *7.5.1 Skill Envelope Formalization:* Wrapping motor skills (`Grasp`, `Move`, `Push`) with checkable parameter bounds and dynamic safety envelopes.
  - *7.5.2 Control Barrier Invariants:* Intuitive safety barrier conditions ($h(x) \ge 0$) guaranteeing the system state remains within safe physical bounds.
  - *7.5.3 Completing the Proposal-Permission Architecture:* Freezing `Action Limits & Enforcement Design` as the complete real-time safety shield.

#### Chapter 7 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** MCU safety check rate vs. CPU overhead, stopping distance conservatism vs. execution speed, fallback response speed vs. mechanical shock.
2. **Dossier Delta:** Freeze `Action Limits & Enforcement Design`.
3. **Systems Fallacies:** "Software clipping on host Linux is sufficient safety", "Neural policies can learn implicit physical safety limits".
4. **Downstream Handoff:** Pass `Enforcement Design` to Chapter 8 (*Heterogeneous System Placement*).

---

## PART IV: Place, Govern & Assure (Chapters 8–10)

> **Part Role Declaration:**  
> *"The role of Part IV is to transform the physical AI system into an engineered, production-ready product—mapping execution across heterogeneous hardware, governing data flywheels and human authority, and assembling the evidence case for release."*

- **Chapters:** Chapter 8 (*Heterogeneous System Placement*), Chapter 9 (*Interaction Trajectories and Human Authority*), & Chapter 10 (*System Qualification and Release Assurance*).
- **Pipeline Stages:** **Stage 7 (Learn & Governance)** $\rightarrow$ **Hardware System Placement** $\rightarrow$ **System Qualification & Release Verdict**.
- **Dossier Deliverables:** `Placement Map & Ledger` (Ch 8) $\longrightarrow$ `Human-Authority Map` (Ch 9) $\longrightarrow$ `Integrated Deployment Case` (Ch 10).

---

### Chapter 8 — Heterogeneous System Placement (Hardware Mapping)

**Opening Question:** Where should each stage run when compute, memory, energy, and thermal budgets are shared across heterogeneous hardware nodes?

**Objective:** Given the 7 canonical stages and hardware node specifications (MCU, MPU, NPU, Cloud), the reader can map workloads, budget memory DMA and interconnect buses, enforce failure domain isolation, and construct a whole-system resource ledger.

#### Section Blueprints
- **8.1 Multi-Rate Sensing and Actuation Loop Dataflow Mapping**
  - *8.1.1 End-to-End Multi-Rate Mapping:* Mapping dataflow across all 7 stages from sensor ingress to motor drive across heterogeneous processors.
  - *8.1.2 Rate Conversion Ring Buffers:* Managing rate transitions between 1000 Hz MCU control, 20 Hz NPU policy inference, and 1 Hz Cloud VLM planning.
  - *8.1.3 Interconnect Scheduling:* Budgeting bus latencies across CAN-FD, EtherCAT, PCIe, and Wi-Fi/5G networks.
- **8.2 Compute Domain Partitioning: MCU, MPU, NPU, and Cloud**
  - *8.2.1 Microcontroller Domain (MCU):* Bare-metal/FreeRTOS, SRAM execution, zero OS paging jitter, sub-millisecond determinism (Stage 6 Enforcement).
  - *8.2.2 Application Processor Domain (MPU):* Linux/ROS2, virtual memory, high compute throughput, non-deterministic OS scheduling (Stage 3 State & Stage 5 Planning).
  - *8.2.3 Neural Accelerator (NPU) & Cloud Offloading:* Matrix acceleration for vision encoders (Stage 2) and off-board VLM reasoning (Stage 4).
- **8.3 Data Movement, Hardware DMA, and Shared Bus Arbitration**
  - *8.3.1 Bus Contention Modeling:* Analyzing AXI/PCIe memory bus saturation when high-resolution cameras stream frames alongside NPU tensor fetches.
  - *8.3.2 Hardware DMA Channel & IPC Shared SRAM Allocation:* Allocating dedicated DMA channels and RPMSG shared SRAM buffers for zero-copy sensory ingestion and trajectory transfers.
  - *8.3.3 Interconnect QoS Priority Schemes:* Enforcing Quality-of-Service (QoS) priorities to ensure sensory data never starves motor control commands.
- **8.4 Failure Isolation, Trust Boundaries, and Safe Fallback Hardware**
  - *8.4.1 Hardware Failure Domain Isolation:* Enforcing physical, memory, and bus isolation (ARM MPU / RISC-V PMP, dual-core lockstep MCUs) between untrusted AI software and safety controllers.
  - *8.4.2 Hardware Watchdogs & Heartbeat Relays:* Independent hardware watchdogs that automatically trigger dynamic braking when application processors hang.
  - *8.4.3 Thermal & Power Budget Distribution:* Allocating thermal TDP (Watts) and electrical current draw across heterogeneous compute nodes under battery constraints.
- **8.5 Hardware Placement Maps and Shared Resource Budget Ledgers**
  - *8.5.1 Multi-Resource Ledger Accounting:* Constructing whole-system budget tables balancing FLOPs, SRAM/DRAM bytes, interconnect bandwidth (GB/s), power (W), thermal TDP, and latency slack.
  - *8.5.2 Mapping Optimization Trade-offs:* Evaluating edge-only vs. edge-cloud hybrid placement tradeoffs.
  - *8.5.3 Formalizing `Placement Map & Resource Ledger`:* Schema locking component placement, bus assignments, and resource allocations (`Placement Ledger`).

#### Chapter 8 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** On-device vs. Cloud offloading latency, SRAM vs. DRAM allocation, bus QoS priority assignments.
2. **Dossier Delta:** Freeze `Placement Map & Resource Ledger`.
3. **Systems Fallacies:** "System components can be optimized independently", "'On-device' implies a single homogeneous chip".
4. **Downstream Handoff:** Pass `Placement Ledger` to Chapter 9 (*Interaction Trajectories and Human Authority*).

---

### Chapter 9 — Interaction Trajectories and Human Authority (Stage 7 Deep-Dive)

**Opening Question:** Who has the right to approve, override, or change what the machine does, and how is physical experience converted to governed data?

**Objective:** Given physical operational records, the reader can structure hardware-synchronized PTP log schemas, manage policy endogeneity/selection bias, engineer bumpless human override handoffs, and manage OTA rollback pipelines.

#### Section Blueprints
- **9.1 Interaction Trajectories and Hardware-Synchronized Log Schemas**
  - *9.1.1 Microsecond PTP Logging (IEEE 1588):* High-frequency binary logging (FlatBuffers/Protobuf) aligning multi-modal sensor streams, internal belief states, neural proposals, MCU vetoes, and human inputs under PTP timestamps.
  - *9.1.2 Ring-Buffer Logging & I/O Bandwidth:* Managing zero-copy logging buffers without saturating local flash storage I/O or stealing memory bus bandwidth from control loops.
  - *9.1.3 Trajectory Episode Schemas:* Structuring full interaction episodes ($O_0, S_0, P_0, A_0, W_1, O_1, \dots, \text{Outcome}$).
- **9.2 Policy Endogeneity, Covariate Shift, and Truncated Episode Tagging**
  - *9.2.1 Policy Endogeneity (Feedback Loops in Data):* How active policy actions dictate future state exposure, creating endogenous feedback loops in logged datasets.
  - *9.2.2 Intervention Selection Bias & Truncated Episode Tagging:* Why naive training on human intervention logs suffers from severe covariate shift. Cryptographically tagging human/MCU intervention logs as "overridden/truncated episodes" so offline behavioral cloning (BC) models do not fit weights to truncated non-nominal transitions.
  - *9.2.3 Mid-Chunk Action Truncation Slicing Protocol:* Formalizing sub-sequence slicing when an MCU safety veto or human override occurs mid-chunk ($H$-step), specifying how partially executed chunks are truncated in log headers so offline datasets stay pristine.
  - *9.2.4 Counterfactual Trajectory Modeling:* Techniques for filtering and weighting intervention logs to prevent policy collapse during re-training.
- **9.3 Trajectory Curation and Hardware Dataset Provenance**
  - *9.3.1 Automated Data Curation Pipelines:* Filtering redundant nominal operations; extracting high-value informative snippets (uncertainty spikes, tracking errors, human takeovers).
  - *9.3.2 Cryptographic Hardware Provenance:* Embedding immutable metadata hashes (robot serial, sensor calibration matrices, ECU firmware IDs, Git commit) into log headers.
  - *9.3.3 Dataset Versioning & Consent Boundaries:* Managing data governance, privacy masking, consent boundaries, and dataset release versioning.
- **9.4 Human Intervention, Bumpless Control Overrides, and Authority Revocation**
  - *9.4.1 Authority Handoff State Machines:* Structuring control switching between autonomous policy commands and human supervisory inputs (joystick, teleoperation, physical E-stop).
  - *9.4.2 Bumpless Transfer & Jerk-Limited Blending:* Rate-limiting filters and state-space blending to prevent mechanical actuator transients during authority handoffs.
  - *9.4.3 Instant Authority Revocation:* Instantaneous hardware-level override revocation mechanics when human safety limits are crossed.
- **9.5 Field Policy Qualification, Shadow Execution, and Instant Rollback**
  - *9.5.1 Passive Shadow Mode Execution:* Deploying candidate neural policies in shadow mode alongside active baseline controllers to score discrepancies on live hardware without risk.
  - *9.5.2 Dual-Bank OTA Memory Rollback Pipelines:* Dual-bank flash memory architecture allowing instant, automated hardware rollback to verified baseline firmware upon anomaly detection.
  - *9.5.3 Formalizing `Human-Authority & Governed Data Record`:* Schema locking human override rights, logging rules, and OTA rollback gates (`Governance Record`).

#### Chapter 9 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** Logging bandwidth vs. storage I/O, intervention filtering vs. sample diversity, shadow mode evaluation duration vs. deployment cadence.
2. **Dossier Delta:** Freeze `Human-Authority & Governed Data Record`.
3. **Systems Fallacies:** "Logged physical data is automatically useful training data", "Human-in-the-loop guarantees safe control without bumpless transfer filters".
4. **Downstream Handoff:** Pass `Governance Record` to Chapter 10 (*System Qualification and Release Assurance*).

---

### Chapter 10 — System Qualification and Release Assurance (Release Verdict)

**Opening Question:** What evidence is sufficient to accept responsibility for releasing this physical AI system into the physical world?

**Objective:** Given the complete physical AI system and cumulative design dossier, the reader can specify target operational envelopes (ODD), execute multi-rung SIM/HIL qualification ladders, inject cross-layer hardware/software faults, build Claim-Argument-Evidence (CAE/GSN) safety cases, and render an evidence-backed release verdict.

#### Section Blueprints
- **10.1 Target Deployment Envelope (ODD) Specifications**
  - *10.1.1 Formal Operational Design Domain (ODD) Specs (ISO 22736):* Defining precise physical boundary matrices: speed limits, friction coefficients ($\mu$), illumination (lux), weather limits, temperature ranges, and terrain gradients.
  - *10.1.2 Real-Time Out-of-Envelope Monitors:* Runtime boundary checking logic that detects when the physical machine is exiting its certified ODD.
  - *10.1.3 Exclusions & Misuse Boundaries:* Explicitly documenting un-certified operating conditions and expected human misuse scenarios.
- **10.2 Qualification Ladders: Replay, Simulation, HIL, and Live Shadow**
  - *10.2.1 The 4-Rung Qualification Ladder:*
    - *Rung 1 (Offline Log Replay):* Testing candidate policies against historical trajectory datasets.
    - *Rung 2 (Closed-Loop SIM):* Testing policies in high-fidelity physics simulators (Isaac Sim, Gazebo).
    - *Rung 3 (Hardware-in-the-Loop - HIL):* Interfacing real ECUs, MCUs, and NPUs with real-time plant simulators over physical CAN-FD/EtherCAT buses.
    - *Rung 4 (Live Shadow Execution):* Running candidate models passively on physical hardware in production.
  - *10.2.2 Quantitative Promotion & Exit Gates:* Setting strict, automated CI/CD entry and exit metrics required to promote a model to the next ladder rung.
  - *10.2.3 Sim-to-Real Gap Metrics:* Measuring domain gap divergence between physics simulation and real-world HIL test benches.
- **10.3 STPA Hazard Analysis and Empirical Evidence Mapping**
  - *10.3.1 STPA Control Structure Analysis (ISO 21448 / SOTIF):* Mapping Systems-Theoretic Process Analysis (STPA) to non-deterministic perception and control loops.
  - *10.3.2 Unsafe Control Action (UCA) Identification:* Cataloging potential UCAs (e.g. command issued too late, stopped too early, un-shielded trajectory).
  - *10.3.3 100% Traceability Matrices:* Building bidirectional matrices linking every identified hazard directly to automated test evidence records.
- **10.4 Physical Fault Injection and Failure Coverage Analysis**
  - *10.4.1 Cross-Layer Fault Injection Test Suites & PTP Drift:*
    - *Physical/Hardware Layer:* Voltage sags, power-rail brownout resets (BOR) under peak NPU/motor loads, PTP grandmaster clock drift/jitter injection, CAN packet corruption, sensor unplugging, frame dropping, memory bit flips.
    - *Model/Software Layer:* Adversarial noise injection, latency spikes, corrupted intent proposals, frozen MPU threads.
  - *10.4.2 Hardware Disturbance Nodes & Injection Rigs:* Building hardware test rigs that physically inject fault states into sensor buses and power rails.
  - *10.4.3 Failure Coverage & Residual Risk Metrics:* Quantifying empirical failure coverage percentages and residual risk bounds.
- **10.5 Claim-Argument-Evidence Safety Cases and Release Verdicts**
  - *10.5.1 Goal Structuring Notation (GSN) / CAE Safety Cases:* Assembling formal safety case trees linking top-level claims (*"System X is safe for deployment within ODD Y"*) to sub-arguments backed by empirical HIL/SIM test evidence.
  - *10.5.2 Rendering Defensible Release Verdicts under Quantitative Targets:* Mapping GSN/CAE release verdicts to quantitative target thresholds (e.g. Probability of Dangerous Failure per Hour $PFH \le 10^{-7}$, $MTTF_d$, SIL 3 / AgPL d/e targets) to render explicit deployment verdicts: **Deploy**, **Condition** (deploy with restricted ODD bounds), or **Refuse** (reject release due to evidence gaps).
  - *10.5.3 Completing the Cumulative Design Dossier:* Freezing the final `Integrated Deployment Case` artifact.

#### Chapter 10 Systems Synthesis & Decision Handoff
1. **Executive Trade-off Table:** HIL test rig fidelity vs. qualification cost, ODD scope vs. evidence complexity, release velocity vs. safety case completeness.
2. **Dossier Delta:** Freeze final `Integrated Deployment Case`.
3. **Systems Fallacies:** "A successful video demo proves deployment readiness", "High simulation performance guarantees real-world safety".
4. **Downstream Handoff:** System is qualified and released! Transfer to Unnumbered Capstone for summative design defense!

---

## Unnumbered Capstone — Final Design Review & System Defense

The summative transfer assessment. The reader defends their complete **Cumulative Design Dossier**, diagnoses a seeded hardware/software failure using *Hypothesis $\rightarrow$ Bisect $\rightarrow$ Confirm*, adapts their system to an unfamiliar physical embodiment, and defends their **Deploy / Condition / Refuse** release verdict before an expert review panel.
