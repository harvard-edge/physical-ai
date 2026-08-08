# Physical AI Authoring Loop

## Goal

Produce a book in which a capable newcomer can reason about, build, measure,
and defend a machine learning system that senses and acts in the real world.
The book should teach an engineering method that survives changes in models,
bodies, sensors, and computing platforms. The labs make that method concrete;
they do not determine what the book teaches.

The finished book should do more than help someone reproduce a demonstration.
After working through it, a reader should be able to approach an unfamiliar
physical AI system and decide:

- what belongs inside the system and what remains outside it;
- what must be sensed, estimated, decided, and acted on;
- what timing, freshness, energy, compute, and action limits matter;
- where a VLM, VLA, policy, controller, or world model belongs and what it does
  not control;
- what evidence supports operation in a particular situation;
- what people may request, approve, override, revoke, and inspect; and
- whether the complete system is ready to deploy.

Each chapter changes what the reader can do. Each section makes one necessary
step in that change. When the chapters are combined, the reader has designed
and defended a complete system.

## The Core Authoring Choice

One chapter is active at a time. One persistent chapter steward owns its
argument and reader-facing prose. Within that chapter, one section is drafted
at a time.

Parallel agents expand the thinking around that section. They can research the
technical material, test the teaching order, propose a representation, or
review a draft. They do not independently write neighboring sections. This
keeps the chapter from becoming a collection of loosely related essays.

With four available agent slots, one slot coordinates the work and up to three
specialists run at once. A larger runtime may raise that number without
changing the dependency order.

## What Every Agent Receives

Every call receives four layers of context.

1. **Book context.** The book goal, reader, final capability, chapter sequence,
   prose rules, visual language, and lab boundary. This changes rarely.
2. **Chapter context.** The chapter objective, reader problem, transfer task,
   section dependency, concept ownership, worked-example state, and approved
   representation plan.
3. **Accepted context.** Definitions, claims, sources, notation, system changes,
   and open questions accepted from earlier sections. The immediately previous
   section may be included in full. Older sections are supplied as short
   accepted summaries.
4. **Current request.** One role, one chapter, one section, one requested
   output, and a precise definition of success.

Later section titles may be visible when needed to explain the dependency.
Their prose is not included. Rejected drafts, raw review conversations, and
unaccepted suggestions do not become context for the next call.

This is progressive disclosure for the authoring process itself. The available
context grows only when a section has passed review.

## The Chapter Loop

### 1. Establish the chapter

Three agents work in parallel before drafting begins.

- The domain scout identifies the indispensable ideas, established results,
  common failure modes, counterexamples, and primary sources.
- The pedagogy auditor works backward from the chapter objective and transfer
  task. It finds prerequisites, likely misconceptions, and the smallest useful
  teaching sequence.
- The representation planner decides which relationships need a figure, table,
  equation, algorithm, trace, worked example, or prose alone.

The chapter steward combines those reports into a chapter plan. Independent
reviewers then test technical scope, teaching order, and practical usefulness.
The book architect approves the plan or returns specific issues to repair.

### 2. Draft one section

For each section in reading order:

1. Run technical research, pedagogy analysis, and representation planning in
   parallel for that section.
2. Have the book architect turn those reports into one section brief.
3. Have the same chapter steward draft exactly that section.
4. Create only the representations requested in the approved brief.
5. Review the section in parallel for technical accuracy, teaching order,
   continuity, engineering usefulness, and representation quality.
6. Return concrete findings to the steward. Revise only that section.
7. Repeat the review at most twice. Escalate unresolved disagreements to the
   book architect instead of silently averaging them.
8. Accept the section and record the small set of facts the next section may
   assume.

The next section does not begin until step 8 is complete.

### 3. Review the complete chapter

After all sections are accepted, the steward reads and edits the chapter as one
argument. Five independent reviews then test accuracy, progression, continuity,
practical transfer, and the full representation program.

Every finding names the earliest section that owns the problem. Repairs happen
one section at a time, in reading order. Reviewers check the repaired chapter
again. They do not replace it with a wholesale rewrite.

### 4. Map the lab

Only after the teaching passes review does the lab mapper receive the chapter.
The lab must exercise decisions already taught in the prose. It should ask the
reader to make a prediction, change one controlled condition, collect evidence,
observe a failure or limit, and make an engineering decision.

The implementation can use a particular board, runtime, model, or hosted
platform. The assessed concept must remain useful when those choices change.

### 5. Accept the chapter

The book architect checks that the objective, prose, sources, representations,
transfer task, and lab agree. A human approves the chapter before the next one
becomes active.

## Choosing Figures, Tables, and Algorithms

The workflow does not ask for one of every artifact in every section. The
representation planner may answer that prose is enough.

A proposed artifact must name the inference it helps the reader make.

| Reader need | Likely form |
|---|---|
| Understand components, boundaries, ownership, or data flow | Figure |
| Understand timing, overlap, freshness, or a changing state | Timeline or trace |
| Compare repeated fields or make an exact lookup | Table |
| Follow conditions, state changes, recovery, or fallback behavior | Algorithm or state machine |
| Understand a quantitative tradeoff or threshold | Equation, plot, or worked calculation |
| See how one design evolves across chapters | Worked system example |

