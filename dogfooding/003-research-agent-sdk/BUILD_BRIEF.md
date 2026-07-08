# Build Brief: Phase 1 — MVP

## Phase Scope
Build the core abstractions for a Research Agent SDK: Agent, Tool, Memory, Provider, and Workflow abstractions. Zero runtime dependencies. Python 3.10+.

## Tasks (in dependency order)

1. **T1.1: Project skeleton** — pyproject.toml, __init__.py, directory structure
2. **T1.2: Tool abstraction** — BaseTool, ToolRegistry (standalone, no deps)
3. **T1.3: Memory abstraction** — BaseMemory, InMemoryMemory (standalone)
4. **T1.4: Provider abstraction** — BaseProvider, MockProvider (standalone)
5. **T1.5: Agent abstraction** — BaseAgent (depends on Provider)
6. **T1.6: Workflow abstraction** — Workflow (depends on all above)
7. **T1.7: __init__.py exports** — public API surface
8. **T1.8: Basic agent example** — single tool
9. **T1.9: Multi-tool example** — tool call loop

## Acceptance Criteria to Satisfy
- AC-1: Agent abstraction (T1.5, T1.7)
- AC-2: Tool abstraction (T1.2, T1.7)
- AC-3: Memory abstraction (T1.3, T1.7)
- AC-4: Provider abstraction (T1.4, T1.7)
- AC-5: Workflow abstraction (T1.6, T1.7)
- AC-6: Examples (T1.1, T1.8, T1.9)

## Architecture Essentials

### Module dependency graph
```
tool.py       → (none)
memory.py     → (none)
provider.py   → (none)
agent.py      → provider.py
workflow.py   → agent.py, tool.py, memory.py, provider.py
__init__.py   → all modules
```

### Interface contracts (MVP)

**BaseTool**: `name: str`, `description: str`, `execute(params: dict) → str`
**ToolRegistry**: `register(tool)`, `get(name) → BaseTool | None`, `list_all() → list`, `execute(name, params) → str`
**BaseMemory**: `store(message: dict)`, `retrieve(query: str) → list[dict]`, `clear()`
**InMemoryMemory**: list-based implementation of BaseMemory
**BaseProvider**: `complete(messages: list[dict]) → str`
**MockProvider**: keyword-based canned responses, fallback to "Mock response to: ..."
**BaseAgent**: `__init__(provider)`, `run(input) → str` (abstract)
**Workflow**: `__init__(agent, tools, memory, provider)`, `run(input) → str`

### Key patterns
- All abstractions are Python ABCs using `abc.ABC` and `@abstractmethod`
- Tool execute() catches all exceptions internally
- Provider response with "TOOL_CALL:name:params" triggers tool execution
- Workflow loop limited to 5 iterations

## Verification

### AC-1: Agent abstraction
- **Command**: `python3 -c "from research_agent_sdk import BaseAgent; print('OK')"`
- **Expected**: `OK`
- **Done when**: Import works without error

### AC-2: Tool abstraction
- **Verify**: BaseTool and ToolRegistry import and function
- **Command**: `python3 -c "from research_agent_sdk import BaseTool, ToolRegistry; print('OK')"`
- **Expected**: `OK`
- **Done when**: Import works

### AC-3: Memory abstraction
- **Verify**: BaseMemory and InMemoryMemory import
- **Command**: `python3 -c "from research_agent_sdk import BaseMemory, InMemoryMemory; m = InMemoryMemory(); m.store({'role': 'user', 'content': 'hi'}); print(m.retrieve(''))"`
- **Expected**: `[{'role': 'user', 'content': 'hi'}]`
- **Done when**: Storage and retrieval work

### AC-4: Provider abstraction
- **Verify**: MockProvider returns configured responses
- **Command**: `python3 -c "from research_agent_sdk import MockProvider; p = MockProvider({'hello': 'Hi there'}); print(p.complete([{'role':'user','content':'hello'}]))"`
- **Expected**: `Hi there`
- **Done when**: MockProvider returns matched response

### AC-5: Workflow abstraction
- **Verify**: Workflow runs end-to-end with all components
- **Command**: `python3 examples/basic_agent.py`
- **Expected**: Prints a response without errors, exit code 0
- **Done when**: Example runs successfully

### AC-6: Examples exist
- **Verify**: Both example files exist and are runnable
- **Command**: `python3 examples/basic_agent.py && python3 examples/multi_tool.py`
- **Expected**: Both print output and exit with code 0
- **Done when**: Both examples run without unhandled exceptions

## Known Plan Gaps
- No test specification for MVP (tests structure exists but deferred)
- Mock provider only supports single-turn canned responses — multi-turn not tested
- Tool call parameter format "TOOL_CALL:name:params" uses colon-separated simple strings — not JSON. May need upgrading for complex params
