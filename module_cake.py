from modules import Module
import networkx as nx

class ModuleCycle(Module):

    def __init__(self, g):
        self.g = g

    def identify(self):
        # If there is at least one node with degree < 2 or > 3, then it's not a cake
        if min(nx.degree(self.g))[1] < 2 or max(nx.degree(self.g))[1] > 3:
            return False

        # If the previous condition is not met but the maximum degree of the nodes of
        # the graph is == 2, then it's a cycle
        if max(nx.degree(self.g))[1] == 2:
            return False



        self.hamilton_cycle(self.g)
        pass

    def calculate(self):
        pass

    def hamilton_cycle(g):
        """
        Finds a hamiltonian cycle using networkx graph library
        :param g: Networkx graph
        :return: Hamiltonian cycle or None if not found
        """
        directed_g = nx.DiGraph(g)
        for cycle in list(nx.simple_cycles(directed_g)):
            if len(cycle) == len(directed_g.nodes):
                return cycle

        return None