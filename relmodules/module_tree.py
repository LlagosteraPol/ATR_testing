from relmodules.reliability_modules import RelModule

import networkx as nx
import sympy

import graphtools


class ModuleTree(RelModule):

    def __init__(self, g):
        self.g = g

    def identify(self):
        """
        Identifies the graph if its a tree or multi-tree
        :return: True if the given graph is a tree or multi-tree, False otherwise
        """
        return nx.is_tree(nx.Graph(self.g))

    def calculate(self):
        """
        Get the polynomial reliability of any tree (multiedge or not)
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