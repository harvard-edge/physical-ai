"""brain/orchestrator.py - the cloud brain loop (Phase 2 on-ramp, SKELETON).

This is NOT wired up yet. Milestone 1 talks to the robot through the local
reflex in web/server.py. This file is the shape of what replaces that reflex:
Claude, holding the conversation, with the body skills and the memory graph as
tools, deciding words + gestures + what to remember.

Two ways to run the brain, both using brain/system-prompt.md:
  1. Claude Desktop  - zero code; see claude_desktop_config.example.json.
  2. This script     - the Agent SDK, for the always-on loop later.

To make this real:
  pip install claude-agent-sdk        # into the project venv
  export ANTHROPIC_API_KEY=...
  then fill in the TODOs below and call `turn("Your name is Pixel.")`.
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent          # code/brain
CODE = HERE.parent                              # code
SYSTEM_PROMPT = (HERE / "system-prompt.md").read_text()
MEMORY_FILE = CODE / "memory" / "graph.jsonl"

# The two MCP servers the brain drives. Same two the Desktop config lists.
MCP_SERVERS = {
    "body": {
        "command": "python",
        "args": ["-m", "reachy_playground.server"],
        # PYTHONPATH must include code/body so the package imports.
        "env": {"PYTHONPATH": str(CODE / "body")},
    },
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "env": {"MEMORY_FILE_PATH": str(MEMORY_FILE)},
    },
}


async def turn(user_text: str) -> str:
    """Run one conversational turn. TODO: implement with the Agent SDK.

    Sketch:
        from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
        options = ClaudeAgentOptions(
            system_prompt=SYSTEM_PROMPT,
            mcp_servers=MCP_SERVERS,
            model="claude-sonnet-5",
        )
        async with ClaudeSDKClient(options) as client:
            await client.query(user_text)
            # Claude calls body + memory tools; collect its final reply.
            return await collect_reply(client)
    """
    raise NotImplementedError("brain loop not wired yet - Milestone 2")


if __name__ == "__main__":
    print("The brain is a skeleton. Milestone 1 runs through web/ + the reflex.")
    print(f"System prompt: {len(SYSTEM_PROMPT)} chars")
    print(f"Memory file:   {MEMORY_FILE}")
    print(f"MCP servers:   {', '.join(MCP_SERVERS)}")
