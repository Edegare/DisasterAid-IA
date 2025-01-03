# search/astar.py

from models import Truck, Car, Helicopter
from utils import calculate_vehicle_combination
from utils import heuristic

from itertools import combinations_with_replacement
from geopy.distance import geodesic

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
        Realiza a busca Greedy Best-First Search no grafo considerando apenas a heurística para explorar
        e calcula o custo total do caminho encontrado após o término.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :return: Caminho, custo total (real) e lista de veículos usados.
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

        visited = set()
        priority_queue = []  # Fila de prioridade (heurística, nó atual)
        parent = {start: None}  # Para reconstruir o caminho
        heapq.heappush(priority_queue, (0, start))  # Inicializa com a heurística do nó inicial

        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)

            if current_node == goal:
                # Reconstruir o caminho a partir dos pais
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                path.reverse()

                # Calcular o custo real do caminho percorrido
                total_cost = 0
                for i in range(len(path) - 1):
                    edge_data = self.graph.get_edge_data(path[i], path[i + 1])
                    total_cost += edge_data.get('weight', 1)

                # Calcular a combinação ótima de veículos para atender à demanda
                vehicle_combination = calculate_vehicle_combination(goal_population, vehicles)
                return path, total_cost, vehicle_combination

            if current_node not in visited:
                visited.add(current_node)

                for neighbor in self.graph.neighbors(current_node):
                    if neighbor in visited:
                        continue

                    edge_data = self.graph.get_edge_data(current_node, neighbor)
                    if edge_data.get('closed', False):  # Ignora estradas fechadas
                        continue

                    # Calcula apenas a heurística para o vizinho
                    heuristic_value = self.heuristic(neighbor, goal)

                    # Adiciona o vizinho na fila de prioridade baseado apenas na heurística
                    heapq.heappush(priority_queue, (heuristic_value, neighbor))
                    parent[neighbor] = current_node

        return None, float('inf'), []  # Nenhum caminho encontrado
