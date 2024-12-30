from search.heuristics import Heuristics
import heapq

class GreedyBestFirstSearch:
    def __init__(self, graph):
        """
        Inicializa a classe Greedy Best-First Search com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def search(self, start, goal):
        """
        Realiza a busca Greedy Best-First Search no grafo.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :return: Caminho do nó inicial ao objetivo, se encontrado.
        """
        visited = set()
        priority_queue = []  # Fila de prioridade (heurística, nó)
        heapq.heappush(priority_queue, (0, start))
        came_from = {}

        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue

            visited.add(current_node)

            # Verificar se atingimos o objetivo
            if current_node == goal:
                return self.reconstruct_path(came_from, current_node)

            # Adicionar vizinhos à fila com suas heurísticas
            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited:
                    heuristic = Heuristics.straight_line_distance(self.graph, neighbor, goal)
                    heapq.heappush(priority_queue, (heuristic, neighbor))
                    came_from[neighbor] = current_node

        return None  # Retorna None se o objetivo não for alcançado

    @staticmethod
    def reconstruct_path(came_from, current):
        """
        Reconstrói o caminho a partir do nó objetivo.

        :param came_from: Dicionário que mapeia cada nó para o nó anterior.
        :param current: Nó objetivo.
        :return: Caminho reconstruído como uma lista de nós.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
