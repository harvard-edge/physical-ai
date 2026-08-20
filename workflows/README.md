# Physical AI — Claude workflows

Project-local agent workflows. They are **prompts with gates**, not CI.

| Workflow | When to use |
| :--- | :--- |
| [`section-bullet-expand.md`](section-bullet-expand.md) | **Architect** lays out what/how (bullets); **agent** is the textbook author who turns approved bullets into flowing CMOS prose and iterates |

## Division of labor

- **You (architect):** what must be expressed, how to express it, approval.  
- **Agent (textbook author):** materialize approved bullets into prose; make paragraphs and sections flow; improve until it reads like a textbook—without inventing new curriculum.

## How to invoke

- `run section-bullet-expand on chapter 2`  
- `/section-craft book/chapters/02-constraints/02-constraints.qmd`  
- Supply architect intent in the same message (“this section must teach… fence CBF… kit-scale SI…”), then wait for bullets  

The agent must **read the workflow first**, capture an **Architect brief**, and **not** expand `.qmd` prose until bullets are approved.
