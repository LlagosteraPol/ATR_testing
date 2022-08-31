import unittest

import networkx as nx
import time

import graphtools

import atr
import relmodules


class TestAtr(unittest.TestCase):

    def setUp(self):
        #self.g = nx.MultiGraph([(1,2),(1,2),(2,4),(3,4),(5,4),(4,6),(4,6),(4,6),(6,7),(7,8),(7,8),(8,9),(6,9),(9,10),
        #                        (9,11),(9,11),(10,11),(11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,12),
        #                        (13,16),(14,17),(16,18),(18,19),(18,19),(19,20),(19,21),(1,20),(3,21)])
        self.g = nx.MultiGraph([(1,4),(4,2),(4,5),(4,6),(2,3),(3,5),(6,7),(7,5),(5,8),(8,9),(8,10),(9,10),(10,11),(11,12)])

    def test_calculate_reliability(self):
        print('-------------------------Test ATR-------------------------')
        start = time.time()
        poly1 = atr.calculate_reliability(self.g)
        end = time.time()
        bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
        print('DC basic elapsed time:', end - start)

        start = time.time()
        poly2 = atr.calculate_reliability(self.g, prune=True, modules=['ModuleCycle'])
        end = time.time()
        bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
        print('Dc with prunning time:', end - start)

        self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")
        print(bin_poly2)


class TestModuleTree(unittest.TestCase):

    def setUp(self):
        #self.g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (5, 8), (5, 9), (5, 9)])
        self.g = nx.MultiGraph([(1, 2), (1, 2), (1, 2), (2, 3), (2, 3), (3, 4)])
        self.treemodule = relmodules.ModuleTree(self.g)

    def testModule(self):
        self.assertTrue(self.treemodule.identify(), "MultiTree not properly identified")
        with self.subTest():
            print('-------------------------Test Tree Module-------------------------')

            start = time.time()
            poly1 = atr.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            poly2 = self.treemodule.calculate()
            end = time.time()
            bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('Tree alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")
            print(bin_poly2)


class TestModuleCycle(unittest.TestCase):

    def setUp(self):
        #self.g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1),
        #                        (1, 2), (3, 4), (7, 8), (7, 8)])
        self.g = nx.MultiGraph([(1, 2), (1, 2), (1, 2), (2, 3), (2, 3), (3, 4), (4, 1), (4, 1)])
        self.cyclemodule = relmodules.ModuleCycle(self.g)

    def testModule(self):
        self.assertTrue(self.cyclemodule.identify(), "MultiCycle not properly identified")
        with self.subTest():
            print('-------------------------Test Cycle Module-------------------------')
            start = time.time()
            poly1 = atr.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            poly2 = self.cyclemodule.calculate()
            end = time.time()
            bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('Cycle alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")
            print(bin_poly2)


class TestModuleCake(unittest.TestCase):

    def setUp(self):
        # self.g  = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), (1, 5), (2, 6), (3, 7)])
        self.g = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1), (1, 5), (2, 6), (3, 7), (4, 8)])
        self.cakemodule = relmodules.ModuleCake(self.g)

    def testModule(self):
        self.assertTrue(self.cakemodule.identify(),  "Cake not properly identified")
        with self.subTest():
            print('-------------------------Test Cake Module-------------------------')
            start = time.time()
            poly1 = atr.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            poly2 = self.cakemodule.calculate()
            end = time.time()
            bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('Cake alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")
            print(bin_poly2)

class TestModuleCycleTree(unittest.TestCase):
    def setUp(self):
        #self.g = nx.Graph([(1, 2), (2, 3), (3, 1), (3, 4), (3, 5), (4, 5), (5, 6), (5, 7), (6, 7)])
        self.g = nx.MultiGraph([(1, 2), (1, 3), (2, 3), (3, 4), (3, 6), (4, 5), (5, 6),
                           (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 6)])
        self.cycletreemodule = relmodules.ModuleCycleTree(self.g)

    def testModule(self):
        self.assertTrue(self.cycletreemodule.identify(), "CycleTree not properly identified")
        with self.subTest():
            print('-------------------------Test CycleTree Module-------------------------')
            start = time.time()
            poly1 = atr.calculate_reliability(self.g)
            end = time.time()
            bin_poly1, bin_coeff1 = graphtools.polynomial2binomial(poly1)
            print('DC basic elapsed time:', end - start)

            start = time.time()
            poly2 = self.cycletreemodule.calculate()
            end = time.time()
            bin_poly2, bin_coeff2 = graphtools.polynomial2binomial(poly2)
            print('CycleTree alg. elapsed time:', end - start)

            self.assertEqual(bin_coeff1, bin_coeff2, "Polynomial not correct")
            print(bin_poly2)

# run the test
if __name__ == '__main__':
    unittest.main()
