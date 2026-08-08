# Repository structure

## Purpose

Physical AI book + **TinyAgents Kit** curriculum (Arduino UNO Q dual-brain). See
[`BRAND.md`](BRAND.md).

## Tree

```text
PhysicalAI/
  README.md
  docs/
    BOOK-GOAL.md
    BRAND.md                    # Physical AI Systems + TinyAgents Kit + dual-brain
    CHAPTER-OUTLINES.md
    DECISIONS.md
    …
  book/
    chapters/
      01-frame/
        01-frame.qmd
        figures/
      …
  labs/                         # TinyAgents Kit realization (postdoc)
    01-close-the-loop/
    shared/                     # MPU–MCU contracts, instrumentation
  authoring/
  tools/
```

## Rules

1. **Chapter folder** short name: `NN-slug` (e.g. `01-frame`).
2. **Chapter file** same basename: `01-frame/01-frame.qmd` — never generic `index.qmd`.
3. **Figures** only in that chapter’s `figures/`; reference as `figures/….svg` from the qmd.
4. **Labs** under top-level `labs/`, numbered to match chapter `NN`. Dual-brain
   shared code in `labs/shared/`.
5. **Prototypes** outside this repo: `../PhysicalAI-prototypes/`.
