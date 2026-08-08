# Physical AI Systems — Course

**One offer.** This is the course: syllabus, schedule, project, and curriculum spine
together. There is no separate “internal curriculum product” to keep in sync.

| Audience | Same materials mean |
| --- | --- |
| **Enrolled cohort** (e.g. ETH project seminar) | Credit, supervision, graded milestones |
| **Open learners / partners** (Arduino, self-study, other schools) | **Welcome to follow the same path**—book + kit + milestones—on your own calendar |
| **Authors / postdocs** | Build the *same* book chapters and lab contracts; do not invent a parallel syllabus |

**Book** = method library (*Physical AI: Machine Learning Systems That Sense and Act*).  
**Kit** = **TinyAgents Kit** (Arduino UNO Q dual-brain: MPU proposes, MCU permits).  
**Project** = one team TinyAgent + design dossier.  
**Host (planned):** e.g. `physical.mlsysbook.ai` (alias `phys.mlsysbook.ai` OK).

> TinyML taught you to deploy a model. TinyAgents teaches you to build an intelligent machine.

---

## What you learn

**Outcome.** Design, measure, and defend a TinyAgent so a learned proposal may
produce physical action only through independent permission, with an
evidence-backed **deploy / condition / refuse** stance.

**Primitives you exercise (the “click together” set):**

| | |
| --- | --- |
| **Loop** | Action changes the next observation |
| **Time** | How old may belief be when the move happens? |
| **Budget** | Shared latency, energy, memory, link |
| **Permission** | What may refuse a capable proposal? |
| **Evidence** | What measurement supports the claim or release? |

**Not this course:** robotics survey, VLM/VLA catalog, LLM-agent chat lab,
TinyML “fit a model to an MCU” alone (that is adjacent heritage, not the endpoint).

**Prereq suggestion:** intro ML systems (models as components; measurement).  
Embedded/real-time helps. Do **not** require a prior “agentic ML” course.

---

## How the course is organized

Project-based seminar shape (standard at places like ETH for P&S / project
work—not a classic exam lecture, not a pure paper seminar):

```text
Proposal → build on kit → midterm demo → harden → release case → final defense + dossier
```

| Contact | Role |
| --- | --- |
| **Weekly seminar block** (~2 h) | Shared method; critique; midterm/final talks |
| **Studio / kit time** | Most of the work—team build |
| **Book chapters** | Read when the project needs them (not “one chapter = one week exam”) |
| **Labs folder** | Phenomenon contracts and kit realizations for the *same* spine |

```text
Block I   Foundations           book Ch 1–4     early seminar
Block II  Building a TinyAgent  book Ch 5–10    project + midterm
Block III Responsibility        book Ch 11–13   late seminar
Capstone  Defend                design review   final talk + report
```

Chapter-by-chapter *authoring* depth (section jobs, every optional lab):
[`TEACHING-FLOW.md`](TEACHING-FLOW.md). That is **not** a second course—it is
detail under this one schedule.

---

## Who follows how

### Enrolled (graded)

Teams of **2–3**. Named roles: MPU · MCU · measurement/evidence.  
Grade example: process 20% · midterm 15% · final talk 25% · dossier 40%.  
Pass signal: real MCU permission path; measured end-to-end claim; evidence-backed
release verdict; each person can explain dual-brain without slides.

### Open follow-along (welcome)

1. Get (or emulate) dual-brain kit per [`labs/`](../labs/).  
2. Form a team or go solo with reduced scope.  
3. Run the **same weeks and milestones** below (self-paced allowed; keep order).  
4. Write the **same design dossier**.  
5. Optional: publish a short “ship memo” + demo video under the course name.

No separate “Arduino curriculum PDF.” **This page + the book + `labs/`** is what
partners point to.

---

## 14-week schedule

