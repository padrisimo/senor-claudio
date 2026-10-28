import json
from pathlib import Path

import senor_claudio.mcp_servers as mcp


def test_load_config_has_servers():
    cfg = mcp._load_config()
    assert isinstance(cfg, dict)
    assert "time" in cfg
    assert "fetch" in cfg
    assert cfg["time"]["command"] == "uvx"


def test_mcp_config_file_valid():
    path = Path(mcp.MCP_CONFIG)
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    assert set(data["mcpServers"]) == {"time", "fetch"}


def test_call_tool_unknown():
    import asyncio

    result = asyncio.run(mcp.call_tool("nope_tool", {}))
    assert "Unknown tool" in result
