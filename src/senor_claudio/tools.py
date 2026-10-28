from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2] / "workspace"
MEMORY_FILE = Path(__file__).parent / "memory.md"


# Local Tools


def load_memory() -> str:
    if MEMORY_FILE.is_file():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return "(nothing saved yet)"


def save_memory(fact: str) -> str:
    """Append one fact about the user long-term memory."""
    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(f" - {fact}\n")
    return f"saved: {fact}"


def list_files(**kwargs) -> str:
    """List all files in the workspace."""
    return "\n".join([f.name for f in WORKSPACE.iterdir()]) or "No files found."


def read_file(filename: str) -> str:
    """Read the contents of a file in the workspace folder."""
    file_path = WORKSPACE / filename
    if not file_path.is_file():
        return f"File '{filename}' does not exist."
    return file_path.read_text(encoding="utf-8")


def write_file(filename: str, content: str) -> str:
    """Write content to a file in the workspace folder."""
    file_path = WORKSPACE / filename
    file_path.write_text(content, encoding="utf-8")
    return f"File '{filename}' written successfully."


LOCAL_TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "load_memory": load_memory,
    "save_memory": save_memory,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in the user's workspace folder.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file in the workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read.",
                    }
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file in the workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to write.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file.",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": (
                "Save one short fact about the user long-term memory."
                "Use whenever you learn something worth: remembering, their name, preferences, projects, recurring tasks"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "fact": {"type": "string"}
                },
                "required": ["fact"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "load_memory",
            "description": "Read Memory file to remember about previous sessions",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]
