# PRD: Research Agent SDK

## Problem Statement
Building research agents requires stitching together LLM providers, tool execution, memory management, and workflow orchestration. Existing frameworks (LangChain, CrewAI, AutoGPT) are heavy, opinionated, and couple these concerns tightly. Developers need a lightweight, composable SDK where each abstraction is independently usable and replaceable.

## Target Audience
- Python developers building research agents
- Teams who want modular agent architectures
- Anyone who finds LangChain too heavy

## User Stories

### MVP (Phase 1)
1. As a developer, I can define a custom agent by extending a base Agent class so I don't reinvent orchestration
2. As a developer, I can define custom tools with a name, description, and execute function so my agent can interact with external systems
3. As a developer, I can plug in different memory backends so conversation history is managed consistently
4. As a developer, I can switch between LLM providers without changing my agent code so I'm not locked into one provider
5. As a developer, I can define a workflow that binds agent + tools + memory + provider together so the full loop is configured in one place
6. As a developer, I can run example scripts to verify the SDK works end-to-end

## Acceptance Criteria

### AC-1 (Phase 1): Agent abstraction
- `BaseAgent` class with `run(input: str) → str` method
- Users create `class MyAgent(BaseAgent): pass` and provide a workflow
- Agent is initialized with a provider reference

### AC-2 (Phase 1): Tool abstraction
- `BaseTool` class with `name: str`, `description: str`, `execute(params: dict) → str` method
- Tool execution errors are caught and returned as error messages, not exceptions
- `ToolRegistry` class for registering and looking up tools by name

### AC-3 (Phase 1): Memory abstraction
- `BaseMemory` class with `store(message: dict)`, `retrieve(query: str) → list[dict]`, `clear()` methods
- `InMemoryMemory` implementation for MVP (no persistence)
- Messages stored as list of `{"role": ..., "content": ...}` dicts

### AC-4 (Phase 1): Provider abstraction
- `BaseProvider` class with `complete(messages: list[dict]) → str` method
- `MockProvider` implementation for testing (returns canned responses based on keyword matching)
- Provider is swappable — agent works with any provider implementation

### AC-5 (Phase 1): Workflow abstraction
- `Workflow` class that binds agent, tools, memory, provider together
- `run(input) → output` method that: stores input → calls provider → executes tools → stores response → returns output
- Supports tool calling loop: provider returns tool call → workflow executes tool → feeds result back to provider

### AC-6 (Phase 1): Examples
- `examples/basic_agent.py` — agent with one tool, one memory, mock provider
- `examples/multi_tool.py` — agent with multiple tools demonstrating tool selection
- Examples are runnable with `python examples/basic_agent.py`

## Security Constraints
- No network access required for mock provider (offline testable)
- Tool execution should sandbox: tools receive only `params` dict, no access to agent internals
- Memory content is not validated — caller responsibility
- Provider API keys are caller's responsibility (not in scope for MVP)
- No code execution or shell access in MVP tools

## Operational Constraints
- Python 3.10+ (for `str | None` union syntax and match statements)
- Zero runtime dependencies for core SDK (stdlib only)
- Testing: pytest (dev dependency)
- No async support in MVP (sync only)
- No persistence for MVP memory (in-memory only)
- Package name: `research_agent_sdk`
