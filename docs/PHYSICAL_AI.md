# Physical AI: a systems way to think about it

## Why this document exists

This project has two purposes at once. One is a robot for Maya. The other is to
use that real use case as a forcing function for thinking rigorously about how
physical AI systems are actually built. The structure below is written so the
architecture doubles as a learning progression: the components are the pieces
you learn about, in order, by building one real thing.

Most public talk about physical AI stops at one sentence: "I deployed a model on
a device and it does something." That is the least interesting part. This
document is about the rest.

## The thesis: from TinyML to Physical AI

TinyML put intelligence ON a device. You sense, you infer, you maybe act once.
It is essentially an open loop running a static model on a constrained box.

Physical AI puts a device IN A LOOP with the world. It senses, decides, acts,
the action changes the world, and then it senses the changed world and goes
again. Three leaps come with that:

1. **Pipeline becomes loop.** Actions change future inputs. The system has
   agency, not just inference. Stability, latency, and safety now matter in ways
   they never did for a one-shot classifier.
2. **Static becomes self-improving.** The loop generates data, and that data
   improves the system. A physical AI system makes its own training set by
   acting in the world.
3. **One box becomes a system of placements.** Capability spreads across
   timescales (reflex, deliberation, learning) and across compute tiers (device,
   local server, cloud), each under a latency, energy, and privacy budget.

The single skill this subject teaches is **placement**: for every capability,
decide which loop (how fast) and which box (where it runs) it belongs in, and be
able to measure the consequence of that choice. TinyML taught "fit a model on a
microcontroller." Physical AI teaches "place each capability in the right loop
and the right box, and prove it with numbers."

## The mental model: nested loops at different timescales

```
 REFLEX loop      ~10-100 ms   sense -> act                  on device
 DELIBERATION     ~1-5 s       perceive -> reason -> act      cloud or local server
 LEARNING loop    hours-days   collect -> curate -> train -> deploy
```

Each slower loop rewrites the policy that the faster loop runs. Reflexes keep
the body responsive and alive. Deliberation handles meaning and intent. Learning
slowly makes both better.

## The components (the pieces you will learn about)

| Component | Job | On Reachy | The hard part / what you measure |
| --- | --- | --- | --- |
| Perception | signals to representations | camera, mic, IMU, joint state | accuracy vs latency vs energy |
| World / self state | fuse over time into a belief | "Maya is here, holding a drawing" | grounding, drift, working memory |
| Cognition / policy | decide what to do | Claude (slow), reflexes (fast) | where the slow/fast line falls |
| Action / control | decision to safe motion | goto_target / set_target | control latency, safety envelope |
| Memory | episodic, semantic, skills | logs + knowledge graph | what to keep, what to forget |
| Learning + data | improve from experience | the flywheel (off device) | data quality, label cost |
| Systems (cross-cutting) | budgets and placement | CM4 plus cloud | latency, energy, privacy, reliability |

## What vision-language models teach

VLMs map pixels and text to text. The frontier extends them to actions:
Vision-Language-Action models output motor commands as just more tokens (RT-2,
OpenVLA, Octo, pi-zero, Gemini Robotics; Hugging Face LeRobot is the open hub).
Five lessons:

1. **Pretraining transfers.** Robot data is scarce; internet-scale priors give
   generalization that robot logs alone cannot. Big pretrained model plus a
   little robot data beats a hand-built pipeline. (The bitter lesson, embodied.)
2. **Tokenize everything.** Pixels, words, and actions become one token stream.
3. **The grounding gap sets the hierarchy.** VLMs are strong on semantics, weak
   on precise control and real-time latency, which forces the slow-brain plus
   fast-controller split. The architecture is not a hack; the models demand it.
4. **Size dictates placement.** A useful VLM does not run a control loop on a
   small device. You distill it or you split it.
5. **Data is the constraint, not models.**

## The data flywheel (where it becomes AI, not automation)

In physical AI the bottleneck is data, not models. So building the system is
largely building the flywheel: collect on the edge (cheap), curate on the edge
(privacy), train in the cloud or on a local server (expensive), distill back to
the device (cheap inference), repeat.

A tiny on-device agent is the data front-end. It logs multimodal episodes
(frame, audio, words, action, outcome) and learns what is worth keeping: the
surprising, novel, or uncertain moments rather than everything. That is active,
curiosity-driven collection.

The insight that ties the use case to the engineering: **the engagement loop and
the learning loop are the same loop.** When Maya teaches the robot, she is
generating curated, human-labeled training data. The thing that keeps the child
engaged is the thing that improves the system.

## The learning progression (a candidate module spine)

Each module adds one component to the loop, confronts one systems tradeoff, and
is built and measured on the robot. This is a candidate table of contents for a
kit or a book, with one real artifact carrying the whole thing.

| Module | Concept | The leap or tradeoff | Build on Reachy | Kit hardware |
| --- | --- | --- | --- | --- |
| 0 Body and loop | open vs closed loop, latency | why a loop, not a pipeline | motion + a reflex | actuator + 1 sensor |
| 1 Perception on the edge | signals to representations | accuracy vs latency vs energy | small model on device | camera, mic, IMU |
| 2 Pixels to meaning | VLMs, grounding gap | capability vs latency, cost, privacy | camera show and tell | (uses 1) |
| 3 Cognition and agency | planning, tool use, agent loop | reflex vs deliberation | the two-speed brain | compute + link |
| 4 Action and control | decisions to safe motion | control latency, safety | smooth gestures, limits | actuators |
| 5 Memory | episodic, semantic, skill | what to keep and forget | teach it and remember | storage |
| 6 The data flywheel | collect, curate, train, distill | data quality, label cost | episode logger + curator | storage + link |
| 7 Systems and deployment | budgets, placement, benchmarking | latency, energy, privacy | measure and place | the whole kit |

## Maya's Reachy as the reference design

This repository is the high-end reference: a capable robot where the full loop
already runs. A buildable kit would decompose the same loop into affordable parts
so each module exposes exactly one piece, and the learner rebuilds the loop step
by step. The reference design proves the target; the kit makes the path.
