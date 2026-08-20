# The Permitter's Check List

**Status:** the gating artifact for Part II. Draft for review.
**Depends on:** `.claude/rules/chapter-architecture.md`, `.claude/rules/north-star.md`
**Status note:** the `docs/` planning tree it replaced was retired on 2026-08-19.


## Why this document exists

The book's matrix can be one of two things. It can be a taxonomy that the
chapters populate, in which case Part II is an expansion of a table Chapter 3
already printed. Or it can be the audit that the permitter runs before it allows
an unverified proposal to move matter, in which case each Part II chapter earns
its place by adding checks that the permitter could not otherwise perform.

This document takes the second reading and writes the audit first. Chapter 12 is
where a student defends a system against this list. Everything in Part II exists
to produce the evidence one of these checks consumes.

**The test that governs Part II.** A chapter section is load-bearing if deleting
it would remove a check from this list or leave a check without evidence. A
section that does neither is a survey and does not ship.


## How to read a check

Each check has five fields.

| Field | Meaning |
| --- | --- |
| **ID** | Stable identifier. Referenced by chapters and notebook checkpoints. |
| **Check** | What the permitter verifies, stated so it can fail. |
| **Falsifiable as** | The observation that would show the check failing on a bench. |
| **Produced by** | The chapter that gives the reader the ability to construct this check. |
| **Evidence** | The notebook checkpoint carrying the number or argument. |

A check that cannot fail on a bench is not a check. It is a wish, and it does
not belong on this list.


## Class A. Freshness and identity of the evidence

The permitter is acting on a description of the world. Before anything else it
must establish that the description is recent enough and is about the world it
is currently in.

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **A1** | Every input carries a timestamp taken at the physical event, not at software arrival. | Two sensors agree on a scene but disagree on when it happened; a logged transform is 65 ms older than its header claims. | Ch4 | observation contract |
| **A2** | The age of information at the point of use is bounded at $P_{99.9}$, not at the mean. | A $P_{50}$ that meets budget while one cycle in a thousand exceeds it by 8x. | Ch4, Ch2 | requirements ledger, observation contract |
| **A3** | All timestamps resolve to one clock domain, and the offsets between domains are measured rather than assumed. | Monotonic and wall clock mixed in one fusion step; PTP holdover drift unlogged. | Ch4 | observation contract |
| **A4** | A proposal names the observation it was derived from, and the permitter can reject a proposal whose observation has expired. | A trajectory executing against a scene that was overwritten two frames ago. | Ch4, Ch6 | intent schema |
| **A5** | Belief that was propagated rather than measured is labeled as such and carries its growth since last measurement. | An occluded object reported at a coordinate with the same confidence it had when visible. | Ch5 | state and timing model |
| **A6** | Every retained belief has a time to live after which it may not authorize action. | A map entry from four minutes ago still admitting a grasp. | Ch5 | state and timing model |

## Class B. Physical admissibility

This is the class the current architecture handles well. It is also the smallest
of the four admissibility classes, which is the point the book has not yet made.

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **B1** | The commanded state lies inside the certified safe set, evaluated within a bounded time. | A QP that occasionally takes two iterations too many and misses its tick. | Ch8 | enforcement design |
| **B2** | Stopping distance at current velocity, computed with the measured $P_{99}$ delay, is less than measured clearance. | $d_{\text{stop}}$ computed with mean latency instead of tail. | Ch8, Ch2 | enforcement design, requirements ledger |
| **B3** | Every emitted trajectory terminates in a state from which the system can still stop. | A plan that is feasible for its horizon and leaves the machine committed past it. | Ch7 | planning schema |
| **B4** | Commanded torque rate stays inside the drivetrain's shear limit, and the enforcement action itself does not violate it. | A clamping veto that injects a step and shears what it was protecting. | Ch7, Ch8 | planning schema, enforcement design |
| **B5** | Integrated current over a duty cycle stays below the continuous thermal rating, not merely the instantaneous limit. | A kinematically legal cycle that cooks a winding over ninety seconds. | Ch7, Ch8 | enforcement design |
| **B6** | The authority chain below the permitter is enumerated, and each layer's autonomous behavior on comms loss is known and tested. | A smart drive that coasts on timeout where the safety case assumed it brakes. | Ch8 | enforcement design |

## Class C. Semantic admissibility

The proposal may be physically legal and still be about the wrong thing.

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **C1** | Intent is expressed in a form a cheaper checker can reject without rerunning the reasoner. | A goal that can only be validated by asking the model again. | Ch6 | intent schema |
| **C2** | Every intent expires, and the behavior during the gap between expiry and the next intent is specified and tested. | An arm that holds a stale goal through a four second reasoning stall. | Ch6 | intent schema |
| **C3** | The target of an action is reachable and inside the declared workspace before planning begins. | A grasp planned for a pose outside the kinematic envelope. | Ch6 | intent schema |
| **C4** | Intent revocation propagates to the permitter faster than the action it revokes can complete. | A revoked goal whose trajectory finishes anyway. | Ch6, Ch8 | intent schema, enforcement design |

## Class D. Epistemic admissibility

