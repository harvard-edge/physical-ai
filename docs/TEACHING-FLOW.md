# Teaching map — blocks, chapters, labs

**Status:** part-level organization and lab placement for Physical AI Systems  
**Book:** *Physical AI: Machine Learning Systems That Sense and Act*  
**Kit:** TinyAgents Kit (UNO Q dual-brain: MPU proposes, MCU permits)  
**Detail contracts:** `CHAPTER-OUTLINES.md` · **Brand:** `BRAND.md`  
**Public course (syllabus = curriculum):** [`COURSE.md`](COURSE.md)  
**Author detail under that course:** this file + `CHAPTER-OUTLINES.md`  
**Optional lecture+lab only:** [`SEMESTER-PACK.md`](SEMESTER-PACK.md)

---

## Two tracks (read this first)

| Track | Use when | Shape |
| --- | --- | --- |
| **Course (default, public)** | Enrolled **or** open follow-along | [`COURSE.md`](COURSE.md) — one project seminar path |
| **Lecture pack (optional)** | Pure lecture + structured labs | [`SEMESTER-PACK.md`](SEMESTER-PACK.md) |
| **Full map (below)** | Chapter authoring / self-study depth | Per-chapter jobs + full lab menu |

The book has thirteen teaching chapters + design review. The **course** does not
run thirteen peer-weight kit nights—it runs the project path in `COURSE.md`.

---

## Shape of the course

Three teaching blocks, then a capstone. Students learn how to *compose* a
TinyAgent, then **demonstrate** one end-to-end.

```text
Block I — Foundations          (Ch. 1–4)
Block II — Building a TinyAgent (Ch. 5–10)
Block III — Responsibility     (Ch. 11–13)
Capstone — Defend the system   (Final design review)
```

**Chapter rule.** Every chapter is conceptually complete before any kit work.
**Lab rule.** Not every chapter needs a full kit session. A lab belongs where a
*physical* or *cross-brain* phenomenon makes the concept hard to fake on paper.
Some chapters are **read/analyze only**; some share a **paired lab** after two
chapters; the capstone **integrates** prior evidence rather than inventing new theory.

**Pre-course / week 0 (optional kit):** `labs/00-kit-bringup` — board, sensors,
actuators, MPU–MCU link, safe idle. Not a book chapter. Required in the
semester pack.

**Cumulative artifact.** One design dossier. Each chapter adds a named piece
whether or not hardware was touched that week.

---

## Fundamentals the course installs

Students leave able to click these together (TinyML installed “fit model to
device”; this course installs “stand behind a machine that may act”):

| Super-primitive | Question |
| --- | --- |
| **Loop** | Does action change the next observation? |
| **Time** | How old may belief be when the move happens? |
| **Budget** | What is shared among sensing, inference, link, actuation? |
| **Permission** | What may refuse a capable proposal? |
| **Evidence** | What measurement supports the claim or the release? |

---

# Block I — Foundations

**Job of the block.** Move the student from “I deploy models” to “I engineer a
continuous physical loop I can measure and that keeps running when intelligence
fails.” Dual-brain appears as *architecture skeleton*, not full TinyAgent yet.

---

### Chapter 1 — From ML Systems to Physical AI

| | |
| --- | --- |
| **Job** | Decide when a learned system is *physical AI*: learned component + consequential physical feedback + delegated authority. Draw the causal boundary. |
| **Decision / dossier** | In / out of scope; **loop charter**. |
| **Lab** | **Yes — kit.** `labs/01-close-the-loop`. Same model advisory vs closed-loop; action changes later observations; name who holds physical authority. |

---

### Chapter 2 — What the Physical World Costs

| | |
| --- | --- |
| **Job** | Derive operating requirements from world timescales, information age, consequence, and interacting budgets—not from board marketing. |
| **Decision / dossier** | Operating regime; **requirements ledger**. |
| **Lab** | **Yes — kit.** `labs/02-freshness-wall`. Raise observation age; show efficacy fall; choose faster / predict / less authority / refuse. |

*Optional pairing:* If the semester is tight, Ch. 1–2 can share one long lab day (charter + freshness wall as two stations). Prefer separate when first week energy allows.

---

### Chapter 3 — Measuring a Moving System

| | |
| --- | --- |
| **Job** | Turn claims about the running loop into instruments, distributions, uncertainty, task floors, and verdicts (accept / narrow / reject). |
| **Decision / dossier** | Measurement plan; **evidence record**. |
| **Lab** | **Yes — kit (signature for dual-brain metrology).** `labs/03-measure-both-brains`. End-to-end path vs component timers; decision-changing latency tail. |

