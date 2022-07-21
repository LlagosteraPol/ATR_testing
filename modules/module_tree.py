from modules.reliability_modules import RelModule

import networkx as nx
import sympy

import graphtools


class ModuleTree(RelModule):

    def __init__(self, g):
        self.g = g

    def identify(self):
        return nx.is_tree(nx.Graph(self.g))

    def calculate(self):
        """
        Get the polynomial reliability of any tree (multiedge or not)
        :param bal_pedges: <tuple> (bool, int); <bool> if is parallel, <int> number of parallel edges
        :param tree_edges: <list> of the edges of the graph tree
        :return: Reliability polynomial of the graph
        """
        p = sympy.symbols('p')
        tree_edges, balanced = graphtools.get_multiedge_number(self.g)

        # Specialized inclusion-exclusion formula for multitrees with balanced parallel edges
        if balanced:
            p_ed = list(tree_edges.values())[0]  # Number of parallel edges in each set of parallel edges
            return (1 - (1 - p) ** p_ed) ** len(tree_edges)

        # Tree Inclusion-Exclusion formula (chunks formula)
        polynomial = 1
        for edgeset in tree_edges:
            polynomial *= 1 - (1 - p) ** tree_edges[edgeset]

        # return sympy.Poly(polynomial)  # TODO: Check if works
        return polynomial