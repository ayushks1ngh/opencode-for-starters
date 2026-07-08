import re

from chatbot.models import ToolResult


def validate_expression(expr: str) -> bool:
    return bool(re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expr))


def execute(args: dict) -> ToolResult:
    expression = args.get("expression", "").strip()
    if not expression:
        return ToolResult(success=False, error="No expression provided")
    if not validate_expression(expression):
        return ToolResult(success=False, error=f"Invalid expression: '{expression}' contains disallowed characters")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return ToolResult(success=True, output=str(result))
    except Exception as e:
        return ToolResult(success=False, error=f"Calculation error: {e}")


name = "calculator"
description = "Evaluate a mathematical expression. Supports +, -, *, /, parentheses, and decimal numbers."
parameters = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "string",
            "description": "The mathematical expression to evaluate (e.g. '2 + 2', '(5 * 3) / 2')",
        }
    },
    "required": ["expression"],
}
