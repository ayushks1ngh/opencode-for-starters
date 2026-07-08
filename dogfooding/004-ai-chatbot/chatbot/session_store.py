import json
from pathlib import Path
from typing import Optional

from chatbot.models import Session
from chatbot.message_store import BASE_DIR, _ensure_dir


INDEX_PATH = BASE_DIR / "index.json"


def _load_index() -> dict:
    _ensure_dir()
    if not INDEX_PATH.exists():
        return {"sessions": [], "schema_version": 1}
    with open(INDEX_PATH) as f:
        return json.load(f)


def _save_index(index: dict) -> None:
    _ensure_dir()
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)


def create_session(session_id: str, title: str) -> Session:
    index = _load_index()
    session = Session(id=session_id, title=title)
    index["sessions"].append({"id": session.id, "title": session.title, "created_at": session.created_at, "message_count": 0})
    _save_index(index)
    return session


def list_sessions() -> list[Session]:
    index = _load_index()
    return [Session(**s) for s in index["sessions"]]


def get_session(session_id: str) -> Optional[Session]:
    index = _load_index()
    for s in index["sessions"]:
        if s["id"] == session_id:
            return Session(**s)
    return None


def delete_session(session_id: str) -> bool:
    index = _load_index()
    before = len(index["sessions"])
    index["sessions"] = [s for s in index["sessions"] if s["id"] != session_id]
    if len(index["sessions"]) == before:
        return True
    _save_index(index)
    return True


def update_message_count(session_id: str, count: int) -> None:
    index = _load_index()
    for s in index["sessions"]:
        if s["id"] == session_id:
            s["message_count"] = count
            break
    _save_index(index)
