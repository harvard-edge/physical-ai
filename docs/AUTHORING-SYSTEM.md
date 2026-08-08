# Physical AI Authoring System

**Status:** canonical execution protocol
**Depends on:** `BOOK-GOAL.md` and `CHAPTER-OUTLINES.md`

## Purpose

This protocol turns the backward design into a repeatable authoring process. It
defines what may be researched in parallel, what must be integrated in sequence,
how context grows between calls, which agents challenge the work, and what
evidence proves that a chapter is ready for its lab.

`AUTHORING-LOOP.md` is the executable companion. It states the plain-language
loop, the feedback cycle, and the provider-neutral request format used by
`tools/authoring_loop.py`.

The process is designed to prevent five common failures:

1. independent sections that repeat definitions or contradict each other;
2. technically correct surveys that never teach an engineering decision;
3. model or vendor novelty replacing durable systems reasoning;
4. labs carrying concepts the prose failed to teach; and
5. locally polished chapters that do not assemble into one working system.

## The Unit of Authorship

One persistent chapter steward owns each chapter's argument. A fresh agent may
research a concept, challenge the pedagogy, design a representation, verify a
claim, or map a lab. Unrelated agents should not write adjacent sections from
cold prompts.

This distinction preserves both independent thought and manuscript continuity:

> **Specialists expand and challenge the material. The chapter steward composes
> it. The book architect controls what the manuscript is allowed to become.**

## What the Reader Sees

The authoring packet is deliberately more structured than the manuscript. Its
field names must not become a repeated set of headings. The normal visible
chapter has:

1. a natural opening built around a scene, failure, contradiction, or question;
2. one compact `callout-objective` written to the reader;
3. chapter-specific sections whose order follows the causal argument;
4. a chapter-specific decision callout that also records the dossier update;
5. a transfer check embedded where it tests the completed reasoning; and
6. the end-of-chapter lab as the final element.

Opening question, entering state, misconception, crux, owned concepts, deferred
concepts, dependency state, and acceptance evidence remain editorial metadata.
Question callouts are optional. Generic headings such as `Learning Objective`,
`What This Chapter Adds`, and production handoff labels are forbidden in
manuscript prose. The extensive machinery should make the chapter feel coherent,
not templated.

## Authoritative Control Artifacts

The authoring system uses six compact control artifacts. They are records of
accepted decisions, not running transcripts.

### 1. Book Constitution

The constitution contains:

- title and promise;
- target readers and prerequisite knowledge;
- terminal transfer performance;
- scope boundaries and explicit exclusions;
- pedagogical commitments;
- platform-neutrality requirement;
- model-as-component requirement;
- lab separation rule;
- voice and prose principles; and
- originality claim and neighboring disciplines.

`BOOK-GOAL.md` currently performs this role.

### 2. Backward-Design Matrix

For every chapter, the matrix records:

- entering learner state;
- observable objective;
- misconception;
- transfer task;
- engineering decision;
- exit capability;
- assessment evidence; and
- downstream dependency.

The matrix is a compact audit view of `CHAPTER-OUTLINES.md`. It does not replace
the detailed scaffold.

### 3. System Build Ledger

The ledger tracks the system the reader is constructing. Every row records:

- chapter and artifact version;
- new capability and interface;
- requirements and assumptions consumed;
- measurements and evidence added;
- unresolved risks;
- authority or trust boundary changed;
- rejected alternative; and
- next chapter dependency.

The ledger prevents the canonical system from resetting between chapters.

### 4. Terminology and Notation Registry

Each entry contains:

- preferred term and definition;
- concept-owning chapter and first-use section;
- allowed abbreviation or synonym;
- forbidden or ambiguous uses;
- notation and units;
- source lineage; and
- later chapters that may consume it.

Terms such as state, memory, world model, policy, intent, action, skill, safety,
confidence, authority, and deployment require explicit ownership because each
has several plausible meanings.

### 5. Claim and Source Ledger

Every nontrivial technical claim records:

- claim identifier and exact wording;
- chapter and first-use section;
- source and supporting location;
- source type;
- whether the claim is theorem, established result, empirical observation,
  engineering heuristic, or explanatory metaphor;
- evidence strength and qualification;
- date sensitivity;
- permitted later reuse; and
- unresolved verification question.

Prefer primary papers, standards, official documentation, and authoritative
texts. Current model examples may illustrate an interface, but no chapter should
depend on a leaderboard or current product being dominant.

### 6. Representation Registry

Every figure, table, equation, algorithm, trace, and recurring worked example
records:

- stable identifier;
- chapter and target section;
- representation type;
- claim and inference it supports;
- concepts it may assume;
- system artifact it modifies;
- source data or technical source;
- status and reviewer;
- risk of misleading the reader; and
- HTML and PDF verification status.

This registry prevents thirteen unrelated diagram styles and repeated
representations of the same idea.

## Agent Roles

Roles are independent review perspectives. One person or model may perform
different roles at different times, but a draft should not review itself.

### Book Architect

Owns the terminal outcome, chapter dependencies, concept ownership, cumulative
system, terminology, scope, and final integration decisions.

The architect may reject technically interesting material that does not serve a
chapter decision or belongs in a neighboring discipline.

### Chapter Steward

Owns one chapter's causal argument, section sequence, prose continuity, worked
example, dossier delta, and landing into the next chapter.

The steward receives accepted specialist output but remains responsible for
what enters the manuscript.

### Domain Scout

Identifies indispensable concepts, competing formulations, formal lineage,
failure modes, current systems implications, important counterexamples, and
primary sources.

The scout returns a concept inventory, not polished manuscript prose.

### Pedagogy Auditor

Works backward from the transfer task. Identifies threshold concepts, hidden
prerequisites, misconceptions, explanatory sequence, examples, counterexamples,
cognitive load, and checks for understanding.

### Representation Designer

Determines which relationships require a figure, table, equation, algorithm,
trace, worked example, or no additional representation. Each proposal names the
inference it supports.

### Skeptical Practitioner

Asks whether the chapter enables an engineer to make and defend a decision on an
unfamiliar system. Looks for hand-waving, omitted operating assumptions, missing
failure behavior, unmeasurable claims, and advice that collapses outside the
reference example.

### Technical and Citation Auditor

Checks definitions, equations, units, claims, primary-source support, date
sensitivity, borrowed lineage, and the boundary between established results and
this book's synthesis.

### Continuity Editor

Checks neighboring chapters, repeated explanations, terminology, notation,
worked-example state, concept ownership, and the cumulative design dossier.

### Lab Mapper

Enters only after the teaching chapter passes its reviews. Converts the objective
into analytical, hosted, and physical manifestations with the same phenomenon,
evidence, failure, and decision.

## Progressive Context Packet

Every generation or review call receives a structured packet. The packet grows
through accepted decisions rather than raw conversation history.

### Static Book Context

```yaml
book_title:
book_promise:
terminal_transfer_performance:
reader_profiles:
prerequisites:
scope_in:
scope_out:
pedagogical_commitments:
visual_thesis:
platform_neutrality:
model_as_component_rule:
lab_separation_rule:
voice_constraints:
```

### Chapter Context

```yaml
chapter_number:
chapter_title:
part:
opening_question:
objective:
entering_learner_state:
misconception:
crux:
engineering_decision:
owned_concepts:
borrowed_concepts:
deferred_concepts:
incoming_dossier_state:
dossier_delta:
quantitative_tool:
transfer_task:
downstream_dependency:
neighbor_chapter_summaries:
known_overlap_risks:
```

### Dynamic Section Context

```yaml
context_version:
section_id:
working_title:
instructional_job:
reader_before:
reader_after:
claim_spine:
prerequisites_allowed:
misconceptions_addressed:
accepted_prior_sections:
canonical_example_state:
approved_terms_and_notation:
approved_sources:
required_representation:
material_deferred:
open_questions:
next_section_may_assume:
lab_handoff_boundary:
length_and_success_tests:
```

The immediately preceding section may be supplied in full. Older accepted
material should be compressed into authoritative summaries and ledger state.
This retains continuity without allowing the context packet to become a pile of
unresolved drafts.

## The Accepted-Context Ratchet

After every section cycle, the book architect or chapter steward records an
accepted context delta:

```yaml
accepted_claims:
new_definitions:
notation_changes:
dossier_changes:
sources_added:
representations_committed:
assumptions_added_or_removed:
rejected_alternatives:
questions_resolved:
open_questions:
next_context_version:
```

Only accepted deltas enter the next generation call. Reviewer suggestions,
discarded prose, unresolved alternatives, and raw agent transcripts remain
outside the canonical context.

Every context packet has a version. A later draft must name the version it used.
This makes terminology drift and stale assumptions detectable.

## Chapter Production Sequence

### Book Readiness Check

Before any chapter is drafted:

- the book goal is canonical;
- the chapter order and concept ownership are locked;
- the cumulative dossier chain is complete;
- the visual grammar exists;
- old conflicting scaffolds are marked as legacy; and
- the chapter has an assigned steward.

