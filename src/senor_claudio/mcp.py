import asyncio
from contextlib import AsyncExitStack
from tkinter.tix import Form

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MCP_SERVERS = {
    "time": StdioServerParameters(command="uvx", args="mcp_server_time"),
    "fetch": StdioServerParameters(command="uvx", args="mcp_server_fetch"),
}

mcp_sessions: dict[str, ClientSession]


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
