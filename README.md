# Physical AI

**Course:** [Physical AI Systems](docs/COURSE.md) — open project-based offer (enrolled or follow-along)  
**Book:** *Physical AI: Machine Learning Systems That Sense and Act*  
**Kit:** **TinyAgents Kit** on Arduino UNO Q (dual-brain: MPU proposes, MCU permits)

> TinyML taught you to deploy a model. TinyAgents teaches you to build an intelligent machine.

**One public product.** The course syllabus *is* the taught curriculum. There is
no separate “partner curriculum” to maintain. Arduino and open learners use the
same schedule, milestones, book, and labs as an enrolled cohort.

Planned site: `physical.mlsysbook.ai` (short alias `phys.mlsysbook.ai` optional).

This repository is the **course + book + kit labs**. Older prototypes live in
[`../PhysicalAI-prototypes`](../PhysicalAI-prototypes). Brand: [`docs/BRAND.md`](docs/BRAND.md).

## Start here

| You are… | Open |
| --- | --- |
| Student / open learner / partner | **[`docs/COURSE.md`](docs/COURSE.md)** |
| Writing a chapter | [`docs/TEACHING-FLOW.md`](docs/TEACHING-FLOW.md) + [`docs/CHAPTER-OUTLINES.md`](docs/CHAPTER-OUTLINES.md) |
| Building kit firmware | [`labs/README.md`](labs/README.md) |
| Checking settled decisions | [`docs/DECISIONS.md`](docs/DECISIONS.md) |

## Layout

| Path | Role |
| --- | --- |
| `docs/COURSE.md` | **Public syllabus = curriculum** |
| `book/` | Quarto manuscript (method library) |
| `book/chapters/NN-slug/` | Chapter entry + figures |
| `labs/` | TinyAgents Kit contracts and realization |
| `docs/` | Authoring control (goal, outlines, brand) |
| `authoring/`, `tools/` | Book production helpers |

## Book build

```bash
cd book
quarto preview    # HTML
quarto render     # HTML + PDF
```
