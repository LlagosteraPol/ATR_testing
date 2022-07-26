import copy
import networkx as nx
import numpy as np
import sympy

from math import factorial

def prune_graph(g):
    """
    Extract the tree parts of the given network.
    :param g: networkx graph.
    :return: <dict> {'trees': induced tree sub-graphs, 'cycles': cycle sub-graphs}.
    """

    g_copy = copy.deepcopy(g)
    g_copy = nx.Graph(g_copy) # Turns the graph into simple undirected graph

    # Get the cycle basis of the given graph
    cycle_basis = nx.cycle_basis(g_copy)

    # Turns each cycle into a networkx graph
    induced_edges = list()
    for induced in cycle_basis:
        induced_edges += list(nx.induced_subgraph(g, induced).edges())

    # Remove all cycles from the graph copy
    g_trees = copy.deepcopy(g)
    for edge in induced_edges:
        g_trees.remove_edges_from([edge] * g.number_of_edges(edge[0], edge[1]))
    g_trees.remove_nodes_from(list(nx.isolates(g_trees)))

    # Remove all the tree parts from the original graph
    g_cycles = copy.deepcopy(g)
    g_cycles.remove_edges_from(g_trees.edges())
    g_cycles.remove_nodes_from(list(nx.isolates(g_cycles)))

    # Return a list of trees and cycles (that forms the given graph)
    return {'trees': [g_trees.subgraph(c).copy() for c in nx.connected_components(g_trees)],
            'cycles': [g_cycles.subgraph(c).copy() for c in nx.connected_components(g_cycles)]}


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


def number_combination(n, k):
    """
    Determines how many combinations can be done.
    :param n: Number of elements.
    :param k: Number of elements to combine.
    :return: Number of combinations with the given specifications.
    """
    if k < 0:
        return 0

    return factorial(n) / factorial(k) / factorial(n - k)


def polynomial2binomial(polynomial):
    """
    This method transforms the given polynomial to its binomial form.
    :param polynomial: Polynomial to convert to binomial form
    :return: Binomial Polynomial, coefficients
    """
    p = sympy.symbols('p')

    # Assuring that the given polynomial is in the right class
    if type(polynomial) is not sympy.polys.polytools.Poly:
        polynomial = sympy.poly(polynomial)

    binomial = 0
    degree = sympy.degree(polynomial, p)

    # Get coefficients (and round the ones really close to 0)
    coefficients = refine_polynomial_coefficients(polynomial)
    coefficients = np.trim_zeros(coefficients)  # Delete all right zeroes
    n_coeff = len(coefficients)

    # Get binomial coefficients
    aux = n_coeff
    aux_degree = degree
    for i in range(1, n_coeff):
        coeff2expand = coefficients[-i]
        expanded = sympy.Poly(coeff2expand * p ** (aux_degree - n_coeff + 1) * (1 - p) ** (aux - 1))
        tmp_coefficients = expanded.all_coeffs()
        tmp_coefficients = np.trim_zeros(tmp_coefficients)
        tmp_n_coeff = len(tmp_coefficients)

        for z in range(2, tmp_n_coeff + 1):
            coefficients[(-z - (n_coeff - tmp_n_coeff))] -= tmp_coefficients[-z]

        aux -= 1
        aux_degree += 1

    # Assemble binomial polynomial
    aux_degree = degree
    for coeff in coefficients:
        binomial += coeff * p ** aux_degree * (1 - p) ** (degree - aux_degree)
        aux_degree -= 1

    return binomial, coefficients


def coefficients2polynomial(coefficients, size):
    """
    This method transforms the given coefficients to its reliability polynomial.
    :param coefficients: coefficients of the reliability polynomial
    :return: Polynomial
    """
    p = sympy.symbols('p')

    count = 0
    polynomial = 0
    for coeff in coefficients:
        polynomial += coeff*p**(size-count)*(1-p)**count
        count += 1

    return sympy.poly(polynomial)


def refine_polynomial_coefficients(polynomial):
    """
    This method will round the coefficients of the polynomial that are almost zero (ex. at the order of e-10).
    When calculating Rel(G,p), if some of the coefficients are like this maybe is due to noise when calculating
    large amounts reliabilities with big polynomials.
    :param polynomial: polynomial to refine
    :return: refined polynomial
    """
    coefficients = polynomial.all_coeffs()

    refined_coefficients = list()
    for coefficient in coefficients:
        refined_coefficients.append(round(coefficient, 0))

    return refined_coefficients


def get_multiedge_number(g):
    """
    This method retrieves the number of multi-links between each pair of adjacent nodes.
    :param g: networkx graph
    :return: a dictionary {edge: number} and a boolean set to True if all pair of adjacent nodes has the same amount of
    edges connecting them (False otherwise).
    """
    edge_dict = {}
    for edge in nx.Graph(g).edges():
        edge_dict[edge] = g.number_of_edges(edge[0], edge[1])

    balanced = True
    if max(edge_dict.values()) != min(edge_dict.values()):
        balanced = False

    return edge_dict, balanced


def get_total_multiedge_number(g):
    """
    Gives the total number of multiedges of the given graph.
    :param g: networkx graph
    :return: total number of multiedges
    """
    arr = nx.to_numpy_matrix(g)
    num_multiedges = np.sum(arr >= 2) / 2
    return num_multiedges


def get_all_subclasses(cls):
    """
    Method that retrieves the name of the sub-classes (if any) of the given class.
    :param cls: name of the class to know if has subclasses
    :return: a list with all the sub-class names (in string format)
    """
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses
