import abc
from typing import Generic, TypeVar
from ldm.logger import Logger
from ....component import Component
from .._dependency import Dependency

Config = TypeVar("Config")


class InstallStrategy(Component, Generic[Config], metaclass=abc.ABCMeta):
    def __init__(
        self,
        config: Config,
        *,
        logger: Logger | None = None,
    ):
        super().__init__(logger=logger)
        self.config = config

    @abc.abstractmethod
    def install(self, dependencies: list[Dependency]):
        raise NotImplementedError