### Call 1 — Fundamental Material

The domain scout receives the static book packet and chapter contract. No
manuscript prose is requested.

Required output:

- indispensable concepts and distinctions;
- governing equations or representations;
- important edge cases and counterexamples;
- common practitioner shortcuts and failure modes;
- formal lineage and primary sources;
- current VLM, VLA, policy, hardware, or evidence examples where relevant;
- material that belongs in another chapter;
- claims likely to age; and
- unresolved technical questions.

### Call 2 — Backward Pedagogy

The pedagogy auditor receives the accepted concept inventory and transfer task.

Required output:

- learner prerequisites;
- threshold concepts;
- misconception progression;
- causal teaching sequence;
- concrete examples and counterexamples;
- retrieval and transfer checks;
- cognitive-load risks;
- what must be understood before the lab; and
- what can remain optional depth.

### Call 3 — Chapter Architecture

The chapter steward receives Calls 1 and 2 and proposes:

- section sequence and dependency;
- claim flow and bridges;
- recurring worked example;
- quantitative tool placement;
- cumulative dossier delta;
- figure, table, equation, and algorithm plan;
- transfer task placement; and
- lab handoff.

No polished prose is produced yet.

### Call 4 — Representation Design

The representation designer evaluates every proposed artifact.

- A figure must clarify topology, time, causality, uncertainty, ownership, or
  change.
- A table must support comparison or exact lookup across repeated fields.
- An equation must expose a relationship, bound, or decision threshold.
- An algorithm must specify state, conditions, timing, invariants, and failure
  behavior.
- A worked example must carry the causal argument rather than decorate it.

Decorative art, repeated prose in boxes, and pseudocode without state or failure
behavior are rejected.

### Call 5 — Outline Red Team

A fresh skeptical practitioner receives the outline, not the intent behind it.

The review searches for:

- concepts used before definition;
- hidden robotics, control, embedded, or probability prerequisites;
- model-centric or vendor-specific framing;
- false universal claims;
- overlap with neighboring chapters;
- missing failure behavior;
- unmeasurable advice;
- a lab being asked to teach missing fundamentals;
- examples that fail to transfer; and
- breadth that prevents the chapter from landing.

The book architect resolves every finding before prose drafting.

### Calls 6A Through 6N — Sequential Section Drafting

The persistent chapter steward drafts one section or tightly coupled section
cluster per call.

Every section call requests two outputs:

1. the proposed manuscript section; and
2. a structured authoring report containing new terms, technical claims,
   sources, representations, assumptions, dossier changes, unresolved questions,
   and the next section's entry condition.

The steward may revise the section after specialist review. The next section is
not drafted until the accepted-context delta is recorded.

### Call 7 — Chapter Integration

The steward reads the assembled chapter as one argument and repairs:

- repeated setup;
- missing transitions;
- concept order;
- notation and terminology drift;
- worked-example discontinuity;
- unsupported claims;
- uneven depth;
- summary without synthesis;
- missing dossier update; and
- a weak landing into the next chapter.

### Call 8 — Independent Review Passes

The integrated chapter receives separate passes for:

1. backward alignment;
2. technical correctness and citation support;
3. novice comprehension and progressive disclosure;
4. practitioner transfer;
5. cumulative-system and cross-chapter continuity;
6. visual, algorithmic, and quantitative sufficiency;
7. platform neutrality and model-age resilience; and
8. human voice and avoidance of formulaic generated prose.

Reviewers diagnose problems and propose specific corrections. They do not replace
the chapter with a stylistically unrelated rewrite.

### Call 9 — Lab Mapping

Only after the prose passes review does the lab mapper receive the chapter.

The lab contract records:

- objective being assessed;
- visible phenomenon;
- predeclared prediction;
- controlled perturbation;
- meaningful alternative or negative control;
- operational definition;
- required evidence and uncertainty;
- chapter-native failure;
- diagnosis path;
- engineering decision;
- dossier update;
- analytical manifestation;
- hosted manifestation;
- physical manifestation;
- concepts the lab may assume; and
- concepts the lab is forbidden to introduce.

### Call 10 — Chapter Acceptance

The book architect signs off only when the chapter, representations, transfer
task, sources, and lab contract agree with one another and with the current
ledgers.

## Parallel Execution

Parallelism should increase independent reasoning, source coverage, and review
quality. It should not create parallel versions of the book's argument.

### Safe to Parallelize

