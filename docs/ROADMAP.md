# Roadmap

Long vision, short deliveries. Each phase ships something Maya can touch, and
each one de-risks the next. We do not move to a later phase before the earlier
one works on the real robot.

## Phases

| Phase | What we add | What Maya gets | What it teaches her | Lift |
| --- | --- | --- | --- | --- |
| 0 Foundation (done) | body, voice, motion, MCP skills | it talks, moves, knows her name | nothing yet, it is the base | done |
| 1 Teach it and memory | knowledge graph memory, teach / recall / quiz | it remembers what she teaches | it only knows what you taught it; recall | low, mostly wiring |
| 2 Always on presence | on-robot reflex loop, local voice, wake or push to talk, hand off to Claude | it lives on her shelf and greets her daily | edge versus cloud, the alive loop | medium, the real build |
| 3 Senses | camera show and tell (vision), voice and face id | it sees her drawings, knows it is her | sensors and perception | medium |
| 4 Authorship ladder | trick recorder, then blocks, then editing code, then seeing the brain | she programs it at her level | sequencing, then code, then how AI works | incremental, over years |

## Why this order

- Phase 1 turns a performer into a companion (memory is what makes it a
  someone), and it is cheap because the knowledge graph is an off the shelf MCP
  server. Highest engagement payoff for the least work.
- Phase 2 is the real engineering: moving the loop onto the robot so it is
  always on and offline capable. Everything social depends on it being present.
- Phase 3 adds the senses that make it feel aware.
- Phase 4 is not a sprint, it grows with Maya for years.

## The multi-year arc (the part that compounds)

The same robot can carry correct intuitions about AI from age 6 to 12.

| Age | What she does | The concept she absorbs |
| --- | --- | --- |
| 6 | teaches it words, corrects its mistakes | it only knows what it is taught; it can be wrong; it senses through a camera and a mic |
| 7 to 8 | records and names tricks (sequences) | programs are sequences; naming; reuse |
| 9 to 10 | edits numbers, then writes a skill | code; parameters; cause of behavior |
| 11 to 12 | sees her facts file versus the model's training | memorized data versus a trained model; inference versus training |

## The technical frontier (optional, later)

- A small always-on box on the same network running a local model, so the
  robot can think without the cloud.
- Learning from demonstration (the LeRobot world), where moving the robot by
  hand teaches it motions, not just facts.

These are real destinations, not commitments. We earn them by finishing the
earlier phases first.
