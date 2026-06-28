# Architecture

## System overview

```
 Maya / family ──speak / teach──►  CLAUDE  (brain: reasoning, vision, conversation)
                                      │ tools via MCP
                  ┌───────────────────┼─────────────────────┐
             skills server       memory server         senses / others
             (our code,          (knowledge graph =     (camera -> vision,
              reachy SDK)          what she taught it)    voice / face id)
                  │
            reachy_mini SDK ──►  ROBOT BODY (CM4: motors, speaker, mic, camera)
                                  hosts the tiny reflex loop locally
```

## The two-speed brain

The robot runs two loops at different speeds, split by cost.

- **Reflexes (on the robot, instant, always on, offline capable):** wake word,
  voice activity detection, "look alive" idle motion, local text to speech,
  canned reactions, turning toward a speaker.
- **Deliberation (cloud, occasional, only when it matters):** real
  conversation, understanding a drawing from the camera, deciding what to teach
  or recall, planning a multi step bit.

The reflex layer keeps the robot responsive and alive even with no network. It
escalates to Claude only when something genuinely needs thought. On this
hardware, that boundary is the design, not a workaround.

## Hardware reality (measured 2026-06-27)

| Property | Value |
| --- | --- |
| Board | Raspberry Pi Compute Module 4 (CM4) Rev 1.1 |
| CPU | Cortex-A72 x4 @ 1.5 GHz (aarch64) |
| RAM | 3.7 GB total (about 2.8 GB free) |
| Storage | 14 GB eMMC (about 6 GB free) |
| Accelerator | none (no Hailo, no Coral, no PCIe NPU) |
| Thermals | about 45 C, no throttling |
| OS | Debian 13 (trixie), kernel 6.12 |
| Runtime | reachy daemon in `/venvs/mini_daemon`, uses about one core |

Implication: the CM4 can host reflexes, ears, and mouth comfortably. It cannot
run a conversational model at usable speed (a 1B model would manage only a few
tokens per second, a 3B model is impractical). So the conversational brain is
Claude in the cloud. If fully local thinking is wanted later, the realistic
path is a small always-on box on the same network, not the CM4 itself.

## Component responsibilities

| Component | Job | Runs where | Built on | First phase |
| --- | --- | --- | --- | --- |
| `body/` | drive motors, speaker, mic, camera; expose skills | robot or dev Mac | `reachy_mini` SDK | 0 (done) |
| `brain/` | orchestrate: perceive, decide, call skills, converse | cloud client | Claude + MCP | 1 to 2 |
| `memory/` | store and recall what Maya teaches | local file | knowledge graph MCP server | 1 |
| `voice/` | turn text into speech | robot (Piper), Mac (say) for dev | Piper / macOS say | 2 |
| `senses/` | wake word, camera vision, speaker and face id | robot + cloud vision | openWakeWord, Claude vision | 2 to 3 |

## Connection facts

- Robot daemon reachable on the LAN at `10.174.1.60:8000`.
- From a dev machine: `ReachyMini(host="10.174.1.60", connection_mode="network")`.
- Audio to the robot speaker: warm up the WebRTC audio send chain for about
  three seconds after `start_playing()`, then stream samples in real time
  chunks. A single bulk push races the pipeline and plays silent.
- The robot mic over WebRTC is unreliable from a remote machine, which is one
  more reason the listening loop belongs on the robot itself.

## Data flow: "teach it" (Phase 1)

1. Maya tells Claude a fact ("a baby cat is a kitten").
2. Claude writes it to the knowledge graph (entity, relation, observation).
3. Claude calls a body skill to react (a happy nod).
4. Later, Claude reads the graph and quizzes her, spaced over time.

## Data flow: "talk to it" (Phase 2)

1. On-robot wake word or push to talk starts a turn.
2. Local capture plus speech to text produces text (and a recent camera frame).
3. Claude reasons, then returns speech to say and skills to run.
4. Local voice speaks, body moves, robot returns to the idle reflex loop.

## Proposed layout

```
mayas-reachy/
  README.md
  docs/            ARCHITECTURE.md, ROADMAP.md, DECISIONS.md
  body/            robot driver + skills (reachy_mini SDK)
  brain/           agent / orchestrator + MCP wiring (Claude)
  memory/          knowledge graph config and helpers
  voice/           TTS (Piper on robot, say on Mac) + cached clips
  senses/          wake word, vision, identity (later phases)
```

Code arrives phase by phase. The existing happy-birthday app and skills
playground are the Phase 0 building blocks that will move under `body/` and
`brain/`.
