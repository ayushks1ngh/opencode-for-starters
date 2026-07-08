# PRD: Memory-Enabled Agent Chatbot (v0.5.0 Dogfooding)

## Problem Statement
Developers need a local, extensible AI chatbot that persists conversation context and supports multi-tool orchestration. Existing solutions are either cloud-only, lack memory, or cannot be extended with custom tools.

## User Personas
- **Developer**: Wants a local chatbot with conversation history and the ability to add custom tools
- **Power User**: Wants session management, retry on failure, and error recovery without losing context

## Use Cases
- UC-1: Start a new chat session
- UC-2: Send a message and receive an AI response using a configured LLM provider
- UC-3: The agent can call tools (e.g. calculator, web search placeholder) to answer questions
- UC-4: Conversation history persists across restarts
- UC-5: Sessions can be listed, resumed, and deleted
- UC-6: Failed LLM calls are retried with configurable policy
- UC-7: Invalid tool calls are handled gracefully (error recovery)
- UC-8: Multiple tools can be chained in a single turn

## Scope

### In Scope (Phase 1)
- Session management (create, list, resume, delete)
- Conversation memory with persistence (JSON file-based)
- LLM provider abstraction with OpenAI-compatible API support
- Tool calling framework with 2 built-in tools (calculator, current time)
- Retry handling for LLM provider failures
- Error recovery for invalid tool calls
- CLI interface (REPL)

### Out of Scope
- Web UI or HTTP server
- Streaming responses
- Multiple simultaneous sessions
- Authentication / multi-user
- Plugin system for dynamic tool loading
- Vector-based retrieval memory
- Deployment / containerization

## Success Metrics
- All 7 core features implemented and verified
- Conversation history survives restart (persistence)
- Invalid tool calls produce graceful error messages (no crash)
- Retry policy is configurable and observable

## Acceptance Criteria

### AC-1 (Phase 1): Session Management
User can create, list, resume, and delete chat sessions. Sessions are identified by a unique ID and have a human-readable title.

### AC-2 (Phase 1): Message Sending
User can send a message in a session and receive an AI-generated response. The response uses the configured LLM provider.

### AC-3 (Phase 1): Tool Calling
Agent can recognize when a tool call is needed and execute built-in tools (calculator, current time). Results are incorporated into the response.

### AC-4 (Phase 1): Conversation Memory
Conversation history is persisted to disk and loaded on session resume. Messages are stored with role, content, and timestamp.

### AC-5 (Phase 1): Retry Handling
LLM provider failures (network errors, rate limits, 5xx) trigger automatic retry with configurable max_retries and backoff. Non-retryable errors (4xx auth) fail fast.

### AC-6 (Phase 1): Error Recovery
Invalid tool calls (wrong args, non-existent tool) produce a descriptive error message. The agent can continue the conversation without crashing.

### AC-7 (Phase 1): Multi-Tool Orchestration
Agent can call multiple tools sequentially within a single turn (e.g. calculate 2+2, then get current time, then summarize results).

## Security Constraints (L2)
- **API key management**: LLM provider API keys are read from environment variables only (never from config files)
- **Input validation**: User messages are truncated to 4096 characters. Tool arguments are validated against schema before execution
- **Allowed protocols**: Only HTTPS for LLM API calls. No local file access beyond the persistence directory
- **Trust boundaries**: User input is untrusted. Tool output is trusted only after schema validation. LLM responses are treated as untrusted until parsed
- **Security assumptions**: No encryption at rest for persistence files (MVP). No authentication for CLI

## Operational Constraints (L3)
- **Runtime assumptions**: Python 3.11+, required packages (httpx, pydantic), no OS-specific dependencies
- **Storage locations**: Chat history stored in `~/.chatbot/sessions/` as JSON files
- **Database configuration**: File-based JSON storage. No SQL database. Migration: N/A (schema version embedded in file)
- **Environment requirements**: `OPENAI_API_KEY` or compatible provider env var. `CHATBOT_MAX_RETRIES` (default 3). `CHATBOT_RETRY_DELAY` (default 2.0s)
- **Deployment assumptions**: Single-user, single-process CLI. No containerization
