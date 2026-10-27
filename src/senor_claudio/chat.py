import sys
from openai import AsyncOpenAI

sys.stdout.reconfigure(encoding="utf-8")

import json

client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3:1.7b"


from senor_claudio.tools import TOOL_SCHEMAS, TOOLS


async def chat(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful code assistant, follow YAGNI principles and provide concise answers.",
        },
        {"role": "user", "content": user_message},
    ]
    while True:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or ""

        messages.append(message)
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments or {})
            print(f"Calling tool: {tool_call.function.name} with arguments: {args}")
            result = TOOLS[tool_call.function.name](**args)
            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )
