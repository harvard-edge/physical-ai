# Brand and identity

## Hierarchy (accepted)

| Layer | Name | Role |
| --- | --- | --- |
| **Course (public)** | **Physical AI Systems** | One open project-based course—ETH or follow-along. Syllabus = curriculum spine: [`COURSE.md`](COURSE.md) |
| Book | *Physical AI: Machine Learning Systems That Sense and Act* | Method library for the same course |
| Kit (Arduino product) | **TinyAgents Kit** | Reference body for the course project (UNO Q dual-brain) |
| Technical signature | **Dual-brain architecture** | MPU proposes; MCU permits; independent physical authority |
| Site (planned) | `physical.mlsysbook.ai` | Host the course + book; `phys` may redirect |

Tagline for kit and partner materials:

> TinyML taught you to deploy a model. TinyAgents teaches you to build an intelligent machine.

## One course, not two products

Do **not** maintain a separate “syllabus for ETH” and “curriculum for material
development.” Partners (Arduino, etc.) and enrolled students use the **same**
`COURSE.md` path. Chapter outlines and lab contracts are *build details under
that course*, not a second program.

## What “agent” means here

An **agent** is the **complete engineered system**: sensing, representation, state, memory, policy, tools, scheduling, communication, energy awareness, enforcement, actuation, evidence, and human authority.

It is **not**:

- a chat loop or unconstrained tool-using LLM;
- “TinyML plus a large language model”;
- a claim that the model is autonomous authority over actuators.

The learned component remains an **unverified proposal service**. Physical permission is engineered separately—on the TinyAgents Kit, by the MCU side of the dual-brain split.

## Dual-brain architecture

The UNO Q’s Linux **MPU** and real-time **MCU** are not a gimmick; they make a durable systems distinction **physical and teachable**:

| Domain | Responsibility |
| --- | --- |
| MPU (rich, best-effort) | Perception, state, VLMs/VLAs/policies, planning, tools, logs |
| MCU (trusted real-time) | Timing-critical loops, watchdogs, limits, command validation, safe fallback |
| Boundary | Timestamped, expiring **intent proposals** cross from MPU to MCU; MCU may **permit, refuse, interrupt, or recover** |

This boundary is a **teaching realization** of proposal vs permission (runtime-assurance lineage). It is not a complete industrial safety certification claim.

Course and book remain **platform-neutral** in concepts; the kit is the **reference realization**.

## Partner packaging

- **Public course page / store story:** Physical AI Systems · follow the open schedule  
- **Arduino / kit box:** TinyAgents Kit · lab body for Physical AI Systems  
- **Manuscript:** Physical AI (subtitle unchanged)  
- **Repo:** one course (`COURSE.md`) + book + `labs/`

Do not rename the book “TinyAgents.” Do not brand the course as a robotics survey.
