# Chapter 1 Claim and Source Packet

**Status:** core claims and supporting locations verified; permanent SEBoK
revision pin and final bibliography records remain  
**Chapter:** From ML Systems to Physical AI  
**Packet:** `CTX-FND-001`

## Editorial Conclusion

The Chapter 1 scope test is defensible as this book's operational boundary. It
is a synthesis rather than an established definition of Physical AI.

> A system is in scope when a learned proposal is causally material to an
> action path, an allowed action changes task-relevant physical state and can
> alter a later observation or choice, and the system exercises delegated
> physical authority over that action.

The classification therefore uses three checks.

1. **Learned component.** A learned proposal materially affects the action path.
2. **Consequential physical feedback.** An allowed action changes task-relevant
   physical state and can alter later observations or choices.
3. **Delegated physical authority.** The engineered system has permission to
   initiate or shape a defined class of physical actions under stated limits.

Authority is delegated. Consequence results. The manuscript should not use
“delegated physical consequence” as its preferred term.

## Claim Ledger

### `CLM-CH01-001` — A Model Is Not the System

**Claim.** A deployed learned model is one component of a larger ML system whose
behavior also depends on data, interfaces, serving infrastructure, monitoring,
consumers, and feedback paths.

**Classification.** Established systems observation.

**Qualification.** Do not say that ML systems necessarily end at predictions or
are inherently open loop. Existing ML-systems work explicitly discusses hidden
feedback loops, undeclared consumers, boundary erosion, and changes in the
external world.

**Support.** `SRC-MLDEBT-001`.

### `CLM-CH01-002` — Feedback Is Established Lineage

**Claim.** Feedback couples dynamical systems so that each influences the
other's subsequent behavior and appears in physical, biological, informational,
and social systems.

**Classification.** Established concept.

**Qualification.** Feedback cannot define Physical AI by itself. Digital
markets, recommenders, adaptive services, and human organizations also contain
feedback.

**Support.** `SRC-FEEDBACK-001`.

### `CLM-CH01-003` — Physical Coupling Has Cyber-Physical Lineage

**Claim.** Cyber-physical systems integrate computation, networking, and
physical processes, commonly with physical processes affecting computation and
computation affecting physical processes.

**Classification.** Established field definition.

**Qualification.** Position Physical AI as a learned-systems specialization or
engineering lens within this lineage. Do not imply that computation-to-physical
coupling begins with current AI models.

**Support.** `SRC-CPS-001`.

### `CLM-CH01-004` — Action Makes Later Inputs Policy-Dependent

**Claim.** In sequential decision and control problems where actions affect
state transitions, a policy's actions can influence the states or observations
it later encounters.

**Classification.** Established result.

**Qualification.** Use “influences,” not “determines.” Disturbances, other
agents, dynamics, and sensing also shape later observations. Endogeneity does
not require online learning.

**Support.** `SRC-DAGGER-001`.

### `CLM-CH01-005` — Endogeneity Is Not Uniquely Physical

**Claim.** Predictions used in decisions can change the outcomes or populations
they aim to predict and thereby change the deployment distribution.

**Classification.** Established counterexample.

**Qualification.** Credit decisions, traffic or crime predictions,
recommendations, trading, and prices can be endogenous without the system
exercising physical actuation. By this book's scope convention, future-input
change is necessary for the feedback half of the test but insufficient for its
Physical AI boundary.

**Support.** `SRC-PERFORMATIVE-001`.

### `CLM-CH01-006` — The Scope Test Is This Book's Synthesis

**Claim.** The book classifies a learned system as Physical AI when a learned
proposal is causally material to an action path, an allowed action changes
task-relevant physical state and can alter a later observation or choice, and
the system exercises delegated physical authority over that action.

**Classification.** Book synthesis.

**Qualification.** This is a scope convention, not a theorem or a consensus
field definition. A person may approve a high-level task while the system
retains delegated authority over timing, trajectory, force, duration, or
low-level execution. Informational presentation remains advisory for this book
even when its downstream effects are serious.

**Lineage.** `SRC-CPS-001`, `SRC-DAGGER-001`, `SRC-AUTOMATION-001`,
`SRC-SYSTEM-CONTEXT-001`, and `SRC-NIST-AIRMF-001`.

### `CLM-CH01-007` — Authority Can Be Allocated by Stage and Level

**Claim.** Automation may participate separately in information acquisition,
analysis, decision selection, and action implementation, with different levels
of automation at each stage.

**Classification.** Established human-automation model.

