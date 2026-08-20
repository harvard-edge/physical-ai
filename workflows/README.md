# Physical AI — Claude workflows

Project-local agent workflows. They are **prompts with gates**, not CI.

| Workflow | When to use |
| :--- | :--- |
| [`section-bullet-expand.md`](section-bullet-expand.md) | **Architect** lays out what/how (bullets); **agent** is the textbook author who expands approved bullets into CMOS prose, then may run an **Alley revision pass** (structure → precision → flow → cut) |

## Division of labor

- **You (architect):** what must be expressed, how to express it, approval.  
- **Agent (textbook author):** materialize approved bullets into prose; sew flow; revise with Alley’s scientific-writing craft (not as a curriculum method)—without inventing new claims.

## Prose craft stack

1. Architect bullets (curriculum)  
2. Chapter standards (pedagogy)  
3. CMOS (house style)  
4. Alley, *The Craft of Scientific Writing* (revision order for scientific prose)

## How to invoke

- `run section-bullet-expand on chapter 2`  
- `/section-craft book/chapters/02-constraints/02-constraints.qmd`  
- Supply architect intent in the same message (“this section must teach… fence CBF… kit-scale SI…”), then wait for bullets  

The agent must **read the workflow first**, capture an **Architect brief**, and **not** expand `.qmd` prose until bullets are approved.
