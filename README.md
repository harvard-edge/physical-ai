# Physical AI Systems

**Physical AI: Machine Learning Systems That Sense and Act**  
Author & Lecturer: **Prof. Vijay Janapa Reddi** (Harvard University / Visiting Professor, ETH Zurich)  
Kit & Studio Lead: **Dr. Andrea Mattia Garavagno** (Integrated Systems Laboratory, IIS, D-ITET, ETH Zurich)  
Course & Book Site: [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai)

> *TinyML taught you how to deploy a neural model to a microchip. Physical AI teaches you how to build an intelligent, safe machine under physical and resource laws.*

---

## The North Star

Standard machine learning ends at digital output. A classifier emits a label; a language model emits text. In the digital world, software errors are harmlessly contained behind glass: transactions roll back, exceptions are caught, and dropped packets are retried.

**Physical AI Systems** begin at the exact moment software crosses the boundary into the physical world ($W_t \to W_{t+1}$)—commanding pulse-width modulated gate drivers, accelerating kilograms of mass, consuming kinetic energy, interacting with humans, and permanently altering the physical environment.

Because physical actions cannot be rewound (**you cannot `ctrl+z` kinetic energy**), the central question governing this curriculum, reference book, and hardware lab track is:

> **"What must the surrounding system know, measure, enforce, preserve, and prove before an unverified learned proposal may produce a physical consequence?"**

---

## The 4 Bedrock Laws of Physical AI Systems

Every chapter, architectural interface, and laboratory in this project is anchored in 4 inescapable physical and systems laws:

1. **The Law of Physical Causality & Irreversibility:** Software bits can be snapshot and retried with `try/catch`. Physical actions governed by inertia, friction ($\mu$), Joule heating ($I^2R$), and momentum cannot. Every actuation permanently mutates the world ($W_t \to W_{t+1}$) and alters all future sensory observations endogenously ($A_t \to W_{t+1} \to O_{t+1}$).
2. **The Law of Information Freshness (The Time Law):** The physical world does not pause for computation. Sensor data decays the instant photons hit the photodiode. Mean latency ($P_{50}$) is an illusion; tail latency ($P_{99}$), DRAM memory bus contention, and information age ($\Delta t$) dictate dynamic stopping distances ($d_{\text{stop}}$) and physical stability.
3. **The Law of Proposal–Permission Privilege (The Architecture Law):** No stochastic foundation model (VLM, VLA, Diffusion Policy) may hold direct motor authority. Learned models running on application processors (MPU) are *untrusted proposal services*. Deterministic real-time permission belongs to dedicated, zero-allocation microcontrollers (MCU) running mathematical safety enforcers (Control Barrier Functions) and physical fallbacks.
4. **The Law of Governed Change & Defensible Release (The Safety Law):** Simulation demos and benchmark leaderboards are not proof of safety. A physical agent shapes its own future data distribution. Defensible release requires cross-layer fault injection, formal safety cases, and an evidence-backed **Deploy / Condition / Refuse** release verdict.

---

## The Core Architecture: Proposal–Permission (Dual-Brain)

Learned foundation models are non-deterministic and lack intrinsic awareness of physical inertia, memory bus contention, or clock skew. The **Dual-Brain Architecture** cleanly decouples best-effort cognitive proposals from deterministic bare-metal permission:

```text
       ┌─────────────────────────────────────────────────────────────┐
       │                   THE DUAL-BRAIN ARCHITECTURE               │
       │                                                             │
       │       LINUX MPU (Best-Effort Cognitive Cortex)              │
       │       • Vision Encoders (ViT, DINOv2), VLMs, ACT Chunking   │
       │       • Frequency: 1 Hz (Deliberation) → 20–50 Hz (Planning)│
       │       • Role: UNTRUSTED PROPOSAL ENGINE                     │
       │       • Output: Expiring Intent Leases (3D Bounds, TTL)     │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      │  Expiring Intent Proposal (pt)
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │       REAL-TIME MCU (Deterministic Safety Reflex)           │
       │       • 1 kHz Bare-Metal Loop, Zero-Dynamic Allocation      │
       │       • Control Barrier Functions (h(x) ≥ 0), d_stop Bounds │
       │       • Independent Safety Geofencing & Hard Watchdogs      │
       │       • Role: TRUSTED PERMISSION AUTHORITY                  │
       │       • Output: Permitted Actuation (ut = permit(pt))       │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
                              PHYSICAL MOTORS / WORLD
```

---

## The Three Engineering Tribes

Physical AI is the grand synthesis of three engineering cultures, each bringing essential strengths and dangerous blindspots:

```text
┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│     THE BRAIN (ML / CS)      │  THE NERVOUS SYSTEM (ECE)    │ THE BODY & CONTROL (ROBOTICS)│
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ • High-Capacity Models       │ • Microsecond Clock Sync     │ • Dynamics & Inertia M(q)    │
│ • Spatial Token Embeddings   │ • Zero-Copy DMA Pipelines    │ • Control Barrier Functions  │
│ • Diffusion Action Chunks    │ • Lock-Free Shared SRAM      │ • Classical Safe Sets        │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│ Blindspot: Digital Sandbox   │ Blindspot: Static Automation │ Blindspot: Closed-World CAD  │
│ (Ignores tails & crashes)    │ (Cannot parse open worlds)   │ (Distrusts learned models)   │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                              │
                                              ▼
                         THE PHYSICAL AI SYSTEMS SYNTHESIS
      Universal Success Metric: Open-World Semantic Competence AND Strict Invariant Survival
```

---

## Book Structure & Cumulative Design Dossier

The book is organized into **3 Foundational Parts (11 substantive chapters + Capstone)**. Across the spine, readers build an accumulating, versioned **Cumulative Design Dossier** for a physical handling system:

