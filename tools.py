from pathlib import Path

WORKSPACE = Path(__file__).parent / "workspace"


# Tools


def list_files() -> str:
    """List all files in the workspace."""
    return "\n".join([f.name for f in WORKSPACE.iterdir()]) or "No files found."


def read_file(filename: str) -> str:
    """Read the contents of a file in the workspace folder."""
    file_path = WORKSPACE / filename
    if not file_path.is_file():
        return f"File '{filename}' does not exist."
    return file_path.read_text(encoding="utf-8")


TOOLS = {"list_files": list_files, "read_file": read_file}

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
]
