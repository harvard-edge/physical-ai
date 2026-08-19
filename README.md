# Physical AI Systems: Machine Learning Systems That Sense and Act

**An Open Textbook, Curriculum, and Hardware Studio on Engineering Autonomous Physical Agents**

* **Author & Lecturer:** **Prof. Vijay Janapa Reddi** (Harvard University / Visiting Professor, ETH Zurich)
* **Kit & Studio Lead:** **Dr. Andrea Mattia Garavagno** (Integrated Systems Laboratory, IIS, D-ITET, ETH Zurich)
* **Book & Course Portal:** [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai)

> *"TinyML taught you how to deploy a neural model to a microchip. Physical AI teaches you how to build an intelligent, safe machine under physical and resource laws."*

---

## The Big Picture: What is Physical AI Systems?

Standard machine learning ends at digital output. A classifier emits a label; a large language model emits text. In the digital realm, errors are harmlessly contained behind glass: transactions roll back, exceptions are caught, and dropped packets are retried.

**Physical AI Systems begin at the exact moment digital software commands physical actuators—accelerating mass, consuming energy, and permanently altering the state of the world ($W_t \to W_{t+1}$).**

Because physical actions cannot be rewound (**you cannot `ctrl+z` kinetic momentum or Joule heat**), this textbook and course answer one central systems question:

> **"What must the surrounding system know, measure, enforce, preserve, and prove before an unverified learned proposal may produce a physical consequence?"**

---

## The Three Universal Defining Properties of Physical AI

Across robotics, autonomous mobility, smart energy grids, and industrial automation, an engineered system is defined as **Physical AI** if and only if it satisfies three universal criteria:

| Property | Core Physical & Computational Principle | Systems Reality & Contrast |
| :--- | :--- | :--- |
| **1. Learned Foundation Component** | Incorporates high-capacity learned foundation models (Vision-Language-Action models, Latent World Models, Diffusion Policies) | Does not rely on rigid hardcoded if-then state machines; generalizes over unstructured, open-world environmental variability. |
| **2. Operations Across the Analog $\longleftrightarrow$ Digital Boundary** | Discrete software representations (tokens, embeddings, floating-point tensors) directly govern continuous analog energy fluxes | Digital clock ticks command 3-phase inverter MOSFETs, electromagnetic coil flux, hydraulic valves, and kinetic momentum. |
| **3. Governed by Irreversible Physical Laws** | Operates under strict physical conservation laws (conservation of energy, momentum $p=mv$, Joule heating $I^2R$, kinematic friction) | **Zero undo mechanism:** You cannot roll back a physical collision, rewind motor coil overheating, or catch a dropped glass with a software exception handler. |

