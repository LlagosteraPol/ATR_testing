from abc import ABC, abstractmethod


class RelModule(ABC):
    @abstractmethod
    def __init__(self, g):
        self.g = g

    @abstractmethod
    def identify(self) -> bool:
        """
        Abstract method to Identify the graph.
        :return: boolean
        """
        pass

    @abstractmethod
    def calculate(self):
        """
        Abstract method to calculate the reliability of the given graph.
        :return: reliability
        """
        pass