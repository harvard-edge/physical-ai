# Chapters

Each teaching chapter is a folder. The entry file has the **same name as the folder** (not `index.qmd`). Figures live under `figures/`.

| Folder | Title (H1 in qmd) | Lab |
| --- | --- | --- |
| `01-frame/` | From ML Systems to Physical AI | `labs/01-close-the-loop/` |
| `02-costs/` | What the Physical World Costs | `labs/02-freshness-wall/` |
| `03-measure/` | Measuring a Moving System | `labs/03-measure-both-brains/` |
| `04-runtime/` | A Runtime That Must Keep Running | `labs/04-runtime-fault-containment/` |
| `05-perception/` | Perception Under a Deadline | `labs/05-perception-frontier/` |
| `06-state/` | State, Time, and World Models | `labs/06-belief-drift/` |
| `07-intent/` | From Meaning to Intent | `labs/07-two-speed-intent/` |
| `08-limits/` | Keeping Action Within Limits | `labs/08-mcu-enforcer/` |
| `09-placement/` | Where Intelligence Runs | `labs/09-placement-ripple/` |
| `10-assurance/` | Building Confidence Before Deployment | `labs/10-shadow-and-faults/` |
| `11-authority/` | Human Authority | `labs/11-authority-paths/` |
| `12-learning/` | Learning From Interaction | `labs/12-learning-turn/` |
| `13-deploy/` | Ready to Deploy? | `labs/13-ship-gate/` |
| `99-review/` | Final Design Review | `labs/99-design-review/` |

Layout per chapter:

```text
NN-slug/
  NN-slug.qmd    # manuscript
  figures/       # chapter images
```

Outline spine + kit lab mapping: [`docs/TEACHING-FLOW.md`](../../docs/TEACHING-FLOW.md).

Labs stay in repo-root `labs/` (postdoc kit track), not inside these folders.
