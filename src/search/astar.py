# search/astar.py

from utils import calculate_vehicle_combination
from utils import straight_line_distance, heuristic
from models import Truck, Car, Helicopter

from itertools import combinations_with_replacement
from geopy.distance import geodesic

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
        Realiza a busca A* no grafo, considerando tanto o custo acumulado quanto a heurística,
        e calcula o custo total do caminho encontrado após o término.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :return: Caminho, custo total e lista de veículos usados.
        """
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            raise ValueError(f"O nó {start} ou {goal} não está no grafo.")

        # Obter a população da zona de ajuda
        goal_population = self.graph.nodes[goal].get('population', 0)

        # Obter a lista de veículos disponíveis na zona de suporte
        vehicles = self.graph.nodes[start].get('vehicles', [])
        if isinstance(vehicles, list) and vehicles and isinstance(vehicles[0], dict):
            vehicles = [
                Truck(v['id']) if v['type'] == 'truck' else
                Car(v['id']) if v['type'] == 'car' else
                Helicopter(v['id']) if v['type'] == 'helicopter' else None
                for v in vehicles
            ]
            vehicles = [v for v in vehicles if v is not None]

        open_set = []
        heapq.heappush(open_set, (0, start))  # (f_score, nó atual)
        came_from = {}

        g_score = {node: float('inf') for node in self.graph.nodes}
        g_score[start] = 0

        f_score = {node: float('inf') for node in self.graph.nodes}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current_node = heapq.heappop(open_set)

            if current_node == goal:
                # Reconstruir o caminho a partir dos pais
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = came_from.get(current_node, None)
                path.reverse()

                # Calcular o custo real do caminho percorrido
                total_cost = 0
                for i in range(len(path) - 1):
                    edge_data = self.graph.get_edge_data(path[i], path[i + 1])
                    total_cost += edge_data.get('weight', 1)

                # Calcular a combinação ótima de veículos para atender à demanda
                vehicle_combination = calculate_vehicle_combination(goal_population, vehicles)
                return path, total_cost, vehicle_combination

            for neighbor in self.graph.neighbors(current_node):
                edge_data = self.graph.get_edge_data(current_node, neighbor)
                if edge_data.get('closed', False):  # Ignora estradas fechadas
                    continue
                tentative_g_score = g_score[current_node] + edge_data.get('weight', 1)

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)

                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None, float('inf'), []  # Nenhum caminho encontrado