---

### Chapter 4 — A Runtime That Must Keep Running

| | |
| --- | --- |
| **Job** | Design multi-rate continuous services, ownership, proposal boundary (MPU → MCU), and failure as an operating mode—not request/response ML serving. |
| **Decision / dossier** | Cadences and ownership; **runtime skeleton**. |
| **Lab** | **Yes — kit.** `labs/04-runtime-fault-containment`. Hang/delay MPU policy; MCU continues watchdog / safe idle. Closes Block I. |

---

# Block II — Building a TinyAgent

**Job of the block.** Install every functional piece of the agent: observe,
estimate, propose, independently permit, place under shared budgets, qualify
with evidence. Students build *one* accumulating TinyAgent on the kit (with
checkpoints so a broken week does not strand them).

---

### Chapter 5 — Perception Under a Deadline

| | |
| --- | --- |
| **Job** | Treat sensing as a designed service: what to acquire, when, at what cost, before belief goes stale. |
| **Decision / dossier** | Sensing operating point; **observation contract**. |
| **Lab** | **Yes — kit.** `labs/05-perception-frontier`. Quality–age–energy–bandwidth frontier. |

---

### Chapter 6 — State, Time, and World Models

| | |
| --- | --- |
| **Job** | Separate observation from state. Frames, clocks, uncertainty, innovate/correct; what must stay valid now. |
| **Decision / dossier** | State schema and validity horizon; **state / timing model**. |
| **Lab** | **Yes — kit.** `labs/06-belief-drift`. Inject frame/clock error; show disagreement; MCU min safety state independent of MPU belief. |

---

### Chapter 7 — From Meaning to Intent

| | |
| --- | --- |
| **Job** | Treat VLMs / VLAs / policies as **proposal interfaces**: grounding, action representation, two speeds, expiring intent—never direct actuation. |
| **Decision / dossier** | Policy interface; **intent contract**. |
| **Lab** | **Yes — kit (no actuation).** `labs/07-two-speed-intent`. Fast vs slow proposals; validity horizon; proposals only. |

---

### Chapter 8 — Keeping Action Within Limits

| | |
| --- | --- |
| **Job** | Separate intent from motion; independent checks, skill limits, recovery modes. Technical depth of dual-brain permission. |
| **Decision / dossier** | Skills and checks; **enforcement design**. |
| **Lab** | **Yes — kit (signature lab).** `labs/08-mcu-enforcer`. Invalid/stale/out-of-envelope refuse; MPU crash cannot bypass MCU. |

*Paired option:* Ch. 7+8 can be one extended lab week (proposals only day 1; enforcer day 2) if students struggle with “intent never drives PWM.” Prefer teaching both concepts first, then one long kit session.

---

### Chapter 9 — Where Intelligence Runs

| | |
| --- | --- |
| **Job** | Place every service under shared latency, energy, memory, bandwidth, and failure domains; one move ripples. |
| **Decision / dossier** | **Placement map** + resource ledger. |
| **Lab** | **Yes — kit or hybrid.** `labs/09-placement-ripple`. Move one capability (e.g. perception or policy host); measure ripple. Analytical replay of prior traces is acceptable if kit time is scarce. |

---

### Chapter 10 — Building Confidence Before Deployment

| | |
| --- | --- |
| **Job** | Evidence tiers: what each test justifies; invalidation; shadow and fault injection criteria *before* scores; promote / hold / reject. |
| **Decision / dossier** | **Promotion record**. |
| **Lab** | **Yes — kit (or hosted + kit faults).** `labs/10-shadow-and-faults`. Shadow policy vs allowed action; inject MPU/link/MCU faults. Closes Block II. |

*Paired option:* Ch. 9–10 as one “composition week”: placement change *then* re-qualification so students feel that moving compute invalidates prior evidence.

---

# Block III — Responsibility

**Job of the block.** The machine is buildable; now the student learns who may
authorize it, when it may learn from interaction, and how to accept or refuse
deployment. Concepts first; labs can be lighter on new firmware, heavier on
procedure and evidence.

---

### Chapter 11 — Human Authority

| | |
| --- | --- |
| **Job** | Design teach / approve / interrupt / revoke / inspect / forget as operational paths with scope and time—not a generic “human in the loop” slogan. |
| **Decision / dossier** | **Authority map**. |
| **Lab** | **Prefer kit procedure, can be thin firmware.** `labs/11-authority-paths`. Approve gate, MCU hard stop, revoke, inspect, forget on retained segment. |

