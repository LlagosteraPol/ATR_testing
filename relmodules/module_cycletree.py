from relmodules.reliability_modules import RelModule
from relmodules.module_cycle import ModuleCycle

import networkx as nx
import sympy

import graphtools


class ModuleCycleTree(RelModule):

    def __init__(self, g):
        self.g = g
        self.cycles = nx.cycle_basis(self.g)

    def identify(self):
        """
        Identifies the graph if its a tree of cycles
        :return: True if the given graph is a tree of cycles, False otherwise
        """
        if self.g.order() == self.g.size() - (len(self.cycles) - 1):
            return True
        return False

    def calculate(self):
        """
        Calculates the reliability polynomial coefficients of a CycleTree graph.
        :return: Reliability Polynomial of the given CycleTree graph
        """
        polynomial = 1

        for cycle in self.cycles:
            tmp_g = self.g.subgraph(cycle).copy()
            polynomial *= ModuleCycle(tmp_g).calculate()
        return polynomial
