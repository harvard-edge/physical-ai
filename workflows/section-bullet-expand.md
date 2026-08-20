# Workflow: Architect Bullets → Textbook Prose

**ID:** `section-bullet-expand`  
**Tracked copy:** `workflows/section-bullet-expand.md`  
**Also:** `.claude/workflow/section-bullet-expand.md` (if present)  
**House rules:** `.claude/CLAUDE.md` §9 (CMOS), `.claude/rules/expert-review-board.md`, `.claude/rules/prose-craft.md`, `.claude/rules/chapter-architecture.md`, `.cursor/rules/chapter-standards.mdc`

This is an **experiment**: can a textbook be co-authored by splitting *architecture* (human) from *authorship* (agent)? The workflow exists to enforce that split.

---

## Roles (non-negotiable)

### Human = Architect

You decide **what** must be expressed and **how** it should be expressed:

- Which claims belong in this section (and which defer)
- Order, emphasis, and teaching ladder (intuition → mechanism → SI)
- Transfer bar (what the reader must compute, decide, or measure)
- Tone constraints, kit anchors, fences (“preview only; Ch8 owns CBF”)
- Approval or revision of the bullet outline

You are **not** responsible for polishing paragraph rhythm or sewing transitions. That is the agent’s job after approval.

### Agent = Textbook author

You are a **textbook author**. You are good at taking approved bullets and ideas and **materializing them into prose**, and at making sure that prose **flows from one paragraph and section to the next**.

Once the architect’s instructions are captured and the bullets are approved, your job is to:

1. Expand bullets into continuous CMOS paragraphs (not telegraphic fragments).  
2. Iterate: read aloud in your head, fix seams, cut repetition, restore ladder.  
3. Improve until it reads like a systems textbook—not a slide deck, not a blog, not a bullet dump with connective tissue glued on.

You do **not** invent a new curriculum under the guise of “better prose.” New claims become new proposed bullets and return to the architect.

---

## Purpose (the loop)

1. **Capture the architect brief** (what/how) when the workflow is triggered.  
2. Read the target section; optional multi-persona feedback (coverage vs explanation).  
3. Propose or refine a **bullet outline** the architect can edit.  
4. **Hard stop** until bullets are approved.  
5. Expand approved bullets into flowing textbook prose in the `.qmd`.  
6. Short post-expand pass for flow and transfer; new claims → new bullets, not silent scope creep.

Do **not** dump a full rewritten chapter before bullets are approved. Do **not** treat bullets as final prose.

---

## Triggers

- `run section-bullet-expand on <path or chapter N>`
- `/section-craft <path>`
- `bullet-outline <section heading>` / `expand approved bullets for <section>`
- “iterate section by section with feedback then bullets then expand”
- Any message that supplies architect intent for a chapter/section (“here’s what this section must teach…”)

If the user names only a chapter, default to **one `##` section at a time** unless they say “whole chapter outline.”

---

## Phase A — Capture the architect brief (on every trigger)

Before auditing or drafting bullets, write an **Architect Brief** into the craft file. If the user already stated intent in chat, **transcribe it faithfully**—do not dilute or “improve” their architecture.

```markdown
## Architect brief
- **Target:** path + `##` heading (or whole-chapter map)
- **Must express:** (claims / ideas that must appear)
- **How to express:** (ladder, emphasis, kit anchor, fences, tone)
- **Must not:** (overlap with preface / later chapters / slogans)
- **Transfer:** after this section the reader can …
- **Success looks like:** (one sentence — what “textbook quality” means here)
- **Source:** chat | edited craft file | prior board
```

If the brief is thin, ask **at most three** clarifying questions, then proceed with explicit assumptions listed under the brief. Do not guess a new chapter thesis.

---

## Non-negotiable gates

| Gate | Rule |
| :--- | :--- |
| **G0 Scope** | One chapter path; prefer one `##` section per expand cycle unless whole-chapter map was approved. |
| **G1 Architect owns claims** | Bullets encode what/how. Agent may suggest bullets from a board pass; architect approves. |
| **G2 No silent rewrite** | Before approval: audit notes + bullet outline only—not body prose replacement. |
| **G3 Bullet approval** | Expand only on `approve bullets` / `approved` / `expand` / craft `Status: APPROVED`. |
| **G4 CMOS + flow** | Complete sentences; no `**Label:**` body telegraphs; no `---` rules; autopsy = six-field schema. Prose must bridge bullets so the section reads as one argument. |
| **G5 Ownership** | Preface vs chapter ownership; no eras/tribes/behind-glass re-sermon in chapter leads. |
| **G6 Transfer** | Every bullet states what the reader can compute, decide, or measure—not only what is named. |
| **G7 No curriculum invention** | During expansion, do not add unapproved teaching claims. |

