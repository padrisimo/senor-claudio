import asyncio
from contextlib import AsyncExitStack

from senor_claudio.agent_loop import run_agent
from senor_claudio.commands import handle_command
from senor_claudio import models
from senor_claudio.prompts import CASA_LOG, SYSTEM_PROMPT
from senor_claudio.mcp_servers import connect_mcp
from senor_claudio.tools import load_memory

messages = [{"role": "system", "content": SYSTEM_PROMPT.format(memory=load_memory())}]


async def core():
    async with AsyncExitStack() as stack:
        await connect_mcp(stack)
        print(CASA_LOG.format(MODEL=models.MODELS[models.model_name].model))
        try:
            while True:
                line = (await asyncio.to_thread(input, "you: ")).strip()
                if not line or handle_command(line):
                    continue
                answer = await run_agent(messages, line)
                print(f"Señor Claudio:", answer)
        except (EOFError, KeyboardInterrupt, SystemExit):
            print("\nAdios amigo!")