**Qualification.** “Human in the loop” is not an authority specification.
Accordingly, this book's loop charter records what the system may select,
initiate, shape, execute, and stop, and what remains with a person. That charter
is the book's design rule rather than a prescription from the cited automation
literature. Chapter 11 owns the detailed rights, timing, revocation, and
accountability design.

**Support.** `SRC-AUTOMATION-001` and `SRC-SUPERVISORY-001`.

### `CLM-CH01-008` — The Boundary Serves a Claim

**Claim.** A system boundary is selected for an engineering purpose. The wider
context contains interacting technical, natural, and social systems needed to
understand behavior and consequence.

**Classification.** Established systems-engineering principle.

**Qualification.** Distinguish the engineered system, wider causal context,
authority boundary, and affected people. Do not draw a person inside a
controlled-system box merely because that person influences behavior.

**Support.** `SRC-SYSTEM-CONTEXT-001` and `SRC-SAFER-WORLD-001`.

### `CLM-CH01-009` — Affected People Extend Beyond Operators

**Claim.** AI systems are sociotechnical, and affected people need not directly
interact with the deployed system.

**Classification.** Established risk-management principle.

**Qualification.** Name roles such as requester, nearby collaborator,
bystander, data subject, owner, operator, and maintainer rather than using a
generic human icon.

**Support.** `SRC-NIST-AIRMF-001`.

### `CLM-CH01-010` — Feedback and Authority Are Independent

**Claim.** Feedback concerns how observed behavior or state is coupled back to
influence later behavior. Delegation concerns which functions and actions the
engineered system is permitted to perform.

**Classification.** Book synthesis supported by established lineages.

**Qualification.** A system may respond promptly while exercising excessive
authority. It may also have legitimate authority while acting on stale state.

**Support.** `SRC-FEEDBACK-001`, `SRC-AUTOMATION-001`, and
`SRC-SUPERVISORY-001`.

### `CLM-CH01-011` — The Book Extends Rather Than Replaces

**Claim.** The book brings an ML-systems method to learned components that
participate in physical action while borrowing established ideas from control,
robotics, cyber-physical systems, systems engineering, human factors, safety,
and security.

**Classification.** Positioning synthesis.

**Qualification.** Reject claims that control assumes completely known plants,
robotics assumes tightly defined workcells, cyber-physical systems concern only
deterministic dynamics, ML systems are universally open loop, or human
oversight is unique to Physical AI.

**Support.** ML systems through `SRC-MLDEBT-001`; control through
`SRC-FEEDBACK-001`; cyber-physical systems through `SRC-CPS-001`; robotics
through `SRC-ROBOTICS-001`; systems context through `SRC-SYSTEM-CONTEXT-001`;
human automation through `SRC-AUTOMATION-001`; safety through
`SRC-SAFER-WORLD-001`; and systems security through `SRC-NIST-SSE-001`.

## Verified Supporting Locations

| Claim | Supporting location | Use boundary |
| --- | --- | --- |
| `CLM-CH01-001` | Sculley et al., PDF p. 1, Abstract and §1; p. 4, Figure 1 and §4 | System dependencies, surrounding infrastructure, consumers, monitoring, and feedback |
| `CLM-CH01-002` | Åström and Murray, printed p. ix; §1.1, pp. 1-1–1-2 and Figure 1.1 | Feedback lineage and breadth; digital examples require Sculley or Perdomo |
| `CLM-CH01-003` | Lee and Seshia, Chapter 1, printed p. 1; p. 5, Figure 1.1 and surrounding text | Computation and physical processes interact, commonly through feedback |
| `CLM-CH01-004` | Ross et al., proceedings p. 627, Abstract and §1; p. 628, §2 and Eq. (1) defining \(d_\pi\) | Policy-induced observation distributions in sequential imitation learning |
| `CLM-CH01-005` | Perdomo et al., PDF p. 1, Abstract and §1; pp. 1–2, §1.1 and \(D(\theta)\) | Deployment-dependent distributions in credit, traffic, crime, recommendation, trading, and pricing examples |
| `CLM-CH01-006` | Lee and Seshia pp. 1, 5; Ross pp. 627–628; Parasuraman et al. pp. 286, 288–289; SEBoK system-of-interest section; NIST AI RMF pp. 26–27, 37, 40 | Composite lineage only; the exact scope test remains book synthesis |
| `CLM-CH01-007` | Parasuraman et al., p. 286 Abstract; p. 288 §III and Figure 2; p. 289 §§C–D; Sheridan et al., printed p. 344 Figure 1 and p. 349 §4 | Automation stages and levels; the loop-charter verbs remain a book design rule |
| `CLM-CH01-008` | SEBoK, narrower and wider system-of-interest paragraphs; Leveson, Chapter 4, pp. 81–82 and Figure 4.4; §4.3 p. 87 | Purpose-dependent boundaries and wider sociotechnical context |
| `CLM-CH01-009` | NIST AI RMF, printed p. 1 and Appendix A p. 37 | Sociotechnical systems and affected people who need not directly interact |
| `CLM-CH01-010` | Åström and Murray §1.1, pp. 1-1–1-2; Parasuraman et al. pp. 287–289; Sheridan et al. pp. 344, 349 | Feedback and automation allocation support the book's independence synthesis |
| `CLM-CH01-011` | Sculley pp. 1, 4; Åström and Murray §1.1 and §15.6 p. 15-30; Lee and Seshia pp. 1, 5; *Modern Robotics* Chapters 2–13; SEBoK system-of-interest section; Parasuraman pp. 286–289; Leveson Chapter 4; NIST SP 800-160 Vol. 1 Rev. 1 Abstract | Source-by-discipline positioning rather than one diffuse citation |

