# Semester pack — lecture + structured labs (optional)

**Status:** optional format only  
**Default public course:** [`COURSE.md`](COURSE.md) (project-based; enrolled or open follow-along)  
**Full chapter map:** `TEACHING-FLOW.md`  

Use this pack only if an institution wants a classical lecture + multi-lab
sequence. Partners and the default offer should point at **COURSE.md**, not this
file.

---

## Design rules (from review)

1. **Book ≠ week count.** Thirteen chapters remain in the manuscript; the semester does not run thirteen peer-weight kit nights.
2. **~7 kit contact points** (bring-up + teaching sessions + integration that feeds the defense). Analytical / dossier work fills the rest.
3. **Pair on the calendar, not by deleting theory.** Propose before permit stays two chapters; one lab window can cover both.
4. **Never cut** measure (Ch 3), runtime continuity (Ch 4), or independent enforcement (Ch 8) from the kit path.
5. **Capstone = defense**, not new machinery. Ship-gate memo is the integration checkpoint; design review is the graded transfer event.
6. Every kit session ships a **starter checkpoint** so a broken prior week does not strand the cohort.

---

## At a glance

| Mode | What students touch |
| --- | --- |
| **Lecture / read** | All chapters 1–13 + final design review material |
| **Kit (default pack)** | Bring-up + L1…L6 lab windows below |
| **Dossier** | Every chapter still contributes an artifact (see table) |
| **Full kit menu** | Optional / self-study / long form — remains under `labs/` |

### Kit sessions in this pack

| Session | Covers chapters | Lab dirs used |
| --- | --- | --- |
| **0 Bring-up** | — | `00-kit-bringup` |
| **L1 Loop & freshness** | 1–2 | `01-close-the-loop` + `02-freshness-wall` (one window, two stations or sequenced) |
| **L2 Measure both brains** | 3 | `03-measure-both-brains` |
| **L3 Runtime fault containment** | 4 | `04-runtime-fault-containment` |
| **L4 Observation & belief** | 5–6 | Prefer `06-belief-drift` with sensing knobs from `05-perception-frontier` (one station); or short 05 then 06 same week |
| **L5 Propose then permit** | 7–8 | `07-two-speed-intent` → `08-mcu-enforcer` (same week or back-to-back lab slots) |
| **L6 Place & qualify** | 9–10 | `09-placement-ripple` then immediate `10-shadow-and-faults` criteria on the new placement |
| **L7 Authority & lineage** | 11–12 | Thin kit or logs: `11-authority-paths` + refuse-bad-trajectory from `12-learning-turn` |
| **L8 Ship → defend** | 13 + review | `13-ship-gate` checkpoint; `99-design-review` graded |

If one contact hour must disappear first, drop **L7 kit** to pure procedural (paper authority map + log-based learning refuse) and keep **L5** and **L8**.

---

## 14-week schedule (default)

Assumes one main lecture block per week + one lab block where marked. Adjust offsets to local calendar; keep **ordering**.

| Week | Block | Read / teach | Kit / lab | Dossier updates (min) |
| ---: | --- | --- | --- | --- |
| **0** | Setup | Syllabus, brand, dual-brain preview; kit distribution | **Session 0:** `00-kit-bringup` (safe idle, link, sensors, actuators) | Board / pin map signed off |
| **1** | I | **Ch 1** From ML Systems to Physical AI | — (read + charter draft on paper) | Loop charter v0 |
| **2** | I | **Ch 2** What the Physical World Costs | **L1:** close-the-loop + freshness wall | Charter locked; requirements ledger |
| **3** | I | **Ch 3** Measuring a Moving System | **L2:** measure both brains | Evidence record |
| **4** | I | **Ch 4** A Runtime That Must Keep Running | **L3:** runtime fault containment | Runtime skeleton · **Foundations gate** |
| **5** | II | **Ch 5** Perception Under a Deadline | Sensing contract on paper / light acquisition if needed | Observation contract |
| **6** | II | **Ch 6** State, Time, and World Models | **L4:** belief drift (+ perception knobs) | State / timing model |
| **7** | II | **Ch 7** From Meaning to Intent | Start **L5:** two-speed intent (proposals only) | Intent contract draft |
| **8** | II | **Ch 8** Keeping Action Within Limits | **L5 cont.:** MCU enforcer · **signature midpoint** | Enforcement design |
| **9** | II | **Ch 9–10** Where Intelligence Runs + Building Confidence | **L6:** placement ripple → shadow/faults qualify | Placement map; promotion record |
| **10** | III | **Ch 11–12** Human Authority + Learning From Interaction | **L7:** authority paths + learning refuse (thin kit OK) | Authority map; change record |
| **11** | III | **Ch 13** Ready to Deploy? | **L8a:** ship-gate run + ship/condition/refuse memo | Release case |
| **12** | Capstone | Final design review material · transfer task assigned | Rehearsal / fault seed | Dossier freeze for defense |
| **13** | Capstone | Defense week (oral or written) | **L8b:** `99-design-review` | Graded defense |
| **14** | Buffer | Overflow defenses · optional enrichment (full lab menu) | Optional deep-dives | — |

