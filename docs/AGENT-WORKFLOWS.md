# Agentic Workflows & Custom Subagent Architecture

**Status:** Canonical Workflow Specification  
**Project:** *Physical AI: Machine Learning Systems That Sense and Act*  
**Scope:** Multi-agent authoring, citation grounding, prospective reader simulation, and technical review boards.

---

## Overview & Philosophical Framing

This project is **not a standard academic textbook** filled with end-of-chapter exercises or abstract proofs. It is a **Definitive Systems Playbook & Architectural Manifesto** (in the tradition of Hennessy & Patterson, Saltzer & Kaashoek, and Leveson) for building real-world Physical AI systems that sense and act.

To execute this work with maximum rigor, clarity, and empirical grounding, we use a **4-Guild Agentic System Architecture**.

---

## The 4 Agent Guilds

```text
                            THE 4-GUILD AGENTIC ARCHITECTURE
 ┌───────────────────────────────────────┐ ┌───────────────────────────────────────┐
 │ GUILD A: Topic Generators & Authors   │ │ GUILD B: Citation & Evidence          │
 │ Drafts section claims, trade-offs,    │ │ Fetches empirical papers, benchmarks, │
 │ figures, and Quarto .qmd manuscript.  │ │ ISO safety standards & BibTeX records.│
 └───────────────────┬───────────────────┘ └───────────────────┬───────────────────┘
                     │                                         │
                     └───────────────────┬─────────────────────┘
                                         ▼
                     ┌─────────────────────────────────────────┐
                     │ GUILD C: Target Reader Simulators       │
                     │ Tests prose against 4 reader personas:  │
                     │ "Does this trigger an 'Oh wow!'?"       │
                     └───────────────────┬─────────────────────┘
                                         │
                                         ▼
                     ┌─────────────────────────────────────────┐
                     │ GUILD D: Expert Review Board            │
                     │ Audits ML systems, real-time safety,    │
                     │ embodied AI, and eliminates LLM fluff.  │
                     └─────────────────────────────────────────┘
```

---

### Guild A — Topic-Specialized Generators (Author Team)

Specialized subagents dynamically generated for specific chapter domains:

1. **Metrology & Runtime Author (Ch 1–2):** Focuses on physical dynamics ($\tau_{\text{world}}$), tail latency distributions ($P_{99}$), and continuous multi-rate execution.
2. **Sensors & Perception Author (Ch 3–4):** Focuses on NPU tokenization, DMA bottlenecks, spatial frame graphs ($SE(3)$), and belief estimation.
3. **Embodied AI & Planning Author (Ch 5–6):** Focuses on VLM intent proposals, VLA trajectory rollouts, and $H$-step action chunking.
4. **Safety Enforcer & Embedded Systems Author (Ch 7–8):** Focuses on MCU safety vetoes, dynamic stopping bounds ($d_{\text{stop}}$), and heterogeneous placement maps.
5. **Data Flywheel & Assurance Author (Ch 9–10):** Focuses on trajectory logs, human override maps, fault injection, and Claim-Argument-Evidence (CAE) release verdicts.

---

### Guild B — Citation & Evidence Cartographers

Dedicated to grounding every claim in empirical literature, real-world benchmarks, and hardware specifications:

- **Skills Utilized:** `literature-search-arxiv`, `literature-search-openalex`, `pubmed-database`, `dbsnp-database`.
- **Primary Job:** 
  1. Map empirical literature and benchmarks to every section (e.g., linking $P_{99}$ latency drops to real autonomous vehicle disengagements; linking action chunking to ACT/Diffusion Policy papers; linking safety vetoes to ISO 21448 SOTIF).
  2. Verify primary sources and DOIs.
  3. **Strict Policy:** Zero hallucinated citations. Every reference must be verified against real DOIs and canonical systems papers.

---

### Guild C — Target Reader Persona Simulators ("The Reader Panel")

Evaluates draft prose through the eyes of 4 distinct target reader personas to ensure every section triggers an **"Oh wow!"** realization:

1. **The Senior ML Systems Engineer:** *"Can I actually deploy this VLA model safely on an edge accelerator?"*
2. **The Embedded Robotics Hardware Lead:** *"Will this run on an MCU with 512KB RAM and a CAN bus without blocking my 1 kHz loop?"*
3. **The Autonomous Systems Architect:** *"How does this handle dynamic stopping when network latency spikes?"*
4. **The Applied Graduate Student:** *"Is this concept crystal clear? Did I just have an 'Oh wow!' moment reading this section?"*

---

### Guild D — Expert Review Board ("The Skeptical Panel")

Provides rigorous technical auditing for safety, systems correctness, and non-LLM prose:

1. **ML Systems Architect:** Audits memory bandwidth, NPU tokenization, DMA overheads, and Pareto frontiers.
2. **Real-Time Safety Specialist:** Audits MCU safety vetoes, hardware watchdog limits, and failure domain isolation.
3. **Embodied AI Researcher:** Audits spatial grounding, action chunking, and VLA interfaces.
4. **Prose & Style Editor:** Enforces Saltzer & Kaashoek claim-first style, American English, no explanatory colons, and zero LLM buzzwords ("unlocking", "empowering", "seamlessly").

---

## The Iterative Authoring Workflow

For every section in the book, the subagent workflow runs through this 5-step pass:

$$\text{1. Citation Grounding} \longrightarrow \text{2. Author Drafting} \longrightarrow \text{3. Reader Audit} \longrightarrow \text{4. Expert Review} \longrightarrow \text{5. Commit}$$

```text
STEP 1: CITATION GROUNDING (Guild B - Citation Agent)
  │ Fetch 2–3 citable empirical papers/benchmarks for the section claim.
  ▼
STEP 2: SECTION DRAFTING (Guild A - Topic Author)
  │ Write claim-first prose, trade-off matrix, code contract, and Quarto .qmd text.
  ▼
STEP 3: READER PERSONA AUDIT (Guild C - Reader Panel)
  │ Evaluate draft across the 4 reader personas: "Does this spark 'Oh wow!'?"
  ▼
STEP 4: EXPERT TECHNICAL & PROSE CRITIQUE (Guild D - Expert Board)
  │ Audit safety math, hardware reality, and eliminate any residual LLM fluff.
  ▼
STEP 5: RECONCILIATION & BUILD (Orchestrator)
  │ Refine draft, update dossier artifact, build Quarto HTML/PDF, and commit.
```
