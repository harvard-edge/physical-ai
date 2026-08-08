# TinyAgents Kit Labs

Physical realization of *Physical AI: Machine Learning Systems That Sense and
Act* on the **TinyAgents Kit** (Arduino UNO Q: Linux MPU + real-time MCU).

Brand hierarchy: field/course **Physical AI Systems** · book above · product
**TinyAgents Kit**. See [`docs/BRAND.md`](../docs/BRAND.md).

This folder is owned by the postdoc for kit bring-up, firmware, starter
checkpoints, wiring, and lab write-ups. The book steward owns the learning
objective, phenomenon, evidence, and decision contract for every lab. Hardware
implements pedagogy; it does not invent it.

## Ownership

| Role | Owns |
| --- | --- |
| Book steward | Chapter concept, lab contract (phenomenon, prediction, perturbation, measurement, failure, decision, dossier update) |
| Postdoc | UNO Q realization: wiring, MPU/MCU code, starter checkpoints, assembly guides, validation on hardware |
| Learner | Prediction, measurement, diagnosis, engineering decision, dossier update |

## Dual-brain invariant (kit signature)

The dual-brain split is the technical depth of the kit—not branding fluff.

- **MPU** proposes: perception, state, policy (including VLMs/VLAs as components), planning, tools, logging.
- **MCU** permits: timing-critical sensing/actuation where required, watchdogs, limits, command validation, safe fallback, final physical authority.
- Messages: typed, timestamped, expiring **intent** from MPU; MCU may permit, refuse, interrupt, or recover.
- No peer, cloud service, or MPU process may bypass the receiving MCU enforcer.
- Teaching instrument for proposal vs permission (runtime-assurance lineage); not a complete safety certification.

## Taught formats

**Default (public):** [`docs/COURSE.md`](../docs/COURSE.md) — one project-based
course for enrolled and open/Arduino follow-along. Kit work is the team project
with forced experiences (measure, runtime continuity, enforcer).

**Optional lecture track:** [`docs/SEMESTER-PACK.md`](../docs/SEMESTER-PACK.md).

**Chapter author map:** [`docs/TEACHING-FLOW.md`](../docs/TEACHING-FLOW.md).

Do not invent a second lab syllabus for partners—the course *is* the curriculum.

### Semester pack sessions (lecture track only)

| Session | Weeks (typ.) | Chapters | Lab dirs |
| --- | --- | --- | --- |
| 0 Bring-up | 0 | — | `00-kit-bringup` |
| L1 Loop & freshness | 2 | 1–2 | `01` + `02` |
| L2 Measure both brains | 3 | 3 | `03-measure-both-brains` |
| L3 Runtime fault | 4 | 4 | `04-runtime-fault-containment` |
| L4 Observe & belief | 6 | 5–6 | `06` (+ knobs from `05`) |
| L5 Propose → permit | 7–8 | 7–8 | `07` then `08` |
| L6 Place & qualify | 9 | 9–10 | `09` then `10` |
| L7 Authority & lineage | 10 | 11–12 | `11` + light `12` |
| L8 Ship → defend | 11–13 | 13 + review | `13-ship-gate` → `99-design-review` |

### Full lab catalogue

| Dir | Book chapter | Lab focus | Semester role |
| --- | --- | --- | --- |
| `00-kit-bringup/` | — | Board, sensors, actuators, MPU–MCU link | Session 0 |
| `01-close-the-loop/` | 1 | Advisory vs actuating loop | L1 / seminar W2 |
| `02-freshness-wall/` | 2 | Efficacy vs information age | L1 / seminar W2 |
| `03-measure-both-brains/` | 3 | End-to-end timing across MPU and MCU | L2 / seminar W3 |
| `04-runtime-fault-containment/` | 4 | MPU failure, MCU continuity | L3 · Foundations gate / T2 |
| `05-perception-frontier/` | 5 | Sensing operating point | Folded into L4 / project |
| `06-belief-drift/` | 6 | State, frames, clocks, innovation | L4 / seminar W5–6 |
| `07-two-speed-intent/` | 7 | Reflex vs deliberation proposals | L5 / project |
| `08-mcu-enforcer/` | 8 | Independent action check and veto | L5 · signature / midterm |
| `09-placement-ripple/` | 9 | Re-place one capability; measure ripple | L6 / light in seminar |
| `10-shadow-and-faults/` | 10 | Shadow policy and fault injection | L6 / light in seminar |
| `11-authority-paths/` | 11 | Approve, stop, revoke, forget | L7 / seminar W10 |
| `12-learning-turn/` | 12 | Trajectory admission and candidate check | L7 light / seminar W10 |
| `13-ship-gate/` | 13 | Integrated deploy / refuse case | L8a / seminar W11 |
| `99-design-review/` | Final review | Transfer and diagnosed failure | L8b / final talk |

## Per-lab layout

Each lab directory should contain:

```text
NN-name/
  CONTRACT.md     # accepted pedagogy handoff from book steward
  README.md       # learner-facing bring-up and procedure (postdoc)
  mpu/            # Linux-side starter and student work
  mcu/            # real-time-side starter and student work
  checkpoint/     # tested starter snapshot for this chapter
  evidence/       # example logs, plots, schemas (no secrets)
```

Do not begin firmware until `CONTRACT.md` is accepted for that chapter.

## Shared code

`shared/` holds reusable MPU–MCU contracts, instrumentation helpers, and kit
utilities used by more than one lab. Prefer stable message schemas over
chapter-specific forks.

## Relation to the rest of the repo

Canonical public offer: `docs/COURSE.md`. Kit implements that course’s project.
Authoring detail: `docs/TEACHING-FLOW.md`, `docs/CHAPTER-OUTLINES.md`.
This folder is firmware and lab contracts only.
