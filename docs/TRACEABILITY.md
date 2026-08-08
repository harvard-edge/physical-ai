# Physical AI Curriculum Traceability

**Status:** canonical audit map
**Sources:** `BOOK-GOAL.md`, `CHAPTER-OUTLINES.md`, `AUTHORING-SYSTEM.md`,
`PRODUCTION-PLAN.md`, and `WAVE-1-BRIEFS.md`

## Purpose

This document proves that the book's terminal performance is covered by the
chapter sequence, that each chapter contributes a distinct engineering decision
and dossier artifact, and that figures, tables, algorithms, and labs serve named
instructional jobs.

It is an audit surface, not a substitute for the detailed chapter scaffold.

## Terminal Performance Coverage

| **Graduate performance** | **Primary teaching** | **Reinforcement** | **Summative evidence** |
|---|---|---|---|
| Define the physical-AI boundary and causal loop | Chapter 1 | Chapters 2, 10, 12 | Loop charter and unfamiliar-system classification |
| Derive requirements from world dynamics and consequence | Chapter 2 | Chapters 5, 8, 9 | Requirements ledger and defended operating regime |
| Measure and diagnose the complete running loop | Chapter 3 | Chapters 4–13 | Evidence records and diagnosed final-review failure |
| Design a continuous runtime | Chapter 4 | Chapters 5–9 | Runtime skeleton and failure/recovery demonstration |
| Convert observation into time-indexed belief | Chapters 5–6 | Chapters 7, 8, 10 | Observation and estimator contracts |
| Treat VLMs and VLAs as policy interfaces | Chapter 7 | Chapters 8–10, 12 | Policy-interface card and intent contract |
| Keep actions within limits and check them independently | Chapter 8 | Chapters 9, 10, 13 | Action limits, refusal evidence, and recovery path |
| Place the complete system under shared constraints | Chapter 9 | Chapters 10, 13 | Placement map and re-placement sensitivity analysis |
| Build confidence from evidence tied to explicit claims | Chapter 10 | Chapters 12–13 | Assurance plan and promotion decision |
| Allocate meaningful human authority | Chapter 11 | Chapters 12–13 | Authority map and exercised revocation paths |
| Govern interaction data and system change | Chapter 12 | Chapter 13 | Provenance, coverage, update decision, and rollback |
| Make a release decision with explicit conditions | Chapter 13 | Final design review | Integrated deployment case and verdict |

No terminal performance depends on ownership of prescribed hardware. The final
design review requires transfer to an unfamiliar model, embodiment, or
environment.

## Chapter Alignment Matrix

| **Ch.** | **Primary verb** | **Engineering decision** | **Dossier artifact** | **Primary representation** | **Lab evidence** |
|---:|---|---|---|---|---|
| 1 | Frame | Choose the causal boundary | Loop charter | Two-world-state causal loop | Open- versus closed-loop divergence |
| 2 | Specify | Choose an operating regime | Requirements ledger | Efficacy versus information age | Measured freshness wall |
| 3 | Measure | Accept, reject, or narrow a claim | Evidence record | Loop boundary and tail distribution | Complete claim-and-verdict record |
| 4 | Architect | Choose services, cadences, and failure behavior | Runtime skeleton | Multi-rate runtime and lifecycle | Required behavior during service failure |
| 5 | Observe | Choose sensing strategy and operating point | Observation contract | Perception operating frontier | Quality, age, energy, and data tradeoff |
| 6 | Estimate | Choose state, frames, timing, and correction | State and timing model | Belief update and frame graph | Detected and corrected disagreement |
| 7 | Propose | Choose policy interface and escalation | Intent contract | Policy interface and chunk timeline | Grounding, latency, validity, and abstention |
| 8 | Enforce | Choose action limits, where they are checked, and recovery | Enforcement design | Proposal-to-command check | Refusal latency and stopping behavior |
| 9 | Place | Choose whole-system placement | Placement and resource map | Compute, trust, and failure domains | Multi-property re-placement ripple |
| 10 | Qualify | Promote, hold, or reject | Assurance and promotion record | Evidence ladder and invalidation | Offline versus closed-loop disagreement |
| 11 | Authorize | Allocate and revoke authority | Authority map | Authority sequence and state machine | Approval, override, revoke, inspect, forget |
| 12 | Change | Admit data and decide whether an update qualifies | Governed change record | Provenance and update loop | Data/update admission verdict |
| 13 | Deploy | Deploy, deploy under conditions, or refuse | Deployment case | Claim-argument-evidence map | Integrated release verdict |

