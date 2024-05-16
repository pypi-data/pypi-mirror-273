import abc
from ...component import Component
from ldm.logger import Logger


class Scheme(Component, metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        *,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(logger)
        self.name = name

    @abc.abstractmethod
    def install(self, entry: str) -> None:
        raise NotImplementedError
