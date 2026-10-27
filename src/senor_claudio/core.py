from contextlib import AsyncExitStack

from senor_claudio.agent_loop import MODEL, run_agent
from senor_claudio.mcp_servers import connect_mcp
from senor_claudio.tools import TOOL_SCHEMAS


async def core():
    async with AsyncExitStack() as stack:
        await connect_mcp(stack)
        print(f"""

                      ███████████████████████████████████      
                      ███████████████████████████████████      
                      ███████████████████████████████████      
                      ███████████████████████████████████      
                      ██████  ███████████████████  ██████      
                      ██████  ██      ███      ██  ██████      
                ██████████████                   ██████████████
                ████████                               ████████
                ████████                               ████████
                ███████████          █████          ███████████
                      ███████████████████████████████████      
                      ███████████████████████████████████      
                      ███████████████████████████████████      
                        ████  ████           ████  ████        
                        ████  ████           ████  ████        
                        ████  ████           ████  ████      


                                   ███████╗
                                   ╚══════╝
                ███████╗ ███████╗ ███╗   ██╗  ██████╗  ██████╗
                ██╔════╝ ██╔════╝ ████╗  ██║ ██╔═══██╗ ██╔══██╗
                ███████╗ █████╗   ██╔██╗ ██║ ██║   ██║ ██████╔╝
                ╚════██║ ██╔══╝   ██║╚██╗██║ ██║   ██║ ██╔══██╗
                ███████║ ███████╗ ██║ ╚████║ ╚██████╔╝ ██║  ██║
                ╚══════╝ ╚══════╝ ╚═╝  ╚═══╝  ╚═════╝  ╚═╝  ╚═╝

                 ██████╗ ██╗       █████╗  ██╗   ██╗ ██████╗  ██╗  ██████╗
                ██╔════╝ ██║      ██╔══██╗ ██║   ██║ ██╔══██╗ ██║ ██╔═══██╗
                ██║      ██║      ███████║ ██║   ██║ ██║  ██║ ██║ ██║   ██║
                ██║      ██║      ██╔══██║ ██║   ██║ ██║  ██║ ██║ ██║   ██║
                ╚██████╗ ███████╗ ██║  ██║ ╚██████╔╝ ██████╔╝ ██║ ╚██████╔╝
                 ╚═════╝ ╚══════╝ ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═════╝

            Señor Claudio está en la casa! You are now connected to the {MODEL} model 
            with {len(TOOL_SCHEMAS)} tools - ctrl+c to exit.
            """)
        try:
            while True:
                question = input("\nYou: ")
                answer = await run_agent(question)
                print(f"Señor Claudio: {answer}")
        except (EOFError, KeyboardInterrupt):
            print("\nAdios amigo!")