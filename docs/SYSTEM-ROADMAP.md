# Maya's Reachy System Roadmap

## Product Direction

Maya's Reachy is the complete character and reference system. The children
experience a robot that can listen, learn, remember, speak, and act. The book
explains how those capabilities arise from cooperating subsystems. UNO Q labs
then reconstruct the same ideas in small, observable exercises.

The product will evolve along two tracks. The child-facing experience can change
quickly through play sessions with Maya and Alexander. The cognitive and physical
runtime must evolve through stable interfaces, migrations, tests, and safety
reviews. Neither track should force the other to wait.

## Target Architecture

```text
Child-facing clients
website · future tablet UI · lab tools
             │ stable HTTP and event contracts
             ▼
Interaction gateway
sessions · progress · cancellation · accessibility
             │
             ▼
Cognitive runtime
perception → retrieval → interpretation → planning → reflection
     │             │             │              │
     ▼             ▼             ▼              ▼
media adapters   memory       policies     capabilities
Whisper/local    SQLite       Groq/local   Reachy SDK
camera later     FTS/vec      VLA later    Arduino RPC
     │             │             │              │
     └──────────── typed cognitive events ──────┘
                           │
                           ▼
                    safety supervisor
               limits · authorization · timeout
                           │
                           ▼
                       robot body
```

The robot remains useful when cloud services are unavailable. Local code owns
identity, memory policy, cancellation, basic speech, capability limits, and safe
recovery. Cloud or edge models supply expensive perception and reasoning through
replaceable provider interfaces.

## Stable Frontend Contract

The website should depend on a small interaction API rather than internal model
or database details. This keeps visual experiments safe and inexpensive.

| **Operation** | **Contract** | **User expectation** |
| --- | --- | --- |
| Read status | `GET /api/status` | Current activity appears within 500 ms |
| Send text | `POST /api/chat` | Message is accepted once and produces one turn |
| Start speech | `POST /api/listen/start` | Listening state appears immediately |
| Stop speech | `POST /api/listen/stop` | Recording indicator stops immediately |
| Read result | `GET /api/listen/result/{id}` | Progress and final result are pollable |
| Read memory | `GET /api/memory` | Adult or lab tools can inspect learned facts |
| Reset memory | `POST /api/memory/reset` | Destructive actions require confirmation |

The next interface revision should replace polling with a server-sent event or
WebSocket stream. The session API will remain valid, so that change will not
alter the cognitive runtime.

## Core System Contracts

Five contracts keep frameworks replaceable.

1. `PerceptionProvider` converts media into timestamped observations.
2. `MemoryRepository` records episodes and retrieves relevant evidence.
3. `ReasoningPolicy` converts observations and evidence into a bounded plan.
4. `ActionPolicy` proposes capabilities rather than raw motor coordinates.
5. `CapabilityExecutor` validates and performs approved physical behavior.

Pydantic models should define inputs and outputs at each boundary. Provider code
may depend on Groq, Piper, LeRobot, or NVIDIA software. Domain code should depend
only on these contracts.

## Memory Model

SQLite remains the authoritative embedded store. It contains three related forms
of memory.

| **Memory** | **Stored material** | **Primary use** |
| --- | --- | --- |
| Episodic | Interactions, observations, time, speaker, source | Evidence and recall |
| Semantic | Entities, aliases, temporal claims, confidence, origin | Knowledge and relationships |
| Procedural | Registered skills, requirements, implementation, safety class | Available behavior |

Embeddings are a derived search index. They never replace episodes, claims, or
evidence. The index may be deleted and rebuilt when the embedding model changes.
Initial retrieval combines entity matching, graph neighbors, and FTS5. A later
`sqlite-vec` adapter will add semantic similarity and reranking.

Knowledge consolidation will run as a bounded background task. It will resolve
aliases, reinforce repeated claims, identify contradictions, and propose inferred
concepts. Explicit statements, observations, inferences, and imported knowledge
remain distinguishable. Inferred knowledge cannot silently overwrite an asserted
fact.

## Framework Adoption Plan

The project follows an adoption ladder. Reuse a framework directly when it fits
the target device. Wrap it when its API should not become a domain dependency.
Borrow a proven pattern when its runtime is too heavy. Build only the small gap
that remains.

| **Area** | **Current choice** | **Planned integration** |
| --- | --- | --- |
| Robot body | Reachy Mini SDK | Capability adapter remains authoritative |
| UNO Q | Arduino Bridge/RPC | Linux cognition with MCU execution labs |
| API | FastAPI and Pydantic | WebSocket or server-sent progress events |
| Memory | SQLite and FTS5 | Optional `sqlite-vec` derived index |
| Speech recognition | Groq Whisper | Local provider for privacy and offline use |
| Speech output | Piper | Multiple local voices and prosody controls |
| Robot data | Typed events | LeRobot-compatible episode export |
| Workflow | Explicit state machine | LangGraph only for branching resumable plans |
| Distributed robotics | Native process | ROS 2 or Zenoh adapters when distribution is needed |
| Learned action | Capability rules | Remote OpenVLA or GR00T policy provider |
| Simulation | Reachy simulation | Isaac Sim evaluation when learned policies begin |

NVIDIA GR00T and OpenVLA belong on a GPU policy server. Reachy sends observations
and receives an action proposal. The local safety supervisor still decides
whether and how that proposal may execute.

## Delivery Phases

### Phase 1. Interaction Reliability

The first phase makes every child-facing operation cancellable, observable, and
idempotent.

