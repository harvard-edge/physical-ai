# brain

The thinking layer: Claude, which holds the conversation, looks at camera
frames when needed, decides what to say, and chooses which body skills and
memory operations to run. Connected to everything else through MCP.

- Cloud reasoning, called from a client (Claude Desktop or the Agent SDK).
- Phases 1 to 2. Starts as the orchestrator of skills plus memory, then grows
  to drive the always-on loop.