Every row has a different primary verb and decision. Placement is one chapter's
integrating decision rather than the answer imposed on every topic.

## Concept Ownership and Progressive Disclosure

| **Concept** | **Introduced** | **Owned and defined** | **Later use without reteaching** |
|---|---:|---:|---|
| Causal closure and endogeneity | 1 | 1 | 2, 5, 10, 12 |
| Feedback and delegation constraints | 1 | 1 | Entire book |
| World timescale and information age | 2 | 2 | 3–10, 13 |
| Efficacy floor and operating regime | 2 | 2 | 3, 5, 9, 10, 13 |
| Operational definition and evidence record | 3 | 3 | 4–13 |
| Hypothesis, bisect, and confirm | 3 | 3 | Every later lab |
| Continuous runtime and lifecycle | 4 | 4 | 5–10, 13 |
| Proposal boundary | 4 | Completed in 7–8 | 9–13 |
| Observation contract | 5 | 5 | 6–10, 12 |
| State, frame, clock, belief, and innovation | 6 | 6 | 7–10, 12–13 |
| Operational world model | 6 | 6 | 7–10 |
| Generative world model as scenario tool | Foreshadowed in 6 | 10 | 13 |
| VLM as semantic component | Foreshadowed in 5 | 7 | 9–10, 12 |
| VLA as policy interface | 7 | 7 | 8–10, 12 |
| Action representation and embodiment adapter | 7 | 7 | 8–9, 12 |
| Action chunking and asynchronous policy execution | 7 | 7 | 8–10 |
| Skills with explicit limits and independent action checks | 8 | 8 | 9–10, 13 |
| Runtime assurance and independent enforcement | 8 | 8 | 9–10, 13 |
| Whole-system placement and shared budgets | Constraints recorded in 2–8 | 9 | 10, 13 |
| Evidence tier and promotion | 10 | 10 | 12–13 |
| Consent, approval, override, revocation, forgetting | Foreshadowed in 1 | 11 | 12–13 |
| Trajectory, provenance, coverage, and update decision | 12 | 12 | 13 |
| Integrated deployment claim | Foreshadowed in 1 | 13 | Final review |

The ownership pattern prevents three forms of repetition:

- earlier chapters record constraints without solving whole-system placement;
- later chapters consume measurement without reintroducing metrology; and
- human authority is established before interaction data may change the system.

## Modern Model Concepts

| **Modern concept** | **Instructional home** | **Durable systems question** | **Excluded treatment** |
|---|---|---|---|
| VLMs | Chapters 5 and 7 | What observations, context, grounding, latency, uncertainty, and egress does the interface require? | Transformer tutorial or model catalog |
| VLAs | Chapter 7 | What belief becomes what action proposal, at what cadence, for which embodiment? | Training recipe or leaderboard |
| Action tokens and continuous actions | Chapter 7 | What semantics, frames, interruption, and enforcement follow from the representation? | Decoder internals |
| Action chunks | Chapters 7–9 | How do horizon, overlap, freshness, cancellation, and shared serving affect behavior? | Treating chunks as tensor shapes |
| Generalist policies | Chapters 7 and 12 | What transfers, what requires adaptation, and what evidence remains embodiment-specific? | Dedicated model-family survey |
| Cross-embodiment learning | Chapters 7, 9, and 12 | What normalization, frames, skills, morphology, and action semantics must align? | Assuming dataset scale creates compatibility |
| Demonstrations and teleoperation | Chapter 12 | What trajectory, coverage, consent, operator bias, and lineage make experience admissible? | “Record and fine-tune” walkthrough |
| World foundation models | Chapter 10 | Which scenarios can they generate, and what claims do those scenarios fail to prove? | Treating generated worlds as evidence |
| Runtime assurance | Chapter 8 | Which trusted monitor, safe set, fallback, and timing protect the physical boundary? | Generic safety-layer box |

