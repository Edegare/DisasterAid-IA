
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
        self.m_graph = {}  # edge will have a cost (distance) (to do after - check if road closed or not for each pair of zones)


    #############
    # Graph as string
    #############
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + '\n'
            return out

    ################################
    # Node by a name
    ################################

    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
            else:
                return None

    ##############################
    # Print edges
    ############################

    def print_edges (self):
        list = ""
        list2 = self.m_graph.keys()
        for node in list2:
            for (node2, cost) in self.m_graph[node]:
                list = list + node + " ->" + node2 + " cost:" + str(cost) + "\n"
        return list

    #############################
    # Add edge to a graph
    #############################

    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if (n1 not in self.m_nodes):
            n1_id = len(self.m_nodes)  # numeração sequencial
            n1.setId(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []
        else:
            n1 = self.get_node_by_name(node1)

        if (n2 not in self.m_nodes):
            n2_id = len(self.m_nodes)  # numeração sequencial
            n2.setId(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []
        else:
            n2 = self.get_node_by_name(node2)

        self.m_graph[node1].append((node2, weight)) 

        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))


    #############################
    # Graph nodes
    ############################

    def getNodes(self):
        return self.m_nodes

    ###############################
    # Edge Cost
    ################################

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  
        for (node, cost) in a:
            if node == node2:
                custoT = cost

        return custoT

    ##############################
    #  Cost of a path
    ###############################

    def cost_calc (self, path):
        # path - list of nodes
        test = path
        cost = 0
        i = 0
        while i + 1 < len(test):
            cost = cost + self.get_arc_cost(test[i], test[i + 1])
            #print(test[i])
            i = i + 1
        return cost
    
    ###########################
    # Draw graph
    #########################

    def draw(self):
        # create nodes list 
        list_v = self.m_nodes
        list_a = []
        g = nx.Graph()
        for node in list_v:
            n = node.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                list = (n, adjacente)
                # list_a.append(list)
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def createTest1(self):
        self.add_edge("elvas", "borba", 15)
        self.add_edge("borba", "estremoz", 15)
        self.add_edge("estremoz", "evora", 40)
        self.add_edge("evora", "montemor", 20)
        self.add_edge("montemor", "vendasnovas", 15)
        self.add_edge("vendasnovas", "lisboa", 50)
        self.add_edge("elvas", "arraiolos", 50)
        self.add_edge("arraiolos", "alcacer", 90)
        self.add_edge("alcacer", "palmela", 35)
        self.add_edge("palmela", "almada", 25)
        self.add_edge("palmela", "barreiro", 25)
        self.add_edge("barreiro", "palmela", 30)
        self.add_edge("almada", "lisboa", 15)
        self.add_edge("elvas", "alandroal", 40)
        self.add_edge("alandroal", "redondo", 25)
        self.add_edge("redondo", "monsaraz", 30)
        self.add_edge("monsaraz", "barreiro", 120)
        self.add_edge("barreiro", "baixadabanheira", 5)
        self.add_edge("baixadabanheira", "moita", 7)
        self.add_edge("moita", "alcochete", 20)
        self.add_edge("alcochete", "lisboa", 20)