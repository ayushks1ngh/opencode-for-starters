from datetime import datetime, timezone

from chatbot.models import ToolResult


def execute(args: dict) -> ToolResult:
    fmt = args.get("format", "iso")
    now = datetime.now(timezone.utc)
    if fmt == "iso":
        return ToolResult(success=True, output=now.isoformat())
    elif fmt == "unix":
        return ToolResult(success=True, output=str(int(now.timestamp())))
    elif fmt == "readable":
        return ToolResult(success=True, output=now.strftime("%Y-%m-%d %H:%M:%S UTC"))
    else:
        return ToolResult(success=False, error=f"Unknown format: {fmt}. Supported: iso, unix, readable")


name = "current_time"
description = "Get the current date and time in various formats."
parameters = {
    "type": "object",
    "properties": {
        "format": {
            "type": "string",
            "enum": ["iso", "unix", "readable"],
            "description": "Output format: iso (default), unix timestamp, or readable text",
        }
    },
}
