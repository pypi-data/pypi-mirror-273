import abc
from ..component import Component
from ..logger import Logger, ClickLogger


class Command(Component, metaclass=abc.ABCMeta):
    def __init__(
        self,
        *,
        logger: Logger = ClickLogger(),
    ):
        super().__init__(logger=logger)

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
