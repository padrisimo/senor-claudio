from pathlib import Path

from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from senor_claudio.tools import LOCAL_TOOLS, TOOL_SCHEMAS

ROOT = Path(__file__).resolve().parents[2]
MCP_CONFIG = ROOT / "mcp_servers.json"

MAX_TOOL_RESULT_CHARS = 4000

DEFAULT_MCP_SERVERS = {
    "time": {"command": "uvx", "args": ["mcp-server-time"]},
    "fetch": {"command": "uvx", "args": ["mcp-server-fetch"]},
}

mcp_sessions: dict[str, ClientSession] = {}


def _load_config() -> dict:
    if MCP_CONFIG.is_file():
        import json

        try:
            return json.loads(MCP_CONFIG.read_text(encoding="utf-8")).get("mcpServers", {})
        except Exception as e:
            print(f"  [mcp] bad config ({e}); using defaults")
            return DEFAULT_MCP_SERVERS
    return DEFAULT_MCP_SERVERS


async def connect_mcp(stack: AsyncExitStack):
    """Launch every server in mcp_servers.json and merge in its tools."""
    for name, spec in _load_config().items():
        params = StdioServerParameters(
            command=spec["command"], args=spec.get("args", [])
        )
        try:
            read, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
        except Exception as e:
            print(f"  [mcp] '{name}' failed to start: {e}")
            continue

        tools = (await session.list_tools()).tools
        for tool in tools:
            # Guard against duplicate schemas if connect_mcp runs more than once.
            if tool.name not in mcp_sessions:
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
            mcp_sessions[tool.name] = session  # keep session up to date on reconnect
        print(f"  [mcp] connected '{name}': {[t.name for t in tools]}")


async def call_tool(name: str, args: dict) -> str:
    """Run a tool - ours directly or an MCP server's over the protocol"""
    try:
        if name in LOCAL_TOOLS:
            result = LOCAL_TOOLS[name](**args)
        else:
            session = mcp_sessions.get(name)
            if session is None:
                return f"Unknown tool: {name}"
            raw = await session.call_tool(name, args)
            result = "\n".join(c.text for c in raw.content if hasattr(c, "text"))
    except Exception as e:
        return f"Error running tool '{name}': {e}"

    if isinstance(result, str) and len(result) > MAX_TOOL_RESULT_CHARS:
        result = result[:MAX_TOOL_RESULT_CHARS] + "\n... (truncated)"
    return result
