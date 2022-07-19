import networkx as nx
import sympy
from random import choice

class Atr(object):
    modules = []

    # default constructor
    def __init__(self, modules):
        self.modules = modules

    def relpoly_binary_improved(self, g):
        """
        This is the improved contraction-deletion algorithm. In each recursion, if there exist some method
        that can retrieve the Reliability Polynomial directly or with less cost than another recursion,
        will retrieve it and stop the recursion in that generated sub-graph.
        :param g: networkx graph
        :return: the reliability Polynomial of the given graph or another execution of the method.
        """
        # print("---------Input graph-----")
        # AdjMaBox.plot(g)
        p = sympy.symbols('p')
        polynomial = 1
        g = nx.MultiGraph(g)

        """
        # If the graph is k > 2 regular, proceed with contraction-deletion
        elif nx.is_distance_regular(g) and g.degree(choice(g.nodes())) > 2:
            for other in type[1]:
                # if other type, then we perform the two subcases of the Factoring theorem.
                # Look for joined cycles, to optimize the choosed edge
                # common_edge = GraphTools.get_a_common_edge(other)

                # e = copy.deepcopy(common_edge)
                e = choice(list(other.edges()))

                contracted = nx.contracted_edge(other, e, self_loops=False)  # TODO: Expected tuple

                other.remove_edge(*e)
                # AdjMaBox.plot(other)
                rec_deleted = GraphRel.__recursive_improved(other)
                # AdjMaBox.plot(contracted)

                rec_contracted = GraphRel.__recursive_improved(contracted)

                polynomial *= sympy.Poly(p) * rec_contracted + sympy.Poly(1 - p) * rec_deleted
        """

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

            for gi in g_lst:
                # if other type, then we perform the two subcases of the Factoring theorem.
                # Look for joined cycles, to optimize the choosed edge

                # TODO: The function .get_a_common_edge doesn't work due a maltfunction of the networkx function minimum_cycle_basis
                # common_edge = GraphTools.get_a_common_edge(other) # Not working for ordered cycles
                # e = copy.deepcopy(common_edge)

                # TODO: Needs opitmization
                e = choice(list(gi.edges()))  # Random choice

                contracted = nx.contracted_edge(gi, e, self_loops=False)  # TODO: Expected tuple

                gi.remove_edge(*e)
                # AdjMaBox.plot(other)
                rec_deleted = self.relpoly_binary_improved(gi)
                # AdjMaBox.plot(contracted)

                rec_contracted = self.relpoly_binary_improved(contracted)

                polynomial *= sympy.Poly(p) * rec_contracted + sympy.Poly(1 - p) * rec_deleted

        return polynomial



"""
    subgraphs = GraphTools.get_sub_graphs(g, False if filter_depth == 0 else True)

    for g_type in subgraphs:

        if g_type[0] == GraphType.Tree and g_type[1] != {}:
            # TODO: Check if we can obtain the balancing flag
            polynomial *= GraphRel.relpoly_multitree((False, -1), g_type[1])

        elif g_type[0] == GraphType.PureCycle and g_type[1] != list():
            for pure_cycle in g_type[1]:
                # Get information about the cycle/multicycle
                mcy_bal_pedges, mcy_tree_edges, mcy_cycle_edges, mcy_total_edges = GraphTools.get_detailed_graph_edges(
                    pure_cycle)
                polynomial *= GraphRel.relpoly_multicycle(mcy_bal_pedges,
                                                          mcy_cycle_edges[0])  # [0] to select the first (and only) cycle

        elif g_type[0] == GraphType.OrderedCycles and g_type[1] != list():
            for ordered_cycles in g_type[1]:
                # Get information about the graph
                ocy_bal_pedges, ocy_tree_edges, ocy_cycle_edges, ocy_total_edges = \
                    GraphTools.get_detailed_graph_edges(ordered_cycles)
                polynomial *= GraphRel.relpoly_ordered_cycles(ordered_cycles, ocy_cycle_edges)

        elif g_type[0] == GraphType.Others and g_type[1] != list():
            if filter_depth > 0:
                filter_depth -= 1  # Depth control

            for other in g_type[1]:
                # if other type, then we perform the two subcases of the Factoring theorem.
                # Look for joined cycles, to optimize the choosed edge

                # TODO: The function .get_a_common_edge doesn't work due a maltfunction of the networkx function minimum_cycle_basis
                # common_edge = GraphTools.get_a_common_edge(other) # Not working for ordered cycles
                # e = copy.deepcopy(common_edge)

                # TODO: Needs opitmization
                e = choice(list(other.edges()))  # Random choice

                contracted = nx.contracted_edge(other, e, self_loops=False)  # TODO: Expected tuple

                other.remove_edge(*e)
                # AdjMaBox.plot(other)
                rec_deleted = self.relpoly_binary_improved(other, filter_depth)
                # AdjMaBox.plot(contracted)

                rec_contracted = self.relpoly_binary_improved(contracted, filter_depth)

                polynomial *= sympy.Poly(p) * rec_contracted + sympy.Poly(1 - p) * rec_deleted

return polynomial 
"""
