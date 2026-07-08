from typing import Protocol

from chatbot.models import ToolResult


class Tool(Protocol):
    name: str
    description: str
    parameters: dict

    def execute(self, args: dict) -> ToolResult: ...
