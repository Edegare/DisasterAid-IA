# search/bfs.py

from utils import calculate_vehicle_combination
from models import Truck, Car, Helicopter

from itertools import combinations_with_replacement

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

                # Calcular a combinação ótima de veículos para atender à demanda
                vehicle_combination = calculate_vehicle_combination(goal_population, vehicles)
                return path, cost, vehicle_combination

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    edge_data = self.graph.get_edge_data(node, neighbor)
                    edge_cost = edge_data.get('weight', 1)  # Assumir peso 1 se não especificado

                    new_path = list(path)  # Copiar o caminho atual
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None, float('inf'), []  # Nenhum caminho encontrado

