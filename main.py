from pathlib import Path
import requests
from classes import ModelInfoList, TaskType
from pathlib import Path

from config import load_config

CONFIG_PATH = Path(__file__).parent / "config.toml"



if __name__ == "__main__":
    try:
        model_list = ModelInfoList()
        model_list.initialize()
        model_list.display()

    except requests.exceptions.ConnectionError:
        print("Could not connect to Ollama. Make sure Ollama is running.")

    except requests.exceptions.Timeout:
        print("The request timed out. Check model performance and try again.")

    except requests.exceptions.HTTPError as error:
        print(f"Ollama returned an HTTP error: {error}")
        if error.response is not None:
            print(error.response.text)

