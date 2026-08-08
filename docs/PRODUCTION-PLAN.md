# Physical AI Production Plan

**Status:** canonical execution plan  
**Depends on:** `BOOK-GOAL.md`, `CHAPTER-OUTLINES.md`,
`AUTHORING-SYSTEM.md`, and `TRACEABILITY.md`

## Production Goal

Produce a systems-first book that enables a reader to take an unfamiliar
learned capability, embodiment, environment, and computing platform and turn
them into a defensible physical-AI system. The reader must be able to explain
the causal loop, derive requirements from the world, measure the running system,
maintain a current belief, treat learned outputs as proposals, keep actions
within explicit limits, place the computation, build evidence, allocate human
authority, govern change, and defend a release decision.

The writing program succeeds only when three conditions hold together.

1. Every chapter teaches one observable engineering capability and stands
   without its lab.
2. Every chapter changes the same cumulative system and adds traceable evidence
   or a design artifact.
3. The complete sequence transfers to a system, model family, and embodiment
   not shown in the book.

The immediate production goal is narrower. The foundation wave will make
Chapters 1 through 4 draft-ready and will validate the progressive authoring
process on Chapter 1. The wave establishes the argument on which the rest of the
book depends.

> **Recognize the consequential loop → derive requirements from the world →
> make claims measurable → architect a runtime that survives model failure**

This is a design and sketching phase, not a race to produce four rough
manuscripts. Its output is enough resolved pedagogy, technical lineage,
representation design, and accepted context that a chapter steward can draft
without inventing the chapter architecture while writing it.

## Reader-Facing Chapter Form

The chapter contract is extensive. The visible chapter is not.

1. Open with a physical scene, failure, contradiction, or question in natural
   prose.
2. Use one compact `callout-objective`. It is not a section and does not enter
   the chapter hierarchy.
3. Teach through chapter-specific headings chosen by the argument.
4. Use figures, tables, equations, and algorithms only where they enable a named
   inference.
5. End the teaching argument in a chapter-specific decision callout. Include one
   concise sentence recording the dossier update.
6. Test transfer through an unfamiliar case without requiring a repeated
   heading.
7. Place the lab last. Nothing reader-facing follows it.

Opening question, entering state, misconception, crux, concept ownership,
dependency state, and acceptance tests remain in the authoring packet. A
question callout is available when the question itself deserves visual
emphasis, but it is not mandatory.

## Decisions to Lock Before Prose

### The Learned-System Scope Test

Feedback alone does not distinguish physical AI from recommenders, trading
systems, fixed control systems, or other systems that alter future inputs. Begin
with one premise. A learned component must materially influence the proposal or
decision and thereby the action path. When that premise holds, apply two tests.

1. **Consequential physical feedback.** An accepted action changes task-relevant
   physical state and can alter later observations or choices.
2. **Delegated physical authority.** The system has permission to move matter,
   expend energy, alter access, change an environmental process, or directly
   affect a person.

Chapter 1 must teach the premise and tests as an operational classification
method rather than a branding claim. This is the book's working synthesis, not a
theorem or consensus definition of the field.

### Minimal System Notation

The book needs enough notation to connect the chapters without becoming a
control textbook.

| Symbol | Meaning |
| --- | --- |
| \(W_t\) | Physical world state at time \(t\) |
| \(o_t\) | Timestamped observation of the world |
| \(b_t\) | Maintained belief used for a decision |
| \(p_t\) | Learned proposal, including its validity conditions |
| \(\operatorname{permit}\) | Check that a proposal satisfies current limits and authority before it becomes an action |
| \(u_t\) | Allowed action issued to the physical system |
| \(d_t\) | Disturbance or unmodeled influence |
| \(W_{t+1}\) | World state after action and disturbance |

The recurring relationship is:

\[
o_t \leftarrow W_t, \qquad
b_t \leftarrow \operatorname{update}(b_{t-1}, o_t), \qquad
p_t \leftarrow \pi(b_t), \qquad
u_t \leftarrow \operatorname{permit}(p_t, b_t, \text{limits}, \text{authority}), \qquad
W_{t+1} \leftarrow F(W_t, u_t, d_t).
\]

The notation makes proposal and permitted action visibly different. Later
chapters may refine each term but may not silently redefine it.

### Canonical Evolving Case

Use one platform-neutral shared-workspace handling system across all thirteen
chapters. The system observes objects and people in a defined tabletop area,
interprets a requested handling or sorting task, proposes a physical action,
checks the proposal against spatial, temporal, and authority constraints, acts,
and observes the result.

The case is intentionally modest. It supports simple classifiers, VLMs, VLAs,
continuous or symbolic action, local and hosted compute, human demonstration,
and several embodiments without making any one implementation the book's
definition of physical AI.

The case provides real systems pressure.