| Part | Chapter | Focus / Organ | Design Dossier Artifact |
| :--- | :--- | :--- | :--- |
| **Part I: Foundations** | `01-boundary` | **Physical Causality** | `LOOP-01` (Loop Charter) |
| | `02-latency` | **Time, Freshness & Latency** | `REQ-01` (Requirements & Latency Ledger) |
| | `03-workflow` | **The Agent Workflow** | `FLOW-01` (Workflow & Multi-Rate Charter) |
| **Part II: Pipeline Organs** | `04-perception`| **Perception & Encoders** | `OBS-01` (Observation Contract) |
| | `05-state` | **Memory & World Models** | `STATE-01` (State & Timing Model) |
| | `06-intent` | **Reasoning & Intent** | `INTENT-01` (Intent Schema & Leases) |
| | `07-planning` | **Planning & Chunking** | `PLAN-01` (Trajectory Planning Schema) |
| | `08-enforcement`| **Reflex & Safety Veto** | `ENF-01` (Safety Enforcer & CBF) |
| **Part III: Integration & Release** | `09-placement` | **Workload Placement** | `PLACE-01` (Heterogeneous Silicon Ledger)|
| | `10-governance` | **Human Governance** | `AUTH-01` (Governance Record & Lineage) |
| | `11-assurance` | **Defensible Assurance** | `REL-01` (Claim-Argument-Evidence Case) |
| **Capstone** | `99-capstone` | **Capstone Bench Defense** | Full Dossier Defense & Release Verdict |


---

## Repository Structure

```text
PhysicalAI/
├── README.md               # Project overview, architecture & quickstart
├── NEXT_STEPS.md           # Engineering status handoff & immediate roadmap
│
├── course/                 # Academic administration & syllabus
│   └── syllabus.md         # Official 14-week ETH Zurich course syllabus (6 ECTS)
│
├── slides/                 # Weekly lecture & seminar slide decks
│   └── README.md           # Slide deck index
│
├── book/                   # The Architectural Reference Text (Quarto source)
│   ├── index.qmd           # Preface & Manifesto (Four Eras, Three Tribes, 4 Laws)
│   ├── front-matter/       # About the Author, Prerequisites & How to Use
│   ├── parts/              # Architectural part overview files (Parts 1–3)
│   ├── chapters/           # 12 Chapter manuscripts with localized TikZ figures/
│   ├── appendix/           # Dossier templates, Uno Q reference, math & glossary
│   ├── tex/                # TikZ figure generation scripts & LaTeX preambles
│   └── _quarto.yml         # Master Quarto configuration (HTML web + publication PDF)
│
└── labs/                   # Hardware Lab Track on Arduino UNO Q Dual-Brain
    ├── 00-kit-bringup/     # Board bring-up, IPC link & safe idle state
    ├── 01-close-the-loop/  # Advisory mode vs. closed-loop state mutation
    ├── 02-freshness-wall/  # Information age vs. task efficacy collapse
    ├── 03-measure-both-brains/ # Complete-path latency tail metrology (P99, DMA)
    ├── 04-runtime-fault-containment/ # Multi-rate scheduling & MPU crash survival
    ├── 05-perception-frontier/ # DMA ingestion tax & spatial affordance tokens
    ├── 06-belief-drift/    # SE(3) frame graphs & temporal belief TTL leases
    ├── 07-two-speed-intent/# VLM 3D bounding boxes & expiring intent leases
    ├── 08-mcu-enforcer/    # Signature Lab: 1 kHz MCU safety vetoes & d_stop
    ├── 09-placement-ripple/# Heterogeneous resource allocation & bus QoS
    ├── 10-shadow-and-faults/# Seeded fault injection & shadow runtime auditing
    ├── 11-authority-paths/ # Bumpless human overrides & joystick handoff
    ├── 12-learning-turn/   # Closed-loop policy refinement & covariate shift
    ├── 13-ship-gate/       # Release gate defense & Deploy/Condition/Refuse verdict
    ├── 99-design-review/   # Capstone dossier jury defense
    └── shared/             # Shared MPU/MCU headers, contracts & schemas
```

---

## Reference Hardware Kit: The Physical AI Kit (Arduino UNO Q)

The course and laboratory track ground all theoretical concepts on zero-magic bench hardware:

* **Host Brain (MPU):** Qualcomm-based Linux application processor running PyTorch, TensorRT, Vision-Language Models (VLMs), and ACT Action Chunk decoders.
* **Reflex Brain (MCU):** Dedicated 32-bit Cortex-M4 microcontroller running bare-metal / FreeRTOS, executing 1 kHz Control Barrier Functions, hardware watchdog leases, and emergency power interlocks.
* **Actuator Subsystem:** Multi-axis precision motion stage with current-sense telemetry and hardware emergency interlock relay.
* **Sensor Suite:** MIPI CSI-2 camera with DMA hardware capture, high-speed optical encoders, and 6-DoF IMU.

---

## Building the Book

The book is written in [Quarto](https://quarto.org) and compiles into both an interactive web edition and a publication-quality PDF via LuaLaTeX:

```bash
cd book

# 1. Live local HTML preview server (with hot reload)
quarto preview

# 2. Render complete HTML website and publication PDF deliverable
quarto render
```

### Compiling TikZ Vector Figures

All architectural figures are standalone, publication-grade vector graphics using `TeX Gyre Heros` and `sfmath`:

```bash
cd book

# Build core figures (Eras Evolution, Agent Anatomy, Three Tribes)
python3 tex/polish_figures.py

# Build recurring pipeline locator figures across all 12 chapters
python3 tex/build_locators.py
```

---

## Teaching Team & Credits

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
