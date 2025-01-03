# search/dfs.py

from models import Truck, Car, Helicopter 
from utils import calculate_vehicle_combination

class DFS:
    def __init__(self, graph):
        """
        Inicializa a classe DFS com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def search(self, start, goal):
        """
        Realiza uma busca em profundidade (DFS) no grafo.

        :param start: Nó inicial (zona de suporte).
        :param goal: Nó objetivo (zona que precisa de ajuda).
        :return: Caminho, custo total e combinação de veículos utilizados.
        """
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            raise ValueError(f"O nó {start} ou {goal} não está no grafo.")

        # Obter a população do nó objetivo e os veículos disponíveis no nó inicial
        goal_population = self.graph.nodes[goal].get("population", 0)
        vehicles = self.graph.nodes[start].get("vehicles", [])

        # Inicializar os veículos disponíveis
        if isinstance(vehicles, list) and vehicles and isinstance(vehicles[0], dict):
                    vehicles = [
                        Truck(v['id']) if v['type'] == 'truck' else
                        Car(v['id']) if v['type'] == 'car' else
                        Helicopter(v['id']) if v['type'] == 'helicopter' else None
                        for v in vehicles
                    ]
                    vehicles = [v for v in vehicles if v is not None]

        # Inicializar estruturas para DFS
        visited = set()
        stack = [[start]]

        while stack:
            path = stack.pop()
            current_node = path[-1]

            # Verifica se atingiu o objetivo
            if current_node == goal:
                # Calcula o custo total do caminho
                total_cost = sum(
                    self.graph.get_edge_data(path[i], path[i + 1]).get("weight", 1)
                    for i in range(len(path) - 1)
                )
                # Calcular a combinação ótima de veículos para atender à demanda
                vehicle_combination = calculate_vehicle_combination(goal_population, vehicles)
                return path, total_cost, vehicle_combination

            if current_node not in visited:
                visited.add(current_node)
                for neighbor in self.graph.neighbors(current_node):
                    edge_data = self.graph.get_edge_data(current_node, neighbor)
                    if edge_data.get("closed", False):  # Ignorar estradas fechadas
                        continue
                    new_path = path + [neighbor]
                    stack.append(new_path)

        return None, float("inf"), []  # Falha em encontrar o caminho
