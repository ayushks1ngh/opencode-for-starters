"""Verification tests for AC-1, AC-4, AC-5, AC-6 — runs without an API key."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

# Override storage to temp dir for testing
import chatbot.message_store as ms
import chatbot.session_store as ss

tmpdir = Path(tempfile.mkdtemp(prefix="chatbot_test_"))
ms.BASE_DIR = tmpdir
ss.BASE_DIR = tmpdir
ss.INDEX_PATH = tmpdir / "index.json"

from chatbot.models import Message, ToolResult
from chatbot import session_manager
from chatbot import retry_handler
from chatbot.tool_registry import register_builtins, execute, list_tools


passed = 0
failed = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name} {'- ' + detail if detail else ''}")
        failed += 1


# AC-1: Session Management
print("\n=== AC-1: Session Management ===")
s1 = session_manager.create_session("test-session-1")
check("create_session returns Session", isinstance(s1.id, str) and s1.title == "test-session-1")

sessions = session_manager.list_sessions()
check("list_sessions shows new session", any(s.id == s1.id for s in sessions))

s2 = session_manager.get_session(s1.id)
check("get_session returns session", s2 is not None and s2.title == "test-session-1")

session_manager.set_active_session(s1.id)
active = session_manager.get_active_session()
check("set/get_active_session works", active is not None and active.id == s1.id)

session_manager.delete_session(s1.id)
sessions_after = session_manager.list_sessions()
check("delete_session removes from list", not any(s.id == s1.id for s in sessions_after))

# AC-4: Conversation Memory
print("\n=== AC-4: Conversation Memory ===")
s3 = session_manager.create_session("memory-test")
session_manager.set_active_session(s3.id)

msgs = [Message(role="user", content="Hello"), Message(role="assistant", content="Hi there!")]
session_manager.append_messages(s3.id, msgs)

history = session_manager.get_history(s3.id)
check("get_history returns messages", len(history) == 2)
check("first message preserved", history[0].role == "user" and history[0].content == "Hello")
check("second message preserved", history[1].role == "assistant" and history[1].content == "Hi there!")

# AC-5: Retry Handling
print("\n=== AC-5: Retry Handling ===")
call_count = 0

def failing_function():
    global call_count
    call_count += 1
    raise ConnectionError("Test transient error")

call_count = 0
try:
    retry_handler.execute(failing_function, max_retries=2, delay=0.01)
    check("retry exhausted raises error", False, "should have raised")
except retry_handler.RetryExhaustedError:
    check("retry exhausted after max_retries+1 calls", call_count == 3, f"called {call_count} times, expected 3")
except Exception:
    check("retry exhausted raises RetryExhaustedError", False, "wrong exception type")

def non_retryable():
    raise ValueError("Bad input")

try:
    retry_handler.execute(non_retryable, max_retries=3, delay=0.01)
    check("non-retryable raises immediately", False, "should have raised")
except ValueError:
    check("non-retryable passes through original error", True)

def succeeds_on_second():
    global call_count
    call_count += 1
    if call_count < 2:
        raise ConnectionError("Transient")
    return "success"

call_count = 0
result = retry_handler.execute(succeeds_on_second, max_retries=3, delay=0.01)
check("retry succeeds on second attempt", result == "success")

# AC-6: Error Recovery
print("\n=== AC-6: Error Recovery ===")
register_builtins()

# Invalid tool name
result = execute("nonexistent_tool", {})
check("unknown tool returns error result", not result.success and "Unknown tool" in result.error)

# Invalid calculator args
result = execute("calculator", {"expression": ""})
check("empty calculator expression returns error", not result.success)

# Calculator with invalid chars
result = execute("calculator", {"expression": "import os"})
check("calculator rejects dangerous input", not result.success and "disallowed" in result.error)

# Valid calculator
result = execute("calculator", {"expression": "2 + 2"})
check("calculator returns correct result", result.success and result.output == "4")

# Current time
result = execute("current_time", {})
check("current_time returns ISO by default", result.success and "T" in result.output)

result = execute("current_time", {"format": "readable"})
check("current_time readable format", result.success and "UTC" in result.output)

# Tool listing
tools = list_tools()
check("tool registry lists 2 tools", len(tools) == 2)
tool_names = [t.name for t in tools]
check("calculator registered", "calculator" in tool_names)
check("current_time registered", "current_time" in tool_names)

print(f"\n{'='*40}")
print(f"Results: {passed} passed, {failed} failed")
print(f"{'='*40}")
