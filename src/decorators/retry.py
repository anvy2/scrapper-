import asyncio
import functools
import logging
from typing import Type, Union, Tuple

logger = logging.getLogger(__name__)


def retry_async(
    max_tries: int = 3,
    delay: float = 1.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
):
    """
    Retry decorator for async functions.

    Args:
        max_tries: Maximum number of attempts
        delay: Initial delay between retries in seconds
        exceptions: Exception(s) that trigger a retry attempt
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tries = 0
            current_delay = delay

            while True:
                tries += 1
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if tries >= max_tries:
                        logger.error(
                            f"Function {func.__name__} failed after {tries} tries: {str(e)}"
                        )
                        raise e

                    logger.warning(
                        f"Attempt {tries}/{max_tries} for {func.__name__} failed: {str(e)}. "
                        f"Retrying in {current_delay} seconds..."
                    )

                    await asyncio.sleep(current_delay)

        return wrapper

    return decorator


def retry_sync(
    max_tries: int = 3,
    delay: float = 1.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
):
    """
    Retry decorator for synchronous functions.

    Args:
        max_tries: Maximum number of attempts
        delay: Initial delay between retries in seconds
        exceptions: Exception(s) that trigger a retry attempt
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time

            tries = 0
            current_delay = delay

            while True:
                tries += 1
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries >= max_tries:
                        logger.error(
                            f"Function {func.__name__} failed after {tries} tries: {str(e)}"
                        )
                        raise e

                    logger.warning(
                        f"Attempt {tries}/{max_tries} for {func.__name__} failed: {str(e)}. "
                        f"Retrying in {current_delay} seconds..."
                    )

                    time.sleep(current_delay)

        return wrapper

    return decorator


__all__ = ["retry_async", "retry_sync"]