- A stale observation can cause a wrong or unsafe action.
- A person may enter the workspace after inference begins.
- An action may be late, duplicated, out of order, or incompatible with the
  embodiment.
- A camera creates privacy and retention questions.
- Demonstrations create consent, provenance, and coverage questions.
- A successful demonstration does not by itself justify deployment.

Every chapter also needs at least one contrasting transfer case drawn from a
different physical regime.

### Traceability Identifiers

The dossier is one engineering case rather than thirteen unrelated forms. Use
stable identifiers that survive later chapters.

| Prefix | Record |
| --- | --- |
| `LOOP-` | Boundary, affected people, and feedback path |
| `REQ-` | Requirement and operating assumption |
| `MEAS-` | Operational definition, instrument, and evidence record |
| `RUN-` | Runtime service, invariant, cadence, or recovery behavior |
| `OBS-` | Observation contract |
| `STATE-` | Belief, frame, clock, and correction behavior |
| `INTENT-` | Policy interface and proposal contract |
| `ENF-` | Action bound and enforcement mechanism |
| `PLACE-` | Placement and failure-domain decision |
| `EVID-` | Scenario, evidence tier, and promotion result |
| `AUTH-` | Human authority, consent, or revocation rule |
| `DATA-` | Trajectory, provenance, update, and rollback record |
| `REL-` | Deployment claim, condition, owner, and verdict |

A requirement should be traceable to its measurement, runtime invariant,
enforcement mechanism, evidence, and final release claim.

### Fault Taxonomy

The book needs one compact vocabulary before Chapter 4. Every fault example
should identify at least one of these dimensions.

| Dimension | Examples |
| --- | --- |
| Availability | Missing, unavailable, disconnected, or crashed |
| Timing | Late, stale, expired, or deadline-missing |
| Ordering | Duplicated, replayed, dropped, or out of order |
| Integrity | Corrupted, spoofed, tampered with, or from the wrong version |
| Semantics | Incorrect, incompatible, out of distribution, or misframed |
| Authority | Unapproved, revoked, excessive, or impossible to interrupt |
| Physical recovery | Body and world state disagree with software after failure |

The taxonomy supports diagnosis and ownership. It is not a claim that every
fault has the same consequence or remedy.

### Security Thread

Security remains a cross-cutting system property rather than a late checklist.

- Chapter 4 introduces message identity, version, replay, ordering, and command
  delivery assumptions.
- Chapter 5 treats sensor integrity and spoofing as observation validity.
- Chapter 9 maps trust boundaries and shared failure domains.
- Chapter 12 governs data and update provenance.
- Chapter 13 integrates command authenticity, dependency provenance, update
  integrity, and recovery into the release case.

The early chapters may name these obligations but must not preempt their later
owners.

## Foundation-Wave Work Packages

### WP0 — Production Controls

**Purpose.** Make the authoring system internally consistent before prose.

**Deliverables.**

- accepted scope test;
- minimal notation registry;
- canonical-case charter;
- traceability-ID schema;
- fault taxonomy and concept owners;
- security-thread map;
- backward-design matrix for Chapters 1 through 4;
- system-build ledger through runtime version 0.4;
- source-ledger and representation-registry templates;
- objective-callout rendering test; and
- versioned context-packet template.

**Acceptance.** Every chapter has one objective, decision, and dossier delta.
Each output is an explicit input to the next chapter. No archived plan controls
generation. Reader-facing and editorial structures are unambiguous.

### WP1 — Chapter 1 Authoring Packet

**Capability.** Frame the consequential loop.  
**Decision.** Choose the causal and authority boundary.  
**Dossier delta.** Loop charter.

**Deliverables.**

1. accepted chapter contract;
2. fundamental-material and source packet;
3. seven section briefs;
4. matched-deployment figure, scope-test table, and loop-charter schema briefs;
5. worked-example plan using one model in advisory and actuating deployments;
6. transfer-task specification;
7. independent outline red team;
8. lab interface containing phenomenon, evidence, failure, decision, and dossier
   update but no build instructions; and
9. accepted exit-state packet for Chapter 2.

### WP2 — Chapter 2 Authoring Packet

**Capability.** Derive requirements from the world.  
**Decision.** Choose a defensible operating regime.  
**Dossier delta.** Requirements and assumptions ledger.

**Deliverables.**

1. accepted chapter contract;
2. material and source packet for world timescales, information age, consequence,
   prediction, partial state, and interacting budgets;
3. nine section briefs with endogeneity kept as a short application of Chapter
   1 rather than a second lesson;
4. timing plate, regime-conditioned efficacy plot, definition table, and
   consequence-to-requirement procedure briefs;
5. worked case for the loop diagnostic and its limitations;
6. two-regime transfer task;
7. independent outline red team;
8. lab interface for locating a task-specific freshness wall; and
9. accepted exit-state packet for Chapter 3.

