# Memory

The first working memory is implemented in
`body/reachy_playground/memory.py`. It stores an explicitly taught robot name in
a small local JSON file and replaces that file atomically.

The default path is `~/.local/share/mayas-reachy/memory.json`. Set
`MAYAS_REACHY_MEMORY_FILE` to use another path.

The LLM extracts a candidate fact, but application code controls persistence.
Only a `teach_robot_name` result with a valid short name can write to disk.
Conversation history remains in RAM. The knowledge-graph design in this folder
is the planned extension for additional facts.
