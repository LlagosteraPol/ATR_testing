import networkx as nx
import time
import sys

import graphtools

#from modules.reliability_modules import Module
#from modules.module_tree import ModuleTree
#from modules.module_cycle import ModuleCycle
#from modules.module_cake import ModuleCake

from modules import *

from atr import calculate_reliability




def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


# pass base class as argument
print(get_all_subclasses(RelModule))

print('Cake graph:')
g_cake = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1), (1, 5), (2, 6), (3, 7), (4, 8)])
print(g_cake)
mc = getattr(sys.modules[__name__], 'ModuleCake')(g_cake)
mc.identify()
print('Is cake?',mc.identify())
print(graphtools.polynomial2binomial(mc.calculate()))

poly = calculate_reliability(g_cake, prune=False)
print(graphtools.polynomial2binomial(poly))


print('Multi Tree:')
g_tree = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (5, 8), (5, 9), (5, 9)])
print(g_tree)
mt = getattr(sys.modules[__name__], 'ModuleTree')(g_tree)
print('Is a tree?', mt.identify())
print('Reliability:')
print(graphtools.polynomial2binomial(mt.calculate()))

poly = calculate_reliability(g_tree, prune=False)
print(graphtools.polynomial2binomial(poly))


print('Multi graph tree+cycles:')
gs = nx.MultiGraph([(1,2), (1,2), (2,3), (2,4), (3,4), (3,4),(4,5),(5,6),(5,7),(6,7)])
print(gs)
#print('Pruned components:')
#graphs = graphtools.prune_graph(gs)
#g_lst = graphs['trees'] + graphs['cycles']
#for graph in g_lst:
#    print(graph)
print('Reliability:')
poly = calculate_reliability(gs, prune=True)
print(graphtools.polynomial2binomial(poly))

poly = calculate_reliability(gs, prune=False)
print(graphtools.polynomial2binomial(poly))
