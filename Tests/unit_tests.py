import unittest

import networkx as nx
import time

import graphtools

from atr import Atr
from modules.module_tree import RelModuleTree
from modules.module_cycle import RelModuleCycle
from modules.module_cake import RelModuleCake


class TestAtr(unittest.TestCase):

    def setUp(self):
        self.g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1),
                                (1, 2), (3, 4), (7, 8), (7, 8)])
        self.atr = Atr(self.g)

class TestModuleTree(unittest.TestCase):

    def setUp(self):
        self.g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (5, 8), (5, 9), (5, 9)])
        self.treemodule = RelModuleTree(self.g)

    def testModule(self):
        self.assertTrue(self.treemodule.identify(), "MultiTree not properly identified")
        with self.subTest():
            print('---------------------------------------------------')
            atr_obj = Atr([1])

            start = time.time()
            poly1 = atr_obj.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            poly2 = self.treemodule.calculate()
            end = time.time()
            bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('Tree alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")


class TestModuleCycle(unittest.TestCase):

    def setUp(self):
        self.g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1),
                                (1, 2), (3, 4), (7, 8), (7, 8)])
        self.cyclemodule = RelModuleCycle(self.g)

    def testModule(self):
        self.assertTrue(self.cyclemodule.identify(), "MultiCycle not properly identified")
        with self.subTest():
            print('---------------------------------------------------')
            atr_obj = Atr([1])

            start = time.time()
            poly1 = atr_obj.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            poly2 = self.cyclemodule.calculate()
            end = time.time()
            bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('Cycle alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")


class TestModuleCake(unittest.TestCase):

    def setUp(self):
        self.g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1), (1, 5), (2, 6), (3, 7), (4, 8)])
        #self.g  = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), (1, 5), (2, 6), (3, 7)])
        self.cakemodule = RelModuleCake(self.g)

    def testModule(self):
        self.assertTrue(self.cakemodule.identify(),  "Cake not properly identified")
        with self.subTest():
            print('---------------------------------------------------')
            atr_obj = Atr([1])

            start = time.time()
            poly1 = atr_obj.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            bin_coeff2 = self.cakemodule.calculate()
            end = time.time()
            #bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('Cake alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")

# run the test
if __name__ == '__main__':
    unittest.main()
