# Physical AI Systems — Course Syllabus

**ETH Zurich · Project-Based Course · 6 ECTS**  
**Online / Partner Offering:** [`physical.mlsysbook.ai`](https://physical.mlsysbook.ai)

| | |
| :--- | :--- |
| **Course** | Physical AI Systems (*Physical AI: Machine Learning Systems That Sense and Act*) |
| **Credits** | 6 ECTS (≈ 150–180 total workload hours) |
| **Format** | Project seminar + hardware studio / group project · **No written final exam** |
| **Language** | English |
| **Level** | Advanced Bachelor (3rd/4th year) & Master (D-ITET, D-INFK, Robotics/CPS) |
| **Contact** | Weekly Seminar (2 h / week) + Hands-On Studio / Lab Time |
| **Reference Book** | *Physical AI: Machine Learning Systems That Sense and Act* (Vijay Janapa Reddi) |
| **Hardware Kit** | **TinyAgents Kit** (Arduino UNO Q Dual-Brain: Linux MPU + Real-Time MCU) |

---

## 1. Teaching Team

### Prof. Vijay Janapa Reddi — Lecturer
* Gordon McKay Professor of Electrical Engineering, Harvard University
* Visiting Professor, ETH Zurich (Integrated Systems Laboratory, IIS, D-ITET)
* **Office:** ETZ F 83 · **Email:** [vjanapa@ethz.ch](mailto:vjanapa@ethz.ch) · **Web:** [Homepage](https://profvjreddi.github.io/homepage)

### Dr. Andrea Mattia Garavagno — Co-Teacher & Studio Lead
* Postdoctoral Researcher, ETH Zurich (Integrated Systems Laboratory, IIS, D-ITET)
* Runs day-to-day TinyAgents Kit bring-up, studio hours, and hardware milestone checkpoints.

**Office Hours:** By appointment (email instructors with subject `[Physical AI]`).

---

## 2. Course Overview

Standard machine learning ends at digital output. A classifier emits a label; a language model emits text. **Physical AI Systems** begin when that output moves matter, consumes kinetic energy, affects humans, and alters all future sensory observations ($W_t \to W_{t+1}$). **You cannot `ctrl+z` kinetic energy.**

In this course, student teams design, build, measure, and defend an intelligent **TinyAgent** on the **Arduino UNO Q Dual-Brain Kit**:

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

### What This Course Is (and Is Not)

| What This Course Is NOT | What This Course IS |
| :--- | :--- |
| ✗ A compressed classical robotics kinematics / ROS course | ✓ A **systems engineering discipline** for learned, acting machines |
| ✗ TinyML “quantize and deploy” alone | ✓ Bridging **high-level foundation models to real-time safety** |
| ✗ A cloud LLM prompt-chaining / chatbot lab | ✓ **Multi-rate runtimes, zero-copy DMA, IPC, and watchdogs** |
| ✗ A purely theoretical or simulation-only seminar | ✓ Real hardware with **mass, inertia, bus contention, and tails** |

---

## 3. The 14-Week Schedule

The curriculum follows **The Anatomy of a Physical AI Agent**, moving from physical foundations to internal spatial belief, deliberative reasoning, real-time safety vetoes, and defensible release:

| Week | Seminar Topic | Project & Kit Milestone | Due Artifact |
| :---: | :--- | :--- | :---: |
| **W1** | **Kickoff & The Dual-Brain Architecture** | Team formation & UNO Q kit bring-up | **T0: Roster + Kit (`labs/00`)** |
| **W2** | **Physical Causality & Causal Boundaries** | Matter, momentum & drawing causal boundaries | **T1: Loop Charter (`labs/01`)** |
| **W3** | **Time and Latency Metrology** | Measuring sense-to-actuation $P_{99}$ tail latency | `labs/02` + `labs/03` |
| **W4** | **Multi-Rate Systems & Crash Survival** | Multi-rate scheduling; MPU crash $\to$ MCU holds | **T2: Runtime Skeleton (`labs/04`)** |
| **W5** | **Perception & Vision Encoders (ViTs/DINOv2)** | Pre-inference DMA tax & UMA bus contention | `labs/05` |
| **W6** | **Memory, State & Latent World Models (JEPAs)**| $SE(3)$ frame graphs, PTP sync & TTL leases | `labs/06` |
| **W7** | **MIDTERM DESIGN REVIEWS (T3 Milestone)** | **Team Talks:** Propose $\to$ Permit demonstration | **T3: Midterm Talk & Demo** |
| **W8** | **Reasoning & Deliberation (VLMs & Intent Leases)**| Grounding open-vocabulary goals with VLMs | `labs/07` |
| **W9** | **Planning & Action Chunking (Diffusion/ACT)**| Trajectory rollouts & temporal ensembling ($\mathcal{C}^2$) | — |
| **W10** | **Reflex & Safety Enforcement (1 kHz CBFs)**| 1 kHz safety filters & dynamic stopping bounds ($d_{\text{stop}}$)| **`labs/08` (Signature Lab)** |
| **W11** | **Placement & Silicon Resource Ledgers**| Mapping across MCU, MPU, NPU, and Cloud | **T4: Release Draft (`labs/09`)** |
| **W12** | **Governance & Human Authority (Bumpless Overrides)**| Bumpless overrides, tagged truncated logs & OTA | `labs/10` + `labs/11` |
| **W13** | **Release & Cross-Layer Fault Injection** | Hardware fault injection rig (HIL / stress test) | `labs/12` + `labs/13` |
| **W14** | **FINAL CAPSTONE DEFENSE & DOSSIER SUBMISSION** | **Oral defense under seeded bench faults** | **T5: Final Defense & T6: Dossier** |

---

## 4. Assessment & The Cumulative Design Dossier

There is **no written final exam**. Graded semester performance is evaluated based on continuous engineering progress, oral defense, and the written engineering record:

| Component | Weight | Description |
| :--- | :---: | :--- |
| **Process & Studio Checkpoints** | **20%** | Weekly milestone progress, active studio debugging, and team collaboration. |
| **Midterm Presentation (T3)** | **15%** | 10-minute talk + live demo of the working observe $\to$ propose $\to$ permit loop. |
| **Final Design Defense (T5)** | **25%** | Oral capstone defense and live diagnosis of an instructor-seeded bench fault. |
| **Cumulative Design Dossier (T6)** | **40%** | The complete versioned engineering dossier (`LOOP-01` through `REL-01`). |

### The Cumulative Design Dossier

Rather than writing a free-form essay, students produce an industrial-grade **Cumulative Design Dossier** that evolves across the semester:
1. `Loop Charter` (Scope, boundary, and authority)
2. `Requirements Ledger` (World deadlines and $P_{99}$ latency budgets)
3. `Runtime Skeleton` (Asynchronous IPC and watchdog protocols)
4. `Observation Contract` (Sensor rates, DMA channels, and timestamps)
5. `State & Timing Model` ($SE(3)$ frame tree and TTL validity leases)
6. `Policy & Intent Schema` (VLM 3D bounding boxes and expiration leases)
7. `Planning Schema` (Action chunk horizons $H$ and temporal ensembling)
8. `Enforcement Design` (MCU 1 kHz safety filters and physical fallback states)
9. `Placement Map & Resource Ledger` (Whole-system compute/memory/power budgets)
10. `Human-Authority & Governance Record` (Bumpless overrides and truncated logs)
11. `Integrated Deployment Case` (Claim-Argument-Evidence case and **Deploy / Condition / Refuse** release verdict)

---

## 5. Prerequisites & The Two On-Ramps

We pair students with complementary backgrounds into **2–3 person teams**:

* **On-Ramp 1 (ML & Software / D-INFK):** Strong Python/PyTorch background; learns real-time MCU enforcers, DMA bus contention, and hardware watchdogs.
* **On-Ramp 2 (Embedded & CPS / D-ITET):** Strong C/C++, FreeRTOS, and electronics background; learns VLM spatial grounding, action chunk unrolling, and governed data flywheels.

---

## 6. Course Policies & Integrity

* **Safety Invariant:** All autonomous machines must run with an active MCU safety enforcer. Intentionally bypassing the hardware enforcer for a demo is an immediate failure.
* **Collaboration:** High-level architectural discussion between teams is encouraged; firmware and dossier schemas must be the team's own original work.
* **Materials & Kit Loan:** Kits are provided on loan for the duration of the semester. Open follow-along materials are available at `physical.mlsysbook.ai`.
