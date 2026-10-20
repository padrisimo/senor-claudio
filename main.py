import sys
from openai import OpenAI

sys.stdout.reconfigure(encoding="utf-8")

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen3:1.7b"


def chat(user_message):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful code assistant, follow YAGNI principles and provide concise answers.",
            },
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    print(
        f"Señor Claudio está en la casa! You are now connected to the {MODEL} model. - ctrl+c to exit."
    )
