from abc import ABC, abstractmethod


class Module(ABC):

    @abstractmethod
    def __init__(self, g):
        self.g = g

    @abstractmethod
    def identify(self) -> bool:
        pass

    @abstractmethod
    def calculate(self):
        pass