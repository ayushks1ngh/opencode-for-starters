import json
import logging

from chatbot.models import Message, LLMResponse
from chatbot.llm_provider import LLMProvider
from chatbot.tool_registry import execute as execute_tool, get_tool_defs

logger = logging.getLogger(__name__)
MAX_TOOL_CALLS_PER_TURN = 5


class Orchestrator:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def run(self, user_message: str, history: list[Message]) -> str:
        if not user_message or not user_message.strip():
            return "Message cannot be empty."

        messages = list(history)
        messages.append(Message(role="user", content=user_message.strip()[:4096]))

        tools = get_tool_defs()
        tool_call_count = 0

        while tool_call_count < MAX_TOOL_CALLS_PER_TURN:
            response = self.provider.chat(messages, tools if tools else None)

            if response.error:
                return f"Error: {response.error}"

            if response.finish_reason == "tool_calls" and response.tool_calls:
                for tc in response.tool_calls:
                    tool_call_count += 1
                    fn = tc.get("function", {})
                    name = fn.get("name", "")
                    try:
                        args = json.loads(fn.get("arguments", "{}"))
                    except json.JSONDecodeError:
                        args = {}

                    logger.debug("Tool call %d/%d: %s(%s)", tool_call_count, MAX_TOOL_CALLS_PER_TURN, name, args)

                    result = execute_tool(name, args)
                    result_text = result.output if result.success else f"Error: {result.error}"

                    messages.append(Message(role="assistant", content="", timestamp=""))
                    messages.append(Message(role="tool", content=json.dumps({"tool": name, "result": result_text})))
                continue

            if response.text is not None:
                return response.text

            return "I received an unexpected response from the AI."

        return "I've used too many tools for this request. Please try a simpler question."