- primary-source discovery;
- competing concept inventories;
- misconception research;
- current model-interface examples;
- candidate cases and counterexamples;
- figure and table concepts;
- quantitative derivations;
- technical fact-checking;
- independent red-team reviews; and
- lab feasibility research after the teaching contract is stable.

### Keep Serialized

- book outcome and chapter dependency;
- concept ownership and first-use definitions;
- final objective and engineering decision;
- final section sequence;
- drafting adjacent explanatory sections;
- evolution of the canonical example and dossier;
- terminology or notation changes;
- cross-chapter integration; and
- lab mapping before teaching approval.

### Four-Slot Rolling Pipeline

| Slot | Work |
| --- | --- |
| Architect | Integrate decisions and update the authoritative ledgers |
| Previous chapter | Independent review and continuity audit |
| Current chapter | Persistent steward drafts against an accepted outline |
| Next chapter | Domain, pedagogy, and representation research |

At the beginning of a difficult part, the three worker slots may fan out across
domain, pedagogy, and representation audits. They converge before prose drafting
resumes.

### Production Waves

1. **Foundation wave, Chapters 1 through 4.** Finalize largely in order. These
   chapters establish language, requirements, measurement, and runtime.
2. **Loop wave, Chapters 5 through 8.** Research may run in parallel. Final prose
   integrates observe → estimate → propose → enforce.
3. **System wave, Chapters 9 and 10.** Integrate placement before confidence.
4. **Lifecycle wave, Chapters 11 and 12.** Research authority and learning in
   parallel, but finalize authority before interaction becomes data or change.
5. **Release wave, Chapter 13 and the design review.** Begin only after every
   preceding dossier artifact is stable.

## Representation Selection Check

Before commissioning a representation, ask what the reader must infer.

| Reader must infer | Preferred representation |
| --- | --- |
| Causal or spatial relationship | Figure |
| Timing, cadence, age, overlap, or change | Timeline or timing figure |
| Exact interface fields or repeated comparison | Table or schema |
| Quantitative tradeoff or decision boundary | Plot or equation with worked case |
| Stateful conditional behavior | Algorithm or state machine |
| One claim with one qualification | Prose |

Every representation is rejected if removing it leaves the reader's inference
unchanged.

## Chapter Acceptance Reviews

### Review 1 — Contract

- The objective is observable.
- The misconception and crux create a real instructional need.
- The decision and dossier artifact contribute to the final system.
- Owned and deferred concepts are explicit.

### Review 2 — Outline

- Every section changes the reader's capability.
- Concepts appear in dependency order.
- The chapter has enough depth for its decision and no survey material by habit.
- Every proposed representation has a named inference.
- The lab is not carrying missing teaching.

### Review 3 — Draft

- Technical claims are supported and qualified.
- The chapter uses one coherent example or a deliberate set of transfer cases.
- Alternatives and failure behavior are explicit.
- The reader practices reasoning rather than imitation.
- The ending updates the cumulative dossier.

### Review 4 — Continuity

- Terminology and notation match the registries.
- No neighboring chapter has been duplicated or preempted.
- The canonical system state is consistent.
- The next chapter receives exactly what it expects.

### Review 5 — Lab Readiness

- The chapter stands without hardware.
- All lab concepts have already been taught.
- Analytical, hosted, and physical forms test the same inference.
- The lab ends in evidence, diagnosis, decision, and dossier update.

## Definition of Done for a Chapter

A chapter is complete when a reader without the prescribed hardware can:

1. explain the central physical-AI systems problem;
2. use its quantitative or representational tool;
3. diagnose a non-obvious chapter-native failure;
4. compare alternatives under stated assumptions;
5. make and defend the chapter's engineering decision;
6. update the cumulative system dossier;
7. transfer the method to an unfamiliar system;
8. enter the next chapter without a hidden prerequisite; and
9. understand what the lab will test without depending on it for theory.

## Book-Level Acceptance

The manuscript is ready only when:

- all thirteen chapter contracts trace to the terminal transfer performance;
- every concept has one owner and appears before use;
- every chapter adds its promised dossier artifact;
- the complete dossier supports the final design review;
- the model and hardware examples can change without breaking the argument;
- figures use the canonical PhysicalAI grammar and pass rendered inspection;
- tables, equations, and algorithms earn their place;
- labs remain downstream of complete teaching;
- authority precedes data reuse and system change;
- the deployment decision integrates safety, security, privacy, recovery, evidence,
  authority, updates, and residual risk; and
- the reader is equipped to analyze a system not shown in the book.