The SEBoK entry is a living source and must be pinned to a permanent revision in
the final bibliography. Page-level Parasuraman citations should use the primary
IEEE article rather than only its PubMed abstract.

## First-Use Definitions

| Term | Chapter 1 definition | Boundary |
| --- | --- | --- |
| Learned proposal \(p_t\) | A candidate interpretation, target, intent, or action produced by a learned component that has not acquired physical authority | Chapter 7 later defines the complete intent contract |
| Allowed action \(u_t\) | An action issued to the physical process after the applicable authority path and system checks permit it | Permission is not proof of safety |
| Physical consequence | An observable change in matter, a body, environment, energy flow, physical access, or physical process caused through actuation | Informational presentation alone is excluded by this book's convention |
| Feedback | Use of observed system behavior or state to influence subsequent behavior | Established control and cybernetics lineage |
| Consequential physical feedback | A system-issued action changes task-relevant physical state and can alter later observation or choice | Book term |
| Endogeneity | Dependence of later task-relevant states or observations on earlier system actions | The policy is not necessarily the only cause |
| Delegated physical authority | Permission assigned to the engineered system to initiate or shape a defined class of physical actions under stated conditions | May be shared, supervised, conditional, or revocable |
| Authority boundary | The interface across which responsibility for selecting, permitting, initiating, or stopping action changes hands | Not necessarily a hardware boundary |
| System boundary | The chosen limit of the engineered system for a particular claim or decision | Pair with a wider causal context |
| Affected person | Someone exposed to the system's observation, action, data, or consequence whether or not they operate it | Use named roles |
| Physical AI, in this book | A learned system in which a learned proposal is causally material to an action path, an allowed action changes task-relevant physical state and can alter a later observation or choice, and the system exercises delegated physical authority over that action | Working definition, not a universal standard |

## Scope-Test Counterexamples

| System | Learned action path | Consequential physical feedback | Delegated physical authority | Book-scope verdict |
| --- | ---: | ---: | ---: | --- |
| Image-description model | Yes | No | No | ML component, out of scope |
| Recommender | Yes | Digital endogeneity only | No physical actuation | Adjacent digital ML |
| Scripted thermostat | No | Yes | Yes | Control or CPS, not learned Physical AI |
| Learned HVAC controller | Yes | Yes | Yes | In scope |
| Inspection model that alerts a worker | Yes | Human-mediated | No automated actuation | Advisory ML system |
| Inspection model that activates a rejector | Yes | Yes | Yes | In scope |
| Directly teleoperated robot without learned action selection | No | Yes | Human retains action selection | Robotics or CPS, not learned Physical AI |
| Human-approved learned handling proposal with automated execution | Yes | Yes | Shared and conditional | In scope; show the authority path |

These are book-scope verdicts, not judgments that excluded systems are harmless
or unimportant.

## Source Registry

### `SRC-MLDEBT-001`

Sculley et al., [“Hidden Technical Debt in Machine Learning
Systems”](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems).

Use for the model-as-component claim, system dependencies, hidden feedback
loops, and the continuation from ML systems.

### `SRC-DAGGER-001`

