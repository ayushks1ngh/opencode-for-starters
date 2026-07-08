# Tasks: Research Agent SDK

## Phase 1: MVP

### T1.1: Project skeleton — depends_on: none (AC-6)
- [ ] Create directory structure: `research_agent_sdk/`, `examples/`, `tests/`
- [ ] Create `pyproject.toml` with build config (setuptools, Python 3.10+)
- [ ] Create `research_agent_sdk/__init__.py` with version and public exports
- [ ] Verify `python -c "import research_agent_sdk"` works

### T1.2: Tool abstraction — depends_on: T1.1 (AC-2)
- [ ] Create `research_agent_sdk/tool.py`
- [ ] Define `BaseTool` abstract class with `name`, `description`, `execute(params)`
- [ ] Implement `ToolRegistry` with `register()`, `get()`, `list_all()`, `execute()`
- [ ] `register()` raises `ValueError` on duplicate name
- [ ] `execute()` returns error string if tool not found
- [ ] `execute()` catches exceptions and returns error strings

### T1.3: Memory abstraction — depends_on: T1.1 (AC-3)
- [ ] Create `research_agent_sdk/memory.py`
- [ ] Define `BaseMemory` abstract class with `store()`, `retrieve()`, `clear()`
- [ ] Implement `InMemoryMemory` with list-based storage
- [ ] Messages stored as `{"role": ..., "content": ...}` dicts

### T1.4: Provider abstraction — depends_on: T1.1 (AC-4)
- [ ] Create `research_agent_sdk/provider.py`
- [ ] Define `BaseProvider` abstract class with `complete(messages)`
- [ ] Implement `MockProvider` with keyword-based canned responses
- [ ] MockProvider falls through to "Mock response to: {message}" if no match

### T1.5: Agent abstraction — depends_on: T1.4 (AC-1)
- [ ] Create `research_agent_sdk/agent.py`
- [ ] Define `BaseAgent` abstract class with `__init__(provider)` and `run(input)`
- [ ] `run()` raises `NotImplementedError` if not overridden

### T1.6: Workflow abstraction — depends_on: T1.2, T1.3, T1.4, T1.5 (AC-5)
- [ ] Create `research_agent_sdk/workflow.py`
- [ ] Implement `Workflow.__init__(agent, tools, memory, provider)`
- [ ] Implement `Workflow.run(input)` — store input → provider → tool loop → store response → return
- [ ] Implement tool call parsing: "TOOL_CALL:{name}:{params}" → execute → feed back
- [ ] Implement 5-iteration loop limit
- [ ] Handle edge cases: empty provider response, tool not found, loop limit

### T1.7: Update __init__.py exports — depends_on: T1.2, T1.3, T1.4, T1.5, T1.6 (AC-1, AC-2, AC-3, AC-4, AC-5)
- [ ] Export all public classes: `BaseAgent`, `BaseTool`, `ToolRegistry`, `BaseMemory`, `InMemoryMemory`, `BaseProvider`, `MockProvider`, `Workflow`

### T1.8: Basic agent example — depends_on: T1.6, T1.7 (AC-6)
- [ ] Create `examples/basic_agent.py`
- [ ] Define `GreetingTool` that returns "Hello, {name}!"
- [ ] Define `SimpleAgent` that runs single-turn with mock provider
- [ ] Wire up Workflow with mock provider, in-memory memory, one tool
- [ ] Verify `python examples/basic_agent.py` runs without error

### T1.9: Multi-tool example — depends_on: T1.6, T1.7 (AC-6)
- [ ] Create `examples/multi_tool.py`
- [ ] Define 2-3 tools (weather mock, calculator mock, greeting mock)
- [ ] Demonstrate tool call loop with mock provider returning "TOOL_CALL:..."
- [ ] Verify `python examples/multi_tool.py` runs without error

## Traceability Matrix

```
AC-1 (Agent abstraction) → T1.5, T1.7
AC-2 (Tool abstraction)  → T1.2, T1.7
AC-3 (Memory abstraction) → T1.3, T1.7
AC-4 (Provider abstraction) → T1.4, T1.7
AC-5 (Workflow abstraction) → T1.6, T1.7
AC-6 (Examples)          → T1.1, T1.8, T1.9
```
