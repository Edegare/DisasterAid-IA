
import math
from queue import Queue

import networkx as nx 
import matplotlib.pyplot as plt  

from Node import Node
from Vehicle import Vehicle

class Graph:
    # Graph representing the network of zones and connections between them.
    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # on add_edge, to do - roads closed, distance
        self.m_h = {} 
        self.m_vehicles = []
