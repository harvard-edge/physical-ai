# memory schema

What Maya teaches the robot, stored as a **knowledge graph**: entities, the
relations between them, and observations attached to each. It lives in one local,
human-readable file (`graph.jsonl`), one JSON object per line. That file is the
whole point of choosing a graph over a vector store: you can open it and show
Maya exactly what the robot knows, and that she is the one who put it there.

This schema is a convention, not code. The off-the-shelf knowledge-graph MCP
server (`@modelcontextprotocol/server-memory`) stores whatever the brain writes;
keeping to these entity and relation types keeps the graph legible as it grows.

## Entities

| entityType | What it is | Example observations |
| --- | --- | --- |
| `robot` | the Reachy itself | `name: Pixel`, `birthday: 2026-06-27` |
| `person` | Maya, Alexander, family | `age: 5`, `favorite color: teal` |
| `concept` | a thing Maya teaches | `a kitten is a baby cat` |
| `trick` | a skill/behavior she made | `spin: turn body, wiggle, nod` |

## Relations

| relationType | Reads as |
| --- | --- |
| `named_by` | robot **named_by** Maya |
| `taught_by` | concept **taught_by** Maya |
| `friend_of` | Alexander **friend_of** Maya |
| `is_a` | kitten **is_a** cat |

## How "teach the name" maps in

1. Maya: "Your name is Pixel." → add/observe on the `robot` entity: `name: Pixel`;
   add relation `robot named_by Maya`.
2. Robot reacts with a body skill (`accept_name`), then remembers across days.
3. Next time, the brain reads the `robot` entity first and greets as Pixel.

See `graph.example.jsonl` for what a small taught graph looks like on disk.
