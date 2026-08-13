# Physical AI Systems

**ETH Zurich · Project-based course (draft syllabus)**

> *Details marked TBD will be filled once the course number, semester, and room are confirmed. The structure below is what students should expect.*

---

## Course information

| | |
| --- | --- |
| **Course title** | Physical AI Systems |
| **Course number** | TBD (assigned by the hosting department) |
| **Credits** | 6 ECTS *(proposed; ≈ 150–180 hours of work)* |
| **Type** | Project-based seminar / group project — **no classical written exam** |
| **Language** | English |
| **Semester** | TBD |
| **Level** | Advanced Bachelor (typically 3rd year) and Master |
| **Hours** | Seminar **2 h / week** + supervised project / studio work |
| **Instructors** | Prof. Vijay Janapa Reddi · Dr. Andrea Mattia Garavagno |
| **Catalogue / site** | TBD · planned materials at `physical.mlsysbook.ai` |

---

## Teaching team

### Prof. Vijay Janapa Reddi — lecturer

Gordon McKay Professor of Electrical Engineering, Harvard University  
Visiting Professor, ETH Zurich  

| | |
| --- | --- |
| **Office** | ETH Zurich, **ETZ F 83** |
| **Email** | [vj@eecs.harvard.edu](mailto:vj@eecs.harvard.edu) |
| **Web** | [profvjreddi.github.io/homepage](https://profvjreddi.github.io/homepage) |

Prof. Reddi works on machine learning systems, edge AI, computer architecture, and TinyML. This course continues that line into **physical AI systems**: complete machines in which learned components sense and act under constraint, with independent permission before physical consequence.

### Dr. Andrea Mattia Garavagno — co-teacher

Postdoctoral researcher, ETH Zurich  
Integrated Systems Laboratory (IIS), Department of Information Technology and Electrical Engineering (D-ITET)

| | |
| --- | --- |
| **Role** | Co-teacher; project / TinyAgents Kit studio lead |
| **Email** | TBD (ETH address — will be posted on the course page) |
| **Office** | TBD (IIS / ETZ — will be posted on the course page) |

Dr. Garavagno co-teaches the seminar and leads day-to-day kit bring-up, studio support, and milestone checkpoints with the project teams.

**Office hours.** By appointment (email either instructor). Drop-in / studio hours TBD once the semester schedule is fixed.

**Additional TAs.** TBD if cohort size requires them.

---

## What this course is

Machine learning systems usually end at a digital output. **Physical AI** begins when that output may move the world. An observation becomes a belief, a belief becomes a **proposal**, and—only if independently **permitted**—an action changes the world that produces the next observation.

In this course you will **design, build, measure, and defend** a complete **TinyAgent** on the **TinyAgents Kit** (Arduino UNO Q dual-brain platform):

| Brain | Role |
| --- | --- |
| **MPU** (Linux, best-effort) | Perception, state, policies, planning, tools — **proposes** |
| **MCU** (real-time) | Limits, watchdogs, validation, safe fallback — **permits or refuses** |

The durable question:

> What must the system know, measure, enforce, preserve, and prove before a learned proposal may produce a physical consequence?

**Five primitives you will practice:** loop · time · budget · permission · evidence.

### What this course is not

- Not a compressed **robotics** curriculum  
- Not a **TinyML** “quantize and deploy” course alone (that background helps; it is not the endpoint)  
- Not an **LLM / software-agents** lab  
- Not a claim that you will produce a **certified** safety case

---

## Learning outcomes

By the end of the semester you should be able to:

1. Decide when a problem is in scope for physical AI (learned component + consequential physical feedback + delegated authority).  
2. Derive requirements from the **world** (freshness, efficacy, budgets)—not from marketing specs.  
3. Measure the full sense→act path (distributions, tails, uncertainty) across both brains.  
4. Run a continuous multi-rate architecture that still meets responsibilities when the learned path fails.  
5. Treat modern models (encoders, VLMs/VLAs, world models) as **proposal interfaces**, not actuators.  
6. Enforce limits on an **independent** MCU path that the MPU cannot bypass.  
7. Place work under shared resource budgets and reason about failure domains.  
8. Allocate human authority and render an evidence-backed **deploy / condition / refuse** verdict.

**Transfer test.** You should be able to apply the same method to a body or model family that never appeared in the lectures.

---

## Format (how the semester works)

This is a **project-first** course in the spirit of ETH Projects & Seminars (P&S) / group projects:

| Contact | What happens |
| --- | --- |
| **Weekly seminar** (~2 h) | Method, demos, discussion, midterm and final talks |
| **Studio / kit time** | Most of your work—team build (scheduled + open hours TBD) |
| **Supervision** | Short team meetings at milestones |

**Teams of 2–3.** Each team names owners for **MPU**, **MCU**, and **measurement / evidence**. Individual contribution must be visible on slides and in the written dossier.

**Book (method library):** *Physical AI: Machine Learning Systems That Sense and Act*  
**Kit:** TinyAgents Kit (UNO Q). Baseline ML-systems topics (quantization, pruning, serving costs, …) are assumed or linked as supplementary reading—not re-taught as the core of this course.

---

## Schedule (indicative 14 weeks)

*Exact calendar dates TBD. Order of topics and milestones is fixed.*

| Week | Seminar | Your project focus | Due |
| ---: | --- | --- | --- |
| 1 | Kickoff, dual-brain, kit, teams | Bring-up; pick a shared-workspace micro-task | **T0** roster + kit |
| 2 | Scope + world-imposed costs | Loop charter; advisory vs closed-loop | **T1 proposal** |
| 3 | Measuring the complete loop | End-to-end timing across MPU and MCU | — |
| 4 | Continuous runtime; fault continuity | Hang the MPU; MCU must still hold | **T2 foundations** |
| 5 | Perception under a deadline | Observation operating point | — |
| 6 | State / time; intent as proposal | Belief path + intent schema (no raw PWM from MPU) | — |
| 7 | **Midterm presentations** | Show propose ⇢ permit; take critique | **T3 midterm** |
| 8 | Studio clinic: enforcement | Harden MCU refuse / recover | — |
| 9 | Placement under budgets | Optional re-host + re-measure | — |
| 10 | Human authority; learning from interaction | Stop / revoke; admit or reject trajectories | — |
| 11 | Release workshop | Ship / condition / refuse draft | **T4 release draft** |
| 12 | Dry-run (optional) | Freeze system + dossier | — |
| 13 | **Final design-review talks** | Defend under Q&A / seeded fault | **T5 final** |
| 14 | Buffer / debrief / return kits | — | **T6 written dossier** |

**Forced kit experiences** (you cannot skip these ideas): bring-up → close the loop → measure both brains → runtime continuity → belief + intent → **MCU enforcer** → authority / ship → defend.

---

## Milestones and deliverables

| ID | When | What you submit |
| --- | --- | --- |
| **T0** | Week 1 | Team roster, kit check |
| **T1** | Week 2 | Project proposal (~3–5 pages or slides): task, loop charter, requirements sketch, risks, roles |
| **T2** | Week 4 | Foundations checkpoint (async sign-off): measured path + MCU continues under MPU failure |
| **T3** | Week 7 | Midterm talk (~10–12 min + questions): working TinyAgent; one measured design-changing claim; contribution split on slide 1 |
| **T4** | Week 11 | Release draft: residual risk, authority map, provisional deploy/condition/refuse |
| **T5** | Week 13 | Final design-review presentation |
| **T6** | Week 14 | Written **design dossier** (the course report) |

The dossier is a cumulative engineering record (charter, requirements, evidence, runtime, contracts, enforcement, placement/promotion as applicable, authority, learning rules, release case, failure appendix)—not a free-form essay. Page budget TBD (indicatively 12–20 pages body + appendix).

---

## Assessment

| Component | Weight (indicative) |
| --- | --- |
| Process and supervision (milestones, studio, contribution) | 20% |
| Midterm presentation | 15% |
| Final presentation | 25% |
| Written design dossier | 40% |

**Type:** graded semester performance · English · **no classical written final exam.**

**Minimum technical bar to pass:**

- Independent MCU permission path is real (MPU cannot bypass).  
- At least one measured end-to-end claim with uncertainty that changed a design decision.  
- Release verdict is evidence-backed.  
- Every team member can explain the dual-brain boundary without reading slides.

Repetition rules follow ETH semester-performance regulations (typically: re-enrol). Exact catalogue wording TBD.

---

## Prerequisites

**Recommended**

- Intro machine learning systems (or equivalent): models as components with latency, memory, energy, and measurement discipline  
- Solid programming (Python and/or C/C++ for embedded)  
- Willingness to work in a small team on physical hardware  

**Helpful**

- Embedded / real-time exposure; basic control or estimation; prior TinyML  

**Not required**

- A prior “agentic ML” course  
- A full robotics sequence  

If kit capacity is limited, analytical / hosted substitutes may be allowed for some stations—but the **permission boundary** must still be implemented for credit.

---

## Registration and capacity

- Registration: via **myStudies** (and departmental P&S / project tools if applicable) — process TBD  
- Places: limited by kit and TA capacity (indicatively on the order of **8–12 teams**)  
- Waiting list: per departmental rules  

---

## Communication

| Channel | Use |
| --- | --- |
| Email (lecturer) | [vj@eecs.harvard.edu](mailto:vj@eecs.harvard.edu) — appointments, exceptions |
| Email (co-teacher) | Dr. Andrea Mattia Garavagno — ETH address TBD (kit / studio / milestones) |
| Course page / Moodle | Announcements, slides, deadlines — TBD |
| Studio / kit hours | Bring-up and debugging with Dr. Garavagno — TBD |

Please put **`[Physical AI]`** in the email subject line.

---

## Policies (draft)

- **Attendance.** Seminar attendance is expected, especially midterm and final weeks.  
- **Integrity.** All submitted work must be your team’s own; declare any external code, models, or assistance. Follow ETH guidelines on scientific integrity and originality.  
- **Safety.** Kits stay in safe idle when unsupervised; never bypass the MCU enforcer “for the demo.” Report damaged hardware promptly.  
- **Collaboration.** Cross-team discussion of ideas is encouraged; copying dossiers or firmware without attribution is not.  
- **Late work.** Policy TBD; communicate early if a milestone is at risk.

---

## Materials

| Resource | Role |
| --- | --- |
| Course book | *Physical AI: Machine Learning Systems That Sense and Act* (method library) |
| Kit | TinyAgents Kit — Arduino UNO Q (MPU proposes, MCU permits) |
| Lab contracts | Repository `labs/` (phenomenon + decision per station) |
| Supplementary | Machine Learning Systems materials for quantization, pruning, serving cost—linked, not re-lectured |

---

## Catalogue blurb (short)

Students design, build, measure, and defend a physical AI system in which a learned component may act only through independent real-time permission. Team projects on a dual-brain kit are supported by weekly method seminars. Assessment: proposal, midterm demo, final design-review talk, and written design dossier (deploy / condition / refuse). English. Proposed 6 ECTS. No classical written exam.

---

## Still to be confirmed

| Item | Status |
| --- | --- |
| Official course number & hosting department | TBD |
| First offering semester & timetable (room, day) | TBD |
| Final ECTS / hour codes in VVZ | TBD (6 ECTS proposed) |
| TA names and studio hours (beyond co-teacher) | TBD |
| Co-teacher ETH email / office | TBD (Dr. Andrea Mattia Garavagno) |
| Kit logistics (loan vs purchase) | TBD |
| Moodle / course website URL | TBD |
| Exact page limits and late policy | TBD |

Questions before the semester starts: email **vj@eecs.harvard.edu** (Prof. Reddi) or Dr. **Andrea Mattia Garavagno** (ETH email TBD) with subject `[Physical AI]`, or visit **ETZ F 83** by appointment.

---

*This syllabus is a living draft for students and for departmental course setup. It mirrors ETH project-seminar practice (proposal → midterm → final talk + written report) while the catalogue entry is finalized.*