- Complete asynchronous listening sessions.
- Add progress events for listening, transcription, reasoning, synthesis, and action.
- Add request identifiers and duplicate-submission protection.
- Measure start, stop, transcription, first-response, and completion latency.
- Preserve a usable local response when the network fails.

The phase is complete when Stop changes the interface within 100 ms, robot
recording ends within 250 ms, and every accepted turn reaches a visible terminal
state.

### Phase 2. Memory Inspection and Correction

This phase makes learning visible and reversible.

- Add an adult-facing memory inspector.
- Show episodes, entities, relationships, confidence, and supporting evidence.
- Support forgetting one claim, merging aliases, and correcting an entity.
- Add soft reset, backed-up hard reset, and backup restoration.
- Add schema migrations and database integrity checks.

The phase is complete when every displayed belief can be traced to evidence and
corrected without manually editing the database.

### Phase 3. Hybrid Retrieval

This phase improves recall without making vector similarity authoritative.

- Add query entity resolution and graph-neighbor expansion.
- Rank exact claims, temporal relevance, FTS5 matches, and evidence quality.
- Add a replaceable embedding provider.
- Add `sqlite-vec` only after confirming an ARM wheel on both target systems.
- Build a small evaluation set from real family interactions.

The phase is complete when retrieval tests measure which evidence was expected,
which evidence was returned, and whether the final answer stayed grounded.

### Phase 4. Knowledge Consolidation

This phase lets the semantic graph develop carefully over time.

- Detect aliases and possible duplicate entities.
- Track supporting and contradicting evidence.
- Distinguish asserted, observed, inferred, and imported claims.
- Propose higher-level concepts during idle periods.
- Ask for confirmation before promoting uncertain personal knowledge.
- Add retention policies for raw episodes and derived knowledge.

The phase is complete when the robot can explain why it believes something,
recognize a contradiction, and revise a belief without destroying its history.

### Phase 5. Multimodal Perception

This phase adds vision through the same observation contract used for speech.

- Add camera-frame sampling with explicit activation and privacy indicators.
- Introduce object, person, and scene observation providers.
- Associate spoken references with visible entities.
- Store derived observations and metadata rather than continuous raw video.
- Add bounded behaviors such as looking toward a named object.

The phase is complete when the robot can connect a spoken concept to a visible
object while preserving source, time, and confidence.

### Phase 6. LeRobot Data and Learned Skills

This phase records physical experience in an ecosystem-compatible format.

- Export selected episodes as LeRobot observations, states, actions, and outcomes.
- Record requested and executed actions separately.
- Record adult interventions and recovery behavior.
- Visualize and review datasets before training.
- Begin with small bounded expressive policies rather than open-ended control.

The phase is complete when an interaction can be replayed, reviewed, and used by
standard LeRobot training tools without a custom conversion project.

### Phase 7. VLA Policy Integration

This phase introduces learned action proposals without surrendering local safety.

- Implement the remote `ActionPolicy` client.
- Evaluate OpenVLA, SmolVLA, and NVIDIA GR00T against the available embodiment.
- Run inference on suitable GPU hardware.
- Validate proposals in simulation and open-loop replay before physical execution.
- Map policy output into approved capabilities and bounded parameters.
- Add confidence thresholds, timeouts, intervention, and emergency stop behavior.

The phase is complete when a learned policy can fail without bypassing the local
safety supervisor or leaving the robot in an unknown state.

### Phase 8. UNO Q Lab Realization

Each lab reconstructs one system boundary rather than copying the full Reachy
application.

1. Capture a sensor observation on the MCU.
2. Send a typed event to the Linux MPU through Arduino Bridge.
3. Persist an episode in SQLite.
4. Extract and validate a semantic relationship.
5. Retrieve evidence for a question.
6. Select and authorize a physical capability.
7. Record an action and its outcome.
8. Correct or forget learned knowledge.
9. Add an embedding index and compare retrieval methods.
10. Connect a remote learned policy while retaining MCU safety.

The labs should expose intermediate representations. Students should be able to
inspect an observation, an entity, a claim, retrieved evidence, a proposed
action, and the final actuator command.

## Verification Strategy

Testing follows the same boundaries as the architecture.

- Unit tests validate schemas, entity resolution, claim policy, retrieval, and safety limits.
- Contract tests run every provider against shared behavioral expectations.
- Integration tests exercise complete text and speech turns with fake hardware.
- Hardware tests measure microphone cancellation, audio playback, and neutral recovery.
- Retrieval evaluations use expected evidence rather than judging only fluent answers.
- Policy evaluations begin with recorded open-loop data, then simulation, then supervised hardware.
- Migration tests upgrade copies of real databases and verify backups before deployment.

Every deployment should expose build version, schema version, provider health,
queue depth, current state, and recent error without exposing credentials or
private conversation content.

## Immediate Build Order

The next implementation sequence keeps the robot usable after every step.

1. Finish responsive audio-session progress and browser verification.
2. Add the memory inspector and claim-level correction.
3. Persist typed events and introduce structured operational metrics.
4. Extract provider and repository interfaces into focused modules.
5. Add graph-neighbor retrieval and an evidence-based evaluation set.
6. Export a first LeRobot-compatible observational episode.
7. Add camera observations behind an explicit privacy control.
8. Prototype a remote policy adapter without allowing physical execution.

This order keeps front-end iteration playful while the backend accumulates
stable contracts, evidence, evaluation data, and safety guarantees.
