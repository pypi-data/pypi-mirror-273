import abc
from ...component import Component
from ..scheme import Scheme


class SchemeFactory(Component, metaclass=abc.ABCMeta):
    name: str

    @abc.abstractmethod
    def create(self, config: dict) -> Scheme:
        raise NotImplementedError
