import json
import os
from pathlib import Path

from chatbot.models import Message


BASE_DIR = Path.home() / ".chatbot" / "sessions"
SCHEMA_VERSION = 1


def _ensure_dir():
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def _session_path(session_id: str) -> Path:
    return BASE_DIR / f"{session_id}.jsonl"


def append(session_id: str, messages: list[Message]) -> None:
    if not messages:
        return
    for m in messages:
        if not m.content:
            raise ValueError("Message content cannot be empty")
    _ensure_dir()
    path = _session_path(session_id)
    with open(path, "a") as f:
        for msg in messages:
            f.write(json.dumps({"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}) + "\n")


def get_history(session_id: str) -> list[Message]:
    path = _session_path(session_id)
    if not path.exists():
        return []
    messages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            messages.append(Message(role=data["role"], content=data["content"], timestamp=data.get("timestamp", "")))
    return messages


def load_session(session_id: str) -> bool:
    path = _session_path(session_id)
    return path.exists()


def close_session(session_id: str) -> None:
    pass
