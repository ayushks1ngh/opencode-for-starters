from chatbot.models import ToolDef, ToolResult
from chatbot.tools import calculator, current_time


_tools: dict[str, dict] = {}


def register(module: object) -> None:
    _tools[module.name] = {
        "name": module.name,
        "description": module.description,
        "parameters": module.parameters,
        "execute": module.execute,
    }


def register_builtins():
    register(calculator)
    register(current_time)


def execute(tool_name: str, args: dict) -> ToolResult:
    if tool_name not in _tools:
        return ToolResult(success=False, error=f"Unknown tool: '{tool_name}'")
    tool = _tools[tool_name]
    try:
        return tool["execute"](args)
    except Exception as e:
        return ToolResult(success=False, error=f"Tool execution error: {e}")


def list_tools() -> list[ToolDef]:
    return [ToolDef(name=t["name"], description=t["description"], parameters=t["parameters"]) for t in _tools.values()]


def get_tool_defs() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            },
        }
        for t in _tools.values()
    ]
