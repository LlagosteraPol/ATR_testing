import networkx as nx
import time
import sys

import atr
import graphtools

#from relmodules.reliability_modules import RelModule
#from relmodules.module_tree import ModuleTree
#from relmodules.module_cycle import ModuleCycle
#from relmodules.module_cake import ModuleCake
from relmodules.module_cycletree import ModuleCycleTree

import relmodules

from atr import calculate_reliability

def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


# pass base class as argument
print(get_all_subclasses(relmodules.RelModule))
"""
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
print('Total number of multiedges = ', graphtools.get_total_multiedge_number(g_tree))
print('Multiedges = ', graphtools.get_multiedge_number(g_tree))

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
"""

# Testing cake module:
#g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (3, 5)])

#ct = getattr(sys.modules[__name__], 'ModuleCake')(g)

#print(ct.identify())

"""
#Testing cycleTree module
g1 = nx.MultiGraph([(1, 2), (2, 3), (3, 1), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)])
g2 = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (3, 7), (7, 8), (8, 9), (9, 3), (9, 10), (10, 11), (9, 11)])


poly1 = atr.calculate_reliability(g2)
bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
print(graphtools.polynomial2binomial(poly1))

cycletreemodule = ModuleCycleTree(g2)
if cycletreemodule.identify():
    poly2 = cycletreemodule.calculate()
    bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
    print(graphtools.polynomial2binomial(poly2))
"""
"""
#Graph6 test
g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
nx.write_graph6(g, "test.txt", header=False)
g = nx.read_graph6("test.txt")
"""
"""
#Basic ATR test
print('-------------------------Test ATR-------------------------')
g = nx.MultiGraph( [(1,2), (1,2), (1,3), (2,3), (2,3), (2,3),
                    (3,4), (4,5), (4,5), (5,6), (5,6), (5,6), (6,7),
                    (7,8), (8,9), (9,10), (10,11), (11,12), (12,7),
                    (8,11), (9,12)] )

start = time.time()
poly1 = atr.calculate_reliability(g)
end = time.time()
bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
print('DC basic elapsed time:', end - start)

start = time.time()
poly2 = atr.calculate_reliability(g, modules=['ModuleTree','ModuleCycle', 'ModuleCycleTree', 'ModuleCake'])
end = time.time()
bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
print('Dc all Modules time:', end - start)

start = time.time()
poly3 = atr.calculate_reliability(g, prune=True, modules=['ModuleTree', 'ModuleCycle', 'ModuleCake'])
end = time.time()
bin_poly3, bin_coeff3 = graphtools.polynomial2binomial(poly3)
print('Dc specific with prunning time:', end - start)

print(bin_poly1)
print(bin_poly2)
print(bin_poly3)
"""

# Testing ModuleCake

#g = nx.Graph([(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (11,1), (3,8), (5,10), (6,11)])
#g  = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), (1, 5), (2, 6), (3, 7)])
g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1), (1, 5), (2, 6), (3, 7), (4, 8)])

cakemodule = relmodules.ModuleCake(g)

start = time.time()
poly1 = atr.calculate_reliability(g)
end = time.time()
bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
print('DC basic elapsed time:', end - start)
print(bin_poly1)

start = time.time()
poly2 = cakemodule.calculate()
end = time.time()
bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
print('Cake alg. elapsed time:', end - start)
print(bin_poly2)
