import networkx as nx
from random import choice

import graphtools


class EdgeSelector:

    def __init__(self, g):
        self.g = g

    def select_random(self):
        """
        Select a random edge from the graph
        :return: random edge
        """
        return choice(list(self.g.edges()))

    def select_min_degree(self):
        """
        Select the edge with minimum degree (sum of its endpoint nodes degree)
        :return: edge with minimum degree (sum of its endpoint nodes degree)
        """
        edge_degrees = graphtools.get_edge_degree(self.g)
        return min(edge_degrees, key=edge_degrees.get)[0:2]

    def select_max_degree(self):
        """
        Select the edge with maximum degree (sum of its endpoint nodes degree)
        :return: edge with maximum degree (sum of its endpoint nodes degree)
        """
        edge_degrees = graphtools.get_edge_degree(self.g)
        return max(edge_degrees, key=edge_degrees.get)[0:2]