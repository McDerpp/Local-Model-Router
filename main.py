import requests



OLLAMA_API = "http://localhost:11434/api/chat"
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
        OLLAMA_API,
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

    response = requests.get(f"{OLLAMA_API}/models", timeout=10)
    response.raise_for_status()
    return response.json()





if __name__ == "__main__":
    try:
        answer = chat("Explain what a Python function is in simple terms.")
        print("\nModel response:\n")
        print(answer)

    except requests.exceptions.ConnectionError:
        print("Could not connect to Ollama. Make sure Ollama is running.")

    except requests.exceptions.Timeout:
        print("The request timed out. Check model performance and try again.")

    except requests.exceptions.HTTPError as error:
        print(f"Ollama returned an HTTP error: {error}")
        if error.response is not None:
            print(error.response.text)
