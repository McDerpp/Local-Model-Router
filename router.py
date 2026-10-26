import requests
from config import config


# Define MODEL constant that chat() needs
MODEL = "qwen3:4b"


def chat(prompt: str) -> str:
    """Send a prompt to a local Ollama model and return its response."""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
        "keep_alive": "5m",
    }

    response = requests.post(
        config["ollama"]["base_url"] + "/api/chat",
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    result = response.json()
    return result["message"]["content"]


def basic_router(prompt: str) -> str:
    """A basic router function that sends a prompt to the chat function."""

    return chat(prompt)



def get_model_list() -> list:
    """Fetch the list of available models from the Ollama API."""

    response = requests.get(f"{config["ollama"]["base_url"]}/api/tags", timeout=10)
    response.raise_for_status()
    
    # Parse JSON response and return model info
    data = response.json()
    for model in data["models"]:
        print(model["name"])
    return data

