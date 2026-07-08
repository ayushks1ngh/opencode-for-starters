# Tasks: Memory-Enabled Agent Chatbot — Phase 1

All tasks are for Phase 1 (MVP). Total effort: ~8 hours.

## T1.1: Define Message model (0.25h)
- Create `models.py` with `Message(role, content, timestamp)`, `Session(id, title, created_at)`, `ToolDef(name, description, parameters)`, `ToolResult(success, output, error)`
- **AC-4**: Conversation memory

## T1.2: Define Tool protocol (0.25h)
- Create `tools/base.py` with `Tool` protocol: `name`, `description`, `parameters`, `execute(args) → ToolResult`
- **AC-3**: Tool calling

## T1.3: Implement MessageStore (0.5h)
- `message_store.py`: append JSON lines, get_history, load_session, close_session
- Files stored at `~/.chatbot/sessions/{session_id}.json`
- Schema version embedded in file header
- **AC-4**: Conversation memory
- **depends_on**: T1.1

## T1.4: Implement SessionStore (0.5h)
- `session_store.py`: metadata about all sessions (index file), CRUD
- Index stored at `~/.chatbot/sessions/index.json`
- **AC-1**: Session management
- **depends_on**: T1.1

## T1.5: Implement SessionManager (0.5h)
- `session_manager.py`: create_session, list_sessions, get_session, delete_session, get/set_active_session
- Wraps SessionStore + MessageStore
- **AC-1**: Session management
- **depends_on**: T1.3, T1.4

## T1.6: Implement RetryHandler (0.5h)
- `retry_handler.py`: execute with max_retries, delay, retryable conditions (timeout, 429, 5xx)
- Non-retryable: 4xx, ValueError, TypeError
- Logging for intermediate failures
- **AC-5**: Retry handling
- **depends_on**: T1.1

## T1.7: Implement LLMProvider (1h)
- `llm_provider.py`: abstract base + OpenAI-compatible implementation
- `chat(messages, tools)` → parsed response (text or tool_call)
- Reads `OPENAI_API_KEY` from env
- Wraps calls in RetryHandler
- **AC-2**: Message sending
- **depends_on**: T1.6

## T1.8: Implement Calculator tool (0.5h)
- `tools/calculator.py`: evaluate safe math expressions
- Parameters: `expression: str`
- Safety: only allows digits, +, -, *, /, (, ), ., space
- Returns numeric result or error
- **AC-3**: Tool calling
- **depends_on**: T1.2

## T1.9: Implement CurrentTime tool (0.25h)
- `tools/current_time.py`: returns current datetime string
- Parameters: `format: str` (optional, default ISO)
- **AC-3**: Tool calling
- **depends_on**: T1.2

## T1.10: Implement ToolRegistry (0.5h)
- `tool_registry.py`: register, execute(tool_name, args), list_tools
- validate args against Tool.parameters schema
- Returns ToolResult (never raises)
- **AC-3**: Tool calling, **AC-6**: Error recovery
- **depends_on**: T1.2, T1.8, T1.9

## T1.11: Implement Orchestrator (2h)
- `orchestrator.py`: main loop — receive message, call LLM, parse response, execute tools, loop until text
- Tool call loop: max 5 tool calls per turn (safety limit)
- LLM hallucination handling: invalid tool names → error message to LLM
- **AC-2**: Message sending, **AC-3**: Tool calling, **AC-6**: Error recovery, **AC-7**: Multi-tool
- **depends_on**: T1.7, T1.10

## T1.12: Implement CLI REPL (0.5h)
- `cli.py`: readline loop, command parsing (/create, /list, /resume, /delete, /exit)
- Displays session context, prompts for input
- Routes user messages to Orchestrator
- **AC-1**: Session management, **AC-2**: Message sending
- **depends_on**: T1.5, T1.11

## T1.13: Implement __main__.py (0.25h)
- Entry point: argparse for debug flag, calls cli.main()
- **depends_on**: T1.12

## T1.14: Verification (0.5h)
- Run all AC verification checks from BUILD_BRIEF
- Fix any failures
- **depends_on**: T1.13

## Traceability Matrix

```
AC-1 → T1.4, T1.5, T1.12
AC-2 → T1.7, T1.11, T1.12
AC-3 → T1.2, T1.8, T1.9, T1.10, T1.11
AC-4 → T1.1, T1.3
AC-5 → T1.6, T1.7
AC-6 → T1.10, T1.11
AC-7 → T1.11
```
