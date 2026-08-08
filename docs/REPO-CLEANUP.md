# Repo cleanup status

**Done (2026-08-08):** Non-book product and prototype material was moved to a sibling directory so this repository is the Physical AI book + TinyAgents kit only.

## Destination

```text
/Users/VJ/GitHub/PhysicalAI-prototypes/
  mayas-reachy/     # Reachy app + product docs
  mios/             # orchestrator, governance, protocol, architecture, evolution/evaluation
  partnerships/     # former outputs/ decks
  legacy-book/      # retired chapters + superseded curriculum docs
```

See [`../../PhysicalAI-prototypes/README.md`](../../PhysicalAI-prototypes/README.md).

## What remains in PhysicalAI

| Path | Role |
| --- | --- |
| `book/` | Manuscript (only files in `_quarto.yml` chapter list) |
| `labs/` | UNO Q postdoc lab track |
| `docs/` | Book control docs (BOOK-GOAL, CHAPTER-OUTLINES, DECISIONS, PRODUCTION-PLAN, TRACEABILITY, authoring, packets, WAVE-1) |
| `authoring/`, `tools/` | Authoring support |
| `README.md` | Book + kit entry point |

## Optional follow-ups

1. Initialize separate git repos under `PhysicalAI-prototypes/*` if those projects need independent history/CI.  
2. Remove `PhysicalAI/.ruff_cache`, empty `dist/`, and other local caches from commits if present.  
3. `git add -A` in PhysicalAI when ready to commit the move (deletions + new README/labs). History of moved files remains in PhysicalAI until filter-repo is used.  
4. After legacy prose is salvaged, delete `PhysicalAI-prototypes/legacy-book/` if unused.
