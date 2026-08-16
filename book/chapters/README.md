# The Book Chapters & Architectural Spine

This directory contains the manuscript source files for the 11 substantive chapters and capstone defense of ***Physical AI: Machine Learning Systems That Sense and Act***.

Each chapter is organized in its own directory, with the main manuscript file matching the directory name (`NN-slug/NN-slug.qmd`) and localized visual assets in `figures/`.

---

## The 3 Parts and 12 Chapters

| Directory | Title | Part / Organ of the Agent | Dossier Artifact |
| :--- | :--- | :--- | :--- |
| `01-boundary/` | **Physical Causality** | Part I: The Physical Foundation | `Loop Charter` (`LOOP-01`) |
| `02-metrology/`| **Time and Latency** | Part I: The Physical Foundation | `Requirements Ledger` (`REQ-01`) |
| `03-runtime/`  | **Multi-Rate Systems** | Part I: The Physical Foundation | `Runtime Skeleton` (`RUN-01`) |
| `04-perception/`| **Perception** | Part II: The Agent Architecture | `Observation Contract` (`OBS-01`) |
| `05-state/`    | **Memory** | Part II: The Agent Architecture | `State and Timing Model` (`STATE-01`) |
| `06-intent/`   | **Reasoning** | Part II: The Agent Architecture | `Intent Schema` (`INTENT-01`) |
| `07-planning/` | **Planning** | Part II: The Agent Architecture | `Planning Schema` (`PLAN-01`) |
| `08-enforcement/`| **Reflex** | Part II: The Agent Architecture | `Enforcement Design` (`ENF-01`) |
| `09-placement/`| **Placement** | Part III: Integration and Release | `Placement Ledger` (`PLACE-01`) |
| `10-governance/`| **Governance** | Part III: Integration and Release | `Governance Record` (`AUTH-01`) |
| `11-assurance/`| **Release** | Part III: Integration and Release | `Deployment Case` (`REL-01`) |
| `99-capstone/` | **Capstone** | Capstone: Final System Defense | Final Release Defense |

---

## Chapter Directory Structure

```text
NN-slug/
  ├── NN-slug.qmd     # Chapter manuscript in Quarto markdown
  └── figures/        # Localized SVG, PNG, and sketch assets
      └── README.md
```
