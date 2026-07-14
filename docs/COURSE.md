# Physical AI: A Hands-On Systems Course

A short course that teaches how physical AI systems are actually built, for
engineers, through one real artifact (a robot). Each chapter adds one component
to the loop, confronts one measurable tradeoff ("the margin"), names the
components you actually use, and ends with something you build and measure.

Reference robot: Reachy Mini (the integrated reference design). Kit target:
Arduino UNO Q / Ventuno Q, whose dual brain (Linux MPU for AI, STM32 MCU for
real time) makes the reflex versus deliberation split physical. The platform is
interchangeable; the structure is the point.

Chapter template: **Question** the chapter answers, the **Margin** (the systems
crux), **Components** (what you use), **Build** (the artifact), **Measure** (the
number that makes the tradeoff real), **Read** (literature anchors for engineers).

---

## Chapter 0. From TinyML to Physical AI: the loop

- **Question:** why is a robot not just a model with a motor attached?
- **Margin:** open loop versus closed loop. Once actions change future inputs,
  latency, stability, and safety appear.
- **Components:** one sensor plus one actuator; the UNO Q MCU for the loop.
- **Build:** a reflex (sense to act) running on the device, no cloud.
- **Measure:** end-to-end loop latency, and what happens to it when you add work.
- **Read:** sense-plan-act versus Brooks's subsumption architecture.

## Chapter 1. Sensing and perception on the edge

- **Question:** how do raw signals become something a model can use, on a small
  budget?
- **Margin:** accuracy versus latency versus energy; what quantization costs you.
- **Components:** camera, MEMS microphone, IMU; a small model on the MPU.
- **Build:** an on-device perception task (wake word or a simple detector).
- **Measure:** inferences per second, milliwatts, accuracy; the curve between them.
- **Read:** MLPerf Tiny; quantization and distillation. (The TinyML bridge.)

## Chapter 2. From pixels to meaning: VLMs and VLAs

- **Question:** what does the scene mean, and who should decide, the device or
  the cloud?
- **Margin:** capability versus latency, cost, and privacy; the grounding gap.
- **Components:** camera; a small on-device VLM (the MPU NPU) or a cloud VLM.
- **Build:** show-and-tell, the robot looks at an object and reacts.
- **Measure:** latency and cost, local versus cloud, for the same task.
- **Read:** RT-2, OpenVLA, pi-zero; SmolVLM and moondream for the tiny end.

## Chapter 3. Cognition and agency: the brain and the agent loop

- **Question:** how does the system decide what to do, and when to think hard?
- **Margin:** reflex versus deliberation; the cost of escalating to a big model.
- **Components:** the MPU running an agent (tools, MCP); a cloud LLM for hard turns.
- **Build:** the two-speed brain, MCU reflexes plus MPU or cloud deliberation.
- **Measure:** fraction of turns handled locally versus escalated; response time.
- **Read:** tool use and agents; MCP; the System 1 / System 2 framing.

## Chapter 4. Action and control

- **Question:** how do decisions become safe, smooth motion?
- **Margin:** control latency and smoothness versus compute; real time versus
  best effort; the safety envelope.
- **Components:** servos or smart actuators; the MCU real-time loop.
- **Build:** smooth trajectories with limits (Reachy goto_target / set_target).
- **Measure:** jitter, overshoot, and time to a safe stop.
- **Read:** PID and impedance control; trajectory interpolation (min-jerk).

## Chapter 5. Memory and state

- **Question:** what should the system remember, and how does it recall it?
- **Margin:** what to keep versus forget; structured versus fuzzy memory.
- **Components:** local storage; a knowledge graph.
- **Build:** teach-it-and-remember, the robot stores what the user teaches.
- **Measure:** recall accuracy over time; storage growth.
- **Read:** knowledge graphs; structured memory versus RAG; retrieval practice.

## Chapter 6. The data flywheel

- **Question:** how does the system get better from its own experience?
- **Margin:** data quality versus quantity; label cost; privacy of collected data.
- **Components:** storage and connectivity; an on-device curator.
- **Build:** an episode logger plus an interestingness curator; human in the
  loop (the child's reactions are the labels).
- **Measure:** data yield, fraction kept, and downstream improvement.
- **Read:** active learning; DAgger and imitation learning; data-centric AI; RLHF.

## Chapter 7. Placement and systems

- **Question:** where should each capability run, and how do you prove the choice?
- **Margin:** the placement decision itself, against latency, energy, and privacy
  budgets.
- **Components:** the full dual brain plus the cloud.
- **Build:** place each capability deliberately and instrument it.
- **Measure:** latency, energy, and privacy per placement; a small benchmark
  harness.
- **Read:** MLPerf; edge-cloud offloading; energy profiling.

## Chapter 8. Safety, privacy, and deployment

- **Question:** what does it take to put this in a home, responsibly?
- **Margin:** always-on sensing risk; reliability; failure modes (this one is
  sharp because the home is a child's room).
- **Components:** indicators, capture gating, a physical on and off, a watchdog.
- **Build:** privacy-gated capture, auto-restart, a visible mute.
- **Measure:** failure recovery time; a data-egress audit (what actually leaves
  the device).
- **Read:** safety engineering; privacy by design; federated and local-first.

---

## Capstone

The full loop running on the reference robot, and a buildable, decomposed
version on the kit hardware, so a learner reconstructs the loop piece by piece
and can point at where every chapter lives in their own build.