**Notes for local timing**

- If **no week 0**, fold bring-up into week 1 lab and keep Ch 1 analytical that week.  
- If **only one lab slot for Ch 7–8**, teach Ch 7 Monday / Ch 8 Wednesday, **L5 single long session** after both lectures.  
- Weeks **12–13** can collapse to one exam week; do not skip ship-gate evidence before defense.  
- **Enrichment** uses unused lab dirs (`05` alone, fuller `12`, etc.) as optional homework, not graded critical path.

---

## What each week must still produce (dossier)

Even without a kit that day, the chapter decision is required.

| Ch | Artifact (always) | In pack: kit required? |
|---:|---|---|
| 1 | Loop charter | No (week 1 paper); validated in L1 |
| 2 | Requirements ledger | L1 |
| 3 | Evidence record | L2 |
| 4 | Runtime skeleton | L3 |
| 5 | Observation contract | Prefer L4; else analytical frontier from traces |
| 6 | State / timing model | L4 |
| 7 | Intent contract | L5 |
| 8 | Enforcement design | L5 |
| 9 | Placement + resource ledger | L6 |
| 10 | Promotion record | L6 |
| 11 | Authority map | L7 or procedural |
| 12 | Change / admit-reject record | L7 or log exercise |
| 13 | Release case | L8a |
| Review | Full defense | L8b |

---

## Course gates (pass criteria on the path)

| Gate | After | Must show |
| --- | --- | --- |
| **G0 Kit ready** | Session 0 | Safe idle; MPU–MCU heartbeat; no stuck actuators |
| **G1 Loop real** | L1 | Same model advisory vs closed-loop documented |
| **G2 Measured** | L2 | End-to-end distribution + one decision-changing tail |
| **G3 Foundations** | L3 | MCU continuity under MPU hang |
| **G4 TinyAgent mid** | L5 | Intent expiring **and** MCU refuse path |
| **G5 Composed** | L6 | One re-placement with re-qualified evidence |
| **G6 Responsible** | L7 / Ch 11–12 | Named authority + reject of bad lineage |
| **G7 Release** | L8a | Ship / condition / refuse with cited evidence |
| **G8 Capstone** | L8b | Transfer + diagnosed failure on the dossier |

---

## Mapping: full lab catalogue → pack

| Lab dir | Full catalog | Semester pack default |
| --- | --- | --- |
| `00-kit-bringup` | Optional | **Required session 0** |
| `01-close-the-loop` | Own week | **L1** (with 02) |
| `02-freshness-wall` | Own week | **L1** (with 01) |
| `03-measure-both-brains` | Own week | **L2** |
| `04-runtime-fault-containment` | Own week | **L3** |
| `05-perception-frontier` | Own week | Folded into **L4** or analytical |
| `06-belief-drift` | Own week | **L4** primary |
| `07-two-speed-intent` | Own week | **L5** first half |
| `08-mcu-enforcer` | Own week | **L5** second half |
| `09-placement-ripple` | Own week | **L6** first half |
| `10-shadow-and-faults` | Own week | **L6** second half |
| `11-authority-paths` | Own week | **L7** thin |
| `12-learning-turn` | Optional | **L7** log / refuse exercise |
| `13-ship-gate` | Integration | **L8a** |
| `99-design-review` | Capstone | **L8b** |

---

## Lecture pacing hint (without rewriting the book)

| Weeks | Emphasize in live lecture |
| --- | --- |
| 1–2 | Scope tests; endogeneity; world clocks |
| 3–4 | Claims vs components; multi-rate; MPU hang demo |
| 5–6 | Observe then believe; **thin** estimators / world-models |
| 7–8 | Interfaces and permission only; minimal VLM/VLA zoo |
| 9 | Shared budgets + evidence death when you move compute |
| 10 | Authority ops + one learning turn (not MLOps encyclopedia) |
| 11–14 | Integration judgment and transfer |

---

## Variants

| Variant | Change |
| --- | --- |
| **12-week trim** | Drop week 14; merge weeks 12–13; L7 procedural only |
| **Long form / book club** | TEACHING-FLOW full kit defaults; one lab dir per chapter where listed |
| **No hardware** | All L1–L8 as analytical + hosted; same gates and dossier |
| **Partner demo day** | Showcase L3 + L5 only; do not sell as full curriculum |

---

## Ownership

| Role | Owns on this pack |
| --- | --- |
| Course steward | Week plan, gates, grading of dossier + defense |
| Book steward | Chapter integrity; TEACHING-FLOW jobs |
| Postdoc / kit | Starter checkpoints for **L1–L6 and L8**; thin L7 scripts |
| Student | Predictions, measurements, diagnosis, decisions, defense |

Do not start firmware for a pack session until that lab’s `CONTRACT.md` is accepted.