Every artifact request includes its purpose, reader inference, source or data,
caption, accessibility needs, and the section that introduces it. An optional
artifact agent can return `not_needed` when the proposed form adds no teaching
value.

## The Whole-Book Feedback Loop

Once all 13 chapters are accepted, seven independent readers examine the full
book from different perspectives:

- a capable newcomer checks prerequisite order and first-use definitions;
- a practitioner tests transfer to an unfamiliar system;
- a technical reviewer checks claims, equations, sources, and qualifications;
- a systems reviewer follows the evolving design and its interfaces;
- a lab reviewer checks that exercises assess what the prose teaches;
- a visual reviewer checks meaning, consistency, accessibility, HTML, and PDF;
- a voice reviewer finds formulaic, vague, repetitive, or needlessly difficult
  writing.

The book architect combines duplicate findings and sends each issue to the
chapter and section that first owns the concept. Revisions proceed from the
earliest affected section forward because a changed definition may alter later
chapters. Only affected dependencies are reopened.

Run the full set of reviews again after repairs. Stop after two full rounds and
bring any remaining disagreement to a human decision. The final human review
checks the complete learning progression and deployment argument.

## Programmatic Form

The orchestration logic is deliberately separate from any model provider. An
adapter receives `request.json` and `prompt.md`, runs an agent, and writes a
`result.json` that follows `authoring/result.schema.json`. Raw output stays in
the ignored `.authoring-runs/` directory. Accepted work is copied into the
manuscript only through an explicit review step.

```python
async def write_book(book, adapter, reviewer, human):
    accepted_book_context = load_book_context(book)

    for chapter in book.chapters_in_dependency_order:
        steward = persistent_steward(chapter)

        chapter_reports = await run_in_parallel(
            domain_scout(chapter, accepted_book_context),
            pedagogy_auditor(chapter, accepted_book_context),
            representation_planner(chapter, accepted_book_context),
            maximum=3,
        )
        chapter_plan = await steward.plan(chapter_reports)
        chapter_plan = await review_and_repair_plan(chapter_plan, limit=2)
        await human.approve(chapter_plan)

        accepted_chapter_context = begin_chapter_context(chapter_plan)

        for section in chapter.sections_in_reading_order:
            request_context = disclose(
                book=accepted_book_context,
                chapter=accepted_chapter_context,
                previous_section="full",
                older_sections="accepted summaries",
                future_sections="titles and dependencies only",
            )

            support = await run_in_parallel(
                domain_scout(section, request_context),
                pedagogy_auditor(section, request_context),
                representation_planner(section, request_context),
                maximum=3,
            )
            brief = await book.architect.make_section_brief(support)
            draft = await steward.write_one_section(brief, request_context)

            artifacts = await build_requested_artifacts(
                brief.representations,
                draft,
                maximum=3,
            )
            draft = await review_and_revise_one_section(
                draft,
                artifacts,
                reviewers=[
                    "technical",
                    "progression",
                    "continuity",
                    "practitioner",
                    "representation",
                ],
                maximum_parallel=3,
                revision_limit=2,
            )
            accepted_chapter_context = accept_section_and_update_context(
                draft,
                accepted_chapter_context,
            )

        chapter_draft = await steward.integrate(accepted_chapter_context)
        chapter_draft = await review_and_repair_chapter(
            chapter_draft,
            repair_order="earliest owning section first",
            revision_limit=2,
        )
        lab = await map_lab_from_accepted_teaching(chapter_draft)
        await human.approve_chapter(chapter_draft, lab)
        accepted_book_context = accept_chapter(chapter_draft, lab)

    for round_number in range(2):
        findings = await review_whole_book_in_parallel(book, maximum=3)
        findings = combine_duplicates_and_assign_owners(findings)
        if not findings.requiring_change:
            break
        for issue in findings.in_dependency_order:
            await revise_one_owning_section(issue)
            await recheck_affected_dependencies(issue)

    await human.approve_book(book)
```

The actual planner can be inspected without contacting any model:

```bash
python3 tools/authoring_loop.py plan
```

It can also materialize every provider-neutral request in a safe working
directory:

```bash
python3 tools/authoring_loop.py dry-run \
  --output .authoring-runs/first-pass
```

The current implementation plans and materializes work but does not call an
agent provider or modify the book. That is intentional while the current book
baseline contains uncommitted work. The next implementation step is a small
adapter for the chosen agent runtime plus a result validator and promotion
command. The authoring order and review logic remain the same.

## What Completion Means

The loop is complete when all sections have accepted context records, every
claim and representation has an owner and source, labs assess already-taught
concepts, whole-book feedback has been resolved or explicitly decided, and the
book renders cleanly in its intended formats. Completion is a property of the
learning progression and the resulting system, not the number of generated
pages or agent calls.
