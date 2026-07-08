import logging
import time
from typing import Callable

logger = logging.getLogger(__name__)


class RetryExhaustedError(Exception):
    pass


def is_retryable(error: Exception) -> bool:
    if isinstance(error, RetryExhaustedError):
        return False
    if isinstance(error, (TimeoutError, ConnectionError)):
        return True
    msg = str(error).lower()
    if "429" in msg or "rate limit" in msg:
        return True
    if "5" in msg and any(code in msg for code in ["50", "502", "503", "504"]):
        return True
    if "connection" in msg or "timeout" in msg:
        return True
    return False


def execute(callable_fn: Callable, max_retries: int = 3, delay: float = 2.0) -> any:
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return callable_fn()
        except Exception as e:
            last_error = e
            if not is_retryable(e):
                raise
            if attempt < max_retries:
                logger.debug("Attempt %d failed: %s. Retrying in %.1fs...", attempt + 1, e, delay)
                time.sleep(delay)
            else:
                logger.debug("All %d retries exhausted for: %s", max_retries, e)
    raise RetryExhaustedError(f"Failed after {max_retries} retries: {last_error}") from last_error
