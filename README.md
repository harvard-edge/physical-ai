# Physical AI Systems

**Physical AI: Machine Learning Systems That Sense and Act**  
Author & Lecturer: **Prof. Vijay Janapa Reddi** (Harvard University / Visiting Professor, ETH Zurich)  
Course Site: [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai)

> *TinyML taught you how to deploy a model to a microchip. Physical AI teaches you how to build an intelligent, safe machine under physical and resource laws.*

---

## The North Star

Standard machine learning ends at digital output. A classifier emits a label; a language model emits text. **Physical AI Systems** begin when that output moves matter, consumes kinetic energy, interacts with humans, and permanently alters the physical world ($W_t \to W_{t+1}$).

Because physical actions are irreversible (**you cannot `ctrl+z` kinetic energy**), the central question governing this curriculum and book is:

> **"What must the surrounding system know, measure, enforce, preserve, and prove before an unverified learned proposal may produce a physical consequence?"**

---

## The Architecture: Propose vs. Permit (Dual-Brain)

Learned foundation models (VLMs, VLAs, Diffusion Policies) are non-deterministic and have no intrinsic awareness of physical inertia, memory bus contention, or clock skew. They must be treated as **untrusted proposal services**, strictly isolated from direct motor authority.

```text
       ┌─────────────────────────────────────────────────────────────┐
       │                   THE DUAL-BRAIN ARCHITECTURE               │
       │                                                             │
       │       LINUX MPU (Best-Effort Cortex)                        │
       │       • Vision Encoders, VLMs, Action Chunking              │
       │       • Role: UNTRUSTED PROPOSAL ENGINE                     │
       │       • Output: Expiring Intent Leases (3D Bounds, TTL)     │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      │  Expiring Intent Proposal (pt)
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │       REAL-TIME MCU (Deterministic Reflex)                  │
       │       • 1 kHz Timing Loop, Dynamic Stopping Bounds (d_stop) │
       │       • Independent Safety Geofencing & Hard Interrupts     │
       │       • Role: TRUSTED PERMISSION AUTHORITY                  │
       │       • Output: Permitted Actuation (ut = permit(pt))       │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
                              PHYSICAL MOTORS / WORLD
```

---

## Repository Structure

This repository contains the complete open curriculum, reference textbook, and hardware lab tracks for **Physical AI Systems**:

```text
PhysicalAI/
├── README.md               # Overview & quickstart guide
│
├── course/                 # Course administration & academic materials
│   └── syllabus.md         # Official 14-week course syllabus & schedule (ETH 6 ECTS)
│
├── slides/                 # Weekly seminar & lecture slide decks
│   └── README.md           # Slide index for Weeks 1–14
│
├── book/                   # The Architectural Field Manual (Quarto Source)
│   ├── index.qmd           # Preface & Manifesto (Vijay's 4 Bedrock Laws)
│   ├── front-matter/       # About Author, Prerequisites & Field Manual Guide
│   ├── chapters/           # 11 Substantive Chapters (with localized figures/)
│   ├── appendix/           # Dossier templates, UNO Q hardware specs, math & glossary
│   └── _quarto.yml         # Master Quarto build configuration (HTML & PDF)
│
└── labs/                   # Hardware Lab Track on Arduino UNO Q (Postdoc / Andrea)
    ├── 00-kit-bringup/     # Board bring-up, IPC link & safe idle
    ├── 01-close-the-loop/  # Advisory vs. closed-loop state mutation
    ├── 02-freshness-wall/  # Information age vs. task efficacy collapse
    ├── 03-measure-brains/  # Complete-path latency tail metrology (P99)
    ├── 04-runtime-faults/  # Multi-rate scheduling & MPU crash survival
    ├── 05-perception/      # DMA ingestion tax & spatial affordance tokens
    ├── 06-belief-drift/    # SE(3) frame graphs & temporal belief TTL leases
    ├── 07-vlm-intent/      # VLM 3D bounding boxes & expiring intent leases
    ├── 08-mcu-enforcer/    # Signature Lab: 1 kHz MCU safety vetoes & d_stop
    ├── 09-placement/       # Heterogeneous resource allocation & bus QoS
    ├── 10-governed-data/   # Bumpless human overrides & truncated log streams
    ├── 11-release-gate/    # Seeded fault injection & Deploy/Refuse verdict
    └── shared/             # Shared MPU/MCU headers, schemas & utilities
```

---

## Building the Book

The reference text is written in [Quarto](https://quarto.org) and builds both an interactive web edition and a professional publication-quality PDF.

```bash
cd book

# Live local preview server
quarto preview

# Render full HTML and PDF deliverables
quarto render
```

---

## The Lineage & Pedagogy

This project is the natural continuation of the open systems curriculum lineage established by Prof. Vijay Janapa Reddi:

1. **TinyML (2018–2022):** Making deep learning run on constrained microcontrollers (Harvard/edX + Arduino Nano 33 BLE Sense).
2. **MLSys (2020–2025):** Scaling machine learning training and inference under physical hardware laws (MLCommons, [`mlsysbook.ai`](https://mlsysbook.ai)).
3. **Physical AI Systems (2026+):** Governing and shockproofing learned models whose proposals act in the physical world (ETH Zurich + TinyAgents Kit on Arduino UNO Q).

### Key Contacts
* **Course Lecturer:** Prof. Vijay Janapa Reddi ([vjanapa@ethz.ch](mailto:vjanapa@ethz.ch))
* **Kit & Studio Lead:** Dr. Andrea Mattia Garavagno (IIS, D-ITET, ETH Zurich)