Model names may appear as dated case studies. The instructional question remains
valid when the example is replaced.

## Representation Coverage

| **Ch.** | **Figure job** | **Table or schema job** | **Equation or quantitative tool** | **Algorithm or state transition** |
|---:|---|---|---|---|
| 1 | Distinguish digital output from causal closure | Compare neighboring disciplines | None | Boundary classification reasoning |
| 2 | Show the freshness wall | Convert consequences to requirements | Normalized loop-latency diagnostic | Consequence-to-requirement procedure |
| 3 | Expose measurement boundary and tail | Define the evidence record | Percentiles and uncertainty | Hypothesis → bisect → confirm |
| 4 | Show multi-rate runtime continuity | Assign service responsibility | Event-age and deadline budgets | Runtime supervisor |
| 5 | Reveal operating frontier | Specify observation contract | Data rate and observation age | Operating-point selection |
| 6 | Separate evidence from belief | Distinguish state and memory meanings | State transition and observation model | Predict → observe → correct |
| 7 | Separate policy interfaces and show chunk time | Compare action representations | Validity and escalation budgets | Abstain and escalate |
| 8 | Separate proposal from physical authority | Specify skills and limits | Calculate stopping margin | Validate, refuse, execute, recover |
| 9 | Map complete loop onto compute and trust domains | Record placement evidence | Shared resource constraints | Placement ripple audit |
| 10 | Show evidence ladder and invalidation | Compare evidence tiers | Coverage and promotion thresholds | Promote, hold, reject |
| 11 | Attach roles to operations | Record authority and revocation | Intervention and revocation timing | Approve, override, revoke, forget |
| 12 | Show provenance and controlled change | Specify trajectories | Coverage and intervention rates | Admit, evaluate, deploy, roll back |
| 13 | Connect release claims to evidence and gaps | Record hazards and owners | Time to safe versus time to harm | Release decision |

A representation remains optional until its brief names the inference it makes
easier. This matrix states required instructional jobs, not a quota of artifacts.

## Lab Manifestation Matrix

| **Ch.** | **Analytical manifestation** | **Hosted manifestation** | **Physical manifestation** | **Decision preserved across all forms** |
|---:|---|---|---|---|
| 1 | Compare causal traces | Toggle advisory and closed-loop traces | Same model with and without allowed actuation | Classify and bound the system |
| 2 | Calculate information-age regimes | Explore a recorded freshness curve | Inject delay into a moving task | Choose operating regime |
| 3 | Audit conflicting measurement records | Instrument and inspect a replayable loop | Measure the complete sensor-to-effect path | Accept or narrow a claim |
| 4 | Analyze a runtime event trace | Fault-inject services in an interactive runtime | Hang or restart a policy while supervision continues | Choose runtime and failure behavior |
| 5 | Compare sensing frontiers from supplied data | Vary resolution, cadence, or semantic path | Change sensor acquisition settings | Choose observation operating point |
| 6 | Correct timestamped frame/state records | Inject frame, clock, and drift errors | Misalign a sensor or clock | Choose state and correction policy |
| 7 | Compare policy-interface cards | Run contrasting VLM/VLA proposal paths | Generate expiring intents against live state | Choose interface and escalation |
| 8 | Evaluate action limits and stopping cases | Submit valid and invalid proposals to an independent check | Refuse and stop an actuator under stated limits | Choose where actions are checked |
| 9 | Solve and perturb a placement map | Re-place services in a profiled runtime | Move work across heterogeneous compute | Accept or reject placement |
| 10 | Audit evidence-tier claims | Compare replay, simulation, and shadow traces | Introduce controlled closed-loop divergence | Promote, hold, or reject |
| 11 | Analyze an authority failure sequence | Exercise approval, revocation, and deletion | Trigger intervention and verify effect | Allocate and test authority |
| 12 | Audit trajectory lineage and coverage | Curate and evaluate a candidate update | Collect interaction records with a defined scope | Admit data and decide on change |
| 13 | Assemble a release case from conflicting records | Interactive claim-evidence audit | Run failure, egress, recovery, and authority checks | Deploy, deploy under conditions, or refuse |

