# BUILD_BRIEF: Memory-Enabled Agent Chatbot — Phase 1

## Phase Scope
Phase 1 (MVP): Core chat loop with session management, LLM provider, tool calling, retry, error recovery, and persistence.

## Tasks to Implement (in order)

```
T1.1  models.py               (depends_on: none)
T1.2  tools/base.py           (depends_on: none)
T1.3  message_store.py        (depends_on: T1.1)
T1.4  session_store.py        (depends_on: T1.1)
T1.5  session_manager.py      (depends_on: T1.3, T1.4)
T1.6  retry_handler.py        (depends_on: T1.1)
T1.7  llm_provider.py         (depends_on: T1.6)
T1.8  tools/calculator.py     (depends_on: T1.2)
T1.9  tools/current_time.py   (depends_on: T1.2)
T1.10 tool_registry.py        (depends_on: T1.2, T1.8, T1.9)
T1.11 orchestrator.py         (depends_on: T1.7, T1.10)
T1.12 cli.py                  (depends_on: T1.5, T1.11)
T1.13 __main__.py             (depends_on: T1.12)
T1.14 Verification            (depends_on: T1.13)
```

## Acceptance Criteria

| AC | Description | Phase |
|----|-------------|-------|
| AC-1 | Session management: create, list, resume, delete | P1 |
| AC-2 | Message sending: user message → AI response via LLM provider | P1 |
| AC-3 | Tool calling: agent executes built-in tools (calculator, current time) | P1 |
| AC-4 | Conversation memory: history persisted to disk, loaded on resume | P1 |
| AC-5 | Retry handling: transient failures retried, non-retryable fail fast | P1 |
| AC-6 | Error recovery: invalid tool calls produce graceful error, no crash | P1 |
| AC-7 | Multi-tool orchestration: multiple tools in a single turn | P1 |

## Architecture Essentials

### File Structure
```
chatbot/
  __main__.py
  cli.py
  session_manager.py
  session_store.py
  message_store.py
  orchestrator.py
  llm_provider.py
  tool_registry.py
  retry_handler.py
  models.py
  tools/
    __init__.py
    base.py
    calculator.py
    current_time.py
```

### Key Interfaces (for this phase)

**MessageStore**: `append(session_id, messages)`, `get_history(session_id)`, `load_session(session_id)`, `close_session(session_id)`

**LLMProvider**: `chat(messages, tools) → LLMResponse` — wrapped in RetryHandler

**ToolRegistry**: `register(tool)`, `execute(name, args) → ToolResult`, `list_tools()`

**Orchestrator**: `run(user_message, history, tools) → str` — main loop

**RetryHandler**: `execute(callable, max_retries=3, delay=2.0) → Any`

## Verification Section

### AC-1: Session Management
- **Verify**: Create, list, resume, delete sessions
- **Command**: `python -m chatbot` then:
  - `/create test-session` → "Created session <id>"
  - `/list` → shows session with title "test-session"
  - `/resume <id>` → session becomes active
  - `/delete <id>` → "Deleted session <id>", `/list` no longer shows it
- **Expected**: All 4 operations succeed without errors
- **Done when**: All 4 operations verified

### AC-2: Message Sending
- **Verify**: Send message in active session, get AI response
- **Command**: `python -m chatbot` → `/create test` → type "Hello" → see AI response
- **Expected**: AI responds appropriately. Message appears in history on resume
- **Done when**: User message + AI response are persisted and visible on `/resume`

### AC-3: Tool Calling
- **Verify**: Agent uses calculator and current_time tools
- **Command**: Type "what is 2 + 2?" → AI should calculate. Type "what time is it?" → AI should use current_time
- **Expected**: Calculator returns ~4, current_time returns valid datetime string
- **Done when**: Both tools execute and results are incorporated into AI response

### AC-4: Conversation Memory
- **Verify**: History persists after restart
- **Command**: Send messages, exit, restart, `/resume <id>`, send "What was my last message?"
- **Expected**: AI can reference conversation history from before restart
- **Done when**: AI correctly refers to pre-restart messages

### AC-5: Retry Handling
- **Verify**: Transient failures cause retry, auth errors fail fast
- **Command**: Set `OPENAI_API_KEY` to invalid key → send message → expect immediate auth error
- **Expected**: Auth error message shown, no retry. For transient (simulate by dropping network), retry observed in logs (with --debug flag)
- **Done when**: Auth errors fail fast, transient errors show retry attempts in debug output

### AC-6: Error Recovery
- **Verify**: Invalid tool calls don't crash the chatbot
- **Command**: Ask "calculate foo bar" (invalid expression for calculator)
- **Expected**: Chatbot responds with error message like "I couldn't calculate that: invalid expression", conversation continues
- **Done when**: Chatbot continues after tool error without crashing

### AC-7: Multi-Tool Orchestration
- **Verify**: Multiple tools in one turn
- **Command**: Ask "What is 5 + 3 and what time is it?"
- **Expected**: Both calculator and current_time are called (order may vary). Final response includes both results
- **Done when**: Both tools execute in a single turn and results are combined in response

## Known Plan Gaps
- No streaming support (out of scope for P1)
- No vector-based memory (out of scope)
- LLM-specific behavior may vary across providers
- Retry backoff is fixed (not exponential) for P1
