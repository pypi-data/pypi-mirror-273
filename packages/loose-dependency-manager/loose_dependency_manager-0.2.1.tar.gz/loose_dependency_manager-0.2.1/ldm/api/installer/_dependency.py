from typing import Callable
from ldm.logger import Logger
from ...component import Component


class Dependency(Component):
    def __init__(
        self,
        name: str,
        install: Callable[[], None],
        *,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(logger)
        self.name = name
        self.install = install