The physical manifestation is not inherently the strongest evidence. The claim,
regime, coverage, and measurement boundary determine what each manifestation can
support.

## Dossier Completeness at the Final Review

| **Required final evidence** | **Produced by** | **Failure if missing** |
|---|---:|---|
| Causal boundary and affected people | 1 | The system under review is undefined |
| Requirements, assumptions, and operating limits | 2 | Performance and safety claims lack a regime |
| Valid measurement and diagnosis records | 3 | Later numbers are not defensible |
| Runtime, lifecycle, and failure behavior | 4 | Continuous operation is unspecified |
| Observation contract | 5 | Belief inputs have no validity semantics |
| State, frames, timing, and uncertainty | 6 | Policy acts on ambiguous or stale state |
| Policy interface and intent contract | 7 | Model output cannot be interpreted or checked against limits |
| Skills, envelope, enforcement, and recovery | 8 | Learned proposal has uncontrolled authority |
| Placement, resources, and failure domains | 9 | System budgets and isolation cannot be defended |
| Scenario coverage and promotion history | 10 | Deployment confidence exceeds the evidence |
| Authority, consent, revocation, and exit | 11 | Human control is ceremonial or absent |
| Data lineage, change record, and rollback | 12 | The deployed system can change without governance |
| Integrated claim, evidence, gaps, and verdict | 13 | No accountable release decision exists |

## Authoring-System Requirement Coverage

| **Authoring requirement** | **Authoritative evidence** |
|---|---|
| Detailed project goal and scope | `BOOK-GOAL.md` |
| Thirteen cumulative teaching chapters | `CHAPTER-OUTLINES.md` |
| Chapter objectives, decisions, artifacts, sections, and lab handoffs | `CHAPTER-OUTLINES.md` |
| Reader-facing objective callout, natural chapter form, and lab-last rule | `BOOK-GOAL.md`, `AUTHORING-SYSTEM.md`, and `PRODUCTION-PLAN.md` |
| Progressive context and accepted-context ratchet | `AUTHORING-SYSTEM.md` |
| Agent roles, calls, review passes, and parallel pipeline | `AUTHORING-SYSTEM.md` |
| Executable work packages, reviews, schedule, and context inputs | `PRODUCTION-PLAN.md` |
| Foundation-wave claim spines, representations, source families, and deferrals | `WAVE-1-BRIEFS.md` |
| Accepted foundation context, notation, case, fault taxonomy, and permissions | `packets/CONTEXT-v1.yml` |
| Chapter 1 contract, section briefs, representations, transfer, and lab boundary | `packets/CH01-AUTHORING-PACKET.md` |
| Chapter 1 claim qualifications and source set | `packets/CH01-SOURCE-PACKET.md` |
| Chapter 1 visual claims, compositions, encodings, and consistency check | `packets/CH01-REPRESENTATION-PACKET.md` |
| Chapter 2 contract, section architecture, requirement schema, and lab boundary | `packets/CH02-AUTHORING-PACKET.md` |
| Mechanical visible-chapter contract check | `../tools/check_chapter_contract.sh` |
| PhysicalAI-specific visual thesis and grammar | `BOOK-GOAL.md` and private `visual-system.md` |
| Figure families, generation, and rendered QA | private `figures.md` |
| Table discipline | private `tables.md` |
| Lab separation and three manifestations | `BOOK-GOAL.md`, `CHAPTER-OUTLINES.md`, and private `pedagogy-and-labs.md` |
| Concept ownership and progressive disclosure | This document and private `chapter-architecture.md` |
| Model, vendor, robotics-survey, and shallow-tutorial exclusions | `BOOK-GOAL.md` and `AUTHORING-SYSTEM.md` |

## Change Control

A proposed chapter change must identify:

1. the terminal performance it improves;
2. the concept owner it changes;
3. the dossier artifact and downstream chapters affected;
4. the representation and lab contracts that must change;
5. the legacy or duplicate material it replaces; and
6. the evidence that the revised dependency remains complete.

Adding a fashionable model, tool, or hardware example without changing an
instructional decision is not a chapter-level change. Treat it as a dated case
study and verify that the underlying systems question remains visible.