**This class currently has no mature mechanism, and the book must say so.** It
is also the class that accounts for most real deployment failures: a smooth,
in-envelope, kinematically legal action toward the wrong object produces no
timing anomaly and no invariant violation, and every check in classes A and B
passes it.

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **D1** | The proposal is accompanied by a usable statement of the model's confidence, and that statement is calibrated against held-out physical outcomes. | A policy reporting high confidence on a scene unlike anything in training. | Ch6, Ch11 | intent schema, release case |
| **D2** | An out-of-distribution input is detected before its proposal reaches the permitter, or the system declares that it cannot detect one. | Novel lighting producing fluent, confident, wrong output. | Ch6, Ch11 | release case |
| **D3** | Each stage has a named detector for its silent degradation mode, with a stated diagnostic coverage. | A smeared lens returning valid frames at 30 Hz for an hour. | Ch4 to Ch8 | every artifact |
| **D4** | Calibration state is monitored and its drift bounds the claims that depend on it. | Extrinsics that walked with temperature and were never rechecked. | Ch5 | state and timing model |
| **D5** | The permitter's own world model is checked against the perception it is fed, so guaranteed invariance is not asserted over a world that does not exist. | A barrier function proving safety against an obstacle set that missed the obstacle. | Ch8, Ch11 | enforcement design, release case |

## Class E. Authority

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **E1** | A human can assume control at any point, and the transfer does not itself inject a transient. | A takeover that jerks the arm at the moment of handover. | Ch10 | authority design |
| **E2** | Authority state is unambiguous at all times and observable by the operator. | Two subsystems each believing the other is in control. | Ch10 | authority design |
| **E3** | Data produced during intervention and recovery is tagged and cannot silently enter training. | A recovery maneuver teaching the policy that the approach preceding it was correct. | Ch10 | authority design |
| **E4** | Consent and retention constraints on recorded data are enforced where the data is produced. | Faces retained from a workspace camera with no stated basis. | Ch10 | authority design |

## Class F. The permitter's own integrity

The permitter is a controller. It can fail, and it can cause the harm it exists
to prevent. A safety argument that omits this class is a component reliability
argument wearing a systems safety costume.

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **F1** | The permitter continues to enforce when everything above it stops. | A kernel panic that leaves a timer latched at 78 percent duty. | Ch3, Ch8 | workflow charter, enforcement design |
| **F2** | The permitter allocates no memory dynamically and its worst case execution time is analyzable. | A heap allocation on the enforcement path found in review. | Ch8 | enforcement design |
| **F3** | The permitter does not deadlock conservatively, and its conservatism is measured. | A robot that stops permanently in a doorway it could safely pass. | Ch8, Ch11 | enforcement design |
| **F4** | The permitter does not chatter at the constraint boundary. | Sustained oscillation at the barrier under a policy pushing against it. | Ch8 | enforcement design |
| **F5** | The permitter's intervention rate and correction magnitude are logged, so it is known whether the proposer is improving or the enforcer is doing all the work. | An intervention rate nobody has ever measured. | Ch8, Ch10 | enforcement design, authority design |
| **F6** | The permitter is itself subjected to the hazard analysis applied to everything else. | An STPA that covers the policy and stops at the safety layer. | Ch11 | release case |

## Class G. Evidence and release

| ID | Check | Falsifiable as | Produced by | Evidence |
| --- | --- | --- | --- | --- |
| **G1** | Every claim in the release case names its evidence tier: replay, rig, shadow, or live closed loop. | A live safety claim resting on a simulator run. | Ch11 | release case |
| **G2** | Every quantity carries provenance: hardware, thermal state, measurement point, date. | A latency number nobody can reproduce. | Ch11 | release case |
| **G3** | Seeded faults across layers are survived without breaking a stated invariant. | An injected bus stall that produces a physical violation. | Ch11 | release case |
| **G4** | The system's placement across silicon does not create a shared failure domain the safety case assumed was independent. | A permitter sharing a power rail with the thing it polices. | Ch9 | placement ledger |
| **G5** | The verdict is Deploy, Condition, or Refuse, with named conditions and a named owner. | A defense that ends in a demonstration rather than a decision. | Ch12 | full dossier |


## What this list implies for Part II

**Chapter 4 (Perceive)** owns the clock. A1, A2, A3, and the perception half of
D3. Timestamps are minted here and every later freshness claim cites this
chapter. Its dominant column is silicon determinism, because the ingestion path
is where age is manufactured.

**Chapter 5 (Remember)** owns the distinction between measured and propagated,
and owns the body as well as the world. A5, A6, D3, D4. Redefining Remember as
persistent state of the world *and of the body* gives calibration a home and
gives the thermal column a real cell.

**Chapter 6 (Reason)** owns the lease, not the reasoner. C1 through C4, D1, D2.
The chapter's center of gravity is the intent contract, not a survey of vision
language models. Reason against inertia is a two sentence closure that points
forward to B3.

**Chapter 7 (Plan)** owns feasibility and continuity. B3, B4, B5. It also owns
the durable systems idea in the row, which is that inference compute is a
resource scheduled against a deadline rather than a fixed tax.

**Chapter 8 (Execute)** owns physical admissibility and its own integrity. B1,
B2, B6, F1 through F5, D5. It is the only chapter where the permitter is the
subject rather than the audience, and it is the chapter least at risk from
model convergence.

**Every Part II chapter** closes D3 for its own row: the silent degradation mode
and its detector.


## Open questions this list does not settle

1. Whether class D deserves its own chapter rather than being distributed. It is
 the largest gap in the field and the book currently has no home for it.
2. Whether F3 through F5 can be taught without bench measurement, given the
 decision to defer labs.
3. Which checks the desk kit can actually demonstrate, and which remain
 analytical for a reader without hardware.
