import json
import os
import urllib.error
import urllib.request
from typing import Optional

from chatbot.models import LLMResponse, Message
from chatbot import retry_handler


class LLMProvider:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Provide api_key or set OPENAI_API_KEY environment variable.")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.max_retries = int(os.environ.get("CHATBOT_MAX_RETRIES", "3"))
        self.retry_delay = float(os.environ.get("CHATBOT_RETRY_DELAY", "2.0"))

    def chat(self, messages: list[Message], tools: list[dict] | None = None) -> LLMResponse:
        if not messages:
            return LLMResponse(error="messages list is empty", finish_reason="error")

        body = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "max_tokens": 1024,
        }

        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"

        try:
            response = retry_handler.execute(
                lambda: self._call_api(body),
                max_retries=self.max_retries,
                delay=self.retry_delay,
            )
            return self._parse_response(response)
        except retry_handler.RetryExhaustedError as e:
            return LLMResponse(error=str(e), finish_reason="error")
        except ValueError as e:
            return LLMResponse(error=str(e), finish_reason="error")

    def _call_api(self, body: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30.0) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            status = e.code
            body_text = e.read().decode()[:200]
            if status == 401:
                raise ValueError("Authentication failed: check your API key")
            if status == 429:
                raise TimeoutError("Rate limited (429)")
            if status >= 500:
                raise ConnectionError(f"Server error ({status}): {body_text}")
            raise ConnectionError(f"API error ({status}): {body_text}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Connection error: {e.reason}")

    def _parse_response(self, data: dict) -> LLMResponse:
        choices = data.get("choices", [])
        if not choices:
            return LLMResponse(error="no choices in response", finish_reason="error")

        choice = choices[0]
        message = choice.get("message", {})
        finish_reason = choice.get("finish_reason", "stop")

        if finish_reason == "tool_calls":
            tool_calls = []
            for tc in message.get("tool_calls", []):
                tool_calls.append({
                    "id": tc.get("id", ""),
                    "type": "function",
                    "function": {
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"],
                    },
                })
            return LLMResponse(tool_calls=tool_calls, finish_reason="tool_calls")

        text = message.get("content", "")
        return LLMResponse(text=text, finish_reason=finish_reason)

    def list_models(self) -> list[str]:
        return [self.model]
