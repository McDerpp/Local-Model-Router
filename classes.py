from enum import Enum
from typing import List, Optional


class TaskType(Enum):
    CODING = "coding"
    DEBUGGING = "debugging"
    EXPLANATION = "explanation"
    SUMMARIZATION = "summarization"
    REFACTORING = "refactoring"
    LONGANALYSIS = "long_analysis"


@dataclass
class PromptAnalysis:
    """Analyzes prompts with complexity and tags."""

    prompt: str
    complexity: int = 0
    tags: Optional[List[TaskType]] = None

    def __init__(self, prompt: str, complexity: int = 0, tags: List[TaskType] = None):
        self.prompt = prompt
        self.complexity = complexity
        self.tags = tags or []

    def display(self):
        print(f"[PromptAnalysis Debug]")
        print(f"  Prompt: {self.prompt}")
        print(f"  Complexity: {self.complexity}")
        print(f"  Tags: {self.tags if self.tags else 'None'}")



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