from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Message:
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Session:
    id: str
    title: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    message_count: int = 0


@dataclass
class ToolDef:
    name: str
    description: str
    parameters: dict


@dataclass
class ToolResult:
    success: bool
    output: str = ""
    error: str = ""


@dataclass
class LLMResponse:
    text: Optional[str] = None
    tool_calls: list[dict] = field(default_factory=list)
    finish_reason: str = "stop"
    error: Optional[str] = None
