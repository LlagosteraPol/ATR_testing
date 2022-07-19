from modules import Module
import networkx as nx

class ModuleCycle(Module):

    def __init__(self, g):
        self.g = g

    def identify(self):
        return nx.is_k_regular(self.g, 2)

    def calculate(self):
        pass