from contextlib import AsyncExitStack

import json
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from senor_claudio.tools import LOCAL_TOOLS, TOOL_SCHEMAS

MCP_CONFIG = Path(__file__).parent / "mcp.json"


mcp_sessions: dict[str, ClientSession] = {}


async def connect_mcp(stack: AsyncExitStack):
    """Launc each MCP server and merge its tools into TOOLS_SCHEMAS."""
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    for name, spec in config["mcpServers"].items():
        params = StdioServerParameters(command=spec["command"], args=spec["args"])
        try:
            read, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
        except Exception as e:
            print(f"[mcp] '{name}' failed to start: {e}")
            continue

        tools = (await session.list_tools()).tools
        for tool in tools:
            mcp_sessions[tool.name] = session
            TOOL_SCHEMAS.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    },
                }
            )
        print(f" [mcp] connected '{name}': {[t.name for t in tools]}")


async def call_tool(name: str, args: dict) -> str:
    """Run a tool - ours directly or an MCP server's over the protocol"""
    try:
        if name in LOCAL_TOOLS:
            return LOCAL_TOOLS[name](**args)
        if name in mcp_sessions:
            result = await mcp_sessions[name].call_tool(name, args)
            return "\n".join(c.text for c in result.content if hasattr(c, "text"))
    except Exception as e:
        return f"Error running tool '{name}': {e}"
