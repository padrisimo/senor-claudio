# Release Notes

> Señor Claudio — like Claude Code, but with more salsa and a moustache.
> (The logo is just Claude with a big Mexican moustache. Don't tell Anthropic.)

All dates are in ISO format. Versions follow the project's git tags; `pyproject.toml`
currently declares `0.1.0`.

## [Unreleased]

### Added
- Slash commands in the interactive shell: `/models`, `/model <name>`, `/tools`,
  `/memory`, and `/quit`.
- Persistent long-term memory via `save_memory` and `load_memory`, surfaced through
  the `/memory` command and injected into the system prompt.
- MCP tool results are truncated to 4000 characters to keep context windows sane.
- Duplicate MCP tool schemas are ignored when (re)connecting servers.
- Test suite for MCP configuration loading and local tools (`pytest`).
- Dev dependency group (`pytest`) in `pyproject.toml`.

### Changed
- Agentic loop and MCP integration refactored into `agent_loop.py` and
  `mcp_servers.py`; `core.py` now wraps each request in error handling.
- Tool execution distinguishes local tools from MCP tools and reports their origin
  in `/tools`.
- Model switching is available at runtime with `/model`.

### Fixed
- MCP server startup failures are reported without aborting the whole session.
- Unknown tool calls return a clear `Unknown tool` message instead of crashing.
- Models that do not support tool-calling produce a friendly Spanish error
  message instead of a traceback.

## [v0.1] - 2026-10-27

### Added
- MCP server integration driven by `mcp_servers.json` (defaults: `time`, `fetch`).
- Async core loop with `AsyncExitStack`-managed MCP sessions.
- OpenAI-compatible model configuration (local Ollama, OpenAI GPT-4o).
- Workspace file tools: `list_files`, `read_file`, `write_file`.
- System prompt with YAGNI guidance and memory injection.

### Changed
- Reorganized the codebase under `src/senor_claudio/` with a `senor-claudio`
  console entry point.

## [v1] - 2026-10-22

### Added
- Agentic tool-calling loop: the assistant can invoke tools and feed results back
  until it produces a final answer.
- `write_file` tool for creating files in the workspace.
- Sample workspace files (`hello.txt`, `world.txt`, `combined.txt`).

## [v0] - 2026-10-20

### Added
- Initial Python agentic harness ("Señor Claudio está en la casa!").
- Interactive REPL with Ctrl+C / EOF exit.
- README describing the project as a Claude Code parody.

### Removed
- Images from the README.

---

Adios amigo! 🌮
