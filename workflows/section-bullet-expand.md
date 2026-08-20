# Workflow: Section → Feedback → Bullets → Expand

**ID:** `section-bullet-expand`  
**Location:** `.claude/workflow/section-bullet-expand.md`  
**House rules:** `.claude/CLAUDE.md` §9 (CMOS), `.claude/rules/expert-review-board.md`, `.claude/rules/prose-craft.md`, `.claude/rules/chapter-architecture.md`, `.cursor/rules/chapter-standards.mdc`

---

## Purpose

You (the agent) systematically improve a **chapter or one section** by looping:

1. Read the material section by section.  
2. Collect multi-persona feedback (coverage vs explanation quality).  
3. Turn that feedback into a **bullet outline** the human can edit.  
4. **Stop and wait** until the human approves (or revises) the bullets.  
5. Only then expand each approved bullet into one or more CMOS paragraphs in the manuscript.

**Human job:** shape, reorder, cut, and approve bullets.  
**Agent job:** audit, propose bullets, expand approved bullets into prose, re-check.

Do **not** dump a full rewritten chapter before bullets are approved. Do **not** treat bullets as final prose.

---

## Triggers (any of these)

- `run section-bullet-expand on <path or chapter N>`
- `/section-craft <path>`
- `bullet-outline <section heading>` / `expand approved bullets for <section>`
- User asks to “iterate section by section with feedback then bullets then expand”

If the user names only a chapter, default to **one `##` section at a time** (not the whole file in one expand pass).

---

## Non-negotiable gates

| Gate | Rule |
| :--- | :--- |
| **G0 Scope** | Work one chapter path, and within it prefer one `##` section per cycle unless the user explicitly says “whole chapter outline.” |
| **G1 No silent rewrite** | Before bullet approval, you may only write audit notes + bullet outline files—not replace body prose. |
| **G2 Bullet approval** | Expanding into `.qmd` prose requires an explicit human signal: `approve bullets`, `approved`, `expand`, or a marked `Status: APPROVED` in the outline file. |
| **G3 CMOS** | Expanded prose: complete sentences, no `**Label:**` telegraphs in body, no `---` rules, autopsy = six-field schema only. |
| **G4 Ownership** | Respect preface vs chapter ownership; do not re-sermonize eras/tribes/behind-glass in chapter leads. |
| **G5 Transfer** | Every bullet must state what the reader can **compute, decide, or measure** after the expanded prose—not only what is “mentioned.” |

---

## Artifacts (always write these)

Create or update under the chapter directory:

```text
book/chapters/<nn-slug>/_craft/
  SECTION-<slug>.md     # one file per ## section being crafted
  CHAPTER-BOARD.md      # optional roll-up for whole-chapter passes
```

Example: `book/chapters/02-constraints/_craft/SECTION-column-1-freshness-wall.md`

If `_craft/` is missing, create it. Do not put craft notes in the `.qmd` as HTML comments unless the user asks.

---

## Phase 0 — Lock scope

1. Resolve the target path (chapter `.qmd` and optional `##` heading).  
2. Read the chapter lead + objectives + the target section (+ one section before/after for glue).  
3. State in chat (short):

   - **Target:** path + heading  
   - **Owns (this section):** 3–6 concepts this section must teach  
   - **Defers:** concepts named here but owned later  
   - **Deliverable:** what notebook/ledger skill this section supports (if any)

4. Open or create the `_craft/SECTION-….md` file with YAML-ish header:

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

Walk the target section only:

1. List every `###` / figure / table / callout / equation block in order.  
2. For each block, one line: **role** (intuition / mechanism / SI rigor / callout / figure) and **claim**.  
3. Flag obvious CMOS or structure defects (callout pile before first `##`, Bold Lead-In body, broken lab path, `<br>` in tables)—note only; do not fix yet unless the user asked for a drive-by.

---

## Phase 2 — Multi-iteration feedback loop

Run the **4-expert board** on *this section* (not the whole book unless asked):

1. Embedded & Silicon Lead  
2. Embodied ML Specialist  
3. System Safety Lead  
4. Student & Practitioner UX Lead  

Criteria: `.claude/rules/expert-review-board.md`.

### Iteration protocol (default 3 cycles, stop early if stable)

For each cycle `k = 1..3`:

1. Each persona answers, for this section only:

   - Coverage: Strong / Adequate / Weak  
   - Explanation quality: Strong / Adequate / Weak  
   - **Explained well** (keep)  
   - **Named only** (fence or teach)  
   - **Missing** (add bullet or defer with pointer)  
   - **Blocking** (wrong number, broken lab path, contradicts another section)

2. Merge into a single board note inside the craft file under `## Board cycle k`.  
3. Change the section outline **only as bullets** (Phase 3). Do not expand prose in this phase.  
4. Stop iterating when:

   - no new *Missing* items that this section owns, and  
   - *Named only* items are either promoted to bullets or explicitly `Deferred OK` with a chapter pointer, and  
   - no unresolved *Blocking* items.

Optional: spawn parallel subagents per persona; merge yourself. Prefer depth over performative disagreement.

---

## Phase 3 — Craft the bullets (human-editable)

Rewrite the craft file’s `## Bullet outline` to the **current proposal**. Bullets are the contract with the human.

### Bullet format (required)

Each bullet is one teachable move. Use this template exactly:

