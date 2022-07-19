import copy
import networkx as nx


def prune_graph(g):
    """
    Extract the tree parts of the given network.
    :param g: networkx graph.
    :return: <dict> {'trees': induced tree sub-graphs, 'cycles': induced cycle sub-graphs}.
    """
    g = nx.Graph(g)  # Turns the graph into simple undirected graph
    g_copy = copy.deepcopy(g)

    # Get the cycle basis of the given graph
    cycle_basis = nx.cycle_basis(g)

    # Turns each cycle into a networkx graph
    induced_edges = list()
    for induced in cycle_basis:
        induced_edges += list(nx.induced_subgraph(g, induced).edges())

    # Remove all cycles from the graph copy
    g_copy.remove_edges_from(induced_edges)
    g_copy.remove_nodes_from(list(nx.isolates(g_copy)))

    # Remove all the tree parts from the original graph
    g.remove_edges_from(g_copy.edges())
    g.remove_nodes_from(list(nx.isolates(g)))

    # Return a list of trees and cycles (that forms the given graph)
    return [{'trees': [g_copy.subgraph(c).copy() for c in nx.connected_components(g_copy)]},
            {'cycles': [g.subgraph(c).copy() for c in nx.connected_components(g)]}]

def get_edge_degree(g):
    """
    Give the 'degree' of each edge as a sum of the degrees of constituting nodes.
    :param g: networkx graph.
    :return: <dict> {edge:degree}
    """
    edge_degree = {}
    for e in g.edges:
        edge_degree[e] = g.degree(e[0]) + g.degree(e[1])
    return edge_degree