from search.heuristics import Heuristics
import heapq

class AStar:
    def __init__(self, graph):
        """
        Inicializa o algoritmo A* com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def search(self, start, goal):
        """
        Realiza a busca A* no grafo.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :return: Caminho do nó inicial ao objetivo, se encontrado.
        """
        open_set = []
        heapq.heappush(open_set, (0, start))  # (f_score, nó)
        came_from = {}

        g_score = {node: float('inf') for node in self.graph.nodes}
        g_score[start] = 0

        f_score = {node: float('inf') for node in self.graph.nodes}
        f_score[start] = Heuristics.straight_line_distance(self.graph, start, goal)

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.graph.neighbors(current):
                tentative_g_score = g_score[current] + self.graph[current][neighbor]['weight']

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + Heuristics.straight_line_distance(self.graph, neighbor, goal)

                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

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