: The Three Universal Defining Properties of Physical AI. {#tbl-defining-properties}

---

## The Three Canonical Archetypes

To ensure broad engineering generalization beyond any single robotics niche, every concept in this curriculum is anchored across **Three Canonical Archetypes** and a dedicated **Desk Bench Twin**:

| Archetype | Primary Physical Action | Representative Industrial Systems | Core Systems Challenge |
| :--- | :--- | :--- | :--- |
| **Archetype 1: Locomotion & Mobility** | Free-Space Movement & Spatial Navigation | Autonomous Vehicles (Waymo), High-Speed Delivery Drones (Skydio), Quadrupeds (Spot) | Tail latency ($P_{99}$) and dynamic stopping envelopes ($d_{\text{stop}}$) under high-speed kinetic momentum. |
| **Archetype 2: Contact Manipulation** | Touching, Shaping & Assembling Matter | Humanoid Robots (Optimus, Figure), 6-DoF Industrial Arms, Surgical Robots | Discontinuous contact transitions, torque rate limits ($\dot{\boldsymbol{\tau}}$), and harmonic drive gearbox shear. |
| **Archetype 3: Cybernetic Process & Energy** | Continuous State & Flow Regulation | Smart Grid Power Inverters, EV Battery Management Systems (BMS), Dialysis Pumps | Microsecond AC phase tracking, $I^2R$ Joule heating, and electrochemical thermal runaway prevention. |
| **The Desk Bench Twin (The Lab Kit)** | Precision Dual-Brain Desktop Pick-and-Place | **Arduino UNO Q Dual-Brain Kit** (Linux Application MPU + Cortex-M4 MCU + MIPI Camera) | Zero-magic laboratory realization grounding every architectural contract on real bench silicon. |

: The Three Canonical Archetypes and the Desk Bench Twin. {#tbl-canonical-archetypes}

---

## The Grand Systems Conflict: Less Time vs. More Time

The foundational tension of Physical AI is the structural collision between two opposing vectors:

```
                  THE FUNDAMENTAL TUG-OF-WAR IN PHYSICAL AI
                  
     PHYSICS & HARDWARE LAWS                 COGNITIVE FOUNDATION MODELS
     (Chapter 2: The Physical Columns)       (Chapter 3: The Cognitive Rows)
   ─────────────────────────────────────   ─────────────────────────────────────
   • LESS TIME IS BETTER ($t \to 0$)       • MORE TIME IS BETTER ($t \to \infty$)
   • Moving mass travels ($v \cdot \Delta t$)      • Foundation models need FLOPs & tokens
   • Stator coils heat ($I^2 R$)           • Spatial transformers need self-attention
   • Sensor evidence decays instantly      • Diffusion policies need denoising steps
   • Phase margin erodes ($e^{-s T_d}$)    • VLMs need chain-of-thought reasoning
   • "Act in 1 ms or the arm collides!"    • "Give me 500 ms to resolve ambiguity!"
```

### The Resolution: The Three Cadences of Intelligence

Physical AI reconciles this conflict by decoupling execution across **three asynchronous temporal cadences** hosted on heterogeneous silicon:

| Temporal Tier | Cadence & Frequency | Silicon Substrate | Operating System | Primary Systems Role | Privilege Tier |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **System 2: Semantic Deliberation** | $0.5\text{--}2\text{ Hz}$ ($500\text{--}2000\text{ ms}$) | Multi-Core Host (Linux MPU / Cloud) | Embedded Linux (`PREEMPT_RT`) | Open-world goal decomposition & VLM scene reasoning | **Untrusted Proposal Service** (Emits Expiring Intent Leases $\mathcal{L}_{\text{intent}}$) |
| **System 1.5: Trajectory Decoding** | $20\text{--}50\text{ Hz}$ ($20\text{--}50\text{ ms}$) | Edge NPU / Tensor Accelerator | Linux User Space (`SCHED_FIFO`) | Multi-step action chunking (ACT / Diffusion) & $\mathcal{C}^2$ jerk splines | **Candidate Trajectory Generator** (Emits $H=16$ Waypoint Chunks) |
| **System 1: Real-Time Reflex** | $1000\text{ Hz}$ ($1.0\text{ ms} \pm 5\,\mu\text{s}$) | Dedicated Bare-Metal MCU (Cortex-M4) | Bare-Metal / FreeRTOS (Static Memory) | 1 kHz Control Barrier Functions (CBF), dynamic stopping ($d_{\text{stop}}$), & $20\text{ kHz}$ FOC | **Sole Hardware Permission Authority** (Holds Inverter PWM Locks) |

: The Three Cadences of Intelligence. Decoupling cognitive speeds across heterogeneous silicon. {#tbl-three-cadences}

---

## The Grand Map: The Physical AI Co-Design Matrix

The curriculum and book are organized around the **$5 \times 4$ Co-Design Matrix**, formed by crossing the **Five Cognitive Work Dimensions (Chapter 3 Rows)** with the **Four Physical Constraints (Chapter 2 Columns)**:

| Cognitive Row | Column 1: Time & Freshness | Column 2: Inertia & Momentum | Column 3: Jerk & Thermal | Column 4: Silicon & Memory Bus | Owning Part II Chapter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Row 1: Perceive** | Optical exposure time & IEEE 1588 PTP sync | Motion blur smear bounds ($\Delta x = v \cdot t_{\text{exp}}$) | Rolling shutter angular shear compensation | $1.5\text{ GB/s}$ MIPI DMA DRAM bus ingestion tax | **Chapter 4** (`04-perception`) |
| **Row 2: Remember** | Latent belief age decay & TTL state leases | Occlusion spatial drift ($\sigma = \sigma_0 + v\Delta t$) | Stator winding thermal state memory ($I^2t$) | $SE(3)$ dynamic frame tree SRAM caching | **Chapter 5** (`05-state`) |
| **Row 3: Reason** | Slow 1 Hz MPU deliberation timeout containment | Kinematic reachability & workspace bounding $\mathcal{B}$ | Commanded speed clamps ($v_{\text{max}}$) in intent leases | Isolated MPU user-space proposal sandbox | **Chapter 6** (`06-intent`) |
| **Row 4: Plan** | Action Chunking delay amortization ($H=16$) | Multi-waypoint dynamic stopping profiles | $\mathcal{C}^2$ quintic splines bounding jerk ($\dddot{\mathbf{q}}$) | Lock-free shared SRAM ring buffers | **Chapter 7** (`07-planning`) |
| **Row 5: Execute** | Deterministic 1 kHz ($1.0\text{ ms}$) bare-metal tick | Dynamic stopping audit ($d_{\text{stop}} \le d_{\text{clear}}$) | Torque rate clamps ($\|\dot{\boldsymbol{\tau}}\| \le \dot{\tau}_{\text{max}}$) & $I_{\text{cont}}$ derating | **Zero dynamic heap allocation (`malloc = 0`)** | **Chapter 8** (`08-enforcement`) |

: The Physical AI Co-Design Matrix. Crossing the 5 cognitive rows against the 4 physical columns. {#tbl-codesign-matrix}

---

## The 4-Pillar Pedagogical Formula for Part II (Chapters 4–8)

Every chapter in Part II systematically conquers one row of the matrix using a standardized **4-Pillar Pedagogical Formula**:

1. **The Model Standpoint:** The machine learning representation, foundation model algorithm, and mathematical formulation (ViTs, latent JEPAs, VLMs, ACT/Diffusion, CBFs).
2. **The Silicon & System Substrate:** The physical execution target (MPU vs. NPU vs. MCU), DRAM crossbar contention, DMA memory channels, cache line invalidations, and allocation rules.
3. **The Timing Cadence & Multi-Rate Mapping:** The operational clock frequency, synchronization mechanisms (PTP exposure midpoints, delay amortization), and IPC mailboxes.
4. **The Physical Invariant & Safety Constraint:** The mathematical conservation laws, geometric bounds, and safety filters that prevent physical destruction.

---

## Textbook Structure & Cumulative Design Dossier

Across the 12 chapters, students and engineers construct an 11-artifact **Cumulative Design Dossier** for an embodied physical system:

| Part | Chapter | Title / Subsystem Focus | Design Dossier Deliverable | Companion Lab |
| :--- | :--- | :--- | :--- | :--- |
| **Part I: Foundations & Co-Design Matrix** | Chapter 1 | **The Causal Boundary & The Co-Design Challenge** | `LOOP-01` (Loop Charter & Invariants) | `labs/01-close-the-loop` |
| | Chapter 2 | **The Physical Constraints: Freshness, Stopping & Silicon** | `REQ-01` (Requirements & Latency Ledger) | `labs/02-metrology-wall` |
| | Chapter 3 | **The Cognitive Dimensions: The 5 Stages & Co-Design Matrix** | `FLOW-01` (Workflow & Multi-Rate Charter) | `labs/03-agent-workflow` |
| **Part II: The Embodied Lifecycle** | Chapter 4 | **Perception: Spatial Grounding & Ingestion Taxes** | `OBS-01` (Observation Contract & 3D Tokens) | `labs/04-dma-tokens` |
| | Chapter 5 | **Memory & State: Latent World Models & SE(3) Trees** | `STATE-01` (State & Timing Model) | `labs/05-latent-state` |
| | Chapter 6 | **Semantic Intent: Multimodal VLMs & Expiring Leases** | `INTENT-01` (Policy & Intent Schema) | `labs/06-vlm-intent` |
| | Chapter 7 | **Planning & Chunking: Diffusion Policies & C2 Jerk** | `PLAN-01` (Planning Schema & Chunking) | `labs/07-action-chunking` |
| | Chapter 8 | **Execution & Safety: 1 kHz MCU Safety Invariants** | `ENF-01` (Enforcement Design & CBFs) | `labs/08-cbf-enforcer` |
| **Part III: Placement, Governance & Release** | Chapter 9 | **Placement: Heterogeneous Silicon & Memory Bus QoS** | `PLACE-01` (Placement Map & Resource Ledger) | `labs/09-heterogeneous-placement` |
| | Chapter 10 | **Governance: Bumpless Transfer & Governed Flywheels** | `AUTH-01` (Authority & Governance Record) | `labs/10-bumpless-governance` |
| | Chapter 11 | **Assurance & Release: Seeded Faults & Safety Cases** | `REL-01` (Claim-Argument-Evidence Case) | `labs/11-fault-injection-rig` |
| **Capstone** | Chapter 12 | **Whole-System Bench Defense Under Seeded Faults** | **Full Dossier Sign-Off & Release Verdict** | `labs/99-capstone-defense` |

: The Complete 12-Chapter Textbook Curriculum and Cumulative Design Dossier Milestones. {#tbl-curriculum-dossier}

---

## Hardware Lab Track: The Arduino UNO Q Dual-Brain Kit

The laboratory track grounds every theoretical concept on zero-magic, reproducible bench hardware:

* **Host Brain (MPU):** Qualcomm Linux Application Processor running PyTorch, TensorRT, Vision-Language Models (VLMs), and ACT Action Chunk decoders.
* **Reflex Brain (MCU):** Dedicated ARM Cortex-M4 Microcontroller running bare-metal / FreeRTOS with strictly **zero dynamic heap allocation (`malloc = 0`)**, executing 1 kHz Control Barrier Functions and hardware emergency braking.
* **Sensory Suite:** MIPI CSI-2 camera with hardware DMA ring buffers, high-resolution optical encoders, and 6-DoF IMU.
* **Actuation Suite:** Multi-axis precision motion stage with phase current telemetry, thermal sensing, and hardware Safe Torque Off (STO) relays.

---

## Repository Structure

```text
PhysicalAI/
├── README.md               # Master course & textbook overview
├── NEXT_STEPS.md           # Engineering roadmap & active milestones
│
├── course/                 # Academic administration & syllabus
│   └── syllabus.md         # Official 14-week ETH Zurich syllabus (6 ECTS)
│
├── book/                   # Quarto publication source
│   ├── index.qmd           # Preface & Manifesto (3 Defining Properties, 3 Archetypes)
│   ├── chapters/           # 12 Chapter manuscripts (01-boundary through 99-capstone)
│   │   ├── 01-boundary/    # Chapter 1: The Causal Boundary
│   │   ├── 02-constraints/ # Chapter 2: The Physical Constraints (The Columns)
│   │   ├── 03-cognition/   # Chapter 3: The Cognitive Dimensions (The Rows)
│   │   ├── 04-perception/  # Chapter 4: Stage 1 — Perceive (Spatial Tokens & DMA)
│   │   ├── 05-state/       # Chapter 5: Stage 2 — Remember (Latent World Models)
│   │   ├── 06-intent/      # Chapter 6: Stage 3 — Reason (VLMs & Intent Leases)
│   │   ├── 07-planning/    # Chapter 7: Stage 4 — Plan (Diffusion Chunking & Jerk)
│   │   ├── 08-enforcement/ # Chapter 8: Stage 5 — Execute (1 kHz CBF Enforcers)
│   │   ├── 09-placement/   # Chapter 9: Workload Placement & Bus QoS
│   │   ├── 10-governance/  # Chapter 10: Human Authority & Data Flywheels
│   │   ├── 11-assurance/   # Chapter 11: Seeded Faults & Defensible Release
│   │   └── 99-capstone/    # Chapter 12: Whole-System Defense
│   ├── appendix/           # Dossier templates, hardware schematics & math reference
│   └── _quarto.yml         # Master Quarto configuration (Web + PDF LuaLaTeX)
│
└── labs/                   # Hands-on Dual-Brain Laboratory Track
    ├── 01-close-the-loop/  # Lab 1: Advisory open-loop vs closed-loop state mutation
    ├── 02-metrology-wall/  # Lab 2: Tail latency metrology (P99, P99.9) & stopping bounds
    ├── 03-agent-workflow/  # Lab 3: Multi-rate scheduling & proposal-permission split
    ├── 04-dma-tokens/      # Lab 4: MIPI DMA bus contention & 3D spatial tokenization
    ├── 05-latent-state/    # Lab 5: SE(3) frame trees & belief persistence under occlusion
    ├── 06-vlm-intent/      # Lab 6: VLM prompt grounding & expiring intent leases
    ├── 07-action-chunking/ # Lab 7: ACT trajectory decoding & C2 quintic jerk splines
    ├── 08-cbf-enforcer/    # Lab 8: 1 kHz MCU Control Barrier Function safety filtering
    ├── 09-heterogeneous-placement/ # Lab 9: UMA memory arbitration & thermal derating
    ├── 10-bumpless-governance/     # Lab 10: Bumpless joystick takeover & policy flywheels
    ├── 11-fault-injection-rig/     # Lab 11: Cross-layer seeded fault injection & safety cases
    └── 99-capstone-defense/        # Lab 12: Whole-system oral jury defense
```

---

## Building the Book

The book is authored in [Quarto](https://quarto.org) and compiles cleanly to both an interactive website and a publication-quality PDF via LuaLaTeX:

```bash
cd book

# 1. Live preview local web server with hot reload
quarto preview

# 2. Render complete HTML book and publication PDF
quarto render
```

---

## Teaching Team & Academic Credits

* **Prof. Vijay Janapa Reddi** — Author & Course Lecturer  
  *Gordon McKay Professor of Electrical Engineering, Harvard University*  
  *Visiting Professor, Integrated Systems Laboratory (IIS), D-ITET, ETH Zurich*  
  Email: [vjanapa@ethz.ch](mailto:vjanapa@ethz.ch) · Web: [Homepage](https://profvjreddi.github.io/homepage)

* **Dr. Andrea Mattia Garavagno** — Kit & Studio Lead / Co-Instructor  
  *Postdoctoral Researcher, Integrated Systems Laboratory (IIS), D-ITET, ETH Zurich*  
  Leads the Physical AI Kit hardware design, bench laboratory firmware contracts, and hands-on studio checkpoints.

---

## The Lineage of Open Systems Education

This project is the culmination of a decade-long systems engineering progression:

1. **The TinyML Era (2018–2022):** *Can we compress and deploy neural models onto constrained microcontrollers?* (Focus: Quantization, micro-kernels, TinyML Kit with Arduino).
2. **The MLSys Era (2020–2025):** *How do we engineer systems that train, serve, and scale machine learning under physical hardware laws?* (Focus: Distributed training, serving systems, MLPerf, [`mlsysbook.ai`](https://mlsysbook.ai)).
3. **The Physical AI Systems Era (2026+):** *What must the system know, measure, enforce, and prove before a learned proposal may produce a physical consequence?* (Focus: Multi-rate runtimes, proposal-permission dual-brain architectures, $P_{99}$ latency tails, real-time safety enforcers, and defensible release cases).
