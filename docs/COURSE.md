# Physical AI Systems — Course Syllabus

**One offer.** This is the public syllabus, project schedule, and curriculum spine for **Physical AI Systems**.

| Audience | Same materials mean |
| --- | --- |
| **Enrolled cohort** (e.g., university seminar / project work) | Credit, supervision, graded milestones |
| **Open learners / partners** (Arduino, self-study, other schools) | **Welcome to follow the same path**—book + kit + milestones—on your own calendar |
| **Authors / postdocs** | Build the *same* book chapters and lab contracts |

**Book** = *Physical AI: Machine Learning Systems That Sense and Act*  
**Kit** = **TinyAgents Kit** (Arduino UNO Q dual-brain: MPU proposes, MCU permits)  
**Project** = One team TinyAgent + cumulative design dossier  
**Host:** `physical.mlsysbook.ai` (alias `phys.mlsysbook.ai`)

> TinyML taught you to deploy a model. TinyAgents teaches you to build an intelligent machine.

---

## What You Learn

**Outcome:** Design, measure, and defend a physical AI system so a learned proposal may produce physical action only through independent permission, culminating in an evidence-backed **Deploy / Condition / Refuse** release verdict.

**The 5 Super-Primitives:**
- **Loop:** Action changes the next observation ($W_t \rightarrow W_{t+1}$)
- **Time:** Freshness boundaries—how old may belief be when action occurs?
- **Budget:** Shared latency, energy, memory, and bandwidth constraints
- **Permission:** Independent MCU mechanisms that veto or permit proposals
- **Evidence:** Quantitative measurement supporting a release claim

---

## 10-Chapter Course Schedule

```text
Block I   Foundations & Metrology      book Ch 1–2     early seminar
Block II  Sense, Perception & Memory   book Ch 3–4     project setup
Block III Reasoning & Planning         book Ch 5–6     midterm milestone
Block IV  Enforcement & Placement       book Ch 7–8     permission hardening
Block V   Governance & Release         book Ch 9–10    final dossier & defense
```

| Week | Seminar Topic | Project Work | Milestone / Lab Handoff |
| ---: | --- | --- | --- |
| **1** | Kickoff: Scope, TinyAgent, dual-brain kit, teams | Kit bring-up; pick physical micro-task | **T0** Roster + Kit (`labs/00`) |
| **2** | Physical AI Scope: Consequential feedback & authority | Draw causal boundary; loop charter | **T1 Proposal** (`labs/01`) |
| **3** | Sense-to-Actuation Metrology & World Timescales | Measure latency distributions ($P_{99}$) & information age | `labs/02` + `labs/03` |
| **4** | Continuous Multi-Rate Runtimes & Fault Isolation | Multi-rate scheduling; MPU crash $\rightarrow$ MCU continues | **T2 Foundations** (`labs/04`) |
| **5** | Perception Frontiers & Multimodal Sensor Encoders | Sensor acquisition points; quality vs latency vs energy | `labs/05` |
| **6** | State Estimation, Spatial Memory & Temporal Belief | Frame graphs, clock sync, belief & innovation residuals | `labs/06` |
| **7** | **Midterm Presentations** (Reasoning & Intent Proposals) | VLM intent proposals; expiring intent leases | **T3 Midterm** (`labs/07`) |
| **8** | Policy Interfaces, VLAs & Action Chunking | Multi-step action chunks & temporal ensembling | — |
| **9** | Real-Time Action Enforcement & MCU Safety Enforcers | MCU safety vetoes & dynamic stopping bounds | `labs/08` (Signature Lab) |
| **10** | Heterogeneous System Placement & Resource Ledgers | Map 7 stages across MCU/MPU/Cloud; audit ripples | `labs/09` |
| **11** | Interaction Trajectories & Human Authority | Telemetry logging, overrides, E-stops & consent maps | **T4 Release Draft** (`labs/11`+`12`) |
| **12** | Pre-Deployment Qualification & Fault Injection | SIL/HIL testing; hardware fault injection | `labs/10` |
| **13** | **Final Design-Review Talks** | Present CAE release verdict (Deploy/Condition/Refuse) | **T5 Final Defense** (`labs/99`) |
| **14** | Dossier Freeze & Kit Return | Final dossier submission | **T6 Dossier** |

---

## Milestones & Graded Artifacts

- **T1 Proposal (Week 2):** Task/world scope, loop charter, requirements sketch (`Ch 1`).
- **T2 Foundations (Week 4):** End-to-end metrology, multi-rate runtime, MCU continues under MPU hang (`Ch 2–4`).
- **T3 Midterm (Week 7):** Observe $\rightarrow$ Estimate $\rightarrow$ Propose $\rightarrow$ Permit $\rightarrow$ Act loop working (`Ch 5–7`).
- **T4 Release Draft (Week 11):** Placement map, MCU safety enforcer, authority map (`Ch 8–9`).
- **T5 Final Defense (Week 13):** Capstone talk defending the system under seeded faults.
- **T6 Written Dossier (Week 14):** Complete Cumulative Design Dossier matching Chapters 1–10.
