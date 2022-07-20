import networkx as nx
import time

import graphtools

#from modules.reliability_modules import Module
#from modules.module_tree import ModuleTree
#from modules.module_cycle import ModuleCycle
#from modules.module_cake import ModuleCake

from modules import *

from atr import Atr


def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


# pass base class as argument
print(get_all_subclasses(RelModule))