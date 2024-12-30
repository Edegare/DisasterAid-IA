# Arquivo: search/bfs.py

class BFS:
    def __init__(self, graph):
        """
        Inicializa a classe BFS com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def search(self, start, goal):
        """
        Realiza uma busca em largura (BFS) no grafo.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :return: Caminho do nó inicial ao objetivo, se encontrado.
        """
        visited = set()
        queue = [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == goal:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None