---

## Artifacts

```text
book/chapters/<nn-slug>/_craft/
  SECTION-<slug>.md     # architect brief + board + bullets + expand log
  CHAPTER-BOARD.md      # optional whole-chapter roll-up
```

Example: `book/chapters/02-constraints/_craft/SECTION-column-1-freshness-wall.md`

---

## Phase 0 — Lock scope

1. Resolve path + optional `##` heading.  
2. Read lead, objectives, target section, and neighbors (for flow).  
3. Complete **Phase A** (architect brief).  
4. Chat summary (short): Target · Owns · Defers · Deliverable · Brief captured.  
5. Ensure craft file header:

```markdown
# Craft: <Section heading>

- Chapter: `book/chapters/…/….qmd`
- Section: `## …`
- Status: DRAFT_BULLETS   # DRAFT_BULLETS | AWAITING_APPROVAL | APPROVED | EXPANDING | DONE
- Cycle: 1
- Last board: (date)
```

---

## Phase 1 — Section inventory (mechanical)

1. List every `###` / figure / table / callout / equation in order.  
2. One line each: role (intuition / mechanism / SI / callout / figure) + claim.  
3. Note CMOS/structure defects; do not fix yet unless asked.

---

## Phase 2 — Optional multi-iteration feedback

Run the 4-expert board on *this section* when useful (or when the architect asks):

1. Embedded & Silicon · Embodied ML · Safety · Student UX  
2. Criteria: `.claude/rules/expert-review-board.md`  
3. Each cycle: Explained well / Named only / Missing / Blocking  
4. Merge into craft `## Board cycle k`  
5. Update **bullets only** (Phase 3)—no prose expansion  

Default ≤3 cycles; stop when Missing/Blocking for this section’s ownership are resolved or explicitly deferred.

---

## Phase 3 — Bullet outline (architect-editable)

Bullets are the **contract** with the architect. Prefer the architect’s wording when they edit.

```markdown
## Bullet outline
Status: AWAITING_APPROVAL

### B1. <short phrase>
- **Owns:** …
- **Transfer:** reader can <compute|decide|measure|…>
- **Ladder:** intuition | mechanism | SI rigor
- **Depends on:** …
- **Assets:** none | equation | figure | table | callout | new: …
- **How (architect):** optional — emphasis, fence, kit number, “sound like …”
- **Expand to:** 1–3 paragraphs (hint)
- **State:** PROPOSED   # PROPOSED | KEEP | REVISE | DROP | APPROVED
```

**Bar:** 4–12 bullets per `##` section; one idea per bullet; kit-scale and SI when the brief demands it.

After drafting: set `AWAITING_APPROVAL`, paste titles + Transfer in chat, **stop**.

---

## Phase 4 — Architect approval (wait)

Accept: `approve bullets` · `approved` · `expand B1 B3` · `expand all approved` · craft `Status: APPROVED` with per-bullet `APPROVED`.

Architect revisions to bullet text are authoritative.

---

## Phase 5 — Author: expand into textbook prose

You are no longer outlining. You are **writing the book**.

For each `APPROVED` bullet, in order:

1. Draft the requested paragraphs in CMOS.  
2. **Sew the seam:** opening sentence of bullet *n* must follow from bullet *n−1* (or from the section’s established claim). No orphan blocks.  
3. Place in the `.qmd` at the right locus; remove or fence contradictory thin passages.  
4. Follow systems lens (`prose-craft.md`): budgets, composition, shared resources.  
5. One bullet may become multiple paragraphs; do not smuggle unapproved claims.  
6. Mark bullets `EXPANDED`; craft `EXPANDING` → `DONE` when finished.

### Textbook flow checklist (required)

- [ ] Section can be read top-to-bottom as one argument  
- [ ] No bullet residue (“First,… Second,…” unlabeled lists of claims) unless the architect asked for a list  
- [ ] Definitions before uses; equations when the ladder calls for SI  
- [ ] Forward/back references are honest fences, not fake teaching  
- [ ] Neighbor sections still join (read last paragraph of prior `##` and first of this)  
- [ ] Transfer claim of each bullet is actually satisfied  

