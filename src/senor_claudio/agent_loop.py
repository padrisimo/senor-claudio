import sys
from openai import AsyncOpenAI

from senor_claudio.models import MODELS, model_name

sys.stdout.reconfigure(encoding="utf-8")

import json

cfg = MODELS[model_name]
client = AsyncOpenAI(base_url=cfg.base_url, api_key=cfg.api_key)


from senor_claudio.tools import TOOL_SCHEMAS
from senor_claudio.mcp_servers import call_tool


async def run_agent(messages: list) -> str:
    while True:
        response = await client.chat.completions.create(
            model=cfg.model,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or ""

        messages.append(message)
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling tool: {tool_call.function.name} with arguments: {args}")
            result = await call_tool(tool_call.function.name, args)
            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )
