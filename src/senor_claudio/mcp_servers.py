from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from senor_claudio.tools import LOCAL_TOOLS, TOOL_SCHEMAS

MCP_SERVERS = {
    "time": StdioServerParameters(command="uvx", args=["mcp-server-time"]),
    "fetch": StdioServerParameters(command="uvx", args=["mcp-server-fetch"]),
}

mcp_sessions: dict[str, ClientSession] = {}


async def connect_mcp(stack: AsyncExitStack):
    """Launc each "MCP server and merge its tools into TOOLS_SCHEMAS."""
    for name, params in MCP_SERVERS.items():
        read, write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()

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
        session = mcp_sessions.get(name)
        if session is None:
            return f"Unknown tool: {name}"
        result = await session.call_tool(name, args)
        return "\n".join(c.text for c in result.content if hasattr(c, "text"))
    except Exception as e:
        return f"Error running tool '{name}': {e}"
