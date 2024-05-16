from typing import Callable
from traceback import format_exc
from ..logger import Logger


def error_boundary(func: Callable, logger: Logger):
    try:
        func()
    except Exception as e:
        for line in format_exc().split("\n"):
            logger.debug(line)
        for line in str(e).split("\n"):
            logger.error(line)
        exit(1)
