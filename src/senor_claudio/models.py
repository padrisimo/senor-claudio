import os
from pydantic import BaseModel


class ModelConfig(BaseModel):
    base_url: str
    api_key: str = "none"
    model: str


MODELS: dict[str, ModelConfig] = {
    "local": ModelConfig(
        base_url="http://localhost:11434/v1", api_key="ollama", model="qwen3:1.7b"
    ),
    "local-visual": ModelConfig(
        base_url="http://localhost:11434/v1", api_key="ollama", model="qwen2.5vl:3b"
    ),
    "gpt": ModelConfig(
        base_url="https://api.openai.com/v1",
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model="gpt-4o",
    ),
}

model_name = "local"