import uuid
from typing import Optional

from chatbot.models import Message, Session
from chatbot import message_store, session_store


_active_session: Optional[Session] = None


def create_session(title: str) -> Session:
    session_id = str(uuid.uuid4())[:8]
    session = session_store.create_session(session_id, title)
    return session


def list_sessions() -> list[Session]:
    return session_store.list_sessions()


def get_session(session_id: str) -> Optional[Session]:
    return session_store.get_session(session_id)


def delete_session(session_id: str) -> bool:
    global _active_session
    if _active_session and _active_session.id == session_id:
        _active_session = None
    return session_store.delete_session(session_id)


def get_active_session() -> Optional[Session]:
    return _active_session


def set_active_session(session_id: str) -> None:
    global _active_session
    session = session_store.get_session(session_id)
    if session is None:
        raise ValueError(f"Session {session_id} does not exist")
    _active_session = session


def get_history(session_id: str) -> list[Message]:
    return message_store.get_history(session_id)


def append_messages(session_id: str, messages: list[Message]) -> None:
    message_store.append(session_id, messages)
    history = message_store.get_history(session_id)
    session_store.update_message_count(session_id, len(history))
