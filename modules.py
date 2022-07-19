from abc import ABC, abstractmethod


class Module(ABC):
    # TODO: Use an observer to detect its subclasses?
    @abstractmethod
    def __init__(self, g):
        self.g = g

    @abstractmethod
    def identify(self) -> bool:
        pass

    @abstractmethod
    def calculate(self):
        pass