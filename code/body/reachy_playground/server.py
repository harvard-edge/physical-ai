"""MCP server: exposes every skill in skills.py as a tool Claude can call.

Add a new @skill in skills.py and it automatically becomes a new MCP tool here,
no changes needed in this file. Run over stdio (how MCP clients launch it):

    python -m reachy_playground.server

See README.md for how to register this with Claude Desktop / Claude Code.
"""
from mcp.server.fastmcp import FastMCP

from . import skills

mcp = FastMCP("reachy-playground")

# Turn each skill function into an MCP tool. FastMCP reads the function's name,
# type hints, and docstring to build the tool schema Claude sees.
for _name, _fn in skills.SKILLS.items():
    mcp.tool()(_fn)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
