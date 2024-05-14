#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

import functools
import logging
from inspect import getcallargs
from typing import Callable

__all__ = ["do_logging", "log_this_function"]


def do_logging(
    message: str, logger: logging.Logger, level: int = logging.DEBUG
) -> None:
    """Function to handle calls to a logger.

    Checks to see if logging is allowed at the specified `level` before attemping to log.

    Args:
        message: message to log.
        logger: logger to use when logging the message.
        level: level at which the log should be made. Default: WARNING.
    """
    if logger.isEnabledFor(level):
        logger.log(level, message)


def log_this_function(logger: logging.Logger, level: int = logging.INFO) -> Callable:
    """Decorator to log function calls.

    Args:
        logger: Logger to use when performing the log.
        level: Logging level to use. Default: logging.WARNING

    Returns:
        Decorated function.
    """

    def inner(func: Callable):
        """Extra level of indirection to allow passing parameter to the decorator.
        Args:
            func: Function that is being decorated.

        Returns:
            Wrapping function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # print(inspect.currentframe().f_code)
            # print(dir(inspect.currentframe()))
            params = ", ".join(
                (
                    f"{k}: {str(type(v))[8:-2]} = {v}" if k != "self" else "self"
                    for k, v in getcallargs(func, *args, **kwargs).items()
                )
            )
            message = f"Function call: {func.__name__}({params})"
            do_logging(message, logger, level)
            # logger.log(level, message)  # can use do_logging here
            return func(*args, **kwargs)

        return wrapper

    return inner
