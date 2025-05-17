from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

class UserInput(BaseModel):
    """Basic user input for the agent."""
    prompt: str = Field(
        description="User input to the agent.",
        examples=["What is the weather in Tokyo?"],
    )
    thread_id: str | None = Field(
        description="Thread ID to persist and continue a multi-turn conversation.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )