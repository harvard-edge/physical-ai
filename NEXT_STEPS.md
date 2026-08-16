# Physical AI Systems — Project State & Next Steps

This document captures the current engineering status of the book, curriculum, and hardware labs, providing an immediate handoff to resume development seamlessly.

---

## 1. Current State (Clean & Verified)

* **Git Branch:** `dev` (synchronized with `origin/dev`).
* **Book Structure:** Consolidated into a rigorous **3-Part Architecture** across 11 substantive chapters + 1 Capstone Defense.
* **Front Matter & Preface:** Fully drafted in `book/index.qmd`:
  * *The Four Eras of AI Systems* (Cloud $\to$ TinyML $\to$ Foundation Models $\to$ Physical AI).
  * *The Three Engineering Tribes* (The Brain [CS/ML], The Nervous System [ECE], The Body [Robotics/Control]).
  * *The Backward Design Matrix* (What each tribe leaves behind and masters).
* **Part Overviews:** Fully authored across `book/parts/01-foundations.qmd`, `book/parts/02-agent-architecture.qmd`, and `book/parts/03-integration-release.qmd`.
* **Chapter 1 (*Physical Causality*):** Full publication-grade prose completed in `book/chapters/01-boundary/01-boundary.qmd`:
  * Philosophical framing of digital idempotency (`try/catch`) vs. physical irreversibility ($W_t \to W_{t+1}$).
  * Mathematical foundations (kinetic energy $\frac{1}{2}\mathbf{\dot{q}}^T \mathbf{M}(\mathbf{q}) \mathbf{\dot{q}}$, Joule heating $I^2 R$, compounding covariate shift $\mathcal{O}(T^2 \epsilon)$).
  * *Latent Runaway Actuator* Incident Autopsy (silicon timer peripheral register latching).
  * The **`LOOP-01` Loop Charter** Cumulative Design Dossier YAML specification.
* **Figure Typography & Vector Assets:**
  * All core figures (`fig01_agent_anatomy`, `fig01_eras_evolution`, `fig01_three_tribes`) compiled with clean **TeX Gyre Heros** sans-serif font and **`sfmath`** for mathematical notation.
  * Automated `fig_pipeline_locator.pdf` generated and synchronized across all 12 chapters.
  * Full Quarto PDF build (`quarto render --to pdf`) renders with zero errors.

---

## 2. Immediate Next Steps Roadmap

### Step 1: Draft Chapter 2 — *Time and Latency* (`book/chapters/02-metrology/02-metrology.qmd`)
* **Core Question:** *How does information age ($\Delta t$) decay across heterogeneous memory buses, and why does tail latency ($P_{99}$) govern physical stopping distance ($d_{\text{stop}}$)?*
* **Key Sections to Write:**
  1. *The Illusion of Average Latency:* Why $P_{50}$ hides catastrophic physical tails; UMA DRAM bus contention between CPU, GPU, and DMA.
  2. *Photon-to-Actuator Latency Deconstruction:* Tracing nanosecond-by-nanosecond time across optical exposure, MIPI CSI-2 serialization, NPU tensor execution, inter-process IPC, and inductive coil current rise time.
  3. *The Physics of Stopping Distance:* Deriving $d_{\text{stop}}(v_0, \Delta t, a_{\max}, j_{\max})$ and proving why stale sensor data expands collision envelopes.
  4. *Design Dossier Artifact:* Authoring and locking **`REQ-01` (Requirements & Latency Budget Ledger)**.
  5. *Bench Realization:* Instrumenting GPIO toggle profiling and hardware PTP timestamps on the Arduino UNO Q dual-brain kit.

### Step 2: Draft Chapter 3 — *Multi-Rate Systems* (`book/chapters/03-runtime/03-runtime.qmd`)
* **Core Question:** *How do we architect an asynchronous runtime that connects a 1 Hz VLM, a 20–50 Hz VLA, and a 1 kHz MCU reflex loop without race conditions or starvation?*
* **Key Sections to Write:**
  1. *The Three Speeds of Intelligence:* Decoupling 1 Hz semantic intent leases, 20–50 Hz action chunk trajectories, and 1 kHz bare-metal reflexes.
  2. *Lock-Free Shared Memory IPC:* Seqlocks, atomic sequence counters, and double-buffered ring buffers in heterogeneous SRAM.
  3. *Fault Containment & Watchdog Leases:* Designing expiring intent leases ($t_{\text{expire}}$) and proving MCU fail-safe motor shutdown when Linux crashes (`SIGKILL` / kernel panic).
  4. *Design Dossier Artifact:* Authoring and locking **`RUN-01` (Continuous Runtime Skeleton)**.

### Step 3: Part I Review & Transition to Part II
* Lock the foundational triad: `LOOP-01` + `REQ-01` + `RUN-01`.
* Begin Part II deep dive across the agent's organs: Perception (Ch 4), Memory (Ch 5), Reasoning (Ch 6), Planning (Ch 7), and Reflex (Ch 8).

---

## 3. Quick Prompts to Resume Work

When starting the next conversation, pick up immediately by issuing any of these prompts:

1. **`"Let's draft Chapter 2 (Time and Latency)"`**  
   *Will outline sections, write publication-grade prose, add mathematical proofs, and generate the `REQ-01` ledger.*

2. **`"Let's review the technical plan for Part I before drafting Chapter 2 and 3"`**  
   *Will provide a complete systems architecture walkthrough of Part I contracts and bench labs.*

3. **`"Render a preview of the latest book PDF"`**  
   *Will compile and inspect the visual layout of any chapter or page.*
