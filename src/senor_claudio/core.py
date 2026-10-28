from senor_claudio.agent_loop import MODEL, run_agent
from senor_claudio.tools import load_memory

SYSTEM_PROMPT = """You are a helpful code assistant, follow YAGNI principles and provide concise answers.

Here is what you remember about the user from previous sessions:
{memory}

When you learn a new lasting fact about the user, save it with save_memory"""


async def core():

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(memory=load_memory())}
    ]

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

            Señor Claudio está en la casa! You are now connected to the {MODEL} model - ctrl+c to exit.
            """)
    try:
        while True:
            messages.append({"role": "user", "content": input("\nYou: ")})
            answer = await run_agent(messages)
            print(f"Señor Claudio:", answer)
    except (EOFError, KeyboardInterrupt):
        print("\nAdios amigo!")
