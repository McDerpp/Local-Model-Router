from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
import requests

from config import config


class ModelStatus(Enum):
    LOADING = "loading"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"


class TaskType(Enum):
    CODING = "coding"
    DEBUGGING = "debugging"
    EXPLANATION = "explanation"
    SUMMARIZATION = "summarization"
    REFACTORING = "refactoring"
    LONGANALYSIS = "long_analysis"


@dataclass
class ModelInfoList:
    """A list of available models."""

    models: List[ModelInfo] = field(default_factory=list)

    def __init__(self, models: List[ModelInfo] = None):
        self.models = models or []

    def initialize(self):
        """Fetch models and configure their capabilities."""

        self.get_model_list()

        # self.assign_tags_to_model(
        #     "qwen3:0.6b",
        #     [TaskType.CODING, TaskType.DEBUGGING],
        # )

        # self.assign_complexity_to_model(
        #     "qwen3:0.6b",
        #     1,
        #     5,
        # )

    def get_model_list(self):
        """Fetch the list of available models from the Ollama API."""

        response = requests.get(f"{config["ollama"]["base_url"]}/tags", timeout=10)
        data = response.json()

        for model in data["models"]:
            self.models.append(
                ModelInfo(name=model["name"], status=ModelStatus.READY, tags=[])
            )
            


    def display(self):
        for model in self.models:
            model.display()

    def assign_tags_to_model(self, model_name: str, tags: List[TaskType]):
        """Assign tags to a specific model by name."""
        for model in self.models:
            if model.name == model_name:
                model.tags = tags
                return
        raise ValueError(f"Model with name '{model_name}' not found.")

    def assign_complexity_to_model(
        self, model_name: str, min_complexity: int, max_complexity: int
    ):
        """Assign complexity range to a specific model by name."""
        for model in self.models:
            if model.name == model_name:
                model.min_complexity = min_complexity
                model.max_complexity = max_complexity
                return
        raise ValueError(f"Model with name '{model_name}' not found.")


@dataclass
class ModelInfo:
    """Information about a model."""

    name: str
    status: ModelStatus
    tags: List[TaskType] = field(default_factory=list)
    min_complexity: Optional[int] = None
    max_complexity: Optional[int] = None

    def __init__(
        self,
        name: str,
        status: ModelStatus,
        tags: List[TaskType] = None,
        min_complexity: int = None,
        max_complexity: int = None,
    ):
        self.name = name
        self.status = status
        self.tags = tags or []
        self.min_complexity = min_complexity
        self.max_complexity = max_complexity

    def display(self):
        print(f"[ModelInfo Debug]")
        print(f"  Name: {self.name}")
        print(f"  Status: {self.status}")
        print(f"  Tags: {self.tags if self.tags else 'None'}")
        print(f"  Min Complexity: {self.min_complexity}")
        print(f"  Max Complexity: {self.max_complexity}")


@dataclass
class Prompt:
    """Analyzes prompts with complexity and tags."""

    prompt: str
    model_router: ModelInfo
    complexity: int = 0
    tags: Optional[List[TaskType]] = None

    def __init__(
        self,
        prompt: str,
        complexity: int = 0,
        tags: List[TaskType] = None,
        model_router: ModelInfo = None,
    ):
        self.prompt = prompt
        self.complexity = complexity
        self.tags = tags or []
        self.model_router = model_router

    def analyze_to_route(self):
        chat(self.prompt)

    def chat(prompt: str) -> str:
        """Send a prompt to a local Ollama model and return its response."""

        payload = {
            "model": ["mdoels"]["router"],
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
            config["ollama"]["base_url"],
            json=payload,
            timeout=180,
        )

        response.raise_for_status()

        result = response.json()
        return result["message"]["content"]

    def display(self):
        print(f"[PromptAnalysis Debug]")
        print(f"  Prompt: {self.prompt}")
        print(f"  Complexity: {self.complexity}")
        print(f"  Tags: {self.tags if self.tags else 'None'}")
        print(
            f"  Model Router: {self.model_router.name if self.model_router else 'None'}"
        )


@dataclass
class ModelRequest:
    """Simple request for model inference."""

    prompt: str
    model: str

    def __init__(self, prompt: str, model: str):
        self.prompt = prompt
        self.model = model

    def display(self):
        print(f"[ModelRequest Debug]")
        print(f"  Prompt: {self.prompt}")
        print(f"  Model: {self.model}")

    @dataclass
    class ModelClassification:
        """Simple request for model inference."""

        model_name: str
        min_complexity: Optional[int] = None
        max_complexity: Optional[int] = None
        tags: Optional[List[TaskType]] = None

        def __init__(self, model_name: str, min_complexity: int):
            self.model_name = model_name
            self.min_complexity = min_complexity
            self.max_complexity = max_complexity
            self.tags = tags

        def display(self):
            print(f"[ModelClassification Debug]")
            print(f"  Model Name: {self.model_name}")
            print(f"  Min Complexity: {self.min_complexity}")
            print(f"  Max Complexity: {self.max_complexity}")
            print(f"  Tags: {self.tags if self.tags else 'None'}")
