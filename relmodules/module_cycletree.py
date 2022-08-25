from relmodules.reliability_modules import RelModule
from relmodules.module_cycle import ModuleCycle

import itertools as itt
import networkx as nx
import sympy

import graphtools


class ModuleCycleTree(RelModule):

    def __init__(self, g):
        self.g = g
        self.cycles = nx.cycle_basis(nx.Graph(self.g))

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

        if graphtools.get_total_multiedge_number(self.g) == 0:
            return self.simple_treecyc()

        else:
            for cycle in self.cycles:
                tmp_g = self.g.subgraph(cycle).copy()
                polynomial *= ModuleCycle(tmp_g).calculate()
            return polynomial

    def simple_treecyc(self):
        """
        Get the Reliability Polynomial of a tree+cycles graph shape (no multiedge).
        :return: reliability polynomial
        """
        p = sympy.symbols('p')

        n_edges = len(self.g.edges)
        polynomial = 0

        # Broken edges >1
        for i in range(0, len(self.cycles) + 1):
            result = 0

            for subset in itt.combinations(self.cycles, i):
                oper = 1
                for cycle in subset:
                    oper *= len(cycle)
                result += oper
            polynomial += result * p ** n_edges * (1 - p) ** i
            n_edges -= 1

        return polynomial
