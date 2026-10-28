from senor_claudio.models import MODELS
from senor_claudio.tools import LOCAL_TOOLS, TOOL_SCHEMAS, load_memory


def handle_command(line: str) -> bool:
    """Returns True if the line was a command."""
    global model_name
    if not line.startswith("/"):
        return False
    cmd, _, arg = line.partition(" ")
    if cmd == "/models":
        for name, cfg in MODELS.items():
            marker = "*" if name == model_name else " "
            print(f" {marker} {name:<12} {cfg.model}  ({cfg.base_url})")
    elif cmd == "/model":
        if arg in MODELS:
            model_name = arg
            print(f"  switched to {arg} ({MODELS[arg].model})")
        else:
            print(f"  unknown model '{arg}' - try /models")
    elif cmd == "/tools":
        for schema in TOOL_SCHEMAS:
            fn = schema["function"]
            origin = "local" if fn["name"] in LOCAL_TOOLS else "mcp"
            print(f"  [{origin}] {fn['name']}: {fn['description'][:60]}")
    elif cmd == "/memory":
        print(load_memory())
    elif cmd == "/quit":
        raise SystemExit
    else:
        print("  commands: /models /model <name> /tools /memory /quit")
    return True