---

### Chapter 12 — Learning From Interaction

| | |
| --- | --- |
| **Job** | Only authorized, lineage-clean trajectories become data; candidate updates with evaluation and rollback; policy shapes its own dataset. |
| **Decision / dossier** | Admit/reject experience; **change record**. |
| **Lab** | **Optional kit / strong analytical.** `labs/12-learning-turn` if capturing cross-brain trajectories is feasible; otherwise replay dossiers + refuse bad lineage on logs. Do not invent new learning theory here. |

*Paired option:* Ch. 11–12 as one responsibility lab: no write without consent; no update without authority path exercised.

---

### Chapter 13 — Ready to Deploy?

| | |
| --- | --- |
| **Job** | Integrate the dossier into a release case: residual risk, monitoring, owners, conditions; **deploy / condition / refuse**. No new subsystems—only judgment. |
| **Decision / dossier** | **Release case**. |
| **Lab** | **Integration lab (feeds capstone).** `labs/13-ship-gate`. Run the assembled TinyAgent; plant or use a known stress; write a ship/no-ship memo with evidence from earlier labs. |

---

# Capstone — Defend the system

**Job.** Transfer. No new chapter theory. Unfamiliar task and/or injected
failure; hypothesis → bisect → confirm; oral/written defense of loop, time,
budget, permission, evidence, authority, and release stance.

| | |
| --- | --- |
| **Manuscript** | Final design review (`99-review`). |
| **Lab** | `labs/99-design-review` — builds on ship-gate evidence; instructor or self-injected fault. |

---

## Lab policy (read this once)

| Pattern | When to use |
| --- | --- |
| **Course (default)** | Project path and forced kit experiences in [`COURSE.md`](COURSE.md) |
| **Lecture pack (optional)** | Paired L1–L8 in [`SEMESTER-PACK.md`](SEMESTER-PACK.md) |
| **One chapter → one kit lab** | Full map / self-study when a single phenomenon needs its own night |
| **Two chapters → one lab window** | Semester default for 1–2, 5–6, 7–8, 9–10, 11–12 |
| **Chapter without kit** | Paper/analytical that week; artifact still due |
| **Analytical / hosted double** | Always acceptable parallel to kit; same decision and dossier artifact |
| **Checkpoint** | Every *kit* lab ships a starter so a failed prior week does not block the next |

**Not assumed:** 13 equally heavy hardware sessions. **Assumed for teaching:** the
semester pack finishes the dossier and capstone defense without burning the
cohort on parallel firmware every week.

---

## Master map (at a glance)

| Ch | Title | Block | Full-map lab | Semester pack |
|---:|---|---|---|---|
| 1 | From ML Systems to Physical AI | I Foundations | `01-close-the-loop` | Paper W1 → **L1** with Ch 2 |
| 2 | What the Physical World Costs | I | `02-freshness-wall` | **L1** |
| 3 | Measuring a Moving System | I | `03-measure-both-brains` | **L2** |
| 4 | A Runtime That Must Keep Running | I | `04-runtime-fault-containment` | **L3** |
| 5 | Perception Under a Deadline | II TinyAgent | `05-perception-frontier` | Fold into **L4** |
| 6 | State, Time, and World Models | II | `06-belief-drift` | **L4** |
| 7 | From Meaning to Intent | II | `07-two-speed-intent` | **L5** (with 8) |
| 8 | Keeping Action Within Limits | II | `08-mcu-enforcer` | **L5** |
| 9 | Where Intelligence Runs | II | `09-placement-ripple` | **L6** (with 10) |
| 10 | Building Confidence Before Deployment | II | `10-shadow-and-faults` | **L6** |
| 11 | Human Authority | III Responsibility | `11-authority-paths` | **L7** thin |
| 12 | Learning From Interaction | III | `12-learning-turn` | **L7** |
| 13 | Ready to Deploy? | III | `13-ship-gate` | **L8a** |
| — | Final design review | Capstone | `99-design-review` | **L8b** |

---

## Folder slugs

`01-frame` · `02-costs` · `03-measure` · `04-runtime` · `05-perception` ·
`06-state` · `07-intent` · `08-limits` · `09-placement` · `10-assurance` ·
`11-authority` · `12-learning` · `13-deploy` · `99-review`
