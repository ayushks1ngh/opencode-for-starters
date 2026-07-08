# Architecture: Research Agent SDK

## Tech Stack
- Language: Python 3.10+
- Dependencies: None (stdlib only)
- Testing: pytest

## System Design

The SDK is organized as a set of composable abstractions. Each abstraction is an abstract base class in its own module. Users extend these classes to create custom implementations.

```
User Code
    │
    ▼
Workflow (orchestration loop)
    │
    ├── Agent (receives input, delegates to workflow)
    ├── Tool (executes functions)
    ├── Memory (stores/retrieves context)
    └── Provider (completes via LLM)
```

## Interface Contracts

### BaseAgent (`research_agent_sdk/agent.py`)
```
class BaseAgent:
    - __init__(self, provider: BaseProvider) → None
    - run(self, input: str) → str
    Property:
    - provider → BaseProvider
```
- `run()` must be implemented by subclasses
- `provider` is the single provider used for all completions
- Error convention: raises `NotImplementedError` if `run()` not overridden

### BaseTool (`research_agent_sdk/tool.py`)
```
class BaseTool:
    Properties:
    - name → str              # tool identifier, used by registry
    - description → str       # natural language description for LLM
    Methods:
    - execute(params: dict) → str
```
- `name` must be unique across registered tools
- `description` is the string sent to the LLM for tool selection
- `execute()` catches all exceptions internally — returns error string, never raises
- Return value is always a string (result or error message)

### ToolRegistry (`research_agent_sdk/tool.py`)
```
class ToolRegistry:
    Methods:
    - register(tool: BaseTool) → None
    - get(name: str) → BaseTool | None
    - list_all() → list[BaseTool]
    - execute(name: str, params: dict) → str
```
- `register()` raises `ValueError` if tool with same name already registered
- `execute()` returns error string if tool not found

### BaseMemory (`research_agent_sdk/memory.py`)
```
class BaseMemory:
    Methods:
    - store(message: dict) → None
    - retrieve(query: str) → list[dict]
    - clear() → None
```
- Messages are `{"role": str, "content": str}` dicts
- `retrieve()` returns all messages for MVP (no filtering)
- `clear()` removes all stored messages

### InMemoryMemory (`research_agent_sdk/memory.py`)
```
class InMemoryMemory(BaseMemory):
    - __init__() → None
    - store(message: dict) → None
    - retrieve(query: str) → list[dict]
    - clear() → None
```
- Stores messages in a list in memory
- No persistence across sessions

### BaseProvider (`research_agent_sdk/provider.py`)
```
class BaseProvider:
    Methods:
    - complete(messages: list[dict]) → str
```
- `messages` is a list of `{"role": ..., "content": ...}` dicts
- Returns the response content as a string

### MockProvider (`research_agent_sdk/provider.py`)
```
class MockProvider(BaseProvider):
    - __init__(responses: dict[str, str] | None = None) → None
    - complete(messages: list[dict]) → str
```
- If `responses` dict is provided, returns the value for the first matching key found in the last user message
- If no match, returns "Mock response to: {last user message}"
- Used for testing and examples without an LLM

### Workflow (`research_agent_sdk/workflow.py`)
```
class Workflow:
    - __init__(agent: BaseAgent, tools: ToolRegistry, memory: BaseMemory, provider: BaseProvider) → None
    - run(input: str) → str
```
- Orchestrates the full loop: store input → provider complete → execute tools → store response → return
- If provider response contains "TOOL_CALL:{tool_name}:{params}", extracts and executes the tool, feeds result back
- Loop limit: 5 iterations max (prevents infinite tool loops)

## Module Dependency Graph

```
research_agent_sdk/
├── __init__.py       # exports all public classes
├── agent.py          # → depends on: provider.py
├── tool.py           # → depends on: (none — standalone)
├── memory.py         # → depends on: (none — standalone)
├── provider.py       # → depends on: (none — standalone)
└── workflow.py       # → depends on: agent.py, tool.py, memory.py, provider.py

examples/
├── basic_agent.py    # → depends on: research_agent_sdk
└── multi_tool.py     # → depends on: research_agent_sdk
```

Dependency order (import-safe):
1. `tool.py` (no deps)
2. `memory.py` (no deps)
3. `provider.py` (no deps)
4. `agent.py` (depends on provider.py)
5. `workflow.py` (depends on all above)
6. `__init__.py` (imports all modules)

No circular dependencies. Each module is independently importable.

## Project Structure

```
research_agent_sdk/
  __init__.py        # public API exports
  agent.py           # BaseAgent abstraction
  tool.py            # BaseTool + ToolRegistry
  memory.py          # BaseMemory + InMemoryMemory
  provider.py        # BaseProvider + MockProvider
  workflow.py        # Workflow orchestration
examples/
  basic_agent.py     # single-tool example
  multi_tool.py      # multi-tool example
tests/
  test_agent.py
  test_tool.py
  test_memory.py
  test_provider.py
  test_workflow.py
pyproject.toml       # packaging config
```

## Data Flow

```
User → Workflow.run("input text")
         ↓
      1. memory.store({"role": "user", "content": "input text"})
         ↓
      2. provider.complete(messages) → "response" or "TOOL_CALL:tool_name:params"
         ↓
      3a. If text response:
          memory.store({"role": "assistant", "content": "response"})
          return "response"
         ↓
      3b. If tool call:
          tool_registry.execute(tool_name, params)
          memory.store({"role": "tool", "content": result})
          goto step 2 (up to 5 iterations)
```

## Error Handling
- Tool execution errors → returned as string, never raised
- Provider returns empty string → "No response from provider"
- Workflow loop exceeds 5 iterations → returns "Workflow exceeded maximum iterations"
- `NotImplementedError` for abstract methods not overridden