### Iteration (the experiment)

After the first expansion pass, do **one** authoring revision pass focused only on flow and clarity (cut throat-clearing, fix whiplash transitions, restore ladder). If you discover a missing *concept*, add a `PROPOSED` bullet and return to Gate G3—do not silently teach it.

---

## Phase 5b — Alley revision pass (prose craft)

**Doctrine:** Michael Alley, *The Craft of Scientific Writing* — used as the **revision method** for how the textbook author writes and rewrites, **not** as a substitute for architect bullets, CMOS, or chapter pedagogy.

**Stack (do not invert):**

| Layer | Owns |
| :--- | :--- |
| Architect brief + bullets | What to teach and how (curriculum) |
| Chapter standards | Pedagogy skeleton (objectives, autopsy, contract, ladder, lab) |
| CMOS | House surface style |
| Alley | Scientific prose craft and revision order |

### Alley revision order (strict)

Run passes in this order. Do not polish diction before structure is right.

1. **Audience and purpose** — Who is reading this section, and what must they be able to do after it? Cut anything that serves the author’s ego more than that purpose.  
2. **Structure** — One primary claim per section/subsection; open with that claim or with the concrete situation that forces it; put secondary detail after. Prefer visible hierarchy (short headings, short paragraphs, tables/figures that carry structure) over buried lists of claims.  
3. **Precision** — Prefer concrete nouns and verbs; put SI numbers where the ladder claims rigor; replace hedges and throat-clearing (“It is important to note…”, “As we shall see…”, “The material is foundational…”) with the fact or cut them.  
4. **Flow** — Sew paragraph seams so each sentence follows from the last; fix whiplash jumps between intuition → mechanism → SI; read the join to the previous and next `##`.  
5. **Cut** — Delete repetition, roadmap paragraphs that only announce later sections, and double-telling of the same claim in adjacent paragraphs.

### Alley checklist (required when this pass is invoked)

- [ ] Purpose of each `##` is clear in the first one or two paragraphs  
- [ ] No throat-clearing openers or empty roadmap closures  
- [ ] Structure is visible without `**Label:**` telegraphs (CMOS still wins)  
- [ ] Numbers and equations appear when the section claims quantitative transfer  
- [ ] Redundant restatements of the same claim are collapsed  
- [ ] No new curriculum claims (Gate G7 still holds)

### When to run

- Explicit trigger: `alley pass on chapter N` / `Alley revision on <path>`  
- Or as the default second revision after Phase 5 expansion when the architect asks for textbook-quality polish  

Log the pass in `_craft/ALLEY-PASS.md` (or a section craft file): what was cut, what was restructured, what was left alone because it is architect-owned.

---

## Phase 6 — Post-expand micro-board

Student UX + the most relevant expert: Did we fix Named only / Blocking? Any new density or overlap? Small fixes OK; new claims → new bullets.

---

## Phase 7 — Handoff

1. Craft file path  
2. Brief + bullets expanded vs waiting  
3. Diff summary  
4. Suggested next `##`  

Do not start the next section’s expansion unless the architect asked to walk the chapter.

---

## Whole-chapter mode

1. Phase A brief at chapter level → `CHAPTER-BOARD.md`  
2. Coverage matrix + ordered section map (still no prose)  
3. Architect approves the **map**  
4. Phases 1–6 per section in order  

---

## Anti-patterns

- Rewriting the full section “for efficiency” before approval  
- Expanding while bullets are `PROPOSED`  
- Overwriting architect bullet wording without confirmation  
- Adding concepts during expansion that were not approved  
- Slide-deck residue: bold-label stacks, motto paragraphs, callout piles before narrative  
- Replacing textbook prose with more bullets  
- Calling the craft outline an “Abstract”  

---

## Companion prompts

**Architect intake:** “Transcribe the user’s what/how into the Architect brief. Do not improve their curriculum.”

**Auditor:** “Persona \<Name\>. Audit ONLY section \<H\>. Explained well / Named only / Missing / Blocking. No rewrites.”

**Bullet smith:** “Given brief + board, propose 4–12 bullets in template. Do not edit the `.qmd`.”

**Textbook author:** “You are a textbook author. Expand ONLY APPROVED bullets into CMOS prose that flows bullet-to-bullet and section-to-section. No new claims.”
