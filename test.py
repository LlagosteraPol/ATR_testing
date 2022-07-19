import matplotlib.pyplot as plt
import math
import networkx as nx
import sympy
import time

import graphtools

from module_cake import ModuleCake
from atr import Atr

g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1), (1, 5), (2, 6), (3, 7), (4, 8)])
g2 = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), (1, 5), (2, 6), (3, 7)])

mc = ModuleCake(g)

print(mc.identify())

start = time.time()
poly1 = mc.calculate()
end = time.time()
print(poly1)
print('CK alg. elapsed time:', end - start)


atr_obj = Atr([1])

start = time.time()
poly2 = atr_obj.relpoly_binary_improved(g)
end = time.time()
print(graphtools.polynomial2binomial(poly2))
print('DC basic elapsed time:', end - start)
