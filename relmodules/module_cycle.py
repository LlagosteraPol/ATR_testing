from relmodules.reliability_modules import RelModule

import itertools as itt
import networkx as nx
import sympy

import graphtools


class ModuleCycle(RelModule):

    def __init__(self, g):
        self.g = g

    def identify(self):
        """
        Identifies the graph if its a simple cycle or multi-cycle
        :return: True if the given graph is a simple cycle or multi-cycle, False otherwise
        """
        return nx.is_k_regular(nx.Graph(self.g), 2)

    def calculate(self):
        """
        Get the polynomial reliability of any cycle (multiedge or not)
        :return: Reliability polynomial of the graph
        """
        p = sympy.symbols('p')
        polynomial = 0
        cycle_edges, balanced = graphtools.get_multiedge_number(self.g)

        # Specialized inclusion-exclusion formula for multicycles with balanced parallel edges
        if balanced:
            len_pedges = len(cycle_edges)
            p_ed = list(cycle_edges.values())[0]  # Number of parallel edges in each set of parallel edges

            for i in range(2, len_pedges + 1):
                nci = graphtools.number_combination(len_pedges, i)
                polynomial += (-1) ** i * nci * (i - 1) * (1 - p) ** (p_ed * i)

            polynomial = 1 - polynomial

        # Inclusion-exclusion formula
        else:
            part = 0
            tmp = 0

            for i in range(2, len(cycle_edges) + 1):
                for subset in itt.combinations(cycle_edges, i):
                    exp = 0
                    for element in subset:
                        exp += cycle_edges[element]
                    tmp += (1 - p) ** exp
                part += (-1) ** i * (i - 1) * tmp
                tmp = 0

            polynomial = 1 - part

            # if polynomial == 2*(-p + 1)**3 - 3*(-p + 1)**2 + 1:  # TODO: Debug test
            #   debug = 1

        # return sympy.Poly(polynomial)  # TODO: Check if also works properly
        return polynomial