# models/graph.py

class Graph:
    def __init__(self):
        """Classe que representa um grafo com adjacências."""
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        """
        Adiciona um nó ao grafo.

        :param node: Instância da classe Node.
        """
        self.nodes[node.id] = node
        self.edges[node.id] = []

    def add_edge(self, from_id, to_id, cost):
        """
        Adiciona uma aresta ao grafo.

        :param from_id: ID do nó de origem.
        :param to_id: ID do nó de destino.
        :param cost: Custo associado à aresta.
        """
        if from_id in self.nodes and to_id in self.nodes:
            self.edges[from_id].append((to_id, cost))
        else:
            raise ValueError("Um ou ambos os nós não existem no grafo.")

    def get_neighbors(self, node_id):
        """
        Obtém os vizinhos de um nó.

        :param node_id: ID do nó.
        :return: Lista de tuplos (vizinho, custo).
        """
        return self.edges.get(node_id, [])

    def __repr__(self):
        return f"Graph(nodes={list(self.nodes.keys())}, edges={self.edges})"