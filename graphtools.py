import copy
import networkx as nx


def prune_graph(g):
    # TODO: Write method docu
    """
    Determine the edges of the inner cycles of the given graph 'g'.
    :param g: networkx graph.
    :return: <list> the edges of the inner cylces.
    """
    g = nx.Graph(g)  # Make a no multicycle and non directed graph copy
    g_copy = copy.deepcopy(g)

    cycle_basis = nx.cycle_basis(g)

    induced_edges = list()
    for induced in cycle_basis:
        induced_edges += list(nx.induced_subgraph(g, induced).edges())

    g_copy.remove_edges_from(induced_edges)
    g_copy.remove_nodes_from(list(nx.isolates(g_copy)))

    g.remove_edges_from(g_copy.edges())
    g.remove_nodes_from(list(nx.isolates(g)))

    return [g.subgraph(c).copy() for c in nx.connected_components(g)] + \
           [g_copy.subgraph(c).copy() for c in nx.connected_components(g_copy)]