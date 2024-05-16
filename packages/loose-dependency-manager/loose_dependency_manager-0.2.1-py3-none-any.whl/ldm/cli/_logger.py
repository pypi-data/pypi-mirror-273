import os
from typing import Callable
from ..logger import Logger, ClickLogger


def get_debug_level() -> int:
    debug = os.environ.get("DEBUG", None)
    return 1 if debug else 2


def create_logger(level: int = get_debug_level()) -> ClickLogger:
    return ClickLogger(level=level)


def error_boundary(func: Callable, logger: Logger):
    try:
        func()
    except Exception as e:
        for line in str(e).split("\n"):
            logger.error(line)
        exit(1)