| Week | Seminar (cohort) | Project work | Milestone |
| ---: | --- | --- | --- |
| **1** | Kickoff: scope, TinyAgent, dual-brain, kit, teams | Bring-up; pick shared-workspace micro-task | **T0** roster + kit |
| **2** | Physical AI boundary; world costs; how to propose | Loop charter; advisory vs closed-loop | **T1 proposal** |
| **3** | Measuring the loop (both brains) | End-to-end instrumentation | — |
| **4** | Continuous runtime; MPU fail → MCU continues | Fault containment | **T2 foundations** |
| **5** | Observe → estimate (thin state/world-model depth) | Perception + belief on MPU | — |
| **6** | Intent as proposal; enforcer preview | Intent schema; enforcer draft | — |
| **7** | **Midterm presentations** | Refine from critique | **T3 midterm** |
| **8** | Studio clinic (permission hardening) | Refuse / recover path solid | — |
| **9** | Placement + evidence (short) | Optional re-host stress | — |
| **10** | Authority + one learning turn | Stop/revoke; admit/reject data | — |
| **11** | Release workshop | Ship / condition / refuse draft | **T4 release draft** |
| **12** | Dry-run (optional) | Freeze dossier | — |
| **13** | **Final design-review talks** | — | **T5 final** |
| **14** | Buffer / debrief / return kits | — | **T6 dossier** |

**Forced kit experiences** (order fixed; timing can flex slightly):

| | When | Lab DNA |
| --- | --- | --- |
| Bring-up | W1 | `labs/00-kit-bringup` |
| Loop + freshness | W2 | `01` + `02` |
| Measure both brains | W3 | `03` |
| Runtime continuity | W4 | `04` |
| Belief + intent | W5–6 | `06` + `07` |
| MCU enforcer | W6–8 | `08` (signature) |
| Place/qualify (light) | W9 | `09`/`10` |
| Authority + ship | W10–11 | `11`, `13` |
| Defend | W13 | `99` |

---

## Milestones (everyone—enrolled or open)

### T1 — Proposal (week 2)

Task/world · loop charter · requirements sketch · risks · roles.  
≈ book Ch 1–2.

### T2 — Foundations (week 4)

Advisory vs closed-loop documented · end-to-end measurement · MCU continues under
MPU hang. ≈ Ch 1–4.

### T3 — Midterm (week 7)

Working observe → propose ⇢ **permit** → act · one measured design-changing claim ·
honest failure list · contribution split on slide 1. ≈ Ch 5–8 in progress.

### T4 — Release draft (week 11)

Promotion history · residual risk · authority map · provisional ship verdict.

### T5 — Final talk (week 13)

Design review: loop, time, budget, permission, evidence, authority; optional
seeded fault.

### T6 — Written dossier (week 14)

The course report **is** the cumulative design dossier (not a second novel):

| Dossier piece | Book |
| --- | --- |
| Loop charter | 1 |
| Requirements ledger | 2 |
| Evidence record | 3 |
| Runtime skeleton | 4 |
| Observation + state contracts | 5–6 |
| Intent + enforcement | 7–8 |
| Placement + promotion (as done) | 9–10 |
| Authority + learning rules | 11–12 |
| Release case | 13 |
| Failure diagnosis | Capstone |

---

## Curriculum = this course (no dual maintenance)

| You need | Open this |
| --- | --- |
| **Syllabus / week plan / how to follow** | **This file (`COURSE.md`)** |
| Chapter jobs & full optional lab menu | `TEACHING-FLOW.md` (detail under the same spine) |
| Full section-level contracts for writing chapters | `CHAPTER-OUTLINES.md` (authoring) |
| Book constitution | `BOOK-GOAL.md` |
| Brand / TinyAgent definition | `BRAND.md` |
| Kit ownership & lab dirs | `labs/README.md` |
| Optional other institution: pure lecture+lab | `SEMESTER-PACK.md` (not the default story) |

**Rule:** If the public course changes, edit **this file first**. Propagate into
book preface and kit only if the *offer* changed—not a weekly dual rewrite of
“syllabus doc” and “curriculum doc.”

---

## Staffing (enrolled offering)

| Role | Owns |
| --- | --- |
| Course steward | Seminar blocks, milestones, grade |
| Postdoc / TA | Kit checkpoints, studio, T2 sign-off |
| Book steward | Chapter + lab *contracts* match this course |

Cap teams to kit/TA capacity (often 8–12 teams).

---

## Catalogue blurb (copy-paste)

> **Physical AI Systems.** Open project-based course on engineering learned
> components that sense and act under constraint. Teams build a TinyAgent on the
> TinyAgents Kit (dual-brain: MPU proposes, MCU permits). Shared sessions cover
> foundations and key methods; grade (or self-certificate) via proposal, midterm,
> final design-review talk, and design dossier. Not a robotics survey; not an
> LLM-agents lab. Materials free to follow with the book and kit.

**ETH-shaped notes (local):** P&S/group-project scale is a reasonable band
(~150–180 h / student if ~6 ECTS); confirm catalogue. Same public path for open
learners without credit.