### WP3 — Chapter 3 Authoring Packet

**Capability.** Turn a system claim into defensible evidence.  
**Decision.** Accept, reject, or narrow the claim.  
**Dossier delta.** Measurement plan and evidence record.

**Deliverables.**

1. accepted chapter contract;
2. material and source packet for operational definitions, complete-path
   measurement, distributions, censoring, uncertainty, efficacy, and diagnosis;
3. nine section briefs;
4. complete-loop measurement figure, decision-changing distribution,
   evidence-record schema, and diagnosis algorithm briefs;
5. conflicting-measurements transfer task;
6. independent technical and quantitative audit;
7. lab interface for producing an honest evidence record; and
8. accepted exit-state packet for Chapter 4.

### WP4 — Chapter 4 Authoring Packet

**Capability.** Architect a runtime that continues through model failure.  
**Decision.** Choose services, cadences, ownership, queues, and failure behavior.
**Dossier delta.** Continuous runtime skeleton.

**Deliverables.**

1. accepted chapter contract;
2. material and source packet for continuous supervision, multi-rate execution,
   temporal contracts, finite queues, ordering, failure modes, and recovery;
3. eight section briefs;
4. multi-rate timeline, service-contract table, and supervisor-algorithm briefs;
5. synchronous-to-continuous transfer task;
6. independent architecture and failure audit;
7. lab interface for late, hung, restarted, and unavailable policy behavior; and
8. accepted exit-state packet for Chapters 5 through 8.

### WP5 — Foundation Integration

**Purpose.** Prove that Chapters 1 through 4 form one argument.

**Deliverables.**

- cross-chapter terminology and notation audit;
- concept first-use and deferral audit;
- requirement-to-measurement-to-runtime traceability map;
- coherent cumulative-system plates for versions 0.1 through 0.4;
- canonical-case state through Chapter 4;
- Part I and Part II narrative synopsis;
- duplication and gap report;
- Chapter 5 entry packet; and
- recorded reasons for rejected alternatives.

**Acceptance.** A reader can follow this reasoning without a hidden step.

1. This accepted action closes a consequential physical loop.
2. That world imposes a regime, timescale, and assumptions.
3. Those requirements become measurable claims with decision rules.
4. Those measured claims determine a runtime that continues when the learned
   component does not.

## Four-Lane Parallel Pipeline

The project has one integration lane and three worker lanes.

| Lane | Current responsibility | Output |
| --- | --- | --- |
| Architect | Resolve decisions, approve reviews, and update registries | Accepted packet version |
| Previous chapter | Technical, pedagogical, citation, continuity, and voice review | Diagnosed findings |
| Current chapter | Persistent steward develops the accepted architecture and later prose | Integrated chapter state |
| Next chapter | Research material, sources, misconceptions, counterexamples, and representations | Candidate packet |

Parallel work expands the available reasoning. It does not create several
competing manuscripts. Research, source discovery, representation proposals,
counterexamples, and red-team passes may run concurrently. Chapter objectives,
concept ownership, final section order, adjacent prose, notation changes, and
cross-chapter integration remain serialized through the architect.

When a chapter is unusually difficult, all three worker lanes may briefly fan
out across domain, pedagogy, and representation design. They converge before a
steward drafts prose.

## Progressive Context Contract

Every call receives a versioned packet. Accepted decisions accumulate. Raw
conversation and rejected drafts do not.

### Static Book Context

- terminal transfer performance;
- reader profiles and prerequisites;
- scope and exclusions;
- model-as-component and platform-neutrality rules;
- lab separation rule;
- visual grammar and minimal notation;
- canonical-case charter;
- terminology, source, representation, and traceability registries; and
- visible-chapter contract.

### Chapter Context

- observable objective and reader-facing callout text;
- entering state and accepted upstream artifacts;
- misconception and crux;
- owned, borrowed, and deferred concepts;
- engineering decision and dossier delta;
- section architecture and representation jobs;
- transfer task and lab boundary;
- overlap risks; and
- required exit state.

### Dynamic Section Context

- accepted section brief;
- immediately preceding accepted prose;
- compressed summary of earlier prose;
- current canonical-case state;
- approved sources and representation brief;
- open review findings; and
- what the next section may assume.

Every specialist returns proposed claims, definitions, sources, representations,
assumptions, disagreements, deferrals, and a candidate context delta. The
architect decides what becomes accepted context.

## Acceptance Reviews

### Contract Review

- The objective names one observable performance.
- The misconception and crux create a real need for the chapter.
- The decision changes the cumulative system.
- Owned and deferred concepts are explicit.
- The visible objective is a callout rather than a section.

### Fundamental-Material Review

- Indispensable concepts and their lineage are identified.
- Limits, counterexamples, and competing formulations are present.
- Current models and platforms illustrate rather than organize the chapter.
- The source packet is not a disguised literature survey.