```markdown
## Bullet outline
Status: AWAITING_APPROVAL

### B1. <short imperative or noun phrase>
- **Owns:** what concept this bullet is responsible for
- **Transfer:** after reading the expanded prose, the reader can <compute|decide|measure|…>
- **Ladder:** intuition | mechanism | SI rigor   (mark which this bullet must carry; a bullet may be only one rung)
- **Depends on:** prior bullets or earlier sections (or `none`)
- **Assets:** equation / figure / table / callout needed (`none` | specific id or “new: …”)
- **Notes:** optional constraint (kit-scale, defer CBF to Ch8, reconcile P99, …)
- **Expand to:** 1–3 paragraphs (agent hint; human may change)
- **State:** PROPOSED   # PROPOSED | KEEP | REVISE | DROP | APPROVED
```

### Bullet quality bar

- One bullet = one idea the human can accept or reject.  
- Prefer **kit-scale, SI, decision** language over slogans.  
- If feedback said “named only,” the bullet must say how teaching will change (worked example, fence + deferral sentence, mechanism paragraph).  
- Cap: roughly **4–12 bullets per `##` section**. If you need more, split the section or mark some `DROP`/`Deferred`.  
- Do **not** use Bold Lead-In as the bullet title style in the eventual `.qmd`; titles here are craft labels only.

### After writing bullets

1. Set craft `Status: AWAITING_APPROVAL`.  
2. Paste a compact bullet list in chat (titles + Transfer only).  
3. **Stop.** Ask the human to mark bullets KEEP / REVISE / DROP / APPROVED (or edit the craft file).  
4. Do not open the `.qmd` for prose expansion until Gate G2 clears.

---

## Phase 4 — Human approval (wait)

Accept any of:

- Chat: `approve bullets`, `approved`, `expand B1 B3 B5`, `expand all approved`  
- Craft file: section `Status: APPROVED` and per-bullet `State: APPROVED`  
- Partial: expand only bullets marked APPROVED; leave others

If the human revises bullet text, treat their wording as authoritative. Re-run a **short** board cycle only if they ask or if revisions change ownership/deferrals materially.

---

## Phase 5 — Expand approved bullets into prose

For each `State: APPROVED` bullet, in order:

1. Draft **1+ complete paragraphs** (and only the assets listed).  
2. Place them in the `.qmd` at the right point in the section (replace thin named-only passages; do not orphan old contradictions—delete or fence).  
3. Follow CMOS + systems lens (`prose-craft.md`): budgets, composition, shared resources; intuition → mechanism → SI when the bullet’s Ladder requires it.  
4. One bullet may become multiple paragraphs; do not smuggle a second unapproved bullet’s content.  
5. Update bullet `State: EXPANDED` and craft `Status: EXPANDING` → `DONE` when all approved bullets are in.

### Expansion checklist (per bullet)

- [ ] Transfer claim is actually satisfied (reader can compute/decide)  
- [ ] No preface overlap sermon  
- [ ] Numbers reconciled with chapter ledger / nearby examples  
- [ ] Callouts only where schema requires (autopsy/contract/etc.)  
- [ ] Lab paths and forward refs are real  

---

## Phase 6 — Post-expand micro-board (one cycle)

Quick pass (Student UX + the persona most relevant to the section):

- Did expansion fix *Named only* / *Blocking*?  
- Any new overlap or density problem?  

If fixes are small, apply them. If they need new teaching claims, add **new PROPOSED bullets** and return to Gate G2—do not silently grow scope.

---

## Phase 7 — Handoff

Report in chat:

1. Craft file path  
2. Bullets expanded vs still waiting  
3. Diff summary (sections touched)  
4. Recommended next `##` section  

Do not start the next section’s expansion without asking, unless the user said “walk the whole chapter section by section.”

---

## Whole-chapter mode (optional)

If the user asks for a **whole chapter** craft:

1. Phase 0–2 once at chapter level → `CHAPTER-BOARD.md` (coverage matrix + top priorities).  
2. Produce a **chapter bullet map**: ordered list of section slugs + bullet counts—still no prose.  
3. Wait for approval of the **map**.  
4. Then run Phases 3–6 **per section** in order.

---

## Anti-patterns (do not do)

- Rewriting the full section in one shot “for efficiency”  
- Expanding while bullets are still `PROPOSED`  
- Replacing human bullet wording without confirmation  
- Adding new concepts during expansion that were not in an approved bullet  
- Re-litigating CMOS vs Bold Lead-In (CMOS won)  
- Using checkpoint IDs (`LOOP-01`, …)  
- Calling the craft outline an “Abstract”

---

## Minimal example (shape only)

```markdown
### B3. Kit-scale freshness wall derivation
- **Owns:** Δt_wall from clearance, σ0, v_target
- **Transfer:** compute Δt_wall for the desk-kit numbers and see why the ledger’s 100 ms is not arbitrary
- **Ladder:** mechanism + SI rigor
- **Depends on:** B2 (definition of Δt)
- **Assets:** short worked example (new); pointer to requirements ledger
- **Notes:** must reconcile with P99 story in Column 1
- **Expand to:** 2 paragraphs
- **State:** APPROVED
```

After approval, those two paragraphs land in the `.qmd`; B3 becomes `EXPANDED`.

---

## Companion prompts (copy into subagents)

**Auditor:** “You are persona \<Name\>. Audit ONLY section \<H\>. Return Explained well / Named only / Missing / Blocking. No rewrites.”

**Bullet smith:** “Given the board notes in \<craft file\>, propose 4–12 bullets in the required template. Do not edit the `.qmd`.”

**Expander:** “Expand ONLY bullets with State APPROVED in \<craft file\> into CMOS paragraphs in \<qmd\>. Do not add unapproved claims.”
