import networkx as nx
import sympy
import sys
from random import choice
# Local Libraries
import graphtools
from selector import EdgeSelector
from relmodules import *


def calculate_reliability(g, modules=[], prune=False, edge_selector = 'select_random'):
    """
    This is the improved contraction-deletion algorithm. In each recursion, all the activated modules will analyze if
    the graph (or sub-graph if it's not the first iteration) can be calculated by them, if so will retrieve the
    reliability and stop the recursion in that generated sub-graph. If cannot be identified by any modules, a normal
    iteration of the contraction-deletion algorithm will be performed.
    :param g: networkx graph
    :param modules: list of the class name modules desired to be activated in order to calculate the reliability
    :param prune: boolean, True to separate the tree parts in the graph
    :param edge_selector: name of the function from the class EdgeSelector which will be used to select the edge for the
    contraction/deletion algorithm.
    :return: the reliability Polynomial of the given graph.
    """
    # print("---------Input graph-----")
    p = sympy.symbols('p')
    polynomial = 1
    g = nx.MultiGraph(g) # Since DC needs a graph defined as multigraph to work (ex. when edge contraction)

    # If the graph is not connected, then it has a rel poly of 0
    if not nx.is_connected(g):
        return sympy.Poly(0, p)

    # If we only have 0 edges and 1 vertex, is connected, so we return 1.
    elif len(g.edges()) == 0:
        return sympy.Poly(1, p)

    # Else, separate the graph into subgraphs
    else:
        # Encapsulate the given graph with a list
        if not isinstance(g, list):
            g_lst = [g]

        if prune:
            subgraphs = graphtools.prune_graph(g_lst[0])
            g_lst = subgraphs['trees'] + subgraphs['cycles']

        for gi in g_lst:
            graph_identified = False
            for module in modules:
                obj = getattr(sys.modules[__name__], module)(g)
                graph_identified = obj.identify()
                if graph_identified:
                    polynomial *= obj.calculate()
                    break

            if not graph_identified:
                # if other type, then we perform the two subcases of the Factoring theorem.
                # Look for joined cycles, to optimize the choosed edge
                select_edge = getattr(EdgeSelector(gi), edge_selector)
                e = select_edge()

                contracted = nx.contracted_edge(gi, e, self_loops=False)  # TODO: Expected tuple

                gi.remove_edge(*e)
                # AdjMaBox.plot(other)
                rec_deleted = calculate_reliability(gi, modules, prune)
                # AdjMaBox.plot(contracted)

                rec_contracted = calculate_reliability(contracted, modules, prune)

                polynomial *= sympy.Poly(p) * rec_contracted + sympy.Poly(1 - p) * rec_deleted

    return polynomial