### Section-Architecture Review

- Every section has one instructional job.
- Concepts appear in causal dependency order.
- Each section moves toward a measurement, representation, diagnosis, bound, or
  decision.
- The lab is not responsible for missing theory.

### Representation Review

- Every figure, table, equation, and algorithm enables a named inference.
- No representation assumes a later concept in completed form.
- Quantitative visuals have a source or are labeled as analytical examples.
- The cumulative plate remains visually coherent.

### Red-Team Review

- No hidden robotics, control, embedded, statistics, or probability prerequisite
  remains.
- No vendor or model family defines the argument.
- No false universal claim survives.
- Neighboring chapter ownership remains intact.
- The transfer task cannot be completed through imitation alone.

### Draft-Readiness Review

- Section, source, visual, example, and assessment briefs agree.
- The chapter steward can draft sequentially without making new architectural
  decisions.
- The chapter can stand without hardware.

### Foundation-Integration Review

- Chapters 1 through 4 create one continuous system state.
- Chapter 4 consumes actual requirements and evidence from Chapters 2 and 3.
- Terms and notation have one owner.
- Traceability links remain intact.
- Chapter 5 receives a complete measured runtime foundation.

Run `tools/check_chapter_contract.sh` after every chapter-structure change. It
checks objective, decision, and lab callout counts, keeps the objective before
the first H2, rejects editorial field names in the heading tree, and verifies
that the lab is the final reader-facing block.

## Ten-Day Foundation Schedule

The schedule assumes one architect and three worker lanes.

| Day | Architect | Review lane | Current steward | Next-chapter lane |
| ---: | --- | --- | --- | --- |
| 1 | Lock scope, notation, case, traceability, fault, and security decisions | Audit visible chapter scaffolds and control files | Validate Chapter 1 contract | Build Chapter 2 concept and source inventory |
| 2 | Approve Chapter 1 contract | Audit technical boundaries and neighboring disciplines | Build Chapter 1 backward-pedagogy map | Extend Chapter 2 counterexamples and claims |
| 3 | Resolve Chapter 1 findings | Red-team Chapter 1 architecture | Produce Chapter 1 section briefs | Draft Chapter 2 architecture and representation candidates |
| 4 | Accept Chapter 1 packet | Verify sources and representation briefs | Begin Chapter 2 stewardship | Build Chapter 3 concept and source inventory |
| 5 | Approve Chapter 2 contract and integration state | Red-team Chapter 2 | Produce Chapter 2 section briefs | Extend Chapter 3 measurement and diagnosis research |
| 6 | Integrate Chapters 1 and 2 | Audit Chapter 2 continuity and quantitative claims | Begin Chapter 3 stewardship | Build Chapter 4 runtime and fault inventory |
| 7 | Approve Chapter 3 contract | Red-team Chapter 3 | Produce Chapter 3 section briefs | Draft Chapter 4 architecture and representations |
| 8 | Integrate Chapters 1 through 3 | Audit Chapter 3 sources and measurements | Begin Chapter 4 stewardship | Pilot the Chapter 1 opening cluster with progressive context |
| 9 | Approve Chapter 4 contract | Red-team Chapter 4 | Produce Chapter 4 section briefs | Review the Chapter 1 pilot for comprehension and voice |
| 10 | Complete the foundation integration review and issue the Chapter 5 packet | Cross-chapter continuity audit | Close Chapter 4 findings | Revise the Chapter 1 pilot and validate the context ratchet |

At the end of Day 10, Chapters 1 through 4 are draft-ready, Chapter 1 has a
reviewed prose pilot, the cumulative dossier has reached runtime version 0.4,
and Chapter 5 has a valid entry packet. No lab contains build instructions yet.

## Immediate Launch Queue

The first parallel launch contains three specific tasks.

1. **Chapter-contract audit.** Verify the visible template, objective callout,
   lab placement, and separation of editorial metadata.
2. **Foundation-wave design.** Produce work packages, reviews, context inputs, and
   the rolling four-lane schedule.
3. **Technical red team.** Challenge Chapters 1 through 4, identify indispensable
   claims and sources, and expose missing book-wide decisions.

That launch has been completed. Its accepted findings are incorporated into
this plan and `WAVE-1-BRIEFS.md`.

The rolling pipeline has now advanced one stage beyond that first launch. The
foundation control packet is accepted; Chapter 1 has authoring, source, and
representation packets; and Chapter 2 has an architecture candidate. Manuscript
drafting is authorized only for a progressive Chapter 1 opening-cluster pilot.
The next parallel launch should build and verify the Chapter 1 visual assets,
check the pilot prose and figures against the resolved red-team findings, audit
the Chapter 2 claim-and-source spine, and begin Chapter 3 stewardship from the
accepted context packet.
