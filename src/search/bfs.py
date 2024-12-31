# Arquivo: search/bfs.py

class BFS:
    def __init__(self, graph):
        """
        Inicializa a classe BFS com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def search(self, start, goal):
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            raise ValueError(f"O nó {start} ou {goal} não está no grafo.")

        visited = set()
        queue = [[start]]  # Cada entrada é [lista de nós]

        while queue:
            path = queue.pop(0)  # Remove o primeiro caminho da fila
            node = path[-1]  # Último nó no caminho atual

            if node == goal:
                # Calcula o custo total do caminho
                cost = sum(self.graph.get_edge_data(path[i], path[i + 1])['weight']
                        for i in range(len(path) - 1))
                return path, cost

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    edge_data = self.graph.get_edge_data(node, neighbor)
                    edge_cost = edge_data.get('weight', 1)  # Assumir peso 1 se não especificado

                    new_path = list(path)  # Copiar o caminho atual
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None, float('inf')  # Nenhum caminho encontrado

