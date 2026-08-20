# Physical AI — Claude workflows

Project-local agent workflows live here. They are **prompts with gates**, not CI.

| Workflow | When to use |
| :--- | :--- |
| [`section-bullet-expand.md`](section-bullet-expand.md) | Craft or rewrite a chapter/section: section-by-section audit → expert feedback loop → **user-approved bullets** → automated prose expansion |

## How to invoke

In chat, say one of:

- `run section-bullet-expand on chapter 2`
- `/section-craft book/chapters/02-constraints/02-constraints.qmd`
- `bullet-outline section “Column 1: Time Constants…” then wait for my approval`

The agent must **read the workflow file first** and follow its phases in order. Do not skip the bullet-approval gate.
