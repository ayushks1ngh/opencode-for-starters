import logging
import sys

from chatbot import session_manager
from chatbot.llm_provider import LLMProvider
from chatbot.models import Message
from chatbot.orchestrator import Orchestrator
from chatbot.tool_registry import register_builtins


def print_help():
    print("Commands:")
    print("  /create <title>  Create a new session")
    print("  /list           List all sessions")
    print("  /resume <id>    Resume a session")
    print("  /delete <id>    Delete a session")
    print("  /help           Show this help")
    print("  /exit           Exit the chatbot")
    print("  <message>       Send a message to the AI")


def main(debug: bool = False):
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    register_builtins()
    provider = LLMProvider()
    orchestrator = Orchestrator(provider)

    session = session_manager.get_active_session()

    print("Memory-Enabled Agent Chatbot")
    print("Type /help for commands, /exit to quit.")
    print()

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        if line == "/exit":
            break
        elif line == "/help":
            print_help()
            continue
        elif line.startswith("/create "):
            title = line[8:].strip()
            if not title:
                print("Usage: /create <title>")
                continue
            session = session_manager.create_session(title)
            session_manager.set_active_session(session.id)
            print(f"Created session {session.id}: {session.title}")
            continue
        elif line == "/list":
            sessions = session_manager.list_sessions()
            if not sessions:
                print("No sessions.")
            else:
                for s in sessions:
                    active = " (active)" if session and s.id == session.id else ""
                    print(f"  {s.id}: {s.title}{active}")
            continue
        elif line.startswith("/resume "):
            sid = line[8:].strip()
            if not sid:
                print("Usage: /resume <id>")
                continue
            try:
                session_manager.set_active_session(sid)
                session = session_manager.get_session(sid)
                print(f"Resumed session {sid}: {session.title}")
            except ValueError as e:
                print(f"Error: {e}")
            continue
        elif line.startswith("/delete "):
            sid = line[8:].strip()
            if not sid:
                print("Usage: /delete <id>")
                continue
            session_manager.delete_session(sid)
            print(f"Deleted session {sid}")
            if session and session.id == sid:
                session = None
            continue
        else:
            if session is None:
                print("No active session. Create or resume one first.")
                continue

            history = session_manager.get_history(session.id)
            response = orchestrator.run(line, history)

            session_manager.append_messages(session.id, [
                Message(role="user", content=line[:4096]),
                Message(role="assistant", content=response[:4096]),
            ])

            print(response)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    main(debug=debug)