Ross, Gordon, and Bagnell, [“A Reduction of Imitation Learning and Structured
Prediction to No-Regret Online
Learning”](https://proceedings.mlr.press/v15/ross11a.html).

Use for policy-induced observation distributions and the failure of fixed-
distribution assumptions in sequential action.

### `SRC-PERFORMATIVE-001`

Perdomo et al., [“Performative
Prediction”](https://proceedings.mlr.press/v119/perdomo20a.html).

Use as the counterexample showing that feedback and endogeneity are not uniquely
physical.

### `SRC-FEEDBACK-001`

Åström and Murray, [*Feedback
Systems*](https://fbswiki.org/wiki/index.php/FBS).

Use for feedback and control lineage. The adaptive and learning-control material
also prevents a caricature of control as excluding learning.

### `SRC-CPS-001`

Lee and Seshia, [*Introduction to Embedded Systems: A Cyber-Physical Systems
Approach*](https://ptolemy.berkeley.edu/books/leeseshia/download.html).

Use for computation-to-physical integration, mutual feedback, and the
relationship to cyber-physical systems.

### `SRC-NIST-AIRMF-001`

NIST, [*Artificial Intelligence Risk Management Framework
1.0*](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10).

Use for sociotechnical context, affected individuals and communities, deployment
scope, human oversight, and context-dependent boundaries.

### `SRC-NIST-SSE-001`

NIST, [*Engineering Trustworthy Secure Systems*, SP 800-160 Vol. 1 Rev.
1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final).

Use for the systems-security lineage: trustworthiness and security properties
must be engineered across the system lifecycle, not attached to a model after
deployment.

### `SRC-SYSTEM-CONTEXT-001`

SEBoK, [“Engineered System
Context”](https://sebokwiki.org/wiki/Engineered_System_Context).

Use for purpose-dependent system boundaries, wider context, exchanges, and
stakeholders.

### `SRC-AUTOMATION-001`

Parasuraman, Sheridan, and Wickens, [“A Model for Types and Levels of Human
Interaction with Automation”](https://pubmed.ncbi.nlm.nih.gov/11760769/).

Use for separating information, decision, and action automation and for making
delegated authority nonbinary.

### `SRC-SUPERVISORY-001`

Sheridan, Verplank, and Brooks, [“Human/Computer Control of Undersea
Teleoperators”](https://ntrs.nasa.gov/citations/19790007441).

Use for supervisory control, intermittent human involvement, and authority over
lower-level execution.

### `SRC-SAFER-WORLD-001`

Leveson, [*Engineering a Safer
World*](https://mitpress.mit.edu/9780262016629/engineering-a-safer-world/).

Use for sociotechnical control structures and why a software-only boundary is
often inadequate for consequence analysis.

### `SRC-ROBOTICS-001`

Lynch and Park, [*Modern Robotics: Mechanics, Planning, and
Control*](https://hades.mech.northwestern.edu/index.php/Modern_Robotics).

Use to credit robotics' established ownership of mechanics, planning, and
control and to avoid straw-man positioning.

### `SRC-ROBOT-VOCAB-001`

ISO, [*ISO 8373:2021 Robotics —
Vocabulary*](https://www.iso.org/standard/75539.html).

Use only when standardized robotics terminology is needed. The book's scope
must not depend on whether a device satisfies a robot definition.

## Canonical-Case Audit

Keep the shared-workspace handler. It makes \(W_t \rightarrow W_{t+1}\)
visible and can use the same learned component in advisory and delegated modes.
It can later support classifiers, semantic requests, VLMs, VLAs,
demonstrations, and governed updates without requiring those concepts in Chapter
1.

Tighten the case before drafting.

- The service routes or relocates a requested object within a shared work
  surface.
- Task state includes object identity and pose, destination zones, human
  occupancy, pending request, and system status.
- The learned role identifies or grounds the requested object or proposes a
  handling target.
- Proposal \(p_t\) contains a candidate object, destination, and requested
  action.
- Allowed action \(u_t\) is move, divert, stop, hold, or request clarification.
- Early success means the correct object reaches the declared destination
  without entering an excluded zone or violating an operating condition.
- Requester, nearby collaborator, bystander, operator or owner, and maintainer
  remain separate roles.
- Interaction data and updates remain disabled until Chapters 11 and 12.

Pair the case regularly with a learned HVAC or process-control example and a
powered assistive or access-control example. This prevents the manuscript from
quietly becoming a manipulation book.

## Citation-Audit Queue

Before Chapter 1 prose is accepted:

1. pin the SEBoK entry to a permanent revision;
2. cite the primary IEEE article for Parasuraman et al. using
   [DOI 10.1109/3468.844354](https://doi.org/10.1109/3468.844354);
3. use ISO 8373 only for terminology available in the public record, not as
   support for the book's scope test;
4. mark `CLM-CH01-006` and `CLM-CH01-010` as book synthesis rather than sourced
   field definitions;
5. ensure “endogeneity” is not used for every form of distribution shift;
6. ensure no cited source is used to caricature a neighboring discipline;
7. preserve the counterexamples that limit the scope test; and
8. complete final bibliography formatting and access-date records.
