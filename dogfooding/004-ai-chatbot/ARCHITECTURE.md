# Architecture: Memory-Enabled Agent Chatbot

## System Design

```
User (CLI)
  │
  ▼
SessionManager ──► MessageStore ──► (persistence/JSON)
  │
  ▼
Orchestrator ──► LLMProvider ──► (external API)
  │                 │
  ▼                 ▼
ToolRegistry    RetryHandler
  │
  ▼
Tool (calc, time, ...)
```

### Component Boundaries

| Component | Responsibility | Stateful |
|-----------|---------------|----------|
| SessionManager | CRUD sessions, active session tracking | Yes (active session ID, session list cache) |
| MessageStore | Read/write messages to disk, load on resume | Yes (loaded messages cache) |
| Orchestrator | Main loop: receive message → call LLM → parse response → execute tools → return result | Yes (conversation context within turn) |
| LLMProvider | Abstract interface for LLM API calls | No |
| ToolRegistry | Register, list, and invoke tools by name | Yes (registered tool map) |
| Tool | Individual tool with schema and execute | No (stateless) |
| RetryHandler | Configurable retry with backoff for transient failures | No |
| SessionStore | Persistence layer for sessions metadata | No |

## Data Flow (Message Turn)

```
1. CLI reads user input → SessionManager.get_active_session()
2. SessionManager → MessageStore.get_history(session_id)
3. SessionManager → Orchestrator.run(user_message, history, tools)
4. Orchestrator → LLMProvider.chat(history + message, tools_schema)
5. LLMProvider → RetryHandler.wrap(...) → external API → response
6. Orchestrator parses response: text or tool_call
7. If tool_call → Orchestrator → ToolRegistry.execute(tool_name, args)
8. Tool result → Orchestrator → LLMProvider.chat(history + tool_result)
9. Repeat 6-8 until LLM returns text
10. Orchestrator returns final response → SessionManager
11. SessionManager → MessageStore.append(session_id, user_msg, assistant_msg)
```

## Technology Choices
- **Language**: Python 3.11+
- **HTTP client**: httpx (async support, connection pooling)
- **Validation**: pydantic (tool schemas, message models)
- **Persistence**: JSON lines files (append-only, simple schema)
- **CLI**: readline + argparse (no external CLI framework needed)

## Interface Contracts

### SessionManager
- `create_session(title: str) → Session`
- `list_sessions() → list[Session]`
- `get_session(session_id: str) → Session | None`
  - Invalid input: returns None for non-existent ID
  - State transition: session must exist (created via create_session)
  - Concurrency: single-threaded, no locking needed
- `delete_session(session_id: str) → bool`
  - Idempotent: Yes — deleting already-deleted session returns True
  - State transition: ACTIVE → DELETED, messages remain on disk
- `get_active_session() → Session | None`
- `set_active_session(session_id: str) → None`
  - Invalid input: raises ValueError if session_id does not exist

### MessageStore
- `append(session_id: str, messages: list[Message]) → None`
  - Duplicate: No dedup — caller must ensure no duplicate appends
  - Invalid input: raises ValueError if any message has empty content
- `get_history(session_id: str) → list[Message]`
  - Invalid input: returns empty list for non-existent session
- `load_session(session_id: str) → bool`
  - Idempotent: Yes — loading already-loaded session is a no-op
- `close_session(session_id: str) → None`
  - Lifecycle: messages are flushed to disk on close
  - State transition: loaded → flushed → closed (cannot append after close)

### LLMProvider
- `chat(messages: list[Message], tools: list[ToolDef]) → LLMResponse`
  - Idempotent: No — each call may produce different results (non-deterministic LLM)
  - Duplicate call: repeated identical calls may return different responses
  - Invalid input: raises ValueError if messages list is empty
  - Retry: transient failures (timeout, 429, 5xx) retried via RetryHandler
  - Non-retryable: 4xx auth errors fail immediately
  - Resource limits: max 4096 input tokens, max 1024 output tokens
- `list_models() → list[str]`
  - Idempotent: Yes

### ToolRegistry
- `register(tool: Tool) → None`
  - Duplicate: overwrites existing tool with same name (last wins)
  - Invalid input: raises TypeError if tool does not implement Tool protocol
- `execute(tool_name: str, args: dict) → ToolResult`
  - Invalid input: raises KeyError if tool_name not found
  - Invalid args: tool returns error result (not exception) for bad args
  - Idempotent: depends on tool (calculator is idempotent, email-send is not)
  - Concurrency: single-threaded, no locking
- `list_tools() → list[str]`
  - Idempotent: Yes

### Tool (protocol)
- `name → str`
- `description → str`
- `parameters → dict` (JSON Schema)
- `execute(args: dict) → ToolResult`
  - Invalid input: returns ToolResult(success=False, error="reason") never raises
  - Retry: caller may retry on transient failures (not for invalid args)
  - Resource limits: tool execution hard-limited to 10s timeout

### RetryHandler
- `execute(callable, max_retries: int, delay: float) → Any`
  - Retry condition: timeout, ConnectionError, HTTP 429, HTTP 5xx
  - Fail-fast: HTTP 4xx, ValueError, TypeError
  - Backoff: fixed delay between retries (exponential for v2)
  - Duplicate: retries may result in duplicate side effects (caller must handle)
  - State: no internal state between calls

## Behavioral Edge Cases

### Session Lifecycle
- Creating a session with duplicate title: allowed (IDs are unique, not titles)
- Resuming a deleted session: returns None, no crash
- Deleting active session: session is deactivated, messages remain on disk
- Empty session with no messages: valid state, shows empty history

### Message Handling
- Empty message: rejected with user-facing error "Message cannot be empty"
- Very long message (>4096 chars): truncated with warning
- Special characters in messages: stored and displayed as-is (no escaping issues with JSON)

### Tool Execution
- Unknown tool: "I don't have a tool named X" response, conversation continues
- Tool returns error: error is sent back to LLM, LLM can decide next action
- Tool times out (>10s): orchestrator interrupts, returns timeout error to LLM
- LLM hallucinates tool call with wrong args: args fail schema validation, error sent to LLM

### Retry Scenarios
- Network timeout on first call: retry after delay, succeed on second → transparent to user
- Rate limit (429) with retry exhausted: user sees "Service temporarily unavailable, try again later"
- Auth error (401): immediate failure, user sees "Check your API key"
- Consecutive failures across retries: all intermediate errors logged to debug output

## Module Dependency Graph

```
chatbot/
  __main__.py      →  cli.py
  cli.py           →  session_manager.py, orchestrator.py
  session_manager.py →  message_store.py, models.py
  message_store.py →  models.py, (json)
  orchestrator.py  →  llm_provider.py, tool_registry.py, retry_handler.py, models.py
  llm_provider.py  →  retry_handler.py, models.py
  tool_registry.py →  tools/__init__.py, models.py
  retry_handler.py →  (httpx)
  tools/
    __init__.py    →  base.py, calculator.py, current_time.py
    base.py        →  models.py
    calculator.py  →  base.py
    current_time.py →  base.py
  models.py        →  (pydantic)
```

Import order: models.py → base.py → message_store.py → session_manager.py → retry_handler.py → llm_provider.py → tool_registry.py → tools/* → orchestrator.py → cli.py → __main__.py

No circular dependencies. Every arrow represents a direct import.
